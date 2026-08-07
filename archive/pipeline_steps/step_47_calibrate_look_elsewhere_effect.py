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

def calibrate_look_elsewhere_effect():
    print("=== Step F5: Look-Elsewhere Calibration of the Search Gain ===", flush=True)
    
    project_root = Path(__file__).resolve().parent.parent.parent
    manifest_path = project_root / 'data' / 'processed' / 'Q1009_union_manifest.json'
    vpfit_path = project_root / 'data' / 'literature_components' / 'model_6a.26'
    noise_model_path = project_root / 'configs' / 'tep_noise_model.json'
    parent_refit_path = project_root / 'data' / 'processed' / 'q1009_parent_h_association_refit.json'
    profile_path = project_root / 'data' / 'processed' / 'q1009_candidate_velocity_profile.json'
    
    with open(manifest_path, 'r') as f: manifest = json.load(f)
    with open(noise_model_path, 'r') as f: noise_cfg = json.load(f)
    with open(parent_refit_path, 'r') as f: parent_refit = json.load(f)
    with open(profile_path, 'r') as f: profile_data = json.load(f)
    
    ll_D_best = parent_refit['ll_D_best']
    ll_H_best = profile_data['ll_H_best']
    obs_search_gain = ll_H_best - ll_D_best
    
    print(f"Penalized Best D Log Likelihood (M_D,best): {ll_D_best:.2f}", flush=True)
    print(f"Free H Log Likelihood (M_H,free):           {ll_H_best:.2f}", flush=True)
    print(f"Observed Search Gain Delta LL_search:        {obs_search_gain:.2f}", flush=True)
    
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
    
    # Pre-calculate true D model flux and search grid model fluxes ONCE
    grouped_D10 = build_model_components('M_Dfree', theta_shared_base, [12.4, 10000.0, 1.0], pm, z_abs_ref, c_kms)
    
    true_D_fluxes = []
    for block in data_blocks:
        tau = engine.compute_optical_depth(block['wave'], ['HI_Lya', 'HI_Lyb', 'HI_Lyg'], grouped_D10['H_I'] + grouped_D10['D_I'])
        true_D_fluxes.append(np.exp(-tau))
        
    v_search_grid = np.arange(-140.0, -124.9, 0.50)
    grid_H_fluxes = []
    for v_h in v_search_grid:
        grouped_H = build_model_components('M_H', theta_shared_base, [v_h, 12.4, 5000.0, 1.0], pm, z_abs_ref, c_kms)
        block_H_fluxes = []
        for block in data_blocks:
            tau = engine.compute_optical_depth(block['wave'], ['HI_Lya', 'HI_Lyb', 'HI_Lyg'], grouped_H['H_I'])
            block_H_fluxes.append(np.exp(-tau))
        grid_H_fluxes.append(block_H_fluxes)
        
    n_realizations = 200
    print(f"\nRunning Fast Vectorized Sequential Simulation ({n_realizations} realizations)...", flush=True)
    
    search_gains = []
    nu = noise_cfg['nu']
    scale = noise_cfg['scale']
    
    for seed in range(n_realizations):
        rng = np.random.default_rng(seed + 2000)
        
        # Add noise to pre-calculated true D model fluxes
        ll_synth_D = 0.0
        ll_synth_H_list = np.zeros(len(v_search_grid))
        
        for b_idx, block in enumerate(data_blocks):
            err = block['err']
            noise = student_t.rvs(df=nu, loc=0.0, scale=err * scale, random_state=rng)
            synth_flux = true_D_fluxes[b_idx] + noise
            
            # Residual under D model
            res_D = synth_flux - true_D_fluxes[b_idx]
            v_res_D = res_D / err
            ll_synth_D += float(np.sum(student_t.logpdf(v_res_D, nu, 0.0, scale)))
            
            # Residual under each H model in grid
            for g_idx in range(len(v_search_grid)):
                res_H = synth_flux - grid_H_fluxes[g_idx][b_idx]
                v_res_H = res_H / err
                ll_synth_H_list[g_idx] += float(np.sum(student_t.logpdf(v_res_H, nu, 0.0, scale)))
                
        gain = np.max(ll_synth_H_list) - ll_synth_D
        search_gains.append(float(gain))
        
    search_gains = np.array(search_gains)
    p_value = float(np.mean(search_gains >= obs_search_gain))
    percentile_95 = float(np.percentile(search_gains, 95))
    percentile_99 = float(np.percentile(search_gains, 99))
    max_synth_gain = float(np.max(search_gains))
    
    print(f"\n--- STEP F5 RESULT ---", flush=True)
    print(f"Observed Free-H Search Gain (Delta LL_search): {obs_search_gain:.2f}", flush=True)
    print(f"Synthetic Look-Elsewhere Gain 95th percentile: {percentile_95:.2f}", flush=True)
    print(f"Synthetic Look-Elsewhere Gain 99th percentile: {percentile_99:.2f}", flush=True)
    print(f"Max Synthetic Look-Elsewhere Gain:             {max_synth_gain:.2f}", flush=True)
    print(f"Calibrated p-value for observed gain:           p = {p_value:.4f}", flush=True)
    print(f"Is observed gain significant at p < 0.01?       {p_value < 0.01}", flush=True)
    
    output_dict = {
        'n_realizations': n_realizations,
        'll_D_best': float(ll_D_best),
        'll_H_best': float(ll_H_best),
        'obs_search_gain': float(obs_search_gain),
        'percentile_95': percentile_95,
        'percentile_99': percentile_99,
        'max_synth_gain': max_synth_gain,
        'calibrated_p_value': p_value,
        'is_significant_p01': bool(p_value < 0.01),
        'search_gains': [float(x) for x in search_gains]
    }
    
    os.makedirs("data/processed", exist_ok=True)
    with open("data/processed/q1009_look_elsewhere_calibration.json", "w") as f:
        json.dump(output_dict, f, indent=2)
        
    print("\nSaved look-elsewhere calibration to data/processed/q1009_look_elsewhere_calibration.json", flush=True)

if __name__ == "__main__":
    calibrate_look_elsewhere_effect()
