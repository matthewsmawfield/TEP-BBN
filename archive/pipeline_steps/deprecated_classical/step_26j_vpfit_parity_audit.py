import json
import numpy as np
from pathlib import Path
import sys
from scipy.stats import skew

script_dir = Path(__file__).parent
project_root = script_dir.parent.parent
sys.path.insert(0, str(project_root))

from scripts.lib.physical_rt_engine import RadiativeTransferEngine
from step_26c_load_vpfit_model import strip_letters
from step_26i_exact_vpfit_validator import parse_vpfit_full

def compute_autocorr(res):
    if len(res) < 2: return 0.0
    var = np.var(res)
    if var == 0: return 0.0
    return np.correlate(res - np.mean(res), res - np.mean(res), mode='full')[len(res)] / (var * len(res))

def count_free_parameters(filepath):
    # Very simple approximation of free Voigt parameters
    # A rigorous parse would trace all SA, SB, etc ties.
    z_ties = set()
    b_ties = set()
    N_ties = set()
    z_free = 0
    b_free = 0
    N_free = 0
    
    with open(filepath, 'r') as f:
        for line in f:
            if line.startswith(' H I') or line.startswith(' D I'):
                parts = line.split()
                if len(parts) < 7: continue
                
                z_raw = parts[2]
                b_raw = parts[4]
                N_raw = parts[6]
                
                if any(c.isalpha() for c in z_raw):
                    tie = ''.join([c for c in z_raw if c.isalpha()])
                    if tie not in z_ties: z_ties.add(tie)
                else: z_free += 1
                
                if any(c.isalpha() for c in b_raw):
                    tie = ''.join([c for c in b_raw if c.isalpha()])
                    if tie not in b_ties: b_ties.add(tie)
                else: b_free += 1
                
                if any(c.isalpha() for c in N_raw):
                    tie = ''.join([c for c in N_raw if c.isalpha()])
                    if tie not in N_ties: N_ties.add(tie)
                else: N_free += 1

    total_voigt = len(z_ties) + z_free + len(b_ties) + b_free + len(N_ties) + N_free
    return total_voigt

def perform_parity_audit():
    manifest_path = project_root / 'data' / 'processed' / 'Q1009_union_manifest.json'
    vpfit_path = project_root / 'data' / 'literature_components' / 'model_1a.26'
    
    voigt_free_params = count_free_parameters(vpfit_path)
    
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
    
    stats_rows = []
    
    for i, r in enumerate(regions):
        rid = i + 1
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
        
        mask = (err > 0) & (wave >= w_min_vp) & (wave <= w_max_vp)
        if np.sum(mask) == 0: continue
            
        wave_fit = wave[mask]
        flux_fit = flux_obs[mask]
        err_fit = err[mask]
        
        tau_hi = engine.compute_optical_depth(wave_fit, transitions_hi, hi_comps)
        tau_di = engine.compute_optical_depth(wave_fit, transitions_hi, di_comps)
        tau_tot = tau_hi + tau_di
        
        x_norm = 2.0 * (wave_fit - w_min_vp) / (w_max_vp - w_min_vp) - 1.0
        
        # Profile 3 parameters: c0, c1 (continuum) and Z (zero level)
        # F = (c0 + c1*x) * exp(-tau) + Z
        P = np.zeros((len(wave_fit), 3))
        P[:, 0] = np.exp(-tau_tot)
        P[:, 1] = x_norm * np.exp(-tau_tot)
        P[:, 2] = 1.0  # Zero level additive constant
        
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
            total_profiled += len(c_opt) # 3 params
            
            mean_r = np.mean(res)
            std_r = np.std(res)
            skew_r = skew(res)
            pct_3s = 100.0 * np.sum(np.abs(res) > 3) / len(res)
            pct_5s = 100.0 * np.sum(np.abs(res) > 5) / len(res)
            autocorr = compute_autocorr(res)
            
            stats_rows.append({
                'rid': rid,
                'coadd': coadd,
                'pixels': len(wave_fit),
                'mean': mean_r,
                'std': std_r,
                'skew': skew_r,
                'pct_3s': pct_3s,
                'pct_5s': pct_5s,
                'autocorr': autocorr,
                'chi2': chi2
            })
            
        except np.linalg.LinAlgError:
            print(f"Failed linear solve for region {rid}")

    # Output Report
    out_md = project_root / 'data' / 'processed' / 'stage3c_vpfit_parity_audit.md'
    with open(out_md, 'w') as f:
        f.write("# VPFIT Parity Audit & Residual Statistics\n\n")
        f.write(f"**Total Valid Pixels:** {total_pixels}\n")
        f.write(f"**Voigt Free Parameters:** {voigt_free_params} (approx tied)\n")
        f.write(f"**Profiled Parameters (Cont+Zero):** {total_profiled}\n")
        dof = total_pixels - (voigt_free_params + total_profiled)
        f.write(f"**Degrees of Freedom ($\\nu$):** {dof}\n")
        f.write(f"**Total $\\chi^2$:** {total_chi2:.1f}\n")
        f.write(f"**Global Reduced $\\chi^2_\\nu$:** {total_chi2 / dof:.3f}\n\n")
        
        f.write("## Normalized Residual Statistics by Region\n\n")
        f.write("| ID | Coadd | Pixels | Mean | StdDev | Skew | >3σ (%) | >5σ (%) | AutoCorr | $\\chi^2$ |\n")
        f.write("|---|---|---|---|---|---|---|---|---|---|\n")
        
        for sr in stats_rows:
            f.write(f"| {sr['rid']} | {sr['coadd'][:10]}... | {sr['pixels']} | {sr['mean']:.2f} | {sr['std']:.2f} | {sr['skew']:.2f} | {sr['pct_3s']:.1f} | {sr['pct_5s']:.1f} | {sr['autocorr']:.2f} | {sr['chi2']:.1f} |\n")

    print(f"Audit completed. Reduced chi2: {total_chi2 / dof:.3f}")
    print(f"Results saved to {out_md}")

if __name__ == '__main__':
    perform_parity_audit()
