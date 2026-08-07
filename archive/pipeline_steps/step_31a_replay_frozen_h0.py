import sys
import json
import hashlib
from pathlib import Path
import numpy as np
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

def in_tep_window(wave, tep_windows):
    mask = np.zeros_like(wave, dtype=bool)
    for w_min, w_max in tep_windows:
        mask |= ((wave >= w_min) & (wave <= w_max))
    return mask

def get_h0_residuals_and_flux(theta_opt, pm, data_blocks, z_abs_ref, c_kms):
    engine = RadiativeTransferEngine(z_abs=z_abs_ref)
    comps = pm.reconstruct(theta_opt)
    grouped_comps = {'H_I': [], 'D_I': [], 'C_IV': [], 'C_III': [], 'C_II': [], 'Si_IV': []}
    for c in comps:
        v = c_kms * (c['z'] - z_abs_ref) / (1.0 + z_abs_ref)
        cd = {'N': 10**c['logN'], 'b': c['b'], 'v': v}
        if c['ion'] == 'D_I':
            cd['v'] -= 81.6
        if c['ion'] in grouped_comps:
            grouped_comps[c['ion']].append(cd)
            
    residuals_all = []
    flux_mod_all = []
    flux_obs_all = []
    wave_all = []
    
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
            c_opt = np.zeros(3)
            flux_mod = np.zeros_like(flux_fit)
            res = np.ones_like(flux_fit) * 1000.0
            
        residuals_all.extend(res)
        flux_mod_all.extend(flux_mod)
        flux_obs_all.extend(flux_fit)
        wave_all.extend(wave_fit)
            
    return np.array(wave_all), np.array(flux_obs_all), np.array(flux_mod_all), np.array(residuals_all)

def get_file_hash(path):
    with open(path, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()

def run_replay():
    print("--- Phase D1: Authoritative Model 6a Replay Gate ---")
    manifest_path = project_root / 'data' / 'processed' / 'Q1009_union_manifest.json'
    vpfit_path = project_root / 'data' / 'literature_components' / 'model_6a.26'
    noise_model_path = project_root / 'configs' / 'tep_noise_model.json'
    
    with open(manifest_path, 'r') as f:
        manifest = json.load(f)
        
    with open(noise_model_path, 'r') as f:
        noise_cfg = json.load(f)
        
    z_abs_ref = manifest['z_abs']
    c_kms = 299792.458
    
    components_raw, regions = parse_vpfit_ties(vpfit_path)
    pm = ParameterManager(components_raw)
    
    tep_windows = define_regions()
    
    data_blocks = []
    all_waves = []
    
    for r in regions:
        coadd = r['filename']
        if coadd not in manifest['coadds']: continue
        w_min_vp = r['w_min']
        w_max_vp = r['w_max']
        
        chunk_wave, chunk_flux, chunk_err = [], [], []
        for chunk in manifest['coadds'][coadd]:
            chunk_wave.extend(chunk['wave'])
            chunk_flux.extend(chunk['flux'])
            chunk_err.extend(chunk['err'])
            
        wave = np.array(chunk_wave)
        flux = np.array(chunk_flux)
        err = np.array(chunk_err)
        
        mask = (np.isfinite(flux)) & (np.isfinite(err)) & (err > 0) & (wave >= w_min_vp) & (wave <= w_max_vp)
        if np.sum(mask) == 0: continue
            
        block = {
            'wave': wave[mask],
            'flux': flux[mask],
            'err': err[mask],
            'vsig': r['vsig'],
            'w_min': w_min_vp,
            'w_max': w_max_vp,
            'coadd': coadd
        }
        data_blocks.append(block)
        all_waves.extend(wave[mask])
                
    all_waves = np.array(all_waves)
    pixel_hash = hashlib.sha256(all_waves.tobytes()).hexdigest()
    
    print(f"Total Pixels: {len(all_waves)}")
    print(f"Pixel Hash: {pixel_hash}")
    
    # Calculate H0 using the initial published parameters from model_6a.26
    theta_base = np.array(pm.theta_init)
    wave_all, flux_obs_all, flux_mod_all, residuals = get_h0_residuals_and_flux(theta_base, pm, data_blocks, z_abs_ref, c_kms)
    
    # Exclude extreme outliers for likelihood eval (as in step 28c)
    valid_mask = np.abs(residuals) < 100.0
    valid_res = residuals[valid_mask]
    
    # Likelihood based on frozen student-t model
    ll_t = np.sum(student_t.logpdf(valid_res, noise_cfg['nu'], noise_cfg['location'], noise_cfg['scale']))
    
    print(f"Frozen H0 Log-Likelihood: {ll_t:.6f}")
    
    # Verify exactness
    freeze_path = project_root / 'configs' / 'tep_bbn_h0_h1_comparison_freeze.json'
    
    # Load previous freeze if it has a pixel hash to verify, otherwise this is the freeze run.
    is_freeze_creation = True
    if freeze_path.exists():
        with open(freeze_path, 'r') as f:
            prev_config = json.load(f)
        if 'pixel_hash' in prev_config:
            is_freeze_creation = False
            
    if not is_freeze_creation:
        print("Checking against previous frozen objective...")
        if prev_config['pixel_hash'] != pixel_hash:
            print(f"Pixel hash mismatch! Prev: {prev_config['pixel_hash']}, Current: {pixel_hash}")
            sys.exit(1)
        ll_diff = abs(prev_config['h0_ll_t'] - ll_t)
        if ll_diff > 1e-6:
            print(f"Log-Likelihood mismatch! Difference: {ll_diff}")
            sys.exit(1)
        print("PASS: Exact frozen-H0 reproduction achieved.")
    else:
        print("First time running. Saving frozen H0 replay configuration.")
        freeze_data = {
            "status": "FROZEN_BEFORE_H1_FITTING",
            "development_system": "Q1009+2956",
            "data_manifest": str(manifest_path),
            "data_hash": get_file_hash(manifest_path),
            "pixel_hash": pixel_hash,
            "baseline_source": "model_6a.26",
            "baseline_parser_version": get_file_hash(project_root / 'scripts' / 'steps' / 'deprecated_classical' / 'step_27c_refit_h0_model_6a.py'),
            "shared_engine": "physical_rt_engine",
            "noise_model": "configs/tep_noise_model.json",
            "continuum_treatment": "analytic_profiling",
            "zero_level_treatment": "analytic_profiling",
            "h0": "H0_D_CONVENTIONAL",
            "h1": "H1_HI_KINEMATIC",
            "h1_velocity_prior_source": "non-D absorber velocity span",
            "h1_prior_uses_isotope_offset": False,
            "shared_pixels": True,
            "shared_transitions": True,
            "shared_instrument_model": True,
            "shared_nuisance_freedom": True,
            "h0_ll_t": float(ll_t),
            "pixel_count": len(all_waves)
        }
        with open(freeze_path, 'w') as f:
            json.dump(freeze_data, f, indent=2)
            
        # Write freeze hash
        freeze_hash = get_file_hash(freeze_path)
        print(f"Freeze created with hash: {freeze_hash}")
            
    # Also save the reference flux for detailed flux-level checking
    ref_flux_path = project_root / 'data' / 'processed' / 'q1009_h0_reference_flux.npz'
    if ref_flux_path.exists():
        loaded = np.load(ref_flux_path)
        max_diff = np.max(np.abs(loaded['flux_mod'] - flux_mod_all))
        print(f"Maximum normalized flux difference: {max_diff:.3e}")
        if max_diff > 1e-8:
            print("Flux mismatch exceeds tolerance!")
            sys.exit(1)
    else:
        np.savez(ref_flux_path, wave=wave_all, flux_mod=flux_mod_all, residuals=residuals)

if __name__ == '__main__':
    run_replay()
