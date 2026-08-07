import re
import json
import numpy as np
from pathlib import Path
import sys

script_dir = Path(__file__).parent
project_root = script_dir.parent.parent
sys.path.insert(0, str(project_root))

from scripts.lib.physical_rt_engine import RadiativeTransferEngine
from step_26c_load_vpfit_model import strip_letters

def parse_vpfit_full(filepath):
    components = []
    regions = []
    
    with open(filepath, 'r') as f:
        for line in f:
            if line.startswith('%%'):
                # %% ../../data/q1011p2941_C1x1.dat     1   4254.4200   4265.0000 vsig=2.6  !  2017/03/06
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

def validate_exact_vpfit():
    manifest_path = project_root / 'data' / 'processed' / 'Q1009_union_manifest.json'
    vpfit_path = project_root / 'data' / 'literature_components' / 'model_1a.26'
    
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
    
    print("| Region ID | Coadd | Range | vsig | Pixels | $\\chi^2$ | Reduced $\\chi^2$ |")
    print("|-----------|-------|-------|------|-------:|---------:|-----------------:|")
    
    for i, r in enumerate(regions):
        rid = i + 1
        coadd = r['filename']
        # Find corresponding chunk in manifest
        if coadd not in manifest['coadds']:
            continue
            
        w_min_vp = r['w_min']
        w_max_vp = r['w_max']
        
        # Merge all chunks from manifest that overlap this region
        all_wave = []
        all_flux = []
        all_err = []
        for chunk in manifest['coadds'][coadd]:
            all_wave.extend(chunk['wave'])
            all_flux.extend(chunk['flux'])
            all_err.extend(chunk['err'])
            
        wave = np.array(all_wave)
        flux_obs = np.array(all_flux)
        err = np.array(all_err)
        
        # Exact masking to VPFIT bounds
        mask = (err > 0) & (wave >= w_min_vp) & (wave <= w_max_vp)
        
        if np.sum(mask) == 0:
            continue
            
        # We evaluate tau over the exact masked wave
        wave_fit = wave[mask]
        flux_fit = flux_obs[mask]
        err_fit = err[mask]
        
        tau_hi = engine.compute_optical_depth(wave_fit, transitions_hi, hi_comps)
        tau_di = engine.compute_optical_depth(wave_fit, transitions_hi, di_comps)
        tau_tot = tau_hi + tau_di
        
        x_norm = 2.0 * (wave_fit - w_min_vp) / (w_max_vp - w_min_vp) - 1.0
        
        # Degree 1 continuum (Linear)
        P = np.zeros((len(wave_fit), 2))
        P[:, 0] = 1.0
        P[:, 1] = x_norm
        
        # Compute convolution BEFORE the exact mask? 
        # VPFIT convolves the entire theoretical spectrum, then compares to pixels.
        # But for analytic solving, we'll convolve the basis matrix over the valid pixels.
        # To avoid edge effects, we should create a slightly padded grid, but for a 3 km/s kernel, it's tiny.
        
        X = P * np.exp(-tau_tot)[:, np.newaxis]
        for k in range(X.shape[1]):
            X[:, k] = engine.apply_convolution(X[:, k], wave_fit, r['vsig'])
            
        W = 1.0 / err_fit**2
        
        H = X.T @ (W[:, np.newaxis] * X)
        b_vec = X.T @ (W * flux_fit)
        
        try:
            c_opt = np.linalg.solve(H, b_vec)
            flux_mod = X @ c_opt
            chi2 = np.sum(W * (flux_fit - flux_mod)**2)
            dof = len(wave_fit) - len(c_opt)
            red_chi2 = chi2 / dof if dof > 0 else 0
            
            print(f"| {rid:2d} | {coadd:15s} | {w_min_vp:.1f}-{w_max_vp:.1f} | {r['vsig']:.1f} | {len(wave_fit):6d} | {chi2:8.1f} | {red_chi2:16.2f} |")
            
            total_chi2 += chi2
            total_pixels += len(wave_fit)
        except np.linalg.LinAlgError:
            print(f"| {rid:2d} | {coadd:15s} | Failed linear solve")

    print(f"\nExact VPFIT Region Validation:")
    print(f"Total Chi2: {total_chi2:.1f} / {total_pixels} pixels (Reduced: {total_chi2/total_pixels:.2f})")

if __name__ == '__main__':
    validate_exact_vpfit()
