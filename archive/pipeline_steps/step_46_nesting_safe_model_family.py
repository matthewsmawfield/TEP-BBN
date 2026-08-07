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

def run_nesting_safe_model_family():
    print("=== Step F4: Nesting-Safe Rerun of the Complete Model Family ===")
    
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
    parent_h_v = 0.0
    for c in comps:
        if c['ion'] == 'H_I':
            parent_h_v = c_kms * (c['z'] - z_abs_ref) / (1.0 + z_abs_ref)
            break
            
    v_D = parent_h_v - 81.6
    
    # 1. Fit M_Dfree
    def obj_Dfree(p):
        logN_D, T_K, b_turb = p
        b_D = compute_doppler_b(T_K, b_turb, isotope='D')
        grouped = build_model_components('M_Dfree', theta_shared_base, [logN_D, T_K, b_turb], pm, z_abs_ref, c_kms)
        res = compute_residuals(grouped, data_blocks, engine)
        v_res = res[np.abs(res) < 100.0]
        return -np.sum(student_t.logpdf(v_res, noise_cfg['nu'], noise_cfg['location'], noise_cfg['scale']))
        
    res_Dfree = minimize(obj_Dfree, [12.4, 10000.0, 1.0], method='L-BFGS-B', bounds=[(10.0, 16.0), (1000.0, 40000.0), (1.0, 30.0)])
    ll_Dfree = -res_Dfree.fun
    opt_Dfree = res_Dfree.x
    print(f"M_Dfree Best LL: {ll_Dfree:.2f} (logN_D={opt_Dfree[0]:.4f}, T_K={opt_Dfree[1]:.1f}, b_turb={opt_Dfree[2]:.2f})")
    
    # 2. Fit M_H starting from nesting-safe pool (including exact b-matched D embedding)
    def obj_H(p):
        v_H, logN_H, T_K, b_turb = p
        b_H = compute_doppler_b(T_K, b_turb, isotope='H')
        grouped = build_model_components('M_H', theta_shared_base, [v_H, logN_H, T_K, b_turb], pm, z_abs_ref, c_kms)
        res = compute_residuals(grouped, data_blocks, engine)
        v_res = res[np.abs(res) < 100.0]
        return -np.sum(student_t.logpdf(v_res, noise_cfg['nu'], noise_cfg['location'], noise_cfg['scale']))
        
    # Pool of nesting-safe initial starts
    starts_H = [
        [v_D, opt_Dfree[0], opt_Dfree[1] / 2.0, opt_Dfree[2]], # Exact b-matched D embedding start
        [-132.0, 12.45, 5000.0, 1.0],                         # Free-H optimum start
        [-135.0, 12.50, 10000.0, 1.0]                          # Standard start
    ]
    
    best_ll_H = -np.inf
    best_opt_H = None
    bounds_H = [(-160.0, 50.0), (10.0, 16.0), (1000.0, 40000.0), (1.0, 30.0)]
    for x0 in starts_H:
        res = minimize(obj_H, x0, method='L-BFGS-B', bounds=bounds_H)
        if -res.fun > best_ll_H:
            best_ll_H = -res.fun
            best_opt_H = res.x
            
    print(f"M_H Best LL: {best_ll_H:.2f} (v_H={best_opt_H[0]:.2f}, logN_H={best_opt_H[1]:.4f}, T_K={best_opt_H[2]:.1f}, b_turb={best_opt_H[3]:.2f})")
    
    # Automated Nesting Invariant 1 Assertion
    assert best_ll_H >= ll_Dfree - 1e-4, f"Nesting Invariant 1 Violated: LL(M_H)={best_ll_H:.4f} < LL(M_Dfree)={ll_Dfree:.4f}"
    print("-> Nesting Invariant 1 Assertion PASSED: LL(M_H) >= LL(M_Dfree)")
    
    # 3. Fit M_D+H (D candidate + H interloper)
    def obj_DplusH(p):
        logN_D, v_H, logN_H, T_K, b_turb = p
        b_D = compute_doppler_b(T_K, b_turb, isotope='D')
        b_H = compute_doppler_b(T_K, b_turb, isotope='H')
        grouped = build_model_components('M_D+H', theta_shared_base, [logN_D, v_H, logN_H, T_K, b_turb], pm, z_abs_ref, c_kms)
        res = compute_residuals(grouped, data_blocks, engine)
        v_res = res[np.abs(res) < 100.0]
        return -np.sum(student_t.logpdf(v_res, noise_cfg['nu'], noise_cfg['location'], noise_cfg['scale']))
        
    bounds_DplusH = [(10.0, 16.0), (-160.0, 50.0), (10.0, 16.0), (1000.0, 40000.0), (1.0, 30.0)]
    res_DplusH = minimize(obj_DplusH, [12.28, -127.89, 12.07, 10000.0, 1.0], method='L-BFGS-B', bounds=bounds_DplusH, options={'maxiter': 15})
    ll_DplusH = -res_DplusH.fun
    opt_DplusH = res_DplusH.x
    print(f"M_D+H Best LL: {ll_DplusH:.2f}")
    
    # 4. Fit M_H+H (Two ordinary H components)
    def obj_HplusH(p):
        v_H1, logN_H1, v_H2, logN_H2, T_K, b_turb = p
        b_H = compute_doppler_b(T_K, b_turb, isotope='H')
        grouped = pm.reconstruct(theta_shared_base)
        grouped_dict = {'H_I': [], 'D_I': [], 'C_IV': [], 'C_III': [], 'C_II': [], 'Si_IV': []}
        for comp in grouped:
            v = c_kms * (comp['z'] - z_abs_ref) / (1.0 + z_abs_ref)
            cd = {'N': 10**comp['logN'], 'b': comp['b'], 'v': v}
            if comp['ion'] in grouped_dict:
                grouped_dict[comp['ion']].append(cd)
        grouped_dict['H_I'].append({'v': v_H1, 'N': 10**logN_H1, 'b': b_H})
        grouped_dict['H_I'].append({'v': v_H2, 'N': 10**logN_H2, 'b': b_H})
        res = compute_residuals(grouped_dict, data_blocks, engine)
        v_res = res[np.abs(res) < 100.0]
        return -np.sum(student_t.logpdf(v_res, noise_cfg['nu'], noise_cfg['location'], noise_cfg['scale']))
        
    # Embedded D+H start for H+H: H1 = embedded D (T=5000 K), H2 = H interloper
    x0_HplusH_embed = [v_D, opt_DplusH[0], opt_DplusH[1], opt_DplusH[2], opt_DplusH[3] / 2.0, opt_DplusH[4]]
    bounds_HplusH = [(-160.0, 50.0), (10.0, 16.0), (-160.0, 50.0), (10.0, 16.0), (1000.0, 40000.0), (1.0, 30.0)]
    res_HplusH = minimize(obj_HplusH, x0_HplusH_embed, method='L-BFGS-B', bounds=bounds_HplusH, options={'maxiter': 15})
    ll_HplusH = -res_HplusH.fun
    opt_HplusH = res_HplusH.x
    print(f"M_H+H Best LL: {ll_HplusH:.2f}")
    
    # Automated Nesting Invariant 2 Assertion
    assert ll_HplusH >= ll_DplusH - 1e-4, f"Nesting Invariant 2 Violated: LL(M_H+H)={ll_HplusH:.4f} < LL(M_D+H)={ll_DplusH:.4f}"
    print("-> Nesting Invariant 2 Assertion PASSED: LL(M_H+H) >= LL(M_D+H)")
    
    output_dict = {
        'll_Dfree': float(ll_Dfree),
        'll_H': float(best_ll_H),
        'll_DplusH': float(ll_DplusH),
        'll_HplusH': float(ll_HplusH),
        'nesting_invariant_1_passed': bool(best_ll_H >= ll_Dfree - 1e-4),
        'nesting_invariant_2_passed': bool(ll_HplusH >= ll_DplusH - 1e-4),
        'opt_H': [float(x) for x in best_opt_H],
        'opt_HplusH': [float(x) for x in opt_HplusH]
    }
    
    os.makedirs("data/processed", exist_ok=True)
    with open("data/processed/q1009_nesting_safe_model_family.json", "w") as f:
        json.dump(output_dict, f, indent=2)
        
    print("\nSaved nesting-safe model family results to data/processed/q1009_nesting_safe_model_family.json")

if __name__ == "__main__":
    run_nesting_safe_model_family()
