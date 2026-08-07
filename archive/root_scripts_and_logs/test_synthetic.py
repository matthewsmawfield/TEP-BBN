import numpy as np
from scipy.optimize import minimize
import math
from scripts.utils.voigt_fitting import voigt_profile

c_kms = 299792.458
v_grid = np.linspace(-150, 50, 500)
hi_comps = [{'v': -12.43, 'n': 0.31, 'b': 12.0, 'g_i': 0.586}, {'v': 0.0, 'n': 0.69, 'b': 12.0, 'g_i': 0.897}]

def base_model(params_dict):
    flux = np.ones_like(v_grid)
    for hc in hi_comps:
        flux -= hc['n'] * voigt_profile(v_grid, hc['v'], hc['b'], 0.1) * 20.0
    
    if 'D_to_H' in params_dict:
        for hc in hi_comps:
            flux -= hc['n'] * params_dict['D_to_H'] * voigt_profile(v_grid, hc['v'] - 82.0, hc['b']/1.414, 0.1) * 20.0
    
    if 'alpha' in params_dict:
        g_primary = hi_comps[1]['g_i']
        for hc in hi_comps:
            v_phantom = hc['v'] - 82.0 + c_kms * params_dict['alpha'] * (hc['g_i'] - g_primary)
            flux -= hc['n'] * 2.5e-5 * voigt_profile(v_grid, v_phantom, hc['b']/1.414, 0.1) * 20.0
            
    if 'int_v' in params_dict:
        flux -= params_dict['int_n'] * voigt_profile(v_grid, params_dict['int_v'], params_dict['int_b'], 0.1) * 20.0
        
    return np.clip(flux, 0, 1)

f0 = base_model({'D_to_H': 2.5e-5})
f1 = base_model({'alpha': 0.00073})
diff = np.sum((f0 - f1)**2)
print("Difference between M0 and M1:", diff)

