import json
import os
import numpy as np
from pathlib import Path
from scipy.stats import t as student_t
from scipy.optimize import minimize

from scripts.steps.deprecated_classical.step_27c_refit_h0_model_6a import parse_vpfit_ties, ParameterManager
from scripts.lib.physical_rt_engine import RadiativeTransferEngine
from scripts.lib.doppler_physics import compute_doppler_b
from scripts.steps.step_33_build_six_model_family import build_model_components
from scripts.steps.step_34_run_converged_full_models import compute_residuals

def run_embedding_audit():
    print("=== Phase E: D-to-H Spectral Embedding Audit ===")
    
    project_root = Path(__file__).resolve().parent.parent.parent
    manifest_path = project_root / 'data' / 'processed' / 'Q1009_union_manifest.json'
    vpfit_path = project_root / 'data' / 'literature_components' / 'model_6a.26'
    noise_model_path = project_root / 'configs' / 'tep_noise_model.json'
    results_path = project_root / 'data' / 'processed' / 'q1009_six_model_converged_results.json'
    
    with open(manifest_path, 'r') as f: manifest = json.load(f)
    with open(noise_model_path, 'r') as f: noise_cfg = json.load(f)
    with open(results_path, 'r') as f: converged_results = json.load(f)
    
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
    
    # Best fit Dfree candidate parameters
    dfree_cand = converged_results['M_Dfree']['cand_params']
    logN_D = dfree_cand['logN_D']
    T_K = dfree_cand['T_K']
    b_turb = dfree_cand['b_turb']
    
    print(f"Converged M_Dfree candidate: logN_D={logN_D:.4f}, T_K={T_K:.1f}, b_turb={b_turb:.2f}")
    ll_dfree = converged_results['M_Dfree']['log_likelihood']
    print(f"M_Dfree Log Likelihood: {ll_dfree:.2f}")
    
    # --- Test 1: Direct D to H Embedding Conversion ---
    # In M_Dfree: v_D = v_parent - 81.6
    # An equivalent H component must sit at v_H = v_D = parent_h_v - 81.6
    comps = pm.reconstruct(theta_shared_base)
    parent_h_v = 0.0
    for c in comps:
        if c['ion'] == 'H_I':
            parent_h_v = c_kms * (c['z'] - z_abs_ref) / (1.0 + z_abs_ref)
            break
            
    v_H_embed = parent_h_v - 81.6
    logN_H_embed = logN_D
    
    # Calculate b_H for equivalent thermal/turbulent conditions
    b_H_embed = compute_doppler_b(T_K, b_turb, isotope='H')
    b_D_embed = compute_doppler_b(T_K, b_turb, isotope='D')
    
    print(f"\n--- TEST 1: Embedding Parameter Values ---")
    print(f"Parent H1 v: {parent_h_v:.2f} km/s")
    print(f"Embedded v_H: {v_H_embed:.2f} km/s")
    print(f"Embedded logN_H: {logN_H_embed:.4f}")
    print(f"Calculated b_D: {b_D_embed:.3f} km/s vs b_H: {b_H_embed:.3f} km/s")
    
    # --- TEST 1B: Exact b-matching (T_H adjusted so b_H == b_D) ---
    # b_H^2 = b_turb^2 + 2 k_B T_H / m_p = b_D^2
    # -> 2 k_B T_H / m_p = b_D^2 - b_turb^2 = k_B T_D / m_p -> T_H = T_D / 2 = 5000 K
    T_K_b_matched = T_K / 2.0
    b_H_matched = compute_doppler_b(T_K_b_matched, b_turb, isotope='H')
    
    theta_H_matched = [v_H_embed, logN_H_embed, T_K_b_matched, b_turb]
    grouped_H_matched = build_model_components('M_H', theta_shared_base, theta_H_matched, pm, z_abs_ref, c_kms)
    res_H_matched = compute_residuals(grouped_H_matched, data_blocks, engine)
    v_res_H_matched = res_H_matched[np.abs(res_H_matched) < 100.0]
    ll_H_matched = float(np.sum(student_t.logpdf(v_res_H_matched, noise_cfg['nu'], noise_cfg['location'], noise_cfg['scale'])))
    
    print(f"\n--- TEST 1B: Exact b-matching (T_H = {T_K_b_matched:.1f} K -> b_H = {b_H_matched:.3f} km/s) ---")
    print(f"Log Likelihood (M_H b-matched): {ll_H_matched:.2f}")
    print(f"Delta LL (M_H b-matched - M_Dfree): {ll_H_matched - ll_dfree:.2f}")
    
    # --- Test 2: Optimization from Embedded Start ---
    print(f"\n--- TEST 2: Optimization Starting from Embedded Vector ---")
    def obj_H(th_c):
        grouped = build_model_components('M_H', theta_shared_base, th_c, pm, z_abs_ref, c_kms)
        res = compute_residuals(grouped, data_blocks, engine)
        v_res = res[np.abs(res) < 100.0]
        return -np.sum(student_t.logpdf(v_res, noise_cfg['nu'], noise_cfg['location'], noise_cfg['scale']))
        
    bounds_H = [(-160.0, 50.0), (10.0, 16.0), (1000.0, 40000.0), (1.0, 30.0)]
    res_opt = minimize(obj_H, theta_H_matched, method='L-BFGS-B', bounds=bounds_H, options={'maxiter': 50})
    ll_H_opt_from_embed = -res_opt.fun
    
    print(f"Log Likelihood (M_H optimized from b-matched embed start): {ll_H_opt_from_embed:.2f}")
    print(f"Optimized H parameters from embed start: v_H={res_opt.x[0]:.2f}, logN_H={res_opt.x[1]:.4f}, T_K={res_opt.x[2]:.1f}, b_turb={res_opt.x[3]:.2f}")
    
    # --- Test 3: Optical Depth Inspection across Transitions ---
    print(f"\n--- TEST 3: Optical Depth Comparison (Dfree vs b-matched H) ---")
    grouped_Dfree = build_model_components('M_Dfree', theta_shared_base, [logN_D, T_K, b_turb], pm, z_abs_ref, c_kms)
    
    # Inspect Lyman transitions optical depths
    for t_name in ['HI_Lya', 'HI_Lyb', 'HI_Lyg']:
        lam_rest, f_osc, gamma = engine.atomic.get(t_name)
        wave_test = np.linspace(lam_rest * (1.0 + z_abs_ref) * (1 - 200/c_kms), lam_rest * (1.0 + z_abs_ref) * (1 + 50/c_kms), 500)
        
        tau_D = engine.compute_optical_depth(wave_test, [t_name], grouped_Dfree['D_I'])
        tau_H = engine.compute_optical_depth(wave_test, [t_name], [comp for comp in grouped_H_matched['H_I'] if abs(comp['v'] - v_H_embed) < 1e-3])
        
        max_diff = np.max(np.abs(tau_D - tau_H))
        print(f"Transition {t_name}: Max |tau_D - tau_H| = {max_diff:.6e}")
        
    audit_summary = {
        'll_dfree': ll_dfree,
        'll_H_matched': ll_H_matched,
        'll_H_opt_from_embed': ll_H_opt_from_embed,
        'll_H_previous_converged': converged_results['M_H']['log_likelihood'],
        'delta_ll_embed': ll_H_matched - ll_dfree,
        'v_H_embed': v_H_embed,
        'T_K_b_matched': T_K_b_matched
    }
    
    os.makedirs("data/processed", exist_ok=True)
    with open("data/processed/q1009_d_to_h_embedding_audit.json", "w") as f:
        json.dump(audit_summary, f, indent=2)
        
    print("\nSaved embedding audit summary to data/processed/q1009_d_to_h_embedding_audit.json")

if __name__ == "__main__":
    run_embedding_audit()
