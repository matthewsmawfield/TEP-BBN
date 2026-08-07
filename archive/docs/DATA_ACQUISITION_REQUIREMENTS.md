# TEP-BBN Data Acquisition Requirements

**Date**: 2026-07-06
**Status**: CRITICAL - All data must be real, traceable, and have full provenance
**Policy**: No placeholder or synthetic data is allowed

---

## Critical Requirement

**ALL DATA MUST BE REAL, TRACEABLE, AND GENUINE.**

No placeholder data, no synthetic data, no fabricated data. Every data point must be traceable to its original source with full provenance tracking.

---

## Required Data Sources

### 1. Spectroscopic Data (Step 02)

**Source**: Keck Observatory Archive (KOA)
**Instrument**: Keck/HIRES
**Data Type**: FITS files (reduced spectra)

**Acquisition Steps**:
1. Access KOA at: https://koa.ipac.caltech.edu/
2. Create KOA account (requires credentials)
3. Search for each QSO from literature registry:
   - Q0913+072
   - Q1009+2956
   - Q1243+3047
   - Q1351+3221
   - Q1444+2919 (two systems)
4. Select HIRES observations from Cooke et al. (2016)
5. Download reduced spectra (FITS format)
6. Place in: `data/raw/spectra/{system_id}/`
7. Verify file integrity (SHA-256 checksum)

**Provenance Requirements**:
- Archive version: Fixed (not "latest")
- Observation ID: Record specific observation numbers
- Data reduction version: Record reduction software version
- Download date: Timestamp
- Checksum: SHA-256 of downloaded file
- File size: Record actual file size

**Acceptance Criteria**:
- File must be in FITS format
- File must contain wavelength, flux, and error arrays
- File must be from KOA (not synthetic)
- File must have valid checksum
- File must be from Cooke et al. (2016) observations

---

### 2. Atomic Data (Step 03)

**Source**: NIST Atomic Spectra Database (ASD) v5.11.1
**Alternative**: VALD3 (Vienna Atomic Line Database)
**Data Type**: Wavelengths and oscillator strengths (f-values)

**Acquisition Steps**:
1. Access NIST ASD at: https://physics.nist.gov/ASD
2. For each required element:
   - H I (Hydrogen I)
   - D I (Deuterium I)
   - O I (Oxygen I)
   - Si II (Silicon II)
   - C II (Carbon II)
   - Fe II (Iron II)
3. Search for element and ion
4. Select "Lines" tab
5. Download data for required transitions
6. Place in: `data/raw/atomic/{element}/`
7. Update `{element}_lines.txt` with real f-values

**Required Transitions**:
- H I: Lyα (1215.67 Å), Lyβ (1025.72 Å), Lyγ (972.537 Å), Lyδ (949.743 Å), Lyε (937.803 Å)
- D I: Same series, isotope-shifted wavelengths
- O I: 1302.1685 Å, 1304.8576 Å
- Si II: 1526.707 Å, 1304.370 Å
- C II: 1334.532 Å, 1036.337 Å
- Fe II: 1608.451 Å, 1144.938 Å

**Provenance Requirements**:
- Database version: Fixed (NIST ASD 5.11.1 or VALD3)
- Download date: Timestamp
- Source URL: https://physics.nist.gov/ASD
- Data format: Wavelength (Å), oscillator strength, transition name
- Checksum: SHA-256 of downloaded data file

**Acceptance Criteria**:
- Oscillator strengths must be real (not 0.0000)
- Wavelengths must be from NIST/VALD
- Data must be in standard format
- No placeholder values allowed

---

### 3. Literature Data (Step 01)

**Source**: Cooke et al. (2016) ApJ 827, 59
**DOI**: 10.3847/1538-3881/2016/9/6/19
**arXiv**: 1607.03900
**Data Type**: Published D/H measurements

**Provenance Requirements**:
- Publication DOI: 10.3847/1538-3881/2016/9/6/19
- arXiv ID: 1607.03900
- Authors: Cooke, R., Pettini, M., Natarajan, P., Steidel, C.C.
- Journal: ApJ
- Year: 2016
- Volume: 827
- Page: 59
- License: CC BY 4.0

**Acceptance Criteria**:
- All values must be from published paper
- No fabricated or modified values
- Full citation must be recorded

---

## Data Validation (Step 05)

### Rejection Criteria

The following will cause validation to **FAIL**:

1. **Placeholder data**: Any file containing "placeholder" or synthetic data
2. **Missing files**: Expected FITS or atomic data files not present
3. **Invalid format**: Files not in expected format (FITS, JSON, etc.)
4. **Missing checksums**: No SHA-256 checksum calculated
5. **Missing provenance**: No source information recorded
6. **Synthetic values**: Oscillator strengths of 0.0000 or similar placeholders
7. **Fabricated data**: Any data not traceable to original source

### Validation Checks

1. **File integrity**: SHA-256 checksums must match
2. **Format validation**: JSON structure, required fields
3. **Data range checks**: Redshift (2.0-3.5), log N_HI (19.0-22.0), D/H (1e-5-5e-5)
4. **Literature cross-validation**: Compare to published values
5. **Metadata completeness**: All required fields present
6. **Placeholder rejection**: Explicit check for placeholder indicators

---

## Pipeline Behavior

### Step 02 (Spectra Download)
- **If real FITS files exist**: Verify checksums, record provenance, PASS
- **If FITS files missing**: FAIL with clear error message
- **If placeholder files found**: FAIL with clear error message
- **No automatic generation**: Does not create placeholder files

### Step 03 (Atomic Data Download)
- **If real atomic data exists**: Verify no placeholders, record provenance, PASS
- **If atomic data missing**: FAIL with clear error message
- **If placeholder data found**: FAIL with clear error message
- **No automatic generation**: Does not create placeholder files

### Step 04 (Data Ingestion)
- **If real FITS files exist**: Read with astropy, convert to velocity space, PASS
- **If FITS files missing**: FAIL with clear error message
- **No placeholder generation**: Does not create synthetic flux arrays

### Step 05 (Data Validation)
- **If all data is real**: PASS
- **If any placeholder detected**: FAIL with clear error message
- **If any file missing**: FAIL with clear error message
- **Strict enforcement**: No warnings allowed for placeholder data

---

## Error Messages

When real data is not available, the pipeline will produce clear error messages:

```
ERROR: Real FITS files are missing for the following systems:
  - Q0913+072_z2.618
  - Q1009+2956_z2.504
  ...

To proceed with real data analysis:
  1. Access KOA at: https://koa.ipac.caltech.edu/
  2. Download HIRES spectra for each QSO
  3. Place FITS files in: data/raw/spectra/{system_id}/
  4. Re-run this step to verify downloads

CRITICAL: No placeholder or synthetic data is allowed.
Real data must be obtained from the archive before proceeding.
```

```
ERROR: Real atomic data is missing or contains placeholders:
  - H_I: contains_placeholder_data
  - D_I: file_not_found
  ...

To proceed with real data analysis:
  1. Access NIST ASD at: https://physics.nist.gov/ASD
  2. Download atomic data for each required element
  3. Place data files in: data/raw/atomic/{element}/
  4. Ensure files contain real oscillator strengths (not 0.0000)
  5. Re-run this step to verify downloads

CRITICAL: No placeholder or synthetic data is allowed.
Real atomic data must be obtained from NIST/VALD before proceeding.
```

```
ERROR: Placeholder or synthetic data detected.

CRITICAL: No placeholder or synthetic data is allowed.
All data must be real, traceable, and have full provenance.

To fix:
  1. Download real FITS files from KOA (step_02)
  2. Download real atomic data from NIST/VALD (step_03)
  3. Re-run data ingestion with real FITS files (step_04)
  4. Re-run validation to verify
```

---

## Data Provenance Tracking

### Required Metadata for Each File

**Spectra (FITS)**:
- Source archive (KOA)
- Archive version (fixed)
- Observation ID
- Data reduction version
- Download date
- SHA-256 checksum
- File size
- Original instrument (Keck/HIRES)

**Atomic Data**:
- Source database (NIST ASD or VALD)
- Database version (fixed)
- Download date
- SHA-256 checksum
- Element and ion
- Transitions included

**Literature Data**:
- Publication DOI
- arXiv ID
- Authors
- Journal
- Year
- Volume
- Page
- License

---

## Verification Checklist

Before proceeding to analysis (steps 06-14), verify:

- [ ] All 6 FITS files downloaded from KOA
- [ ] All 6 atomic data files downloaded from NIST/VALD
- [ ] All SHA-256 checksums calculated and recorded
- [ ] All provenance metadata complete
- [ ] No placeholder data in any file
- [ ] Step 05 validation passes
- [ ] All data traceable to original sources

---

## Consequences of Non-Compliance

If real data is not obtained:

1. **Pipeline will fail**: Steps 02-05 will fail with clear errors
2. **Analysis cannot proceed**: Steps 06-14 require real data
3. **Results will be invalid**: Any analysis with placeholder data is invalid
4. **Publication impossible**: Peer review will reject placeholder data

---

## Summary

**Policy**: Zero tolerance for placeholder or synthetic data
**Requirement**: All data must be real, traceable, and have full provenance
**Enforcement**: Pipeline will fail if real data is not present
**Verification**: Step 05 validation explicitly rejects placeholder data

**Only proceed to analysis (steps 06-14) when all real data is obtained and validated.**

---

**Prepared by**: Matthew Lukin Smawfield
**Date**: 2026-07-06
**Status**: Strict enforcement of real data requirement
