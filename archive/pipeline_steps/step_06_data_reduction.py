"""
Step 06: Data reduction for TEP-BBN

Reduces raw UVES 2D echelle images to 1D wavelength-calibrated spectra.

Note: This step requires manual reduction using ESO Reflex or similar software.
The pipeline expects reduced 1D spectra as input for Voigt fitting.
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

def reduce_data():
    """
    Reduce raw UVES data to 1D spectra.
    
    Note: This step requires manual reduction using ESO Reflex or similar software.
    The pipeline cannot automatically reduce echelle data without specialized software.
    
    Manual reduction process:
    1. Install ESO Reflex from https://www.eso.org/sci/software/reflex/
    2. Import UVES data from data/raw/spectra/Q0913+072_z2.618/
    3. Run UVES reduction recipe
    4. Validate output quality (S/N > 30, wavelength accuracy < 0.01 Å)
    5. Co-add multiple exposures
    6. Save reduced spectrum to data/processed/reduced/Q0913+072_z2.618/
    """
    print("Step 06: Data reduction")
    print("=" * 60)
    print("CRITICAL: This step requires manual reduction using ESO Reflex.")
    print("No placeholder or synthetic data is allowed.")
    print("=" * 60)
    print()
    
    # Check for raw data
    raw_data_dir = Path('data/raw/spectra/Q0913+072_z2.618')
    if not raw_data_dir.exists():
        print("WARNING: Raw data directory not found")
        print("Expected: data/raw/spectra/Q0913+072_z2.618/")
        print("Checking for data in astropy cache...")
        
        # Check astropy cache
        cache_dir = Path.home() / '.astropy' / 'cache' / 'astroquery' / 'Eso'
        if cache_dir.exists():
            cache_files = list(cache_dir.glob('UVES*.fits'))
            print(f"Found {len(cache_files)} FITS files in astropy cache")
            print(f"Cache location: {cache_dir}")
            print()
            print("Moving files from cache to data directory...")
            
            # Create data directory
            raw_data_dir.mkdir(parents=True, exist_ok=True)
            
            # Copy files from cache
            import shutil
            for cache_file in cache_files:
                dest_file = raw_data_dir / cache_file.name
                shutil.copy(cache_file, dest_file)
                print(f"  Copied: {cache_file.name}")
            
    fits_files = list(raw_data_dir.glob('*.fits'))
    print(f"Found {len(fits_files)} raw FITS files")
    print()
    
    # Check for reduced data
    reduced_data_dir = Path('data/processed/reduced/Q0913+072_z2.618')
    if reduced_data_dir.exists():
        reduced_files = list(reduced_data_dir.glob('*.fits')) + list(reduced_data_dir.glob('*.txt'))
        if len(reduced_files) > 0:
            print(f"Found {len(reduced_files)} reduced data files")
            print("Reduced data already exists")
            print()
            
            # Load existing reduction metadata
            metadata_file = Path('data/processed/reduction_metadata.json')
            if metadata_file.exists():
                with open(metadata_file, 'r') as f:
                    metadata = json.load(f)
                print("Reduction metadata:")
                print(f"  Reduction date: {metadata.get('reduction_date')}")
                print(f"  Software: {metadata.get('reduction_software')}")
                print(f"  Status: {metadata.get('status')}")
                print()
                return metadata
    
    print("MANUAL REDUCTION REQUIRED")
    print()
    print("To reduce the UVES data:")
    print("1. Install ESO Reflex from https://www.eso.org/sci/software/reflex/")
    print("2. Import UVES data from: data/raw/spectra/Q0913+072_z2.618/")
    print("3. Run UVES reduction recipe")
    print("4. Validate output quality:")
    print("   - S/N > 30 per pixel")
    print("   - Wavelength calibration accuracy < 0.01 Å")
    print("   - Continuum normalization residuals < 5%")
    print("5. Co-add multiple exposures")
    print("6. Save reduced spectrum to: data/processed/reduced/Q0913+072_z2.618/")
    print()
    print("See UVES_DATA_REDUCTION_PROCESS.md for detailed instructions")
    print()
    
    # Create placeholder metadata
    metadata = {
        'reduction_date': None,
        'reduction_software': None,
        'reduction_version': None,
        'status': 'manual_reduction_required',
        'raw_data_dir': str(raw_data_dir),
        'n_raw_files': len(fits_files),
        'reduced_data_dir': str(reduced_data_dir),
        'instructions': 'See UVES_DATA_REDUCTION_PROCESS.md'
    }
    
    # Save metadata
    output_path = 'data/processed/reduction_metadata.json'
    Path('data/processed').mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print(f"Reduction metadata saved to {output_path}")
    print()
    
    # If reduced data exists, run validation
    if reduced_data_dir.exists():
        print("Checking for reduced data validation...")
        validation_script = Path('scripts/steps/validate_reduced_data.py')
        if validation_script.exists():
            print("Running validation script...")
            import subprocess
            result = subprocess.run(['python3', str(validation_script)], 
                                  capture_output=True, text=True)
            print(result.stdout)
            if result.stderr:
                print("Validation errors:")
                print(result.stderr)
    
    print("=" * 60)
    print("STATUS: Manual reduction required")
    print("Complete manual reduction, then re-run this step to validate")
    print("=" * 60)
    
    return metadata

if __name__ == '__main__':
    reduce_data()
    
    # Save metadata
    output_path = 'data/processed/reduction_metadata.json'
    Path('data/processed').mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print(f"Reduction metadata saved to {output_path}")
    print()
    print("=" * 60)
    print("STATUS: Manual reduction required")
    print("Complete manual reduction, then re-run this step to validate")
    print("=" * 60)
    
    return metadata

if __name__ == '__main__':
    reduce_data()
        'reduction_software': None,
        'reduction_version': None,
        'status': 'manual_reduction_required',
        'raw_data_dir': str(raw_data_dir),
        'n_raw_files': len(fits_files),
        'reduced_data_dir': str(reduced_data_dir),
        'instructions': 'See UVES_DATA_REDUCTION_PROCESS.md'
    }
    
    # Save metadata
    output_path = 'data/processed/reduction_metadata.json'
    Path('data/processed').mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print(f"Reduction metadata saved to {output_path}")
    print()
    print("=" * 60)
    print("STATUS: Manual reduction required")
    print("Complete manual reduction, then re-run this step to validate")
    print("=" * 60)
    
    return metadata

if __name__ == '__main__':
    reduce_data()
    Path('data/processed').mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print(f"Reduction metadata saved to {output_path}")
    print()
    print("=" * 60)
    print("STATUS: Manual reduction required")
    print("Complete manual reduction, then re-run this step to validate")
    print("=" * 60)
    
    return metadata

if __name__ == '__main__':
    reduce_data()
