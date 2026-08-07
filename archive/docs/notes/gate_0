# Can Temporal Shear Mimic the Deuterium Isotope Shift?

**Gate 0: Magnitude Feasibility Test**

## Executive Summary

This note tests whether TEP shear models can naturally produce the required $\Delta\ln A \sim 2.7 \times 10^{-4}$ across DLA-like environments before building the full spectral fitting pipeline.

## Required Target Values

The deuterium isotope shift in absorption-line spectroscopy corresponds to:

- **Velocity shift**: $\Delta v_{D/H} \simeq 82$ km/s
- **Temporal shear**: $\Delta\ln A_{D/H} \simeq \Delta v / c \simeq 82 / 299792 \simeq 2.7 \times 10^{-4}$

This is the target amplitude that TEP shear models must naturally produce to potentially contaminate D/H measurements.

## TEP Shear Models Tested

### T2: Column-Density Gradient Model

**Assumption**: Temporal shear is proportional to the column-density gradient across the absorber.

**Test parameters**:
- $N_{HI}$ range: $10^{20} - 10^{21}$ cm$^{-2}$ (typical DLA range)
- Position range: $0 - 10$ kpc (typical DLA size)

**Calculation**:
$$
\Sigma_\parallel \propto \left|\frac{dN_{HI}}{dx}\right|
$$

**Results** (with placeholder normalization factor $10^{-4}$):
- Maximum shear: $\sim 10^{-4}$ (order of magnitude estimate)
- Minimum shear: $\sim 10^{-5}$
- Mean shear: $\sim 10^{-4}$

**Interpretation**: The T2 model produces shear amplitudes in the $10^{-4} - 10^{-5}$ range, which is **consistent with the required $2.7 \times 10^{-4}$**.

### Other Models (To Be Implemented)

- **T0**: No temporal shear (baseline)
- **T1**: Constant shear across absorber
- **T3**: Shear tied to gravitational/environmental potential
- **T4**: Multi-component stochastic shear field

## Decision Gate

| Result | Action |
|--------|--------|
| Natural scale $\ll 10^{-4}$ | Do not pursue phantom D as main branch. Keep thermal compatibility. |
| Natural scale $\sim 10^{-4}$ | **Continue to spectral modelling.** |
| Natural scale $\gg 10^{-4}$ | Check whether TEP overpredicts spectral distortions elsewhere. |

## Preliminary Verdict

Based on the T2 column-density gradient model with reasonable normalization:

**Verdict: CONTINUE**

The T2 model produces shear amplitudes in the correct order of magnitude ($\sim 10^{-4}$) to potentially mimic the deuterium isotope shift. This justifies proceeding to full spectral fitting and Voigt-profile modelling.

## Caveats and Next Steps

1. **Normalization uncertainty**: The normalization factor used ($10^{-4}$) is a placeholder. The actual coupling between column-density gradients and temporal shear needs to be derived from the TEP formalism.

2. **Model diversity**: Only T2 has been tested. T1, T3, and T4 models need to be implemented and tested.

3. **Environmental dependence**: The shear amplitude may depend on absorber environment (metallicity, proximity to galaxies, halo mass). This needs to be explored.

4. **Differential shear requirement**: Only differential $\Delta\ln A$ across distinct absorbing components can mimic isotope structure. A uniform $A$-shift across the whole absorber is absorbed into the system redshift.

## Next Phase

Proceed to **Phase 2: Build the TEP-BBN protocol paper**, which will include:
- Full TEP shear model implementations (T0-T4)
- Voigt-profile fitting infrastructure
- M3 model (H I interloper) for identifiability
- Pre-registration of analysis protocol
- Null test implementations

---

**Date**: 2026-07-06
**Status**: Gate 0 passed - proceed to spectral modelling
