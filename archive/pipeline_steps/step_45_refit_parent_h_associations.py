import json
import numpy as np
from pathlib import Path
from scipy.stats import t as student_t
from scipy.optimize import minimize
import os

from scripts.steps.deprecated_classical.step_27c_refit_h0_model_6a import parse_vpfit_ties, ParameterManager
from scripts.lib.physical_rt_engine import RadiativeTransferEngine
from scripts.lib.doppler_physics import compute_doppler_b
from scripts.steps.step_33_build_six_model_family import build_model_components
from scripts.steps.step_34_run_converged_full_models import compute_residuals

def refit_parent_h_associations():
    print("=== Step F3: Plausible Deuterium Parent Component Refitting ===")
    
    project_root = Path(__file__).resolve().parent.parent.parent
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
    comps = pm.reconstruct(theta_shared_base)
    
    # Predeclare plausible H I parent components in the z ~ 2.504 absorption complex
    plausible_parents = []
    h_idx = 0
    for i, c in enumerate(comps):
        if c['ion'] == 'H_I':
            v = c_kms * (c['z'] - z_abs_ref) / (1.0 + z_abs_ref)
            # Only consider components within +- 150 km/s of central system with N_HI > 10^12.5
            if abs(v) < 150.0 and c['logN'] >= 12.5:
                plausible_parents.append({'parent_idx': h_idx, 'z': c['z'], 'v': v, 'logN': c['logN']})
            h_idx += 1
            
    print(f"Found {len(plausible_parents)} physically plausible parent H I components in Q1009 complex:")
    for p in plausible_parents:
        print(f"  Parent {p['parent_idx']}: z={p['z']:.6f}, v={p['v']:.2f} km/s, logN_H={p['logN']:.2f}")
        
    # Discrete parent search penalty: ln(K) where K = len(plausible_parents)
    K_parents = len(plausible_parents)
    ln_K_penalty = np.log(K_parents) if K_parents > 0 else 0.0
    print(f"Parent Search Complexity Penalty: ln(K) = {ln_K_penalty:.3f} nats")
    
    parent_results = []
    best_ll_D_penalized = -np.inf
    best_parent_info = None
    
    for p in plausible_parents:
        p_idx = p['parent_idx']
        target_v_D = p['v'] - 81.6
        
        # Fit D candidate tied to parent p_idx
        def obj_D_parent(th_c):
            logN_D, T_K, b_turb = th_c
            b_D = compute_doppler_b(T_K, b_turb, isotope='D')
            grouped = pm.reconstruct(theta_shared_base)
            grouped_dict = {'H_I': [], 'D_I': [], 'C_IV': [], 'C_III': [], 'C_II': [], 'Si_IV': []}
            for comp in grouped:
                v = c_kms * (comp['z'] - z_abs_ref) / (1.0 + z_abs_ref)
                cd = {'N': 10**comp['logN'], 'b': comp['b'], 'v': v}
                if comp['ion'] in grouped_dict:
                    grouped_dict[comp['ion']].append(cd)
            grouped_dict['D_I'].append({'v': target_v_D, 'N': 10**logN_D, 'b': b_D})
            res = compute_residuals(grouped_dict, data_blocks, engine)
            v_res = res[np.abs(res) < 100.0]
            return -np.sum(student_t.logpdf(v_res, noise_cfg['nu'], noise_cfg['location'], noise_cfg['scale']))
            
        bounds_D = [(10.0, 16.0), (1000.0, 40000.0), (1.0, 30.0)]
        res_opt = minimize(obj_D_parent, [12.4, 10000.0, 1.0], method='L-BFGS-B', bounds=bounds_D)
        ll_raw = -res_opt.fun
        ll_penalized = ll_raw - ln_K_penalty
        
        p_info = {
            'parent_idx': p_idx,
            'parent_v': float(p['v']),
            'target_v_D': float(target_v_D),
            'log_likelihood_raw': float(ll_raw),
            'log_likelihood_penalized': float(ll_penalized),
            'opt_params': {'logN_D': float(res_opt.x[0]), 'T_K': float(res_opt.x[1]), 'b_turb': float(res_opt.x[2])}
        }
        parent_results.append(p_info)
        print(f"  Parent {p_idx} (target v_D = {target_v_D:.2f} km/s): Raw LL = {ll_raw:.2f}, Penalized LL = {ll_penalized:.2f}")
        
        if ll_penalized > best_ll_D_penalized:
            best_ll_D_penalized = ll_penalized
            best_parent_info = p_info
            
    print(f"\n--- STEP F3 RESULT ---")
    print(f"Best D Parent Component: Parent {best_parent_info['parent_idx']} (v_parent = {best_parent_info['parent_v']:.2f} km/s)")
    print(f"Best D-constrained Raw Log Likelihood: {best_parent_info['log_likelihood_raw']:.2f}")
    print(f"Best D-constrained Penalized Log Likelihood (M_D,best): {best_ll_D_penalized:.2f}")
    
    output_dict = {
        'plausible_parents_count': K_parents,
        'parent_search_penalty_ln_K': float(ln_K_penalty),
        'best_parent': best_parent_info,
        'all_parent_results': parent_results,
        'll_D_best': float(best_ll_D_penalized)
    }
    
    os.makedirs("data/processed", exist_ok=True)
    with open("data/processed/q1009_parent_h_association_refit.json", "w") as f:
        json.dump(output_dict, f, indent=2)
        
    print("\nSaved parent H association refit to data/processed/q1009_parent_h_association_refit.json")

if __name__ == "__main__":
    refit_parent_h_associations()
