import os
import sys
import numpy as np
import json
from pathlib import Path

script_dir = Path(__file__).parent
project_root = script_dir.parent.parent
sys.path.append(str(project_root))

from scripts.lib.joint_spectrum_likelihood import fit_model_nested_joint
from scripts.steps.step_14c_joint_power_triage_screen import load_joint_spectra
import scripts.steps.step_13c_nested_synthetic_adversarial_validation as step13c

def run_classification(spectra, suffix="", fixed_shifts=None):
    models_to_test = ["M2_full", "M3_centroid", "M2_primary_only", "M2_free_alpha", "M4_secondary_local"]
    logZs = {}
    logZerrs = {}
    posteriors = {}
    
    # We must enforce the fixed_shifts inside the joint likelihood evaluation if provided
    # However, since we are directly passing spectra to fit_model_nested_joint,
    # the easiest way to apply fixed shifts is to shift the v_grid of the spectra themselves
    # BEFORE calling the fit.
    # We want to "calibrate" the wavelength frame.
    # v_new = v_old - offset
    
    calibrated_spectra = []
    import copy
    for i, spec in enumerate(spectra):
        new_spec = copy.deepcopy(spec)
        if fixed_shifts is not None:
            # apply fixed calibration
            shift = fixed_shifts[i]
            new_spec['v'] = spec['v'] - shift
        calibrated_spectra.append(new_spec)
    
    print(f"Running nested sampling for {len(models_to_test)} models...")
    for m in models_to_test:
        print(f"  Fitting {m}...")
        lz, lzerr, pdiag = fit_model_nested_joint(calibrated_spectra, m, nlive=100, centroid_bounds=[-10, 10])
        logZs[m] = lz
        logZerrs[m] = lzerr
        posteriors[m] = pdiag
        
    is_tep, status, reason = step13c.classify_result(logZs, logZerrs, posteriors)
    
    result = {
        'is_tep': is_tep,
        'status': status,
        'reason': reason,
        'logZs': logZs,
        'logZerrs': logZerrs,
        'posteriors': posteriors
    }
    
    output_path = project_root / f"data/processed/Q1009_formal_classification_result{suffix}.json"
    with open(output_path, 'w') as f:
        json.dump(result, f, indent=2)
    print(f"Classification {suffix}: {status} - {reason}")
    print(f"Saved to {output_path.name}")
    return result

def run_formal_campaign(manifest_path):
    print(f"Loading {manifest_path} for FORMAL CLASSIFICATION...")
    
    # Load correct feature vector!
    target_name = Path(manifest_path).stem.replace("_HIRES_spectrum_manifest", "")
    fv_path = project_root / f"data/processed/measured_feature_vector_{target_name}.json"
    if fv_path.exists():
        with open(fv_path, 'r') as f:
            step13c.set_system_feature_vector(json.load(f))
        print(f"Loaded system feature vector from {fv_path.name}")
    else:
        print(f"WARNING: No feature vector found at {fv_path}. Using default.")
        
    spectra = load_joint_spectra(manifest_path)
    
    # 1. Primary Classification
    # One shared global v_shift, nominal instrumental widths
    print("\n--- 1. PRIMARY CLASSIFICATION ---")
    np.random.seed(420)
    primary_result = run_classification(spectra, suffix="_primary", fixed_shifts=None)
    
    # 2. Registration Robustness
    # Fixed external metal-derived shifts applied as wavelength calibrations
    print("\n--- 2. REGISTRATION ROBUSTNESS ---")
    
    # The external shifts from Step 20e
    external_shifts = [1.449, 1.238, 1.851, 1.712]
    
    np.random.seed(421)
    robust_result = run_classification(spectra, suffix="_robustness", fixed_shifts=external_shifts)
    
    # Compare
    status = primary_result['status']
    print("\n=== FINAL FORMAL DECISION ===")
    print(f"Primary classification: {status}")
    print(f"Robust classification:  {robust_result['status']}")
    
    if primary_result['status'] == robust_result['status']:
        print("\nREGISTRATION_ROBUST")
        print("Both setups yielded the same formal classification.")
    else:
        print("\nCLASSIFICATION_REGISTRATION_SENSITIVE")
        print("The formal outcome depended on the choice of registration zero-points.")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest")
    args = parser.parse_args()
    
    run_formal_campaign(args.manifest)
