# Instrument Differences: UVES vs HIRES

**Date**: 2026-07-06
**Purpose**: Document differences between UVES (VLT) and HIRES (Keck) for TEP-BBN analysis

---

## Overview

The TEP-BBN analysis uses UVES (VLT) data for Q0913+072, while Cooke et al. (2016) used HIRES (Keck) data for their D/H measurements. This document outlines the key differences between these instruments and their implications for TEP-BBN analysis.

---

## Instrument Specifications

### UVES (VLT)
- **Telescope**: Very Large Telescope (VLT), Cerro Paranal, Chile
- **Aperture**: 8.2 m
- **Wavelength range**: 300-1100 nm (varies by configuration)
- **Resolution**: R ~ 40,000-80,000 (varies by slit width)
- **Echelle format**: 2D echelle spectrograph
- **Detector**: Two CCDs (blue and red arms)
- **Typical slit width**: 0.5-1.0 arcsec
- **Typical exposure time**: 1800-5400 s

### HIRES (Keck)
- **Telescope**: W.M. Keck Observatory, Mauna Kea, Hawaii
- **Aperture**: 10 m
- **Wavelength range**: 300-1000 nm (varies by configuration)
- **Resolution**: R ~ 40,000-70,000 (varies by slit width)
- **Echelle format**: 2D echelle spectrograph
- **Detector**: Three CCDs (blue, middle, red arms)
- **Typical slit width**: 0.5-1.0 arcsec
- **Typical exposure time**: 1800-5400 s

---

## Key Differences

### 1. Telescope Aperture
- **UVES**: 8.2 m (VLT)
- **HIRES**: 10 m (Keck)
- **Impact**: HIRES has ~50% more light-gathering power, potentially better S/N for same exposure time

### 2. Wavelength Coverage
- **UVES**: 300-1100 nm (continuous coverage with small gaps)
- **HIRES**: 300-1000 nm (continuous coverage with small gaps)
- **Impact**: UVES has slightly extended red coverage, but both cover Lyman series region

### 3. Resolution
- **UVES**: R ~ 40,000-80,000
- **HIRES**: R ~ 40,000-70,000
- **Impact**: Similar resolution, both sufficient for D/H measurements

### 4. Detector Configuration
- **UVES**: Two CCDs (blue and red arms)
- **HIRES**: Three CCDs (blue, middle, red arms)
- **Impact**: HIRES has better coverage in middle wavelength range

### 5. Site Characteristics
- **UVES**: Cerro Paranal, Chile (altitude 2635 m)
- **HIRES**: Mauna Kea, Hawaii (altitude 4205 m)
- **Impact**: Mauna Kea has better seeing conditions on average, potentially better S/N

---

## Scientific Implications for TEP-BBN

### 1. D/H Measurement Precision
- **Expected difference**: Small (< 5% systematic difference)
- **Reason**: Both instruments have similar resolution and wavelength coverage
- **Mitigation**: Document instrument differences, quantify systematic uncertainties

### 2. Line Profile Fitting
- **Expected difference**: Minimal
- **Reason**: Both instruments produce high-resolution echelle spectra
- **Mitigation**: Use same fitting methodology for both instruments

### 3. Wavelength Calibration
- **Expected difference**: Small (< 0.01 Å)
- **Reason**: Both use ThAr calibration lamps
- **Mitigation**: Verify wavelength calibration accuracy for UVES data

### 4. Signal-to-Noise Ratio
- **Expected difference**: HIRES may have slightly better S/N due to larger aperture
- **Reason**: Keck has 10 m aperture vs VLT 8.2 m
- **Mitigation**: Use longer exposures or co-add multiple UVES exposures

### 5. Continuum Normalization
- **Expected difference**: Minimal
- **Reason**: Both instruments produce high-quality spectra
- **Mitigation**: Use same continuum normalization methodology

---

## TEP-BBN Analysis Considerations

### 1. Scientific Question
- **TEP hypothesis**: Temporal variation of fundamental constants can mimic D/H isotope shift
- **Test**: Compare observed D/H to TEP shear model predictions
- **Instrument relevance**: The scientific question is independent of instrument choice

### 2. Data Quality Requirements
- **Required**: High-resolution echelle spectra (R > 40,000)
- **UVES**: Meets requirements (R ~ 40,000-80,000)
- **HIRES**: Meets requirements (R ~ 40,000-70,000)
- **Conclusion**: Both instruments are suitable for TEP-BBN analysis

### 3. Systematic Uncertainties
- **Instrument systematics**: Quantify and include in error budget
- **Wavelength calibration**: Verify accuracy for UVES data
- **Continuum normalization**: Use consistent methodology
- **Line profile fitting**: Use same fitting code for both instruments

### 4. Reproducibility
- **UVES data**: Publicly available from ESO archive
- **HIRES data**: Requires KOA authentication
- **Advantage**: UVES data is more reproducible (public access)
- **Conclusion**: UVES data is preferable for reproducibility

---

## Quantitative Comparison

### Resolution Comparison
| Parameter | UVES | HIRES |
|-----------|------|-------|
| Resolution (R) | 40,000-80,000 | 40,000-70,000 |
| Velocity resolution (km/s) | 3.75-7.5 | 4.3-7.5 |
| Typical slit width | 0.5-1.0 arcsec | 0.5-1.0 arcsec |

### Wavelength Coverage
| Parameter | UVES | HIRES |
|-----------|------|-------|
| Blue arm | 300-500 nm | 300-500 nm |
| Middle arm | - | 500-600 nm |
| Red arm | 500-1100 nm | 600-1000 nm |
| Lyman series coverage | Yes | Yes |

### Light Gathering Power
| Parameter | UVES | HIRES |
|-----------|------|-------|
| Telescope aperture | 8.2 m | 10 m |
| Collecting area | 52.8 m² | 78.5 m² |
| Relative power | 1.0 | 1.49 |

---

## Recommendations for TEP-BBN Analysis

### 1. Acknowledge Instrument Differences
- **Manuscript**: Clearly state that UVES data is used instead of HIRES
- **Justification**: UVES data is publicly available and reproducible
- **Impact**: Document that both instruments are suitable for TEP-BBN analysis

### 2. Quantify Systematic Uncertainties
- **Wavelength calibration**: Verify accuracy to < 0.01 Å
- **Continuum normalization**: Ensure < 5% residuals
- **Line profile fitting**: Use same methodology for all data
- **Instrument systematics**: Include in error budget

### 3. Use Consistent Methodology
- **Data reduction**: Use standard reduction pipeline (ESO Reflex)
- **Voigt fitting**: Use same fitting code for all data
- **Error analysis**: Include all relevant uncertainties
- **TEP shear model**: Apply consistently to all data

### 4. Validate Results
- **Cross-check**: Compare UVES results to HIRES results if available
- **Internal consistency**: Check consistency across multiple Lyman lines
- **Null tests**: Perform null tests to verify methodology
- **Reproducibility**: Ensure results are reproducible

---

## Conclusion

### Instrument Suitability
- **UVES**: Suitable for TEP-BBN analysis ✅
- **HIRES**: Suitable for TEP-BBN analysis ✅
- **Difference**: Minimal impact on scientific conclusions

### Scientific Validity
- **TEP question**: Independent of instrument choice
- **Data quality**: Both instruments meet requirements
- **Reproducibility**: UVES data is more reproducible (public access)

### Recommendation
Proceed with UVES data for TEP-BBN analysis. Document instrument differences in the manuscript. The scientific question (temporal equivalence principle) can be tested with UVES data just as well as with HIRES data.

---

**Prepared by**: Matthew Lukin Smawfield
**Date**: 2026-07-06
**Status**: Instrument differences documented, ready for analysis
