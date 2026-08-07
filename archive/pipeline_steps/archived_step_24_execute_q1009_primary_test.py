import os
import sys
import numpy as np
import json
from pathlib import Path

script_dir = Path(__file__).parent
project_root = script_dir.parent.parent
sys.path.append(str(project_root))

from scripts.steps.step_14c_joint_power_triage_screen import load_joint_spectra
from scripts.lib.q1009_primary_test_engine import fit_deterministic_model
from scripts.steps.step_23a_deterministic_smoke_calibration import compute_masks
import scripts.steps.step_13c_nested_synthetic_adversarial_validation as step13c

def run_q1009_primary_test():
    print("--- EXECUTING FORMAL Q1009 TARGET CLASSIFICATION ---")
    
    calib_path = project_root / 'data/processed/q1009_primary_test_calibration.json'
    if not calib_path.exists():
        print(f"ERROR: Calibration file {calib_path} not found.")
        sys.exit(1)
        
    with open(calib_path, 'r') as f:
        calibration = json.load(f)
        
    t_full_threshold = calibration['t_full_threshold']
    print(f"Loaded formal T_full threshold: {t_full_threshold:.4f}")
    
    manifest_path = project_root / 'data/processed/Q1009+2956_z2.504_HIRES_spectrum_manifest.json'
    real_spectra = load_joint_spectra(str(manifest_path))
    print(f"Loaded real target data from manifest.")
    
    feature_vector_path = project_root / 'data/processed/measured_feature_vector_Q1009+2956_z2.504.json'
    with open(feature_vector_path) as f:
        step13c.set_system_feature_vector(json.load(f))
        
    compute_masks(real_spectra)
    print("Computed strict spatial masks.")
    
    print("\nFitting H0 (Conventional Null)...")
    r_h0 = fit_deterministic_model(real_spectra, 'H0')
    print("Fitting H1 (Primary TEP Only)...")
    r_h1 = fit_deterministic_model(real_spectra, 'H1')
    print("Fitting H2 (Full Metal-Derived TEP)...")
    r_h2 = fit_deterministic_model(real_spectra, 'H2')
    
    T_full = 2 * (r_h2['logL_train'] - r_h0['logL_train'])
    T_sec = 2 * (r_h2['logL_train'] - r_h1['logL_train'])
    S_held = 2 * (r_h2['logL_held'] - max(r_h0['logL_held'], r_h1['logL_held']))
    
    converged = r_h0['converged'] and r_h1['converged'] and r_h2['converged']
    
    # Classification rule
    pass_t_full = T_full >= t_full_threshold
    pass_t_sec = T_sec > 0
    pass_s_held = S_held > 0
    
    is_positive = pass_t_full and pass_t_sec and pass_s_held and converged
    
    print("\n--- RESULTS ---")
    print(f"T_full      = {T_full:.4f} (Required: >= {t_full_threshold:.4f}) -> {'PASS' if pass_t_full else 'FAIL'}")
    print(f"T_secondary = {T_sec:.4f} (Required: > 0) -> {'PASS' if pass_t_sec else 'FAIL'}")
    print(f"S_held      = {S_held:.4f} (Required: > 0) -> {'PASS' if pass_s_held else 'FAIL'}")
    print(f"Converged   = {converged} -> {'PASS' if converged else 'FAIL'}")
    
    print(f"\nFINAL CLASSIFICATION: {'TEP_POSITIVE' if is_positive else 'REAL_NEGATIVE'}")
    
    # Dump detailed results
    final_result = {
        "classification": "TEP_POSITIVE" if is_positive else "REAL_NEGATIVE",
        "T_full": T_full,
        "T_secondary": T_sec,
        "S_held": S_held,
        "pass_t_full": bool(pass_t_full),
        "pass_t_sec": bool(pass_t_sec),
        "pass_s_held": bool(pass_s_held),
        "converged": bool(converged),
        "H0": {
            "logL_train": r_h0['logL_train'],
            "logL_held": r_h0['logL_held'],
            "converged": r_h0['converged'],
            "physical_parameters": r_h0['physical_parameters']
        },
        "H1": {
            "logL_train": r_h1['logL_train'],
            "logL_held": r_h1['logL_held'],
            "converged": r_h1['converged'],
            "physical_parameters": r_h1['physical_parameters']
        },
        "H2": {
            "logL_train": r_h2['logL_train'],
            "logL_held": r_h2['logL_held'],
            "converged": r_h2['converged'],
            "physical_parameters": r_h2['physical_parameters']
        }
    }
    
    out_path = project_root / 'data/processed/q1009_empirical_results_deterministic.json'
    with open(out_path, 'w') as f:
        json.dump(final_result, f, indent=2)
    print(f"\nSaved full results to {out_path}")

if __name__ == '__main__':
    run_q1009_primary_test()
