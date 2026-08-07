import json
import numpy as np
from pathlib import Path
import sys
from scipy.optimize import least_squares

script_dir = Path(__file__).parent
project_root = script_dir.parent.parent
sys.path.insert(0, str(project_root))

from scripts.lib.physical_rt_engine import RadiativeTransferEngine

def strip_letters(val_str):
    return float(''.join(c for c in val_str if c.isdigit() or c in '.-+'))

# VPFIT tie parser
def parse_vpfit_ties(filepath):
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
            elif line.startswith(' ') and len(line) > 50 and line[1:2].isalpha():
                # Component line
                parts = line.split()
                if len(parts) < 6: continue
                
                # Determine ion and shifts
                if parts[1][0].isalpha():
                    ion = parts[0] + '_' + parts[1]
                    z_str = parts[2]
                    b_str = parts[4]
                    N_str = parts[6]
                else:
                    # Ion is just parts[0]
                    # Insert underscore between element and roman numeral
                    ion_base = parts[0]
                    # Simple heuristic: split at first capital I or V
                    for i, c in enumerate(ion_base):
                        if c in 'IV' and i > 0:
                            ion = ion_base[:i] + '_' + ion_base[i:]
                            break
                    else:
                        ion = ion_base
                        
                    z_str = parts[1]
                    b_str = parts[3]
                    N_str = parts[5]
                
                z_val = strip_letters(z_str)
                b_val = strip_letters(b_str)
                N_val = strip_letters(N_str)
                
                z_tie = ''.join(c for c in z_str if c.isalpha() or c in '%')
                b_tie = ''.join(c for c in b_str if c.isalpha() or c in '%')
                N_tie = ''.join(c for c in N_str if c.isalpha() or c in '%')
                
                # Check for thermal block
                b_turb, T = None, None
                if '[' in line:
                    idx = line.index('[')
                    block = line[idx+1:].split()
                    if len(block) >= 4:
                        b_turb = float(block[0])
                        T = float(block[2])
                        
                components.append({
                    'ion': ion,
                    'z': z_val, 'z_tie': z_tie,
                    'b': b_val, 'b_tie': b_tie,
                    'logN': N_val, 'N_tie': N_tie,
                    'b_turb': b_turb, 'T': T
                })
                
    return components, regions

# Define masses for thermal scaling (amu)
MASSES = {
    'H_I': 1.00784,
    'D_I': 2.01410,
    'C_II': 12.011,
    'C_III': 12.011,
    'C_IV': 12.011,
    'Si_II': 28.085,
    'Si_III': 28.085,
    'Si_IV': 28.085,
    'O_VI': 15.999
}

class ParameterManager:
    def __init__(self, components):
        self.components = components
        self.theta_names = []
        self.theta_init = []
        self.bounds_lower = []
        self.bounds_upper = []
        self.comp_map = [] # stores how to reconstruct each component from theta
        
        # Maps for ties
        self.z_map = {}
        self.b_therm_map = {}
        self.N_map = {}
        self.N_offsets = {} # For D/H % ties
        
        def add_param(name, val, lb, ub):
            idx = len(self.theta_names)
            self.theta_names.append(name)
            self.theta_init.append(val)
            self.bounds_lower.append(lb)
            self.bounds_upper.append(ub)
            return idx
            
        for i, c in enumerate(components):
            cmap = {}
            # Z
            if c['z_tie']:
                if c['z_tie'] not in self.z_map:
                    self.z_map[c['z_tie']] = add_param(f"z_{c['z_tie']}", c['z'], c['z']-0.01, c['z']+0.01)
                cmap['z_idx'] = self.z_map[c['z_tie']]
            else:
                cmap['z_idx'] = add_param(f"z_free_{i}", c['z'], c['z']-0.01, c['z']+0.01)
                
            # logN
            if c['N_tie']:
                if c['N_tie'] == '%':
                    cmap['N_idx'] = -1
                    cmap['N_val'] = c['logN'] 
                else:
                    if c['N_tie'] not in self.N_map:
                        self.N_map[c['N_tie']] = add_param(f"logN_{c['N_tie']}", c['logN'], 10.0, 22.0)
                    cmap['N_idx'] = self.N_map[c['N_tie']]
            else:
                cmap['N_idx'] = add_param(f"logN_free_{i}", c['logN'], 10.0, 22.0)
                
            # B
            if c['b_tie']:
                tie_key = c['b_tie'].lower()
                if tie_key not in self.b_therm_map:
                    if c['b_turb'] is not None and c['T'] is not None:
                        idx_turb = add_param(f"bturb_{tie_key}", c['b_turb'], 0.0, 200.0)
                        idx_T = add_param(f"T_{tie_key}", c['T'], 1e2, 1e7)
                        self.b_therm_map[tie_key] = (idx_turb, idx_T)
                    else:
                        idx_b = add_param(f"b_{tie_key}", c['b'], 0.5, 300.0)
                        self.b_therm_map[tie_key] = idx_b
                        
                val = self.b_therm_map[tie_key]
                if isinstance(val, tuple):
                    cmap['b_turb_idx'] = val[0]
                    cmap['T_idx'] = val[1]
                else:
                    cmap['b_idx'] = val
            else:
                cmap['b_idx'] = add_param(f"b_free_{i}", c['b'], 0.5, 300.0)
                
            self.comp_map.append(cmap)
            
        # Post-process D/H % ties
        for i, c in enumerate(components):
            if c['N_tie'] == '%':
                h_idx = -1
                for j, hc in enumerate(components):
                    if hc['ion'] == 'H_I' and hc['z_tie'] == c['z_tie']:
                        h_idx = j
                        break
                if h_idx != -1:
                    offset = c['logN'] - components[h_idx]['logN']
                    self.comp_map[i]['N_parent_idx'] = self.comp_map[h_idx]['N_idx']
                    self.comp_map[i]['N_offset'] = offset
                else:
                    self.comp_map[i]['N_fixed'] = c['logN']

    def reconstruct(self, theta):
        res = []
        for i, c in enumerate(self.components):
            cmap = self.comp_map[i]
            z = theta[cmap['z_idx']]
            
            if 'N_idx' in cmap and cmap['N_idx'] != -1:
                logN = theta[cmap['N_idx']]
            elif 'N_parent_idx' in cmap:
                logN = theta[cmap['N_parent_idx']] + cmap['N_offset']
            else:
                logN = cmap.get('N_fixed', c['logN'])
                
            if 'b_idx' in cmap:
                b = theta[cmap['b_idx']]
            else:
                b_turb = theta[cmap['b_turb_idx']]
                T = theta[cmap['T_idx']]
                mass = MASSES.get(c['ion'], 1.0)
                # b_therm^2 = 2 k_B T / m.  For T in 10^4 K, m in amu, b_therm = 12.85 * sqrt(T4 / m)
                b_therm = 12.85 * np.sqrt((T / 1e4) / mass)
                b = np.sqrt(b_turb**2 + b_therm**2)
                
            res.append({'ion': c['ion'], 'z': z, 'logN': logN, 'b': b})
        return res

def refit_model(model_name):
    manifest_path = project_root / 'data' / 'processed' / 'Q1009_union_manifest.json'
    vpfit_path = project_root / 'data' / 'literature_components' / f'{model_name}.26'
    
    with open(manifest_path, 'r') as f:
        manifest = json.load(f)
        
    z_abs_ref = manifest['z_abs']
    c_kms = 299792.458
    engine = RadiativeTransferEngine(z_abs=z_abs_ref)
    
    components_raw, regions = parse_vpfit_ties(vpfit_path)
    pm = ParameterManager(components_raw)
    
    # We need to compile the list of transitions present in the model
    # Wait, the RT engine needs to be called per-region with all relevant transitions.
    # To keep it simple, we use a fixed set of all transitions that might be in Q1009.
    all_transitions = [
        'HI_Lya', 'HI_Lyb', 'HI_Lyg', 'HI_Ly6', 'HI_Ly13', 'HI_Ly14', 'HI_Ly21',
        'CIV_1548', 'CIV_1550', 'CIII_977', 'CII_1334'
    ]
    
    # Pre-extract data chunks
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
        
        # Group components by ion so engine can process them efficiently
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
            
            # Compute total tau
            tau_tot = np.zeros_like(wave_fit)
            # Add HI
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
                residuals.extend(np.ones_like(flux_fit) * 1000.0) # Penalty
                
        return np.array(residuals)
        
    print(f"Starting {model_name} refit. Free params: {len(pm.theta_init)}, Data points: {sum(len(b['wave']) for b in data_blocks)}")
    
    theta_0 = np.array(pm.theta_init)
    res_0 = residual_fn(theta_0)
    chi2_0 = np.sum(res_0**2)
    print(f"Initial Chi2: {chi2_0:.1f}")
    
    # We optimize!
    bounds = (pm.bounds_lower, pm.bounds_upper)
    res_opt = least_squares(residual_fn, theta_0, bounds=bounds, method='trf', loss='linear', max_nfev=50, x_scale='jac')
    
    chi2_final = np.sum(res_opt.fun**2)
    dof = len(res_opt.fun) - len(theta_0) - len(data_blocks)*3
    print(f"Final Chi2: {chi2_final:.1f} | Reduced Chi2: {chi2_final/dof:.3f}")

if __name__ == '__main__':
    refit_model('model_6a')
