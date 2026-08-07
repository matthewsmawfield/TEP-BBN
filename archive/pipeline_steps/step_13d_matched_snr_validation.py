import sys
import json
from pathlib import Path
import numpy as np
from datetime import datetime
from joblib import Parallel, delayed

script_dir = Path(__file__).parent
project_root = script_dir.parent.parent
sys.path.insert(0, str(project_root))

from scripts.steps.step_13c_nested_synthetic_adversarial_validation import (
    base_model, fit_model_nested, classify_result, set_system_feature_vector
)
import scripts.steps.step_13c_nested_synthetic_adversarial_validation as step13

def generate_synthetic_data(snr, tep_alpha=0.0):
    # Base parameters matching Q1009
    params = {
        'c0': 1.0, 'c1': 0.0, 'c2': 0.0,
        'v_shift': 0.0, 'lsf_scale': 1.0,
        'B_abs': 1.0, 'f_D': 0.8
    }
    
    if tep_alpha > 0:
        params['alpha'] = tep_alpha
        flux_clean = base_model(params, tep_primary_only=False)
    else:
        # Null model (standard physics)
        flux_clean = base_model(params, tep_primary_only=True)
        
    noise = np.ones_like(flux_clean) / snr
    flux_noisy = flux_clean + np.random.normal(0, noise)
    return flux_noisy, noise

def run_single_trial(snr, tep_alpha, seed):
    np.random.seed(seed)
    flux, noise = generate_synthetic_data(snr, tep_alpha)
    
    models = ['Mnull', 'M0', 'M1_full', 'M1_primary_only', 'M2_full', 'M2_primary_only', 'M2_free_alpha', 'M3_global', 'M3_Dlocal']
    logZs = {}
    logZerrs = {}
    posteriors = {}
    
    for m in models:
        lz, lzerr, pdiag = fit_model_nested(flux, m, noise)
        logZs[m] = lz
        logZerrs[m] = lzerr
        posteriors[m] = pdiag
        
    # Simplified Dlocal and M4 for speed in this test (since it's mostly about proving we can reject nulls)
    # Actually, we MUST run M4 to get the gate to pass.
    v_int_samples = np.array(posteriors['M3_Dlocal']['v_int_samples'])
    v_int_weights = np.array(posteriors['M3_Dlocal']['weights'])
    v_hat = np.average(v_int_samples, weights=v_int_weights)
    sigma_v = np.sqrt(np.average((v_int_samples - v_hat)**2, weights=v_int_weights))
    half_width = max(1.0, 3 * sigma_v)
    centroid_bounds = [v_hat - half_width, v_hat + half_width]
    
    c_kms = 299792.458
    alpha_blind_interval = [0.0005, 0.0009]
    g_primary = step13.components[step13.primary_idx]['g_i']
    sec_windows_raw = []
    w_sec = max(1.0, 3 * sigma_v, 3.0)
    for i, hc in enumerate(step13.hi_comps):
        if i == step13.primary_idx: continue
        g_i = step13.components[i]['g_i']
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
                
    lz, lzerr, pdiag = fit_model_nested(flux, 'M3_centroid', noise, centroid_bounds=centroid_bounds)
    logZs['M3_centroid'] = lz
    logZerrs['M3_centroid'] = lzerr
    posteriors['M3_centroid'] = pdiag
    
    if not merged_windows:
        logZs['M4_secondary_local'] = -1e9
        logZerrs['M4_secondary_local'] = 0.0
        posteriors['M4_secondary_local'] = {}
    else:
        lz, lzerr, pdiag = fit_model_nested(flux, 'M4_secondary_local', noise, centroid_bounds=centroid_bounds, sec_windows=merged_windows)
        logZs['M4_secondary_local'] = lz
        logZerrs['M4_secondary_local'] = lzerr
        posteriors['M4_secondary_local'] = pdiag

    # Held-out diff
    held_out_diff = 0.0
    if 'M2_primary_only' in posteriors:
        ml_sample = posteriors['M2_primary_only']['ml_sample']
        p_ml = {'c0': ml_sample[0], 'c1': ml_sample[1], 'c2': ml_sample[2], 
                'v_shift': ml_sample[3], 'lsf_scale': ml_sample[4],
                'B_abs': ml_sample[5], 'f_D': ml_sample[6], 'alpha': ml_sample[7]}
        flux_null = base_model(p_ml, tep_primary_only=True)
        flux_pred = base_model(p_ml, tep_primary_only=False)
        sec_mask = np.zeros(len(step13.v_grid), dtype=bool)
        for w in merged_windows:
            sec_mask |= (step13.v_grid >= w[0]) & (step13.v_grid <= w[1])
        if np.any(sec_mask):
            logL_null_sec = -0.5 * np.sum(((flux[sec_mask] - flux_null[sec_mask]) / noise[sec_mask])**2)
            logL_pred_sec = -0.5 * np.sum(((flux[sec_mask] - flux_pred[sec_mask]) / noise[sec_mask])**2)
            held_out_diff = logL_pred_sec - logL_null_sec
        posteriors['held_out_diff'] = float(held_out_diff)
        
    is_tep_win, classification, reason = classify_result(logZs, logZerrs, posteriors)
    return is_tep_win, classification, reason

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true', help="Run small sample")
    args = parser.parse_args()
    
    prov_path = project_root / "data/processed/Q1009+2956_z2.504_spectrum_provenance.json"
    fv_path = project_root / "data/processed/measured_feature_vector_Q1009+2956_z2.504.json"
    
    with open(prov_path, "r") as f:
        prov = json.load(f)
    with open(fv_path, "r") as f:
        fv = json.load(f)
        
    snr = prov['median_snr']
    print(f"Matched SNR: {snr:.1f}")
    
    set_system_feature_vector(fv)
    
    step13.v_grid = np.loadtxt(project_root / "data/processed/Q1009+2956_z2.504_1D_spectrum.txt", skiprows=1)[:,0]
    step13.x_norm = (step13.v_grid - step13.v_grid[0]) / (step13.v_grid[-1] - step13.v_grid[0]) * 2.0 - 1.0
    
    n_null = 10 if args.debug else 100
    n_inj = 10 if args.debug else 100
    
    print(f"Running {n_null} null trials...")
    null_results = Parallel(n_jobs=-1)(
        delayed(run_single_trial)(snr, 0.0, seed) for seed in range(n_null)
    )
    
    null_fpr = sum(1 for r in null_results if r[1] == "TEP_CANDIDATE") / len(null_results)
    print(f"Null False Positive Rate: {null_fpr:.3f}")
    
    print(f"Running {n_inj} injection trials (alpha=0.0007)...")
    inj_results = Parallel(n_jobs=-1)(
        delayed(run_single_trial)(snr, 0.0007, 1000 + seed) for seed in range(n_inj)
    )
    
    inj_tpr = sum(1 for r in inj_results if r[1] == "TEP_CANDIDATE") / len(inj_results)
    print(f"Injection True Positive Rate: {inj_tpr:.3f}")
    
    status = "INFORMATIVE_NEGATIVE" if (null_fpr == 0.0 and inj_tpr > 0.8) else "INCONCLUSIVE_LOW_POWER"
    
    if args.debug:
        print("Debug run complete. Did not pass power threshold (TPR > 0.8).")
        
    out_data = {
        "system_id": "Q1009+2956_z2.504",
        "snr": snr,
        "n_null": n_null,
        "null_fpr": null_fpr,
        "n_injection": n_inj,
        "injection_tpr": inj_tpr,
        "status": status,
        "timestamp": datetime.now().isoformat()
    }
    
    with open(project_root / "data/processed/Q1009+2956_power_validation.json", "w") as f:
        json.dump(out_data, f, indent=2)
        
    print(f"Validation complete. Status: {status}")

if __name__ == '__main__':
    main()
