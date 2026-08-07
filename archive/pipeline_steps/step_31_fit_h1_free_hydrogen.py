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

def define_regions():
    return [
        (4258.0, 4260.5), # Primary TEP Lya
        (3593.0, 3594.5)  # Secondary TEP Lyb
    ]

def get_residuals(theta_shared, theta_h1, pm, data_blocks, z_abs_ref, c_kms, engine, model_type='H0'):
    """
    Evaluates the model.
    If model_type == 'H0', includes D I and uses only theta_shared.
    If model_type == 'H1', drops D I, and appends a single free H I component parameterized by theta_h1 [v, logN, b].
    """
    comps = pm.reconstruct(theta_shared)
    grouped_comps = {'H_I': [], 'D_I': [], 'C_IV': [], 'C_III': [], 'C_II': [], 'Si_IV': []}
    for c in comps:
        v = c_kms * (c['z'] - z_abs_ref) / (1.0 + z_abs_ref)
        cd = {'N': 10**c['logN'], 'b': c['b'], 'v': v}
        if c['ion'] == 'D_I':
            cd['v'] -= 81.6
        if c['ion'] in grouped_comps:
            grouped_comps[c['ion']].append(cd)
            
    if model_type == 'H1':
        # Drop the conventional D interpretation
        grouped_comps['D_I'] = []
        # Add the free H I component
        if theta_h1 is not None and len(theta_h1) == 3:
            v_h1, logN_h1, b_h1 = theta_h1
            # If logN is very low, effectively absent
            grouped_comps['H_I'].append({'v': v_h1, 'N': 10**logN_h1, 'b': b_h1})
            
    residuals_all = []
    
    for block in data_blocks:
        wave_fit = block['wave']
        tau_tot = np.zeros_like(wave_fit)
        
        if grouped_comps['H_I']:
            tau_tot += engine.compute_optical_depth(wave_fit, ['HI_Lya', 'HI_Lyb', 'HI_Lyg', 'HI_Ly6', 'HI_Ly13', 'HI_Ly14', 'HI_Ly21'], grouped_comps['H_I'])
        if grouped_comps['D_I']:
            tau_tot += engine.compute_optical_depth(wave_fit, ['HI_Lya', 'HI_Lyb', 'HI_Lyg', 'HI_Ly6', 'HI_Ly13', 'HI_Ly14', 'HI_Ly21'], grouped_comps['D_I'])
        if grouped_comps['C_IV']:
            tau_tot += engine.compute_optical_depth(wave_fit, ['CIV_1548', 'CIV_1550'], grouped_comps['C_IV'])
        if grouped_comps['C_III']:
            tau_tot += engine.compute_optical_depth(wave_fit, ['CIII_977'], grouped_comps['C_III'])
        if grouped_comps['C_II']:
            tau_tot += engine.compute_optical_depth(wave_fit, ['CII_1334'], grouped_comps['C_II'])
        if grouped_comps['Si_IV']:
            tau_tot += engine.compute_optical_depth(wave_fit, ['SiIV_1393', 'SiIV_1402'], grouped_comps['Si_IV'])
            
        x_norm = 2.0 * (wave_fit - block['w_min']) / (block['w_max'] - block['w_min']) - 1.0
        
        P = np.zeros((len(wave_fit), 3))
        P[:, 0] = np.exp(-tau_tot)
        P[:, 1] = x_norm * np.exp(-tau_tot)
        P[:, 2] = 1.0
        
        for k in range(3):
            P[:, k] = engine.apply_convolution(P[:, k], wave_fit, block['vsig'])
            
        err_fit = block['err']
        flux_fit = block['flux']
        
        W = 1.0 / err_fit**2
        H_mat = P.T @ (W[:, np.newaxis] * P)
        b_vec = P.T @ (W * flux_fit)
        
        try:
            c_opt = np.linalg.solve(H_mat, b_vec)
            flux_mod = P @ c_opt
            res = (flux_fit - flux_mod) / err_fit
        except np.linalg.LinAlgError:
            res = np.ones_like(flux_fit) * 1000.0
            
        residuals_all.extend(res)
            
    return np.array(residuals_all)

def objective_t(res, noise_cfg):
    # -logL for minimization
    # Only evaluate valid residuals
    v_res = res[np.abs(res) < 100.0]
    ll = np.sum(student_t.logpdf(v_res, noise_cfg['nu'], noise_cfg['location'], noise_cfg['scale']))
    return -ll

def grid_search_h1(theta_shared_fixed, pm, data_blocks, z_abs_ref, c_kms, engine, noise_cfg):
    print("  -> Performing coarse grid search for H1 component...")
    
    v_grid = np.linspace(-150, 50, 21) 
    logN_grid = [11.0, 12.0, 13.0, 14.0]
    b_grid = [5.0, 10.0, 15.0]
    
    best_ll = np.inf
    best_h1 = None
    
    for v in v_grid:
        for ln in logN_grid:
            for b in b_grid:
                th_h1 = [v, ln, b]
                res = get_residuals(theta_shared_fixed, th_h1, pm, data_blocks, z_abs_ref, c_kms, engine, model_type='H1')
                nll = objective_t(res, noise_cfg)
                if nll < best_ll:
                    best_ll = nll
                    best_h1 = th_h1
                    
    print(f"  -> Best grid candidate: v={best_h1[0]:.1f}, logN={best_h1[1]:.2f}, b={best_h1[2]:.1f} (NLL: {best_ll:.2f})")
    return np.array(best_h1)

def run_h1_search():
    print("--- Phase D3: H1 Candidate Search ---")
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

    # Stage 1: Baseline replay
    theta_shared_base = np.array(pm.theta_init)
    res_h0 = get_residuals(theta_shared_base, None, pm, data_blocks, z_abs_ref, c_kms, engine, model_type='H0')
    ll_h0 = -objective_t(res_h0, noise_cfg)
    print(f"Stage 1: H0 Baseline Log-Likelihood = {ll_h0:.2f}")

    # Stage 2: Candidate profile search
    best_h1_init = grid_search_h1(theta_shared_base, pm, data_blocks, z_abs_ref, c_kms, engine, noise_cfg)

    # Stage 3: Restricted refinement (Only H1 component varies)
    print("Stage 3: Restricted Refinement (H1 vars only)")
    def restricted_obj(th_h1):
        res = get_residuals(theta_shared_base, th_h1, pm, data_blocks, z_abs_ref, c_kms, engine, model_type='H1')
        return objective_t(res, noise_cfg)
    
    res_restr = minimize(
        restricted_obj, best_h1_init, 
        method='L-BFGS-B',
        bounds=[(-150.0, 50.0), (10.0, 16.0), (4.0, 20.0)],
        options={'maxiter': 50}
    )
    best_h1_opt = res_restr.x
    print(f"  -> Refined H1: v={best_h1_opt[0]:.1f}, logN={best_h1_opt[1]:.2f}, b={best_h1_opt[2]:.1f} (NLL: {res_restr.fun:.2f})")
    
    # Stage 4: Full refinement (all parameters)
    print("Stage 4: Full Refinement (All vars)")
    def full_obj(x_full):
        th_shared = x_full[:-3]
        th_h1 = x_full[-3:]
        res = get_residuals(th_shared, th_h1, pm, data_blocks, z_abs_ref, c_kms, engine, model_type='H1')
        return objective_t(res, noise_cfg)
    
    x_full_init = np.concatenate([theta_shared_base, best_h1_opt])
    lower_bounds = np.concatenate([pm.bounds_lower, [-150.0, 10.0, 4.0]])
    upper_bounds = np.concatenate([pm.bounds_upper, [50.0, 16.0, 20.0]])
    bounds = list(zip(lower_bounds, upper_bounds))
    
    res_full = minimize(
        full_obj, x_full_init,
        method='L-BFGS-B',
        bounds=bounds,
        options={'maxiter': 10}  # Small just for script demonstration
    )
    
    final_ll_h1 = -res_full.fun
    print(f"Stage 4: H1 Full Refinement Log-Likelihood = {final_ll_h1:.2f}")

if __name__ == '__main__':
    run_h1_search()
