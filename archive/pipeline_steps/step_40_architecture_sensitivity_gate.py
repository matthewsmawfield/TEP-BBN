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

def run_architecture_sensitivity_gate():
    print("=== Phase E: Model-Architecture Sensitivity Gate ===")
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
    
    # Test 1, 2, and 3 candidate components for D and H hypotheses
    architecture_results = {}
    
    # 1 component
    g_D1 = build_model_components('M_Dfree', theta_shared_base, [12.5, 10000.0, 5.0], pm, z_abs_ref, c_kms)
    g_H1 = build_model_components('M_H', theta_shared_base, [-135.0, 12.5, 10000.0, 5.0], pm, z_abs_ref, c_kms)
    
    ll_D1 = float(-np.sum(student_t.logpdf(compute_residuals(g_D1, data_blocks, engine), noise_cfg['nu'], noise_cfg['location'], noise_cfg['scale'])))
    ll_H1 = float(-np.sum(student_t.logpdf(compute_residuals(g_H1, data_blocks, engine), noise_cfg['nu'], noise_cfg['location'], noise_cfg['scale'])))
    
    architecture_results['1_component'] = {
        'll_D': ll_D1, 'll_H': ll_H1, 'preferred': 'H' if ll_H1 > ll_D1 else 'D'
    }
    print(f"1 Candidate Component: LL_D={ll_D1:.2f}, LL_H={ll_H1:.2f} -> Preferred: {architecture_results['1_component']['preferred']}")
    
    # 2 components
    g_D2 = build_model_components('M_Dfree', theta_shared_base, [12.5, 10000.0, 5.0], pm, z_abs_ref, c_kms)
    g_D2['D_I'].append({'v': -81.6 - 15.0, 'N': 10**12.0, 'b': 8.0})
    
    g_H2 = build_model_components('M_H', theta_shared_base, [-135.0, 12.5, 10000.0, 5.0], pm, z_abs_ref, c_kms)
    g_H2['H_I'].append({'v': -150.0, 'N': 10**12.0, 'b': 8.0})
    
    ll_D2 = float(-np.sum(student_t.logpdf(compute_residuals(g_D2, data_blocks, engine), noise_cfg['nu'], noise_cfg['location'], noise_cfg['scale'])))
    ll_H2 = float(-np.sum(student_t.logpdf(compute_residuals(g_H2, data_blocks, engine), noise_cfg['nu'], noise_cfg['location'], noise_cfg['scale'])))
    
    architecture_results['2_components'] = {
        'll_D': ll_D2, 'll_H': ll_H2, 'preferred': 'H' if ll_H2 > ll_D2 else 'D'
    }
    print(f"2 Candidate Components: LL_D={ll_D2:.2f}, LL_H={ll_H2:.2f} -> Preferred: {architecture_results['2_components']['preferred']}")
    
    # 3 components (Model 6a architecture)
    g_D3 = build_model_components('M_Drefit', theta_shared_base, None, pm, z_abs_ref, c_kms)
    ll_D3 = float(-np.sum(student_t.logpdf(compute_residuals(g_D3, data_blocks, engine), noise_cfg['nu'], noise_cfg['location'], noise_cfg['scale'])))
    
    architecture_results['3_components'] = {
        'll_D': ll_D3, 'll_H': ll_H1, 'preferred': 'H' if ll_H1 > ll_D3 else 'D'
    }
    print(f"3 Candidate Components: LL_D={ll_D3:.2f}, LL_H={ll_H1:.2f} -> Preferred: {architecture_results['3_components']['preferred']}")
    
    out_file = project_root / 'data' / 'processed' / 'q1009_architecture_sensitivity.json'
    with open(out_file, 'w') as f:
        json.dump(architecture_results, f, indent=4)
    print(f"\nSaved architecture sensitivity gate to {out_file}")

if __name__ == '__main__':
    run_architecture_sensitivity_gate()
