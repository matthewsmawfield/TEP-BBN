import os
import sys
import numpy as np
import json
from pathlib import Path
from scipy.optimize import minimize
import scipy.ndimage
import scipy.linalg
import itertools

script_dir = Path(__file__).parent
project_root = script_dir.parent.parent
sys.path.append(str(project_root))

from scripts.steps.step_14c_joint_power_triage_screen import load_joint_spectra
from scripts.steps.step_23a_deterministic_smoke_calibration import compute_masks
import scripts.steps.step_13c_nested_synthetic_adversarial_validation as step13c
from scripts.lib.joint_spectrum_likelihood import evaluate_frozen_model
from scripts.lib.q1009_primary_test_engine import precompute_spectrum_matrices

def custom_evaluate_logL_profiled(spectra, precomps, eval_params, eval_type):
    total_logl = 0.0
    c_opts = []
    
    for i, spec in enumerate(spectra):
        pc = precomps[i]
        if pc['chol_masked'] is None:
            return -1e100, []
            
        flux_zero_c = evaluate_frozen_model(
            velocity=spec['v'],
            shared_params=eval_params,
            local_params={'c0': 0.0, 'c1': 0.0, 'c2': 0.0},
            model_type=eval_type,
            sigma_v_kms=spec['sigma_v_kms']
        )
        
        A_theta_masked = -flux_zero_c[pc['mask']]
        r_theta_masked = pc['flux_masked'] + A_theta_masked
        b_theta_masked = pc['Phi_masked'].T @ (pc['W_masked'] * r_theta_masked)
        
        try:
            c_hat = scipy.linalg.cho_solve(pc['chol_masked'], b_theta_masked)
        except np.linalg.LinAlgError:
            return -1e100, []
            
        c_opt = np.clip(c_hat, [0.9, -0.1, -0.1], [1.1, 0.1, 0.1])
        c_opts.append(c_opt)
        
        residuals = r_theta_masked - (pc['Phi_masked'] @ c_opt)
        chi2 = np.sum(pc['W_masked'] * residuals**2)
        logL_i = pc['C_0_masked'] - 0.5 * chi2
        total_logl += logL_i
        
    return total_logl, c_opts

def custom_evaluate_logL_fixed_continuum(spectra, precomps_held, eval_params, eval_type, c_opts):
    total_logl = 0.0
    for i, spec in enumerate(spectra):
        pc = precomps_held[i]
        if not np.any(pc['mask']): continue
            
        flux_zero_c = evaluate_frozen_model(
            velocity=spec['v'],
            shared_params=eval_params,
            local_params={'c0': 0.0, 'c1': 0.0, 'c2': 0.0},
            model_type=eval_type,
            sigma_v_kms=spec['sigma_v_kms']
        )
        
        A_theta_masked = -flux_zero_c[pc['mask']]
        r_theta_masked = pc['flux_masked'] + A_theta_masked
        c_opt = c_opts[i]
        
        residuals = r_theta_masked - (pc['Phi_masked'] @ c_opt)
        chi2 = np.sum(pc['W_masked'] * residuals**2)
        logL_i = pc['C_0_masked'] - 0.5 * chi2
        total_logl += logL_i
    return total_logl

# Define bounds for the models
BOUNDS = {
    'v_shift': (-1.0, 1.0),
    'B_abs': (0.0, 1e-4),
    'int_v': (-10.0, 10.0),      # H0's central interloper
    'int_n': (0.0, 1e-4),
    'int_b': (4.0, 12.0),
    'free_H_v': (-100.0, -60.0), # H1's replacement for Deuterium
    'free_H_n': (0.0, 1e-4),
    'free_H_b': (4.0, 12.0)
}

def generate_starts(model_name):
    if model_name == 'H0':
        params = ['v_shift', 'B_abs', 'int_v', 'int_n', 'int_b']
        grid = {
            'v_shift': [0.0, -0.5, 0.5],
            'B_abs': [1.5e-5, 5e-5],
            'int_v': [-5.0, 0.0, 5.0],
            'int_n': [1e-5, 5e-5],
            'int_b': [5.0, 8.0, 11.0]
        }
    elif model_name == 'H1':
        params = ['v_shift', 'int_v', 'int_n', 'int_b', 'free_H_v', 'free_H_n', 'free_H_b']
        grid = {
            'v_shift': [0.0, -0.5, 0.5],
            'int_v': [-5.0, 0.0, 5.0],
            'int_n': [1e-5, 5e-5],
            'int_b': [5.0, 8.0, 11.0],
            'free_H_v': [-85.0, -82.0, -79.0],
            'free_H_n': [1e-5, 5e-5],
            'free_H_b': [5.0, 8.0, 11.0]
        }
    
    keys = list(grid.keys())
    combinations = list(itertools.product(*(grid[k] for k in keys)))
    starts = [dict(zip(keys, combo)) for combo in combinations]
    return starts, params

def evaluate_H0(spectra, precomps_train, precomps_held):
    starts, param_names = generate_starts('H0')
    bounds_list = [BOUNDS[p] for p in param_names]
    
    def obj_func(x):
        shared_params = dict(zip(param_names, x))
        # H0 has fixed f_D=1.0, alpha=0.0 to enable Deuterium via B_abs
        eval_params = shared_params.copy()
        eval_params['f_D'] = 1.0
        eval_params['alpha'] = 0.0
        
        # M3_centroid is the engine type that evaluates int_v
        logL, _ = custom_evaluate_logL_profiled(spectra, precomps_train, eval_params, 'M3_centroid')
        return -logL if logL != -1e100 else 1e100

    best_logL = -1e100
    best_x = None
    
    start_evals = []
    for s_dict in starts:
        x_init = np.array([s_dict[p] for p in param_names])
        start_evals.append((obj_func(x_init), x_init))
    
    start_evals.sort(key=lambda x: x[0])
    
    for _, x_init in start_evals[:3]:
        res = minimize(obj_func, x_init, method='L-BFGS-B', bounds=bounds_list, options={'ftol': 1e-9, 'maxiter': 200})
        if -res.fun > best_logL:
            best_logL = -res.fun
            best_x = res.x
            
    best_params = dict(zip(param_names, best_x))
    best_params['f_D'] = 1.0
    best_params['alpha'] = 0.0
    
    final_logL, c_opts = custom_evaluate_logL_profiled(spectra, precomps_train, best_params, 'M3_centroid')
    held_logL = custom_evaluate_logL_fixed_continuum(spectra, precomps_held, best_params, 'M3_centroid', c_opts)
    
    return {'logL_train': final_logL, 'logL_held': held_logL, 'params': best_params}

def evaluate_H1(spectra, precomps_train, precomps_held):
    starts, param_names = generate_starts('H1')
    bounds_list = [BOUNDS[p] for p in param_names]
    
    def obj_func(x):
        shared_params = dict(zip(param_names, x))
        # Map free_H to sec_v in the base model (M4 evaluates sec_v)
        eval_params = {
            'v_shift': shared_params['v_shift'],
            'int_v': shared_params['int_v'],
            'int_n': shared_params['int_n'],
            'int_b': shared_params['int_b'],
            'sec_v': shared_params['free_H_v'],
            'sec_n': shared_params['free_H_n'],
            'sec_b': shared_params['free_H_b']
        }
        # M4_secondary_local evaluates int_v and sec_v without B_abs
        logL, _ = custom_evaluate_logL_profiled(spectra, precomps_train, eval_params, 'M4_secondary_local')
        return -logL if logL != -1e100 else 1e100

    best_logL = -1e100
    best_x = None
    
    start_evals = []
    for s_dict in starts:
        x_init = np.array([s_dict[p] for p in param_names])
        start_evals.append((obj_func(x_init), x_init))
    
    start_evals.sort(key=lambda x: x[0])
    
    for _, x_init in start_evals[:5]: # Search slightly wider for H1
        res = minimize(obj_func, x_init, method='L-BFGS-B', bounds=bounds_list, options={'ftol': 1e-9, 'maxiter': 200})
        if -res.fun > best_logL:
            best_logL = -res.fun
            best_x = res.x
            
    shared_params = dict(zip(param_names, best_x))
    best_params = {
        'v_shift': shared_params['v_shift'],
        'int_v': shared_params['int_v'],
        'int_n': shared_params['int_n'],
        'int_b': shared_params['int_b'],
        'sec_v': shared_params['free_H_v'],
        'sec_n': shared_params['free_H_n'],
        'sec_b': shared_params['free_H_b']
    }
    
    final_logL, c_opts = custom_evaluate_logL_profiled(spectra, precomps_train, best_params, 'M4_secondary_local')
    held_logL = custom_evaluate_logL_fixed_continuum(spectra, precomps_held, best_params, 'M4_secondary_local', c_opts)
    
    return {'logL_train': final_logL, 'logL_held': held_logL, 'params': best_params}

def run_h1_test():
    print("--- EXECUTING Q1009 H0 vs H1 COMPARISON ---")
    
    manifest_path = project_root / 'data/processed/Q1009+2956_z2.504_HIRES_spectrum_manifest.json'
    real_spectra = load_joint_spectra(str(manifest_path))
    
    fv_path = project_root / 'data/processed/measured_feature_vector_Q1009+2956_z2.504.json'
    with open(fv_path) as f:
        step13c.set_system_feature_vector(json.load(f))
        
    compute_masks(real_spectra)
    
    precomps_train = [precompute_spectrum_matrices(s, 'train_mask') for s in real_spectra]
    precomps_held = [precompute_spectrum_matrices(s, 'held_out_mask') for s in real_spectra]
    
    print("\nFitting H0 (Deuterium + Interloper)...")
    res_h0 = evaluate_H0(real_spectra, precomps_train, precomps_held)
    print(f"H0 Train logL: {res_h0['logL_train']:.2f}")
    
    print("\nFitting H1 (Free Hydrogen + Interloper)...")
    res_h1 = evaluate_H1(real_spectra, precomps_train, precomps_held)
    print(f"H1 Train logL: {res_h1['logL_train']:.2f}")
    
    delta_train = res_h1['logL_train'] - res_h0['logL_train']
    delta_held = res_h1['logL_held'] - res_h0['logL_held']
    
    print("\n--- COMPARISON RESULTS ---")
    print(f"Delta logL (Train) [H1 - H0]: {delta_train:.2f}")
    print(f"Delta logL (Held)  [H1 - H0]: {delta_held:.2f}")
    
    print("\nBest Parameters H0:")
    for k, v in res_h0['params'].items():
        print(f"  {k}: {v:.5g}")
        
    print("\nBest Parameters H1:")
    for k, v in res_h1['params'].items():
        print(f"  {k}: {v:.5g}")
        
    results = {
        'H0': res_h0,
        'H1': res_h1,
        'delta_train': delta_train,
        'delta_held': delta_held
    }
    
    out_path = project_root / 'data/processed/q1009_h0_vs_h1_results.json'
    with open(out_path, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\nSaved results to {out_path}")

if __name__ == '__main__':
    run_h1_test()
