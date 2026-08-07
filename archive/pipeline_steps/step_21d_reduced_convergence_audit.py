import os
import sys
import json
import math
import hashlib
import subprocess
import numpy as np
from pathlib import Path
import multiprocessing

script_dir = Path(__file__).parent
project_root = script_dir.parent.parent
sys.path.append(str(project_root))

from scripts.lib.joint_spectrum_likelihood import fit_model_nested_joint
from scripts.steps.step_14c_joint_power_triage_screen import load_joint_spectra, generate_synthetic_joint_flux
import scripts.steps.step_13c_nested_synthetic_adversarial_validation as step13c

def run_single_audit_trial(args):
    data_seed, nlive, sampler_seed = args
    
    np.random.seed(data_seed)
    manifest_path = 'data/processed/Q1009+2956_z2.504_HIRES_spectrum_manifest.json'
    spectra = load_joint_spectra(manifest_path)
    
    alpha_inject = 0.0007
    f_D_inject = 0.0
    shared_params_inject = {'v_shift': 0.0, 'B_abs': 1.5e-5, 'f_D': f_D_inject, 'alpha': alpha_inject}
    
    synth_spectra = generate_synthetic_joint_flux(spectra, shared_params_inject, alpha_inject)
    
    rstate_null = np.random.default_rng(sampler_seed)
    rstate_full = np.random.default_rng(sampler_seed + 1)
    
    try:
        v_hat = 0.0
        centroid_bounds = [v_hat - 3.0, v_hat + 3.0]
        null_logz, null_logzerr, null_diag = fit_model_nested_joint(
            synth_spectra, 'M3_centroid', nlive=nlive, centroid_bounds=centroid_bounds, rstate=rstate_null)
    except Exception as e:
        return {'error': f"M3 Error: {str(e)}"}
        
    try:
        full_logz, full_logzerr, full_diag = fit_model_nested_joint(
            synth_spectra, 'M2_full', nlive=nlive, rstate=rstate_full)
    except Exception as e:
        return {'error': f"M2 Error: {str(e)}"}
        
    delta_logz = full_logz - null_logz
    at_lower = full_diag.get('alpha_at_lower_edge', True)
    at_upper = full_diag.get('alpha_at_upper_edge', True)
    edges_hit = at_lower or at_upper
    
    classification = "TEP_POSITIVE" if (delta_logz > 5.0 and not edges_hit) else "REAL_NEGATIVE"
    
    return {
        'data_seed': int(data_seed),
        'nlive': int(nlive),
        'sampler_seed': int(sampler_seed),
        'null_logz': float(null_logz),
        'null_logzerr': float(null_logzerr),
        'null_max_logl': float(null_diag.get('max_logl', 0.0)),
        'null_eff_samples': float(null_diag.get('eff_samples', 0.0)),
        'full_logz': float(full_logz),
        'full_logzerr': float(full_logzerr),
        'full_max_logl': float(full_diag.get('max_logl', 0.0)),
        'full_eff_samples': float(full_diag.get('eff_samples', 0.0)),
        'alpha_mean': float(full_diag.get('alpha_mean', 0.0)),
        'alpha_std': float(full_diag.get('alpha_std', 0.0)),
        'at_lower': bool(at_lower),
        'at_upper': bool(at_upper),
        'classification': str(classification),
        'delta_logz': float(delta_logz),
        'ncall': int(full_diag.get('ncall', 0) + null_diag.get('ncall', 0))
    }

def main():
    print("Running Reduced Bounded Convergence Audit...")
    feature_vector_path = 'data/processed/measured_feature_vector_Q1009+2956_z2.504.json'
    manifest_path = 'data/processed/Q1009+2956_z2.504_HIRES_spectrum_manifest.json'
    
    with open(feature_vector_path) as f:
        step13c.set_system_feature_vector(json.load(f))
        
    data_seeds = [1001, 1008, 1002]
    nlives = [100, 300, 600]
    sampler_seeds = [50001, 50002, 50003]
    
    results = []
    tasks = []
    for nl in nlives:
        for ds in data_seeds:
            for ss in sampler_seeds:
                tasks.append((ds, nl, ss))
                
    with multiprocessing.Pool(processes=min(12, multiprocessing.cpu_count())) as pool:
        for res in pool.imap_unordered(run_single_audit_trial, tasks):
            if 'error' in res:
                print(f"Error in trial: {res['error']}")
                continue
            results.append(res)
            print(f"nlive={res['nlive']} data_seed={res['data_seed']} sampler_seed={res['sampler_seed']}: {res['classification']} delta_logZ={res['delta_logz']:.1f}")

    with open('data/processed/q1009_reduced_convergence_audit_results.json', 'w') as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    main()
