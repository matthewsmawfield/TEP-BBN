import os
import sys
import numpy as np
import math
import json
from pathlib import Path
from scipy.optimize import minimize
from scipy.stats import norm

script_dir = Path(__file__).parent
project_root = script_dir.parent.parent
sys.path.append(str(project_root))

C_KMS = 299792.458

def load_metal_spectra(manifest_path, rest_wave, z_abs):
    with open(manifest_path, 'r') as f:
        manifest = json.load(f)
        
    spectra = []
    obs_wave = rest_wave * (1.0 + z_abs)
    
    for s_info in manifest['spectra']:
        path = s_info['file']
        sigma_v = s_info['sigma_v_kms']
        
        # Load
        if path.endswith('.dat'):
            data = np.loadtxt(path)
            wave = data[:, 0]
            flux = data[:, 1]
            err = data[:, 2] if data.shape[1] > 2 else np.ones_like(flux)*np.std(flux)
        elif path.endswith('.fits'):
            from astropy.io import fits
            hdul = fits.open(path)
            header = hdul[0].header
            flux = hdul[0].data
            crval = header['CRVAL1']
            cdelt = header['CDELT1']
            crpix = header.get('CRPIX1', 1)
            wave = crval + (np.arange(len(flux)) - (crpix - 1)) * cdelt
            if 'LOG10' in header.get('CTYPE1', '').upper() or header.get('DC-FLAG', 0) == 1:
                wave = 10**wave
            err_path = path.replace('_f.fits', '_e.fits')
            if os.path.exists(err_path):
                err = fits.open(err_path)[0].data
            else:
                err = np.ones_like(flux) * 0.05
        
        valid_mask = err > 0
        wave = wave[valid_mask]
        flux = flux[valid_mask]
        err = err[valid_mask]
        
        v_grid = (wave - obs_wave) / obs_wave * C_KMS
        
        # Extract [-100, 100] km/s window around the metal line
        window_mask = (v_grid >= -100) & (v_grid <= 100)
        
        # We need to make sure we actually have data in this window
        if np.sum(window_mask) < 10:
            continue
            
        spectra.append({
            'name': s_info['setup'],
            'v': v_grid[window_mask],
            'flux': flux[window_mask],
            'err': err[window_mask],
            'sigma_v_kms': sigma_v,
            'wave': wave[window_mask]
        })
        
    return spectra

def eval_metal_template(v, v_shift, scale, c0, c1, sigma_v_kms):
    """
    Fixed 3-component template based on Q1009 metals.
    v_comps = [0.0, 10.863, 14.713]
    rel_N = [1.0, 0.3, 0.05]
    """
    b_intrinsic = 5.0 # representative km/s
    b_eff = math.sqrt(b_intrinsic**2 + sigma_v_kms**2)
    
    v_comps = [0.0, 10.863, 14.713]
    weights = [1.0, 0.3, 0.05]
    
    tau = np.zeros_like(v)
    for vc, w in zip(v_comps, weights):
        # Gaussian optical depth
        tau += scale * w * np.exp(-((v - v_shift - vc)**2) / (b_eff**2))
        
    continuum = c0 + c1 * v
    return continuum * np.exp(-tau)

def estimate_vshift(v, flux, err, sigma_v_kms, init_vshift=0.0):
    def nll(params):
        v_shift, scale, c0, c1 = params
        model = eval_metal_template(v, v_shift, scale, c0, c1, sigma_v_kms)
        return 0.5 * np.sum(((flux - model) / err)**2)
        
    # Initial guesses
    p0 = [init_vshift, 0.5, 1.0, 0.0]
    
    # Bounds: v_shift in [-20, 20], scale > 0
    bounds = [(-20.0, 20.0), (0.0, 100.0), (0.0, 5.0), (-0.1, 0.1)]
    
    # We want to run optimization
    res = minimize(nll, p0, bounds=bounds, method='L-BFGS-B')
    
    # Calculate uncertainty from the inverse Hessian approximation
    # If it hit a boundary, flag it
    hit_bound = False
    for i, (b_min, b_max) in enumerate(bounds):
        if np.isclose(res.x[i], b_min, atol=1e-5) or np.isclose(res.x[i], b_max, atol=1e-5):
            hit_bound = True
            
    # Compute formal covariance using numerical Hessian if L-BFGS-B inverse hessian isn't robust
    # Actually L-BFGS-B provides res.hess_inv which is a LinearOperator. 
    # We can compute numerical hessian of nll at optimum
    eps = 1e-4
    hessian = np.zeros((4, 4))
    for i in range(4):
        for j in range(4):
            p1, p2, p3, p4 = res.x.copy(), res.x.copy(), res.x.copy(), res.x.copy()
            p1[i] += eps; p1[j] += eps
            p2[i] += eps; p2[j] -= eps
            p3[i] -= eps; p3[j] += eps
            p4[i] -= eps; p4[j] -= eps
            hessian[i, j] = (nll(p1) - nll(p2) - nll(p3) + nll(p4)) / (4 * eps**2)
            
    try:
        cov = np.linalg.inv(hessian)
        v_err = math.sqrt(cov[0, 0]) if cov[0, 0] > 0 else 999.0
    except np.linalg.LinAlgError:
        v_err = 999.0
        
    return res.x[0], v_err, hit_bound, res.success, res.fun

def run_synthetic_validation(manifest_path):
    print("--- Q1009 Synthetic Registration Validation ---")
    
    # C II 1334
    rest_wave = 1334.5323
    z_abs = 2.5035873411
    
    spectra = load_metal_spectra(manifest_path, rest_wave, z_abs)
    print(f"Loaded {len(spectra)} setups for synthetic validation.")
    
    injected_shifts = [-1.0, -0.5, 0.0, 0.5, 1.0]
    n_sims = 200
    
    np.random.seed(42)
    
    results_dict = {}
    for spec in spectra:
        print(f"\nEvaluating setup: {spec['name']}")
        results_dict[spec['name']] = {}
        
        for inj_v in injected_shifts:
            recovered_v = []
            recovered_err = []
            hit_bounds_count = 0
            success_count = 0
            
            # True parameters
            true_scale = 0.5
            true_c0 = 1.0
            true_c1 = 0.0
            
            for _ in range(n_sims):
                # Generate synthetic truth on the exact setup grid
                truth = eval_metal_template(spec['v'], inj_v, true_scale, true_c0, true_c1, spec['sigma_v_kms'])
                
                # Add noise
                noise = np.random.normal(0, spec['err'])
                synth_flux = truth + noise
                
                # Recover
                est_v, est_err, hit_bound, success, _ = estimate_vshift(spec['v'], synth_flux, spec['err'], spec['sigma_v_kms'])
                
                if success and not hit_bound:
                    recovered_v.append(est_v)
                    recovered_err.append(est_err)
                    success_count += 1
                if hit_bound:
                    hit_bounds_count += 1
                    
            if len(recovered_v) == 0:
                print(f"  Inj {inj_v:+.1f} km/s: ALL FAILED")
                continue
                
            rec_v = np.array(recovered_v)
            rec_err = np.array(recovered_err)
            
            mean_v = np.mean(rec_v)
            bias = mean_v - inj_v
            rms = np.std(rec_v)
            median_err = np.median(rec_err)
            
            # Coverage
            pulls = (rec_v - inj_v) / rec_err
            cov_68 = np.mean(np.abs(pulls) <= 1.0)
            cov_95 = np.mean(np.abs(pulls) <= 2.0)
            
            results_dict[spec['name']][f"{inj_v:+.1f}"] = {
                "number_of_simulations": success_count,
                "mean_recovered_shift": float(mean_v),
                "mean_bias": float(bias),
                "rms_error": float(rms),
                "median_quoted_uncertainty": float(median_err),
                "coverage_68_percent": float(cov_68),
                "coverage_95_percent": float(cov_95),
                "boundary_hit_rate": float(hit_bounds_count / n_sims),
                "failure_rate": float((n_sims - success_count - hit_bounds_count) / n_sims)
            }
            
            print(f"  Inj {inj_v:+.1f} km/s:")
            print(f"    Mean recovered: {mean_v:+.3f} km/s (Bias: {bias:+.3f} km/s)")
            print(f"    RMS error:      {rms:.3f} km/s")
            print(f"    Median uncert:  {median_err:.3f} km/s")
            print(f"    68% Coverage:   {cov_68*100:.1f}%")
            print(f"    95% Coverage:   {cov_95*100:.1f}%")
            if hit_bounds_count > 0:
                print(f"    Optimizer boundaries hit: {hit_bounds_count}/{n_sims}")
                
    output_path = project_root / "data/processed/Q1009_synthetic_registration_validation.json"
    with open(output_path, "w") as f:
        json.dump(results_dict, f, indent=2)
    print(f"\n[REPORT GENERATED] Saved to {output_path.name}")
                
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest")
    args = parser.parse_args()
    
    run_synthetic_validation(args.manifest)
