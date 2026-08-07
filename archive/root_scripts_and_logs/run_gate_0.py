"""
Gate 0: Magnitude Feasibility Test Results

This document contains the magnitude feasibility calculation for TEP-BBN.
"""

# Required target values
# Δv_D/H ≃ 82 km/s
# ΔlnA ≃ Δv/c ≃ 82 / 299792 ≃ 2.7×10⁻⁴

target_delta_ln_A = 2.7e-4
target_velocity = 82.0  # km/s

print("=" * 60)
print("Gate 0: Magnitude Feasibility Test")
print("=" * 60)
print()
print(f"Required ΔlnA: {target_delta_ln_A:.2e}")
print(f"Required velocity shift: {target_velocity:.1f} km/s")
print()

# Test with typical DLA parameters
# Typical DLA: N_HI ~ 10^20 - 10^21 cm^-2, size ~ 1-10 kpc
import numpy as np

n_hi_test = np.logspace(20, 21, 10)  # Column density range
position_test = np.linspace(0, 10, 10)  # Size range in kpc

print("Test parameters:")
print(f"  N_HI range: {n_hi_test[0]:.2e} - {n_hi_test[-1]:.2e} cm^-2")
print(f"  Position range: {position_test[0]:.1f} - {position_test[-1]:.1f} kpc")
print()

# Calculate column density gradient
gradient = np.gradient(n_hi_test, position_test)

# T2 shear model: shear proportional to column-density gradient
# Using normalization factor of 1e-4 (this is a placeholder)
normalization = 1e-4
shear_from_gradient = normalization * np.abs(gradient)

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

# Save results
results = {
    'target_delta_ln_A': target_delta_ln_A,
    'target_velocity_kms': target_velocity,
    'max_shear_t2': float(max_shear),
    'verdict': verdict,
    'test_parameters': {
        'n_hi_range': [float(np.min(n_hi_test)), float(np.max(n_hi_test))],
        'position_range_kpc': [float(np.min(position_test)), float(np.max(position_test))]
    }
}

import json
from pathlib import Path
Path('/Users/matthewsmawfield/www/Temporal Equivalence Principle/TEP-BBN/results/outputs').mkdir(parents=True, exist_ok=True)

with open('/Users/matthewsmawfield/www/Temporal Equivalence Principle/TEP-BBN/results/outputs/gate_0_magnitude_feasibility.json', 'w') as f:
    json.dump(results, f, indent=2)

print("Results saved to results/outputs/gate_0_magnitude_feasibility.json")
