# UVES Data Reduction Process for TEP-BBN

**Date**: 2026-07-06
**System**: Q0913+072 (z=2.618)
**Instrument**: UVES (VLT)
**Program ID**: 68.B-0115

---

## Overview

The downloaded UVES data are raw 2D echelle images that require reduction to 1D spectra before scientific analysis. This document outlines the recommended reduction process for TEP-BBN.

---

## Data Characteristics

### Raw Data Format
- **Type**: 2D echelle images (FITS format)
- **Files**: 26 FITS files
- **Total size**: 146.9 MB
- **Observation dates**: January-March 2002
- **Exposure times**: Various (10s to 4800s)

### Data Structure
- **Format**: Echelle spectroscopy data
- **Dimensions**: 2D detector images
- **Content**: Raw detector counts, wavelength calibration frames, flat fields
- **Status**: Requires reduction to extract 1D spectra

---

## Recommended Reduction Software

### Option 1: ESO Reflex (Recommended)
**Software**: ESO Reflex (ESO Recipe Execution Tool)
**Website**: https://www.eso.org/sci/software/reflex/
**Advantages**:
- Official ESO software for UVES data reduction
- Automated recipes for UVES
- Well-documented and maintained
- Produces high-quality 1D spectra

**Installation**:
```bash
# Download from ESO website
# Requires Java runtime environment
# Follow installation instructions on ESO website
```

**Usage**:
1. Import UVES data into ESO Reflex
2. Select UVES reduction recipe
3. Execute reduction pipeline
4. Output: 1D wavelength-calibrated spectra

### Option 2: IRAF
**Software**: IRAF (Image Reduction and Analysis Facility)
**Website**: https://iraf.noao.edu/
**Advantages**:
- Widely used in astronomy
- Flexible and customizable
- Extensive documentation

**Installation**:
```bash
# Download from NOAO website
# Requires Linux/Unix environment
# Follow installation instructions
```

**Usage**:
1. Use `echelle` package for echelle data reduction
2. Calibrate wavelength solution
3. Extract 1D spectra
4. Flux calibration

### Option 3: Custom Python Pipeline
**Software**: Python with astropy, specutils
**Advantages**:
- Fully customizable
- Reproducible
- Integrates with TEP-BBN pipeline

**Libraries**:
```python
import astropy.io.fits as fits
from astropy.wcs import WCS
import numpy as np
```

---

## Reduction Steps

### Step 1: Bias Subtraction
**Purpose**: Remove detector bias level
**Method**: Subtract master bias frame from science frames
**Input**: Raw science frames, bias frames
**Output**: Bias-subtracted frames

### Step 2: Flat Field Correction
**Purpose**: Correct for pixel-to-pixel sensitivity variations
**Method**: Divide by normalized flat field
**Input**: Bias-subtracted frames, flat field frames
**Output**: Flat-field corrected frames

### Step 3: Order Tracing
**Purpose**: Identify echelle orders on detector
**Method**: Trace order positions across detector
**Input**: Flat-field corrected frames
**Output**: Order tracing information

### Step 4: Wavelength Calibration
**Purpose**: Convert pixel coordinates to wavelengths
**Method**: Use ThAr calibration frames
**Input**: Calibration frames, order tracing
**Output**: Wavelength solution for each order

### Step 5: Extraction
**Purpose**: Extract 1D spectra from 2D echelle images
**Method**: Sum flux along spatial direction for each order
**Input**: Calibrated 2D frames, wavelength solution
**Output**: 1D spectra per order

### Step 6: Order Merging
**Purpose**: Merge echelle orders into continuous spectrum
**Method**: Stitch orders with appropriate overlap
**Input**: 1D spectra per order
**Output**: Continuous 1D spectrum

### Step 7: Flux Calibration
**Purpose**: Convert counts to physical flux units
**Method**: Use standard star observations
**Input**: 1D spectrum, standard star data
**Output**: Flux-calibrated spectrum

### Step 8: Continuum Normalization
**Purpose**: Normalize continuum to unity
**Method**: Fit continuum and divide
**Input**: Flux-calibrated spectrum
**Output**: Continuum-normalized spectrum

### Step 9: Co-addition
**Purpose**: Combine multiple exposures
**Method**: Weighted average or median combination
**Input**: Multiple reduced spectra
**Output**: Co-added final spectrum

---

## Expected Output

### Reduced Spectrum Format
- **Format**: 1D spectrum (FITS or ASCII)
- **Columns**: Wavelength (Å), Flux, Error (optional)
- **Wavelength range**: ~3450-6648 Å (UVES coverage)
- **Resolution**: R ~ 40,000-60,000 (UVES)
- **Units**: Flux (erg/s/cm²/Å) or normalized flux

### Data Quality Indicators
- **Signal-to-noise ratio**: Target S/N > 30 per pixel
- **Wavelength calibration accuracy**: < 0.01 Å
- **Continuum normalization**: Unity with < 5% residuals
- **Cosmic ray removal**: Cleaned spectrum

---

## Integration with TEP-BBN Pipeline

### Step 06: Data Reduction
**File**: `scripts/steps/step_06_data_reduction.py`

**Purpose**: Reduce raw UVES data to 1D spectra

**Input**: 
- Raw FITS files: `data/raw/spectra/Q0913+072_z2.618/`
- Calibration frames: Included in raw data

**Output**:
- Reduced 1D spectra: `data/processed/reduced/Q0913+072_z2.618/`
- Reduction metadata: `data/processed/reduction_metadata.json`

**Implementation Options**:
1. **ESO Reflex integration**: Call ESO Reflex from Python
2. **Custom Python pipeline**: Implement reduction in Python
3. **Manual reduction**: Document manual reduction process

**Recommended**: ESO Reflex integration for reliability and reproducibility

---

## Provenance Tracking

### Reduction Metadata
```json
{
  "reduction_date": "2026-07-06",
  "reduction_software": "ESO Reflex",
  "reduction_version": "2.12.0",
  "reduction_parameters": {
    "bias_subtraction": true,
    "flat_field_correction": true,
    "wavelength_calibration": "ThAr",
    "extraction_method": "optimal",
    "flux_calibration": true,
    "continuum_normalization": true
  },
  "input_files": ["UVES.2002-02-14T04:09:54.782.fits", ...],
  "output_files": ["Q0913+072_z2.618_reduced.fits"],
  "quality_metrics": {
    "snr": 45,
    "wavelength_accuracy": 0.008,
    "continuum_residuals": 0.03
  }
}
```

---

## Timeline and Resources

### Estimated Time
- **ESO Reflex reduction**: 2-4 hours (including setup)
- **Custom Python pipeline**: 1-2 weeks (development time)
- **Manual reduction**: 4-8 hours (if experienced)

### Required Resources
- **Disk space**: ~500 MB for reduced data
- **Memory**: 4-8 GB RAM
- **Processing**: Modern CPU (Intel i5 or equivalent)

### Expertise Level
- **ESO Reflex**: Beginner to intermediate
- **IRAF**: Intermediate to advanced
- **Custom Python**: Advanced (requires programming experience)

---

## Troubleshooting

### Common Issues

1. **Wavelength calibration errors**
   - Check ThAr frame quality
   - Verify calibration lamp lines
   - Re-run wavelength calibration

2. **Order tracing failures**
   - Check flat field quality
   - Verify order positions
   - Manual order tracing if needed

3. **Flux calibration issues**
   - Verify standard star observations
   - Check atmospheric extinction correction
   - Use alternative standard stars

4. **Continuum normalization problems**
   - Check for absorption features
   - Use appropriate continuum regions
   - Manual continuum fitting if needed

---

## References

### ESO Documentation
- ESO Reflex User Manual: https://www.eso.org/sci/software/reflex/
- UVES Data Reduction Guide: https://www.eso.org/sci/facilities/paranal/instruments/uves/doc/
- UVES Pipeline Manual: https://www.eso.org/sci/software/pipelines/

### Scientific References
- Dekker et al. (2000): UVES instrument paper
- Ballester et al. (2000): UVES performance and calibration
- UVES calibration handbook

---

## Next Steps

1. **Choose reduction software**: ESO Reflex (recommended)
2. **Install software**: Follow installation instructions
3. **Reduce data**: Follow reduction steps
4. **Validate output**: Check quality metrics
5. **Integrate with pipeline**: Update step_06 with reduced data
6. **Proceed to Voigt fitting**: Use reduced spectra for analysis

---

**Prepared by**: Matthew Lukin Smawfield
**Date**: 2026-07-06
**Status**: Documentation complete, ready for reduction
