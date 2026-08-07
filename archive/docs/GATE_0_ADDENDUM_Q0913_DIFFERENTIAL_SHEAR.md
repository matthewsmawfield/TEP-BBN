# Gate 0 Addendum: Q0913+072 Differential Shear Feasibility

**Date**: 2026-07-06
**System**: Q0913+072 (z=2.618)
**Purpose**: Assess whether TEP can produce the required differential temporal shear to mimic deuterium

---

## Executive Summary

The Q0913+072 pipeline run validates the data processing and baseline D/H reconstruction, but has not yet tested the decisive TEP-BBN condition: whether a physically predicted differential temporal-shear field across the DLA can produce ΔlnA ≈ 2.7×10⁻⁴ with the correct sign, while also fitting the full Lyman-series and metal-line structure better than both standard D/H and ordinary H I interloper models.

---

## Key Physical Insight

### Uniform Shift Degeneracy

**Critical Principle**: A uniform temporal shift along the entire light path from z=2.618 to Earth is degenerate with the absorber redshift and does not mimic deuterium.

**Mathematical Statement**:
```
A uniform A(z) shift across the absorber → absorbed into redshift calibration
→ Not observable as deuterium contamination
```

**Requirement**: Only differential temporal shear between absorbing components can mimic isotope structure.

### Differential Shear Requirement

**Gate 0 Condition**: TEP must produce a differential clock-rate contrast across the DLA absorbing structure of:
```
ΔlnA_D/H ≈ 2.7×10⁻⁴
```

**Physical Meaning**: This is the difference in clock-rate normalization between absorbing components inside the DLA system, not the accumulated temporal distance from z=2.618 to Earth.

---

## Feasibility Questions

### 1. DLA Structure Assumptions

**Question**: What DLA length scale, density, column density, or potential gradient is assumed?

**Current Status**: Not yet specified.

**Required Analysis**:
- Characterize the physical structure of Q0913+072 DLA
- Determine typical cloud sizes, densities, and velocity structure
- Identify potential gradients (density, gravitational potential, etc.)
- Map the multi-component structure of the absorbing gas

**Literature Data**: Q0913+072 is a well-studied DLA with known velocity structure. Need to extract:
- Number of velocity components
- Component separation (km/s)
- Column densities per component
- Physical size estimates
- Density estimates

### 2. TEP Shear Law

**Question**: What TEP shear law maps DLA structure to ΔlnA?

**Current Status**: Not yet specified.

**Required Analysis**:
- Define the TEP shear law relating physical quantities to temporal shear
- Specify how density, potential, or other gradients affect clock rates
- Determine the functional form: ΔlnA = f(ρ, Φ, B, ...)
- Establish whether shear depends on local conditions or integrated path

**Candidate Mechanisms**:
- Density-dependent shear: ΔlnA ∝ ρ^α
- Potential-dependent shear: ΔlnA ∝ Φ^β
- Magnetic field-dependent shear: ΔlnA ∝ B^γ
- Gradient-dependent shear: ΔlnA ∝ ∇X

### 3. Predicted ΔlnA Magnitude

**Question**: Does the predicted ΔlnA naturally approach 2.7×10⁻⁴?

**Current Status**: Not yet calculated.

**Required Analysis**:
- Apply TEP shear law to Q0913+072 DLA structure
- Calculate predicted ΔlnA between components
- Compare to required ΔlnA ≈ 2.7×10⁻⁴
- Assess whether the prediction is natural or requires fine-tuning

**Success Criterion**: The predicted ΔlnA should be within an order of magnitude of the required value without parameter fine-tuning.

### 4. Sign Convention

**Question**: Does the shift have the correct sign to mimic deuterium?

**Current Status**: Not yet determined.

**Required Analysis**:
- Determine the sign of the apparent D I isotope displacement relative to H I
- Calculate the sign of predicted TEP shear
- Ensure TEP shear produces the correct direction of shift

**Critical Requirement**: A model that reaches |ΔlnA| ~ 2.7×10⁻⁴ with the wrong sign does not mimic deuterium.

### 5. Differential vs Global

**Question**: Is the shift differential within the absorber, or merely global along the light path?

**Current Status**: Not yet distinguished.

**Required Analysis**:
- Calculate both global and differential shear contributions
- Determine if the shear is primarily differential between components
- Assess if global shift dominates (would be degenerate with redshift)
- Ensure the differential component is sufficient to mimic deuterium

**Critical Requirement**: The differential component must be the dominant effect, not the global accumulated shift.

### 6. Distinguishability from H I Blending

**Question**: Can the TEP model be distinguished from ordinary H I velocity blending?

**Current Status**: Not yet tested.

**Required Analysis**:
- Implement Model M3: H I-only ordinary velocity interloper, no TEP shear
- Compare M1 (TEP shear) to M3 (H I interloper)
- Assess whether TEP provides better fit than ordinary velocity structure
- Test if TEP predictions are distinguishable from H I blending

**Critical Requirement**: If M1 beats M0 but does not beat M3, the result is not TEP evidence—it is just an H I blending explanation.

---

## Model Comparison Framework

### Required Models

| Model | Description | Purpose |
|-------|-------------|---------|
| **M0** | Standard H I + real D I | Baseline standard model |
| **M1** | H I + TEP temporal-shear shifted component | TEP hypothesis test |
| **M2** | Hybrid: real D/H plus temporal-shear nuisance term | Mixed model |
| **M3** | H I-only ordinary velocity interloper, no TEP shear | Alternative explanation |

### Model Comparison Criteria

**Fit Quality**:
- χ² per degree of freedom
- Residual structure across Lyman series
- Metal-line consistency
- Parameter physicality

**Physical Plausibility**:
- TEP shear law consistency
- DLA structure consistency
- Sign and magnitude requirements
- Differential vs global distinction

**Distinguishability**:
- M1 vs M0: Does TEP beat standard D/H?
- M1 vs M3: Does TEP beat H I interloper?
- M1 vs M2: Is pure TEP better than hybrid?

---

## Current Status Assessment

### Pipeline Validation: ✅ Successful

**Achievements**:
- Data ingestion works correctly
- Reduction produces high-quality spectra (S/N = 659.6)
- D/H reconstruction matches literature (2.527×10⁻⁵)
- Atomic data integration functional
- TEP shear model operational

**Status**: The pipeline is validated and ready for TEP-BBN testing.

### TEP-BBN Physical Test: ❌ Not Yet Complete

**Missing Components**:
- DLA structure characterization
- TEP shear law specification
- ΔlnA prediction calculation
- Sign determination
- Differential vs global analysis
- Model comparison (M0, M1, M2, M3)

**Status**: The decisive TEP-BBN condition has not yet been tested.

---

## Required Next Steps

### Immediate Actions

1. **Characterize Q0913+072 DLA Structure**
   - Extract velocity component information from literature
   - Determine physical scales and densities
   - Map potential gradients

2. **Specify TEP Shear Law**
   - Define functional form relating physical quantities to ΔlnA
   - Establish parameter values and ranges
   - Ensure physical consistency

3. **Calculate Predicted ΔlnA**
   - Apply shear law to DLA structure
   - Compute differential shear between components
   - Compare to required 2.7×10⁻⁴

4. **Determine Sign**
   - Calculate sign of predicted shear
   - Compare to required sign for deuterium mimicry
   - Ensure correct direction

5. **Distinguish Differential vs Global**
   - Calculate both contributions
   - Assess relative importance
   - Ensure differential component dominates

6. **Implement Model Comparison**
   - Implement M0, M1, M2, M3
   - Perform comprehensive model comparison
   - Assess distinguishability from H I blending

### Success Criteria

**TEP-BBN Success**:
- Predicted ΔlnA ≈ 2.7×10⁻⁴ (within order of magnitude)
- Correct sign for deuterium mimicry
- Differential shear dominates over global
- M1 beats both M0 and M3
- Physical consistency across all tests

**TEP-BBN Failure**:
- Predicted ΔlnA differs significantly from required
- Wrong sign for deuterium mimicry
- Global shift dominates (degenerate with redshift)
- M1 does not beat M3 (indistinguishable from H I blending)
- Physical inconsistencies

---

## Scientific Interpretation

### Current Status

**Pipeline**: ✅ Validated and functional
**TEP-BBN Test**: ❌ Not yet complete
**Hot Big Bang**: ❌ Not yet affected

### Correct Interpretation

The Q0913+072 run validates the TEP-BBN pipeline against a real high-quality D/H system and reproduces the standard D/H interpretation. The earlier rejection of TEP based on comparison to the ΛCDM universe age was invalid. However, the analysis has not yet tested the decisive TEP-BBN condition: whether a physically predicted differential temporal-shear field across the DLA can produce ΔlnA ≈ 2.7×10⁻⁴ with the correct sign, while also fitting the full Lyman-series and metal-line structure better than both standard D/H and ordinary H I interloper models.

Therefore, the result is a successful pipeline validation, not yet evidence for or against phantom deuterium.

---

## Decision Tree Status

The plan's decision tree remains applicable:

* **If TEP-BBN fails**: TEP keeps screened-limit thermal compatibility
* **If TEP-BBN partially succeeds**: D/H exists but the inferred primordial abundance may be biased
* **If TEP-BBN strongly succeeds**: The hot Big Bang becomes unnecessary and the Hoyle-compatible branch becomes viable

**Current Position**: Before the decision fork. Pipeline validation complete, but TEP-BBN physical test not yet complete.

---

**Prepared by**: Matthew Lukin Smawfield
**Date**: 2026-07-06
**Status**: Pipeline successful; TEP-BBN physical test not yet complete
