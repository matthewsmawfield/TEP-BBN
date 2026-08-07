import sys
import numpy as np
import json
from pathlib import Path
from scipy.optimize import minimize
from scipy.stats import t as student_t
import time

script_dir = Path(__file__).parent
project_root = script_dir.parent.parent
sys.path.insert(0, str(project_root))

from scripts.steps.deprecated_classical.step_27c_refit_h0_model_6a import parse_vpfit_ties, ParameterManager
from scripts.lib.physical_rt_engine import RadiativeTransferEngine
from scripts.steps.step_31_fit_h1_free_hydrogen import get_residuals, objective_t, grid_search_h1
from scripts.steps.step_31b_h0_h1_recovery_tests import generate_synthetic_data

def run_expanded_synthetic_tests():
    print("--- Phase E3: Expanded Synthetic Tests ---")
    manifest_path = project_root / 'data' / 'processed' / 'Q1009_union_manifest.json'
    vpfit_path = project_root / 'data' / 'literature_components' / 'model_6a.26'
    noise_model_path = project_root / 'configs' / 'tep_noise_model.json'
    
    with open(manifest_path, 'r') as f: manifest = json.load(f)
    with open(noise_model_path, 'r') as f: noise_cfg = json.load(f)
    
    z_abs_ref = manifest['z_abs']
    c_kms = 299792.458
    
    components_raw, regions = parse_vpfit_ties(vpfit_path)
    pm = ParameterManager(components_raw)
    engine = RadiativeTransferEngine(z_abs=z_abs_ref)
    
    data_blocks = []
    for r in regions:
        coadd = r['filename']
        if coadd not in manifest['coadds']: continue
        chunk_wave, chunk_flux, chunk_err = [], [], []
        for chunk in manifest['coadds'][coadd]:
            chunk_wave.extend(chunk['wave'])
            chunk_flux.extend(chunk['flux'])
            chunk_err.extend(chunk['err'])
        wave, flux, err = np.array(chunk_wave), np.array(chunk_flux), np.array(chunk_err)
        mask = (np.isfinite(flux)) & (np.isfinite(err)) & (err > 0) & (wave >= r['w_min']) & (wave <= r['w_max'])
        if np.sum(mask) == 0: continue
        data_blocks.append({
            'wave': wave[mask], 'flux': flux[mask], 'err': err[mask],
            'vsig': r['vsig'], 'w_min': r['w_min'], 'w_max': r['w_max']
        })

    theta_shared_base = np.array(pm.theta_init)
    
    num_realizations = 3
    
    print("\n[Test Suite 1: H0 (D I) Injections]")
    h0_results = []
    for i in range(num_realizations):
        np.random.seed(42 + i)
        syn_data = generate_synthetic_data(theta_shared_base, None, pm, data_blocks, z_abs_ref, c_kms, engine, noise_cfg, 'H0')
        
        # Fit H0b
        def obj_h0b(th): return objective_t(get_residuals(th, None, pm, syn_data, z_abs_ref, c_kms, engine, 'H0'), noise_cfg)
        res_h0b = minimize(obj_h0b, theta_shared_base, method='L-BFGS-B', options={'maxiter': 10})
        ll_h0b = -res_h0b.fun
        
        # Fit H1
        best_h1 = grid_search_h1(theta_shared_base, pm, syn_data, z_abs_ref, c_kms, engine, noise_cfg)
        def obj_h1(th_joint): return objective_t(get_residuals(th_joint[:-3], th_joint[-3:], pm, syn_data, z_abs_ref, c_kms, engine, 'H1'), noise_cfg)
        res_h1 = minimize(obj_h1, np.concatenate([theta_shared_base, best_h1]), method='L-BFGS-B', 
                          bounds=[(None, None)] * len(theta_shared_base) + [(-150.0, 50.0), (10.0, 16.0), (4.0, 20.0)],
                          options={'maxiter': 10})
        ll_h1 = -res_h1.fun
        
        aic_h0b = -2 * ll_h0b
        aic_h1 = 6 - 2 * ll_h1
        
        selected = 'H0' if aic_h0b < aic_h1 else 'H1'
        print(f"  Realization {i+1}: LL_H0b={ll_h0b:.2f}, LL_H1={ll_h1:.2f} -> {selected} (AIC_H0={aic_h0b:.2f}, AIC_H1={aic_h1:.2f})")
        h0_results.append(selected)
        
    false_h1_rate = h0_results.count('H1') / len(h0_results)
    print(f"  => False H1 Selection Rate: {false_h1_rate:.2f}")

    print("\n[Test Suite 2: H1 (H I) Injections]")
    h1_results = []
    # Grid of H1 injections
    h1_injections = [
        [-40.0, 13.5, 10.0],
        [-100.0, 12.0, 6.0],
        [-140.0, 13.0, 15.0]
    ]
    
    for i, inj in enumerate(h1_injections):
        print(f"  Injection case {i+1}: v={inj[0]}, logN={inj[1]}, b={inj[2]}")
        for j in range(3): # 3 noise realizations per case
            np.random.seed(100 + i*10 + j)
            syn_data = generate_synthetic_data(theta_shared_base, inj, pm, data_blocks, z_abs_ref, c_kms, engine, noise_cfg, 'H1')
            
            # Fit H0b
            def obj_h0b2(th): return objective_t(get_residuals(th, None, pm, syn_data, z_abs_ref, c_kms, engine, 'H0'), noise_cfg)
            res_h0b = minimize(obj_h0b2, theta_shared_base, method='L-BFGS-B', options={'maxiter': 10})
            ll_h0b = -res_h0b.fun
            
            # Fit H1
            best_h1 = grid_search_h1(theta_shared_base, pm, syn_data, z_abs_ref, c_kms, engine, noise_cfg)
            def obj_h12(th_joint): return objective_t(get_residuals(th_joint[:-3], th_joint[-3:], pm, syn_data, z_abs_ref, c_kms, engine, 'H1'), noise_cfg)
            res_h1 = minimize(obj_h12, np.concatenate([theta_shared_base, best_h1]), method='L-BFGS-B', 
                              bounds=[(None, None)] * len(theta_shared_base) + [(-150.0, 50.0), (10.0, 16.0), (4.0, 20.0)],
                              options={'maxiter': 10})
            ll_h1 = -res_h1.fun
            
            aic_h0b = -2 * ll_h0b
            aic_h1 = 6 - 2 * ll_h1
            selected = 'H0' if aic_h0b < aic_h1 else 'H1'
            print(f"    R{j+1}: LL_H0b={ll_h0b:.2f}, LL_H1={ll_h1:.2f} -> {selected}")
            h1_results.append(selected)
            
    false_h0_rate = h1_results.count('H0') / len(h1_results)
    print(f"  => False H0 Selection Rate: {false_h0_rate:.2f}")

    results = {
        'false_h1_rate': float(false_h1_rate),
        'false_h0_rate': float(false_h0_rate)
    }
    with open(project_root / 'data' / 'processed' / 'q1009_forensic_synthetic.json', 'w') as f:
        json.dump(results, f, indent=4)

if __name__ == '__main__':
    run_expanded_synthetic_tests()
