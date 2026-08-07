import os
import sys
import numpy as np
import math
import json
from pathlib import Path
from scipy.optimize import minimize

script_dir = Path(__file__).parent
project_root = script_dir.parent.parent
sys.path.append(str(project_root))

from scripts.steps.step_20d_registration_synthetic_validation import load_metal_spectra, estimate_vshift

# Preregistered metal lines
METAL_LINES = {
    "C_II_1334": 1334.5323,
    "Si_IV_1393": 1393.7550,
    "Si_IV_1402": 1402.7700,
    "C_IV_1548": 1548.1950,
    "C_IV_1550": 1550.7700
}

# Predefined quality rules
MIN_VALID_PIXELS = 10
MAX_MASKED_FRACTION = 0.5
MIN_SNR = 5.0  # Kept reasonable to allow weaker Si IV lines
MAX_UNCERTAINTY_KMS = 1.0

def run_registration_audit(manifest_path):
    print("=== Q1009 REGISTRATION AUDIT (Step 20e) ===")
    
    with open(manifest_path, 'r') as f:
        manifest = json.load(f)
        
    z_abs = manifest['kinematic_reference_redshift']
    
    # We will accumulate results per setup
    setup_results = {s_info['setup']: [] for s_info in manifest['spectra']}
    
    # Analyze each transition
    for line_name, rest_wave in METAL_LINES.items():
        print(f"\n--- Transition: {line_name} ---")
        spectra = load_metal_spectra(manifest_path, rest_wave, z_abs)
        
        for spec in spectra:
            setup = spec['name']
            
            # Compute quality metrics
            n_pixels_total = len(spec['wave'])
            # We already masked err <= 0 during loading, but let's check basic stats
            if n_pixels_total < MIN_VALID_PIXELS:
                print(f"  {setup}: REJECTED (Insufficient pixels: {n_pixels_total})")
                continue
                
            median_err = np.median(spec['err'])
            median_flux = np.median(spec['flux'])
            snr = median_flux / median_err if median_err > 0 else 0.0
            
            if snr < MIN_SNR:
                print(f"  {setup}: REJECTED (Low SNR: {snr:.1f} < {MIN_SNR})")
                continue
                
            # Fit
            est_v, est_err, hit_bound, success, _ = estimate_vshift(
                spec['v'], spec['flux'], spec['err'], spec['sigma_v_kms']
            )
            
            quality_pass = (
                success and 
                not hit_bound and 
                est_err <= MAX_UNCERTAINTY_KMS
            )
            
            if quality_pass:
                setup_results[setup].append({
                    'line': line_name,
                    'v_shift': est_v,
                    'v_err': est_err,
                    'snr': snr
                })
                print(f"  {setup}: ACCEPTED -> v = {est_v:+.3f} ± {est_err:.3f} km/s (SNR={snr:.1f})")
            else:
                reason = "Hit Bound" if hit_bound else "Optimization Failed" if not success else f"High Uncert ({est_err:.2f})"
                print(f"  {setup}: REJECTED ({reason})")
                
    # Combine results
    print("\n=== COMBINED REGISTRATION ===")
    
    combined_offsets = {}
    
    for setup, results in setup_results.items():
        if len(results) == 0:
            print(f"{setup}: NO USABLE TRANSITIONS")
            sys.exit(1)
            
        # Inverse variance weighting
        weights = np.array([1.0 / (r['v_err']**2) for r in results])
        v_shifts = np.array([r['v_shift'] for r in results])
        
        weighted_mean = np.sum(weights * v_shifts) / np.sum(weights)
        weighted_err = math.sqrt(1.0 / np.sum(weights))
        
        # Heterogeneity (chi2)
        chi2 = np.sum(((v_shifts - weighted_mean) / np.array([r['v_err'] for r in results]))**2)
        
        combined_offsets[setup] = {
            'v_shift': weighted_mean,
            'v_err': weighted_err,
            'n_lines': len(results),
            'chi2': chi2
        }
        
        print(f"{setup}: v = {weighted_mean:+.3f} ± {weighted_err:.3f} km/s (from {len(results)} lines, internal chi2={chi2:.1f})")
        
    # Global heterogeneity and pairwise
    print("\n=== PAIRWISE ANALYSIS ===")
    
    setups = list(combined_offsets.keys())
    max_diff = 0.0
    max_sig = 0.0
    worst_pair = ("", "")
    
    for i in range(len(setups)):
        for j in range(i + 1, len(setups)):
            s1 = setups[i]
            s2 = setups[j]
            v1, e1 = combined_offsets[s1]['v_shift'], combined_offsets[s1]['v_err']
            v2, e2 = combined_offsets[s2]['v_shift'], combined_offsets[s2]['v_err']
            
            diff = abs(v1 - v2)
            sig = diff / math.sqrt(e1**2 + e2**2)
            
            print(f"{s1} vs {s2}: Diff = {diff:.3f} km/s, Significance = {sig:.2f} sigma")
            
            if diff > max_diff:
                max_diff = diff
            if sig > max_sig:
                max_sig = sig
                worst_pair = (s1, s2)
                
    print(f"\nMaximum Difference: {max_diff:.3f} km/s")
    print(f"Maximum Significance: {max_sig:.2f} sigma")
    
    if max_diff > 1.0 and max_sig > 3.0:
        print("\nWAVELENGTH_REGISTRATION_INCONSISTENT")
        print("Registration FAILS preregistered threshold (>1.0 km/s AND >3 sigma).")
        sys.exit(1)
    else:
        print("\nREGISTRATION_CONSISTENT")
        print("Registration passes preregistered threshold.")
        sys.exit(0)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest")
    args = parser.parse_args()
    
    run_registration_audit(args.manifest)
