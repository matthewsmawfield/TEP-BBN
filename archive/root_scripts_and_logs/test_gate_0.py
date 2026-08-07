"""
Test script for Gate 0 magnitude feasibility calculation.
"""

import sys
sys.path.insert(0, '/Users/matthewsmawfield/www/Temporal Equivalence Principle/TEP-BBN')
from scripts.utils.isotopic_shift import required_delta_ln_A, deuterium_gate_velocity, temporal_shear_shift
from scripts.utils.dla_analysis import column_density_gradient, shear_from_column_density_gradient
import numpy as np

print("=" * 60)
print("Gate 0: Magnitude Feasibility Test")
print("=" * 60)
print()

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

print("Test parameters:")
print(f"  N_HI range: {n_hi_test[0]:.2e} - {n_hi_test[-1]:.2e} cm^-2")
print(f"  Position range: {position_test[0]:.1f} - {position_test[-1]:.1f} kpc")
print()

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
print("=" * 60)
