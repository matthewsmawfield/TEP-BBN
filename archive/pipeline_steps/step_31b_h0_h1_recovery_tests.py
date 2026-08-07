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

def generate_synthetic_data(theta_shared, theta_h1, pm, original_data_blocks, z_abs_ref, c_kms, engine, noise_cfg, model_type='H0'):
    """
    Generates synthetic data from the specified model by calculating the exact forward model
    and adding Student-t noise.
    """
    syn_blocks = []
    
    # Forward model is just observed minus residuals
    # But wait, our get_residuals computes: res = (flux_fit - flux_mod) / err_fit
    # So flux_mod = flux_fit - res * err_fit
    
    # We will get the residuals using the true theta
    res_true = get_residuals(theta_shared, theta_h1, pm, original_data_blocks, z_abs_ref, c_kms, engine, model_type=model_type)
    
    # Instead of reconstructing the blocks manually here, it's easier to just call get_residuals,
    # extract the exact flux_mod array, and add noise to it.
    # To do that, we can modify get_residuals to return flux_mod, but for now we can hack it:
    
    idx = 0
    for block in original_data_blocks:
        n_pixels = len(block['wave'])
        res_chunk = res_true[idx:idx+n_pixels]
        idx += n_pixels
        
        flux_mod = block['flux'] - res_chunk * block['err']
        
        # Add synthetic noise
        noise = student_t.rvs(noise_cfg['nu'], loc=noise_cfg['location'], scale=noise_cfg['scale'], size=n_pixels)
        syn_flux = flux_mod + noise * block['err']
        
        syn_blocks.append({
            'wave': block['wave'],
            'flux': syn_flux,
            'err': block['err'],
            'vsig': block['vsig'],
            'w_min': block['w_min'],
            'w_max': block['w_max']
        })
        
    return syn_blocks

def run_recovery_tests():
    print("--- Phase D4: Synthetic H0/H1 Recovery Tests ---")
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
    
    # Load original data blocks
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
    
    print("\n--- Test 1: Inject H0, Recover H0 vs H1 ---")
    np.random.seed(42)
    syn_blocks_h0 = generate_synthetic_data(theta_shared_base, None, pm, data_blocks, z_abs_ref, c_kms, engine, noise_cfg, model_type='H0')
    
    # Fit H0
    res_h0_syn = get_residuals(theta_shared_base, None, pm, syn_blocks_h0, z_abs_ref, c_kms, engine, model_type='H0')
    ll_h0_syn = -objective_t(res_h0_syn, noise_cfg)
    
    # Fit H1
    best_h1_init = grid_search_h1(theta_shared_base, pm, syn_blocks_h0, z_abs_ref, c_kms, engine, noise_cfg)
    def restr_obj_syn_h0(th_h1):
        r = get_residuals(theta_shared_base, th_h1, pm, syn_blocks_h0, z_abs_ref, c_kms, engine, model_type='H1')
        return objective_t(r, noise_cfg)
    res_h1_syn = minimize(restr_obj_syn_h0, best_h1_init, method='L-BFGS-B', bounds=[(-150.0, 50.0), (10.0, 16.0), (4.0, 20.0)], options={'maxiter': 50})
    ll_h1_syn = -res_h1_syn.fun
    
    print(f"Injected H0: LL(H0) = {ll_h0_syn:.2f}, LL(H1) = {ll_h1_syn:.2f}")
    aic_h0 = -2 * ll_h0_syn
    aic_h1 = 6 - 2 * ll_h1_syn
    if aic_h0 < aic_h1:
        print("PASS: H0 correctly preferred by AIC when H0 is injected.")
    else:
        print("FAIL: False H1 selection under H0 injection by AIC!")
        
    print("\n--- Test 2: Inject H1 (v=-45 km/s), Recover H0 vs H1 ---")
    true_h1_params = [-45.0, 13.5, 10.0]
    syn_blocks_h1 = generate_synthetic_data(theta_shared_base, true_h1_params, pm, data_blocks, z_abs_ref, c_kms, engine, noise_cfg, model_type='H1')
    
    # Fit H0
    res_h0_syn2 = get_residuals(theta_shared_base, None, pm, syn_blocks_h1, z_abs_ref, c_kms, engine, model_type='H0')
    ll_h0_syn2 = -objective_t(res_h0_syn2, noise_cfg)
    
    # Fit H1
    best_h1_init2 = grid_search_h1(theta_shared_base, pm, syn_blocks_h1, z_abs_ref, c_kms, engine, noise_cfg)
    def restr_obj_syn_h1(th_h1):
        r = get_residuals(theta_shared_base, th_h1, pm, syn_blocks_h1, z_abs_ref, c_kms, engine, model_type='H1')
        return objective_t(r, noise_cfg)
    res_h1_syn2 = minimize(restr_obj_syn_h1, best_h1_init2, method='L-BFGS-B', bounds=[(-150.0, 50.0), (10.0, 16.0), (4.0, 20.0)], options={'maxiter': 50})
    ll_h1_syn2 = -res_h1_syn2.fun
    
    print(f"Injected H1: LL(H0) = {ll_h0_syn2:.2f}, LL(H1) = {ll_h1_syn2:.2f}")
    aic_h0 = -2 * ll_h0_syn2
    aic_h1 = 6 - 2 * ll_h1_syn2
    if aic_h1 < aic_h0:
        print(f"PASS: H1 correctly preferred by AIC when H1 is injected. Recovered params: {res_h1_syn2.x}")
    else:
        print(f"FAIL: False H0 selection under H1 injection by AIC! Recovered params: {res_h1_syn2.x}")

if __name__ == '__main__':
    run_recovery_tests()
