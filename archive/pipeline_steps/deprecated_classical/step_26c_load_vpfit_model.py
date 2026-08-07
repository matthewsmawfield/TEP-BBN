import re
import json
import numpy as np
from pathlib import Path
import sys
import matplotlib.pyplot as plt

script_dir = Path(__file__).parent
project_root = script_dir.parent.parent
sys.path.insert(0, str(project_root))

from scripts.lib.physical_rt_engine import RadiativeTransferEngine

def strip_letters(s):
    # Remove any letters from the end of the string like "19.74814aa" -> "19.74814"
    return re.sub(r'[a-zA-Z]+', '', s)

def parse_vpfit(filepath):
    components = []
    with open(filepath, 'r') as f:
        for line in f:
            if line.startswith(' H I') or line.startswith(' D I'):
                parts = line.split()
                ion = parts[0] + '_' + parts[1] # H_I or D_I
                z_str = strip_letters(parts[2])
                b_str = strip_letters(parts[4])
                logN_str = strip_letters(parts[6])
                
                try:
                    z = float(z_str)
                    b = float(b_str)
                    logN = float(logN_str)
                    
                    components.append({
                        'ion': ion,
                        'z': z,
                        'b': b,
                        'logN': logN
                    })
                except Exception as e:
                    print(f"Failed to parse line: {line.strip()} | Error: {e}")
    return components

def plot_conventional_reproduction(manifest_path, vpfit_path, out_dir):
    with open(manifest_path, 'r') as f:
        manifest = json.load(f)
        
    components = parse_vpfit(vpfit_path)
    
    # Separate into HI and DI components but convert them to relative velocity
    # relative to the primary z_abs of the manifest
    z_abs_ref = manifest['z_abs'] # 2.5042
    
    c_kms = 299792.458
    
    hi_comps = []
    di_comps = []
    for c in components:
        # v = c * (z - z_ref) / (1 + z_ref)
        v = c_kms * (c['z'] - z_abs_ref) / (1.0 + z_abs_ref)
        
        comp_dict = {
            'N': 10**c['logN'],
            'b': c['b'],
            'v': v
        }
        if c['ion'] == 'H_I':
            hi_comps.append(comp_dict)
        elif c['ion'] == 'D_I':
            # For DI, the RadiativeTransferEngine will evaluate HI lines.
            # But DI lines are intrinsically shifted by -81.6 km/s relative to HI.
            # So if we use HI atomic data to evaluate DI, we must shift the velocity by -81.6 km/s.
            comp_dict['v'] = v - 81.6
            di_comps.append(comp_dict)

    engine = RadiativeTransferEngine(z_abs=z_abs_ref)
    
    transitions_hi = ['HI_Lya', 'HI_Lyb', 'HI_Lyg', 'HI_Ly6', 'HI_Ly13', 'HI_Ly14', 'HI_Ly21']
    
    # We will compute the optical depth and solve for the optimal continuum for each chunk
    # just like the ProfiledFitter, but without optimization (evaluating at fixed params).
    
    total_chi2 = 0
    total_pixels = 0
    
    # Plotting setup
    fig, axes = plt.subplots(7, 1, figsize=(10, 20), sharey=False)
    # We'll plot chunks in their respective approximate transition windows
    t_windows = {
        'Lya': (4250, 4270),
        'Lyb': (3590, 3600),
        'Lyg': (3403, 3412),
        'Ly6': (3258, 3265),
        'Ly13': (3209, 3213),
        'Ly14': (3207, 3211),
        'Ly21': (3199, 3202)
    }
    
    ax_map = list(t_windows.keys())
    
    for coadd, chunks in manifest['coadds'].items():
        for chunk in chunks:
            wave = np.array(chunk['wave'])
            flux_obs = np.array(chunk['flux'])
            err = np.array(chunk['err'])
            mask = err > 0
            if np.sum(mask) == 0:
                continue
                
            w_min, w_max = wave[0], wave[-1]
            if w_min == w_max:
                x_norm = np.zeros_like(wave)
            else:
                x_norm = 2.0 * (wave - w_min) / (w_max - w_min) - 1.0
                
            cont_degree = 2
            P = np.zeros((len(wave), cont_degree + 1))
            for k in range(cont_degree + 1):
                coef = np.zeros(cont_degree + 1)
                coef[k] = 1.0
                P[:, k] = np.polynomial.chebyshev.chebval(x_norm, coef)
                
            tau_hi = engine.compute_optical_depth(wave, transitions_hi, hi_comps)
            tau_di = engine.compute_optical_depth(wave, transitions_hi, di_comps)
            tau_tot = tau_hi + tau_di
            
            exp_tau = np.exp(-tau_tot)
            X = P * exp_tau[:, np.newaxis]
            for k in range(X.shape[1]):
                X[:, k] = engine.apply_convolution(X[:, k], wave, 3.0)
                
            W = 1.0 / err**2
            X_mask = X[mask]
            y_mask = flux_obs[mask]
            W_mask = W[mask]
            
            X_T_W = X_mask.T * W_mask
            H = X_T_W @ X_mask
            b_vec = X_T_W @ y_mask
            
            try:
                c_opt = np.linalg.solve(H, b_vec)
                flux_mod = X_mask @ c_opt
                # for plotting, we need the model everywhere
                flux_mod_full = X @ c_opt
                cont_mod_full = P @ c_opt
            except:
                continue
                
            chi2_chunk = np.sum(W_mask * (y_mask - flux_mod)**2)
            total_chi2 += chi2_chunk
            total_pixels += np.sum(mask)
            
            # Find which axis to plot in
            w_center = 0.5 * (w_min + w_max)
            ax_idx = None
            for i, name in enumerate(ax_map):
                if t_windows[name][0] - 2 < w_center < t_windows[name][1] + 2:
                    ax_idx = i
                    break
                    
            if ax_idx is not None:
                ax = axes[ax_idx]
                ax.step(wave, flux_obs, color='black', alpha=0.5, where='mid')
                ax.plot(wave, flux_mod_full, color='red', alpha=0.8)
                ax.plot(wave, cont_mod_full, color='blue', linestyle='--', alpha=0.5)
                ax.set_title(ax_map[ax_idx])

    print(f"Conventional Model Validation:")
    print(f"Parsed {len(hi_comps)} HI and {len(di_comps)} DI components.")
    print(f"Total Chi2: {total_chi2:.2f} / {total_pixels} pixels (Reduced Chi2: {total_chi2/total_pixels:.2f})")
    
    plt.tight_layout()
    plot_path = out_dir / 'conventional_reproduction.png'
    plt.savefig(plot_path, dpi=150)
    print(f"Plot saved to {plot_path}")
    
    # Save parsed model for future use
    with open(out_dir / 'parsed_conventional_model.json', 'w') as f:
        json.dump({'hi_comps': hi_comps, 'di_comps': di_comps}, f, indent=2)

if __name__ == '__main__':
    manifest = project_root / 'data' / 'processed' / 'Q1009_union_manifest.json'
    vpfit = project_root / 'data' / 'literature_components' / 'model_1a.26'
    out_dir = project_root / 'data' / 'processed'
    plot_conventional_reproduction(manifest, vpfit, out_dir)
