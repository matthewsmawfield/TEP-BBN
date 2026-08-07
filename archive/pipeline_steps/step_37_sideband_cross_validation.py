import sys
import numpy as np
import json
import hashlib
from pathlib import Path
from scipy.optimize import minimize
from scipy.stats import t as student_t

script_dir = Path(__file__).parent
project_root = script_dir.parent.parent
sys.path.insert(0, str(project_root))

from scripts.steps.deprecated_classical.step_27c_refit_h0_model_6a import parse_vpfit_ties, ParameterManager
from scripts.lib.physical_rt_engine import RadiativeTransferEngine
from scripts.lib.block_coordinate_optimizer import BlockCoordinateOptimizer
from scripts.steps.step_33_build_six_model_family import build_model_components
from scripts.steps.step_34_run_converged_full_models import compute_residuals

def hash_array(arr):
    return hashlib.sha256(arr.tobytes()).hexdigest()[:16]

def run_sideband_cross_validation():
    print("=== Phase E: Sideband-Calibrated Cross-Transition Validation ===")
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
        
        w_center = (r['w_min'] + r['w_max']) / 2.0
        if 4250.0 <= w_center <= 4270.0 or 4670.0 <= w_center <= 5440.0:
            is_lya = True
        else:
            is_lya = False
            
        data_blocks.append({
            'wave': wave[mask], 'flux': flux[mask], 'err': err[mask],
            'vsig': r['vsig'], 'w_min': r['w_min'], 'w_max': r['w_max'],
            'coadd': coadd, 'is_lya': is_lya
        })

    train_lya_blocks = [b for b in data_blocks if b['is_lya']]
    test_higher_blocks = [b for b in data_blocks if not b['is_lya']]
    
    # Hash verification
    train_pixels = np.concatenate([b['wave'] for b in train_lya_blocks])
    test_pixels = np.concatenate([b['wave'] for b in test_higher_blocks])
    
    hash_train = hash_array(train_pixels)
    hash_test = hash_array(test_pixels)
    
    print(f"Train (Ly-alpha) Hash: {hash_train} (Pixels: {len(train_pixels)})")
    print(f"Test (Higher-order) Hash: {hash_test} (Pixels: {len(test_pixels)})")
    assert hash_train != hash_test, "Train and test pixel hashes must be strictly distinct!"
    
    theta_shared_base = np.array(pm.theta_init)
    
    # Evaluate M_Dfree vs M_H on Train -> Test
    models_to_val = {
        'M_Dfree': {'cand_init': [12.5, 10000.0, 5.0], 'bounds_cand': [(10.0, 16.0), (1000.0, 40000.0), (1.0, 30.0)], 'n_cand': 3},
        'M_H': {'cand_init': [-135.0, 12.5, 10000.0, 5.0], 'bounds_cand': [(-160.0, 50.0), (10.0, 16.0), (1000.0, 40000.0), (1.0, 30.0)], 'n_cand': 4}
    }
    
    cv_results = {}
    
    for m_name, cfg in models_to_val.items():
        print(f"\nTraining {m_name} on Ly-alpha...")
        def cand_obj_train(th_c):
            grouped = build_model_components(m_name, theta_shared_base, th_c, pm, z_abs_ref, c_kms)
            res = compute_residuals(grouped, train_lya_blocks, engine)
            v_res = res[np.abs(res) < 100.0]
            return -np.sum(student_t.logpdf(v_res, noise_cfg['nu'], noise_cfg['location'], noise_cfg['scale']))
            
        opt = BlockCoordinateOptimizer(cand_obj_train, candidate_param_indices=list(range(cfg['n_cand'])), rel_tol=1e-7, abs_tol=0.01)
        x0 = np.array(cfg['cand_init'], dtype=float)
        bounds = cfg['bounds_cand']
        
        fit_res = opt.optimize_block_coordinate(x0, bounds=bounds, verbose=False)
        th_c_opt = fit_res['x']
        
        # Evaluate on Test (higher-order lines) without fitting continua on test line pixels
        grouped_test = build_model_components(m_name, theta_shared_base, th_c_opt, pm, z_abs_ref, c_kms)
        res_test = compute_residuals(grouped_test, test_higher_blocks, engine)
        v_res_test = res_test[np.abs(res_test) < 100.0]
        test_ll = float(np.sum(student_t.logpdf(v_res_test, noise_cfg['nu'], noise_cfg['location'], noise_cfg['scale'])))
        
        print(f"  -> {m_name} Train LL: {-fit_res['fun']:.2f}")
        print(f"  -> {m_name} Test LL (Sideband-Calibrated): {test_ll:.2f}")
        
        cv_results[m_name] = {
            'train_ll': float(-fit_res['fun']),
            'test_ll': test_ll
        }
        
    out_file = project_root / 'data' / 'processed' / 'q1009_sideband_cross_validation.json'
    with open(out_file, 'w') as f:
        json.dump(cv_results, f, indent=4)
    print(f"\nSaved cross-validation results to {out_file}")

if __name__ == '__main__':
    run_sideband_cross_validation()
