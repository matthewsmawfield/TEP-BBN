import json
import numpy as np
from pathlib import Path
from scipy.stats import t as student_t
import os

from scripts.steps.deprecated_classical.step_27c_refit_h0_model_6a import parse_vpfit_ties, ParameterManager
from scripts.lib.physical_rt_engine import RadiativeTransferEngine
from scripts.lib.doppler_physics import compute_doppler_b
from scripts.steps.step_33_build_six_model_family import build_model_components
from scripts.steps.step_34_run_converged_full_models import compute_residuals

def profile_candidate_velocity():
    print("=== Step F1: Adaptive Candidate Velocity Profiling ===", flush=True)
    
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
            
    v_D_predicted = parent_h_v - 81.6
    print(f"Parent H I velocity: {parent_h_v:.2f} km/s", flush=True)
    print(f"Predicted D I velocity: {v_D_predicted:.2f} km/s", flush=True)
    
    # Evaluate M_Dfree at predicted D position
    grouped_Dfree = build_model_components('M_Dfree', theta_shared_base, [12.4096, 9999.9, 1.0], pm, z_abs_ref, c_kms)
    res_Dfree = compute_residuals(grouped_Dfree, data_blocks, engine)
    v_res_Dfree = res_Dfree[np.abs(res_Dfree) < 100.0]
    ll_Dfree = float(np.sum(student_t.logpdf(v_res_Dfree, noise_cfg['nu'], noise_cfg['location'], noise_cfg['scale'])))
    print(f"Evaluated Log Likelihood (M_Dfree): {ll_Dfree:.2f}", flush=True)
    
    # 1. Coarse Scan: -140.0 to -125.0 km/s at 0.20 km/s
    coarse_grid = np.arange(-140.0, -124.95, 0.20)
    
    def eval_at_v(v_h):
        # Evaluate candidate H I component at velocity v_h with logN_H = 12.4573, T_K = 5000.0, b_turb = 1.0
        grouped = build_model_components('M_H', theta_shared_base, [v_h, 12.4573, 5000.0, 1.0], pm, z_abs_ref, c_kms)
        res = compute_residuals(grouped, data_blocks, engine)
        v_res = res[np.abs(res) < 100.0]
        return float(np.sum(student_t.logpdf(v_res, noise_cfg['nu'], noise_cfg['location'], noise_cfg['scale'])))
        
    print("\nRunning Adaptive Coarse & Fine Scan...", flush=True)
    ll_coarse = np.array([eval_at_v(v) for v in coarse_grid])
    
    best_coarse_idx = int(np.argmax(ll_coarse))
    best_coarse_v = coarse_grid[best_coarse_idx]
    best_coarse_ll = ll_coarse[best_coarse_idx]
    
    print(f"Coarse Scan Best v_H: {best_coarse_v:.2f} km/s, Log L: {best_coarse_ll:.2f}", flush=True)
    
    # 2. Fine Scan: +- 1.0 km/s around peak at 0.01 km/s
    fine_grid = np.arange(best_coarse_v - 1.0, best_coarse_v + 1.01, 0.01)
    ll_fine = np.array([eval_at_v(v) for v in fine_grid])
    
    best_fine_idx = int(np.argmax(ll_fine))
    v_H_best = fine_grid[best_fine_idx]
    ll_H_best = ll_fine[best_fine_idx]
    
    delta_v = v_H_best - v_D_predicted
    delta_ll_de_novo = ll_H_best - ll_Dfree
    
    # Statistical 1-sigma and 3-sigma confidence intervals
    in_1sig = fine_grid[ll_H_best - ll_fine <= 0.5]
    in_3sig = fine_grid[ll_H_best - ll_fine <= 4.5]
    
    sig1_min, sig1_max = np.min(in_1sig), np.max(in_1sig)
    sig3_min, sig3_max = np.min(in_3sig), np.max(in_3sig)
    
    print(f"\n--- STEP F1 RESULT ---", flush=True)
    print(f"Predicted D velocity (v_D): {v_D_predicted:.2f} km/s", flush=True)
    print(f"Best Free-H velocity (v_H): {v_H_best:.2f} km/s", flush=True)
    print(f"Observed Velocity Displacement (Delta v): {delta_v:.2f} km/s", flush=True)
    print(f"Log Likelihood (M_Dfree): {ll_Dfree:.2f}", flush=True)
    print(f"Log Likelihood (M_H best): {ll_H_best:.2f}", flush=True)
    print(f"De Novo Delta Log Likelihood: {delta_ll_de_novo:.2f}", flush=True)
    print(f"1-sigma Statistical Interval on v_H: [{sig1_min:.2f}, {sig1_max:.2f}] km/s", flush=True)
    print(f"3-sigma Statistical Interval on v_H: [{sig3_min:.2f}, {sig3_max:.2f}] km/s", flush=True)
    print(f"Is v_D_predicted (-134.03) excluded at 3-sigma? {v_D_predicted < sig3_min or v_D_predicted > sig3_max}", flush=True)
    
    output_dict = {
        'v_D_predicted': float(v_D_predicted),
        'v_H_best': float(v_H_best),
        'delta_v': float(delta_v),
        'll_Dfree': float(ll_Dfree),
        'll_H_best': float(ll_H_best),
        'delta_ll_de_novo': float(delta_ll_de_novo),
        'logN_H_best': 12.4573,
        'T_K_best': 5000.0,
        'b_turb_best': 1.0,
        'sig1_interval': [float(sig1_min), float(sig1_max)],
        'sig3_interval': [float(sig3_min), float(sig3_max)],
        'v_D_excluded_3sig': bool(v_D_predicted < sig3_min or v_D_predicted > sig3_max),
        'fine_grid': [float(x) for x in fine_grid],
        'll_fine': [float(x) for x in ll_fine]
    }
    
    os.makedirs("data/processed", exist_ok=True)
    with open("data/processed/q1009_candidate_velocity_profile.json", "w") as f:
        json.dump(output_dict, f, indent=2)
        
    print("\nSaved velocity profile to data/processed/q1009_candidate_velocity_profile.json", flush=True)

if __name__ == "__main__":
    profile_candidate_velocity()
