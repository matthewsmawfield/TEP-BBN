"""
Actual TEP shear model analysis for TEP-BBN

Applies TEP shear model to fitted spectra to test temporal equivalence principle.
"""

import json
from pathlib import Path
from datetime import datetime
import sys
import numpy as np

# Add parent directory to path for imports
script_dir = Path(__file__).parent
project_root = script_dir.parent.parent
sys.path.insert(0, str(project_root))

from scripts.utils.tep_shear_model import TEPShearModel

def analyze_tep_shear_actual():
    """
    Apply TEP shear model to fitted spectra to test temporal equivalence principle.
    
    This step:
    1. Loads D/H measurement from step_07
    2. Initializes TEP shear model
    3. Calculates required shear to mimic D/H
    4. Assesses physical plausibility
    5. Compares to cosmological time scales
    """
    print("Step 08: TEP shear model analysis (Actual)")
    print("=" * 60)
    print("CRITICAL: This step uses real D/H measurement from step_07.")
    print("No placeholder or synthetic data is allowed.")
    print("=" * 60)
    print()
    
    # Check for Voigt fitting results
    fitting_results_path = project_root / 'data/processed/voigt_fitting_results.json'
    if not fitting_results_path.exists():
        print("ERROR: Voigt fitting results not found")
        print("Expected: data/processed/voigt_fitting_results.json")
        print("Run step_07 to perform Voigt fitting")
        return None
    
    with open(fitting_results_path, 'r') as f:
        fitting_results = json.load(f)
    
    print(f"Found Voigt fitting results: {fitting_results['status']}")
    print()
    
    # Extract D/H ratio
    dh_ratio = fitting_results['fitting_results']['dh_ratio']['value']
    print(f"D/H ratio from step_07: {dh_ratio:.2e}")
    print()
    
    # Initialize TEP shear model
    print("Initializing TEP shear model...")
    model = TEPShearModel()
    print(f"✓ Alpha variation rate: {model.alpha_variation_rate:.2e} /year")
    print(f"✓ Mu variation rate: {model.mu_variation_rate:.2e} /year")
    print()
    
    # Calculate required shear for observed D/H
    print("Calculating required shear to mimic observed D/H...")
    required_shear = model.calculate_required_shear_for_d_h(dh_ratio)
    print(f"Required Δln(A): {required_shear['required_delta_ln_a']:.2e}")
    print(f"Required time: {required_shear['required_time_years']:.2e} years")
    print()
    
    # Calculate time to mimic deuterium isotope shift
    mimicry_time = model.find_mimicry_time()
    print(f"Time to mimic deuterium isotope shift: {mimicry_time:.2e} years")
    print()
    
    # Calculate ln(A) variation for different times
    times = [1e6, 1e7, 1e8, 1e9, 1e10]
    print("ln(A) variation for different times:")
    for time in times:
        delta_ln_a = model.calculate_ln_a_variation(time)
        print(f"  {time:.0e} years: {delta_ln_a:.2e}")
    print()
    
    # Assess physical plausibility
    print("Physical plausibility assessment:")
    print()
    
    # Compare to age of universe
    age_universe = 13.8e9  # years
    print(f"Age of universe: {age_universe:.2e} years")
    print(f"Required time for observed D/H: {required_shear['required_time_years']:.2e} years")
    
    if required_shear['required_time_years'] > 0:
        time_ratio = required_shear['required_time_years'] / age_universe
        print(f"Time ratio: {time_ratio:.2e}")
        
        if time_ratio > 1:
            print("⚠️  Required time exceeds age of universe")
            print("   This suggests TEP shear is unlikely to explain observed D/H")
        elif time_ratio > 0.1:
            print("⚠️  Required time is comparable to age of universe")
            print("   This suggests TEP shear may be marginally plausible")
        else:
            print("✓ Required time is much less than age of universe")
            print("   This suggests TEP shear could be physically plausible")
    else:
        print("✓ No shear required (D/H consistent with standard physics)")
    
    print()
    
    # Calculate wavelength shift for observed D/H
    print("Wavelength shift analysis:")
    print()
    
    # Calculate wavelength shift for Lyman-alpha (1215.67 Å)
    lyman_alpha = 1215.67  # Å
    wavelength_shift = model.calculate_wavelength_shift(lyman_alpha, required_shear['required_time_years'])
    print(f"Lyman-alpha wavelength shift: {wavelength_shift:.2e} Å")
    print(f"Relative shift: {wavelength_shift/lyman_alpha:.2e}")
    print()
    
    # Create results
    results = {
        'analysis_date': datetime.now().isoformat(),
        'system_id': 'Q0913+072_z2.618',
        'status': 'analysis_complete',
        'dh_ratio': dh_ratio,
        'tep_model': {
            'alpha_variation_rate': model.alpha_variation_rate,
            'mu_variation_rate': model.mu_variation_rate,
            'deuterium_isotope_shift': model.deuterium_isotope_shift
        },
        'shear_analysis': {
            'required_delta_ln_a': required_shear['required_delta_ln_a'],
            'required_time_years': required_shear['required_time_years'],
            'mimicry_time_years': mimicry_time
        },
        'physical_plausibility': {
            'age_universe_years': age_universe,
            'time_ratio': time_ratio if required_shear['required_time_years'] > 0 else 0,
            'plausible': time_ratio < 1 if required_shear['required_time_years'] > 0 else True
        },
        'wavelength_analysis': {
            'lyman_alpha_wavelength': lyman_alpha,
            'wavelength_shift': wavelength_shift,
            'relative_shift': wavelength_shift/lyman_alpha
        },
        'ln_a_variations': {
            f'{time:.0e}_years': model.calculate_ln_a_variation(time)
            for time in times
        },
        'interpretation': 'TEP shear analysis complete. Physical plausibility assessed based on time scales.'
    }
    
    # Save results
    output_path = project_root / 'data/processed/tep_shear_analysis.json'
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"TEP shear analysis saved to {output_path}")
    print()
    print("=" * 60)
    print("STATUS: TEP shear analysis complete")
    print(f"D/H ratio: {dh_ratio:.2e}")
    print(f"Required time: {required_shear['required_time_years']:.2e} years")
    print(f"Physical plausibility: {'Plausible' if results['physical_plausibility']['plausible'] else 'Implausible'}")
    print("=" * 60)
    
    return results

if __name__ == '__main__':
    analyze_tep_shear_actual()
