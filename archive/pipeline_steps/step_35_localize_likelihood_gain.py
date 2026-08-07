import sys
import numpy as np
import json
from pathlib import Path
from scipy.stats import t as student_t

script_dir = Path(__file__).parent
project_root = script_dir.parent.parent
sys.path.insert(0, str(project_root))

from scripts.steps.deprecated_classical.step_27c_refit_h0_model_6a import parse_vpfit_ties, ParameterManager
from scripts.lib.physical_rt_engine import RadiativeTransferEngine
from scripts.steps.step_33_build_six_model_family import build_model_components
from scripts.steps.step_34_run_converged_full_models import compute_residuals

def run_likelihood_gain_localization():
    print("=== Phase E: Likelihood Gain Localization ===")
    results_path = project_root / 'data' / 'processed' / 'q1009_six_model_converged_results.json'
    manifest_path = project_root / 'data' / 'processed' / 'Q1009_union_manifest.json'
    vpfit_path = project_root / 'data' / 'literature_components' / 'model_6a.26'
    noise_model_path = project_root / 'configs' / 'tep_noise_model.json'
    
    if not results_path.exists():
        print(f"Waiting for converged results file {results_path}...")
        return
        
    with open(results_path, 'r') as f: models_res = json.load(f)
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
        
        # Categorize Lyman transition window
        w_center = (r['w_min'] + r['w_max']) / 2.0
        if 4250.0 <= w_center <= 4270.0 or 4670.0 <= w_center <= 5440.0:
            trans = 'Lya'
        elif 3590.0 <= w_center <= 3600.0:
            trans = 'Lyb'
        elif 3400.0 <= w_center <= 3430.0:
            trans = 'Lyg'
        else:
            trans = 'Lye+'
            
        data_blocks.append({
            'wave': wave[mask], 'flux': flux[mask], 'err': err[mask],
            'vsig': r['vsig'], 'w_min': r['w_min'], 'w_max': r['w_max'],
            'coadd': coadd, 'transition': trans
        })

    # D-sensitive in-window definition: 4254.4 - 4265.0
    in_window_mask = []
    block_info = []
    
    for b in data_blocks:
        in_win = (b['wave'] >= 4254.4) & (b['wave'] <= 4265.0)
        in_window_mask.extend(in_win)
        block_info.extend([(b['coadd'], b['transition'], b['w_min'], b['w_max'])] * len(b['wave']))
        
    in_window_mask = np.array(in_window_mask)
    
    # We compare M_H vs M_Dfree
    # Reconstruct grouped comps for M_Dfree and M_H
    # If not fully saved, evaluate default candidate params from json
    theta_shared_base = np.array(pm.theta_init)
    
    cand_Dfree = [models_res['M_Dfree']['cand_params'][k] for k in ['logN_D', 'T_K', 'b_turb']] if 'M_Dfree' in models_res else [12.5, 10000.0, 5.0]
    cand_H = [models_res['M_H']['cand_params'][k] for k in ['v_H', 'logN_H', 'T_K', 'b_turb']] if 'M_H' in models_res else [-135.0, 12.5, 10000.0, 5.0]
    
    g_Dfree = build_model_components('M_Dfree', theta_shared_base, cand_Dfree, pm, z_abs_ref, c_kms)
    g_H = build_model_components('M_H', theta_shared_base, cand_H, pm, z_abs_ref, c_kms)
    
    res_Dfree = compute_residuals(g_Dfree, data_blocks, engine)
    res_H = compute_residuals(g_H, data_blocks, engine)
    
    ll_pix_Dfree = student_t.logpdf(res_Dfree, noise_cfg['nu'], noise_cfg['location'], noise_cfg['scale'])
    ll_pix_H = student_t.logpdf(res_H, noise_cfg['nu'], noise_cfg['location'], noise_cfg['scale'])
    
    dll_pix = ll_pix_H - ll_pix_Dfree
    
    in_window_dll = np.sum(dll_pix[in_window_mask])
    out_window_dll = np.sum(dll_pix[~in_window_mask])
    total_dll = np.sum(dll_pix)
    
    print(f"\n[Likelihood Gain Localization: M_H vs M_Dfree]")
    print(f"  Total dLL:       {total_dll:.2f}")
    print(f"  In-Window dLL:   {in_window_dll:.2f} (Pixels: {np.sum(in_window_mask)})")
    print(f"  Out-Window dLL:  {out_window_dll:.2f} (Pixels: {np.sum(~in_window_mask)})")
    
    output = {
        'total_dll': float(total_dll),
        'in_window_dll': float(in_window_dll),
        'out_window_dll': float(out_window_dll),
        'in_window_pixels': int(np.sum(in_window_mask)),
        'out_window_pixels': int(np.sum(~in_window_mask))
    }
    
    out_file = project_root / 'data' / 'processed' / 'q1009_likelihood_localization.json'
    with open(out_file, 'w') as f:
        json.dump(output, f, indent=4)
    print(f"Saved localization summary to {out_file}")

if __name__ == '__main__':
    run_likelihood_gain_localization()
