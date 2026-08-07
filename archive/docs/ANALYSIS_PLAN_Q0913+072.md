# TEP-BBN Analysis Plan for Q0913+072

**Date**: 2026-07-06
**System**: Q0913+072 (z=2.618)
**Instrument**: UVES (VLT)
**Program ID**: 68.B-0115

---

## Overview

This analysis plan outlines the step-by-step process for analyzing the UVES data of Q0913+072 to test the Temporal Equivalence Principle (TEP) hypothesis. The analysis will determine whether temporal shear effects can mimic the deuterium isotope shift.

---

## Scientific Objectives

### Primary Objective
Test whether temporal variation of fundamental constants (α and μ) can produce absorption line shifts that mimic the deuterium isotope shift.

### Secondary Objectives
1. Measure D/H ratio from UVES data
2. Compare D/H measurement to TEP shear model predictions
3. Quantify systematic uncertainties
4. Perform null tests to validate methodology

---

## Analysis Workflow

### Phase 1: Data Reduction (Week 1-2)

#### Step 1.1: Reduce UVES Data
**Goal**: Convert raw 2D echelle images to 1D wavelength-calibrated spectra

**Tasks**:
1. Install ESO Reflex software
2. Import 26 UVES FITS files
3. Run UVES reduction recipe
4. Verify output quality (S/N, wavelength calibration)
5. Co-add multiple exposures
6. Save reduced 1D spectrum

**Output**: 
- Reduced 1D spectrum: `data/processed/reduced/Q0913+072_z2.618.fits`
- Reduction metadata: `data/processed/reduction_metadata.json`

**Quality Criteria**:
- S/N > 30 per pixel
- Wavelength calibration accuracy < 0.01 Å
- Continuum normalization residuals < 5%

#### Step 1.2: Validate Reduced Data
**Goal**: Verify reduced data quality and suitability for analysis

**Tasks**:
1. Check Lyman series coverage
2. Verify wavelength range includes Lyα, Lyβ, Lyγ
3. Check for cosmic rays and artifacts
4. Verify continuum normalization
5. Compare to literature values (if available)

**Output**: Validation report

---

### Phase 2: Voigt Profile Fitting (Week 3-4)

#### Step 2.1: Fit H I Lyman Series
**Goal**: Measure H I column density from Lyman series lines

**Tasks**:
1. Identify Lyman series lines in reduced spectrum
2. Fit Voigt profiles to each line
3. Extract column densities
4. Calculate weighted average N(H I)
5. Estimate uncertainties

**Tools**: `core/voigt_fitter.py`

**Output**: 
- H I column density: log N(H I) ± error
- Fitting parameters for each line
- Chi-squared values

**Expected Result**: log N(H I) ≈ 20.52 (from literature)

#### Step 2.2: Fit D I Lyman Series
**Goal**: Measure D I column density from Lyman series lines

**Tasks**:
1. Identify D I Lyman series lines (isotope-shifted)
2. Fit Voigt profiles to each line
3. Extract column densities
4. Calculate weighted average N(D I)
5. Estimate uncertainties

**Tools**: `core/voigt_fitter.py`

**Output**: 
- D I column density: log N(D I) ± error
- Fitting parameters for each line
- Chi-squared values

**Expected Result**: log N(D I) ≈ 14.68 (from literature)

#### Step 2.3: Calculate D/H Ratio
**Goal**: Calculate D/H ratio from column densities

**Tasks**:
1. Calculate D/H = N(D I) / N(H I)
2. Propagate uncertainties
3. Compare to literature value
4. Assess consistency

**Output**: D/H ratio ± error

**Expected Result**: D/H ≈ 2.527 × 10⁻⁵ (from literature)

---

### Phase 3: TEP Shear Model Analysis (Week 5-6)

#### Step 3.1: Initialize TEP Shear Model
**Goal**: Set up TEP shear model with appropriate parameters

**Tasks**:
1. Initialize model with α and μ variation rates
2. Set up time range for analysis
3. Calculate expected Δln(A) for different times
4. Verify model behavior

**Tools**: `core/tep_shear_model.py`

**Output**: Initialized TEP shear model

#### Step 3.2: Apply TEP Shear to Spectrum
**Goal**: Generate sheared spectra for different time periods

**Tasks**:
1. Apply TEP shear model to reduced spectrum
2. Generate sheared spectra for different time periods
3. Calculate wavelength shifts
4. Calculate flux differences

**Tools**: `core/tep_shear_model.py`

**Output**: 
- Sheared spectra for different time periods
- Wavelength shift vs time
- Flux difference vs time

#### Step 3.3: Compare Shear to Deuterium
**Goal**: Determine if TEP shear can mimic D/H isotope shift

**Tasks**:
1. Calculate required shear to mimic observed D/H
2. Calculate required time for this shear
3. Compare to cosmological time scales
4. Assess physical plausibility

**Tools**: `core/tep_shear_model.py`

**Output**: 
- Required shear factor
- Required time
- Physical plausibility assessment

---

### Phase 4: Null Tests (Week 7)

#### Step 4.1: Metal-Line Coherence Test
**Goal**: Verify that metal lines are not affected by TEP shear

**Tasks**:
1. Fit metal lines (O I, Si II, C II, Fe II)
2. Check for systematic shifts
3. Verify consistency with no shear
4. Quantify any discrepancies

**Tools**: `core/voigt_fitter.py`

**Output**: Metal line analysis results

#### Step 4.2: Multi-Lyman Consistency Test
**Goal**: Verify consistency across multiple Lyman lines

**Tasks**:
1. Compare D/H measurements from different Lyman lines
2. Check for systematic trends
3. Verify consistency with no shear
4. Quantify any discrepancies

**Tools**: `core/voigt_fitter.py`

**Output**: Multi-Lyman consistency analysis

#### Step 4.3: Environmental Correlation Test
**Goal**: Check for correlation with environmental parameters

**Tasks**:
1. Correlate D/H with N(H I)
2. Correlate D/H with metallicity
3. Check for expected TEP shear correlations
4. Assess significance

**Output**: Environmental correlation analysis

---

### Phase 5: Statistical Analysis (Week 8)

#### Step 5.1: Bayesian Model Comparison
**Goal**: Compare TEP shear model to standard D/H model

**Tasks**:
1. Define likelihood functions for both models
2. Calculate Bayesian evidence for each model
3. Compute Bayes factor
4. Assess model preference

**Tools**: dynesty, emcee

**Output**: 
- Bayesian evidence for TEP model
- Bayesian evidence for standard model
- Bayes factor

#### Step 5.2: Parameter Estimation
**Goal**: Estimate TEP shear parameters (α and μ variation rates)

**Tasks**:
1. Define parameter priors
2. Perform MCMC sampling
3. Extract posterior distributions
4. Calculate credible intervals

**Tools**: dynesty, emcee

**Output**: 
- Posterior distributions for α and μ variation rates
- Credible intervals
- Correlation plots

#### Step 5.3: Sensitivity Analysis
**Goal**: Assess sensitivity to different assumptions

**Tasks**:
1. Test different priors
2. Test different fitting methodologies
3. Test different systematic error models
4. Quantify impact on results

**Output**: Sensitivity analysis results

---

### Phase 6: Results and Interpretation (Week 9)

#### Step 6.1: Compile Results
**Goal**: Compile all analysis results

**Tasks**:
1. Compile D/H measurement
2. Compile TEP shear model results
3. Compile null test results
4. Compile statistical analysis results

**Output**: Comprehensive results summary

#### Step 6.2: Interpret Results
**Goal**: Interpret results in context of TEP hypothesis

**Tasks**:
1. Assess whether TEP shear can mimic D/H
2. Evaluate physical plausibility
3. Compare to literature
4. Discuss implications

**Output**: Scientific interpretation

#### Step 6.3: Document Uncertainties
**Goal**: Document all sources of uncertainty

**Tasks**:
1. Statistical uncertainties
2. Systematic uncertainties
3. Instrument systematics
4. Model uncertainties

**Output**: Uncertainty budget

---

## Timeline Summary

| Phase | Duration | Key Deliverables |
|-------|----------|-----------------|
| Phase 1: Data Reduction | 2 weeks | Reduced 1D spectrum |
| Phase 2: Voigt Fitting | 2 weeks | D/H measurement |
| Phase 3: TEP Shear Model | 2 weeks | Shear model analysis |
| Phase 4: Null Tests | 1 week | Null test results |
| Phase 5: Statistical Analysis | 1 week | Bayesian comparison |
| Phase 6: Results | 1 week | Final interpretation |

**Total**: 9 weeks

---

## Required Resources

### Software
- ESO Reflex (data reduction)
- Python 3.9+ (analysis)
- Scientific libraries: numpy, scipy, astropy, dynesty, emcee
- Custom code: voigt_fitter.py, tep_shear_model.py

### Hardware
- Computer with 8+ GB RAM
- Disk space: ~2 GB for data and analysis
- CPU: Modern processor (Intel i5 or equivalent)

### Expertise
- Spectroscopic data reduction (intermediate)
- Voigt profile fitting (intermediate)
- Bayesian inference (intermediate)
- Python programming (intermediate)

---

## Success Criteria

### Data Reduction
- ✅ Reduced spectrum with S/N > 30
- ✅ Wavelength calibration accuracy < 0.01 Å
- ✅ Continuum normalization residuals < 5%

### Voigt Fitting
- ✅ Successful Voigt fits to Lyman series
- ✅ D/H measurement consistent with literature (within 10%)
- ✅ Reasonable chi-squared values

### TEP Shear Model
- ✅ Quantitative comparison to D/H measurement
- ✅ Assessment of physical plausibility
- ✅ Required time calculation

### Null Tests
- ✅ Metal lines show no systematic shifts
- ✅ Multi-Lyman consistency verified
- ✅ No environmental correlations

### Statistical Analysis
- ✅ Bayesian model comparison completed
- ✅ Parameter estimation completed
- ✅ Sensitivity analysis completed

---

## Risk Mitigation

### Risk 1: Data Reduction Issues
**Mitigation**: Use ESO Reflex (official ESO software), verify output quality, consult ESO documentation

### Risk 2: Voigt Fitting Failures
**Mitigation**: Use robust fitting algorithms, verify initial parameters, check for degeneracies

### Risk 3: TEP Model Implementation Errors
**Mitigation**: Verify model behavior with test cases, compare to literature, cross-check calculations

### Risk 4: Null Test Failures
**Mitigation**: Document discrepancies, investigate causes, assess impact on conclusions

### Risk 5: Statistical Analysis Issues
**Mitigation**: Use well-tested libraries (dynesty, emcee), verify convergence, perform sensitivity analysis

---

## Expected Outcomes

### Scenario 1: TEP Shear Cannot Mimic D/H
- **Result**: Required time for shear is physically implausible
- **Conclusion**: Standard D/H interpretation is correct
- **Implication**: No evidence for temporal variation of fundamental constants

### Scenario 2: TEP Shear Can Mimic D/H
- **Result**: Required time for shear is physically plausible
- **Conclusion**: TEP hypothesis is viable
- **Implication**: Temporal variation of fundamental constants may explain D/H measurements

### Scenario 3: Inconclusive Results
- **Result**: Evidence is mixed or ambiguous
- **Conclusion**: More data needed
- **Implication**: Need additional systems or higher S/N data

---

## Documentation

### Required Documentation
1. Data reduction process and parameters
2. Voigt fitting methodology and results
3. TEP shear model parameters and assumptions
4. Null test procedures and results
5. Statistical analysis methods and results
6. Complete uncertainty budget

### Deliverables
1. Reduced spectrum (FITS format)
2. D/H measurement with uncertainties
3. TEP shear model analysis results
4. Null test results
5. Bayesian model comparison results
6. Comprehensive analysis report

---

## Next Steps

1. **Begin data reduction**: Install ESO Reflex and reduce UVES data
2. **Validate results**: Verify reduced data quality
3. **Proceed with analysis**: Follow analysis workflow
4. **Document progress**: Update analysis plan as needed
5. **Prepare manuscript**: Document results for publication

---

**Prepared by**: Matthew Lukin Smawfield
**Date**: 2026-07-06
**Status**: Analysis plan complete, ready for execution
