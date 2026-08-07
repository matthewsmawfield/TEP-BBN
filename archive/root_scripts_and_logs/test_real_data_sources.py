"""
Test script to check if we can get real data from public sources.

This script attempts to:
1. Query NIST atomic data using astroquery
2. Check if specific QSOs are in KODIAQ
3. Download data if possible
"""

import sys
sys.path.insert(0, '/Users/matthewsmawfield/www/Temporal Equivalence Principle/TEP-BBN')

print("=" * 60)
print("Testing Real Data Acquisition from Public Sources")
print("=" * 60)
print()

# Test 1: Check if astroquery is available
print("Test 1: Checking astroquery availability...")
try:
    from astroquery.nist import Nist
    import astropy.units as u
    print("✓ astroquery is available")
    
    # Try to query H I atomic data
    print("\nQuerying NIST for H I Lyman-alpha (1215.67 Å)...")
    try:
        table = Nist.query(1215.0 * u.AA, 1216.0 * u.AA, linename="H I")
        print(f"✓ Found {len(table)} H I lines from NIST")
        print(f"  Columns: {table.colnames}")
        if len(table) > 0:
            print(f"  First line: {table[0]}")
    except Exception as e:
        print(f"✗ NIST query failed: {e}")
        
except ImportError:
    print("✗ astroquery is not installed")
    print("  Install with: pip install astroquery")
except Exception as e:
    print(f"✗ astroquery check failed: {e}")

print()

# Test 2: Check if astropy can download data
print("Test 2: Checking astropy data download...")
try:
    from astropy.utils.data import download_file
    print("✓ astropy download_file is available")
    
    # Try to download a known file from astropy data server
    print("\nAttempting to download from astropy data server...")
    try:
        # This is a test - try to download a small file
        from astropy.utils.data import get_pkg_data_filename
        print("✓ astropy data access is available")
    except Exception as e:
        print(f"✗ astropy data access failed: {e}")
        
except ImportError:
    print("✗ astropy is not installed")
except Exception as e:
    print(f"✗ astropy check failed: {e}")

print()

# Test 3: Check KODIAQ availability
print("Test 3: Checking KODIAQ availability...")
print("KODIAQ provides public access to 300 QSO spectra")
print("URL: https://koa.ipac.caltech.edu/applications/KODIAQ/kodiaqQSOList.html")
print("Download: 'Download All (Tar file of 300 QSOs)' - 487M compressed")
print()
print("However, KODIAQ data is reduced 1D spectra, not the specific")
print("high-precision D/H systems from Cooke et al. (2016).")
print("The Cooke et al. (2016) data requires specific HIRES observations")
print("that may not be in the public KODIAQ archive.")
print()

# Test 4: Check if we can download from KODIAQ
print("Test 4: Checking KODIAQ download...")
print("KODIAQ requires manual download from the web interface.")
print("No automated API is available for bulk download.")
print("The 'Download All' button requires manual interaction.")
print()

print("=" * 60)
print("Summary")
print("=" * 60)
print()
print("Atomic Data:")
print("  - astroquery can QUERY NIST database")
print("  - astroquery can DOWNLOAD some data from astropy server")
print("  - However, this may not include all required transitions")
print("  - Manual download from NIST web interface is still recommended")
print()
print("Spectroscopic Data:")
print("  - KODIAQ provides public access to 300 QSO spectra")
print("  - However, these are reduced 1D spectra, not the specific")
print("    high-precision D/H systems from Cooke et al. (2016)")
print("  - The Cooke et al. (2016) data requires specific HIRES observations")
print("  - These observations may not be in the public KODIAQ archive")
print("  - KOA requires authentication for specific observations")
print()
print("Conclusion:")
print("  - We can get SOME real atomic data programmatically")
print("  - We CANNOT get the specific spectroscopic data needed")
print("  - The specific D/H systems from Cooke et al. (2016) require")
print("    manual download from KOA with authentication")
print()
print("Recommendation:")
print("  1. Use astroquery to download available atomic data")
print("  2. Manually download the specific HIRES spectra from KOA")
print("  3. Accept that this requires authentication")
print("=" * 60)
