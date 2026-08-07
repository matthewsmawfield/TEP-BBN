"""
Calculate SHA-256 checksums for atomic data
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

# Load existing registry
registry_path = '/Users/matthewsmawfield/www/Temporal Equivalence Principle/TEP-BBN/data/processed/atomic_data_registry.json'
with open(registry_path, 'r') as f:
    registry = json.load(f)

# Calculate checksums for all atomic data files
atomic_data_dir = Path('/Users/matthewsmawfield/www/Temporal Equivalence Principle/TEP-BBN/data/raw/atomic')

for element_key, element_data in registry['data'].items():
    if element_data['status'] in ['real_data', 'partial_data']:
        file_path = Path(element_data['file'])
        if file_path.exists():
            checksum = calculate_sha256(file_path)
            file_size = file_path.stat().st_size
            registry['data'][element_key]['checksum'] = checksum
            registry['data'][element_key]['size_bytes'] = file_size
            print(f"{element_key}: {checksum[:16]}... ({file_size} bytes)")
        else:
            print(f"{element_key}: File not found at {file_path}")

# Save updated registry
with open(registry_path, 'w') as f:
    json.dump(registry, f, indent=2)

print(f"\nUpdated registry with checksums")
