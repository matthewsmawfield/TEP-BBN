import sys
import numpy as np
import json
from pathlib import Path
from scipy.optimize import minimize
import time

script_dir = Path(__file__).parent
project_root = script_dir.parent.parent
sys.path.insert(0, str(project_root))

from scripts.steps.deprecated_classical.step_27c_refit_h0_model_6a import parse_vpfit_ties, ParameterManager
from scripts.lib.physical_rt_engine import RadiativeTransferEngine
from scripts.steps.step_31_fit_h1_free_hydrogen import get_residuals, objective_t, grid_search_h1
from scripts.steps.step_31c_compare_h0_h1_q1009 import partition_data

def run_cross_validation():
    print("--- Phase E2: Genuine Cross Validation (H0b vs H1) ---")
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
            'vsig': r['vsig'], 'w_min': r['w_min'], 'w_max': r['w_max'],
            'coadd': coadd
        })

    theta_shared_base = np.array(pm.theta_init)
    
    set_a, set_b = partition_data(data_blocks)
    
    folds = [
        {'name': 'Fold A (Train Lya, Test Higher)', 'train': set_a, 'test': set_b},
        {'name': 'Fold B (Train Higher, Test Lya)', 'train': set_b, 'test': set_a}
    ]
    
    results = {}
    
    for fold in folds:
        print(f"\n[{fold['name']}]")
        train_blocks = fold['train']
        test_blocks = fold['test']
        
        # ---------------------------------------------------------
        # H0b: Refit D on Train
        # ---------------------------------------------------------
        def obj_h0b_train(th):
            return objective_t(get_residuals(th, None, pm, train_blocks, z_abs_ref, c_kms, engine, model_type='H0'), noise_cfg)
            
        print("  -> Training H0b...")
        res_h0b_train = minimize(obj_h0b_train, theta_shared_base, method='L-BFGS-B', options={'maxiter': 10, 'ftol': 1e-6})
        
        # Evaluate H0b on Test
        res_test = get_residuals(res_h0b_train.x, None, pm, test_blocks, z_abs_ref, c_kms, engine, model_type='H0')
        ll_h0b_test = -objective_t(res_test, noise_cfg)
        
        # ---------------------------------------------------------
        # H1: Refit H1 on Train
        # ---------------------------------------------------------
        print("  -> Grid search for H1...")
        best_h1_init = grid_search_h1(theta_shared_base, pm, train_blocks, z_abs_ref, c_kms, engine, noise_cfg)
        
        def obj_h1_joint_train(th_joint):
            th_sh = th_joint[:-3]
            th_h1 = th_joint[-3:]
            return objective_t(get_residuals(th_sh, th_h1, pm, train_blocks, z_abs_ref, c_kms, engine, model_type='H1'), noise_cfg)
            
        th_joint_init = np.concatenate([theta_shared_base, best_h1_init])
        bounds_joint = [(None, None)] * len(theta_shared_base) + [(-150.0, 50.0), (10.0, 16.0), (4.0, 20.0)]
        
        print("  -> Training H1...")
        res_h1_train = minimize(obj_h1_joint_train, th_joint_init, method='L-BFGS-B', bounds=bounds_joint, options={'maxiter': 10, 'ftol': 1e-6})
        
        # Evaluate H1 on Test
        res_test_h1 = get_residuals(res_h1_train.x[:-3], res_h1_train.x[-3:], pm, test_blocks, z_abs_ref, c_kms, engine, model_type='H1')
        ll_h1_test = -objective_t(res_test_h1, noise_cfg)
        
        print(f"  -> Test LL H0b: {ll_h0b_test:.2f}")
        print(f"  -> Test LL H1: {ll_h1_test:.2f}")
        
        results[fold['name']] = {
            'H0b_Test_LL': float(ll_h0b_test),
            'H1_Test_LL': float(ll_h1_test)
        }
        
    cv_ll_h0b = sum(r['H0b_Test_LL'] for r in results.values())
    cv_ll_h1 = sum(r['H1_Test_LL'] for r in results.values())
    
    print(f"\n[Overall CV Predictive LL]")
    print(f"  -> H0b: {cv_ll_h0b:.2f}")
    print(f"  -> H1:  {cv_ll_h1:.2f}")
    
    results['Overall'] = {
        'H0b_CV_LL': float(cv_ll_h0b),
        'H1_CV_LL': float(cv_ll_h1)
    }
    
    with open(project_root / 'data' / 'processed' / 'q1009_forensic_cv.json', 'w') as f:
        json.dump(results, f, indent=4)

if __name__ == '__main__':
    run_cross_validation()
