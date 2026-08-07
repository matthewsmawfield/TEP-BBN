import sys
import numpy as np
import json
from pathlib import Path

script_dir = Path(__file__).parent
project_root = script_dir.parent.parent
sys.path.append(str(project_root))

from scripts.steps.step_14c_joint_power_triage_screen import load_joint_spectra
from scripts.lib.joint_spectrum_likelihood import fit_model_nested_joint

def verify_registration(manifest_path):
    print("Verifying independent registration zero-points for Q1009 datasets...")
    spectra = load_joint_spectra(manifest_path)
    
    shifts = []
    
    import contextlib
    for i, spec in enumerate(spectra):
        print(f"Fitting independent M3_centroid for {spec['name']}...")
        
        with contextlib.redirect_stdout(None), contextlib.redirect_stderr(None):
            lz, lzerr, pdiag = fit_model_nested_joint(
                [spec], 
                'M3_centroid',
                nlive=100,
                centroid_bounds=[-10, 10]
            )
            
        v_shift = pdiag.get('v_shift_mean', 0.0)
        print(f"  v_shift: {v_shift:.3f} km/s")
        shifts.append(v_shift)
        
    shifts = np.array(shifts)
    max_diff = np.max(shifts) - np.min(shifts)
    print(f"\nMaximum pairwise offset difference: {max_diff:.3f} km/s")
    if max_diff <= 1.0:
        print("Registration is consistent (<= 1.0 km/s). PASS.")
    else:
        print("WAVELENGTH_REGISTRATION_INCONSISTENT. FAIL.")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest")
    args = parser.parse_args()
    
    verify_registration(args.manifest)
