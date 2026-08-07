import os
import sys
import numpy as np
import json
import time
import concurrent.futures
from pathlib import Path

script_dir = Path(__file__).parent
project_root = script_dir.parent.parent
sys.path.append(str(project_root))

from scripts.steps.step_14c_joint_power_triage_screen import load_joint_spectra, generate_synthetic_joint_flux
from scripts.lib.q1009_primary_test_engine import fit_deterministic_model
from scripts.steps.step_23a_deterministic_smoke_calibration import compute_masks
import scripts.steps.step_13c_nested_synthetic_adversarial_validation as step13c
import scipy.stats

def run_single_trial(task):
    seed = task['seed']
    cond = task['condition']
    alpha_inj = task['alpha']
    base_spectra = task['base_spectra']
    
    if cond == 'null':
        gen_model = 'H0'
        phys_params = {'v_shift': 0.0, 'B_abs': 1.5e-5, 'f_D': 1.0, 'alpha': 0.0, 'int_v': 0.0, 'int_n': 0.0, 'int_b': 5.0}
    else:
        gen_model = 'H2'
        phys_params = {'v_shift': 0.0, 'B_abs': 1.5e-5, 'f_D': 0.0, 'alpha': alpha_inj}
        
    synth_spec, manifest = generate_synthetic_joint_flux(
        spectra=base_spectra,
        generating_model=gen_model,
        physical_parameters=phys_params,
        data_seed=seed
    )
    
    for s, bs in zip(synth_spec, base_spectra):
        s['train_mask'] = bs['train_mask']
        s['held_out_mask'] = bs['held_out_mask']
        
    r_h0 = fit_deterministic_model(synth_spec, 'H0')
    r_h1 = fit_deterministic_model(synth_spec, 'H1')
    r_h2 = fit_deterministic_model(synth_spec, 'H2')
    
    T_full = 2 * (r_h2['logL_train'] - r_h0['logL_train'])
    T_sec = 2 * (r_h2['logL_train'] - r_h1['logL_train'])
    S_held = 2 * (r_h2['logL_held'] - max(r_h0['logL_held'], r_h1['logL_held']))
    
    return {
        "condition": cond,
        "data_seed": seed,
        "generating_model": gen_model,
        "actual_parameters": phys_params,
        "flux_sha256": manifest["flux_sha256"],
        "H0": {"logL_train": r_h0['logL_train'], "logL_held": r_h0['logL_held'], "converged": r_h0['converged']},
        "H1": {"logL_train": r_h1['logL_train'], "logL_held": r_h1['logL_held'], "converged": r_h1['converged']},
        "H2": {"logL_train": r_h2['logL_train'], "logL_held": r_h2['logL_held'], "converged": r_h2['converged']},
        "T_full": T_full,
        "T_secondary": T_sec,
        "S_held": S_held,
        "active_boundaries": list(set(list(r_h0['active_bounds'].keys()) + list(r_h1['active_bounds'].keys()) + list(r_h2['active_bounds'].keys()))),
        "completed": True
    }

def run_calibration_campaign():
    print("--- Formal Calibration Campaign ---")
    
    # Load previously completed pilot results
    pilot_path = project_root / 'data/processed/q1009_calibration_pilot.json'
    with open(pilot_path, 'r') as f:
        results = json.load(f)
        
    completed_seeds = set([r['data_seed'] for r in results])
    print(f"Loaded {len(results)} previously completed pilot trials.")
    
    manifest_path = project_root / 'data/processed/Q1009+2956_z2.504_HIRES_spectrum_manifest.json'
    base_spectra = load_joint_spectra(str(manifest_path))
    
    feature_vector_path = project_root / 'data/processed/measured_feature_vector_Q1009+2956_z2.504.json'
    with open(feature_vector_path) as f:
        step13c.set_system_feature_vector(json.load(f))
        
    compute_masks(base_spectra)
    
    # Target totals
    targets = {
        'null': {'count': 1000, 'seeds': range(40001, 40001 + 1000), 'alpha': 0.0},
        'TEP_0.0005': {'count': 250, 'seeds': range(60001, 60001 + 250), 'alpha': 0.0005},
        'TEP_0.0007': {'count': 250, 'seeds': range(50001, 50001 + 250), 'alpha': 0.0007},
        'TEP_0.0009': {'count': 250, 'seeds': range(70001, 70001 + 250), 'alpha': 0.0009}
    }
    
    tasks = []
    for cond, info in targets.items():
        for s in info['seeds']:
            if s not in completed_seeds:
                tasks.append({
                    'condition': cond,
                    'seed': s,
                    'alpha': info['alpha'],
                    'base_spectra': base_spectra
                })
                
    print(f"Prepared {len(tasks)} remaining trials to run.")
    
    # Run multiprocessing
    if tasks:
        start_t = time.time()
        with concurrent.futures.ProcessPoolExecutor(max_workers=os.cpu_count()) as executor:
            future_to_task = {executor.submit(run_single_trial, t): t for t in tasks}
            
            done_count = 0
            for future in concurrent.futures.as_completed(future_to_task):
                try:
                    res = future.result()
                    results.append(res)
                    done_count += 1
                    if done_count % 50 == 0:
                        elapsed = time.time() - start_t
                        rate = elapsed / done_count
                        rem = (len(tasks) - done_count) * rate
                        print(f"  Completed {done_count}/{len(tasks)} remaining. Est remaining time: {rem/60:.1f} min")
                except Exception as exc:
                    print(f"Task generated an exception: {exc}")
                    
        # Save intermediate in case of crash later
        with open(project_root / 'data/processed/q1009_calibration_full_raw.json', 'w') as f:
            json.dump(results, f, indent=2)
            
    print("\n--- Calibration Complete, Computing Thresholds ---")
    
    nulls = [r for r in results if r['condition'] == 'null']
    null_t_full = [r['T_full'] for r in nulls]
    
    # Empirical 99th percentile
    t_full_threshold = np.percentile(null_t_full, 99)
    print(f"Empirical 99th Percentile Threshold for T_full: {t_full_threshold:.4f}")
    
    # Calculate false positive rate strictly using the proposed rule
    def is_positive(r):
        return (r['T_full'] >= t_full_threshold) and (r['T_secondary'] > 0) and (r['S_held'] > 0) and r['H0']['converged'] and r['H1']['converged'] and r['H2']['converged']
        
    # Wait, the rule is "all three model fits converged". 
    # But wait, earlier I determined that H0 non-convergence is mostly due to int_n=0 boundary locking which is mathematically valid!
    # If I enforce "converged == True", then legitimate fits might fail the convergence gate and be rejected.
    # The user rule states: "AND all three model fits converged"
    # I will strictly follow the user rule for the classification gate.
    
    false_positives = sum(1 for r in nulls if is_positive(r))
    print(f"Total False Positives on Null Data: {false_positives} / 1000")
    
    # Exact binomial interval for false positives
    res_null = scipy.stats.binomtest(false_positives, 1000, alternative='less')
    upper_95_fpr = res_null.proportion_ci(confidence_level=0.95).high
    print(f"One-sided 95% upper confidence bound on FPR: {upper_95_fpr:.5f} ({upper_95_fpr*100:.2f}%)")
    
    calibration_summary = {
        "t_full_threshold": float(t_full_threshold),
        "null_false_positives": int(false_positives),
        "null_total": 1000,
        "fpr_95_upper_bound": float(upper_95_fpr),
        "recoveries": {}
    }
    
    for cond in ['TEP_0.0005', 'TEP_0.0007', 'TEP_0.0009']:
        trials = [r for r in results if r['condition'] == cond]
        recovered = sum(1 for r in trials if is_positive(r))
        res_tep = scipy.stats.binomtest(recovered, len(trials), alternative='two-sided')
        ci = res_tep.proportion_ci(confidence_level=0.95)
        calibration_summary["recoveries"][cond] = {
            "recovered": int(recovered),
            "total": len(trials),
            "rate": recovered / len(trials),
            "ci_95_lower": float(ci.low),
            "ci_95_upper": float(ci.high)
        }
        print(f"Recovery {cond}: {recovered}/{len(trials)} ({recovered/len(trials)*100:.1f}%) [95% CI: {ci.low:.3f} - {ci.high:.3f}]")

    # Freeze record
    import hashlib
    with open(project_root / 'data/processed/q1009_calibration_full_raw.json', 'rb') as f:
        results_hash = hashlib.sha256(f.read()).hexdigest()
        
    freeze_record = {
        "status": "FROZEN_BEFORE_Q1009",
        "models": {
            "H0": "M3_centroid",
            "H1": "M2_primary_only",
            "H2": "M2_full"
        },
        "thresholds": {
            "T_full": float(t_full_threshold),
            "T_secondary": 0.0,
            "S_held": 0.0
        },
        "calibration_results": calibration_summary,
        "results_sha256": results_hash,
        "real_classification_run": False
    }
    
    with open(project_root / 'data/processed/q1009_primary_test_calibration.json', 'w') as f:
        json.dump(calibration_summary, f, indent=2)
        
    with open(project_root / 'data/processed/q1009_primary_test_freeze.json', 'w') as f:
        json.dump(freeze_record, f, indent=2)
        
    print("\nCalibration successfully frozen. Records written.")
    print("STOP: Review formal calibration before unblinding real Q1009 target data.")

if __name__ == '__main__':
    run_calibration_campaign()
