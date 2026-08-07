import os
import sys
import numpy as np
import json
from pathlib import Path

script_dir = Path(__file__).parent
project_root = script_dir.parent.parent
sys.path.append(str(project_root))

from scripts.steps.step_21_formal_power_campaign import run_single_trial
from scripts.steps.step_14c_joint_power_triage_screen import load_joint_spectra
import scripts.steps.step_13c_nested_synthetic_adversarial_validation as step13c

def debug_power():
    manifest_path = project_root / "data/processed/Q1009+2956_z2.504_HIRES_spectrum_manifest.json"
    spectra = load_joint_spectra(manifest_path)
    
    # Load feature vector
    fv_path = project_root / "data/processed/measured_feature_vector_Q1009+2956_z2.504.json"
    with open(fv_path, 'r') as f:
        step13c.set_system_feature_vector(json.load(f))
        
    shared_inj = {'v_shift': 0.0, 'B_abs': 1.5e-5, 'f_D': 0.0}
    alpha_inject = 0.0007
    seed = 42
    
    print("Running single trial injection with alpha=0.0007...")
    is_tep, delta_tep, logZs, posteriors = None, None, None, None
    
    # Modified run_single_trial to return posteriors too
    from scripts.steps.step_21_formal_power_campaign import generate_synthetic_joint_flux, fit_model_nested_joint, compute_sec_windows_and_held_out
    
    np.random.seed(seed)
    synth_spectra = generate_synthetic_joint_flux(spectra, shared_inj, "M2_full", inject_alpha=alpha_inject)
    
    logZs = {}
    logZerrs = {}
    posteriors = {}
    
    m = "M3_centroid"
    print(f"Fitting {m}...")
    lz, lzerr, pdiag = fit_model_nested_joint(synth_spectra, m, nlive=100, centroid_bounds=[-10, 10])
    logZs[m] = lz
    logZerrs[m] = lzerr
    posteriors[m] = pdiag
    
    merged_windows, _ = compute_sec_windows_and_held_out(synth_spectra, posteriors)
    
    for m in ["M2_full", "M2_primary_only", "M2_free_alpha"]:
        print(f"Fitting {m}...")
        lz, lzerr, pdiag = fit_model_nested_joint(synth_spectra, m, nlive=100, centroid_bounds=[-10, 10])
        logZs[m] = lz
        logZerrs[m] = lzerr
        posteriors[m] = pdiag
        
    m = "M4_secondary_local"
    print(f"Fitting {m}...")
    lz, lzerr, pdiag = fit_model_nested_joint(synth_spectra, m, nlive=100, centroid_bounds=[-10, 10], sec_windows=merged_windows)
    logZs[m] = lz
    logZerrs[m] = lzerr
    posteriors[m] = pdiag
    
    _, held_out_diff = compute_sec_windows_and_held_out(synth_spectra, posteriors)
    posteriors['held_out_diff'] = float(held_out_diff)
        
    is_tep, status, reason = step13c.classify_result(logZs, logZerrs, posteriors)
    
    print(f"\nResult: is_tep={is_tep}")
    print(f"Status: {status}")
    print(f"Reason: {reason}")
    print("\nDiagnostics:")
    
    best_TEP = max(['M1_full', 'M2_full'], key=lambda k: logZs.get(k, -1e9))
    best_non_TEP = max(['Mnull', 'M0', 'M3_global', 'M3_Dlocal', 'M3_centroid', 'M4_secondary_local'], key=lambda k: logZs.get(k, -1e9))
    print(f"Best TEP model: {best_TEP} ({logZs.get(best_TEP, 0):.2f})")
    print(f"Best non-TEP model: {best_non_TEP} ({logZs.get(best_non_TEP, 0):.2f})")
    
    print("\nLogZs:")
    for k, v in logZs.items():
        print(f"  {k}: {v:.2f} ± {logZerrs[k]:.2f}")
        
    pdiag = posteriors.get('M2_full', {})
    pdiag_free = posteriors.get('M2_free_alpha', {})
    print("\nM2_full Posteriors:")
    print(f"  P_f_D_lt_0p5: {pdiag.get('P_f_D_lt_0p5', 0):.4f}")
    print(f"  alpha_at_lower_edge: {pdiag.get('alpha_at_lower_edge', True)}")
    print(f"  alpha_at_upper_edge: {pdiag.get('alpha_at_upper_edge', True)}")
    print(f"  alpha_mean: {pdiag.get('alpha_mean', 0.0)}")
    
    print("\nM2_free_alpha Posteriors:")
    print(f"  P_alpha_in_prior: {pdiag_free.get('P_alpha_in_prior', 0):.4f}")
    print(f"  alpha_mean: {pdiag_free.get('alpha_mean', 0.0)}")
    
    delta_sec = logZs.get('M2_full', 0) - logZs.get('M2_primary_only', 0)
    delta_m4 = logZs.get('M2_full', 0) - logZs.get('M4_secondary_local', 0)
    
    print("\nBayes Factors:")
    print(f"  M2_full vs M2_primary_only: {delta_sec:.2f}")
    print(f"  M2_full vs M4_secondary_local: {delta_m4:.2f}")
    print(f"  held_out_diff: {posteriors.get('held_out_diff', 0.0):.2f}")

if __name__ == "__main__":
    debug_power()
