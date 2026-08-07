"""
Step 04: Data ingestion and standardization for TEP-BBN

Ingests and standardizes spectroscopic data for analysis.

Note: The downloaded UVES data are raw 2D echelle images, not 1D spectra.
Proper reduction requires specialized software (ESO Reflex, IRAF, etc.).
This step creates metadata and marks data as ready for reduction.
"""

import json
from pathlib import Path
from datetime import datetime
import hashlib

def calculate_sha256(filepath):
    """Calculate SHA-256 checksum of a file."""
    sha256_hash = hashlib.sha256()
    with open(filepath, 'rb') as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def ingest_data():
    """
    Ingest and standardize spectroscopic data.
    
    Note: UVES data are raw 2D echelle images requiring reduction.
    This step creates metadata and documents the data structure.
    """
    print("Step 04: Data ingestion and standardization")
    print("=" * 60)
    print("CRITICAL: This step requires REAL FITS files from step_02.")
    print("No placeholder or synthetic data is allowed.")
    print("=" * 60)
    print()
    
    # Load literature registry
    registry_path = '../../data/processed/dh_literature_registry.json'
    with open(registry_path, 'r') as f:
        registry = json.load(f)
    
    systems = registry['systems']
    print(f"Processing {len(systems)} systems")
    print()
    
    # Create output directory
    processed_dir = Path('../../data/processed/standardized')
    processed_dir.mkdir(parents=True, exist_ok=True)
    
    processing_metadata = {
        'processing_date': datetime.now().isoformat(),
        'processing_software_version': '0.1.0',
        'processing_notes': 'UVES data are raw 2D echelle images requiring reduction',
        'systems': []
    }
    
    for system in systems:
        system_id = system['system_id']
        qso_name = system['qso_name']
        redshift = system['redshift']
        
        print(f"Processing system: {system_id}")
        
        # Real FITS files directory
        fits_dir = Path(f'../../data/raw/spectra/{system_id}')
        
        if not fits_dir.exists():
            print(f"  WARNING: FITS directory not found: {fits_dir}")
            continue
        
        fits_files = list(fits_dir.glob('*.fits'))
        if len(fits_files) == 0:
            print(f"  WARNING: No FITS files found in directory")
            continue
        
        print(f"  Found {len(fits_files)} FITS files")
        
        # Load checksums
        checksums_path = fits_dir / 'checksums.json'
        checksums_data = {}
        if checksums_path.exists():
            with open(checksums_path, 'r') as f:
                checksums_data = json.load(f)
        
        # Create standardized metadata
        standardized_data = {
            'system_id': system_id,
            'qso_name': qso_name,
            'redshift': redshift,
            'processing_status': 'raw_data_ready_for_reduction',
            'data_type': 'raw_2d_echelle',
            'instrument': 'UVES',
            'n_files': len(fits_files),
            'files': [],
            'notes': 'UVES data are raw 2D echelle images. Reduction requires ESO Reflex or similar software.',
            'reduction_software': ['ESO Reflex', 'IRAF', 'Custom reduction pipeline'],
            'next_steps': [
                'Reduce raw 2D echelle images to 1D spectra',
                'Calibrate wavelength solution',
                'Flux calibration',
                'Continuum normalization',
                'Co-add multiple exposures'
            ]
        }
        
        # Add file metadata
        for fits_file in fits_files:
            checksum = calculate_sha256(fits_file)
            file_size = fits_file.stat().st_size
            standardized_data['files'].append({
                'filename': fits_file.name,
                'size_bytes': file_size,
                'checksum': checksum
            })
        
        # Save standardized metadata
        output_file = processed_dir / f'{system_id}_standardized.json'
        with open(output_file, 'w') as f:
            json.dump(standardized_data, f, indent=2)
        
        print(f"  ✓ Standardized metadata created: {output_file}")
        
        processing_metadata['systems'].append({
            'system_id': system_id,
            'n_files': len(fits_files),
            'output_file': str(output_file),
            'processing_status': 'raw_data_ready_for_reduction'
        })
    
    # Save processing metadata
    output_path = '../../data/processed/processing_metadata.json'
    with open(output_path, 'w') as f:
        json.dump(processing_metadata, f, indent=2)
    
    print()
    print("=" * 60)
    print(f"Processing complete: {len(processing_metadata['systems'])} systems processed")
    print(f"Processing metadata saved to {output_path}")
    print()
    print("Note: UVES data are raw 2D echelle images requiring reduction.")
    print("Use ESO Reflex or similar software for reduction to 1D spectra.")
    print("=" * 60)
    
    return processing_metadata

if __name__ == '__main__':
    ingest_data()
