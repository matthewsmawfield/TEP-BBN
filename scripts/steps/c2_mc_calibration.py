#!/usr/bin/env python3
"""
C2': Freed-Scaffold Monte Carlo Calibration

Runs the freed-scaffold optimization inside the MC loop to calibrate
the p-value for the C2 statistic (T_scaffold = 73.86 for Q1009).

For each MC realization:
  1. Generate true-D synthetic data on the fixed scaffold
  2. Fit M_Dfree and M_Hfree with N freed scaffold components
  3. Compute T_scaffold = 2*(LL_H - LL_D)
  4. Count exceedances of T_scaffold_obs

Usage:
  python scripts/steps/c2_mc_calibration.py --sightline Q1009+2956 --n-sims 200
"""

import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

import json
import argparse
import numpy as np
import multiprocessing
from scipy.optimize import minimize
from scipy.stats import t as student_t

from scripts.utils.logger import print_status, setup_step_logger
from scripts.lib.model_builder import build_model_components
from scripts.lib.model_parser import ParameterManager, parse_vpfit_ties
from scripts.lib.physical_rt_engine import RadiativeTransferEngine
from scripts.lib.residual_engine import build_frozen_cache, compute_residuals, split_frozen_candidate
from scripts.lib.sightline_config import load_sightline_config
from scripts.steps.secondary_analyses import _load_pipeline_data, _make_fast_logpdf_sum


# ---------------------------------------------------------------------------
# Multiprocessing initializer: share data once per worker to avoid pickling
# the same ~1 MB of data per task.  Same pattern as step_03_significance.py.
# ---------------------------------------------------------------------------
_worker_shared = None

def _init_worker(shared_data):
    global _worker_shared
    _worker_shared = shared_data

np.seterr(all="ignore")

# Canonical transition lists (must match residual_engine / Gate 3 exactly).
_LYMAN = [
    'HI_Lya', 'HI_Lyb', 'HI_Lyg', 'HI_Lyd', 'HI_Lye',
    'HI_Ly6', 'HI_Ly7', 'HI_Ly8', 'HI_Ly9', 'HI_Ly10',
    'HI_Ly11', 'HI_Ly12', 'HI_Ly13', 'HI_Ly14', 'HI_Ly21',
]
_CIV = ['CIV_1548', 'CIV_1550']
_CIII = ['CIII_977']
_CII = ['CII_1334']
_SiIV = ['SiIV_1393', 'SiIV_1402']


def run_c2_mc_simulation(args):
    """Run a single C2 MC realization.

    Uses globally shared data (_worker_shared) when available (multiprocessing),
    or unpacks from args when running serially.
    """
    global _worker_shared
    if _worker_shared is not None:
        # Multiprocessing path: data shared via initializer
        (seed, starts_H, bounds_D, bounds_H,
         cfg_multistart_D,
         d_velocity_offset_kms, parent_window_kms, canonical_parent_idx,
         opt_D_obs, free_param_slices, n_cand_D, n_cand_H) = args
        data_blocks = _worker_shared['data_blocks']
        noise_cfg = _worker_shared['noise_cfg']
        pm = _worker_shared['pm']
        z_abs_ref = _worker_shared['z_abs_ref']
        c_kms = _worker_shared['c_kms']
        theta_shared_base = _worker_shared['theta_shared_base']
        engine = _worker_shared['engine']
        frozen_grouped = _worker_shared['frozen_grouped']
    else:
        # Serial path: all data in args
        (seed, data_blocks, noise_cfg, pm, z_abs_ref, c_kms,
         theta_shared_base, engine, starts_H, bounds_D, bounds_H,
         frozen_grouped, frozen_cache, cfg_multistart_D,
         d_velocity_offset_kms, parent_window_kms, canonical_parent_idx,
         opt_D_obs, free_param_slices, n_cand_D, n_cand_H) = args

    rng = np.random.default_rng(seed)
    _fast_logpdf_sum = _make_fast_logpdf_sum(noise_cfg)

    # Generate synthetic true-D data using the same forward model as Gate 3:
    #   1. Compute optical depth from ALL model components (shared + candidate D)
    #   2. Apply instrumental convolution to exp(-tau)
    #   3. Add per-pixel Student-t noise with scale = err * noise_cfg["scale"]
    #
    # The continuum is NOT baked into the generated flux — it is fit analytically
    # inside compute_residuals() during the likelihood evaluation, exactly as in
    # the observed-data fit and the Gate 3 MC loop.  This ensures the synthetic
    # data has the same statistical structure as the real data.
    grouped_D = build_model_components(
        "M_Dfree", theta_shared_base, opt_D_obs, pm, z_abs_ref, c_kms,
        d_velocity_offset_kms=d_velocity_offset_kms,
        parent_window_kms=parent_window_kms,
    )

    nu = noise_cfg["nu"]
    loc = noise_cfg["location"]
    scale = noise_cfg["scale"]

    noisy_blocks = []
    for block in data_blocks:
        tau_tot = np.zeros_like(block["wave"])
        if grouped_D["H_I"]:
            tau_tot += engine.compute_optical_depth(block["wave"], _LYMAN, grouped_D["H_I"])
        if grouped_D["D_I"]:
            tau_tot += engine.compute_optical_depth(block["wave"], _LYMAN, grouped_D["D_I"])
        if grouped_D["C_IV"]:
            tau_tot += engine.compute_optical_depth(block["wave"], _CIV, grouped_D["C_IV"])
        if grouped_D["C_III"]:
            tau_tot += engine.compute_optical_depth(block["wave"], _CIII, grouped_D["C_III"])
        if grouped_D["C_II"]:
            tau_tot += engine.compute_optical_depth(block["wave"], _CII, grouped_D["C_II"])
        if grouped_D["Si_IV"]:
            tau_tot += engine.compute_optical_depth(block["wave"], _SiIV, grouped_D["Si_IV"])
        base_flux = engine.apply_convolution(np.exp(-tau_tot), block["wave"], block["vsig"])

        # Per-pixel Student-t noise: scale = err * noise_cfg["scale"]
        # (matches Gate 3 and the noise model calibration).
        err = block["err"]
        noise = student_t.rvs(df=nu, loc=0.0, scale=err * scale, random_state=rng)
        sim_flux = base_flux + noise

        noisy_blocks.append({
            "wave": block["wave"],
            "flux": sim_flux,
            "err": block["err"],
            "vsig": block["vsig"],
            "w_min": block["w_min"],
            "w_max": block["w_max"],
            "coadd": block["coadd"],
        })

    # Fit M_Dfree with scaffold freedom (reduced starts for MC efficiency)
    # Use only the D-optimal start (from observed fit) — the MC is calibrating
    # the null distribution, not searching for the global optimum
    mc_starts_D = [list(opt_D_obs)] if opt_D_obs is not None else [cfg_multistart_D[0]]
    best_ll_D = -np.inf
    for x0 in mc_starts_D:
        scaffold_init = []
        for n_idx, b_idx in free_param_slices:
            scaffold_init.extend([theta_shared_base[n_idx], theta_shared_base[b_idx]])
        x0_ext = list(x0) + scaffold_init
        bounds_D_ext = bounds_D + [(10.0, 20.0), (1.0, 50.0)] * len(free_param_slices)

        def obj_D(p):
            cand_params = p[:n_cand_D]
            scaffold_params = p[n_cand_D:]
            theta_mod = theta_shared_base.copy()
            for i, (n_idx, b_idx) in enumerate(free_param_slices):
                theta_mod[n_idx] = scaffold_params[i*2]
                theta_mod[b_idx] = scaffold_params[i*2+1]
            grouped = build_model_components(
                "M_Dfree", theta_mod, cand_params, pm, z_abs_ref, c_kms,
                d_velocity_offset_kms=d_velocity_offset_kms,
                parent_window_kms=parent_window_kms,
            )
            res = compute_residuals(grouped, noisy_blocks, engine)
            return -_fast_logpdf_sum(res)

        r = minimize(obj_D, x0_ext, method="L-BFGS-B", bounds=bounds_D_ext,
                     options={"maxiter": 100, "ftol": 1e-6})
        if -r.fun > best_ll_D:
            best_ll_D = -r.fun

    # Fit M_Hfree with scaffold freedom (reduced starts for MC efficiency)
    # Use only 1 H-start (vs 20 in the observed fit) — sufficient for MC calibration
    # where the goal is to calibrate the null distribution, not find the global optimum
    mc_starts_H = starts_H[:1] if len(starts_H) > 0 else starts_H
    best_ll_H = -np.inf
    for x0 in mc_starts_H:
        scaffold_init = []
        for n_idx, b_idx in free_param_slices:
            scaffold_init.extend([theta_shared_base[n_idx], theta_shared_base[b_idx]])
        x0_ext = list(x0) + scaffold_init
        bounds_H_ext = bounds_H + [(10.0, 20.0), (1.0, 50.0)] * len(free_param_slices)

        def obj_H(p):
            cand_params = p[:n_cand_H]
            scaffold_params = p[n_cand_H:]
            theta_mod = theta_shared_base.copy()
            for i, (n_idx, b_idx) in enumerate(free_param_slices):
                theta_mod[n_idx] = scaffold_params[i*2]
                theta_mod[b_idx] = scaffold_params[i*2+1]
            grouped = build_model_components(
                "M_H", theta_mod, cand_params, pm, z_abs_ref, c_kms,
                d_velocity_offset_kms=d_velocity_offset_kms,
                parent_window_kms=parent_window_kms,
            )
            res = compute_residuals(grouped, noisy_blocks, engine)
            return -_fast_logpdf_sum(res)

        r = minimize(obj_H, x0_ext, method="L-BFGS-B", bounds=bounds_H_ext,
                     options={"maxiter": 100, "ftol": 1e-6})
        if -r.fun > best_ll_H:
            best_ll_H = -r.fun

    T_sim = 2.0 * (best_ll_H - best_ll_D)
    return T_sim


def main():
    parser = argparse.ArgumentParser(description="C2' Freed-Scaffold MC Calibration")
    parser.add_argument("--sightline", default="Q1009+2956")
    parser.add_argument("--n-sims", type=int, default=200)
    parser.add_argument("--n-free", type=int, default=5)
    args = parser.parse_args()

    setup_step_logger(Path(__file__).stem)
    print_status(f"=== C2': FREED-SCAFFOLD MC CALIBRATION ({args.sightline}) ===", "SUCCESS")
    print_status(f"N_sims: {args.n_sims}, N_free_components: {args.n_free}", "PROCESS")

    cfg, manifest, noise_cfg, z_abs_ref, c_kms, pm, engine, data_blocks, g2, opt_D_obs, theta_shared_base = _load_pipeline_data(args.sightline)

    # Load observed T_scaffold
    output_prefix = cfg.get("output_prefix", "gate")
    c2_path = project_root / "results" / f"{output_prefix}3_c2_scaffold_freedom.json"
    with open(c2_path) as f:
        c2 = json.load(f)
    T_obs = c2["T_scaffold"]
    print_status(f"Observed T_scaffold: {T_obs:.2f}", "PROCESS")

    # Identify freed components (same logic as run_c2_limited_scaffold)
    parent_window = cfg["parent_window_kms"]
    comps = pm.reconstruct(theta_shared_base)
    h_comps = [(i, c) for i, c in enumerate(comps) if c["ion"] == "H_I"]
    d_zs = set(round(c["z"], 10) for c in comps if c["ion"] == "D_I")
    d_parent_indices = set()
    for i, c in enumerate(comps):
        if c["ion"] == "H_I" and round(c["z"], 10) in d_zs:
            d_parent_indices.add(i)
    h_comps_absorber = []
    for i, c in h_comps:
        v = c_kms * (c["z"] - z_abs_ref) / (1.0 + z_abs_ref)
        if abs(v) <= parent_window and i not in d_parent_indices:
            h_comps_absorber.append((i, c))
    h_comps_sorted = sorted(h_comps_absorber, key=lambda x: x[1]["logN"], reverse=True)
    free_indices = set(x[0] for x in h_comps_sorted[:args.n_free])
    # Map each freed component to its actual theta indices via pm.comp_map.
    # The naive idx*3 mapping is WRONG — ParameterManager uses ties.
    free_param_slices = []  # list of (logN_theta_idx, b_theta_idx) tuples
    for idx in sorted(free_indices):
        cmap = pm.comp_map[idx]
        n_idx = cmap.get('N_idx')
        if n_idx is None:
            raise ValueError(f"Component {idx} has no free N_idx — cannot free")
        b_idx = cmap.get('b_idx')
        if b_idx is None:
            b_idx = cmap.get('b_turb_idx')
            if b_idx is None:
                raise ValueError(f"Component {idx} has no free b or b_turb_idx — cannot free")
        free_param_slices.append((n_idx, b_idx))

    # Get bounds and starts
    cb = cfg["candidate_bounds"]
    bounds_D = [tuple(b) for b in cb["M_Dfree"]["bounds"]]
    bounds_H = [tuple(b) for b in cb["M_Hfree"]["bounds"]]
    starts_H = cfg.get("multistart", {}).get("M_Hfree", [cb["M_Hfree"]["init"]])
    starts_D = cfg.get("multistart", {}).get("M_Dfree", [cb["M_Dfree"]["init"]])
    n_cand_D = len(bounds_D)
    n_cand_H = len(bounds_H)

    # Build frozen cache for D generation
    frozen_grouped = build_model_components(
        "M_NULL", theta_shared_base, None, pm, z_abs_ref, c_kms,
        d_velocity_offset_kms=cfg["d_velocity_offset_kms"],
        parent_window_kms=parent_window,
    )

    # Prepare shared data for multiprocessing initializer
    shared_data = {
        'data_blocks': data_blocks,
        'noise_cfg': noise_cfg,
        'pm': pm,
        'z_abs_ref': z_abs_ref,
        'c_kms': c_kms,
        'theta_shared_base': theta_shared_base,
        'engine': engine,
        'frozen_grouped': frozen_grouped,
    }

    # Prepare args (only per-task data, not shared data)
    base_seed = cfg.get("mc_seed", 910000)
    sim_args = [
        (base_seed + i, starts_H, bounds_D, bounds_H,
         starts_D, cfg["d_velocity_offset_kms"],
         parent_window, 0, opt_D_obs, free_param_slices, n_cand_D, n_cand_H)
        for i in range(args.n_sims)
    ]

    # Run simulations.  Use multiprocessing with fork start method (faster
    # than spawn on macOS/Linux) when n_sims is large enough to justify
    # the overhead; run serially for small n_sims.
    n_workers = min(multiprocessing.cpu_count(), args.n_sims)
    if args.n_sims <= 20:
        print_status(f"Running {args.n_sims} sims serially (small N)...", "PROCESS")
        # Set shared data for serial execution
        global _worker_shared
        _worker_shared = shared_data
        T_sims = [run_c2_mc_simulation(arg) for arg in sim_args]
    else:
        print_status(f"Running {args.n_sims} sims on {n_workers} workers (fork)...", "PROCESS")
        ctx = multiprocessing.get_context('fork')
        with ctx.Pool(
            processes=n_workers,
            initializer=_init_worker,
            initargs=(shared_data,),
        ) as pool:
            T_sims = pool.map(run_c2_mc_simulation, sim_args)

    T_sims = np.array(T_sims)
    exceedances = np.sum(T_sims >= T_obs)
    p_value = (exceedances + 1) / (args.n_sims + 1)  # Laplace-corrected

    print_status(f"Exceedances: {exceedances}/{args.n_sims}", "PROCESS")
    print_status(f"p_C2 (Laplace): {p_value:.6f}", "PROCESS")
    print_status(f"T_sim range: [{T_sims.min():.2f}, {T_sims.max():.2f}]", "PROCESS")
    print_status(f"T_sim median: {np.median(T_sims):.2f}", "PROCESS")

    # Save results
    out_path = project_root / "results" / f"{output_prefix}3_c2_mc_calibration.json"
    with open(out_path, "w") as f:
        json.dump({
            "sightline": cfg["sightline_id"],
            "analysis": "C2_freed_scaffold_MC_calibration",
            "n_sims": args.n_sims,
            "n_free_components": args.n_free,
            "T_obs": float(T_obs),
            "exceedances": int(exceedances),
            "p_value": float(p_value),
            "T_sim_min": float(T_sims.min()),
            "T_sim_max": float(T_sims.max()),
            "T_sim_median": float(np.median(T_sims)),
            "T_sim_mean": float(np.mean(T_sims)),
        }, f, indent=2)
    print_status(f"Saved to {out_path}", "SUCCESS")


if __name__ == "__main__":
    main()
