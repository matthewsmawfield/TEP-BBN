"""
ESO Reflex Data Reduction Guide for TEP-BBN

This guide provides step-by-step instructions for reducing UVES data
using ESO Reflex, with validation scripts to check output quality.
"""

import json
from pathlib import Path
from datetime import datetime

def create_reduction_guide():
    """
    Create a comprehensive data reduction guide.
    """
    
    guide = """
# ESO Reflex Data Reduction Guide for TEP-BBN

## Overview

This guide provides step-by-step instructions for reducing UVES data from 
raw 2D echelle images to 1D wavelength-calibrated spectra using ESO Reflex.

## Prerequisites

### Software Installation

1. Download ESO Reflex from: https://www.eso.org/sci/software/reflex/
2. Install Java Runtime Environment (JRE) 8 or higher
3. Follow ESO Reflex installation instructions for your platform
4. Verify installation by running: `reflex`

### Data Preparation

Raw data location: `data/raw/spectra/Q0913+072_z2.618/`
- 26 UVES FITS files
- Total size: ~147 MB

## Step-by-Step Reduction Process

### Step 1: Launch ESO Reflex

```bash
# Launch ESO Reflex
reflex
```

### Step 2: Create New Workflow

1. Click "File" → "New Workflow"
2. Name workflow: "TEP_BBN_Q0913_072"
3. Click "Create"

### Step 3: Add UVES Recipe

1. Click "Add" → "Recipe"
2. Search for "UVES"
3. Select "UVES Reflex recipe (v2.9.1)" or latest version
4. Click "Add"

### Step 4: Import Data

1. Click "Add" → "Data"
2. Navigate to: `data/raw/spectra/Q0913+072_z2.618/`
3. Select all 26 FITS files
4. Click "Add"

### Step 5: Configure Recipe Parameters

#### Basic Parameters
- **Instrument**: UVES
- **Mode**: Standard
- **Reduction**: Science

#### Calibration
- **Bias subtraction**: Yes
- **Flat field**: Yes
- **Wavelength calibration**: ThAr
- **Extraction**: Optimal

#### Output
- **Format**: FITS
- **Wavelength scale**: Linear
- **Flux calibration**: Yes (if standard stars available)
- **Continuum normalization**: Yes

### Step 6: Run Reduction

1. Click "Run" → "Execute Workflow"
2. Wait for reduction to complete (may take 10-30 minutes)
3. Monitor progress in the console

### Step 7: Validate Output

ESO Reflex will output reduced 1D spectra in the output directory.

Expected output:
- 1D wavelength-calibrated spectra
- Wavelength range: ~3450-6648 Å
- Format: FITS files
- Quality: S/N > 30 per pixel

### Step 8: Save Reduced Data

1. Navigate to output directory
2. Copy reduced FITS files to: `data/processed/reduced/Q0913+072_z2.618/`
3. Verify file integrity

## Quality Validation

After reduction, run the validation script:

```bash
python scripts/steps/step_06_data_reduction.py
```

This will:
- Check for reduced data files
- Validate file formats
- Calculate checksums
- Update reduction metadata

## Troubleshooting

### Common Issues

1. **ESO Reflex won't launch**
   - Check Java installation
   - Verify ESO Reflex installation
   - Check system requirements

2. **Data import fails**
   - Verify FITS file paths
   - Check file permissions
   - Ensure files are not corrupted

3. **Reduction fails**
   - Check recipe parameters
   - Verify calibration frames are available
   - Check for missing files

4. **Output quality poor**
   - Verify S/N > 30
   - Check wavelength calibration
   - Verify continuum normalization

## Expected Results

After successful reduction:
- Reduced 1D spectrum: `data/processed/reduced/Q0913+072_z2.618/`
- Wavelength range: ~3450-6648 Å
- Resolution: R ~ 40,000-60,000
- S/N: > 30 per pixel
- Wavelength accuracy: < 0.01 Å
- Continuum residuals: < 5%

## Next Steps

After successful data reduction:

1. Run step 07: Voigt fitting
   ```bash
   python scripts/steps/step_07_voigt_fitting.py
   ```

2. Run step 08: TEP shear analysis
   ```bash
   python scripts/steps/step_08_tep_shear_analysis.py
   ```

## References

- ESO Reflex User Manual: https://www.eso.org/sci/software/reflex/
- UVES Data Reduction Guide: https://www.eso.org/sci/facilities/paranal/instruments/uves/doc/
- UVES Pipeline Manual: https://www.eso.org/sci/software/pipelines/

## Support

For issues with ESO Reflex:
- ESO User Support: https://support.eso.org/
- ESO Reflex Forum: https://forum.eso.org/

For issues with TEP-BBN pipeline:
- Check documentation in: `DOCUMENTATION/`
- Run validation scripts
- Check logs in: `logs/`
"""
    
    # Save guide
    guide_path = 'DOCUMENTATION/ESO_REFLEX_REDUCTION_GUIDE.md'
    Path('DOCUMENTATION').mkdir(parents=True, exist_ok=True)
    
    with open(guide_path, 'w') as f:
        f.write(guide)
    
    print(f"ESO Reflex reduction guide saved to {guide_path}")
    print()
    print("Next steps:")
    print("1. Install ESO Reflex")
    print("2. Follow the guide to reduce UVES data")
    print("3. Run validation script to check output")
    print("4. Proceed with steps 07 and 08")

if __name__ == '__main__':
    create_reduction_guide()
