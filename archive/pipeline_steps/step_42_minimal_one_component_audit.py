import json
import numpy as np
from pathlib import Path
from scipy.stats import t as student_t

from scripts.steps.deprecated_classical.step_27c_refit_h0_model_6a import parse_vpfit_ties, ParameterManager
from scripts.lib.physical_rt_engine import RadiativeTransferEngine
from scripts.lib.doppler_physics import compute_doppler_b
from scripts.steps.step_34_run_converged_full_models import compute_residuals

def run_minimal_one_component_audit():
    print("=== Phase E: Minimal Independent One-Component Likelihood Surface Audit ===")
    
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
            
    v_D_target = parent_h_v - 81.6
    print(f"Parent H I v: {parent_h_v:.2f} km/s, Target D I v: {v_D_target:.2f} km/s")
    
    # Baseline components without candidate
    grouped_base = {'H_I': [], 'D_I': [], 'C_IV': [], 'C_III': [], 'C_II': [], 'Si_IV': []}
    for c in comps:
        v = c_kms * (c['z'] - z_abs_ref) / (1.0 + z_abs_ref)
        cd = {'N': 10**c['logN'], 'b': c['b'], 'v': v}
        if c['ion'] in grouped_base and c['ion'] != 'D_I':
            grouped_base[c['ion']].append(cd)
            
    # Direct profile grid for D component: logN_D in [12.0, 13.0], b_D = 9.141 km/s (T=10000, b_turb=1.0)
    b_D = compute_doppler_b(10000.0, 1.0, isotope='D')
    logN_grid = np.linspace(12.0, 13.0, 21)
    
    best_ll_D = -np.inf
    best_logN_D = None
    for logN in logN_grid:
        grouped = {k: list(v) for k, v in grouped_base.items()}
        grouped['D_I'].append({'v': v_D_target, 'N': 10**logN, 'b': b_D})
        res = compute_residuals(grouped, data_blocks, engine)
        v_res = res[np.abs(res) < 100.0]
        ll = np.sum(student_t.logpdf(v_res, noise_cfg['nu'], noise_cfg['location'], noise_cfg['scale']))
        if ll > best_ll_D:
            best_ll_D = ll
            best_logN_D = logN
            
    print(f"Minimal D Profile Best LL: {best_ll_D:.2f} (logN_D={best_logN_D:.2f}, b_D={b_D:.3f})")
    
    # Direct profile grid for H component: v_H in [-140.0, -125.0], logN_H in [12.0, 13.0]
    # For H with T=5000 K, b_turb=1.0 -> b_H = 9.141 km/s (b-matched to D)
    b_H_matched = compute_doppler_b(5000.0, 1.0, isotope='H')
    v_grid = np.linspace(-136.0, -130.0, 13)
    logN_grid_h = np.linspace(12.2, 12.6, 9)
    
    best_ll_H = -np.inf
    best_v_H = None
    best_logN_H = None
    
    for v_H in v_grid:
        for logN in logN_grid_h:
            grouped = {k: list(v) for k, v in grouped_base.items()}
            grouped['H_I'].append({'v': v_H, 'N': 10**logN, 'b': b_H_matched})
            res = compute_residuals(grouped, data_blocks, engine)
            v_res = res[np.abs(res) < 100.0]
            ll = np.sum(student_t.logpdf(v_res, noise_cfg['nu'], noise_cfg['location'], noise_cfg['scale']))
            if ll > best_ll_H:
                best_ll_H = ll
                best_v_H = v_H
                best_logN_H = logN
                
    print(f"Minimal H Profile Best LL: {best_ll_H:.2f} (v_H={best_v_H:.2f}, logN_H={best_logN_H:.2f}, b_H={b_H_matched:.3f})")
    print(f"Delta LL (Minimal H Profile Best - Minimal D Profile Best): {best_ll_H - best_ll_D:.2f}")

if __name__ == "__main__":
    run_minimal_one_component_audit()
