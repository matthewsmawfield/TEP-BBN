#!/usr/bin/env python3
"""
Gate 8 Calibration: True-D Injection Monte Carlo

Calibrates the Gate 8 statistics (b-value ratio, velocity deviation,
column density difference) against true-D simulations. The reviewer
correctly notes that the nominal sigma values are not calibrated against
the true-D null, and that the three statistics are not independent
(they come from the same free-H fit).

This script reuses the exact same setup as step_03_significance.py,
generates true-D spectra, fits M_Hfree, and extracts the fitted
parameters to build the null distribution.
"""

import sys
from pathlib import Path
import json
import numpy as np
from scipy.optimize import minimize
from scipy.stats import t as student_t
from scipy.special import gammaln

project_root = Path(__file__).resolve().parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from scripts.utils.logger import print_status, setup_step_logger
from scripts.lib.model_builder import build_model_components
from scripts.lib.model_parser import ParameterManager, parse_vpfit_ties
from scripts.lib.physical_rt_engine import RadiativeTransferEngine
from scripts.lib.residual_engine import (
    compute_residuals_fast,
    build_frozen_cache,
    split_frozen_candidate,
)
from scripts.lib.doppler_physics import compute_doppler_b


def run_gate8_calibration(sightline="Q1009+2956", n_sims=200):
    setup_step_logger(Path(__file__).stem)
    print_status(f"=== GATE 8 CALIBRATION: {sightline} ===", "SUCCESS")

    # ---- Load config ----
    cfg = json.load(open(project_root / f"configs/sightlines/{sightline}.json"))
    z_abs = cfg["z_abs"]
    c_kms = 299792.458
    v_iso = cfg["d_velocity_offset_kms"]
    parent_window = cfg["parent_window_kms"]
    output_prefix = cfg.get("output_prefix", "gate_")

    noise_path = project_root / f"configs/sightlines/{sightline}_noise_model.json"
    noise_cfg = json.load(open(noise_path))

    # ---- Parse VPFIT model (same as step_03) ----
    vpfit_path = project_root / cfg["vpfit_model_path"]
    components_raw, regions = parse_vpfit_ties(vpfit_path)
    pm = ParameterManager(components_raw)
    engine = RadiativeTransferEngine(z_abs=z_abs)

    # ---- Build data blocks (same as step_03) ----
    manifest_path = project_root / cfg["manifest_path"]
    with open(manifest_path) as f:
        manifest = json.load(f)

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
                np.isfinite(flux) & np.isfinite(err) & (err > 0)
                & (wave >= r["w_min"]) & (wave <= r["w_max"])
            )
            if np.sum(mask) == 0:
                continue
            data_blocks.append({
                "wave": wave[mask], "flux": flux[mask], "err": err[mask],
                "vsig": r["vsig"], "w_min": r["w_min"], "w_max": r["w_max"],
                "coadd": coadd,
            })

    # ---- Load Gate 2 results for observed params and shared params ----
    gate2_file = project_root / "results" / f"{output_prefix}2_parameter_ledger.json"
    with open(gate2_file) as f:
        g2 = json.load(f)

    m_h_obs = g2["results"]["M_Hfree"]
    obs_params = m_h_obs.get("cand_params", m_h_obs.get("params", []))
    v_H_obs = obs_params[0]
    logN_H_obs = obs_params[1]
    # Compute total b from fitted T_K and b_turb (not just b_turb)
    # M_Hfree params: [v_H, logN_H, T_K, b_turb]
    T_K_H_obs = obs_params[2]
    b_turb_H_obs = obs_params[3]
    b_H_obs = compute_doppler_b(T_K_H_obs, b_turb_H_obs, isotope='H')

    # Use profiled shared params from M_Dfree as truth (same as step_03)
    if "cand_params" in g2["results"]["M_Dfree"]:
        opt_D_obs = g2["results"]["M_Dfree"]["cand_params"]
        theta_shared_base = np.array(g2["results"]["M_Dfree"]["shared_params"])
    else:
        opt_D_obs = g2["results"]["M_Dfree"]["params"]
        theta_shared_base = pm.theta_init

    theta_shared_comps = pm.reconstruct(theta_shared_base)

    # ---- Get canonical parent (highest logN_H among H I with D counterpart) ----
    h_comps = [c for c in theta_shared_comps if c["ion"] == "H_I"]
    d_comps = [c for c in theta_shared_comps if c["ion"] == "D_I"]
    canonical_parent_idx = 0
    d_zs = set(round(c["z"], 10) for c in theta_shared_comps if c["ion"] == "D_I")
    _best_logN = float("-inf")
    for i, c in enumerate(h_comps):
        if round(c["z"], 10) in d_zs:
            if c["logN"] > _best_logN:
                _best_logN = c["logN"]
                canonical_parent_idx = i

    parent_comp = h_comps[canonical_parent_idx]
    v_parent = c_kms * (parent_comp["z"] - z_abs) / (1.0 + z_abs)
    b_parent = parent_comp["b"]
    logN_parent = parent_comp["logN"]

    # D-predicted b value: mixed thermal+turbulent formula
    # b_H^2 = b_turb^2 + 2kT/m_H, b_D^2 = b_turb^2 + 2kT/m_D
    # The turbulent contribution does NOT divide by sqrt(2)
    # Only the thermal contribution scales as 1/sqrt(m_D/m_H) = 1/sqrt(2)
    parent_raw = None
    for rc in components_raw:
        if rc.get('ion') == 'H_I' and abs(rc.get('z', 0) - parent_comp['z']) < 1e-10:
            parent_raw = rc
            break
    if parent_raw and parent_raw.get('b_turb') is not None and parent_raw.get('T') is not None:
        b_turb = parent_raw['b_turb']
        T = parent_raw['T']
        b_therm_H = 12.85 * np.sqrt(T / 1e4 / 1.0)  # m_H = 1 amu
        b_therm_D = 12.85 * np.sqrt(T / 1e4 / 2.0)  # m_D = 2 amu
        b_D_pred = np.sqrt(b_turb**2 + b_therm_D**2)
        print_status(f"  Mixed b_D: b_turb={b_turb:.3f}, T={T:.0f}, b_therm_H={b_therm_H:.3f}, b_therm_D={b_therm_D:.3f}", "PROCESS")
        print_status(f"  b_D_pred = sqrt({b_turb:.3f}^2 + {b_therm_D:.3f}^2) = {b_D_pred:.3f} (vs thermal-only {b_parent/np.sqrt(2):.3f})", "PROCESS")
    else:
        # Fallback: no T/b_turb available, use thermal-only approximation
        b_D_pred = b_parent / np.sqrt(2)
        print_status(f"  WARNING: No T/b_turb for parent, using thermal-only b_D = {b_D_pred:.3f}", "WARN")
    DH_BBN = 2.527e-5  # BBN D/H ratio (Cooke et al. 2018, Planck 2018)
    logN_D_pred = np.log10(10**logN_parent * DH_BBN)

    # Observed Gate 8 statistics
    v_expected_D = v_parent + v_iso
    obs_deviation = v_H_obs - v_expected_D
    obs_b_ratio = b_H_obs / b_D_pred
    obs_logN_diff = logN_H_obs - logN_D_pred

    print_status(f"\n--- Observed Parameters ---", "TITLE")
    print_status(f"  v_H={v_H_obs:.2f}, b_H={b_H_obs:.2f}, logN_H={logN_H_obs:.2f}", "PROCESS")
    print_status(f"  v_parent={v_parent:.1f}, b_parent={b_parent:.1f}, logN_parent={logN_parent:.2f}", "PROCESS")
    print_status(f"  b_D_pred={b_D_pred:.2f}, b_ratio={obs_b_ratio:.3f}", "PROCESS")
    print_status(f"  v_deviation={obs_deviation:.1f} km/s, logN_diff={obs_logN_diff:.3f} dex", "PROCESS")

    # ---- Build frozen scaffold (M_NULL = shared components only) ----
    frozen_grouped = build_model_components(
        "M_NULL", theta_shared_base, None, pm, z_abs, c_kms,
        d_velocity_offset_kms=v_iso, parent_window_kms=parent_window,
    )
    frozen_cache = build_frozen_cache(frozen_grouped, data_blocks, engine)
    print_status(f"  Frozen cache: {len(frozen_cache)} blocks", "PROCESS")

    # ---- Compute base fluxes (D model = truth for simulations) ----
    grouped_D = build_model_components(
        "M_Dfree", theta_shared_base, opt_D_obs,
        pm, z_abs, c_kms,
        d_velocity_offset_kms=v_iso,
        parent_window_kms=parent_window,
        parent_idx=canonical_parent_idx,
    )
    candidate_D = split_frozen_candidate(grouped_D, frozen_grouped)

    # Compute base fluxes (model flux = data - residual*err) for all blocks
    # Residuals from compute_residuals_fast are in sigma units: (flux - model)/err
    # So model = flux - res * err, NOT flux - res (which would be ~38x too large)
    all_res = compute_residuals_fast(candidate_D, data_blocks, engine, frozen_cache)
    base_fluxes = []
    offset = 0
    for block in data_blocks:
        n = len(block["wave"])
        res_block = all_res[offset:offset+n]
        base_fluxes.append(block["flux"] - res_block * block["err"])
        offset += n

    # ---- Get bounds and starts ----
    bounds_H = g2.get("bounds", {}).get("M_Hfree", g2.get("bounds", {}).get("M_H", []))
    starts_H = cfg["multistart"]["M_Hfree"]
    # Use all configured starts + obs_params for MC fairness
    mc_starts = [list(obs_params)] + [list(s) for s in starts_H]

    # ---- Student-t logpdf (same as step_03) ----
    _nu = noise_cfg["nu"]
    _loc = noise_cfg["location"]
    _scale = noise_cfg["scale"]
    _logpdf_const = (
        gammaln((_nu + 1) / 2.0) - gammaln(_nu / 2.0)
        - 0.5 * np.log(_nu * np.pi) - np.log(_scale)
    )
    _logpdf_alpha = (_nu + 1) / 2.0
    _logpdf_inv_nu = 1.0 / _nu

    def _fast_logpdf_sum(residuals):
        v = residuals[np.abs(residuals) < 100.0]
        z = (v - _loc) / _scale
        return _logpdf_const * len(v) - _logpdf_alpha * np.sum(
            np.log1p(_logpdf_inv_nu * z * z)
        )

    # ---- Run simulations ----
    print_status(f"\n--- Running {n_sims} true-D simulations ---", "TITLE")
    base_seed = cfg.get("monte_carlo", {}).get("seed", 900000)

    sim_results = []
    for sim_idx in range(n_sims):
        seed = base_seed + sim_idx + 200000  # Different from Gate 3
        rng = np.random.default_rng(seed)

        sim_blocks = []
        for i, block in enumerate(data_blocks):
            noise = student_t.rvs(
                df=_nu, loc=0.0, scale=block["err"] * _scale, random_state=rng,
            )
            sim_blocks.append({
                "wave": block["wave"], "flux": base_fluxes[i] + noise,
                "err": block["err"], "vsig": block["vsig"],
                "w_min": block["w_min"], "w_max": block["w_max"],
                "coadd": block["coadd"],
            })

        def obj_H(p):
            grouped = build_model_components(
                "M_H", theta_shared_base, p, pm, z_abs, c_kms,
                d_velocity_offset_kms=v_iso, parent_window_kms=parent_window,
            )
            cand = split_frozen_candidate(grouped, frozen_grouped)
            res = compute_residuals_fast(cand, sim_blocks, engine, frozen_cache)
            return -float(_fast_logpdf_sum(res))

        best_ll = -np.inf
        best_p = None
        for x0 in mc_starts:
            res_H = minimize(obj_H, x0, method="L-BFGS-B", bounds=bounds_H)
            if -res_H.fun > best_ll:
                best_ll = -res_H.fun
                best_p = res_H.x.copy()

        if best_p is not None:
            v_H_sim = best_p[0]
            logN_H_sim = best_p[1]
            # Compute total b from fitted T_K and b_turb (not just b_turb)
            T_K_sim = best_p[2]
            b_turb_sim = best_p[3]
            b_H_sim = compute_doppler_b(T_K_sim, b_turb_sim, isotope='H')
            sim_results.append({
                "v_H": float(v_H_sim), "logN_H": float(logN_H_sim),
                "b_H": float(b_H_sim),
                "b_ratio": float(b_H_sim / b_D_pred),
                "deviation": float(v_H_sim - v_expected_D),
                "logN_diff": float(logN_H_sim - logN_D_pred),
            })

        if (sim_idx + 1) % 25 == 0:
            print_status(f"  {sim_idx + 1}/{n_sims} done", "PROCESS")

    n_ok = len(sim_results)
    print_status(f"  Successful fits: {n_ok}/{n_sims}", "PROCESS")

    if n_ok < 10:
        print_status(f"  Too few successful fits — aborting", "ERROR")
        return

    # ---- Compute calibrated p-values ----
    print_status(f"\n--- Calibrated Gate 8 Statistics ---", "TITLE")

    sim_b_ratios = np.array([s["b_ratio"] for s in sim_results])
    sim_devs = np.array([s["deviation"] for s in sim_results])
    sim_logN_diffs = np.array([s["logN_diff"] for s in sim_results])

    obs_b_dev = abs(obs_b_ratio - 1.0)
    p_b = np.mean(np.abs(sim_b_ratios - 1.0) >= obs_b_dev)
    sigma_b = np.std(sim_b_ratios)
    nominal_b = obs_b_dev / sigma_b if sigma_b > 0 else float('inf')

    obs_abs_dev = abs(obs_deviation)
    p_dev = np.mean(np.abs(sim_devs) >= obs_abs_dev)
    sigma_dev = np.std(sim_devs)
    nominal_dev = obs_abs_dev / sigma_dev if sigma_dev > 0 else float('inf')

    obs_abs_logN = abs(obs_logN_diff)
    p_logN = np.mean(np.abs(sim_logN_diffs) >= obs_abs_logN)
    sigma_logN = np.std(sim_logN_diffs)
    nominal_logN = obs_abs_logN / sigma_logN if sigma_logN > 0 else float('inf')

    print_status(f"  {'Statistic':<25} {'Nominal σ':<12} {'Calibrated p':<15} {'Verdict'}", "PROCESS")
    print_status(f"  {'-'*25} {'-'*12} {'-'*15} {'-'*20}", "PROCESS")

    def verdict(p):
        if p < 0.05: return "SIGNIFICANT"
        if p < 0.10: return "MARGINAL"
        return "NOT SIGNIFICANT"

    print_status(f"  {'b-value ratio':<25} {nominal_b:<12.1f} {p_b:<15.3f} {verdict(p_b)}", "PROCESS")
    print_status(f"  {'Velocity deviation':<25} {nominal_dev:<12.1f} {p_dev:<15.3f} {verdict(p_dev)}", "PROCESS")
    print_status(f"  {'Column density':<25} {nominal_logN:<12.1f} {p_logN:<15.3f} {verdict(p_logN)}", "PROCESS")

    # Joint Mahalanobis
    obs_vec = np.array([obs_b_ratio, obs_deviation, obs_logN_diff])
    sim_vecs = np.array([[s["b_ratio"], s["deviation"], s["logN_diff"]] for s in sim_results])
    sim_mean = np.mean(sim_vecs, axis=0)
    sim_cov = np.cov(sim_vecs.T)
    # Regularize covariance to handle near-singular matrices from correlated statistics
    sim_cov += 1e-6 * np.eye(3)

    try:
        from scipy.linalg import pinv
        cov_inv = pinv(sim_cov)
        diff = obs_vec - sim_mean
        mahal_sq = float(diff @ cov_inv @ diff)
        sim_mahal = np.array([float((sv - sim_mean) @ cov_inv @ (sv - sim_mean)) for sv in sim_vecs])
        p_joint = float(np.mean(sim_mahal >= mahal_sq))
        print_status(f"  {'Joint (Mahalanobis)':<25} {'':12} {p_joint:<15.3f} {verdict(p_joint)}", "PROCESS")
    except Exception as e:
        print_status(f"  Mahalanobis failed: {e}", "PROCESS")
        p_joint = None
        mahal_sq = None

    # ---- Summary ----
    print_status(f"\n--- Key Finding ---", "TITLE")
    print_status(f"  The nominal sigma values were computed from spectral", "PROCESS")
    print_status(f"  resolution / measurement uncertainty. The calibrated", "PROCESS")
    print_status(f"  p-values show how extreme the observations are relative", "PROCESS")
    print_status(f"  to what true-D simulations actually produce.", "PROCESS")
    print_status(f"  ", "PROCESS")
    if p_joint is not None and p_joint < 0.05:
        print_status(f"  The joint statistic IS significant after calibration.", "SUCCESS")
        print_status(f"  The Gate 8 evidence survives the true-D injection test.", "SUCCESS")
    elif p_joint is not None and p_joint < 0.10:
        print_status(f"  The joint statistic is MARGINAL after calibration.", "PROCESS")
        print_status(f"  Some individual statistics may be inflated.", "PROCESS")
    else:
        print_status(f"  The joint statistic is NOT significant after calibration.", "PROCESS")
        print_status(f"  The nominal sigma values were inflated by not accounting", "PROCESS")
        print_status(f"  for the true-D null distribution.", "PROCESS")

    # ---- Save ----
    ledger = {
        "gate": "8-calibration",
        "sightline": sightline,
        "n_sims": n_sims, "n_successful": n_ok,
        "observed": {
            "v_H": float(v_H_obs), "b_H": float(b_H_obs), "logN_H": float(logN_H_obs),
            "b_ratio": float(obs_b_ratio), "deviation": float(obs_deviation),
            "logN_diff": float(obs_logN_diff),
        },
        "simulated_stats": {
            "b_ratio_mean": float(np.mean(sim_b_ratios)), "b_ratio_std": float(sigma_b),
            "deviation_mean": float(np.mean(sim_devs)), "deviation_std": float(sigma_dev),
            "logN_diff_mean": float(np.mean(sim_logN_diffs)), "logN_diff_std": float(sigma_logN),
        },
        "calibrated_p_values": {
            "b_value": float(p_b), "velocity_deviation": float(p_dev),
            "column_density": float(p_logN),
            "joint_mahalanobis": float(p_joint) if p_joint is not None else None,
        },
        "nominal_sigmas": {
            "b_value": float(nominal_b), "velocity_deviation": float(nominal_dev),
            "column_density": float(nominal_logN),
        },
        "mahalanobis_distance": float(mahal_sq) if mahal_sq is not None else None,
    }

    out_dir = project_root / "results"
    out_dir.mkdir(parents=True, exist_ok=True)
    sl_clean = sightline.replace("+", "").replace("-", "")
    out_file = out_dir / f"gate8_calibration_{sl_clean}.json"
    with open(out_file, "w") as f:
        json.dump(ledger, f, indent=2)
    print_status(f"\n[COMPLETED] {out_file}", "SUCCESS")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--sightline", default="Q1009+2956")
    parser.add_argument("--n-sims", type=int, default=200)
    args = parser.parse_args()
    run_gate8_calibration(args.sightline, args.n_sims)
