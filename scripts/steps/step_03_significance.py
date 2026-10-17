#!/usr/bin/env python3
"""
Gate 3R: Genuine Monte Carlo Calibration

This script calibrates the significance of the H-free likelihood gain using
actual True-D Monte Carlo simulations. The loop generates flux from the
fitted true-D model, draws noise from the frozen noise model, and reruns
the complete M_D and multi-start M_Hfree search for each realization.

It also explicitly computes leave-one-coadd and leave-one-transition fits.

Supports multiple sightlines via per-sightline JSON configs in
configs/sightlines/. Defaults to Q1009+2956 for backward compatibility.
"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))
import json

import numpy as np

from scripts.utils.logger import print_status, setup_step_logger

np.seterr(all="ignore")
import multiprocessing
from pathlib import Path

from scipy.optimize import minimize
from scipy.stats import t as student_t

project_root = Path(__file__).resolve().parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from scripts.lib.residual_engine import likelihood_residuals
from scripts.lib.model_builder import build_model_components
from scripts.lib.model_parser import ParameterManager, parse_vpfit_ties
from scripts.lib.physical_rt_engine import RadiativeTransferEngine
from scripts.lib.residual_engine import (
    build_frozen_cache,
    compute_residuals,
    compute_residuals_fast,
    split_frozen_candidate,
)
from scripts.lib.sightline_config import load_sightline_config, SightlineConfigError


# ---------------------------------------------------------------------------
# Multiprocessing initializer: set shared data once per worker process to
# avoid pickling the same ~1 MB of data 1000 times (once per task).  With
# the spawn start method (default on macOS), each worker process would
# otherwise receive a fresh copy of base_fluxes, data_blocks, frozen_cache,
# etc. for every single simulation.  The initializer sends it once per
# worker (15 times) instead of once per task (1000 times).
# ---------------------------------------------------------------------------
_worker_shared = None

def _init_worker(shared_data):
    global _worker_shared
    _worker_shared = shared_data

def _run_worker(seed_and_extras):
    """Run a single simulation using globally shared data."""
    seed, starts_H, bounds_D, bounds_H, cfg_multistart_D, d_vel, parent_win, canonical_parent_idx = seed_and_extras
    return run_simulation(
        seed,
        _worker_shared['base_fluxes'],
        _worker_shared['data_blocks'],
        _worker_shared['noise_cfg'],
        _worker_shared['pm'],
        _worker_shared['z_abs_ref'],
        _worker_shared['c_kms'],
        _worker_shared['theta_shared_base'],
        _worker_shared['engine'],
        starts_H,
        bounds_D,
        bounds_H,
        _worker_shared['frozen_grouped'],
        _worker_shared['frozen_cache'],
        cfg_multistart_D,
        d_vel,
        parent_win,
        canonical_parent_idx,
    )


def run_simulation(
    seed,
    base_fluxes,
    data_blocks,
    noise_cfg,
    pm,
    z_abs_ref,
    c_kms,
    theta_shared_base,
    engine,
    starts_H,
    bounds_D,
    bounds_H,
    frozen_grouped,
    frozen_cache,
    cfg_multistart_D,
    d_velocity_offset_kms,
    parent_window_kms,
    canonical_parent_idx=0,
):
    rng = np.random.default_rng(seed)

    # Precompute Student-t logpdf constants (avoids scipy overhead per call).
    # logpdf(x, nu, loc, scale) = C0 - ((nu+1)/2) * log(1 + (1/nu) * ((x-loc)/scale)^2)
    # where C0 = log(Γ((nu+1)/2)) - log(Γ(nu/2)) - 0.5*log(nu*π) - log(scale)
    from scipy.special import gammaln
    _nu = noise_cfg["nu"]
    _loc = noise_cfg["location"]
    _scale = noise_cfg["scale"]
    _logpdf_const = (
        gammaln((_nu + 1) / 2.0)
        - gammaln(_nu / 2.0)
        - 0.5 * np.log(_nu * np.pi)
        - np.log(_scale)
    )
    _logpdf_alpha = (_nu + 1) / 2.0
    _logpdf_inv_nu = 1.0 / _nu

    def _fast_logpdf_sum(residuals):
        """Sum of Student-t logpdf over every finite residual on the input mask."""
        v = likelihood_residuals(residuals)
        z = (v - _loc) / _scale
        return _logpdf_const * len(v) - _logpdf_alpha * np.sum(
            np.log1p(_logpdf_inv_nu * z * z)
        )

    # 1. Generate noisy flux realization
    sim_blocks = []
    for i, block in enumerate(data_blocks):
        err = block["err"]
        noise = student_t.rvs(
            df=noise_cfg["nu"],
            loc=0.0,
            scale=err * noise_cfg["scale"],
            random_state=rng,
        )
        sim_flux = base_fluxes[i] + noise

        sim_blocks.append(
            {
                "wave": block["wave"],
                "flux": sim_flux,
                "err": block["err"],
                "vsig": block["vsig"],
                "w_min": block["w_min"],
                "w_max": block["w_max"],
                "coadd": block["coadd"],
            }
        )

    def make_obj_parent(model_name, blocks, parent_idx=0):
        def obj(p):
            grouped = build_model_components(
                model_name,
                theta_shared_base,
                p,
                pm,
                z_abs_ref,
                c_kms,
                parent_idx=parent_idx,
                d_velocity_offset_kms=d_velocity_offset_kms,
                parent_window_kms=parent_window_kms,
            )
            # Frozen scaffold contributes an identical optical depth on every
            # evaluation, so only the candidate components are recomputed here.
            cand = split_frozen_candidate(grouped, frozen_grouped)
            res = compute_residuals_fast(cand, blocks, engine, frozen_cache)
            ll = _fast_logpdf_sum(res)
            return -float(ll)

        return obj

    # 2. Fit M_Dfree across all eligible parents to find the maximum possible D likelihood
    # Only parents within the absorber velocity window AND column density threshold
    # are considered (matching the observed scan criteria).
    comps = pm.reconstruct(theta_shared_base)
    h_comps = [c for c in comps if c["ion"] == "H_I"]
    parent_window_kms = parent_window_kms
    logN_H_max = max(c["logN"] for c in h_comps)
    logN_H_min = logN_H_max - 2.0  # Match observed scan: max - 2.0 dex
    valid_parents = []
    for j, c in enumerate(h_comps):
        v = c_kms * (c["z"] - z_abs_ref) / (1.0 + z_abs_ref)
        if abs(v) <= parent_window_kms and c["logN"] >= logN_H_min:
            valid_parents.append(j)
    best_ll_D = -np.inf
    ll_D_canonical = -np.inf  # Track D at canonical (auto-detected) parent for fair standard
    res_D_success = False

    # The data was generated using opt_D_obs on the canonical parent
    # So opt_D_obs should be passed into the simulation to use as a strong prior start
    opt_D_obs = starts_H["opt_D_obs"]  # Extract from a dict we'll pass
    actual_starts_H = starts_H["starts"]

    # --- Two-phase parent scan for efficiency ---
    # Phase 1: Quick 1-start scan of all parents to find the best one
    # Phase 2: Full multistart only on the best parent and canonical parent
    # This reduces 14×9=126 D fits to 14×1 + 2×9 = 32 D fits (~4x speedup)

    quick_start = opt_D_obs  # Use true generating params as the quick start

    # Phase 1: Quick scan
    parent_lls = {}
    for j in valid_parents:
        obj_D = make_obj_parent("M_Dfree", sim_blocks, j)
        res_D = minimize(obj_D, quick_start, method="L-BFGS-B", bounds=bounds_D)
        parent_lls[j] = -res_D.fun
        if j == canonical_parent_idx:
            ll_D_canonical_quick = -res_D.fun
            res_D_success = res_D.success

    # Find best parent from quick scan
    best_parent = max(parent_lls, key=parent_lls.get)

    # Phase 2: Full multistart on best parent and canonical parent
    parents_to_refine = set([best_parent, canonical_parent_idx])
    best_ll_D = -np.inf
    ll_D_canonical = -np.inf

    for j in parents_to_refine:
        obj_D = make_obj_parent("M_Dfree", sim_blocks, j)
        starts_D = [list(s) for s in cfg_multistart_D]
        if j == canonical_parent_idx:
            starts_D.insert(0, opt_D_obs)

        best_local_ll_D = -np.inf
        local_success = False
        for x0 in starts_D:
            res_D = minimize(obj_D, x0, method="L-BFGS-B", bounds=bounds_D)
            if -res_D.fun > best_local_ll_D:
                best_local_ll_D = -res_D.fun
                local_success = res_D.success

        if j == canonical_parent_idx:
            ll_D_canonical = best_local_ll_D

        if best_local_ll_D > best_ll_D:
            best_ll_D = best_local_ll_D
            res_D_success = local_success

    # 3. Fit M_Hfree (multi-start)
    # Note: M_H has free v_H, so parent_idx does not affect the H fit.
    # The H interloper velocity is unrestricted, making the H model
    # parent-independent. This ensures the T_parent comparison is fair:
    # D is best-of-parents (tied to a parent by v_D = parent_v - 81.6),
    # while H is fully free (no parent dependence).
    # 3. Fit M_Hfree (multi-start, full grid for MC fairness)
    # The MC H fits must use the same multistart grid as the observed fit
    # (step_02).  Using a reduced grid risks missing a better H optimum,
    # which lowers LL_H, lowers T_sim, and makes p-values anti-conservative
    # (too small).  All configured starts are used.
    obj_H = make_obj_parent("M_H", sim_blocks)
    best_ll_H = -np.inf
    h_success = False

    # Use all configured starts (same as step_02 observed fit)
    mc_starts_H = actual_starts_H

    for x0 in mc_starts_H:
        res_H = minimize(obj_H, x0, method="L-BFGS-B", bounds=bounds_H)
        if -res_H.fun > best_ll_H:
            best_ll_H = -res_H.fun
            h_success = res_H.success

    # T_parent: Hfree vs best possible parent for D (fair: H is parent-free)
    T_parent = 2.0 * (best_ll_H - best_ll_D)

    # T_standard: Hfree vs D at canonical (auto-detected) parent
    # (fair: matches obs T_obs which also uses the auto-detected parent for D).
    # This eliminates the asymmetry where sim D could cherry-pick the best
    # parent while obs D is locked to the canonical parent.
    T_standard = 2.0 * (best_ll_H - ll_D_canonical)

    return {
        "simulation_id": seed,
        "seed": seed,
        "logL_D_max": best_ll_D,
        "logL_D_canonical": ll_D_canonical,
        "logL_Hfree": best_ll_H,
        "T_parent": T_parent,
        "T_standard": T_standard,
        "converged_D": res_D_success,
        "converged_H": h_success,
    }


def compute_physical_parent_window(pm, theta_shared_base, z_abs_ref, c_kms, factor=3.0):
    """Compute a physically motivated parent window: ±factor × largest b-value
    of H I components within ±500 km/s of the absorber systemic velocity.

    This replaces the arbitrary ±1000 km/s fixed window with a window scaled
    to the velocity structure of the main absorber complex.
    """
    comps = pm.reconstruct(theta_shared_base)
    h_comps = [c for c in comps if c['ion'] == 'H_I']
    b_values = []
    for c in h_comps:
        v = c_kms * (c['z'] - z_abs_ref) / (1.0 + z_abs_ref)
        if abs(v) <= 500.0:  # main complex definition
            b_values.append(c['b'])
    if not b_values:
        # Fallback: use all H I components
        b_values = [c['b'] for c in h_comps]
    b_max = max(b_values)
    window = factor * b_max
    return window, b_max, len(b_values)


def run_gate3(sightline=None, parent_window_mode='fixed', n_sims=None, workers=12):
    setup_step_logger(Path(__file__).stem)

    # Load per-sightline configuration
    try:
        cfg = load_sightline_config(sightline)
    except SightlineConfigError as e:
        print_status(f"Sightline config error: {e}", "ERROR")
        raise

    sightline_id = cfg["sightline_id"]
    output_prefix = cfg.get("output_prefix", "gate")

    print_status(f"=== GATE 3R: GENUINE MONTE CARLO CALIBRATION ({sightline_id}) ===", "SUCCESS")

    if not cfg["_data_available"]:
        print_status(
            f"Data not yet ingested for sightline '{sightline_id}'. Skipping.",
            "ERROR",
        )
        return

    manifest_path = Path(cfg["_manifest_abs"])
    vpfit_path = Path(cfg["_vpfit_abs"])
    noise_model_path = Path(cfg["_noise_abs"])

    with open(manifest_path, "r") as f:
        manifest = json.load(f)
    with open(noise_model_path, "r") as f:
        noise_cfg = json.load(f)

    z_abs_ref = cfg.get("z_abs", manifest["z_abs"])
    c_kms = 299792.458

    components_raw, regions = parse_vpfit_ties(vpfit_path)
    pm = ParameterManager(components_raw)
    engine = RadiativeTransferEngine(z_abs=z_abs_ref)

    data_blocks = []
    for r in regions:
        coadd = r["filename"]
        if coadd not in manifest["coadds"]:
            continue
        for chunk in manifest["coadds"][coadd]:
            wave, flux, err = (
                np.array(chunk["wave"]),
                np.array(chunk["flux"]),
                np.array(chunk["err"]),
            )
            mask = (
                (np.isfinite(flux))
                & (np.isfinite(err))
                & (err > 0)
                & (wave >= r["w_min"])
                & (wave <= r["w_max"])
            )
            if np.sum(mask) == 0:
                continue
            data_blocks.append(
                {
                    "wave": wave[mask],
                    "flux": flux[mask],
                    "err": err[mask],
                    "vsig": r["vsig"],
                    "w_min": r["w_min"],
                    "w_max": r["w_max"],
                    "coadd": coadd,
                }
            )

    gate2_ledger_path = project_root / "results" / f"{output_prefix}2_parameter_ledger.json"
    with open(gate2_ledger_path, "r") as f:
        g2 = json.load(f)

    ll_D_max_obs = g2["results"]["M_Dfree"]["LL"]
    ll_H_max_obs = g2["results"]["M_Hfree"]["LL"]
    T_obs = 2.0 * (ll_H_max_obs - ll_D_max_obs)

    # Support both old (params) and new (cand_params) ledger formats
    if "cand_params" in g2["results"]["M_Dfree"]:
        opt_D_obs = g2["results"]["M_Dfree"]["cand_params"]
        # Use profiled shared params from M_Dfree fit as the "truth" for MC
        theta_shared_base = np.array(g2["results"]["M_Dfree"]["shared_params"])
        print_status(f"Using profiled shared params from Gate 2 (n={len(theta_shared_base)})", "PROCESS")
    else:
        opt_D_obs = g2["results"]["M_Dfree"]["params"]
        # Fall back to VPFIT init values
        theta_shared_base = np.array(pm.theta_init)
        print_status(f"Using VPFIT init shared params (legacy format)", "PROCESS")

    # Compute parent window: fixed (±1000 km/s) or physical (±3× largest b-value)
    if parent_window_mode == 'physical':
        phys_window, b_max, n_complex = compute_physical_parent_window(
            pm, theta_shared_base, z_abs_ref, c_kms, factor=3.0
        )
        cfg["parent_window_kms"] = phys_window
        print_status(
            f"Physical parent window: ±{phys_window:.1f} km/s "
            f"(3 × b_max={b_max:.1f} km/s, {n_complex} components in main complex)",
            "PROCESS"
        )
    else:
        print_status(
            f"Fixed parent window: ±{cfg['parent_window_kms']:.0f} km/s",
            "PROCESS"
        )

    # Pre-calculate base True-D model fluxes
    # Must match the full model used in compute_residuals: all 7 Lyman transitions,
    # all metal ions, and instrumental convolution. The continuum polynomial is
    # fit (not fixed) in the residual engine, so the absorption
    # template exp(-tau) convolved with the instrumental profile. The continuum
    # is implicitly 1.0 (the residual engine will fit it from the noisy data).
    print_status("Pre-calculating base True-D model fluxes...", "PROCESS")
    grouped_D = build_model_components(
        "M_Dfree", theta_shared_base, opt_D_obs, pm, z_abs_ref, c_kms,
        d_velocity_offset_kms=cfg["d_velocity_offset_kms"],
        parent_window_kms=cfg["parent_window_kms"],
    )

    # Auto-detect the canonical parent index (among H I with a D counterpart,
    # pick the one with the highest logN_H — strongest D signal).  This must
    # match the logic in build_model_components().  The simulation must use
    # the same parent for the "fair standard" comparison to be valid.
    comps_for_parent = pm.reconstruct(theta_shared_base)
    d_zs = set(round(c["z"], 10) for c in comps_for_parent if c["ion"] == "D_I")
    canonical_parent_idx = 0
    _h_count = 0
    _best_logN = float("-inf")
    for c in comps_for_parent:
        if c["ion"] == "H_I":
            if round(c["z"], 10) in d_zs:
                if c["logN"] > _best_logN:
                    _best_logN = c["logN"]
                    canonical_parent_idx = _h_count
            _h_count += 1
    print_status(f"Canonical parent index (auto-detected): {canonical_parent_idx}", "PROCESS")
    lyman_transitions = [
        "HI_Lya", "HI_Lyb", "HI_Lyg", "HI_Lyd", "HI_Lye",
        "HI_Ly6", "HI_Ly7", "HI_Ly8", "HI_Ly9", "HI_Ly10",
        "HI_Ly11", "HI_Ly12", "HI_Ly13", "HI_Ly14", "HI_Ly21",
    ]
    base_fluxes = []
    for block in data_blocks:
        tau_tot = np.zeros_like(block["wave"])
        if grouped_D["H_I"]:
            tau_tot += engine.compute_optical_depth(
                block["wave"], lyman_transitions, grouped_D["H_I"]
            )
        if grouped_D["D_I"]:
            tau_tot += engine.compute_optical_depth(
                block["wave"], lyman_transitions, grouped_D["D_I"]
            )
        if grouped_D["C_IV"]:
            tau_tot += engine.compute_optical_depth(
                block["wave"], ["CIV_1548", "CIV_1550"], grouped_D["C_IV"]
            )
        if grouped_D["C_III"]:
            tau_tot += engine.compute_optical_depth(
                block["wave"], ["CIII_977"], grouped_D["C_III"]
            )
        if grouped_D["C_II"]:
            tau_tot += engine.compute_optical_depth(
                block["wave"], ["CII_1334"], grouped_D["C_II"]
            )
        if grouped_D["Si_IV"]:
            tau_tot += engine.compute_optical_depth(
                block["wave"], ["SiIV_1393", "SiIV_1402"], grouped_D["Si_IV"]
            )
        # Convolve with instrumental profile (matches residual_engine)
        flux = engine.apply_convolution(
            np.exp(-tau_tot), block["wave"], block["vsig"]
        )
        base_fluxes.append(flux)

    # Support both old (flat) and new (shared+cand) bounds formats
    # Note: bounds keys may be "M_H" or "M_Hfree" depending on ledger version
    bounds_H_key = "M_Hfree" if "M_Hfree" in g2["bounds"] else "M_H"
    if "cand" in g2["bounds"]["M_Dfree"]:
        bounds_D = [tuple(b) for b in g2["bounds"]["M_Dfree"]["cand"]]
        bounds_H = [tuple(b) for b in g2["bounds"][bounds_H_key]["cand"]]
    else:
        bounds_D = g2["bounds"]["M_Dfree"]
        bounds_H = g2["bounds"][bounds_H_key]
    starts_H_list = cfg["multistart"]["M_Hfree"]
    starts_H = {"starts": starts_H_list, "opt_D_obs": opt_D_obs}

    # Frozen-scaffold optical depth cache. The shared architecture is identical
    # under every hypothesis and identical between the observed and simulated
    # spectra (which share wave, err and region bounds), so this is computed once
    # and reused for every likelihood evaluation in this step.
    frozen_grouped = build_model_components(
        "M_NULL", theta_shared_base, None, pm, z_abs_ref, c_kms,
        d_velocity_offset_kms=cfg["d_velocity_offset_kms"],
        parent_window_kms=cfg["parent_window_kms"],
    )
    frozen_cache = build_frozen_cache(frozen_grouped, data_blocks, engine)
    print_status(
        f"Frozen-scaffold cache built for {len(frozen_cache)} blocks "
        f"({len(frozen_grouped['H_I'])} shared H I + metals cached)",
        "PROCESS",
    )

    # Precompute Student-t logpdf constants for the observed-data objectives.
    from scipy.special import gammaln as _gammaln
    _nu_obs = noise_cfg["nu"]
    _loc_obs = noise_cfg["location"]
    _scale_obs = noise_cfg["scale"]
    _logpdf_const_obs = (
        _gammaln((_nu_obs + 1) / 2.0)
        - _gammaln(_nu_obs / 2.0)
        - 0.5 * np.log(_nu_obs * np.pi)
        - np.log(_scale_obs)
    )
    _logpdf_alpha_obs = (_nu_obs + 1) / 2.0
    _logpdf_inv_nu_obs = 1.0 / _nu_obs

    def _fast_logpdf_sum_obs(residuals):
        """Sum of Student-t logpdf for the observed-data residuals."""
        v = likelihood_residuals(residuals)
        z = (v - _loc_obs) / _scale_obs
        return _logpdf_const_obs * len(v) - _logpdf_alpha_obs * np.sum(
            np.log1p(_logpdf_inv_nu_obs * z * z)
        )

    # Compute observed parent reassignment T (best parent for D) before MC loop
    # Also builds the parent_reassignment ledger for later use
    print_status("\n--- Computing observed parent reassignment T ---", "TITLE")
    comps_obs = pm.reconstruct(theta_shared_base)
    h_comps_obs = [c for c in comps_obs if c["ion"] == "H_I"]

    # Restrict parent reassignment to H I components within the SAME absorber
    # system. Components at very different redshifts (v ~ -47000 to -74000 km/s)
    # belong to unrelated absorber systems along the line of sight; tying D to
    # them places the D absorption at a completely different wavelength, where
    # it fits unrelated residuals — a physically meaningless comparison.
    #
    # Additionally, require logN_H >= logN_H_max - parent_logN_window_dex
    # (default 2.0 dex).  Parents more than 2 dex below the strongest H I
    # component produce D absorption (logN_D = logN_H + log(D/H)) below the
    # detection threshold, making the parent reassignment test degenerate:
    # the D model fits nearly as well as the H model simply because the D
    # absorption is too weak to matter, not because H genuinely explains
    # the feature.  Restricting to physically meaningful parents prevents
    # this degeneracy from inflating p_parent.
    parent_window_kms = cfg["parent_window_kms"]  # ±window of absorber systemic
    parent_logN_window_dex = cfg.get("parent_logN_window_dex", 2.0)
    logN_H_max = max(c["logN"] for c in h_comps_obs)
    logN_H_min = logN_H_max - parent_logN_window_dex
    valid_parent_indices = []
    for j, c in enumerate(h_comps_obs):
        v = c_kms * (c["z"] - z_abs_ref) / (1.0 + z_abs_ref)
        if abs(v) <= parent_window_kms and c["logN"] >= logN_H_min:
            valid_parent_indices.append(j)
    print_status(
        f"Parent reassignment window: ±{parent_window_kms:.0f} km/s, "
        f"logN_H >= {logN_H_min:.2f} (max={logN_H_max:.2f} - {parent_logN_window_dex:.1f} dex) → "
        f"{len(valid_parent_indices)}/{len(h_comps_obs)} H I components eligible",
        "PROCESS",
    )

    T_obs_parent_best = np.inf
    parent_ledger = []
    for j in valid_parent_indices:
        def _obj_d_parent(p, _j=j):
            grouped = build_model_components(
                "M_Dfree", theta_shared_base, p, pm, z_abs_ref, c_kms, parent_idx=_j,
                d_velocity_offset_kms=cfg["d_velocity_offset_kms"],
                parent_window_kms=cfg["parent_window_kms"],
            )
            cand = split_frozen_candidate(grouped, frozen_grouped)
            res = compute_residuals_fast(cand, data_blocks, engine, frozen_cache)
            return -float(_fast_logpdf_sum_obs(res))
        starts_D_obs = [list(s) for s in cfg["multistart"]["M_Dfree"]]
        best_ll_D_parent = -np.inf
        for x0 in starts_D_obs:
            rD = minimize(_obj_d_parent, x0, method="L-BFGS-B", bounds=bounds_D)
            if -rD.fun > best_ll_D_parent:
                best_ll_D_parent = -rD.fun
        t_p = 2.0 * (ll_H_max_obs - best_ll_D_parent)
        parent_ledger.append(
            {"parent_idx": j, "LL_D": best_ll_D_parent, "LL_H": ll_H_max_obs, "T": t_p}
        )
        if t_p < T_obs_parent_best:
            T_obs_parent_best = t_p
        print_status(f"  Parent {j}: LL_D = {best_ll_D_parent:.2f}, T = {t_p:.2f}", "PROCESS")
    print_status(f"Observed T_parent_best = {T_obs_parent_best:.2f}", "PROCESS")

    N_sims = n_sims if n_sims is not None else cfg.get("monte_carlo", {}).get("n_sims", 1000)
    seed_base = cfg.get("monte_carlo", {}).get("seed_base", 42)
    print_status(
        f"\n--- Running True-D Monte Carlo Simulations ({N_sims} realizations) ---",
        "TITLE",
    )

    pool_args = []
    # Read D multistart starts from config
    cfg_multistart_D = cfg["multistart"]["M_Dfree"]

    # Shared data sent once per worker via initializer (not per task)
    shared_data = {
        'base_fluxes': base_fluxes,
        'data_blocks': data_blocks,
        'noise_cfg': noise_cfg,
        'pm': pm,
        'z_abs_ref': z_abs_ref,
        'c_kms': c_kms,
        'theta_shared_base': theta_shared_base,
        'engine': engine,
        'frozen_grouped': frozen_grouped,
        'frozen_cache': frozen_cache,
    }

    # Per-task args: only the seed and small per-sightline config values
    for i in range(N_sims):
        seed = seed_base + i
        pool_args.append(
            (
                seed,
                starts_H,
                bounds_D,
                bounds_H,
                cfg_multistart_D,
                cfg["d_velocity_offset_kms"],
                cfg["parent_window_kms"],
                canonical_parent_idx,
            )
        )

    results_ledger = []
    exceedances_standard = 0      # Legacy: sim D best-of-parents vs obs D parent-0 (inflated)
    exceedances_standard_fair = 0  # Fair standard: D locked to parent 0 in sims
    exceedances_parent = 0

    # Use multiprocessing with initializer to avoid re-pickling shared data
    # Use fork start method to avoid re-importing modules per worker (macOS default is spawn)
    n_workers = min(workers, multiprocessing.cpu_count(), N_sims)
    ctx = multiprocessing.get_context('fork')
    with ctx.Pool(
        processes=n_workers,
        initializer=_init_worker,
        initargs=(shared_data,),
    ) as pool:
        for i, res in enumerate(pool.imap_unordered(_run_worker, pool_args)):
            results_ledger.append(res)
            # Legacy: sim D best-of-parents vs obs D parent-0 (inflated)
            if res["T_parent"] >= T_obs:
                exceedances_standard += 1
            # Fair standard: sim D at parent 0 vs obs D at parent 0
            if res.get("T_standard", -np.inf) >= T_obs:
                exceedances_standard_fair += 1
            # Parent: sim D best-of-parents vs obs T_parent_best (fair: H is parent-free)
            if res["T_parent"] >= T_obs_parent_best:
                exceedances_parent += 1
            if (i + 1) % 10 == 0:
                print_status(
                    f"Completed {i+1}/{N_sims} simulations. Fair standard exceedances (>=T_obs): {exceedances_standard_fair}, Parent exceedances (>={T_obs_parent_best:.2f}): {exceedances_parent}",
                    "PROCESS",
                )

    p_add_one_standard_fair = (exceedances_standard_fair + 1) / (N_sims + 1)
    p_add_one_parent = (exceedances_parent + 1) / (N_sims + 1)

    # Compute exact Clopper-Pearson 95% upper bounds for both statistics.
    # The standard one-sided Clopper-Pearson upper bound is:
    #   p_upper = Beta^{-1}(1-alpha, k+1, n-k)
    from scipy.stats import beta as beta_dist
    binom_95_upper_standard = float(
        beta_dist.ppf(0.95, exceedances_standard_fair + 1, N_sims - exceedances_standard_fair)
    )
    binom_95_upper_parent = float(
        beta_dist.ppf(0.95, exceedances_parent + 1, N_sims - exceedances_parent)
    )
    # Legacy field name (kept for backward compatibility with existing ledgers):
    # stores the standard-statistic upper bound.
    binom_95_upper = binom_95_upper_standard

    print_status(f"\nObserved T_obs (standard, canonical parent {canonical_parent_idx}) = {T_obs:.2f}", "PROCESS")
    print_status(f"Observed T_obs (best parent) = {T_obs_parent_best:.2f}", "PROCESS")
    print_status(f"Exceedances (fair standard, T_sim_standard >= {T_obs:.2f}): {exceedances_standard_fair}", "PROCESS")
    print_status(f"Calibrated p_add_one (fair standard) = {p_add_one_standard_fair:.5f}", "PROCESS")
    print_status(f"Exceedances (parent, T_sim >= {T_obs_parent_best:.2f}): {exceedances_parent}", "PROCESS")
    print_status(
        f"Calibrated p_add_one for parent reassignment = {p_add_one_parent:.5f}",
        "PROCESS",
    )

    print_status("\n--- Genuine Leave-One-Out Robustness Constraints ---", "TITLE")
    loo_ledger = []

    def eval_loo_models(b_mask):
        subset = [b for idx, b in enumerate(data_blocks) if b_mask[idx]]
        # Leave-one-out removes whole blocks, so the per-block frozen cache is
        # still valid; take the matching subset.
        subset_cache = [c for idx, c in enumerate(frozen_cache) if b_mask[idx]]

        def obj_D(p):
            grouped = build_model_components(
                "M_Dfree", theta_shared_base, p, pm, z_abs_ref, c_kms,
                d_velocity_offset_kms=cfg["d_velocity_offset_kms"],
                parent_window_kms=cfg["parent_window_kms"],
            )
            cand = split_frozen_candidate(grouped, frozen_grouped)
            res = compute_residuals_fast(cand, subset, engine, subset_cache)
            return -float(_fast_logpdf_sum_obs(res))

        def obj_H(p):
            grouped = build_model_components(
                "M_H", theta_shared_base, p, pm, z_abs_ref, c_kms,
                d_velocity_offset_kms=cfg["d_velocity_offset_kms"],
                parent_window_kms=cfg["parent_window_kms"],
            )
            cand = split_frozen_candidate(grouped, frozen_grouped)
            res = compute_residuals_fast(cand, subset, engine, subset_cache)
            return -float(_fast_logpdf_sum_obs(res))

        starts_D_loo = [list(s) for s in cfg.get("multistart", {}).get("M_Dfree", [[12.4, 10000.0, 1.0]])]
        best_D = -np.inf
        for x0 in starts_D_loo:
            rD = minimize(obj_D, x0, method="L-BFGS-B", bounds=bounds_D)
            if -rD.fun > best_D:
                best_D = -rD.fun

        best_H = -np.inf
        for x0 in starts_H["starts"]:
            rH = minimize(obj_H, x0, method="L-BFGS-B", bounds=bounds_H)
            if -rH.fun > best_H:
                best_H = -rH.fun

        return best_D, best_H

    coadds = set(b["coadd"] for b in data_blocks)
    for c_exclude in coadds:
        mask = [b["coadd"] != c_exclude for b in data_blocks]
        if not any(mask):
            # Skip: removing this coadd would leave no data blocks
            print_status(
                f"Leave-one-out coadd '{c_exclude}': SKIPPED (single coadd, no data remaining)",
                "PROCESS",
            )
            loo_ledger.append(
                {
                    "type": "coadd",
                    "excluded": c_exclude,
                    "T": 0.0,
                    "LL_D": 0.0,
                    "LL_H": 0.0,
                    "skipped": True,
                }
            )
            continue
        ll_d, ll_h = eval_loo_models(mask)
        t_loo = 2.0 * (ll_h - ll_d)
        print_status(
            f"Leave-one-out coadd '{c_exclude}': T = {t_loo:.2f} (D={ll_d:.2f}, H={ll_h:.2f})",
            "PROCESS",
        )
        loo_ledger.append(
            {
                "type": "coadd",
                "excluded": c_exclude,
                "T": t_loo,
                "LL_D": ll_d,
                "LL_H": ll_h,
            }
        )

    transitions_to_test = [
        "Lyα", "Lyβ", "Lyγ", "Lyδ", "Lyε",
        "Ly6", "Ly7", "Ly8", "Ly9", "Ly10",
        "Ly11", "Ly12", "Ly13", "Ly14", "Ly21",
    ]
    transition_rest_wavelengths = {
        "Lyα": 1215.6701, "Lyβ": 1025.7223, "Lyγ": 972.5368,
        "Lyδ": 949.7420, "Lyε": 937.8010,
        "Ly6": 930.7483, "Ly7": 926.2265, "Ly8": 923.1504,
        "Ly9": 920.9731, "Ly10": 919.3514, "Ly11": 918.1294,
        "Ly12": 917.1806, "Ly13": 916.4290, "Ly14": 915.8240,
        "Ly21": 913.6510,
    }

    for trans in transitions_to_test:
        lam_obs = transition_rest_wavelengths[trans] * (1 + z_abs_ref)
        mask = []
        for b in data_blocks:
            if b["w_min"] < lam_obs < b["w_max"]:
                mask.append(False)
            else:
                mask.append(True)
        if all(m for m in mask):
            continue  # Trans not in any block
        ll_d, ll_h = eval_loo_models(mask)
        t_loo = 2.0 * (ll_h - ll_d)
        print_status(
            f"Leave-one-out transition '{trans}': T = {t_loo:.2f} (D={ll_d:.2f}, H={ll_h:.2f})",
            "PROCESS",
        )
        loo_ledger.append(
            {
                "type": "transition",
                "excluded": trans,
                "T": t_loo,
                "LL_D": ll_d,
                "LL_H": ll_h,
            }
        )

    print_status("\n--- Parent Component Reassignment Robustness ---", "TITLE")
    # Parent reassignment was already computed before the MC loop;
    # the parent_ledger is reused here for display.
    for entry in parent_ledger:
        print_status(f"Parent {entry['parent_idx']}: LL_D = {entry['LL_D']:.2f}, T = {entry['T']:.2f}", "PROCESS")

    out_dir = project_root / "results"
    out_dir.mkdir(parents=True, exist_ok=True)
    window_suffix = f"_{parent_window_mode}" if parent_window_mode != 'fixed' else ""
    canonical_file = out_dir / f"{output_prefix}3_significance{window_suffix}.json"
    # Reduced runs use an N-specific file and cannot overwrite production.
    if N_sims < cfg.get("monte_carlo", {}).get("n_sims", 1000):
        output_file = out_dir / f"quick_{output_prefix}3_significance{window_suffix}_n{N_sims}.json"
        print_status(
            f"Reduced run (N={N_sims}): writing to {output_file.name} "
            f"to protect canonical ledger",
            "PROCESS",
        )
    else:
        output_file = canonical_file
    with open(output_file, "w") as f:
        json.dump(
            {
                "sightline": sightline_id,
                "parent_window_mode": parent_window_mode,
                "parent_window_kms": float(cfg["parent_window_kms"]),
                "T_obs": float(T_obs),
                "T_obs_parent_best": float(T_obs_parent_best),
                "N_sims": N_sims,
                "exceedances_standard": exceedances_standard,
                "exceedances_standard_fair": exceedances_standard_fair,
                "p_add_one": p_add_one_standard_fair,  # Use fair standard (not legacy inflated)
                "p_add_one_standard_fair": p_add_one_standard_fair,
                "exceedances_parent": exceedances_parent,
                "p_add_one_parent": p_add_one_parent,
                "binom_95_upper": binom_95_upper,
                "binom_95_upper_standard": binom_95_upper_standard,
                "binom_95_upper_parent": binom_95_upper_parent,
                "leave_one_out": loo_ledger,
                "parent_reassignment": parent_ledger,
                "simulations": results_ledger,
            },
            f,
            indent=2,
        )
    print_status(
        f"\n[SUCCESS] Calibration saved to {output_file}",
        "SUCCESS",
    )


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Run Gate 3 MC calibration for a sightline")
    parser.add_argument("--sightline", default=None, help="Sightline ID (default: Q1009+2956)")
    parser.add_argument("--parent-window", default='fixed', choices=['fixed', 'physical'],
                        help="Parent window mode: 'fixed' (±1000 km/s) or 'physical' (±3× largest b-value)")
    parser.add_argument("--n-sims", type=int, default=None,
                        help="Override number of MC simulations (default: config value)")
    parser.add_argument("--workers", type=int, default=12)
    args = parser.parse_args()
    run_gate3(sightline=args.sightline, parent_window_mode=args.parent_window, n_sims=args.n_sims, workers=args.workers)
