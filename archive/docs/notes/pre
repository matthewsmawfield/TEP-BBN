# TEP-BBN Pre-Registration Protocol

**Date**: 2026-07-06
**Status**: Pre-registered (to be finalized before data analysis)
**Purpose**: Prevent after-the-fit tuning and ensure reproducibility

---

## 1. System Selection Criteria

### 1.1 Redshift Range
- **Target**: $2.0 < z < 3.5$
- **Rationale**: High-quality D/H systems are typically found in this range
- **Exclusion**: Systems outside this range will not be included

### 1.2 Signal-to-Noise Threshold
- **Target**: S/N > 30 per pixel in Lyman series
- **Rationale**: High S/N required for precise D/H measurement
- **Exclusion**: Systems with S/N < 30 will be excluded

### 1.3 Instrument Requirements
- **Accepted instruments**: Keck/HIRES, VLT/UVES, Subaru/HDS
- **Rationale**: High-resolution spectrographs with well-understood calibration
- **Exclusion**: Lower-resolution instruments will not be used

### 1.4 Continuum Quality Standards
- **Target**: Continuum placement uncertainty < 1%
- **Rationale**: Continuum errors can bias D/H measurements
- **Exclusion**: Systems with poor continuum regions will be excluded

### 1.5 Exclusion Rules
- **Metal-line contamination**: Systems with strong metal-line blending near D I will be excluded
- **Damped Lyman-alpha limit**: Only systems with $N_{HI} > 10^{20}$ cm$^{-2}$
- **Multiple components**: Systems with > 5 velocity components may be excluded due to complexity
- **Known systematics**: Systems with known instrumental or calibration issues will be excluded

---

## 2. Model Definitions

### 2.1 M0: Standard H I + D I Voigt Model
```python
parameters = {
    'hi_center': float,           # H I line center (km/s)
    'hi_fwhm': float,             # H I line width (km/s)
    'hi_shape': float,            # H I Voigt shape parameter
    'hi_column_density': float,   # H I column density (cm^-2)
    'di_center': float,           # D I line center (km/s)
    'di_fwhm': float,             # D I line width (km/s)
    'di_shape': float,            # D I Voigt shape parameter
    'di_column_density': float    # D I column density (cm^-2)
}
```

### 2.2 M1: Temporal-Shear Model (Phantom D)
```python
parameters = {
    'hi_center': float,
    'hi_fwhm': float,
    'hi_shape': float,
    'hi_column_density': float,
    'shear_delta_ln_A': float,    # Temporal shear amplitude
    'shear_fwhm': float,
    'shear_shape': float,
    'shear_column_density': float
}
```

### 2.3 M2: Hybrid Model (Real D + Temporal Shear)
```python
parameters = {
    'hi_center': float,
    'hi_fwhm': float,
    'hi_shape': float,
    'hi_column_density': float,
    'di_center': float,
    'di_fwhm': float,
    'di_shape': float,
    'di_column_density': float,
    'shear_delta_ln_A': float,
    'shear_fwhm': float,
    'shear_shape': float,
    'shear_column_density': float
}
```

### 2.4 M3: H I Interloper Model (Velocity Blending)
```python
parameters = {
    'hi_primary_center': float,
    'hi_primary_fwhm': float,
    'hi_primary_shape': float,
    'hi_primary_column_density': float,
    'hi_interloper_center': float,    # Velocity-shifted H I
    'hi_interloper_fwhm': float,
    'hi_interloper_shape': float,
    'hi_interloper_column_density': float
}
```

---

## 3. Priors

### 3.1 Line Centers
- **H I center**: Uniform over ±50 km/s around absorber redshift
- **D I center**: Uniform over ±100 km/s around H I center (for M0, M2)
- **Shear center**: Fixed by H I center + temporal-shear shift (for M1, M2)
- **Interloper center**: Uniform over ±100 km/s around H I center (for M3)

### 3.2 Line Widths
- **H I FWHM**: Uniform 5-30 km/s
- **D I FWHM**: Uniform 5-30 km/s
- **Shear FWHM**: Uniform 5-30 km/s
- **Interloper FWHM**: Uniform 5-30 km/s

### 3.3 Shape Parameters
- **All shapes**: Uniform 0.01-0.5

### 3.4 Column Densities
- **H I**: Log-uniform $10^{19} - 10^{22}$ cm$^{-2}$
- **D I**: Log-uniform $10^{13} - 10^{16}$ cm$^{-2}$
- **Shear component**: Log-uniform $10^{13} - 10^{16}$ cm$^{-2}$
- **Interloper**: Log-uniform $10^{13} - 10^{16}$ cm$^{-2}$

### 3.5 Temporal-Shear Amplitude (M1, M2)
- **ΔlnA**: Fixed from Gate 0 feasibility calculation
- **No post-hoc tuning**: Amplitude must be set before fitting begins

---

## 4. Fitting Ranges

### 4.1 Wavelength/Velocity Range
- **Range**: ±200 km/s around absorber redshift
- **Rationale**: Sufficient to capture full absorption profile

### 4.2 Convergence Criteria
- **dynesty**: dlogz < 0.01 for 100 iterations
- **Maximum iterations**: 10,000
- **Minimum live points**: 500

---

## 5. Evidence Thresholds

### 5.1 Model Comparison Decision Rules
| ΔlnZ | Interpretation | Action |
|-----|----------------|--------|
| ΔlnZ < 0 | Model rejected | Do not pursue this model for this system |
| 0 < ΔlnZ < 2 | Inconclusive | No strong evidence either way |
| 2 < ΔlnZ < 5 | Worth investigation | Model shows promise, but not decisive |
| ΔlnZ > 5 | Serious evidence | Strong evidence for this model |

### 5.2 Claim Gates
- **Gate -1 (Identifiability)**: Temporal shear must be distinguishable from velocity blending
- **Gate 0 (Magnitude)**: ΔlnA must be naturally ~10⁻⁴ (already passed)
- **Gate 1 (One-system)**: M1/M2 must beat M0/M3 in one clean absorber
- **Gate 2 (Multi-system)**: Effect must repeat across systems with environmental structure

---

## 6. Null Test Protocols

### 6.1 Null Test A: Metal-Line Coherence
- **Threshold**: Correlation coefficient > 0.5 between H I and metal-line residuals
- **Significance**: p < 0.05
- **Failure**: If metal lines do not show expected shear pattern, temporal-shear model rejected

### 6.2 Null Test B: Multi-Lyman Consistency
- **Requirement**: Same model must fit Lyα, Lyβ, Lyγ simultaneously
- **Threshold**: Reduced χ² < 2 for all three lines
- **Failure**: If model only fits one line, temporal-shear model rejected

### 6.3 Null Test C: Environmental Correlation
- **Parameters**: N_HI, metallicity, velocity width, n_components, proximity to galaxies
- **Threshold**: Correlation coefficient > 0.3 with at least one environmental parameter
- **Significance**: p < 0.05
- **Failure**: If no environmental correlation, temporal-shear model weakened

### 6.4 Null Test D: Component Asymmetry
- **Metric**: Ratio of shear component on left vs right side of velocity structure
- **Threshold**: Asymmetry ratio > 1.5 or < 0.67
- **Failure**: If no asymmetry, temporal-shear model weakened

### 6.5 Null Test E: Blind Injection
- **Success rate**: > 80% correct model identification
- **Test cases**: 100 synthetic spectra (50 with D, 50 without)
- **Failure**: If success rate < 80%, pipeline needs debugging

---

## 7. Exclusion Rules

### 7.1 System Exclusion
- **Failed null tests**: Systems failing > 2 null tests will be excluded
- **Poor fit quality**: Systems with reduced χ² > 3 for all models will be excluded
- **Convergence failure**: Systems where dynesty fails to converge will be excluded

### 7.2 Component Exclusion
- **Unphysical parameters**: Components with negative column densities will be excluded
- **Outlier widths**: Components with FWHM > 100 km/s will be flagged for review

---

## 8. Spectral-Only Likelihood Rule

**Critical**: No BBN-predicted abundance prior is allowed in the main evidence comparison.

- **Rationale**: The whole point of TEP-BBN is to test spectroscopic inference
- **Implementation**: D/H priors must be spectral-only, not informed by BBN predictions
- **Exception**: BBN priors may be used in separate compatibility analysis, not in main model comparison

---

## 9. Prior-Volume Discipline

**Critical**: Priors for temporal-shear amplitude must be fixed from Gate 0 before fitting.

- **No post-hoc tuning**: Broad post-hoc priors are not allowed for discovery claims
- **Implementation**: ΔlnA priors must be set from magnitude feasibility calculation
- **Validation**: Prior sensitivity analysis must be performed and reported

---

## 10. Data Provenance Requirements

### 10.1 Source Publications
- **Required**: Full citation (authors, year, journal, DOI, arXiv ID)
- **Required**: Publication date and version

### 10.2 Data Versions
- **Required**: Archive identifiers (MAST ID, ESO program ID, SDSS release)
- **Required**: Data reduction version
- **Required**: Calibration version

### 10.3 Checksums
- **Required**: SHA-256 checksums for all downloaded files
- **Required**: Verification of file integrity

### 10.4 Package Versions
- **Required**: Python version
- **Required**: All package versions (numpy, scipy, astropy, dynesty, etc.)
- **Required**: Git commit hash of analysis code

### 10.5 Configs
- **Required**: Full configuration files for all steps
- **Required**: Random seeds for reproducibility

### 10.6 Logs
- **Required**: Complete execution logs for all pipeline steps
- **Required**: Timestamps for all operations

---

## 11. Version Control

### 11.1 Code Version
- **Required**: Git tag for analysis version
- **Required**: Commit hash for reproducibility
- **Required**: Branch name (e.g., `tep-bbn-v0.1-pre-registration`)

### 11.2 Data Version
- **Required**: Zenodo DOI for data snapshots
- **Required**: Archive-specific version identifiers

### 11.3 Results Version
- **Required**: Timestamp on all output files
- **Required**: Version number in all result JSON files

---

## 12. Pre-Registration Date

**This protocol is pre-registered on**: 2026-07-06

**Finalization required before**: First real data analysis begins

**Changes after pre-registration**: Any changes to this protocol after data analysis begins must be documented and justified in the final manuscript.

---

## 13. Sign-Off

**Prepared by**: Matthew Lukin Smawfield
**Date**: 2026-07-06
**Status**: Ready for implementation

**To be finalized**: Before fitting the first real D/H system
