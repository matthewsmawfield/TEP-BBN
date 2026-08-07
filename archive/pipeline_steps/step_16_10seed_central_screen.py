import os
import sys
import numpy as np
import json
from pathlib import Path
import multiprocessing
import traceback

script_dir = Path(__file__).parent
project_root = script_dir.parent.parent
sys.path.append(str(project_root))

from scripts.lib.joint_spectrum_likelihood import fit_model_nested_joint
from scripts.steps.step_14c_joint_power_triage_screen import load_joint_spectra, generate_synthetic_joint_flux
import scripts.steps.step_13c_nested_synthetic_adversarial_validation as step13c

def run_single_trial(seed):
    np.random.seed(seed)
    manifest_path = 'data/processed/Q1009+2956_z2.504_HIRES_spectrum_manifest.json'
    spectra = load_joint_spectra(manifest_path)
    
    alpha_inject = 0.0007
    f_D_inject = 0.0
    
    # Generate synthetic spectra
    shared_params = {'v_shift': 0.0, 'B_abs': 1.5e-5, 'f_D': f_D_inject, 'alpha': alpha_inject}
    synth_spectra = generate_synthetic_joint_flux(spectra, shared_params, alpha_inject)
    
    # 1. Null model
    try:
        v_hat = 0.0
        centroid_bounds = [v_hat - 3.0, v_hat + 3.0]
        null_logz, null_logzerr, null_pdiag = fit_model_nested_joint(synth_spectra, 'M3_centroid', nlive=100, centroid_bounds=centroid_bounds)
    except Exception as e:
        return {'seed': seed, 'pass': False, 'error': f"M3 Error: {str(e)}"}
        
    # 2. TEP model
    try:
        full_logz, full_logzerr, full_pdiag = fit_model_nested_joint(synth_spectra, 'M2_full', nlive=100)
    except Exception as e:
        return {'seed': seed, 'pass': False, 'error': f"M2 Error: {str(e)}"}
        
    delta_logz = full_logz - null_logz
    at_lower = full_pdiag.get('alpha_at_lower_edge', True)
    at_upper = full_pdiag.get('alpha_at_upper_edge', True)
    edges_hit = at_lower or at_upper
    
    is_pass = (delta_logz > 5.0) and not edges_hit
    
    return {
        'seed': seed,
        'pass': is_pass,
        'delta_logz': delta_logz,
        'full_logz': full_logz,
        'null_logz': null_logz,
        'alpha_mean': full_pdiag.get('alpha_mean'),
        'at_lower': at_lower,
        'at_upper': at_upper
    }

def main():
    print("Running 10-Seed Central Alpha Screen...")
    with open('data/processed/measured_feature_vector_Q1009+2956_z2.504.json') as f:
        step13c.set_system_feature_vector(json.load(f))
        
    seeds = list(range(1001, 1011))
    
    results = []
    with multiprocessing.Pool(processes=min(10, multiprocessing.cpu_count())) as pool:
        for res in pool.imap_unordered(run_single_trial, seeds):
            results.append(res)
            print(f"Seed {res['seed']}: {'PASS' if res['pass'] else 'FAIL'} (dZ={res.get('delta_logz', 0):.1f}, edges={res.get('at_lower')},{res.get('at_upper')})")
            
    num_pass = sum(r['pass'] for r in results)
    print("\n--- Summary ---")
    print(f"Total passes: {num_pass} / 10")
    
    if num_pass >= 9:
        print("DECISION: PROCEED TO FULL CAMPAIGN (9-10/10)")
    elif num_pass >= 4:
        print("DECISION: RUN 50 CENTRAL TRIALS (4-8/10)")
    else:
        print("DECISION: CLOSE AS FAILURE (0-3/10)")
        
    with open('data/processed/q1009_10seed_central_screen_results.json', 'w') as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    main()
