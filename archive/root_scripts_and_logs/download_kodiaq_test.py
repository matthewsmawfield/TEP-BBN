"""
Download KODIAQ data for testing infrastructure

Note: KODIAQ data is for TESTING ONLY - not for TEP-BBN publication
"""

import sys
sys.path.insert(0, '/Users/matthewsmawfield/www/Temporal Equivalence Principle/TEP-BBN')

import requests
from pathlib import Path
import tarfile
from datetime import datetime

print("=" * 60)
print("Downloading KODIAQ Data for Testing Infrastructure")
print("=" * 60)
print()
print("WARNING: KODIAQ data is for TESTING ONLY")
print("This is NOT the specific D/H data from Cooke et al. (2016)")
print("Do NOT use for TEP-BBN publication")
print("=" * 60)
print()

# KODIAQ download URL
kodiaq_url = "https://koa.ipac.caltech.edu/data/KODIAQ/KODIAQ_DR3.tar.gz"

# Create output directory
output_dir = Path('/Users/matthewsmawfield/www/Temporal Equivalence Principle/TEP-BBN/data/raw/kodiaq_test')
output_dir.mkdir(parents=True, exist_ok=True)

# Download KODIAQ tarball
print(f"Downloading KODIAQ data from {kodiaq_url}...")
print("This is a large file (487M compressed, 1002M uncompressed)")
print("This may take several minutes...")
print()

try:
    response = requests.get(kodiaq_url, stream=True)
    response.raise_for_status()
    
    tarball_path = output_dir / 'KODIAQ_DR3.tar.gz'
    
    print(f"Saving to {tarball_path}...")
    with open(tarball_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    
    print(f"✓ Downloaded: {tarball_path.stat().st_size / (1024*1024):.1f} MB")
    
    # Extract tarball
    print()
    print("Extracting tarball...")
    with tarfile.open(tarball_path, 'r:gz') as tar:
        tar.extractall(output_dir)
    
    print(f"✓ Extracted to {output_dir}")
    
    # Create README with warning
    readme_path = output_dir / 'README.txt'
    with open(readme_path, 'w') as f:
        f.write("KODIAQ Data - TEST DATA ONLY\n")
        f.write("=" * 60 + "\n\n")
        f.write("WARNING: This data is for TESTING ONLY\n")
        f.write("This is NOT the specific D/H data from Cooke et al. (2016)\n")
        f.write("Do NOT use for TEP-BBN publication\n\n")
        f.write(f"Downloaded: {datetime.now().isoformat()}\n")
        f.write(f"Source: {kodiaq_url}\n")
        f.write(f"Size: {tarball_path.stat().st_size / (1024*1024):.1f} MB\n\n")
        f.write("KODIAQ contains 300 QSO spectra (reduced 1D spectra)\n")
        f.write("These are NOT the specific high-precision D/H systems\n")
        f.write("required for TEP-BBN analysis.\n\n")
        f.write("For TEP-BBN publication, you must download the specific\n")
        f.write("HIRES spectra from KOA for the 6 D/H systems from\n")
        f.write("Cooke et al. (2016).\n")
    
    print(f"✓ Created README: {readme_path}")
    
    print()
    print("=" * 60)
    print("KODIAQ data download complete")
    print("=" * 60)
    print()
    print("Use this data for:")
    print("  - Testing pipeline infrastructure")
    print("  - Verifying data ingestion code")
    print("  - Testing validation procedures")
    print()
    print("Do NOT use for:")
    print("  - TEP-BBN analysis")
    print("  - Publication")
    print("  - Scientific results")
    print()
    print("For publication, download specific HIRES spectra from KOA:")
    print("  - Q0913+072 (z=2.618)")
    print("  - Q1009+2956 (z=2.504)")
    print("  - Q1243+3047 (z=2.529)")
    print("  - Q1351+3221 (z=2.597)")
    print("  - Q1444+2919 (z=2.428)")
    print("  - Q1444+2919 (z=2.624)")
    print("=" * 60)
    
except Exception as e:
    print(f"✗ Download failed: {e}")
    print()
    print("The KODIAQ download may require:")
    print("  1. Manual download from the web interface")
    print("  2. Authentication (KOA account)")
    print("  3. Different download URL")
    print()
    print("Manual download instructions:")
    print("  1. Access: https://koa.ipac.caltech.edu/applications/KODIAQ/kodiaqQSOList.html")
    print("  2. Click 'Download All (Tar file of 300 QSOs)'")
    print("  3. Place in: data/raw/kodiaq_test/")
