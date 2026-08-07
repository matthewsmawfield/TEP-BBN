import json
import numpy as np
from pathlib import Path
import sys

script_dir = Path(__file__).parent
project_root = script_dir.parent.parent
sys.path.insert(0, str(project_root))

from scripts.lib.physical_rt_engine import RadiativeTransferEngine
from step_26c_load_vpfit_model import parse_vpfit

def get_region_name(w_min, w_max):
    w_center = 0.5 * (w_min + w_max)
    t_windows = {
        'Ly_alpha': (4250, 4270),
        'Ly_beta': (3590, 3600),
        'Ly_gamma': (3403, 3412),
        'Ly_6': (3258, 3265),
        'Ly_13': (3209, 3213),
        'Ly_14': (3207, 3211),
        'Ly_21': (3199, 3202)
    }
    for name, bounds in t_windows.items():
        if bounds[0] - 2 < w_center < bounds[1] + 2:
            return name
    return f"Unknown_{w_center:.0f}"

def decompose_chi2():
    manifest_path = project_root / 'data' / 'processed' / 'Q1009_union_manifest.json'
    vpfit_path = project_root / 'data' / 'literature_components' / 'model_1a.26'
    
    with open(manifest_path, 'r') as f:
        manifest = json.load(f)
        
    components = parse_vpfit(vpfit_path)
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
    
    results = []
    
    for coadd, chunks in manifest['coadds'].items():
        for i, chunk in enumerate(chunks):
            wave = np.array(chunk['wave'])
            flux_obs = np.array(chunk['flux'])
            err = np.array(chunk['err'])
            mask = err > 0
            if np.sum(mask) == 0:
                continue
                
            w_min, w_max = wave[0], wave[-1]
            region = get_region_name(w_min, w_max)
            
            x_norm = 2.0 * (wave - w_min) / (w_max - w_min) - 1.0 if w_min != w_max else np.zeros_like(wave)
                
            cont_degree = 2
            P = np.zeros((len(wave), cont_degree + 1))
            for k in range(cont_degree + 1):
                coef = np.zeros(cont_degree + 1)
                coef[k] = 1.0
                P[:, k] = np.polynomial.chebyshev.chebval(x_norm, coef)
                
            tau_hi = engine.compute_optical_depth(wave, transitions_hi, hi_comps)
            tau_di = engine.compute_optical_depth(wave, transitions_hi, di_comps)
            tau_tot = tau_hi + tau_di
            
            X = P * np.exp(-tau_tot)[:, np.newaxis]
            for k in range(X.shape[1]):
                X[:, k] = engine.apply_convolution(X[:, k], wave, 3.0)
                
            W = 1.0 / err**2
            X_mask = X[mask]
            y_mask = flux_obs[mask]
            W_mask = W[mask]
            
            try:
                H = X_mask.T @ (W_mask[:, np.newaxis] * X_mask)
                b_vec = X_mask.T @ (W_mask * y_mask)
                c_opt = np.linalg.solve(H, b_vec)
                flux_mod = X_mask @ c_opt
                
                residuals = (y_mask - flux_mod) / err[mask]
                chi2 = np.sum(residuals**2)
                dof = np.sum(mask) - len(c_opt) # approximation
                red_chi2 = chi2 / dof if dof > 0 else 0
                rms = np.sqrt(np.mean(residuals**2))
                max_res = np.max(np.abs(residuals))
                
                results.append({
                    'coadd': coadd,
                    'region': region,
                    'pixels': np.sum(mask),
                    'chi2': chi2,
                    'red_chi2': red_chi2,
                    'rms': rms,
                    'max_res': max_res
                })
            except Exception as e:
                print(f"Failed chunk {coadd} {region}: {e}")
                
    # Sort by chi2 contribution (descending)
    results.sort(key=lambda x: x['chi2'], reverse=True)
    
    print("| Coadd | Region | Pixels | $\\chi^2$ | Reduced $\\chi^2$ | RMS residual | Max residual |")
    print("|-------|--------|-------:|---------:|-----------------:|-------------:|-------------:|")
    for r in results:
        print(f"| {r['coadd']:10s} | {r['region']:8s} | {r['pixels']:6d} | {r['chi2']:8.1f} | {r['red_chi2']:16.2f} | {r['rms']:12.2f} | {r['max_res']:12.2f} |")
        
    total_chi2 = sum(r['chi2'] for r in results)
    total_pixels = sum(r['pixels'] for r in results)
    print(f"\nTotal Chi2: {total_chi2:.1f} / {total_pixels} pixels (Reduced: {total_chi2/total_pixels:.2f})")

if __name__ == '__main__':
    decompose_chi2()
