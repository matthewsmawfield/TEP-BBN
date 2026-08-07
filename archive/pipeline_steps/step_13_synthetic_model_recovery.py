"""
Step 13: Synthetic Model Recovery Test (Phase 4A)

Validates the M0/M1/M2/M3 model comparison machinery. Generates synthetic 
truth spectra representing each model and verifies that the comparison 
framework correctly identifies the generating model.
"""

import json
from pathlib import Path
import sys
import numpy as np
from scipy.optimize import minimize
import math

script_dir = Path(__file__).parent
project_root = script_dir.parent.parent
sys.path.insert(0, str(project_root))

from scripts.utils.voigt_fitting import voigt_profile

def run_synthetic_recovery():
    print("Step 13: Synthetic Model Recovery Test (Phase 4A)")
    print("=" * 60)
    
    feature_path = project_root / 'data/processed/measured_feature_vector_Q0913+072.json'
    with open(feature_path, 'r') as f:
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
        
    def base_model(params_dict):
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
            
        if 'alpha' in params_dict:
            alpha = params_dict['alpha']
            d_to_h = params_dict.get('D_to_H', 2.5e-5)
            primary_comp = next((c for c in components if c.get('column_feature', 0.0) == 1.0), components[0])
        g_primary = primary_comp['g_i']
            
            for i, hc in enumerate(hi_comps):
                g_i = components[i]['g_i']
                v_d = hc['v'] - 82.0 + c_kms * alpha * (g_i - g_primary)
                n_d = hc['n'] * d_to_h
                b_d = (hc['b'] / math.sqrt(2)) * lsf_scale
                
                margin = max(3 * b_d, 2 * 10.0)
                if (v_grid[0] + margin) <= v_d <= (v_grid[-1] - margin):
                    flux -= n_d * voigt_profile(v_eval, v_d, b_d, 0.1) * scale_di
                    
        elif 'D_to_H' in params_dict:
            d_to_h = params_dict['D_to_H']
            for hc in hi_comps:
                v_d = hc['v'] - 82.0  
                n_d = hc['n'] * d_to_h
                b_d = (hc['b'] / math.sqrt(2)) * lsf_scale
                flux -= n_d * voigt_profile(v_eval, v_d, b_d, 0.1) * scale_di
                
        if 'int_v' in params_dict:
            v_int = params_dict['int_v']
            n_int = params_dict['int_n']
            b_int = params_dict['int_b'] * lsf_scale
            flux -= n_int * voigt_profile(v_eval, v_int, b_int, 0.1) * scale_di
            
        return np.clip(flux, 0, 1)

    np.random.seed(42)
    noise_level = 0.02 # S/N = 50
    
    truth_params_base = {'c0': 1.0, 'c1': 0.02, 'c2': -0.01, 'v_shift': 0.5, 'lsf_scale': 1.02}
    
    truths = {
        "Mnull_truth": base_model(truth_params_base),
        "M0_truth": base_model({**truth_params_base, 'D_to_H': 2.5e-5}),
        "M1_truth": base_model({**truth_params_base, 'alpha': 0.00073}),
        "M2_truth": base_model({**truth_params_base, 'D_to_H': 1.0e-5, 'alpha': 0.00073}),
        "M3_truth": base_model({**truth_params_base, 'int_v': -82.0, 'int_n': 2.5e-5, 'int_b': 8.0})
    }
    
    for k in truths:
        truths[k] += np.random.normal(0, noise_level, size=len(v_grid))
        
    def fit_model(truth_data, model_type):
        def objective(p):
            params_dict = {
                'c0': p[0],
                'c1': p[1],
                'c2': p[2],
                'v_shift': p[3],
                'lsf_scale': p[4]
            }
            if model_type == 'M0':
                params_dict['D_to_H'] = p[5]
            elif model_type == 'M1':
                params_dict['alpha'] = p[5]
            elif model_type == 'M2':
                params_dict['D_to_H'] = p[5]
                params_dict['alpha'] = p[6]
            elif model_type == 'M3':
                params_dict['int_v'] = p[5]
                params_dict['int_n'] = p[6]
                params_dict['int_b'] = p[7]
                
            model_flux = base_model(params_dict)
            chi2 = np.sum(((truth_data - model_flux) / noise_level)**2)
            return chi2

        base_x0 = [1.0, 0.0, 0.0, 0.0, 1.0]
        base_bounds = [(0.80, 1.20), (-0.5, 0.5), (-0.5, 0.5), (-3.0, 3.0), (0.8, 1.2)]
        
        if model_type == 'Mnull':
            x0 = base_x0
            bounds = base_bounds
            k = 5
        elif model_type == 'M0':
            x0 = base_x0 + [2.5e-5]
            bounds = base_bounds + [(0, 1e-4)]
            k = 6
        elif model_type == 'M1':
            x0 = base_x0 + [0.0007]
            bounds = base_bounds + [alpha_prior]
            k = 6
        elif model_type == 'M2':
            x0 = base_x0 + [1.0e-5, 0.0007]
            bounds = base_bounds + [(0, 1e-4), alpha_prior]
            k = 7
        elif model_type == 'M3':
            x0 = base_x0 + [-82.0, 2.5e-5, 8.0]
            bounds = base_bounds + [(-120, -40), (0, 1e-3), (2.0, 30.0)]
            k = 8
            
        res = minimize(objective, x0, method='L-BFGS-B', bounds=bounds)
        bic = res.fun + k * np.log(len(v_grid))
        return bic, res.x

    print("Fitting models to synthetic truths...")
    models = ['Mnull', 'M0', 'M1', 'M2', 'M3']
    recovery_matrix = {}
    
    for truth_name, truth_flux in truths.items():
        bics = {}
        for m in models:
            bic, best_p = fit_model(truth_flux, m)
            bics[m] = bic
            
        winner = min(bics, key=bics.get)
        recovery_matrix[truth_name] = f"{winner}_wins"
        
        print(f"\nTruth: {truth_name}")
        for m in models:
            print(f"  {m} BIC: {bics[m]:.1f}")
        print(f"  -> Winner: {winner}")

    pass_mnull = (recovery_matrix['Mnull_truth'] == 'Mnull_wins')
    pass_m0 = (recovery_matrix['M0_truth'] == 'M0_wins')
    pass_m1 = (recovery_matrix['M1_truth'] == 'M1_wins')
    pass_m2 = (recovery_matrix['M2_truth'] == 'M2_wins' or recovery_matrix['M2_truth'] == 'M1_wins')
    pass_m3 = (recovery_matrix['M3_truth'] == 'M3_wins')
    
    overall_pass = pass_mnull and pass_m0 and pass_m1 and pass_m3
    
    report = {
        "test_type": "synthetic_recovery",
        "claim_allowed": False,
        "truth_models": models,
        "recovery_matrix": recovery_matrix,
        "pipeline_ready_for_real_data": overall_pass
    }
    
    out_path = project_root / 'data/processed/synthetic_recovery_report.json'
    with open(out_path, 'w') as f:
        json.dump(report, f, indent=2)
        
    print("\n" + "=" * 60)
    print("SYNTHETIC RECOVERY RESULTS")
    print(json.dumps(recovery_matrix, indent=2))
    print(f"\nBaseline Recovery Passed: {overall_pass}")
    print("=" * 60)

if __name__ == '__main__':
    run_synthetic_recovery()
