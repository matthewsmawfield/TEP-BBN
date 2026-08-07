import json
import numpy as np
from pathlib import Path
from scipy.optimize import minimize, Bounds
import sys

script_dir = Path(__file__).parent
project_root = script_dir.parent.parent
sys.path.insert(0, str(project_root))

from scripts.lib.physical_rt_engine import RadiativeTransferEngine

class ProfiledConventionalFitter:
    def __init__(self, manifest_path, cont_degree=1):
        with open(manifest_path, 'r') as f:
            self.manifest = json.load(f)
            
        self.z_abs = self.manifest['z_abs']
        self.engine = RadiativeTransferEngine(z_abs=self.z_abs)
        self.cont_degree = cont_degree
        
        # Load and pre-process data chunks
        self.chunks = []
        for coadd, chunks in self.manifest['coadds'].items():
            for c in chunks:
                wave = np.array(c['wave'])
                flux = np.array(c['flux'])
                err = np.array(c['err'])
                mask = err > 0
                
                if np.sum(mask) == 0:
                    continue
                    
                w_min, w_max = wave[0], wave[-1]
                if w_min == w_max:
                    x_norm = np.zeros_like(wave)
                else:
                    x_norm = 2.0 * (wave - w_min) / (w_max - w_min) - 1.0
                
                # Precompute Chebyshev basis P_k(x)
                P = np.zeros((len(wave), self.cont_degree + 1))
                for k in range(self.cont_degree + 1):
                    coef = np.zeros(self.cont_degree + 1)
                    coef[k] = 1.0
                    P[:, k] = np.polynomial.chebyshev.chebval(x_norm, coef)
                
                self.chunks.append({
                    'coadd': coadd,
                    'wave': wave,
                    'flux': flux,
                    'err': err,
                    'mask': mask,
                    'W': 1.0 / err**2,
                    'P': P
                })
                
        # Metal velocities from feature vector
        self.v_metals = [0.0, 10.863, 14.713]
        
    def pack_params(self, p_dict):
        # 3 components * 3 params + 1 DI_logN = 10 parameters
        arr = []
        for i in range(3):
            arr.append(p_dict['HI_logN'][i])
            arr.append(p_dict['HI_b'][i])
            arr.append(p_dict['HI_v'][i])
        arr.append(p_dict['DI_logN'])
        return np.array(arr)
        
    def unpack_params(self, arr):
        return {
            'HI_logN': arr[0:9:3],
            'HI_b': arr[1:9:3],
            'HI_v': arr[2:9:3],
            'DI_logN': arr[9]
        }
        
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
        return [{
            'N': 10**p_dict['DI_logN'],
            'b': p_dict['HI_b'][0] / 1.4142, # Thermal scaling sqrt(2)
            'v': p_dict['HI_v'][0] - 81.6
        }]
        
    def get_bounds(self):
        # lower and upper bounds
        lower = []
        upper = []
        for i in range(3):
            lower.extend([12.0, 1.0, self.v_metals[i] - 10.0]) # logN, b, v
            upper.extend([18.0, 40.0, self.v_metals[i] + 10.0])
        # DI
        lower.append(10.0)
        upper.append(16.0)
        return Bounds(lower, upper)
        
    def evaluate_optimal_chi2(self, arr):
        p_dict = self.unpack_params(arr)
        hi_comps = self.get_components(p_dict)
        di_comps = self.get_d_components(p_dict)
        
        penalty = 0.0
        # Weak prior on velocity matching metals exactly
        for i in range(3):
            penalty += ((p_dict['HI_v'][i] - self.v_metals[i]) / 2.0)**2
            
        total_chi2 = penalty
        transitions_hi = ['HI_Lya', 'HI_Lyb', 'HI_Lyg', 'HI_Ly6', 'HI_Ly13', 'HI_Ly14', 'HI_Ly21']
        
        # We need to compute total tau, then solve the linear system for the optimal continuum for each chunk
        for chunk in self.chunks:
            wave = chunk['wave']
            flux_obs = chunk['flux']
            mask = chunk['mask']
            W = chunk['W']
            P = chunk['P']
            
            # Compute optical depth
            tau_hi = self.engine.compute_optical_depth(wave, transitions_hi, hi_comps)
            tau_di = self.engine.compute_optical_depth(wave, transitions_hi, di_comps)
            tau_tot = tau_hi + tau_di
            
            # Design matrix X = P * exp(-tau)
            exp_tau = np.exp(-tau_tot)
            X = P * exp_tau[:, np.newaxis]
            
            # Apply convolution conceptually? 
            # In linear profile likelihood, if we convolve X after multiplying by exp(-tau), it's still linear!
            # F_mod = sum c_k [ (P_k exp(-tau)) * Gauss ]
            # So we can convolve each column of X.
            for k in range(X.shape[1]):
                X[:, k] = self.engine.apply_convolution(X[:, k], wave, 3.0)
                
            # Now we solve the weighted least squares: (X^T W X) c = X^T W y
            X_mask = X[mask]
            y_mask = flux_obs[mask]
            W_mask = W[mask]
            
            X_T_W = X_mask.T * W_mask
            H = X_T_W @ X_mask
            b = X_T_W @ y_mask
            
            try:
                c_opt = np.linalg.solve(H, b)
            except np.linalg.LinAlgError:
                # If singular, return a huge penalty
                return 1e10
                
            flux_mod = X_mask @ c_opt
            chi2_chunk = np.sum(W_mask * (y_mask - flux_mod)**2)
            total_chi2 += chi2_chunk
            
        return total_chi2

def run_profiled_fit():
    manifest_path = project_root / 'data' / 'processed' / 'Q1009_union_manifest.json'
    fitter = ProfiledConventionalFitter(manifest_path, cont_degree=2)
    
    # Initial Guess
    p0_dict = {
        'HI_logN': [17.36, 14.0, 14.0],
        'HI_b': [15.0, 10.0, 10.0],
        'HI_v': [0.0, 10.86, 14.71],
        'DI_logN': 12.8
    }
    
    p0 = fitter.pack_params(p0_dict)
    bounds = fitter.get_bounds()
    
    print(f"Starting Profiled Conventional Fit (10 non-linear parameters, {len(fitter.chunks)} independent continuums)")
    
    res = minimize(
        fitter.evaluate_optimal_chi2,
        p0,
        bounds=bounds,
        method='L-BFGS-B',
        options={'disp': True, 'maxiter': 200, 'ftol': 1e-6}
    )
    
    print("\nFit Result:")
    print(res.message)
    print(f"Final Chi2: {res.fun:.2f}")
    
    p_final = fitter.unpack_params(res.x)
    print("\nFinal Components:")
    for i, label in enumerate(['A', 'B', 'C']):
        print(f"HI {label}: logN = {p_final['HI_logN'][i]:.3f}, b = {p_final['HI_b'][i]:.2f}, v = {p_final['HI_v'][i]:.2f}")
    print(f"DI A: logN = {p_final['DI_logN']:.3f} (D/H = {p_final['DI_logN'] - p_final['HI_logN'][0]:.3f} dex)")

if __name__ == '__main__':
    run_profiled_fit()
