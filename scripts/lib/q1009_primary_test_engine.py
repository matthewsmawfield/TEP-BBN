import itertools

import numpy as np
import scipy.linalg
import scipy.ndimage
from scipy.optimize import minimize

from scripts.lib.joint_spectrum_likelihood import evaluate_frozen_model

# Frozen bounds
BOUNDS = {
    'v_shift': (-1.0, 1.0),
    'B_abs': (0.0, 1e-4),
    'f_D': (0.0, 1.0),
    'alpha': (0.0005, 0.0009),
    'int_v': (-10.0, 10.0),
    'int_n': (0.0, 1e-4),
    'int_b': (4.0, 12.0)
}

MODEL_PARAMS = {
    'H0': ['v_shift', 'B_abs', 'int_v', 'int_n', 'int_b'],
    'H1': ['v_shift', 'B_abs', 'f_D', 'alpha'],
    'H2': ['v_shift', 'B_abs', 'f_D', 'alpha']
}

def get_model_eval_type(model_name):
    if model_name == 'H0': return 'M3_centroid'
    if model_name == 'H1': return 'M2_primary_only'
    if model_name == 'H2': return 'M2_full'
    raise ValueError(f"Unknown model {model_name}")

def precompute_spectrum_matrices(spec, mask_key='train_mask'):
    v = spec['v']
    sigma_v_kms = spec['sigma_v_kms']
    dv = np.median(np.diff(v))
    sigma_pixels = sigma_v_kms / dv
    
    x_n = (v - v[0]) / (v[-1] - v[0]) * 2.0 - 1.0
    phi_0 = scipy.ndimage.gaussian_filter1d(np.ones_like(x_n), sigma_pixels, mode='nearest')
    phi_1 = scipy.ndimage.gaussian_filter1d(x_n, sigma_pixels, mode='nearest')
    phi_2 = scipy.ndimage.gaussian_filter1d(x_n**2, sigma_pixels, mode='nearest')
    
    Phi = np.column_stack([phi_0, phi_1, phi_2])
    
    # Apply the mask
    mask = spec.get(mask_key, np.ones_like(spec['flux'], dtype=bool))
    
    Phi_masked = Phi[mask]
    W_masked = 1.0 / (spec['err'][mask]**2)
    flux_masked = spec['flux'][mask]
    
    # For profiled continuum optimization over the masked region
    H_masked = Phi_masked.T @ (W_masked[:, None] * Phi_masked)
    
    try:
        chol_masked = scipy.linalg.cho_factor(H_masked, lower=True)
    except np.linalg.LinAlgError:
        chol_masked = None

    C_0_masked = -0.5 * np.sum(np.log(2.0 * np.pi * spec['err'][mask]**2))
    
    return {
        'mask': mask,
        'Phi': Phi,  # Full Phi for later evaluation
        'Phi_masked': Phi_masked,
        'W_masked': W_masked,
        'flux_masked': flux_masked,
        'chol_masked': chol_masked,
        'C_0_masked': C_0_masked
    }

def evaluate_logL_profiled(spectra, precomps, shared_params, model_name):
    """
    Evaluates logL by analytically profiling c_opt for each spectrum.
    Returns (total_logL, list_of_c_opt)
    """
    eval_type = get_model_eval_type(model_name)
    total_logl = 0.0
    c_opts = []
    
    # Fill in fixed params
    eval_params = shared_params.copy()
    if model_name == 'H0':
        eval_params['f_D'] = 1.0
        eval_params['alpha'] = 0.0

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
            
        # Apply standard bounds: c0 in [0.9, 1.1], c1, c2 in [-0.1, 0.1]
        c_opt = np.clip(c_hat, [0.9, -0.1, -0.1], [1.1, 0.1, 0.1])
        c_opts.append(c_opt)
        
        # Calculate logL
        residuals = r_theta_masked - (pc['Phi_masked'] @ c_opt)
        chi2 = np.sum(pc['W_masked'] * residuals**2)
        logL_i = pc['C_0_masked'] - 0.5 * chi2
        total_logl += logL_i
        
    return total_logl, c_opts

def evaluate_logL_fixed_continuum(spectra, precomps_held, shared_params, model_name, c_opts):
    """
    Evaluates logL on held-out windows using fixed physical parameters and fixed c_opts.
    """
    eval_type = get_model_eval_type(model_name)
    total_logl = 0.0
    
    eval_params = shared_params.copy()
    if model_name == 'H0':
        eval_params['f_D'] = 1.0
        eval_params['alpha'] = 0.0

    for i, spec in enumerate(spectra):
        pc = precomps_held[i]
        # Only evaluate if there are held-out pixels
        if not np.any(pc['mask']):
            continue
            
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

def generate_starting_points(model_name):
    """
    Generate a coarse deterministic grid of starting points for multi-start L-BFGS-B.
    """
    params = MODEL_PARAMS[model_name]
    grid_vals = {}
    for p in params:
        BOUNDS[p]
        if p == 'v_shift':
            grid_vals[p] = [0.0, -0.5, 0.5]
        elif p == 'B_abs':
            grid_vals[p] = [1.5e-5, 5e-5]
        elif p == 'f_D':
            grid_vals[p] = [0.0, 0.5, 1.0]
        elif p == 'alpha':
            grid_vals[p] = [0.0006, 0.0007, 0.0008]
        elif p == 'int_v':
            grid_vals[p] = [-5.0, 0.0, 5.0]
        elif p == 'int_n':
            grid_vals[p] = [1e-5, 5e-5]
        elif p == 'int_b':
            grid_vals[p] = [5.0, 8.0, 11.0]
            
    # Cartesian product
    keys = list(grid_vals.keys())
    combinations = list(itertools.product(*(grid_vals[k] for k in keys)))
    starts = [dict(zip(keys, combo)) for combo in combinations]
    return starts, keys

def fit_deterministic_model(spectra, model_name):
    """
    Fits the specified model deterministically using profiled continuum over train masks.
    """
    precomps_train = [precompute_spectrum_matrices(s, 'train_mask') for s in spectra]
    precomps_held = [precompute_spectrum_matrices(s, 'held_out_mask') for s in spectra]
    
    starts, param_names = generate_starting_points(model_name)
    bounds_list = [BOUNDS[p] for p in param_names]
    
    def obj_func(x):
        shared_params = dict(zip(param_names, x))
        logL, _ = evaluate_logL_profiled(spectra, precomps_train, shared_params, model_name)
        # return negative logL for minimizer
        return -logL if logL != -1e100 else 1e100

    best_logL = -1e100
    best_x = None
    best_res = None
    
    # Evaluate grid to find best 3 starting points
    start_evals = []
    for s_dict in starts:
        x_init = np.array([s_dict[p] for p in param_names])
        val = obj_func(x_init)
        start_evals.append((val, x_init))
        
    start_evals.sort(key=lambda item: item[0])
    best_starts = [item[1] for item in start_evals[:3]]
    
    total_evals = len(starts)
    
    for x_init in best_starts:
        res = minimize(
            obj_func, 
            x_init, 
            method='L-BFGS-B', 
            bounds=bounds_list,
            options={'ftol': 1e-9, 'gtol': 1e-6, 'maxiter': 200}
        )
        total_evals += res.nfev
        
        if -res.fun > best_logL:
            best_logL = -res.fun
            best_x = res.x
            best_res = res
            
    best_params = dict(zip(param_names, best_x))
    
    # Re-evaluate to get final c_opts and exact logL
    final_logL, c_opts = evaluate_logL_profiled(spectra, precomps_train, best_params, model_name)
    
    # Calculate held-out logL using the frozen params and continuum
    held_logL = evaluate_logL_fixed_continuum(spectra, precomps_held, best_params, model_name, c_opts)
    
    # Identify active bounds
    active_bounds = {}
    for p, val in best_params.items():
        b = BOUNDS[p]
        if abs(val - b[0]) < 1e-6:
            active_bounds[p] = 'lower'
        elif abs(val - b[1]) < 1e-6:
            active_bounds[p] = 'upper'
            
    return {
        'logL_train': final_logL,
        'logL_held': held_logL,
        'physical_parameters': best_params,
        'c_opts': c_opts,
        'converged': best_res.success,
        'message': best_res.message,
        'nfev': total_evals,
        'active_bounds': active_bounds
    }
