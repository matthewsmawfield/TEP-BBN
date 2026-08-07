import numpy as np
import json
import math
from dynesty import NestedSampler
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

def voigt_profile(x, center, sigma, gamma):
    from scipy.special import wofz
    z = ((x - center) + 1j * gamma) / (sigma * np.sqrt(2.0))
    v = wofz(z).real / (sigma * np.sqrt(2.0 * np.pi))
    return v

script_dir = Path(__file__).parent
project_root = script_dir.parent.parent

with open(project_root / 'data/processed/measured_feature_vector_Q0913+072.json', 'r') as f:
    features = json.load(f)
    
components = features['components']
c_kms = 299792.458
alpha_prior = [0.0005, 0.0009]
v_grid = np.linspace(-300, 100, 800)
x_norm = (v_grid - v_grid[0]) / (v_grid[-1] - v_grid[0]) * 2.0 - 1.0

hi_comps = []
for comp in components:
    v = comp['velocity_kms']
    n_hi = 1.0 * comp['metal_alignment_strength'] 
    hi_comps.append({'v': v, 'n': n_hi, 'b': 12.0, 'g_i': comp['g_i']})

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
        f_D = params_dict.get('f_D', 1.0)
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

def fit_model_nested(truth_data, model_type, noise_level):
    base_bounds = [(0.90, 1.10), (-0.1, 0.1), (-0.1, 0.1), (-1.0, 1.0), (0.9, 1.1)]
    if model_type == 'Mnull':
        bounds = base_bounds
        def ptform(u):
            x = np.array(u)
            for i, b in enumerate(bounds): x[i] = u[i] * (b[1] - b[0]) + b[0]
            return x
        def logl(x):
            p = {'c0': x[0], 'c1': x[1], 'c2': x[2], 'v_shift': x[3], 'lsf_scale': x[4]}
            return -0.5 * np.sum(((truth_data - base_model(p, apply_misspecification=False)) / noise_level)**2)
        ndim = 5
    elif model_type == 'M3':
        bounds = base_bounds + [(-300, 100), (0, 1e-4), (4.0, 12.0)]
        def ptform(u):
            x = np.array(u)
            for i, b in enumerate(bounds): x[i] = u[i] * (b[1] - b[0]) + b[0]
            return x
        def logl(x):
            p = {'c0': x[0], 'c1': x[1], 'c2': x[2], 'v_shift': x[3], 'lsf_scale': x[4], 'int_v': x[5], 'int_n': x[6], 'int_b': x[7]}
            return -0.5 * np.sum(((truth_data - base_model(p, apply_misspecification=False)) / noise_level)**2)
        ndim = 8

    sampler = NestedSampler(logl, ptform, ndim, bound='single', sample='slice', nlive=100, bootstrap=0)
    sampler.run_nested(dlogz=0.5, print_progress=False)
    res = sampler.results
    return res.logz[-1], res.logzerr[-1]

np.random.seed(50)
truth_params_base = {'c0': 1.0, 'c1': 0.0, 'c2': 0.0, 'v_shift': 0.0, 'lsf_scale': 1.0}
truth_flux = base_model(truth_params_base, apply_misspecification=True)
noise = 1.0 / 50.0
noisy_data = truth_flux + np.random.normal(0, noise, len(v_grid))

print("Fitting Mnull...")
lz_mnull, lzerr_mnull = fit_model_nested(noisy_data, 'Mnull', noise)
print(f"Mnull: logZ = {lz_mnull}, logZerr = {lzerr_mnull}")

print("Fitting M3...")
lz_m3, lzerr_m3 = fit_model_nested(noisy_data, 'M3', noise)
print(f"M3: logZ = {lz_m3}, logZerr = {lzerr_m3}")
print(f"Delta logZ = {lz_m3 - lz_mnull}")
