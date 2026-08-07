import json
import numpy as np
from pathlib import Path
import sys

script_dir = Path(__file__).parent
project_root = script_dir.parent.parent
sys.path.insert(0, str(project_root))

from scripts.lib.physical_rt_engine import RadiativeTransferEngine
def strip_letters(val_str):
    return float(''.join(c for c in val_str if c.isdigit() or c in '.-+'))

def parse_vpfit_full(filepath):
    components = []
    regions = []
    
    with open(filepath, 'r') as f:
        for line in f:
            if line.startswith('%%'):
                parts = line.split()
                filename = parts[1].split('/')[-1]
                idx = int(parts[2])
                w_min = float(parts[3])
                w_max = float(parts[4])
                
                vsig = 3.0
                for p in parts:
                    if p.startswith('vsig='):
                        vsig = float(p.split('=')[1])
                        
                regions.append({
                    'idx': idx,
                    'filename': filename,
                    'w_min': w_min,
                    'w_max': w_max,
                    'vsig': vsig
                })
            elif line.startswith(' H I') or line.startswith(' D I'):
                parts = line.split()
                if len(parts) < 7: continue
                
                ion = parts[0] + '_' + parts[1]
                z = float(strip_letters(parts[2]))
                b = float(strip_letters(parts[4]))
                logN = float(strip_letters(parts[6]))
                
                components.append({'ion': ion, 'z': z, 'b': b, 'logN': logN})
                
    return components, regions

def evaluate_model(model_name):
    manifest_path = project_root / 'data' / 'processed' / 'Q1009_union_manifest.json'
    vpfit_path = project_root / 'data' / 'literature_components' / f'{model_name}.26'
    
    with open(manifest_path, 'r') as f:
        manifest = json.load(f)
        
    components, regions = parse_vpfit_full(vpfit_path)
    z_abs_ref = manifest['z_abs']
    c_kms = 299792.458
    
    hi_comps = []
    di_comps = []
    for c in components:
        v = c_kms * (c['z'] - z_abs_ref) / (1.0 + z_abs_ref)
        comp_dict = {'N': 10**c['logN'], 'b': c['b'], 'v': v}
        if c['ion'] == 'H_I':
            hi_comps.append(comp_dict)
        elif c['ion'] == 'D_I':
            comp_dict['v'] = v - 81.6
            di_comps.append(comp_dict)
            
    engine = RadiativeTransferEngine(z_abs=z_abs_ref)
    transitions_hi = ['HI_Lya', 'HI_Lyb', 'HI_Lyg', 'HI_Ly6', 'HI_Ly13', 'HI_Ly14', 'HI_Ly21']
    
    total_chi2 = 0.0
    total_pixels = 0
    total_profiled = 0
    
    for i, r in enumerate(regions):
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
        flux_obs = np.array(all_flux)
        err = np.array(all_err)
        
        # Native validity mask: exclude negative errors, non-finite values
        mask = (np.isfinite(flux_obs)) & (np.isfinite(err)) & (err > 0) & (wave >= w_min_vp) & (wave <= w_max_vp)
        if np.sum(mask) == 0: continue
            
        wave_fit = wave[mask]
        flux_fit = flux_obs[mask]
        err_fit = err[mask]
        
        tau_hi = engine.compute_optical_depth(wave_fit, transitions_hi, hi_comps)
        tau_di = engine.compute_optical_depth(wave_fit, transitions_hi, di_comps)
        tau_tot = tau_hi + tau_di
        
        x_norm = 2.0 * (wave_fit - w_min_vp) / (w_max_vp - w_min_vp) - 1.0
        
        P = np.zeros((len(wave_fit), 3))
        P[:, 0] = np.exp(-tau_tot)
        P[:, 1] = x_norm * np.exp(-tau_tot)
        P[:, 2] = 1.0
        
        for k in range(3):
            P[:, k] = engine.apply_convolution(P[:, k], wave_fit, r['vsig'])
            
        W = 1.0 / err_fit**2
        H = P.T @ (W[:, np.newaxis] * P)
        b_vec = P.T @ (W * flux_fit)
        
        try:
            c_opt = np.linalg.solve(H, b_vec)
            flux_mod = P @ c_opt
            res = (flux_fit - flux_mod) / err_fit
            chi2 = np.sum(res**2)
            
            total_chi2 += chi2
            total_pixels += len(wave_fit)
            total_profiled += len(c_opt)
        except np.linalg.LinAlgError:
            pass

    return total_pixels, total_profiled, total_chi2

if __name__ == '__main__':
    for m in ['model_1a', 'model_3a', 'model_5a', 'model_6a']:
        try:
            pixels, profiled, chi2 = evaluate_model(m)
            # Rough free params assumption for baseline comparison
            free_params = 111 if m == 'model_1a' else 150 
            dof = pixels - profiled - free_params
            rchi2 = chi2 / dof if dof > 0 else 0
            print(f"{m:10s} | Pixels: {pixels:5d} | chi2: {chi2:8.1f} | dof: {dof:4d} | red_chi2: {rchi2:.3f}")
        except Exception as e:
            print(f"{m:10s} | FAILED: {e}")
