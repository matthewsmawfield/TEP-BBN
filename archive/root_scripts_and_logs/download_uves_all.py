"""
Download UVES spectra from ESO archive for TEP-BBN

This downloads UVES (VLT) data which is publicly available.
Cooke et al. (2016) used both Keck/HIRES and VLT/UVES for different systems.
"""

import sys
sys.path.insert(0, '/Users/matthewsmawfield/www/Temporal Equivalence Principle/TEP-BBN')

from astroquery.eso import Eso
from pathlib import Path
import shutil
from datetime import datetime
import json

print("=" * 60)
print("Downloading UVES Spectra from ESO Archive for TEP-BBN")
print("=" * 60)
print()

# Create ESO instance
eso = Eso()

# Define programs to query (based on Cooke et al. 2016)
# Q0913+072: 68.B-0115 (UVES)
# Other systems may have different program IDs

programs = {
    '68.B-0115': {
        'qso': 'Q0913+072',
        'redshift': 2.618,
        'instrument': 'UVES'
    }
}

# Create output directory
output_dir = Path('/Users/matthewsmawfield/www/Temporal Equivalence Principle/TEP-BBN/data/raw/spectra')
output_dir.mkdir(parents=True, exist_ok=True)

provenance = {
    'download_date': datetime.now().isoformat(),
    'download_method': 'astroquery.eso (programmatic access to ESO archive)',
    'archive': 'ESO Science Archive',
    'archive_url': 'https://archive.eso.org/',
    'programs': {}
}

for prog_id, prog_info in programs.items():
    print(f"Querying program {prog_id} ({prog_info['qso']})...")
    
    try:
        # Query by program ID
        table = eso.query_main(column_filters={'prog_id': prog_id})
        print(f"  ✓ Found {len(table)} observations")
        
        # Filter for SCIENCE observations (not ACQUISITION)
        science_table = table[table['Category'] == 'SCIENCE']
        print(f"  ✓ {len(science_table)} SCIENCE observations")
        
        if len(science_table) > 0:
            # Get dataset IDs
            dataset_ids = science_table['Dataset ID']
            
            # Create system directory
            system_id = f"{prog_info['qso'].replace('+', '')}_z{prog_info['redshift']}"
            system_dir = output_dir / system_id
            system_dir.mkdir(parents=True, exist_ok=True)
            
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
                        downloaded_files.append(str(dest_file))
                        print(f"      ✓ Downloaded")
                    else:
                        print(f"      ✗ File not found in cache")
                        
                except Exception as e:
                    print(f"      ✗ Failed: {e}")
            
            print(f"  ✓ Downloaded {len(downloaded_files)} files to {system_dir}")
            
            provenance['programs'][prog_id] = {
                'qso': prog_info['qso'],
                'redshift': prog_info['redshift'],
                'instrument': prog_info['instrument'],
                'n_observations': len(science_table),
                'n_downloaded': len(downloaded_files),
                'files': downloaded_files,
                'status': 'success'
            }
            
        else:
            print(f"  ✗ No SCIENCE observations found")
            provenance['programs'][prog_id] = {
                'qso': prog_info['qso'],
                'status': 'no_science_observations'
            }
            
    except Exception as e:
        print(f"  ✗ Query failed: {e}")
        provenance['programs'][prog_id] = {
            'qso': prog_info['qso'],
            'status': 'query_failed',
            'error': str(e)
        }

# Save provenance
output_path = '/Users/matthewsmawfield/www/Temporal Equivalence Principle/TEP-BBN/data/processed/uves_provenance.json'
Path('/Users/matthewsmawfield/www/Temporal Equivalence Principle/TEP-BBN/data/processed').mkdir(parents=True, exist_ok=True)
with open(output_path, 'w') as f:
    json.dump(provenance, f, indent=2)

print()
print("=" * 60)
print(f"Provenance saved to {output_path}")
print("=" * 60)
print()
print("Note: This is UVES (VLT) data, not HIRES (Keck) data")
print("Cooke et al. (2016) used both instruments for different systems")
print("UVES data is publicly available from ESO archive")
print("HIRES data requires KOA authentication")
print("=" * 60)
