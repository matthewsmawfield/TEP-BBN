"""
Update spectra provenance with correct paths and checksums
"""

import json
from pathlib import Path

# Load checksums
checksums_path = '/Users/matthewsmawfield/www/Temporal Equivalence Principle/TEP-BBN/data/raw/spectra/Q0913072_z2.618/checksums.json'
with open(checksums_path, 'r') as f:
    checksums_data = json.load(f)

# Update provenance
provenance_path = '/Users/matthewsmawfield/www/Temporal Equivalence Principle/TEP-BBN/data/processed/spectra_provenance.json'
with open(provenance_path, 'r') as f:
    provenance = json.load(f)

# Update the Q0913+072 system with correct paths and checksums
for system in provenance['systems']:
    if system['system_id'] == 'Q0913+072_z2.618':
        system['data_directory'] = 'data/raw/spectra/Q0913072_z2.618/'
        system['files'] = []
        
        for checksum_data in checksums_data['files']:
            system['files'].append({
                'filename': checksum_data['filename'],
                'size_bytes': checksum_data['size_bytes'],
                'checksum': checksum_data['checksum'],
                'path': f"data/raw/spectra/Q0913072_z2.618/{checksum_data['filename']}"
            })
        
        system['total_size_bytes'] = sum(f['size_bytes'] for f in system['files'])
        system['total_size_mb'] = system['total_size_bytes'] / (1024*1024)
        system['n_downloaded'] = len(system['files'])
        system['download_status'] = 'success'

# Save updated provenance
with open(provenance_path, 'w') as f:
    json.dump(provenance, f, indent=2)

print("Updated spectra provenance with correct paths and checksums")
print(f"Total files: {len(provenance['systems'][0]['files'])}")
print(f"Total size: {provenance['systems'][0]['total_size_mb']:.1f} MB")
