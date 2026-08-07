"""
Step 02: Spectra data download for TEP-BBN

Downloads high-resolution quasar spectra from public archives with full provenance tracking.

CRITICAL: This step downloads REAL data from ESO archive using astroquery.eso.
No placeholder or synthetic data is allowed.
"""

import json
import hashlib
from datetime import datetime
from pathlib import Path
import sys
import shutil

def calculate_sha256(filepath):
    """Calculate SHA-256 checksum of a file."""
    sha256_hash = hashlib.sha256()
    with open(filepath, 'rb') as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def download_spectra():
    """
    Download spectroscopic data for target systems with full provenance.
    
    For TEP-BBN, we download UVES (VLT) data from ESO archive using astroquery.eso.
    The ESO archive provides public access to UVES data without authentication.
    
    Systems:
    - Q0913+072 (z=2.618) - Program ID: 68.B-0115 (UVES)
    
    Note: This downloads UVES data, not HIRES data. Cooke et al. (2016) used both
    instruments for different systems. UVES data is publicly available from ESO.
    HIRES data requires KOA authentication.
    
    CRITICAL: This step downloads REAL data from ESO using astroquery.eso.
    """
    print("Step 02: Spectra data download (using astroquery.eso)")
    print("=" * 60)
    print("CRITICAL: This step downloads REAL data from ESO archive.")
    print("No placeholder or synthetic data is allowed.")
    print("=" * 60)
    print()
    
    # Check if astroquery is available
    try:
        from astroquery.eso import Eso
        print("✓ astroquery.eso is available")
    except ImportError:
        print("✗ astroquery.eso is not installed")
        print("Install with: pip install astroquery")
        sys.exit(1)
    except Exception as e:
        print(f"✗ astroquery.eso import failed: {e}")
        sys.exit(1)
    
    # Load literature registry to get target systems
    registry_path = '../../data/processed/dh_literature_registry.json'
    if not Path(registry_path).exists():
        print("ERROR: Literature registry not found. Run step_01 first.")
        sys.exit(1)
    
    with open(registry_path, 'r') as f:
        registry = json.load(f)
    
    systems = registry['systems']
    print(f"Found {len(systems)} systems in literature registry")
    print()
    
    # Define ESO programs for systems with public UVES data
    eso_programs = {
        'Q0913+072_z2.618': {
            'prog_id': '68.B-0115',
            'instrument': 'UVES'
        }
    }
    
    # Create output directory
    raw_data_dir = Path('../../data/raw/spectra')
    raw_data_dir.mkdir(parents=True, exist_ok=True)
    
    provenance = {
        'download_date': datetime.now().isoformat(),
        'download_method': 'astroquery.eso (programmatic access to ESO archive)',
        'archive': 'ESO Science Archive',
        'archive_url': 'https://archive.eso.org/',
        'archive_version': 'public (no authentication required)',
        'systems': []
    }
    
    # Create ESO instance
    eso = Eso()
    
    for system in systems:
        system_id = system['system_id']
        qso_name = system['qso_name']
        redshift = system['redshift']
        
        print(f"Processing system: {system_id} ({qso_name} at z={redshift})")
        
        # Check if this system has ESO program data
        if system_id in eso_programs:
            prog_id = eso_programs[system_id]['prog_id']
            instrument = eso_programs[system_id]['instrument']
            
            print(f"  Found ESO program: {prog_id} ({instrument})")
            
            try:
                # Query ESO archive
                table = eso.query_main(column_filters={'prog_id': prog_id})
                print(f"  ✓ Found {len(table)} observations")
                
                # Filter for SCIENCE observations
                science_table = table[table['Category'] == 'SCIENCE']
                print(f"  ✓ {len(science_table)} SCIENCE observations")
                
                if len(science_table) > 0:
                    # Create system directory
                    system_dir = raw_data_dir / system_id
                    system_dir.mkdir(parents=True, exist_ok=True)
                    
                    # Get dataset IDs
                    dataset_ids = science_table['Dataset ID']
                    
                    print(f"  Downloading {len(dataset_ids)} datasets...")
                    
                    downloaded_files = []
                    for i, dataset_id in enumerate(dataset_ids):
                        print(f"    [{i+1}/{len(dataset_ids)}] {dataset_id}")
                        
                        try:
                            # Retrieve data
                            eso.retrieve_data([dataset_id])
                            
                            # Move from astropy cache to our directory
                            cache_file = Path.home() / '.astropy' / 'cache' / 'astroquery' / 'Eso' / f'{dataset_id}.fits'
                            if cache_file.exists():
                                dest_file = system_dir / f'{dataset_id}.fits'
                                shutil.move(str(cache_file), str(dest_file))
                                
                                # Calculate checksum
                                checksum = calculate_sha256(dest_file)
                                file_size = dest_file.stat().st_size
                                
                                downloaded_files.append({
                                    'filename': dest_file.name,
                                    'size_bytes': file_size,
                                    'checksum': checksum,
                                    'dataset_id': dataset_id
                                })
                                
                                print(f"      ✓ Downloaded ({file_size / (1024*1024):.1f} MB)")
                            else:
                                print(f"      ✗ File not found in cache")
                                
                        except Exception as e:
                            print(f"      ✗ Failed: {e}")
                    
                    print(f"  ✓ Downloaded {len(downloaded_files)} files to {system_dir}")
                    
                    system_provenance = {
                        'system_id': system_id,
                        'qso_name': qso_name,
                        'redshift': redshift,
                        'instrument': instrument,
                        'archive': 'ESO',
                        'program_id': prog_id,
                        'download_status': 'success',
                        'n_observations': len(science_table),
                        'n_downloaded': len(downloaded_files),
                        'files': downloaded_files
                    }
                    
                else:
                    print(f"  ✗ No SCIENCE observations found")
                    system_provenance = {
                        'system_id': system_id,
                        'qso_name': qso_name,
                        'redshift': redshift,
                        'instrument': instrument,
                        'archive': 'ESO',
                        'program_id': prog_id,
                        'download_status': 'no_science_observations'
                    }
                    
            except Exception as e:
                print(f"  ✗ Query failed: {e}")
                system_provenance = {
                    'system_id': system_id,
                    'qso_name': qso_name,
                    'redshift': redshift,
                    'instrument': instrument,
                    'archive': 'ESO',
                    'program_id': prog_id,
                    'download_status': 'query_failed',
                    'error': str(e)
                }
                
        else:
            print(f"  ⚠ No ESO program data available for this system")
            print(f"  Note: This system may require HIRES data from KOA (requires authentication)")
            
            system_provenance = {
                'system_id': system_id,
                'qso_name': qso_name,
                'redshift': redshift,
                'download_status': 'no_eso_program',
                'note': 'No ESO program data available. Requires HIRES data from KOA.'
            }
        
        provenance['systems'].append(system_provenance)
        print()
    
    # Save provenance
    output_path = '../../data/processed/spectra_provenance.json'
    with open(output_path, 'w') as f:
        json.dump(provenance, f, indent=2)
    
    print("=" * 60)
    print(f"Provenance saved to {output_path}")
    print("=" * 60)
    print()
    print("Note: This downloads UVES (VLT) data from ESO archive.")
    print("UVES data is publicly available without authentication.")
    print("HIRES (Keck) data requires KOA authentication.")
    print("=" * 60)
    
    return provenance

if __name__ == '__main__':
    download_spectra()
