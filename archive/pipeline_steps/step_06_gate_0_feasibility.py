"""
Step 06: Gate 0 - Magnitude feasibility test for TEP-BBN

Tests whether TEP shear models can naturally produce the required ΔlnA ~ 2.7×10⁻⁴
across DLA-like environments before building the full spectral fitting pipeline.
"""

import sys
sys.path.insert(0, '../../')
from scripts.utils.isotopic_shift import required_delta_ln_A, deuterium_gate_velocity, temporal_shear_shift
from scripts.utils.dla_analysis import column_density_gradient, shear_from_column_density_gradient
import numpy as np

def magnitude_feasibility_test():
    """
    Test whether TEP shear models can produce the required ΔlnA.
    
    This is Gate 0 - the critical first gate before building the full pipeline.
    """
    print("Step 06: Gate 0 - Magnitude feasibility test")
    print("=" * 60)
    
    # Required target values
    target_delta_ln_A = required_delta_ln_A()
    target_velocity = deuterium_gate_velocity()
    
    print(f"Required ΔlnA: {target_delta_ln_A:.2e}")
    print(f"Required velocity shift: {target_velocity:.1f} km/s")
    print()
    
    # Test with typical DLA parameters
    # Typical DLA: N_HI ~ 10^20 - 10^21 cm^-2, size ~ 1-10 kpc
    n_hi_test = np.logspace(20, 21, 10)  # Column density range
    position_test = np.linspace(0, 10, 10)  # Size range in kpc
    
    # Test T2 shear model (column-density gradient)
    shear_from_gradient = shear_from_column_density_gradient(n_hi_test, position_test)
    
    print("T2 shear model (column-density gradient):")
    print(f"  Max shear: {np.max(shear_from_gradient):.2e}")
    print(f"  Min shear: {np.min(shear_from_gradient):.2e}")
    print(f"  Mean shear: {np.mean(shear_from_gradient):.2e}")
    print()
    
    # Compare to target
    max_shear = np.max(shear_from_gradient)
    
    # Decision gate
    print("Decision gate:")
    if max_shear < 1e-5:
        print("  Result: Natural scale ≪ 10⁻⁴")
        print("  Action: Do not pursue phantom D as main branch. Keep thermal compatibility.")
        verdict = "STOP"
    elif 1e-5 <= max_shear <= 1e-3:
        print("  Result: Natural scale ~ 10⁻⁴")
        print("  Action: Continue to spectral modelling.")
        verdict = "CONTINUE"
    else:
        print("  Result: Natural scale ≫ 10⁻⁴")
        print("  Action: Check whether TEP overpredicts spectral distortions elsewhere.")
        verdict = "CHECK"
    
    print()
    print(f"Gate 0 verdict: {verdict}")
    
    # Save results
    results = {
        'target_delta_ln_A': target_delta_ln_A,
        'target_velocity_kms': target_velocity,
        'max_shear_t2': max_shear,
        'verdict': verdict,
        'test_parameters': {
            'n_hi_range': [float(np.min(n_hi_test)), float(np.max(n_hi_test))],
            'position_range_kpc': [float(np.min(position_test)), float(np.max(position_test))]
        }
    }
    
    import json
    from pathlib import Path
    Path('../../results/outputs').mkdir(parents=True, exist_ok=True)
    
    with open('../../results/outputs/gate_0_magnitude_feasibility.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print("Results saved to results/outputs/gate_0_magnitude_feasibility.json")
    
    return verdict

if __name__ == '__main__':
    magnitude_feasibility_test()
