# Real Data Acquisition from Public Sources - Analysis

**Date**: 2026-07-06
**Status**: Public sources have limitations - manual acquisition still required

---

## Analysis of Public Data Sources

### 1. Spectroscopic Data (HIRES Spectra)

#### KODIAQ Archive
- **URL**: https://koa.ipac.caltech.edu/applications/KODIAQ/
- **Content**: 300 QSO spectra (reduced 1D spectra)
- **Access**: Public, no authentication required
- **Download**: "Download All" tarball (487M compressed, 1002M uncompressed)
- **Problem**: KODIAQ contains reduced 1D spectra, not the specific high-precision D/H systems from Cooke et al. (2016)

#### Cooke et al. (2016) Specific Systems
The 6 systems in our literature registry are:
- Q0913+072 (z=2.618)
- Q1009+2956 (z=2.504)
- Q1243+3047 (z=2.529)
- Q1351+3221 (z=2.597)
- Q1444+2919 (z=2.428)
- Q1444+2919 (z=2.624)

**Issue**: These are specific high-precision D/H systems observed with HIRES. The data may not be in the public KODIAQ archive because:
1. KODIAQ is a survey of 300 QSOs (not all D/H systems)
2. Cooke et al. (2016) may have used specific observing programs not in KODIAQ
3. The reduced spectra may not be in the public domain

#### KOA (Keck Observatory Archive)
- **URL**: https://koa.ipac.caltech.edu/
- **Content**: All Keck/HIRES data
- **Access**: Requires authentication (KOA account)
- **Problem**: Cannot automate without credentials

### 2. Atomic Data (NIST)

#### NIST Atomic Spectra Database
- **URL**: https://physics.nist.gov/ASD
- **Content**: Atomic data for all elements
- **Access**: Public web interface
- **API**: No official download API (web scraping required)
- **Python**: astroquery.nist can QUERY but not reliably DOWNLOAD

#### astroquery.nist
- **Package**: astroquery
- **Function**: Nist.query() can query NIST database
- **Limitation**: Returns query results, not downloadable files
- **Use**: Can get wavelengths and oscillator strengths programmatically

#### astropy Data Server
- **Package**: astropy
- **Function**: astropy.utils.data.download_file()
- **Content**: Some astronomical datasets
- **Limitation**: May not include all required atomic transitions

---

## What Can Be Done Programmatically

### Atomic Data (Partial)
We can use astroquery.nist to query NIST and extract atomic data:

```python
from astroquery.nist import Nist
import astropy.units as u

# Query H I Lyman-alpha
table = Nist.query(1215.0 * u.AA, 1216.0 * u.AA, linename="H I")
# Returns table with wavelengths and oscillator strengths
```

**Limitations**:
- May not include all required transitions
- Requires astroquery installation
- Data still needs to be verified against NIST web interface

### Spectroscopic Data (Not Possible)
**Cannot**:
- Download specific HIRES spectra from KODIAQ (wrong data)
- Download specific HIRES spectra from KOA (requires authentication)
- Download Cooke et al. (2016) specific observations (requires authentication)

**Can**:
- Download KODIAQ "Download All" tarball (but wrong data)
- Use KODIAQ data for testing infrastructure (but not for publication)

---

## Recommendation

### For Atomic Data
**Option 1: Use astroquery.nist (Programmatic)**
```python
# Install astroquery
pip install astroquery

# Query NIST for required transitions
from astroquery.nist import Nist
import astropy.units as u

# Query H I Lyman series
for transition in ['Lyα', 'Lyβ', 'Lyγ', 'Lyδ', 'Lyε']:
    table = Nist.query(...)  # Query appropriate wavelength range
    # Extract wavelengths and oscillator strengths
```

**Option 2: Manual Download from NIST (Reliable)**
- Access https://physics.nist.gov/ASD
- Download data for each element manually
- More reliable, ensures correct data

### For Spectroscopic Data
**Option 1: Manual Download from KOA (Required)**
- Create KOA account (free but requires registration)
- Download specific HIRES observations for 6 QSOs
- This is the only way to get the correct data

**Option 2: Use KODIAQ for Testing (Not for Publication)**
- Download KODIAQ "Download All" tarball
- Use for testing pipeline infrastructure
- Cannot use for actual TEP-BBN analysis (wrong data)

---

## Conclusion

### What I Can Do
1. ✅ Implement astroquery.nist to download atomic data programmatically
2. ✅ Download KODIAQ data for testing infrastructure
3. ✅ Validate that data is real (not placeholder)

### What I Cannot Do
1. ❌ Download specific HIRES spectra from KOA (requires authentication)
2. ❌ Download Cooke et al. (2016) specific observations (requires authentication)
3. ❌ Get the correct spectroscopic data for TEP-BBN analysis

### Reality Check
The requirement that "all data must be real, traceable, and genuine" is correct. However, the specific spectroscopic data needed for TEP-BBN (Cooke et al. 2016 D/H systems) is NOT available through public APIs. It requires:

1. KOA account authentication
2. Manual selection of specific observations
3. Manual download of FITS files

This is a limitation of the data access policies, not the implementation.

---

## Proposed Path Forward

### Phase 1: Atomic Data (Programmatic)
1. Implement astroquery.nist to download atomic data
2. Verify data against NIST web interface
3. Save with full provenance tracking

### Phase 2: Spectroscopic Data (Manual)
1. Create KOA account (you must do this)
2. Download specific HIRES observations for 6 QSOs (you must do this)
3. Place in data/raw/spectra/{system_id}/
4. Run validation to verify

### Phase 3: Testing Infrastructure
1. Download KODIAQ tarball for testing
2. Use to test pipeline infrastructure
3. Clearly label as "TEST DATA ONLY - NOT FOR PUBLICATION"
4. Replace with real data when available

---

**Prepared by**: Matthew Lukin Smawfield
**Date**: 2026-07-06
**Status**: Public sources have limitations - manual acquisition still required for spectroscopic data
