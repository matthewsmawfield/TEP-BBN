import os
import sys
import numpy as np
import json
import math
from pathlib import Path

# Add project root to python path
script_dir = Path(__file__).parent
project_root = script_dir.parent.parent
sys.path.append(str(project_root))

from scripts.lib.joint_spectrum_likelihood import fit_model_nested_joint
import scripts.steps.step_13c_nested_synthetic_adversarial_validation as step13c

def load_joint_spectra(manifest_path):
    with open(manifest_path, 'r') as f:
        manifest = json.load(f)
    
    spectra = []
    z_abs = manifest['kinematic_reference_redshift']
    ly_alpha_rest = 1215.67
    ly_alpha_obs = ly_alpha_rest * (1.0 + z_abs)
    c_kms = 299792.458
    
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
        
        v_grid = (wave - ly_alpha_obs) / ly_alpha_obs * c_kms
        
        # Isolate analysis window [-300, 100]
        window_mask = (v_grid >= -300) & (v_grid <= 100)
        spectra.append({
            'name': s_info['setup'],
            'v': v_grid[window_mask],
            'flux': flux[window_mask],
            'err': err[window_mask],
            'sigma_v_kms': sigma_v
        })
        
    return spectra

import hashlib

def generate_synthetic_joint_flux(
    *,
    spectra,
    generating_model,
    physical_parameters,
    data_seed,
):
    """
    Generate synthetic flux for the given spectra list using the frozen base_model.
    Must use keyword-only arguments.
    """
    from scripts.lib.joint_spectrum_likelihood import evaluate_frozen_model
    
    assert generating_model in ["H0", "H1", "H2", "M2_full", "M3_centroid"], f"Invalid generating model: {generating_model}"
    assert "alpha" in physical_parameters, "physical_parameters must contain 'alpha'"
    assert 0.0 <= physical_parameters["alpha"] <= 0.001, f"alpha out of bounds: {physical_parameters['alpha']}"
    assert "v_shift" in physical_parameters
    assert "B_abs" in physical_parameters
    
    # Check if we are asking for an H2 TEP injection
    is_tep_injection = (generating_model in ["H2", "M2_full"]) and (physical_parameters["alpha"] > 0)
    
    synth_spectra = []
    
    # Save current random state
    rng_state = np.random.get_state()
    np.random.seed(data_seed)
    
    max_diff_from_null = 0.0
    
    for spec in spectra:
        local_params = {'c0': 1.0, 'c1': 0.0, 'c2': 0.0}
        
        # We assume H0 / M3_centroid doesn't use alpha. But we pass the dict as is.
        model_flux = evaluate_frozen_model(
            velocity=spec['v'],
            shared_params=physical_parameters,
            local_params=local_params,
            model_type=generating_model,
            sigma_v_kms=spec['sigma_v_kms']
        )
        
        null_params = physical_parameters.copy()
        null_params['alpha'] = 0.0
        null_flux = evaluate_frozen_model(
            velocity=spec['v'],
            shared_params=null_params,
            local_params=local_params,
            model_type=generating_model, # Evaluate the same model but at alpha=0
            sigma_v_kms=spec['sigma_v_kms']
        )
        
        # Calculate max difference
        diff = np.max(np.abs(model_flux - null_flux))
        max_diff_from_null = max(max_diff_from_null, diff)
        
        noise = np.random.normal(0, spec['err'])
        noisy_flux = model_flux + noise
        
        synth_spectra.append({
            'name': spec['name'],
            'v': spec['v'],
            'flux': noisy_flux,
            'err': spec['err'],
            'sigma_v_kms': spec['sigma_v_kms']
        })
        
    np.random.set_state(rng_state)
    
    if is_tep_injection:
        assert max_diff_from_null > 1e-5, f"TEP injection with alpha={physical_parameters['alpha']} produced no numeric difference from null! max_diff={max_diff_from_null}"
        
    # Generate manifest hash (just a fast SHA256 of the concatenated flux)
    all_flux = np.concatenate([s['flux'] for s in synth_spectra])
    flux_sha256 = hashlib.sha256(all_flux.tobytes()).hexdigest()
    
    manifest = {
        "generating_model": generating_model,
        "physical_parameters": physical_parameters,
        "data_seed": data_seed,
        "observed_flux_used": False,
        "flux_sha256": flux_sha256,
        "maximum_difference_from_null": float(max_diff_from_null)
    }
    
    return synth_spectra, manifest

def run_joint_triage(manifest_path, alpha_inject, n_trials=5):
    print(f"Running joint triage on {manifest_path} with alpha={alpha_inject}...")
    np.random.seed(42) # fixed seed
    
    spectra = load_joint_spectra(manifest_path)
    print(f"Loaded {len(spectra)} spectra.")
    
    recovered_count = 0
    
    shared_inj = {
        'v_shift': 0.0,
        'B_abs': 1.5e-5,
        'f_D': 0.0,
    }
    
    models_to_test = ["M2_full", "M3_centroid"]
    
    for i in range(n_trials):
        print(f" Trial {i+1}/{n_trials}...", end='', flush=True)
        
        synth_spectra, manifest = generate_synthetic_joint_flux(
            spectra=spectra, 
            generating_model="M2_full", 
            physical_parameters={**shared_inj, 'alpha': alpha_inject},
            data_seed=42 + i
        )
        
        logZs = {}
        
        import contextlib
        with contextlib.redirect_stdout(None):
            for m in models_to_test:
                # Fast triage parameters
                lz, lzerr, pdiag = fit_model_nested_joint(synth_spectra, m, nlive=50, centroid_bounds=[-10, 10])
                logZs[m] = lz
                
        delta_tep = logZs.get("M2_full", 0) - logZs.get("M3_centroid", 0)
        if delta_tep > 2.0:
            recovered_count += 1
            print(f" [RECOVERED] delta_logZ={delta_tep:.2f}")
        else:
            print(f" [FAILED] delta_logZ={delta_tep:.2f}")
            
    print(f"\nFinal Joint Triage Result: {recovered_count}/{n_trials} recovered.")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest")
    parser.add_argument("--alpha", type=float, default=0.0007)
    args = parser.parse_args()
    
    run_joint_triage(args.manifest, args.alpha)
