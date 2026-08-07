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

def get_pixel_lls(theta_shared, theta_h1, pm, data_blocks, z_abs_ref, c_kms, engine, noise_cfg, model_type='H0'):
    """Returns the per-pixel log-likelihood contributions."""
    res = get_residuals(theta_shared, theta_h1, pm, data_blocks, z_abs_ref, c_kms, engine, model_type)
    # student_t logpdf
    nu, loc, scale = noise_cfg['nu'], noise_cfg['location'], noise_cfg['scale']
    from scipy.stats import t as student_t
    return student_t.logpdf(res, nu, loc=loc, scale=scale)

def run_symmetric_reopt():
    print("--- Phase E1: Symmetric Re-optimization (H0b vs H1) ---")
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
    
    # ---------------------------------------------------------
    # H0a: Published D
    # ---------------------------------------------------------
    print("\n[H0a] Published D")
    res_h0a = get_residuals(theta_shared_base, None, pm, data_blocks, z_abs_ref, c_kms, engine, model_type='H0')
    ll_h0a = -objective_t(res_h0a, noise_cfg)
    print(f"  -> LL: {ll_h0a:.2f}")

    # ---------------------------------------------------------
    # H0b: Refit D
    # ---------------------------------------------------------
    print("\n[H0b] Refit D (Symmetric Re-optimization)")
    def obj_h0b(th):
        return objective_t(get_residuals(th, None, pm, data_blocks, z_abs_ref, c_kms, engine, model_type='H0'), noise_cfg)
    
    # Note: L-BFGS-B needs bounds. We can construct bounds from pm, or just use unbounded (None) 
    # since we just want local relaxation. We will use unbounded for simplicity in this baseline relaxation.
    t0 = time.time()
    res_h0b = minimize(obj_h0b, theta_shared_base, method='L-BFGS-B', options={'maxiter': 10, 'ftol': 1e-6})
    t1 = time.time()
    ll_h0b = -res_h0b.fun
    print(f"  -> LL: {ll_h0b:.2f} (Time: {t1-t0:.1f}s, Iter: {res_h0b.nit})")
    
    # ---------------------------------------------------------
    # H1: Refit H1
    # ---------------------------------------------------------
    print("\n[H1] Refit H1 (Symmetric Re-optimization)")
    best_h1_init = grid_search_h1(theta_shared_base, pm, data_blocks, z_abs_ref, c_kms, engine, noise_cfg)
    # first restrict refinement
    def restr_obj(th_h1):
        return objective_t(get_residuals(theta_shared_base, th_h1, pm, data_blocks, z_abs_ref, c_kms, engine, model_type='H1'), noise_cfg)
    restr_res = minimize(restr_obj, best_h1_init, method='L-BFGS-B', bounds=[(-150.0, 50.0), (10.0, 16.0), (4.0, 20.0)], options={'maxiter': 50})
    best_h1_refined = restr_res.x
    
    # Joint refinement
    def obj_h1_joint(th_joint):
        th_sh = th_joint[:-3]
        th_h1 = th_joint[-3:]
        return objective_t(get_residuals(th_sh, th_h1, pm, data_blocks, z_abs_ref, c_kms, engine, model_type='H1'), noise_cfg)
        
    th_joint_init = np.concatenate([theta_shared_base, best_h1_refined])
    bounds_joint = [(None, None)] * len(theta_shared_base) + [(-150.0, 50.0), (10.0, 16.0), (4.0, 20.0)]
    
    t0 = time.time()
    res_h1 = minimize(obj_h1_joint, th_joint_init, method='L-BFGS-B', bounds=bounds_joint, options={'maxiter': 10, 'ftol': 1e-6})
    t1 = time.time()
    ll_h1 = -res_h1.fun
    print(f"  -> LL: {ll_h1:.2f} (Time: {t1-t0:.1f}s, Iter: {res_h1.nit})")
    
    th_h1_opt = res_h1.x[-3:]
    print(f"  -> H1 Component Params: v={th_h1_opt[0]:.2f}, logN={th_h1_opt[1]:.2f}, b={th_h1_opt[2]:.2f}")
    
    # ---------------------------------------------------------
    # Decompose Delta LL
    # ---------------------------------------------------------
    ll_pix_h0b = get_pixel_lls(res_h0b.x, None, pm, data_blocks, z_abs_ref, c_kms, engine, noise_cfg, 'H0')
    ll_pix_h1 = get_pixel_lls(res_h1.x[:-3], res_h1.x[-3:], pm, data_blocks, z_abs_ref, c_kms, engine, noise_cfg, 'H1')
    
    delta_ll_pix = ll_pix_h1 - ll_pix_h0b
    
    decomp = []
    idx = 0
    for block in data_blocks:
        n_pix = len(block['wave'])
        dll = delta_ll_pix[idx:idx+n_pix]
        idx += n_pix
        
        sum_dll = np.sum(dll)
        # Identify transition roughly by central wavelength
        cw = (block['w_min'] + block['w_max']) / 2.0
        rest_cw = cw / (1 + z_abs_ref)
        if rest_cw > 1200: trans = "Lya"
        elif rest_cw > 1020: trans = "Lyb"
        elif rest_cw > 970: trans = "Lyg"
        elif rest_cw > 940: trans = "Lyd"
        else: trans = "Lye+"
            
        decomp.append({
            'coadd': block['coadd'],
            'transition': trans,
            'w_min': block['w_min'],
            'w_max': block['w_max'],
            'delta_ll': float(sum_dll),
            'n_pixels': n_pix
        })
        
    print("\n[Decomposition]")
    decomp.sort(key=lambda x: x['delta_ll'], reverse=True)
    for d in decomp:
        print(f"  {d['coadd']:12} | {d['transition']:4} | {d['w_min']:.1f}-{d['w_max']:.1f} | dLL: {d['delta_ll']:6.1f} | N: {d['n_pixels']}")
        
    results = {
        'H0a_LL': float(ll_h0a),
        'H0b_LL': float(ll_h0b),
        'H1_LL': float(ll_h1),
        'H1_params': th_h1_opt.tolist(),
        'decomp': decomp
    }
    with open(project_root / 'data' / 'processed' / 'q1009_forensic_reopt.json', 'w') as f:
        json.dump(results, f, indent=4)

if __name__ == '__main__':
    run_symmetric_reopt()
