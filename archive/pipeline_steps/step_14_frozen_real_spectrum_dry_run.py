"""
Phase 4B-0.5: Frozen Real-Spectrum Dry Run
"""

import sys
from pathlib import Path
import json
import numpy as np

script_dir = Path(__file__).parent
project_root = script_dir.parent.parent
sys.path.insert(0, str(project_root))

from scripts.steps.step_13c_nested_synthetic_adversarial_validation import (
    base_model,
    fit_model_nested,
    classify_result,
    c_kms, components, hi_comps, primary_idx
)

# 1. Real-Data Manifest (Frozen)
MANIFEST = {
    "target": "Q0913+072",
    "absorber_redshift": 2.61843,
    "input_file_path": str(project_root / "data/processed/Q0913+072_1D_spectrum.txt"),
    "flux_column": 1,
    "noise_column": 2,
    "velocity_column": 0,
    "wavelength_convention": "velocity_kms",
    "normalization_state": "continuum_normalized",
    "Lyman_windows": "[-300, 100] km/s relative to z=2.61843",
    "masked_regions": [],
    "LSF_assumptions": "Gaussian, b=3.0 km/s",
    "pixel_scale": "2.0 km/s",
    "commit_hash": "189b506",
    "claim_allowed": False
}

def load_real_data():
    path = Path(MANIFEST["input_file_path"])
    if not path.exists():
        raise FileNotFoundError(f"Real spectrum not found at {path}")
        
    data = np.loadtxt(path)
    v_grid = data[:, MANIFEST["velocity_column"]]
    flux = data[:, MANIFEST["flux_column"]]
    noise = data[:, MANIFEST["noise_column"]]
    
    return v_grid, flux, noise

def run_frozen_pipeline():
    print("Phase 4B-0.5: Frozen Real-Spectrum Dry Run")
    print("=" * 60)
    print("Manifest:")
    print(json.dumps(MANIFEST, indent=2))
    
    v_grid, flux, noise = load_real_data()
    print(f"Data loaded successfully. Length: {len(flux)}")
    
    # We replace v_grid in step_13c so the base_model evaluates correctly
    import scripts.steps.step_13c_nested_synthetic_adversarial_validation as step13
    step13.v_grid = v_grid
    step13.x_norm = (v_grid - v_grid[0]) / (v_grid[-1] - v_grid[0]) * 2.0 - 1.0

    print("Running nested sampling on real data...")
    
    models = ['Mnull', 'M0', 'M1_full', 'M1_primary_only', 'M2_full', 'M2_primary_only', 'M2_free_alpha', 'M3_global', 'M3_Dlocal']
    logZs = {}
    logZerrs = {}
    posteriors = {}
    
    for m in models:
        print(f"  Fitting {m}...")
        lz, lzerr, pdiag = fit_model_nested(flux, m, noise)
        logZs[m] = lz
        logZerrs[m] = lzerr
        posteriors[m] = pdiag
        
    v_int_samples = np.array(posteriors['M3_Dlocal']['v_int_samples'])
    v_int_weights = np.array(posteriors['M3_Dlocal']['weights'])
    v_hat = np.average(v_int_samples, weights=v_int_weights)
    sigma_v = np.sqrt(np.average((v_int_samples - v_hat)**2, weights=v_int_weights))
    half_width = max(1.0, 3 * sigma_v)
    centroid_bounds = [v_hat - half_width, v_hat + half_width]
    
    alpha_blind_interval = [0.0005, 0.0009]
    g_primary = components[primary_idx]['g_i']
    sec_windows_raw = []
    w_sec = max(1.0, 3 * sigma_v, 3.0)
    for i, hc in enumerate(hi_comps):
        if i == primary_idx: continue
        g_i = components[i]['g_i']
        s1 = c_kms * alpha_blind_interval[0] * (g_i - g_primary)
        s2 = c_kms * alpha_blind_interval[1] * (g_i - g_primary)
        v_base = hc['v'] - 82.0
        v_min = v_base + min(s1, s2)
        v_max = v_base + max(s1, s2)
        sec_windows_raw.append([v_min - w_sec, v_max + w_sec])
    
    sec_windows_raw.sort(key=lambda x: x[0])
    merged_windows = []
    for w in sec_windows_raw:
        if not merged_windows:
            merged_windows.append(w)
        else:
            last = merged_windows[-1]
            if w[0] <= last[1]:
                merged_windows[-1] = [last[0], max(last[1], w[1])]
            else:
                merged_windows.append(w)
                
    print(f"  Fitting M3_centroid...")
    lz, lzerr, pdiag = fit_model_nested(flux, 'M3_centroid', noise, centroid_bounds=centroid_bounds)
    logZs['M3_centroid'] = lz
    logZerrs['M3_centroid'] = lzerr
    posteriors['M3_centroid'] = pdiag
    
    print(f"  Fitting M4_secondary_local...")
    lz, lzerr, pdiag = fit_model_nested(flux, 'M4_secondary_local', noise, centroid_bounds=centroid_bounds, sec_windows=merged_windows)
    logZs['M4_secondary_local'] = lz
    logZerrs['M4_secondary_local'] = lzerr
    posteriors['M4_secondary_local'] = pdiag
    
    # Held-out validation
    held_out_diff = 0.0
    if 'M2_primary_only' in posteriors:
        ml_sample = posteriors['M2_primary_only']['ml_sample']
        p_ml = {'c0': ml_sample[0], 'c1': ml_sample[1], 'c2': ml_sample[2], 
                'v_shift': ml_sample[3], 'lsf_scale': ml_sample[4],
                'B_abs': ml_sample[5], 'f_D': ml_sample[6], 'alpha': ml_sample[7]}
        flux_null = base_model(p_ml, tep_primary_only=True)
        flux_pred = base_model(p_ml, tep_primary_only=False)
        sec_mask = np.zeros(len(v_grid), dtype=bool)
        for w in merged_windows:
            sec_mask |= (v_grid >= w[0]) & (v_grid <= w[1])
        logL_null_sec = -0.5 * np.sum(((flux[sec_mask] - flux_null[sec_mask]) / noise[sec_mask])**2)
        logL_pred_sec = -0.5 * np.sum(((flux[sec_mask] - flux_pred[sec_mask]) / noise[sec_mask])**2)
        held_out_diff = logL_pred_sec - logL_null_sec
        posteriors['held_out_diff'] = float(held_out_diff)
        
    print("\n" + "="*60)
    print("RESULTS:")
    for m in logZs:
        print(f"{m:20s}: logZ = {logZs[m]:.2f} ± {logZerrs[m]:.2f}")
        
    print(f"\nHeld out diff: {held_out_diff:.2f}")
    if 'M2_full' in posteriors and 'f_D_mean' in posteriors['M2_full']:
        print(f"M2_full f_D_mean: {posteriors['M2_full']['f_D_mean']:.3f}")
        print(f"M2_full P(f_D < 0.5): {posteriors['M2_full']['P_f_D_lt_0p5']:.3f}")
        
    # Evaluate Gate
    is_tep_win, classification, reason = classify_result(logZs, logZerrs, posteriors)
    
    print("\nGATE PASSED:", is_tep_win)
    print("CLASSIFICATION:", classification)
    print("REASON:", reason)
    
    result_dict = {
        "system": MANIFEST["target"],
        "classification": classification,
        "gate_passed": bool(is_tep_win),
        "interpretation": reason,
        "velocity_width": None,  # To be populated by catalog scale
        "component_count": len(components),
        "primary_secondary_separation": None,
        "delta_m2_vs_m0": logZs.get('M2_full', 0) - logZs.get('M0', 0),
        "delta_m2_vs_m4": logZs.get('M2_full', 0) - logZs.get('M4_secondary_local', 0),
        "held_out_diff": float(held_out_diff)
    }
    
    out_path = project_root / f"data/processed/{MANIFEST['target']}_result.json"
    with open(out_path, 'w') as f:
        json.dump(result_dict, f, indent=2)
    print(f"\nResult archived to {out_path}")

if __name__ == '__main__':
    run_frozen_pipeline()
