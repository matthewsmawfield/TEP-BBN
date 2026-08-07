import sys
import numpy as np
import json
from pathlib import Path
from scipy.optimize import minimize
from scipy.stats import t as student_t

script_dir = Path(__file__).parent
project_root = script_dir.parent.parent
sys.path.insert(0, str(project_root))

from scripts.steps.deprecated_classical.step_27c_refit_h0_model_6a import parse_vpfit_ties, ParameterManager
from scripts.lib.physical_rt_engine import RadiativeTransferEngine
from scripts.steps.step_31_fit_h1_free_hydrogen import get_residuals, objective_t, grid_search_h1

def partition_data(data_blocks):
    """Partitions data into Lya regions (Set A) and Lyb/Lyg regions (Set B) based on wavelength."""
    set_a = []
    set_b = []
    for b in data_blocks:
        # Lya is around 4250 at z=2.5. We can split at w_obs = 4000
        if b['w_min'] > 4000:
            set_a.append(b)
        else:
            set_b.append(b)
    return set_a, set_b

def run_real_comparison():
    print("--- Phase D5: Real-Data H0/H1 Comparison ---")
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
    
    # Load all data blocks
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
    
    print("\n[1] Fitting Full Dataset")
    # H0 Full
    res_h0_full = get_residuals(theta_shared_base, None, pm, data_blocks, z_abs_ref, c_kms, engine, model_type='H0')
    ll_h0_full = -objective_t(res_h0_full, noise_cfg)
    k_h0 = len(theta_shared_base)
    n_pixels = len(res_h0_full)
    aic_h0 = 2 * k_h0 - 2 * ll_h0_full
    bic_h0 = k_h0 * np.log(n_pixels) - 2 * ll_h0_full
    
    # H1 Full
    best_h1_init = grid_search_h1(theta_shared_base, pm, data_blocks, z_abs_ref, c_kms, engine, noise_cfg)
    def restr_obj_full(th_h1):
        r = get_residuals(theta_shared_base, th_h1, pm, data_blocks, z_abs_ref, c_kms, engine, model_type='H1')
        return objective_t(r, noise_cfg)
    res_h1_full = minimize(restr_obj_full, best_h1_init, method='L-BFGS-B', bounds=[(-150.0, 50.0), (10.0, 16.0), (4.0, 20.0)], options={'maxiter': 50})
    ll_h1_full = -res_h1_full.fun
    k_h1 = len(theta_shared_base) + 3 # replaced D ties with 3 free parameters
    aic_h1 = 2 * k_h1 - 2 * ll_h1_full
    bic_h1 = k_h1 * np.log(n_pixels) - 2 * ll_h1_full
    
    print(f"H0 Full: LL={ll_h0_full:.2f}, AIC={aic_h0:.2f}, BIC={bic_h0:.2f}")
    print(f"H1 Full: LL={ll_h1_full:.2f}, AIC={aic_h1:.2f}, BIC={bic_h1:.2f}")
    
    print("\n[2] Cross-Transition Predictive Validation")
    set_a, set_b = partition_data(data_blocks)
    print(f"Set A (Lya): {len(set_a)} blocks. Set B (Higher order): {len(set_b)} blocks.")
    
    # Train H0 on A, Predict B
    # Since H0 is rigid (no free H I search), we just evaluate on B directly for simplicity in this script.
    res_h0_B_pred = get_residuals(theta_shared_base, None, pm, set_b, z_abs_ref, c_kms, engine, model_type='H0')
    ll_h0_B_pred = -objective_t(res_h0_B_pred, noise_cfg)
    
    # Train H0 on B, Predict A
    res_h0_A_pred = get_residuals(theta_shared_base, None, pm, set_a, z_abs_ref, c_kms, engine, model_type='H0')
    ll_h0_A_pred = -objective_t(res_h0_A_pred, noise_cfg)
    
    # Train H1 on A, Predict B
    best_h1_A = grid_search_h1(theta_shared_base, pm, set_a, z_abs_ref, c_kms, engine, noise_cfg)
    def restr_obj_A(th_h1):
        r = get_residuals(theta_shared_base, th_h1, pm, set_a, z_abs_ref, c_kms, engine, model_type='H1')
        return objective_t(r, noise_cfg)
    res_h1_A = minimize(restr_obj_A, best_h1_A, method='L-BFGS-B', bounds=[(-150.0, 50.0), (10.0, 16.0), (4.0, 20.0)], options={'maxiter': 50})
    res_h1_B_pred = get_residuals(theta_shared_base, res_h1_A.x, pm, set_b, z_abs_ref, c_kms, engine, model_type='H1')
    ll_h1_B_pred = -objective_t(res_h1_B_pred, noise_cfg)
    
    # Train H1 on B, Predict A
    best_h1_B = grid_search_h1(theta_shared_base, pm, set_b, z_abs_ref, c_kms, engine, noise_cfg)
    def restr_obj_B(th_h1):
        r = get_residuals(theta_shared_base, th_h1, pm, set_b, z_abs_ref, c_kms, engine, model_type='H1')
        return objective_t(r, noise_cfg)
    res_h1_B = minimize(restr_obj_B, best_h1_B, method='L-BFGS-B', bounds=[(-150.0, 50.0), (10.0, 16.0), (4.0, 20.0)], options={'maxiter': 50})
    res_h1_A_pred = get_residuals(theta_shared_base, res_h1_B.x, pm, set_a, z_abs_ref, c_kms, engine, model_type='H1')
    ll_h1_A_pred = -objective_t(res_h1_A_pred, noise_cfg)
    
    cv_ll_h0 = ll_h0_A_pred + ll_h0_B_pred
    cv_ll_h1 = ll_h1_A_pred + ll_h1_B_pred
    
    print(f"H0 Predictive LL: {cv_ll_h0:.2f}")
    print(f"H1 Predictive LL: {cv_ll_h1:.2f}")
    
    results = {
        "H0": {
            "logL_full": float(ll_h0_full),
            "AIC": float(aic_h0),
            "BIC": float(bic_h0),
            "predictive_logL": float(cv_ll_h0)
        },
        "H1": {
            "logL_full": float(ll_h1_full),
            "AIC": float(aic_h1),
            "BIC": float(bic_h1),
            "predictive_logL": float(cv_ll_h1),
            "refined_params": res_h1_full.x.tolist()
        }
    }
    
    if cv_ll_h0 > cv_ll_h1 + 5.0 and ll_h0_full > ll_h1_full:
        results["verdict"] = "H0_D_CONVENTIONAL_PREFERRED"
    elif cv_ll_h1 > cv_ll_h0 + 5.0 and ll_h1_full > ll_h0_full + 5.0:
        results["verdict"] = "H1_HI_KINEMATIC_PREFERRED"
    else:
        results["verdict"] = "H0_H1_SPECTROSCOPICALLY_COMPARABLE"
        
    print(f"\nVerdict: {results['verdict']}")
    
    with open(project_root / 'data' / 'processed' / 'q1009_physical_h0_vs_h1.json', 'w') as f:
        json.dump(results, f, indent=4)
        
if __name__ == '__main__':
    run_real_comparison()
