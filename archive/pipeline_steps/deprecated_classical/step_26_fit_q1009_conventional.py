import json
import numpy as np
from pathlib import Path
from scipy.optimize import minimize
import sys

script_dir = Path(__file__).parent
project_root = script_dir.parent.parent
sys.path.insert(0, str(project_root))

from scripts.lib.physical_rt_engine import RadiativeTransferEngine

class ConventionalFitter:
    def __init__(self, manifest_path):
        with open(manifest_path, 'r') as f:
            self.manifest = json.load(f)
            
        self.z_abs = self.manifest['z_abs']
        self.engine = RadiativeTransferEngine(z_abs=self.z_abs)
        
        # Load data chunks
        self.chunks = []
        for coadd, chunks in self.manifest['coadds'].items():
            for c in chunks:
                self.chunks.append({
                    'coadd': coadd,
                    'wave': np.array(c['wave']),
                    'flux': np.array(c['flux']),
                    'err': np.array(c['err'])
                })
                
        # Metal velocities from feature vector
        self.v_metals = [0.0, 10.863, 14.713]
        
    def pack_params(self, p_dict):
        # Flatten parameters for scipy
        arr = []
        
        # H I components (A, B, C)
        for i in range(3):
            arr.append(p_dict['HI_logN'][i])
            arr.append(p_dict['HI_b'][i])
            arr.append(p_dict['HI_v'][i])
            
        # D I for component A
        arr.append(p_dict['DI_logN'])
        
        # Continuums (c0, c1 for each chunk)
        for c in p_dict['cont']:
            arr.append(c[0])
            arr.append(c[1])
            
        return np.array(arr)
        
    def unpack_params(self, arr):
        p = {
            'HI_logN': arr[0:9:3],
            'HI_b': arr[1:9:3],
            'HI_v': arr[2:9:3],
            'DI_logN': arr[9],
            'cont': []
        }
        idx = 10
        for _ in range(len(self.chunks)):
            p['cont'].append([arr[idx], arr[idx+1]])
            idx += 2
        return p
        
    def get_components(self, p_dict):
        comps = []
        for i in range(3):
            comps.append({
                'N': 10**p_dict['HI_logN'][i],
                'b': p_dict['HI_b'][i],
                'v': p_dict['HI_v'][i]
            })
        return comps
        
    def get_d_components(self, p_dict):
        # D associated with component A
        return [{
            'N': 10**p_dict['DI_logN'],
            'b': p_dict['HI_b'][0] / 1.4142, # Thermal scaling sqrt(2)
            'v': p_dict['HI_v'][0] - 81.6
        }]
        
    def log_likelihood(self, arr):
        p_dict = self.unpack_params(arr)
        hi_comps = self.get_components(p_dict)
        di_comps = self.get_d_components(p_dict)
        
        # Add basic prior constraints (log-likelihood penalty)
        penalty = 0.0
        
        # Velocity priors (tie to metals)
        for i in range(3):
            penalty += -0.5 * ((p_dict['HI_v'][i] - self.v_metals[i]) / 2.0)**2
            
        # Physical bounds penalty (b > 0)
        for b in p_dict['HI_b']:
            if b < 1.0 or b > 40.0:
                return -np.inf
                
        for logN in p_dict['HI_logN']:
            if logN < 12.0 or logN > 18.0:
                return -np.inf
                
        if p_dict['DI_logN'] < 10.0 or p_dict['DI_logN'] > 16.0:
            return -np.inf
        
        total_logL = penalty
        
        # Transitions to evaluate
        transitions_hi = ['HI_Lya', 'HI_Lyb', 'HI_Lyg', 'HI_Ly6', 'HI_Ly13', 'HI_Ly14', 'HI_Ly21']
        
        for i, chunk in enumerate(self.chunks):
            wave = chunk['wave']
            flux_obs = chunk['flux']
            err = chunk['err']
            
            # Mask valid errors
            mask = err > 0
            if np.sum(mask) == 0:
                continue
                
            tau_hi = self.engine.compute_optical_depth(wave, transitions_hi, hi_comps)
            tau_di = self.engine.compute_optical_depth(wave, transitions_hi, di_comps)
            tau_tot = tau_hi + tau_di
            
            flux_mod = self.engine.apply_continuum_and_zero(tau_tot, wave, p_dict['cont'][i], 0.0)
            
            # Simplified Instrumental Convolution (~3 km/s for HIRES)
            flux_mod = self.engine.apply_convolution(flux_mod, wave, 3.0)
            
            chi2 = np.sum(((flux_obs[mask] - flux_mod[mask]) / err[mask])**2)
            total_logL += -0.5 * chi2
            
        return -total_logL # Return negative for minimization

def run_fit():
    manifest_path = project_root / 'data' / 'processed' / 'Q1009_union_manifest.json'
    fitter = ConventionalFitter(manifest_path)
    
    # Initial Guess
    p0_dict = {
        'HI_logN': [17.36, 14.0, 14.0],
        'HI_b': [15.0, 10.0, 10.0],
        'HI_v': [0.0, 10.86, 14.71],
        'DI_logN': 12.8, # Assuming D/H ~ 2.5e-5 -> 17.36 - 4.6 = 12.76
        'cont': []
    }
    
    # Estimate continuum for each chunk
    for chunk in fitter.chunks:
        flux = chunk['flux']
        sorted_f = np.sort(flux)
        c0 = np.median(sorted_f[-max(5, len(flux)//10):]) if len(flux) > 0 else 1.0
        p0_dict['cont'].append([c0, 0.0])
        
    p0 = fitter.pack_params(p0_dict)
    
    print(f"Starting conventional fit with {len(p0)} parameters over {len(fitter.chunks)} chunks...")
    
    res = minimize(
        fitter.log_likelihood,
        p0,
        method='L-BFGS-B',
        options={'disp': True, 'maxiter': 50} # Short run for testing
    )
    
    print("\nFit Result:")
    print(res.message)
    print(f"Final Chi2: {res.fun * 2:.2f}")
    
    p_final = fitter.unpack_params(res.x)
    print("\nFinal Components:")
    for i, label in enumerate(['A', 'B', 'C']):
        print(f"HI {label}: logN = {p_final['HI_logN'][i]:.3f}, b = {p_final['HI_b'][i]:.2f}, v = {p_final['HI_v'][i]:.2f}")
    print(f"DI A: logN = {p_final['DI_logN']:.3f} (D/H = {p_final['DI_logN'] - p_final['HI_logN'][0]:.3f} dex)")

if __name__ == '__main__':
    run_fit()
