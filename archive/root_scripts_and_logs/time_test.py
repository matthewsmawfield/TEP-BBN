import numpy as np
import time
from dynesty import NestedSampler
from scripts.steps.step_13c_nested_synthetic_adversarial_validation import voigt_profile
from pathlib import Path
import json
import math

script_dir = Path("scripts/steps")
project_root = script_dir.parent.parent
with open(project_root / 'data/processed/measured_feature_vector_Q0913+072.json', 'r') as f:
    features = json.load(f)

components = features['components']
c_kms = 299792.458
v_grid = np.linspace(-300, 100, 800)
x_norm = (v_grid - v_grid[0]) / (v_grid[-1] - v_grid[0]) * 2.0 - 1.0

hi_comps = []
for c in components:
    hi_comps.append({
        'v': c['v_i'],
        'b': c['b_i'],
        'n': 1.0 * c['metal_alignment_strength']
    })

def base_model(params_dict, apply_misspecification=False):
    c0 = params_dict.get('c0', 1.0)
    c1 = params_dict.get('c1', 0.0)
    c2 = params_dict.get('c2', 0.0)
    flux = c0 + c1 * x_norm + c2 * (x_norm**2)
    v_shift = params_dict.get('v_shift', 0.0)
    lsf_scale = params_dict.get('lsf_scale', 1.0)
    v_eval = v_grid - v_shift
    scale_hi = 20.0  
    scale_di = 1.0e5 
    for hc in hi_comps:
        b_eff = hc['b'] * lsf_scale
        flux -= hc['n'] * voigt_profile(v_eval, hc['v'], b_eff, 0.1) * scale_hi
    if 'int_v' in params_dict:
        v_int = params_dict['int_v']
        n_int = params_dict['int_n']
        b_int = params_dict['int_b'] * lsf_scale
        flux -= n_int * voigt_profile(v_eval, v_int, b_int, 0.1) * scale_di
    return np.clip(flux, 0, 1)

truth_data = np.zeros(800)
noise_level = 0.033

bounds = [(0.80, 1.20), (-0.5, 0.5), (-0.5, 0.5), (-3.0, 3.0), (0.8, 1.2), (-120, -40), (0, 1e-3), (2.0, 30.0)]
def ptform(u):
    x = np.array(u)
    for i, b in enumerate(bounds):
        x[i] = u[i] * (b[1] - b[0]) + b[0]
    return x

def logl(x):
    p = {'c0': x[0], 'c1': x[1], 'c2': x[2], 'v_shift': x[3], 'lsf_scale': x[4], 'int_v': x[5], 'int_n': x[6], 'int_b': x[7]}
    model_flux = base_model(p, apply_misspecification=False)
    return -0.5 * np.sum(((truth_data - model_flux) / noise_level)**2)

sampler = NestedSampler(logl, ptform, 8, bound='multi', sample='unif', nlive=150)
t0 = time.time()
sampler.run_nested(dlogz=0.5, print_progress=False)
print(f"Time: {time.time() - t0:.2f} s")
