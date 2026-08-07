#!/usr/bin/env python3
import argparse
import numpy as np
import json
import sys
import os
from pathlib import Path
from scipy.interpolate import interp1d

# Try to import Dynesty and related models from step_13c
try:
    from step_13c_nested_synthetic_adversarial_validation import fit_model_nested, base_model, classify_result
    import step_13c_nested_synthetic_adversarial_validation as step13
except ImportError:
    pass

def load_spectrum(spectrum_path, z_abs):
    """Loads a spectrum, shifts to rest frame, and isolates the Ly-alpha window."""
    print(f"Loading spectrum from {spectrum_path}...")
    if spectrum_path.endswith('.dat'):
        try:
            data = np.loadtxt(spectrum_path)
            wave = data[:, 0]
            flux = data[:, 1]
            if data.shape[1] > 2:
                err = data[:, 2]
            else:
                err = np.ones_like(flux) * np.std(flux)
        except Exception as e:
            print(f"Error loading {spectrum_path}: {e}")
            sys.exit(1)
    elif spectrum_path.endswith('.fits'):
        from astropy.io import fits
        try:
            # Assuming KODIAQ format where _f.fits is flux and _e.fits is error
            # Or SQUAD format. Let's just try to read CRVAL1, CDELT1
            hdul = fits.open(spectrum_path)
            header = hdul[0].header
            flux = hdul[0].data
            crval = header['CRVAL1']
            cdelt = header['CDELT1']
            crpix = header.get('CRPIX1', 1)
            wave = crval + (np.arange(len(flux)) - (crpix - 1)) * cdelt
            if 'LOG10' in header.get('CTYPE1', '').upper() or header.get('DC-FLAG', 0) == 1:
                wave = 10**wave
                
            err_path = spectrum_path.replace('_f.fits', '_e.fits')
            if os.path.exists(err_path):
                err = fits.open(err_path)[0].data
            else:
                # Mock errors if missing
                err = np.ones_like(flux) * 0.05
        except Exception as e:
            print(f"Error loading {spectrum_path}: {e}")
            sys.exit(1)
    else:
        print("Unsupported spectrum format")
        sys.exit(1)
    return wave, flux, err

def verify_coverage_and_snr(spec_path, z_abs):
    wave, flux, err = load_spectrum(spec_path, z_abs)

    # Filter out bad pixels
    valid_mask = err > 0
    wave = wave[valid_mask]
    flux = flux[valid_mask]
    err = err[valid_mask]

    # Target Ly-alpha rest wavelength
    ly_alpha_rest = 1215.67
    ly_alpha_obs = ly_alpha_rest * (1.0 + z_abs)

    # Convert to velocity relative to ly_alpha_obs
    c_kms = 299792.458
    v_grid = (wave - ly_alpha_obs) / ly_alpha_obs * c_kms

    # Check coverage [-300, 100] km/s
    if np.min(v_grid) > -300 or np.max(v_grid) < 100:
        print(f"Insufficient coverage. Wavelength range: {wave[0]:.2f} - {wave[-1]:.2f} A")
        print(f"Velocity range: {np.min(v_grid):.1f} - {np.max(v_grid):.1f} km/s")
        return False, 0.0, None, None

    # Estimate SNR in a nearby sideband free of strong absorption
    # We will pick [-500, -300] km/s or [100, 300] km/s depending on what is available
    mask_sideband = ((v_grid > -500) & (v_grid < -300)) | ((v_grid > 100) & (v_grid < 300))
    if np.sum(mask_sideband) < 50:
        # fallback to a smaller window
        mask_sideband = ((v_grid > -300) & (v_grid < -200)) | ((v_grid > 50) & (v_grid < 100))
        
    chunk_flux = flux[mask_sideband]
    chunk_err = err[mask_sideband]
    
    if len(chunk_flux) < 10:
        print("Could not find enough continuum pixels to measure SNR.")
        snr = 0.0
    else:
        # To avoid being skewed by strong deep absorptions in the sideband, 
        # we calculate SNR on pixels where flux is > 0.5 (assuming normalized)
        valid_continuum = chunk_flux > 0.5
        if np.sum(valid_continuum) > 10:
            snr = np.median(chunk_flux[valid_continuum] / chunk_err[valid_continuum])
        else:
            snr = np.median(chunk_flux / chunk_err)
            
    print(f"  Coverage: {np.min(v_grid):.1f} to {np.max(v_grid):.1f} km/s [PASS]")
    print(f"  Estimated local SNR: {snr:.1f}")

    if snr < 30:
        print("  [FAIL] SNR < 30. Rejecting spectrum.")
        return False, snr, v_grid, err
    else:
        print("  [PASS] SNR >= 30. Spectrum power looks promising.")
        
    # Interpolate onto a uniform grid for the triage test [-200, 100]
    uniform_v = np.linspace(-200, 100, 300)
    interp_err = interp1d(v_grid, err, bounds_error=False, fill_value="extrapolate")
    uniform_err = interp_err(uniform_v)
    
    return True, snr, uniform_v, uniform_err

def run_triage_injection(v_grid, err_grid, alpha_inject, n_trials=5):
    print(f"\nRunning {n_trials} triage injection-recovery trials with alpha={alpha_inject}...")
    
    # Mock a single component feature vector for the triage model
    mock_fv = {
        "components": [
            {"velocity_kms": 0.0, "metal_alignment_strength": 1.0, "g_i": 1.0}
        ]
    }
    step13.set_system_feature_vector(mock_fv)
    step13.v_grid = v_grid
    step13.x_norm = (v_grid - v_grid[0]) / (v_grid[-1] - v_grid[0]) * 2.0 - 1.0
    
    recovered_count = 0
    
    for i in range(n_trials):
        print(f" Trial {i+1}/{n_trials}...", end="", flush=True)
        # Generate noise
        noise = np.random.normal(0, err_grid)
        
        # Base parameters for injection
        params = {
            'c0': 1.0, 'c1': 0.0, 'c2': 0.0,
            'v_shift': 0.0, 'lsf_scale': 1.0,
            'B_abs': 1.0, 'f_D': 0.8,
            'alpha': alpha_inject
        }
        
        # Generate flux
        clean_flux = base_model(params, tep_primary_only=False)
        sim_flux = clean_flux + noise
        
        # Run inference (just the TEP model vs standard)
        # We will run M2_full (standard physics) vs M3_tep_primary
        # Since it's a triage, we can skip other models to save time
        
        models_to_test = ["M2_full", "M3_centroid"]
        logZs = {}
        logZerrs = {}
        posteriors = {}
        
        # Suppress Dynesty output
        import contextlib
        with contextlib.redirect_stdout(None):
            for m in models_to_test:
                lz, lzerr, pdiag = fit_model_nested(sim_flux, m, np.mean(err_grid), centroid_bounds=[-10, 10])
                logZs[m] = lz
                logZerrs[m] = lzerr
                posteriors[m] = pdiag
                
        # Simple Triage Classification
        delta_tep = logZs.get("M2_full", 0) - logZs.get("M3_centroid", 0)
        is_tep = delta_tep > 2.0
        if is_tep:
            recovered_count += 1
            print(" [RECOVERED]")
        else:
            print(" [MISSED]")
            
    print(f"\nFinal Triage Result: {recovered_count}/{n_trials} recovered.")
    if recovered_count == 0:
        print("Verdict: Reject target as obviously low-power.")
    elif recovered_count <= 3:
        print("Verdict: Probably marginal; deprioritise.")
    else:
        print("Verdict: Proceed to full frozen power campaign.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("spectrum_path", type=str)
    parser.add_argument("z_abs", type=float)
    parser.add_argument("--alpha", type=float, default=0.0007)
    args = parser.parse_args()
    
    # Try to add path so step_13c can be found
    sys.path.insert(0, str(Path(__file__).parent))
    
    passed_snr, snr, uniform_v, uniform_err = verify_coverage_and_snr(args.spectrum_path, args.z_abs)
    
    if passed_snr:
        run_triage_injection(uniform_v, uniform_err, args.alpha, n_trials=5)
