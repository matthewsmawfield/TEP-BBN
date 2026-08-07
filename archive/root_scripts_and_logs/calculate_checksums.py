"""
Calculate SHA-256 checksums for downloaded spectroscopic data
"""

import json
import hashlib
from pathlib import Path
from datetime import datetime

def calculate_sha256(filepath):
    """Calculate SHA-256 checksum of a file."""
    sha256_hash = hashlib.sha256()
    with open(filepath, 'rb') as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

# Calculate checksums for all FITS files
spectra_dir = Path('/Users/matthewsmawfield/www/Temporal Equivalence Principle/TEP-BBN/data/raw/spectra/Q0913072_z2.618')

fits_files = list(spectra_dir.glob('*.fits'))

checksums = []
for fits_file in fits_files:
    checksum = calculate_sha256(fits_file)
    file_size = fits_file.stat().st_size
    checksums.append({
        'filename': fits_file.name,
        'size_bytes': file_size,
        'checksum': checksum
    })
    print(f"{fits_file.name}: {checksum[:16]}... ({file_size / (1024*1024):.1f} MB)")

# Save checksums
checksum_file = spectra_dir / 'checksums.json'
with open(checksum_file, 'w') as f:
    json.dump({
        'calculated': datetime.now().isoformat(),
        'files': checksums
    }, f, indent=2)

print(f"\nChecksums saved to {checksum_file}")
print(f"Total files: {len(checksums)}")
