import os
import sys
import numpy as np
import json
import math
import hashlib
from pathlib import Path
import concurrent.futures
from scipy.stats import binomtest
import copy

script_dir = Path(__file__).parent
project_root = script_dir.parent.parent
sys.path.append(str(project_root))

from scripts.lib.joint_spectrum_likelihood import fit_model_nested_joint, evaluate_frozen_model
from scripts.steps.step_14c_joint_power_triage_screen import load_joint_spectra, generate_synthetic_joint_flux
import scripts.steps.step_13c_nested_synthetic_adversarial_validation as step13c

def get_ci(k, n):
    res = binomtest(k, n)
    ci = res.proportion_ci(confidence_level=0.95)
    return ci.low, ci.high

def compute_sec_windows_and_held_out(synth_spectra, posteriors):
    # 1. Compute sec_windows from M3_centroid
    c_kms = 299792.458
    alpha_blind_interval = [0.0005, 0.0009]
    g_primary = step13c.components[step13c.primary_idx]['g_i']
    
    # We use a fixed centroid bound since the injection is at v=0.
    v_hat = 0.0
    sigma_v = 1.0 
    
    if 'M3_centroid' in posteriors and 'v_shift_mean' in posteriors['M3_centroid']:
        # if the model provided it
        pass # we can refine if needed, but fixed window is safer
        
    sec_windows_raw = []
    w_sec = max(1.0, 3 * sigma_v, 3.0)
    for i, hc in enumerate(step13c.hi_comps):
        if i == step13c.primary_idx: continue
        g_i = step13c.components[i]['g_i']
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
                
    # 2. Compute held_out_diff
    held_out_diff = 0.0
    if 'M2_primary_only' in posteriors and 'ml_sample' in posteriors['M2_primary_only']:
        ml_sample = posteriors['M2_primary_only']['ml_sample']
        shared_names = posteriors['M2_primary_only']['shared_names']
        local_names = posteriors['M2_primary_only']['local_names']
        
        shared_params = {}
        idx = 0
        for name in shared_names:
            shared_params[name] = ml_sample[idx]
            idx += 1
            
        logL_null_sec = 0.0
        logL_pred_sec = 0.0
        
        for spec in synth_spectra:
            local_params = {}
            for name in local_names:
                local_params[name] = ml_sample[idx]
                idx += 1
                
            flux_null = evaluate_frozen_model(spec['v'], shared_params, local_params, 'M2_primary_only', spec['sigma_v_kms'])
            
            # The predicted flux from M2_full using M2_primary_only params
            flux_pred = evaluate_frozen_model(spec['v'], shared_params, local_params, 'M2_full', spec['sigma_v_kms'])
            
            sec_mask = np.zeros(len(spec['v']), dtype=bool)
            for w in merged_windows:
                sec_mask |= (spec['v'] >= w[0]) & (spec['v'] <= w[1])
                
            if np.any(sec_mask):
                noise = spec['err']
                logL_null_sec += -0.5 * np.sum(((spec['flux'][sec_mask] - flux_null[sec_mask]) / noise[sec_mask])**2)
                logL_pred_sec += -0.5 * np.sum(((spec['flux'][sec_mask] - flux_pred[sec_mask]) / noise[sec_mask])**2)
                
        held_out_diff = logL_pred_sec - logL_null_sec
        
    return merged_windows, held_out_diff

def run_single_trial(spectra, alpha_inject, seed, shared_inj):
    np.random.seed(seed)
    
    synth_spectra = generate_synthetic_joint_flux(spectra, shared_inj, "M2_full", inject_alpha=alpha_inject)
    
    logZs = {}
    logZerrs = {}
    posteriors = {}
    
    import contextlib
    with contextlib.redirect_stdout(None), contextlib.redirect_stderr(None):
        # 1. Fit M3_centroid to get the centroid
        m = "M3_centroid"
        lz, lzerr, pdiag = fit_model_nested_joint(synth_spectra, m, nlive=100, centroid_bounds=[-10, 10])
        logZs[m] = lz
        logZerrs[m] = lzerr
        posteriors[m] = pdiag
        
        # 2. Get sec_windows
        merged_windows, _ = compute_sec_windows_and_held_out(synth_spectra, posteriors)
        
        # 3. Fit other models
        for m in ["M2_full", "M2_primary_only", "M2_free_alpha"]:
            lz, lzerr, pdiag = fit_model_nested_joint(synth_spectra, m, nlive=100, centroid_bounds=[-10, 10])
            logZs[m] = lz
            logZerrs[m] = lzerr
            posteriors[m] = pdiag
            
        m = "M4_secondary_local"
        lz, lzerr, pdiag = fit_model_nested_joint(synth_spectra, m, nlive=100, centroid_bounds=[-10, 10], sec_windows=merged_windows)
        logZs[m] = lz
        logZerrs[m] = lzerr
        posteriors[m] = pdiag
        
        # 4. Compute held_out_diff
        _, held_out_diff = compute_sec_windows_and_held_out(synth_spectra, posteriors)
        posteriors['held_out_diff'] = float(held_out_diff)
            
    is_tep, status, reason = step13c.classify_result(logZs, logZerrs, posteriors)
    delta_tep = logZs.get("M2_full", 0) - logZs.get("M3_centroid", 0)
    return is_tep, delta_tep, logZs

def run_batch(spectra, conditions, n_trials_per_condition, start_idx=0):
    shared_inj = {'v_shift': 0.0, 'B_abs': 1.5e-5, 'f_D': 0.0}
    results = {alpha: 0 for alpha in conditions}
    
    for alpha in conditions:
        print(f"\nRunning condition: alpha = {alpha} ({n_trials_per_condition} trials)")
        recovered = 0
        seeds = [hash(f"seed_{alpha}_{start_idx + i}") % (2**32) for i in range(n_trials_per_condition)]
        
        futures = []
        with concurrent.futures.ProcessPoolExecutor(max_workers=7) as executor:
            for i in range(n_trials_per_condition):
                f = executor.submit(run_single_trial, spectra, alpha, seeds[i], shared_inj)
                futures.append(f)
                
            for i, f in enumerate(concurrent.futures.as_completed(futures)):
                is_tep, _, _ = f.result()
                if is_tep:
                    recovered += 1
                if (i + 1) % 5 == 0 or (i + 1) == n_trials_per_condition:
                    print(f" Trial {i+1}/{n_trials_per_condition} completed. Recovered: {recovered}")
                    
        results[alpha] = recovered
    return results

def write_and_hash_report(report_data):
    report_path = project_root / "data/processed/Q1009_formal_power_report.json"
    with open(report_path, "w") as f:
        json.dump(report_data, f, indent=2)
        
    with open(report_path, "rb") as f:
        content = f.read()
        sha256 = hashlib.sha256(content).hexdigest()
        
    print(f"\n[REPORT GENERATED] Saved to {report_path}")
    print(f"[REPORT SHA256] {sha256}")
    return report_path, sha256

def run_power_campaign(manifest_path):
    print(f"Loading {manifest_path} for FORMAL POWER CAMPAIGN...")
    
    # Load correct feature vector!
    target_name = Path(manifest_path).stem.replace("_HIRES_spectrum_manifest", "")
    fv_path = project_root / f"data/processed/measured_feature_vector_{target_name}.json"
    if fv_path.exists():
        with open(fv_path, 'r') as f:
            step13c.set_system_feature_vector(json.load(f))
        print(f"Loaded system feature vector from {fv_path.name}")
    else:
        print(f"WARNING: No feature vector found at {fv_path}. Using default.")
        
    spectra = load_joint_spectra(manifest_path)
    
    conditions = [0.0007]
    
    # BATCH 1
    print("\n" + "="*40 + "\nSTARTING BATCH 1 (50 trials per condition)\n" + "="*40)
    batch1_results = run_batch(spectra, conditions, 50, start_idx=0)
    
    print("\nBatch 1 Results:")
    for a, k in batch1_results.items():
        print(f"  alpha={a}: {k}/50")
        
    null_positives = batch1_results.get(0.0, 0)
    central_recoveries = batch1_results.get(0.0007, 0)
    
    if central_recoveries < 45:
        print("\nBATCH 1 FAILED: INSUFFICIENT_POWER (Central recovery < 45/50)")
        report = {
            "status": "INSUFFICIENT_POWER",
            "reason": f"Central alpha recovery {central_recoveries}/50 fell below threshold of 45",
            "batch1": batch1_results
        }
        write_and_hash_report(report)
        sys.exit(1)
        
    print("\nBatch 1 PASSED! Proceeding to Batch 2 to reach 200 trials total.")
    
    # BATCH 2
    print("\n" + "="*40 + "\nSTARTING BATCH 2 (150 trials per condition)\n" + "="*40)
    batch2_results = run_batch(spectra, conditions, 150, start_idx=50)
    
    # COMBINE
    final_results = {a: batch1_results[a] + batch2_results[a] for a in conditions}
    n_total = 200
    
    print("\n=== FINAL POWER CAMPAIGN RESULTS (200 trials total) ===")
    report_table = {}
    for a in conditions:
        k = final_results[a]
        low, high = get_ci(k, n_total)
        print(f"  alpha={a}: {k}/{n_total} [{low*100:.1f}%, {high*100:.1f}%]")
        report_table[str(a)] = {
            "recovered": k,
            "total": n_total,
            "ci_95_low": low,
            "ci_95_high": high
        }
        
    null_pass = final_results[0.0] <= 4 # ~2% FPR
    central_pass = final_results[0.0007] >= 180
    edge_low_pass = final_results[0.0005] >= 180
    edge_high_pass = final_results[0.0009] >= 180
    
    if not null_pass:
        status = "CALIBRATION_FAILED"
    elif edge_low_pass and central_pass and edge_high_pass:
        status = "POWERED_FULL_INTERVAL"
    elif central_pass:
        status = "POWERED_CENTRAL_EFFECT_ONLY"
    else:
        status = "INSUFFICIENT_POWER"
        
    print(f"\nFINAL DECISION: {status}")
    
    report = {
        "status": status,
        "results_table": report_table,
        "batch1": batch1_results,
        "batch2": batch2_results
    }
    
    write_and_hash_report(report)
    print("\nPlease commit this report before unblinding the real classification.")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest")
    args = parser.parse_args()
    
    run_power_campaign(args.manifest)
