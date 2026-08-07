import sys
from pathlib import Path
import numpy as np
from scipy.stats import t as student_t

script_dir = Path(__file__).parent
project_root = script_dir.parent.parent
sys.path.insert(0, str(project_root))

from scripts.steps.step_27c_refit_h0_model_6a import parse_vpfit_ties, ParameterManager, refit_model
import json
from scripts.lib.physical_rt_engine import RadiativeTransferEngine

def estimate_noise_model(model_name):
    manifest_path = project_root / 'data' / 'processed' / 'Q1009_union_manifest.json'
    vpfit_path = project_root / 'data' / 'literature_components' / f'{model_name}.26'
    
    with open(manifest_path, 'r') as f:
        manifest = json.load(f)
        
    z_abs_ref = manifest['z_abs']
    c_kms = 299792.458
    engine = RadiativeTransferEngine(z_abs=z_abs_ref)
    
    components_raw, regions = parse_vpfit_ties(vpfit_path)
    pm = ParameterManager(components_raw)
    
    data_blocks = []
    for r in regions:
        coadd = r['filename']
        if coadd not in manifest['coadds']: continue
        w_min_vp = r['w_min']
        w_max_vp = r['w_max']
        
        all_wave, all_flux, all_err = [], [], []
        for chunk in manifest['coadds'][coadd]:
            all_wave.extend(chunk['wave'])
            all_flux.extend(chunk['flux'])
            all_err.extend(chunk['err'])
            
        wave = np.array(all_wave)
        flux = np.array(all_flux)
        err = np.array(all_err)
        
        mask = (np.isfinite(flux)) & (np.isfinite(err)) & (err > 0) & (wave >= w_min_vp) & (wave <= w_max_vp)
        if np.sum(mask) == 0: continue
            
        data_blocks.append({
            'wave': wave[mask],
            'flux': flux[mask],
            'err': err[mask],
            'vsig': r['vsig'],
            'w_min': w_min_vp,
            'w_max': w_max_vp
        })
        
    def residual_fn(theta):
        comps = pm.reconstruct(theta)
        grouped_comps = {'H_I': [], 'D_I': [], 'C_IV': [], 'C_III': [], 'C_II': [], 'Si_IV': []}
        for c in comps:
            v = c_kms * (c['z'] - z_abs_ref) / (1.0 + z_abs_ref)
            cd = {'N': 10**c['logN'], 'b': c['b'], 'v': v}
            if c['ion'] == 'D_I':
                cd['v'] -= 81.6
            if c['ion'] in grouped_comps:
                grouped_comps[c['ion']].append(cd)
                
        residuals = []
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
                residuals.extend(res)
            except np.linalg.LinAlgError:
                residuals.extend(np.ones_like(flux_fit) * 1000.0) 
        return np.array(residuals)

    theta_0 = np.array(pm.theta_init)
    res_0 = residual_fn(theta_0)
    
    # Filter out wild failure residuals if any
    valid_res = res_0[np.abs(res_0) < 100.0]
    
    # Fit Student-t distribution
    # df, loc, scale
    df, loc, scale = student_t.fit(valid_res)
    
    print(f"Student-t fit for {model_name} initial residuals:")
    print(f"Degrees of freedom (nu): {df:.3f}")
    print(f"Location (mu): {loc:.3f}")
    print(f"Scale (sigma multiplier): {scale:.3f}")
    
    # Write to a config file
    config_path = project_root / 'configs' / 'tep_noise_model.json'
    with open(config_path, 'w') as f:
        json.dump({
            'source': 'model_6a_initial_residuals',
            'nu': df,
            'scale': scale,
            'loc': loc
        }, f, indent=4)
        
    print(f"Saved frozen noise model to {config_path}")

if __name__ == '__main__':
    estimate_noise_model('model_6a')
