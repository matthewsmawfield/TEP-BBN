#!/usr/bin/env python3
"""
Secondary Analyses: C2 (Limited Scaffold Freedom), C3 (Noisy/Offset True-D MC),
C4 (Pure Kinematic Prior Test)

These are secondary robustness checks that build on the main Gate 2/3 pipeline.
Each can be run independently via CLI arguments.

C2: Re-optimise the N strongest H I components (by column density) under both
    M_Dfree and M_Hfree, and recompute T. Tests whether the fixed scaffold
    biases the significance.

C3: Perturb the true-D generating parameters (v_offset, logN_D, b_turb) by
    small random draws consistent with measurement uncertainties, then
    regenerate MC flux and refit. Tests whether the calibration is robust
    to uncertainties in the true-D model.

C4: Fit the candidate feature with M_kinematic (free v, free N, b fixed to
    parent H I) and compare T to M_Dfree and M_Hfree. Tests whether a pure
    kinematic shift without isotope physics can explain the feature.
"""

import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

import json
import numpy as np
import multiprocessing
from scipy.optimize import minimize
from scipy.stats import t as student_t

from scripts.utils.logger import print_status, setup_step_logger
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

np.seterr(all="ignore")


def _make_fast_logpdf_sum(noise_cfg):
    """Return a fast logpdf-sum function precomputing Student-t constants."""
    from scipy.special import gammaln as _gammaln
    nu = noise_cfg["nu"]
    loc = noise_cfg["location"]
    scale = noise_cfg["scale"]
    const = (
        _gammaln((nu + 1) / 2.0)
        - _gammaln(nu / 2.0)
        - 0.5 * np.log(nu * np.pi)
        - np.log(scale)
    )
    alpha = (nu + 1) / 2.0
    inv_nu = 1.0 / nu

    def _fast_logpdf_sum(residuals):
        v = residuals[np.abs(residuals) < 100.0]
        z = (v - loc) / scale
        return const * len(v) - alpha * np.sum(np.log1p(inv_nu * z * z))

    return _fast_logpdf_sum


def _load_pipeline_data(sightline=None):
    """Load shared data structures needed by all secondary analyses."""
    cfg = load_sightline_config(sightline)
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
            data_blocks.append({
                "wave": wave[mask],
                "flux": flux[mask],
                "err": err[mask],
                "vsig": r["vsig"],
                "w_min": r["w_min"],
                "w_max": r["w_max"],
                "coadd": coadd,
            })

    output_prefix = cfg.get("output_prefix", "gate")
    gate2_path = project_root / "results" / f"{output_prefix}2_parameter_ledger.json"
    with open(gate2_path, "r") as f:
        g2 = json.load(f)

    if "cand_params" in g2["results"]["M_Dfree"]:
        opt_D_obs = g2["results"]["M_Dfree"]["cand_params"]
        theta_shared_base = np.array(g2["results"]["M_Dfree"]["shared_params"])
    else:
        opt_D_obs = g2["results"]["M_Dfree"]["params"]
        theta_shared_base = np.array(pm.theta_init)

    return cfg, manifest, noise_cfg, z_abs_ref, c_kms, pm, engine, data_blocks, g2, opt_D_obs, theta_shared_base


# ---- C2: Limited Scaffold Freedom ----

def run_c2_limited_scaffold(sightline=None, n_free_components=5):
    """Re-optimise the N strongest H I components under both models."""
    setup_step_logger(Path(__file__).stem)
    print_status(f"=== C2: LIMITED SCAFFOLD FREEDOM ({sightline or 'Q1009+2956'}) ===", "SUCCESS")

    cfg, manifest, noise_cfg, z_abs_ref, c_kms, pm, engine, data_blocks, g2, opt_D_obs, theta_shared_base = _load_pipeline_data(sightline)

    # Identify the N strongest H I components by column density.
    # Only consider components within the absorber system (|v| <= parent_window).
    # Components from unrelated absorber systems at v ~ -47000 to -74000 km/s
    # must NOT be freed — freeing them allows spurious absorption in unrelated
    # spectral regions, corrupting the fit.
    # Additionally, D parent components must NOT be freed: the D model inherits
    # the parent's b (with mass scaling), so freeing the parent's b creates a
    # conflicting optimization where D's b is doubly controlled (by both the
    # parent's b and D's b_turb candidate parameter), causing D to get WORSE
    # when given more freedom — an unphysical result.
    parent_window = cfg["parent_window_kms"]
    comps = pm.reconstruct(theta_shared_base)
    h_comps = [(i, c) for i, c in enumerate(comps) if c["ion"] == "H_I"]

    # Identify D parent components (H I components at the same z as D I)
    d_zs = set(round(c["z"], 10) for c in comps if c["ion"] == "D_I")
    d_parent_indices = set()
    for i, c in enumerate(comps):
        if c["ion"] == "H_I" and round(c["z"], 10) in d_zs:
            d_parent_indices.add(i)
    print_status(f"D parent components (excluded from freeing): {sorted(d_parent_indices)}", "PROCESS")

    # Filter to absorber-system, non-D-parent components only
    h_comps_absorber = []
    for i, c in h_comps:
        v = c_kms * (c["z"] - z_abs_ref) / (1.0 + z_abs_ref)
        if abs(v) <= parent_window and i not in d_parent_indices:
            h_comps_absorber.append((i, c))
    h_comps_sorted = sorted(h_comps_absorber, key=lambda x: x[1]["logN"], reverse=True)
    free_indices = set(x[0] for x in h_comps_sorted[:n_free_components])
    print_status(f"Freeing {len(free_indices)} strongest non-parent H I components (by logN, within ±1000 km/s)", "PROCESS")
    for idx in free_indices:
        c = comps[idx]
        v = c_kms * (c["z"] - z_abs_ref) / (1.0 + z_abs_ref)
        print_status(f"  Component {idx}: logN={c['logN']:.2f}, b={c['b']:.2f}, v={v:.1f} km/s", "PROCESS")

    # Build a modified theta where freed components have their parameters
    # appended to the candidate vector. We need to split theta_shared into
    # fixed and free parts.
    # The ParameterManager stores parameters as a flat array; we need to
    # identify which entries correspond to the freed components.
    # Each component has 3 parameters: logN, b, z (in theta space).
    # We'll build a wrapper that optimises both the candidate D/H params
    # and the freed scaffold params.

    # Build frozen scaffold with freed components removed
    theta_fixed = theta_shared_base.copy()
    # Map each freed component to its actual theta indices via pm.comp_map.
    # The ParameterManager uses a complex tie structure — the naive idx*3
    # mapping is WRONG and would modify the wrong components' parameters.
    # Each freed component contributes 2 free params: logN and b (z stays fixed).
    # For components with thermal blocks (b_turb + T), we free b_turb only
    # (T is shared via ties and freeing it would affect all tied components).
    # For components with direct b, we free b directly.
    free_param_slices = []  # list of (logN_idx, b_idx) tuples
    for idx in sorted(free_indices):
        cmap = pm.comp_map[idx]
        n_idx = cmap.get('N_idx')
        if n_idx is None:
            raise ValueError(f"Component {idx} has no free N_idx (tied or fixed) — cannot free")
        b_idx = cmap.get('b_idx')
        if b_idx is None:
            # Thermal block: free b_turb (T stays tied)
            b_idx = cmap.get('b_turb_idx')
            if b_idx is None:
                raise ValueError(f"Component {idx} has no free b or b_turb_idx — cannot free")
        free_param_slices.append((n_idx, b_idx))

    # Build the frozen cache with ALL components (we'll handle the freed ones
    # by adding them as candidate components)
    frozen_grouped = build_model_components(
        "M_NULL", theta_shared_base, None, pm, z_abs_ref, c_kms,
        d_velocity_offset_kms=cfg["d_velocity_offset_kms"],
        parent_window_kms=cfg["parent_window_kms"],
    )
    frozen_cache = build_frozen_cache(frozen_grouped, data_blocks, engine)

    # For the freed components, we need to remove them from the frozen scaffold
    # and add them as candidate components that get optimised.
    # Simplest approach: build a modified pm that excludes the freed components
    # from the shared scaffold, and add them manually in the objective function.

    # Actually, the cleanest approach is to use the existing infrastructure:
    # 1. Set the freed components' parameters to 0 in theta_shared (effectively removing them)
    # 2. Add them as extra H_I components in the objective function

    # But this is complex. Let me use a simpler approach: just re-optimise
    # the freed components' b and logN (keeping z fixed) by modifying
    # theta_shared_base in the objective function.

    def _get_bounds(b):
        if isinstance(b, dict) and "cand" in b:
            return [tuple(x) for x in b["cand"]]
        return [tuple(x) for x in b]
    bounds_D = _get_bounds(g2["bounds"]["M_Dfree"])
    bounds_H_key = "M_Hfree" if "M_Hfree" in g2["bounds"] else "M_H"
    bounds_H = _get_bounds(g2["bounds"][bounds_H_key])

    # Extended bounds: candidate params + freed scaffold params (logN, b for each)
    scaffold_bounds = [(10.0, 20.0), (1.0, 50.0)] * len(free_param_slices)  # logN, b for each freed comp
    bounds_D_ext = bounds_D + scaffold_bounds
    bounds_H_ext = bounds_H + scaffold_bounds

    starts_D = cfg["multistart"]["M_Dfree"]
    starts_H = cfg["multistart"]["M_Hfree"]

    _fast_logpdf_sum = _make_fast_logpdf_sum(noise_cfg)

    def make_obj_scaffold(model_name, bounds_ext, starts_cand):
        def obj(p):
            # Split into candidate params and scaffold params
            n_cand = len(starts_cand[0])
            cand_params = p[:n_cand]
            scaffold_params = p[n_cand:]

            # Modify theta_shared_base with freed scaffold params.
            # free_param_slices[i] = (logN_theta_idx, b_theta_idx)
            theta_mod = theta_shared_base.copy()
            for i, (n_idx, b_idx) in enumerate(free_param_slices):
                logN_free = scaffold_params[i * 2]
                b_free = scaffold_params[i * 2 + 1]
                theta_mod[n_idx] = logN_free
                theta_mod[b_idx] = b_free

            grouped = build_model_components(
                model_name, theta_mod, cand_params, pm, z_abs_ref, c_kms,
                d_velocity_offset_kms=cfg["d_velocity_offset_kms"],
                parent_window_kms=cfg["parent_window_kms"],
            )
            res = compute_residuals(grouped, data_blocks, engine)
            ll = _fast_logpdf_sum(res)
            return -float(ll)
        return obj

    # Fit M_Dfree with scaffold freedom
    obj_D = make_obj_scaffold("M_Dfree", bounds_D_ext, starts_D)
    best_ll_D = -np.inf
    for x0 in starts_D:
        # Extend start with current scaffold values
        scaffold_init = []
        for n_idx, b_idx in free_param_slices:
            scaffold_init.extend([theta_shared_base[n_idx], theta_shared_base[b_idx]])
        x0_ext = list(x0) + scaffold_init
        res_D = minimize(obj_D, x0_ext, method="L-BFGS-B", bounds=bounds_D_ext)
        if -res_D.fun > best_ll_D:
            best_ll_D = -res_D.fun
    print_status(f"M_Dfree (scaffold freedom={n_free_components}): LL = {best_ll_D:.2f}", "PROCESS")

    # Fit M_Hfree with scaffold freedom
    obj_H = make_obj_scaffold("M_H", bounds_H_ext, starts_H)
    best_ll_H = -np.inf
    for x0 in starts_H:
        scaffold_init = []
        for n_idx, b_idx in free_param_slices:
            scaffold_init.extend([theta_shared_base[n_idx], theta_shared_base[b_idx]])
        x0_ext = list(x0) + scaffold_init
        res_H = minimize(obj_H, x0_ext, method="L-BFGS-B", bounds=bounds_H_ext)
        if -res_H.fun > best_ll_H:
            best_ll_H = -res_H.fun
    print_status(f"M_Hfree (scaffold freedom={n_free_components}): LL = {best_ll_H:.2f}", "PROCESS")

    T_scaffold = 2.0 * (best_ll_H - best_ll_D)
    T_orig = 2.0 * (g2["results"]["M_Hfree"]["LL"] - g2["results"]["M_Dfree"]["LL"])
    print_status(f"T (original, fixed scaffold) = {T_orig:.2f}", "PROCESS")
    print_status(f"T (with {n_free_components} freed components) = {T_scaffold:.2f}", "PROCESS")
    print_status(f"ΔT = {T_scaffold - T_orig:.2f}", "PROCESS")

    out_dir = project_root / "results"
    out_dir.mkdir(parents=True, exist_ok=True)
    output_prefix = cfg.get("output_prefix", "gate")
    output_file = out_dir / f"{output_prefix}3_c2_scaffold_freedom.json"
    with open(output_file, "w") as f:
        json.dump({
            "sightline": cfg["sightline_id"],
            "analysis": "C2_limited_scaffold_freedom",
            "n_free_components": n_free_components,
            "freed_component_indices": sorted(free_indices),
            "LL_D_free_scaffold": best_ll_D,
            "LL_H_free_scaffold": best_ll_H,
            "T_scaffold": float(T_scaffold),
            "T_original": float(T_orig),
            "delta_T": float(T_scaffold - T_orig),
        }, f, indent=2)
    print_status(f"Saved to {output_file}", "SUCCESS")
    return True


# ---- C3: Noisy/Offset True-D MC ----

def _run_c3_wrapper(args):
    return run_c3_simulation(*args)


def run_c3_simulation(
    seed, data_blocks, noise_cfg, pm, z_abs_ref, c_kms,
    theta_shared_base, engine, starts_H, bounds_D, bounds_H,
    frozen_grouped, frozen_cache, cfg_multistart_D,
    d_velocity_offset_kms, parent_window_kms, canonical_parent_idx,
    opt_D_obs, perturb_sigma,
    lyman_transitions,
):
    """Run a single MC realization with perturbed true-D parameters."""
    rng = np.random.default_rng(seed)

    # Perturb the D component parameters.
    # The velocity offset d_velocity_offset_kms = -81.6 is a fixed physical
    # constant (exact reduced-mass isotope shift), NOT a free parameter.
    # Perturbing it would generate data with D at a wrong velocity while the
    # fitting model looks for D at the correct velocity — a mismatch that
    # artificially inflates T_sim.  Only the nuisance parameters (logN_D,
    # T_K, b_turb) are perturbed.
    logN_D_true, T_K_true, b_turb_true = opt_D_obs
    logN_D_pert = logN_D_true + rng.normal(0, perturb_sigma["logN_D"])
    # Clamp T_K to be physically positive (negative T_K produces unphysical
    # negative thermal broadening).
    T_K_pert = max(T_K_true + rng.normal(0, perturb_sigma["T_K"]), 100.0)
    b_turb_pert = max(b_turb_true + rng.normal(0, perturb_sigma["b_turb"]), 0.1)

    # Build perturbed true-D model (velocity offset is NOT perturbed)
    grouped_D_pert = build_model_components(
        "M_Dfree", theta_shared_base, [logN_D_pert, T_K_pert, b_turb_pert],
        pm, z_abs_ref, c_kms,
        d_velocity_offset_kms=d_velocity_offset_kms,
        parent_window_kms=parent_window_kms,
    )

    # Generate perturbed base fluxes
    base_fluxes_pert = []
    for block in data_blocks:
        tau_tot = np.zeros_like(block["wave"])
        if grouped_D_pert["H_I"]:
            tau_tot += engine.compute_optical_depth(block["wave"], lyman_transitions, grouped_D_pert["H_I"])
        if grouped_D_pert["D_I"]:
            tau_tot += engine.compute_optical_depth(block["wave"], lyman_transitions, grouped_D_pert["D_I"])
        if grouped_D_pert["C_IV"]:
            tau_tot += engine.compute_optical_depth(block["wave"], ["CIV_1548", "CIV_1550"], grouped_D_pert["C_IV"])
        if grouped_D_pert["C_III"]:
            tau_tot += engine.compute_optical_depth(block["wave"], ["CIII_977"], grouped_D_pert["C_III"])
        if grouped_D_pert["C_II"]:
            tau_tot += engine.compute_optical_depth(block["wave"], ["CII_1334"], grouped_D_pert["C_II"])
        if grouped_D_pert["Si_IV"]:
            tau_tot += engine.compute_optical_depth(block["wave"], ["SiIV_1393", "SiIV_1402"], grouped_D_pert["Si_IV"])
        flux = engine.apply_convolution(np.exp(-tau_tot), block["wave"], block["vsig"])
        base_fluxes_pert.append(flux)

    # Generate noisy flux realization
    sim_blocks = []
    for i, block in enumerate(data_blocks):
        err = block["err"]
        noise = student_t.rvs(df=noise_cfg["nu"], loc=0.0, scale=err * noise_cfg["scale"], random_state=rng)
        sim_flux = base_fluxes_pert[i] + noise
        sim_blocks.append({
            "wave": block["wave"], "flux": sim_flux, "err": block["err"],
            "vsig": block["vsig"], "w_min": block["w_min"], "w_max": block["w_max"],
            "coadd": block["coadd"],
        })

    _fast_logpdf_sum_parent = _make_fast_logpdf_sum(noise_cfg)

    def make_obj_parent(model_name, blocks, parent_idx=0):
        def obj(p):
            grouped = build_model_components(
                model_name, theta_shared_base, p, pm, z_abs_ref, c_kms,
                parent_idx=parent_idx,
                d_velocity_offset_kms=d_velocity_offset_kms,
                parent_window_kms=parent_window_kms,
            )
            cand = split_frozen_candidate(grouped, frozen_grouped)
            res = compute_residuals_fast(cand, blocks, engine, frozen_cache)
            ll = _fast_logpdf_sum_parent(res)
            return -float(ll)
        return obj

    # Fit M_Dfree across eligible parents
    # Apply the same column density threshold as Gate 3 (max - 2.0 dex)
    comps = pm.reconstruct(theta_shared_base)
    h_comps = [c for c in comps if c["ion"] == "H_I"]
    logN_H_max = max(c["logN"] for c in h_comps)
    logN_H_min = logN_H_max - 2.0
    valid_parents = []
    for j, c in enumerate(h_comps):
        v = c_kms * (c["z"] - z_abs_ref) / (1.0 + z_abs_ref)
        if abs(v) <= parent_window_kms and c["logN"] >= logN_H_min:
            valid_parents.append(j)

    best_ll_D = -np.inf
    ll_D_canonical = -np.inf
    actual_starts_H = starts_H["starts"]
    opt_D_start = starts_H["opt_D_obs"]

    for j in valid_parents:
        obj_D = make_obj_parent("M_Dfree", sim_blocks, j)
        starts_D = [list(s) for s in cfg_multistart_D]
        if j == canonical_parent_idx:
            starts_D.insert(0, opt_D_start)
        best_local_ll_D = -np.inf
        for x0 in starts_D:
            res_D = minimize(obj_D, x0, method="L-BFGS-B", bounds=bounds_D)
            if -res_D.fun > best_local_ll_D:
                best_local_ll_D = -res_D.fun
        if j == canonical_parent_idx:
            ll_D_canonical = best_local_ll_D
        if best_local_ll_D > best_ll_D:
            best_ll_D = best_local_ll_D

    # Fit M_Hfree
    obj_H = make_obj_parent("M_H", sim_blocks)
    best_ll_H = -np.inf
    for x0 in actual_starts_H:
        res_H = minimize(obj_H, x0, method="L-BFGS-B", bounds=bounds_H)
        if -res_H.fun > best_ll_H:
            best_ll_H = -res_H.fun

    T_parent = 2.0 * (best_ll_H - best_ll_D)
    T_standard = 2.0 * (best_ll_H - ll_D_canonical)

    return {
        "simulation_id": seed,
        "seed": seed,
        "logL_D_max": best_ll_D,
        "logL_D_canonical": ll_D_canonical,
        "logL_Hfree": best_ll_H,
        "T_parent": T_parent,
        "T_standard": T_standard,
        "perturbed_params": {
            "logN_D": logN_D_pert,
            "T_K": T_K_pert,
            "b_turb": b_turb_pert,
        },
    }


def run_c3_perturbed_mc(sightline=None, n_sims=200):
    """Run MC with perturbed true-D generating parameters."""
    setup_step_logger(Path(__file__).stem)
    print_status(f"=== C3: NOISY/OFFSET TRUE-D MC ({sightline or 'Q1009+2956'}) ===", "SUCCESS")

    cfg, manifest, noise_cfg, z_abs_ref, c_kms, pm, engine, data_blocks, g2, opt_D_obs, theta_shared_base = _load_pipeline_data(sightline)

    # Perturbation sigmas: ~10% of typical parameter ranges.
    # v_offset is NOT perturbed — it is a fixed physical constant (-81.6 km/s,
    # exact reduced-mass isotope shift).  Perturbing it creates a mismatch
    # between the generating and fitting models that artificially inflates T.
    perturb_sigma = {
        "logN_D": 0.1,      # ±0.1 dex in logN_D
        "T_K": 1000.0,      # ±1000 K (clamped to >= 100 K)
        "b_turb": 1.0,      # ±1 km/s (clamped to >= 0.1)
    }
    print_status(f"Perturbation sigmas: {perturb_sigma}", "PROCESS")
    print_status(f"N_sims: {n_sims}", "PROCESS")

    ll_D_max_obs = g2["results"]["M_Dfree"]["LL"]
    ll_H_max_obs = g2["results"]["M_Hfree"]["LL"]
    T_obs = 2.0 * (ll_H_max_obs - ll_D_max_obs)

    # Build frozen scaffold
    frozen_grouped = build_model_components(
        "M_NULL", theta_shared_base, None, pm, z_abs_ref, c_kms,
        d_velocity_offset_kms=cfg["d_velocity_offset_kms"],
        parent_window_kms=cfg["parent_window_kms"],
    )
    frozen_cache = build_frozen_cache(frozen_grouped, data_blocks, engine)

    # Auto-detect canonical parent (highest logN_H among H I with D counterpart)
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

    # Compute observed T_parent_best
    # Apply the same column density threshold as Gate 3 (max - 2.0 dex)
    h_comps_obs = [c for c in comps_for_parent if c["ion"] == "H_I"]
    parent_window_kms = cfg["parent_window_kms"]
    logN_H_max_obs = max(c["logN"] for c in h_comps_obs)
    logN_H_min_obs = logN_H_max_obs - 2.0
    valid_parent_indices = []
    for j, c in enumerate(h_comps_obs):
        v = c_kms * (c["z"] - z_abs_ref) / (1.0 + z_abs_ref)
        if abs(v) <= parent_window_kms and c["logN"] >= logN_H_min_obs:
            valid_parent_indices.append(j)

    def _get_bounds(b):
        if isinstance(b, dict) and "cand" in b:
            return [tuple(x) for x in b["cand"]]
        return [tuple(x) for x in b]
    bounds_D = _get_bounds(g2["bounds"]["M_Dfree"])
    bounds_H_key = "M_Hfree" if "M_Hfree" in g2["bounds"] else "M_H"
    bounds_H = _get_bounds(g2["bounds"][bounds_H_key])

    starts_H = {"starts": cfg["multistart"]["M_Hfree"], "opt_D_obs": opt_D_obs}
    cfg_multistart_D = cfg["multistart"]["M_Dfree"]

    lyman_transitions = [
        "HI_Lya", "HI_Lyb", "HI_Lyg", "HI_Lyd", "HI_Lye",
        "HI_Ly6", "HI_Ly7", "HI_Ly8", "HI_Ly9", "HI_Ly10",
        "HI_Ly11", "HI_Ly12", "HI_Ly13", "HI_Ly14", "HI_Ly21",
    ]

    # Compute observed T_parent_best (reuse from main pipeline)
    gate3_path = project_root / "results" / f"{cfg.get('output_prefix', 'gate')}3_significance.json"
    if gate3_path.exists():
        with open(gate3_path, "r") as f:
            g3 = json.load(f)
        T_obs_parent_best = g3.get("T_obs_parent_best", T_obs)
    else:
        T_obs_parent_best = T_obs

    seed_base = cfg.get("monte_carlo", {}).get("seed_base", 900000) + 50000  # Offset to avoid collision

    pool_args = []
    for i in range(n_sims):
        seed = seed_base + i
        pool_args.append((
            seed, data_blocks, noise_cfg, pm, z_abs_ref, c_kms,
            theta_shared_base, engine, starts_H, bounds_D, bounds_H,
            frozen_grouped, frozen_cache, cfg_multistart_D,
            cfg["d_velocity_offset_kms"], cfg["parent_window_kms"],
            canonical_parent_idx, opt_D_obs, perturb_sigma, lyman_transitions,
        ))

    results_ledger = []
    exceedances_standard = 0
    exceedances_parent = 0

    with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
        for i, res in enumerate(pool.imap_unordered(_run_c3_wrapper, pool_args)):
            results_ledger.append(res)
            if res["T_standard"] >= T_obs:
                exceedances_standard += 1
            if res["T_parent"] >= T_obs_parent_best:
                exceedances_parent += 1
            if (i + 1) % 10 == 0:
                print_status(
                    f"Completed {i+1}/{n_sims}. Std exc: {exceedances_standard}, Parent exc: {exceedances_parent}",
                    "PROCESS",
                )

    p_std = (exceedances_standard + 1) / (n_sims + 1)
    p_parent = (exceedances_parent + 1) / (n_sims + 1)

    print_status(f"\nT_obs = {T_obs:.2f}, T_parent_best = {T_obs_parent_best:.2f}", "PROCESS")
    print_status(f"Exceedances (standard): {exceedances_standard}/{n_sims} → p = {p_std:.5f}", "PROCESS")
    print_status(f"Exceedances (parent): {exceedances_parent}/{n_sims} → p = {p_parent:.5f}", "PROCESS")

    out_dir = project_root / "results"
    out_dir.mkdir(parents=True, exist_ok=True)
    output_prefix = cfg.get("output_prefix", "gate")
    output_file = out_dir / f"{output_prefix}3_c3_perturbed_mc.json"
    with open(output_file, "w") as f:
        json.dump({
            "sightline": cfg["sightline_id"],
            "analysis": "C3_perturbed_true_D_MC",
            "perturb_sigma": perturb_sigma,
            "N_sims": n_sims,
            "T_obs": float(T_obs),
            "T_obs_parent_best": float(T_obs_parent_best),
            "exceedances_standard": exceedances_standard,
            "exceedances_parent": exceedances_parent,
            "p_standard": float(p_std),
            "p_parent": float(p_parent),
            "simulations": results_ledger,
        }, f, indent=2)
    print_status(f"Saved to {output_file}", "SUCCESS")
    return True


# ---- C4: Pure Kinematic Prior Test ----

def run_c4_kinematic_test(sightline=None):
    """Fit M_kinematic (free v, free N, b=parent) and compare to M_Dfree and M_Hfree."""
    setup_step_logger(Path(__file__).stem)
    print_status(f"=== C4: PURE KINEMATIC PRIOR TEST ({sightline or 'Q1009+2956'}) ===", "SUCCESS")

    cfg, manifest, noise_cfg, z_abs_ref, c_kms, pm, engine, data_blocks, g2, opt_D_obs, theta_shared_base = _load_pipeline_data(sightline)

    theta_shared = np.array(theta_shared_base)

    # M_kinematic: 2 free params (v_H, logN_H), b fixed to parent
    bounds_kin = [(-160.0, 50.0), (0.0, 20.0)]
    starts_kin = [
        [-81.6, 12.4],
        [-132.0, 12.45],
        [-81.0, 13.0],
        [-100.0, 12.0],
        [-60.0, 12.5],
    ]

    _fast_logpdf_sum_kin = _make_fast_logpdf_sum(noise_cfg)

    def obj_kin(p):
        grouped = build_model_components(
            "M_kinematic", theta_shared, p, pm, z_abs_ref, c_kms,
            d_velocity_offset_kms=cfg["d_velocity_offset_kms"],
            parent_window_kms=cfg["parent_window_kms"],
        )
        res = compute_residuals(grouped, data_blocks, engine)
        ll = _fast_logpdf_sum_kin(res)
        return -float(ll)

    best_ll_kin = -np.inf
    for x0 in starts_kin:
        res_kin = minimize(obj_kin, x0, method="L-BFGS-B", bounds=bounds_kin)
        if -res_kin.fun > best_ll_kin:
            best_ll_kin = -res_kin.fun
            best_params_kin = res_kin.x

    ll_D = g2["results"]["M_Dfree"]["LL"]
    ll_H = g2["results"]["M_Hfree"]["LL"]
    T_D_vs_H = 2.0 * (ll_H - ll_D)
    T_kin_vs_D = 2.0 * (ll_H - best_ll_kin)
    T_kin_vs_H = 2.0 * (best_ll_kin - ll_D)

    print_status(f"M_Dfree: LL = {ll_D:.2f} (k=3)", "PROCESS")
    print_status(f"M_Hfree: LL = {ll_H:.2f} (k=4)", "PROCESS")
    print_status(f"M_kinematic: LL = {best_ll_kin:.2f} (k=2, b=parent)", "PROCESS")
    print_status(f"  Best v_H = {best_params_kin[0]:.2f} km/s, logN_H = {best_params_kin[1]:.2f}", "PROCESS")
    print_status(f"T (M_H vs M_D) = {T_D_vs_H:.2f}", "PROCESS")
    print_status(f"T (M_H vs M_kin) = {T_kin_vs_D:.2f}", "PROCESS")
    print_status(f"T (M_kin vs M_D) = {T_kin_vs_H:.2f}", "PROCESS")

    # AIC comparison
    aic_D = 2 * 3 - 2 * ll_D
    aic_H = 2 * 4 - 2 * ll_H
    aic_kin = 2 * 2 - 2 * best_ll_kin
    print_status(f"AIC: M_D={aic_D:.2f}, M_H={aic_H:.2f}, M_kin={aic_kin:.2f}", "PROCESS")
    print_status(f"ΔAIC (M_kin - M_D) = {aic_kin - aic_D:.2f}", "PROCESS")
    print_status(f"ΔAIC (M_H - M_kin) = {aic_H - aic_kin:.2f}", "PROCESS")

    out_dir = project_root / "results"
    out_dir.mkdir(parents=True, exist_ok=True)
    output_prefix = cfg.get("output_prefix", "gate")
    output_file = out_dir / f"{output_prefix}3_c4_kinematic.json"
    with open(output_file, "w") as f:
        json.dump({
            "sightline": cfg["sightline_id"],
            "analysis": "C4_kinematic_prior_test",
            "LL_Dfree": float(ll_D),
            "LL_Hfree": float(ll_H),
            "LL_kinematic": float(best_ll_kin),
            "k_Dfree": 3,
            "k_Hfree": 4,
            "k_kinematic": 2,
            "best_kinematic_params": {"v_H": float(best_params_kin[0]), "logN_H": float(best_params_kin[1])},
            "T_H_vs_D": float(T_D_vs_H),
            "T_H_vs_kin": float(T_kin_vs_D),
            "T_kin_vs_D": float(T_kin_vs_H),
            "AIC_D": float(aic_D),
            "AIC_H": float(aic_H),
            "AIC_kin": float(aic_kin),
            "dAIC_kin_vs_D": float(aic_kin - aic_D),
            "dAIC_H_vs_kin": float(aic_H - aic_kin),
        }, f, indent=2)
    print_status(f"Saved to {output_file}", "SUCCESS")
    return True


def run_all_secondary_analyses(sightline=None, n_sims=200, n_free_components=5):
    """Run all secondary robustness checks (C2, C3, C4) for a sightline.

    This is the pipeline-callable entry point that runs all three
    secondary analyses in sequence.
    """
    setup_step_logger(Path(__file__).stem)
    print_status("=== SECONDARY ROBUSTNESS ANALYSES (C2 + C3 + C4) ===", "SUCCESS")
    print_status(f"Sightline: {sightline or 'Q1009+2956 (default)'}", "PROCESS")
    print_status(f"C3 simulations: {n_sims}", "PROCESS")
    print_status("")

    results = {}

    print_status("--- C2: Limited Scaffold Freedom ---", "TITLE")
    try:
        c2_result = run_c2_limited_scaffold(
            sightline=sightline, n_free_components=n_free_components
        )
        results["c2"] = "PASS" if c2_result else "FAIL"
        print_status(f"  C2: {results['c2']}", "SUCCESS")
    except Exception as exc:
        results["c2"] = f"ERROR: {exc}"
        print_status(f"  C2: {results['c2']}", "ERROR")
    print_status("")

    print_status("--- C3: Perturbed Monte Carlo ---", "TITLE")
    try:
        c3_result = run_c3_perturbed_mc(sightline=sightline, n_sims=n_sims)
        results["c3"] = "PASS" if c3_result else "FAIL"
        print_status(f"  C3: {results['c3']}", "SUCCESS")
    except Exception as exc:
        results["c3"] = f"ERROR: {exc}"
        print_status(f"  C3: {results['c3']}", "ERROR")
    print_status("")

    print_status("--- C4: Kinematic Test ---", "TITLE")
    try:
        c4_result = run_c4_kinematic_test(sightline=sightline)
        results["c4"] = "PASS" if c4_result else "FAIL"
        print_status(f"  C4: {results['c4']}", "SUCCESS")
    except Exception as exc:
        results["c4"] = f"ERROR: {exc}"
        print_status(f"  C4: {results['c4']}", "ERROR")
    print_status("")

    # Write summary ledger
    project_root = Path(__file__).resolve().parent.parent.parent
    out_dir = project_root / "results"
    out_dir.mkdir(parents=True, exist_ok=True)
    summary_path = out_dir / "secondary_analyses_summary.json"
    with open(summary_path, "w") as f:
        json.dump(
            {
                "sightline": sightline or "Q1009+2956",
                "n_sims_c3": n_sims,
                "n_free_components_c2": n_free_components,
                "results": results,
                "all_passed": all(v == "PASS" for v in results.values()),
            },
            f,
            indent=2,
        )
    print_status(f"Summary written to {summary_path}", "SUCCESS")

    return results


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Run secondary robustness analyses")
    parser.add_argument("--sightline", default=None, help="Sightline ID (default: Q1009+2956)")
    parser.add_argument("--analysis", required=True, choices=["c2", "c3", "c4", "all"],
                        help="Which analysis to run: c2 (scaffold freedom), c3 (perturbed MC), c4 (kinematic), all")
    parser.add_argument("--n-free", type=int, default=5, help="C2: Number of H I components to free")
    parser.add_argument("--n-sims", type=int, default=200, help="C3: Number of MC simulations")
    args = parser.parse_args()

    if args.analysis == "all":
        run_all_secondary_analyses(
            sightline=args.sightline, n_sims=args.n_sims, n_free_components=args.n_free
        )
    elif args.analysis == "c2":
        run_c2_limited_scaffold(sightline=args.sightline, n_free_components=args.n_free)
    elif args.analysis == "c3":
        run_c3_perturbed_mc(sightline=args.sightline, n_sims=args.n_sims)
    elif args.analysis == "c4":
        run_c4_kinematic_test(sightline=args.sightline)
