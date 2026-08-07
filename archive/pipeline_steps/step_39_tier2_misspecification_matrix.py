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

def apply_independent_misspecification(syn_blocks, perturbation_type='none', seed=42):
    """
    Applies independent model misspecifications to synthetic data arrays:
      - 'extra_H': Weak unresolved extra H component
      - 'lsf_shift': 5% LSF width misestimation
      - 'wave_shift': 0.02 A wavelength registration shift by coadd
      - 'continuum_curvature': Quadratic continuum distortion
    """
    np.random.seed(seed)
    mod_blocks = []
    
    for b in syn_blocks:
        flux = np.copy(b['flux'])
        wave = b['wave']
        
        if perturbation_type == 'extra_H':
            # Add weak interloper at v = -70 km/s
            v_extra = -70.0
            dv = (wave - 4258.0) / 4258.0 * 299792.458
            tau_extra = 0.05 * np.exp(-((dv - v_extra) / 10.0)**2)
            flux = flux * np.exp(-tau_extra)
            
        elif perturbation_type == 'lsf_shift':
            vsig_mod = b['vsig'] * 1.05
            b['vsig'] = vsig_mod
            
        elif perturbation_type == 'wave_shift':
            shift = np.random.uniform(-0.02, 0.02)
            wave = wave + shift
            
        elif perturbation_type == 'continuum_curvature':
            x_norm = (wave - b['w_min']) / (b['w_max'] - b['w_min'])
            flux = flux * (1.0 + 0.01 * (x_norm - 0.5)**2)
            
        mod_blocks.append({
            'wave': wave, 'flux': flux, 'err': b['err'],
            'vsig': b['vsig'], 'w_min': b['w_min'], 'w_max': b['w_max'],
            'coadd': b['coadd']
        })
        
    return mod_blocks

def run_tier2_misspecification_matrix():
    print("=== Phase E: Tier-2 Calibration Matrix under Model Misspecifications ===")
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
    
    perturbations = ['none', 'extra_H', 'lsf_shift', 'wave_shift', 'continuum_curvature']
    misspec_results = {}
    
    for pert in perturbations:
        print(f"\n[Testing Misspecification: {pert}]")
        # Generate base synthetic data for M_Dfree under perturbation
        grouped_D = build_model_components('M_Dfree', theta_shared_base, [12.5, 10000.0, 5.0], pm, z_abs_ref, c_kms)
        syn_raw = []
        for b in data_blocks:
            tau = engine.compute_optical_depth(b['wave'], ['HI_Lya', 'HI_Lyb', 'HI_Lyg'], grouped_D['H_I'])
            tau += engine.compute_optical_depth(b['wave'], ['HI_Lya', 'HI_Lyb', 'HI_Lyg'], grouped_D['D_I'])
            f_true = engine.apply_convolution(np.exp(-tau), b['wave'], b['vsig'])
            noise = student_t.rvs(noise_cfg['nu'], loc=noise_cfg['location'], scale=noise_cfg['scale'], size=len(b['wave'])) * b['err']
            syn_raw.append({
                'wave': b['wave'], 'flux': f_true + noise, 'err': b['err'],
                'vsig': b['vsig'], 'w_min': b['w_min'], 'w_max': b['w_max'],
                'coadd': b['coadd']
            })
            
        syn_pert = apply_independent_misspecification(syn_raw, perturbation_type=pert, seed=500)
        
        # Fit M_Dfree vs M_H
        res_D = compute_residuals(grouped_D, syn_pert, engine)
        ll_D = float(-np.sum(student_t.logpdf(res_D, noise_cfg['nu'], noise_cfg['location'], noise_cfg['scale'])))
        
        grouped_H = build_model_components('M_H', theta_shared_base, [-135.0, 12.5, 10000.0, 5.0], pm, z_abs_ref, c_kms)
        res_H = compute_residuals(grouped_H, syn_pert, engine)
        ll_H = float(-np.sum(student_t.logpdf(res_H, noise_cfg['nu'], noise_cfg['location'], noise_cfg['scale'])))
        
        dL = 2.0 * (ll_H - ll_D)
        print(f"  -> {pert}: LL_D={ll_D:.2f}, LL_H={ll_H:.2f}, 2*dL={dL:.2f}")
        
        misspec_results[pert] = {
            'll_Dfree': ll_D,
            'll_H': ll_H,
            'delta_L_H_minus_D': dL
        }
        
    out_file = project_root / 'data' / 'processed' / 'q1009_misspecification_matrix.json'
    with open(out_file, 'w') as f:
        json.dump(misspec_results, f, indent=4)
    print(f"\nSaved misspecification matrix to {out_file}")

if __name__ == '__main__':
    run_tier2_misspecification_matrix()
