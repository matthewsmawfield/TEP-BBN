import numpy as np
import json
import math
from scipy.optimize import minimize
from pathlib import Path

script_dir = Path(__file__).parent
project_root = script_dir.parent.parent

with open(project_root / 'data/processed/measured_feature_vector_Q0913+072.json', 'r') as f:
    features = json.load(f)
    
components = features['components']
c_kms = 299792.458
v_grid = np.linspace(-300, 100, 800)
x_norm = (v_grid - v_grid[0]) / (v_grid[-1] - v_grid[0]) * 2.0 - 1.0

hi_comps = []
for comp in components:
    v = comp['velocity_kms']
    n_hi = 1.0 * comp['metal_alignment_strength'] 
    hi_comps.append({'v': v, 'n': n_hi, 'b': 12.0, 'g_i': comp['g_i']})

def voigt_profile(x, center, sigma, gamma):
    from scipy.special import wofz
    z = ((x - center) + 1j * gamma) / (sigma * np.sqrt(2.0))
    v = wofz(z).real / (sigma * np.sqrt(2.0 * np.pi))
    return v

def base_model(params_dict, apply_misspecification=False):
    c0 = params_dict.get('c0', 1.0)
    c1 = params_dict.get('c1', 0.0)
    c2 = params_dict.get('c2', 0.0)
    
    flux = c0 + c1 * x_norm + c2 * (x_norm**2)
    
    if apply_misspecification:
        flux += 0.01 * np.sin(2.0 * np.pi * x_norm) 
        
    v_shift = params_dict.get('v_shift', 0.0)
    lsf_scale = params_dict.get('lsf_scale', 1.0)
    v_eval = v_grid - v_shift
    
    scale_hi = 20.0  
    scale_di = 1.0e5 
        
    for hc in hi_comps:
        b_eff = hc['b'] * lsf_scale
        if apply_misspecification:
            b_eff *= 1.05 
        flux -= hc['n'] * voigt_profile(v_eval, hc['v'], b_eff, 0.1) * scale_hi
        
    if 'B_abs' in params_dict:
        B_abs = params_dict['B_abs']
        f_D = params_dict.get('f_D', 1.0) # default to M0
        alpha = params_dict.get('alpha', 0.0)
        primary_comp = next((c for c in components if c.get('column_feature', 0.0) == 1.0), components[0])
        g_primary = primary_comp['g_i']
        
        for i, hc in enumerate(hi_comps):
            g_i = components[i]['g_i']
            
            b_d = (hc['b'] / math.sqrt(2)) * lsf_scale
            margin = max(3 * b_d, 2 * 10.0)
            
            if f_D > 0:
                v_d = hc['v'] - 82.0
                n_d = hc['n'] * B_abs * f_D
                if (v_grid[0] + margin) <= v_d <= (v_grid[-1] - margin):
                    flux -= n_d * voigt_profile(v_eval, v_d, b_d, 0.1) * scale_di
            
            if f_D < 1.0:
                v_p = hc['v'] - 82.0 + c_kms * alpha * (g_i - g_primary)
                n_p = hc['n'] * B_abs * (1.0 - f_D)
                if (v_grid[0] + margin) <= v_p <= (v_grid[-1] - margin):
                    flux -= n_p * voigt_profile(v_eval, v_p, b_d, 0.1) * scale_di
                
    if 'int_v' in params_dict:
        v_int = params_dict['int_v']
        n_int = params_dict['int_n']
        b_int = params_dict['int_b'] * lsf_scale
        flux -= n_int * voigt_profile(v_eval, v_int, b_int, 0.1) * scale_di
        
    if apply_misspecification:
        flux -= 2.5e-6 * voigt_profile(v_eval, -110.0, 5.0, 0.1) * scale_di
        
    return flux

def generate_truth(truth_name, seed=42):
    np.random.seed(seed)
    truth_params_base = {'c0': 1.0, 'c1': 0.0, 'c2': 0.0, 'v_shift': 0.0, 'lsf_scale': 1.0}
    noise_level = 1.0 / 50.0  # SNR = 50
    
    if truth_name == 'Mnull':
        truth_flux = base_model(truth_params_base, apply_misspecification=True)
    elif truth_name == 'M0':
        truth_flux = base_model({**truth_params_base, 'B_abs': 2.5e-5, 'f_D': 1.0}, apply_misspecification=True)
    elif truth_name == 'M3_exact_D':
        truth_flux = base_model({**truth_params_base, 'int_v': -82.0, 'int_n': 2.5e-5, 'int_b': 12.0/math.sqrt(2)}, apply_misspecification=True)
        
    noise = np.random.normal(0, noise_level, size=len(v_grid))
    return truth_flux + noise, truth_flux, noise_level

# Optimization routines
base_bounds = [(0.90, 1.10), (-0.1, 0.1), (-0.1, 0.1), (-1.0, 1.0), (0.9, 1.1)]

def opt_Mnull(data, noise):
    def loss(x):
        p = {'c0': x[0], 'c1': x[1], 'c2': x[2], 'v_shift': x[3], 'lsf_scale': x[4]}
        mod = base_model(p)
        return 0.5 * np.sum(((data - mod) / noise)**2)
    x0 = [1.0, 0.0, 0.0, 0.0, 1.0]
    res = minimize(loss, x0, bounds=base_bounds)
    return res, {'c0': res.x[0], 'c1': res.x[1], 'c2': res.x[2], 'v_shift': res.x[3], 'lsf_scale': res.x[4]}

def opt_M0(data, noise):
    def loss(x):
        p = {'c0': x[0], 'c1': x[1], 'c2': x[2], 'v_shift': x[3], 'lsf_scale': x[4], 'B_abs': x[5], 'f_D': 1.0}
        mod = base_model(p)
        return 0.5 * np.sum(((data - mod) / noise)**2)
    x0 = [1.0, 0.0, 0.0, 0.0, 1.0, 2.5e-5]
    res = minimize(loss, x0, bounds=base_bounds + [(0, 1e-4)]) 
    return res, {'B_abs': res.x[5]}

def opt_M2(data, noise):
    def loss(x):
        p = {'c0': x[0], 'c1': x[1], 'c2': x[2], 'v_shift': x[3], 'lsf_scale': x[4], 'B_abs': x[5], 'f_D': x[6], 'alpha': x[7]}
        mod = base_model(p)
        return 0.5 * np.sum(((data - mod) / noise)**2)
    x0 = [1.0, 0.0, 0.0, 0.0, 1.0, 2.5e-5, 0.5, 0.0007]
    res = minimize(loss, x0, bounds=base_bounds + [(0, 1e-4), (0.0, 1.0), (0.0005, 0.0009)])
    return res, {'B_abs': res.x[5], 'f_D': res.x[6], 'alpha': res.x[7]}

def opt_M3(data, noise):
    def loss(x):
        p = {'c0': x[0], 'c1': x[1], 'c2': x[2], 'v_shift': x[3], 'lsf_scale': x[4], 'int_v': x[5], 'int_n': x[6], 'int_b': x[7]}
        mod = base_model(p)
        return 0.5 * np.sum(((data - mod) / noise)**2)
    x0 = [1.0, 0.0, 0.0, 0.0, 1.0, -82.0, 1e-5, 8.0]
    res = minimize(loss, x0, bounds=base_bounds + [(-300, 100), (0, 1e-4), (4.0, 12.0)])
    return res, {'int_v': res.x[5], 'int_n': res.x[6], 'int_b': res.x[7]}

data, truth_flux, noise_level = generate_truth('Mnull', seed=42)
res_Mnull, p_Mnull = opt_Mnull(data, noise_level)
mod_Mnull = base_model(p_Mnull)
chi2_Mnull = np.sum(((data - mod_Mnull)/noise_level)**2) / (len(v_grid) - 5)
resid = (data - mod_Mnull)/noise_level

res_M3, p_M3 = opt_M3(data, noise_level)
depth_M3 = p_M3['int_n'] * voigt_profile(0, 0, p_M3['int_b']/math.sqrt(2), 0.1) * 1e5

out_mnull = {
  "truth": "Mnull",
  "reduced_chi2_Mnull": chi2_Mnull,
  "residual_mean": np.mean(resid),
  "residual_std": np.std(resid),
  "largest_negative_residual_sigma": np.min(resid),
  "M3_best_fit_line_depth_sigma": depth_M3 / noise_level,
  "delta_logL_M3_minus_Mnull": -(res_M3.fun - res_Mnull.fun)
}
print(json.dumps(out_mnull, indent=2))

data, truth_flux, noise_level = generate_truth('M0', seed=42)
res_M0, p_M0 = opt_M0(data, noise_level)
res_M2, p_M2 = opt_M2(data, noise_level)
res_M3, p_M3 = opt_M3(data, noise_level)

out_m0 = {
  "truth": "M0",
  "M0_best_fit_DH": p_M0['B_abs'],
  "M2_best_fit_B": p_M2['B_abs'],
  "M2_best_fit_fD": p_M2['f_D'],
  "M2_best_fit_alpha": p_M2['alpha'],
  "M3_best_fit_v": p_M3['int_v'],
  "delta_logL_M2_minus_M0": -(res_M2.fun - res_M0.fun),
  "delta_logL_M3_minus_M0": -(res_M3.fun - res_M0.fun)
}
print(json.dumps(out_m0, indent=2))
