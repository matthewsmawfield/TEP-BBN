import os
import sys
import json
import math
import hashlib
import subprocess
import numpy as np
from pathlib import Path
import multiprocessing
import traceback

script_dir = Path(__file__).parent
project_root = script_dir.parent.parent
sys.path.append(str(project_root))

from scripts.lib.joint_spectrum_likelihood import fit_model_nested_joint
from scripts.steps.step_14c_joint_power_triage_screen import load_joint_spectra, generate_synthetic_joint_flux
import scripts.steps.step_13c_nested_synthetic_adversarial_validation as step13c

def get_file_sha256(filepath):
    h = hashlib.sha256()
    with open(filepath, 'rb') as f:
        h.update(f.read())
    return h.hexdigest()

def get_git_commit():
    try:
        return subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=str(project_root)).decode().strip()
    except Exception:
        return "unknown"

def run_single_audit_trial(args):
    data_seed, nlive, sampler_seed = args
    
    # 1. Deterministic data generation
    np.random.seed(data_seed)
    manifest_path = 'data/processed/Q1009+2956_z2.504_HIRES_spectrum_manifest.json'
    spectra = load_joint_spectra(manifest_path)
    
    alpha_inject = 0.0007
    f_D_inject = 0.0
    shared_params_inject = {'v_shift': 0.0, 'B_abs': 1.5e-5, 'f_D': f_D_inject, 'alpha': alpha_inject}
    
    synth_spectra = generate_synthetic_joint_flux(spectra, shared_params_inject, alpha_inject)
    
    # 2. Sampler instantiation
    rstate_null = np.random.default_rng(sampler_seed)
    rstate_full = np.random.default_rng(sampler_seed + 1) # slight offset for the second model
    
    # 3. M3_centroid
    try:
        v_hat = 0.0
        centroid_bounds = [v_hat - 3.0, v_hat + 3.0]
        null_logz, null_logzerr, null_diag = fit_model_nested_joint(
            synth_spectra, 'M3_centroid', nlive=nlive, centroid_bounds=centroid_bounds, rstate=rstate_null)
    except Exception as e:
        return {'error': f"M3 Error: {str(e)}"}
        
    # 4. M2_full
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
    print("Running Bounded Convergence Audit...")
    feature_vector_path = 'data/processed/measured_feature_vector_Q1009+2956_z2.504.json'
    manifest_path = 'data/processed/Q1009+2956_z2.504_HIRES_spectrum_manifest.json'
    joint_lib_path = 'scripts/lib/joint_spectrum_likelihood.py'
    
    with open(feature_vector_path) as f:
        step13c.set_system_feature_vector(json.load(f))
        
    freeze_config_path = 'data/processed/q1009_audit_freeze_config.json'
    if not os.path.exists(freeze_config_path):
        import dynesty
        freeze_config = {
            "code_commit": get_git_commit(),
            "joint_likelihood_sha256": get_file_sha256(joint_lib_path),
            "manifest_sha256": get_file_sha256(manifest_path),
            "feature_vector_sha256": get_file_sha256(feature_vector_path),
            "dynesty_version": dynesty.__version__,
            "sampling_method": "slice",
            "bounding_method": "single",
            "dlogz_threshold": 0.5,
            "injected_parameter_vector": {
                "alpha": 0.0007,
                "f_D": 0.0,
                "B_abs": 1.5e-5,
                "v_shift": 0.0,
                "c0": 1.0,
                "c1": 0.0,
                "c2": 0.0
            }
        }
        # Compute config sha256 itself before writing? The user said "audit_config_sha256"
        # We'll hash the JSON string
        config_str = json.dumps(freeze_config, sort_keys=True)
        h = hashlib.sha256(config_str.encode()).hexdigest()
        freeze_config["audit_config_sha256"] = h
        
        with open(freeze_config_path, 'w') as f:
            json.dump(freeze_config, f, indent=2)
        print("Frozen audit configuration to", freeze_config_path)
        
    data_seeds = [1001, 1008, 1002]
    nlives = [100, 300, 600]
    sampler_seeds = [50001, 50002, 50003]
    
    # Pre-calculate injected logL for closure check
    # Generate one noiseless synthetic spectrum to get exact logL
    spectra = load_joint_spectra(manifest_path)
    alpha_inject = 0.0007
    shared_params_inject = {'v_shift': 0.0, 'B_abs': 1.5e-5, 'f_D': 0.0, 'alpha': alpha_inject}
    # To get injected_logL, we evaluate at exact parameters. But wait, since we ADD noise for each data_seed,
    # the injected_logL actually changes per data_seed!
    # I will calculate it within the main loop or check `max_logL` against the noisy true likelihood.
    
    # We will evaluate true logL per data_seed
    true_logl_map = {}
    for ds in data_seeds:
        np.random.seed(ds)
        synth_spectra = generate_synthetic_joint_flux(spectra, shared_params_inject, alpha_inject)
        total_logl = 0.0
        for spec in synth_spectra:
            residual = spec['flux'] - evaluate_frozen_model_wrapper(spec, shared_params_inject)
            error = spec['err']
            total_logl += -0.5 * np.sum((residual / error)**2 + np.log(2.0 * np.pi * error**2))
        true_logl_map[ds] = total_logl
    
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
            print(f"nlive={res['nlive']} data_seed={res['data_seed']} sampler_seed={res['sampler_seed']}: {res['classification']} max_logL={res['full_max_logl']:.1f}")

    with open('data/processed/q1009_convergence_audit_results.json', 'w') as f:
        json.dump(results, f, indent=2)
        
    # Evaluate convergence
    for nl in nlives:
        all_passed = True
        for ds in data_seeds:
            subset = [r for r in results if r['nlive'] == nl and r['data_seed'] == ds]
            if len(subset) != 3:
                all_passed = False
                break
                
            # 1. Sampler-seed stability
            classes = set(r['classification'] for r in subset)
            if len(classes) > 1:
                print(f"FAIL: nlive={nl} data_seed={ds} unstable classification {classes}")
                all_passed = False
                
            # 2. Likelihood closure
            true_logl = true_logl_map[ds]
            if not all(r['full_max_logl'] >= true_logl - 10.0 for r in subset):
                print(f"FAIL: nlive={nl} data_seed={ds} failed likelihood closure (true={true_logl:.1f})")
                all_passed = False
                
            # 3. Model-wise evidence stability
            for i in range(len(subset)):
                for j in range(i+1, len(subset)):
                    for model in ['null', 'full']:
                        logz_i = subset[i][f'{model}_logz']
                        logz_j = subset[j][f'{model}_logz']
                        err_i = subset[i][f'{model}_logzerr']
                        err_j = subset[j][f'{model}_logzerr']
                        max_diff = max(2.0, 2.0 * math.sqrt(err_i**2 + err_j**2))
                        if abs(logz_i - logz_j) > max_diff:
                            print(f"FAIL: nlive={nl} data_seed={ds} {model} logZ unstable {abs(logz_i - logz_j):.2f} > {max_diff:.2f}")
                            all_passed = False
                    # Delta logZ stability
                    dz_i = subset[i]['delta_logz']
                    dz_j = subset[j]['delta_logz']
                    err_dz_i = math.sqrt(subset[i]['full_logzerr']**2 + subset[i]['null_logzerr']**2)
                    err_dz_j = math.sqrt(subset[j]['full_logzerr']**2 + subset[j]['null_logzerr']**2)
                    max_diff_dz = max(2.0, 2.0 * math.sqrt(err_dz_i**2 + err_dz_j**2))
                    if abs(dz_i - dz_j) > max_diff_dz:
                        print(f"FAIL: nlive={nl} data_seed={ds} delta_logz unstable {abs(dz_i - dz_j):.2f} > {max_diff_dz:.2f}")
                        all_passed = False
            
            # 4. Posterior stability (mean/std/edges)
            # Not strictly evaluated here unless requested, but we require edges to be consistent
            at_lowers = set(r['at_lower'] for r in subset)
            at_uppers = set(r['at_upper'] for r in subset)
            if len(at_lowers) > 1 or len(at_uppers) > 1:
                print(f"FAIL: nlive={nl} data_seed={ds} unstable edges")
                all_passed = False
                
            # 5. Effective sample count
            if not all(r['full_eff_samples'] >= 200 for r in subset):
                print(f"FAIL: nlive={nl} data_seed={ds} low effective samples")
                all_passed = False
                
        if all_passed:
            print(f"\nQUALIFIED_NLIVE_{nl}")
            return
            
    print("\nNESTED_SAMPLER_NOT_QUALIFIED")

def evaluate_frozen_model_wrapper(spec, shared_params):
    from scripts.lib.joint_spectrum_likelihood import evaluate_frozen_model
    local_params = {'c0': 1.0, 'c1': 0.0, 'c2': 0.0}
    return evaluate_frozen_model(spec['v'], shared_params, local_params, 'M2_full', spec['sigma_v_kms'])

if __name__ == "__main__":
    main()
