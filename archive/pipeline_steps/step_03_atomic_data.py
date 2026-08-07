"""
Step 03: Atomic data download for TEP-BBN

Downloads and registers atomic data (wavelengths, oscillator strengths, etc.) from
NIST Atomic Spectra Database using astroquery.nist for programmatic access.

CRITICAL: This step downloads REAL data from NIST. No placeholder or synthetic data is allowed.
"""

import json
from datetime import datetime
from pathlib import Path
import sys
import hashlib

def calculate_sha256(filepath):
    """Calculate SHA-256 checksum of a file."""
    sha256_hash = hashlib.sha256()
    with open(filepath, 'rb') as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def download_atomic_data():
    """
    Download atomic data with full provenance tracking using astroquery.nist.
    
    For TEP-BBN, we need atomic data for:
    - H I (Lyman series: Lyα, Lyβ, Lyγ, Lyδ, Lyε)
    - D I (same series, isotope-shifted)
    - Metal lines (O I, Si II, C II, Fe II for null tests)
    
    Source: NIST Atomic Spectra Database (ASD)
    Method: astroquery.nist for programmatic access
    Version: 5.11.1 (fixed)
    
    CRITICAL: This step downloads REAL data from NIST using astroquery.nist.
    """
    print("Step 03: Atomic data download (using astroquery.nist)")
    print("=" * 60)
    print("CRITICAL: This step downloads REAL data from NIST ASD.")
    print("No placeholder or synthetic data is allowed.")
    print("=" * 60)
    print()
    
    # Check if astroquery is available
    try:
        from astroquery.nist import Nist
        import astropy.units as u
        print("✓ astroquery is available")
    except ImportError:
        print("✗ astroquery is not installed")
        print("Install with: pip install astroquery")
        sys.exit(1)
    except Exception as e:
        print(f"✗ astroquery import failed: {e}")
        sys.exit(1)
    
    # Define required atomic data
    required_elements = {
        'H_I': {
            'element': 'Hydrogen',
            'ion': 'I',
            'transitions': ['Lyα', 'Lyβ', 'Lyγ', 'Lyδ', 'Lyε'],
            'wavelength_ranges': [(1215.0, 1216.0), (1025.0, 1026.0), (972.0, 973.0), (949.0, 950.0), (937.0, 938.0)]
        },
        'D_I': {
            'element': 'Deuterium',
            'ion': 'I',
            'transitions': ['Lyα', 'Lyβ', 'Lyγ', 'Lyδ', 'Lyε'],
            'wavelength_ranges': [(1215.0, 1216.0), (1025.0, 1026.0), (972.0, 973.0), (949.0, 950.0), (937.0, 938.0)]
        },
        'O_I': {
            'element': 'Oxygen',
            'ion': 'I',
            'transitions': ['1302 Å', '1304 Å'],
            'wavelength_ranges': [(1302.0, 1303.0), (1304.0, 1305.0)]
        },
        'Si_II': {
            'element': 'Silicon',
            'ion': 'II',
            'transitions': ['1526 Å', '1304 Å'],
            'wavelength_ranges': [(1526.0, 1527.0), (1304.0, 1305.0)]
        },
        'C_II': {
            'element': 'Carbon',
            'ion': 'II',
            'transitions': ['1334 Å', '1036 Å'],
            'wavelength_ranges': [(1334.0, 1335.0), (1036.0, 1037.0)]
        },
        'Fe_II': {
            'element': 'Iron',
            'ion': 'II',
            'transitions': ['1608 Å', '1144 Å'],
            'wavelength_ranges': [(1608.0, 1609.0), (1144.0, 1145.0)]
        }
    }
    
    # Create output directory
    atomic_data_dir = Path('../../data/raw/atomic')
    atomic_data_dir.mkdir(parents=True, exist_ok=True)
    
    atomic_data_registry = {
        'download_date': datetime.now().isoformat(),
        'download_method': 'astroquery.nist (programmatic access to NIST ASD)',
        'nist_version': '5.11.1',
        'nist_url': 'https://physics.nist.gov/ASD',
        'elements': list(required_elements.keys()),
        'data': {}
    }
    
    for element_key, element_data in required_elements.items():
        print(f"Processing element: {element_key}")
        
        # Create element directory
        element_dir = atomic_data_dir / element_key
        element_dir.mkdir(parents=True, exist_ok=True)
        
        # Query NIST for each wavelength range
        all_lines = []
        
        for i, (transition, wavelength_range) in enumerate(zip(element_data['transitions'], element_data['wavelength_ranges'])):
            print(f"  Querying {transition} ({wavelength_range[0]}-{wavelength_range[1]} Å)...")
            
            try:
                table = Nist.query(wavelength_range[0] * u.AA, wavelength_range[1] * u.AA, linename=f"{element_data['element']} {element_data['ion']}")
                
                if len(table) > 0:
                    print(f"    ✓ Found {len(table)} lines")
                    
                    # Extract relevant columns
                    for row in table:
                        line_data = {
                            'transition': transition,
                            'wavelength': float(row['Observed']) if 'Observed' in row.colnames and row['Observed'] != '--' else None,
                            'wavelength_ritz': float(row['Ritz']) if 'Ritz' in row.colnames and row['Ritz'] != '--' else None,
                            'oscillator_strength': float(row['Aki']) if 'Aki' in row.colnames and row['Aki'] != '--' else None,
                            'transition_prob': float(row['fik']) if 'fik' in row.colnames and row['fik'] != '--' else None,
                            'lower_level': str(row['Lower level']) if 'Lower level' in row.colnames else None,
                            'upper_level': str(row['Upper level']) if 'Upper level' in row.colnames else None
                        }
                        all_lines.append(line_data)
                else:
                    print(f"    ✗ No lines found")
                    
            except Exception as e:
                print(f"    ✗ Query failed: {e}")
        
        # Save atomic data
        data_file = element_dir / f'{element_key}_lines.txt'
        with open(data_file, 'w') as f:
            f.write(f"# Atomic data for {element_data['element']} {element_data['ion']}\n")
            f.write(f"# Source: NIST ASD 5.11.1\n")
            f.write(f"# URL: https://physics.nist.gov/ASD\n")
            f.write(f"# Downloaded: {datetime.now().isoformat()}\n")
            f.write(f"# Method: astroquery.nist (programmatic access)\n")
            f.write("#\n")
            f.write("# Format: wavelength (Å)  oscillator_strength  transition  lower_level  upper_level\n")
            f.write("#\n")
            
            for line in all_lines:
                if line['wavelength'] is not None:
                    f.write(f"{line['wavelength']:.4f}  ")
                    if line['oscillator_strength'] is not None:
                        f.write(f"{line['oscillator_strength']:.4e}  ")
                    else:
                        f.write("N/A  ")
                    f.write(f"{line['transition']}  ")
                    if line['lower_level'] is not None:
                        f.write(f"{line['lower_level'][:50]}  ")
                    if line['upper_level'] is not None:
                        f.write(f"{line['upper_level'][:50]}")
                    f.write("\n")
        
        # Calculate checksum
        checksum = calculate_sha256(data_file)
        
        print(f"  ✓ Saved data file: {data_file}")
        print(f"  ✓ SHA-256: {checksum[:16]}...")
        print(f"  ✓ Total lines: {len(all_lines)}")
        
        # Check for placeholder data
        if len(all_lines) == 0:
            print(f"  ✗ ERROR: No lines found")
            atomic_data_registry['data'][element_key] = {
                'status': 'no_data',
                'file': str(data_file),
                'n_lines': len(all_lines),
                'checksum': checksum,
                'error': 'No lines found'
            }
        else:
            # Check if all lines have oscillator strengths
            has_oscillator = sum(1 for line in all_lines if line['oscillator_strength'] is not None)
            if has_oscillator < len(all_lines):
                print(f"  ⚠ WARNING: Only {has_oscillator}/{len(all_lines)} lines have oscillator strengths")
                atomic_data_registry['data'][element_key] = {
                    'status': 'partial_data',
                    'file': str(data_file),
                    'n_lines': len(all_lines),
                    'n_with_oscillator': has_oscillator,
                    'checksum': checksum,
                    'warning': f'Only {has_oscillator}/{len(all_lines)} lines have oscillator strengths'
                }
            else:
                print(f"  ✓ Real atomic data obtained: {len(all_lines)} lines with oscillator strengths")
                atomic_data_registry['data'][element_key] = {
                    'status': 'real_data',
                    'file': str(data_file),
                    'n_lines': len(all_lines),
                    'n_with_oscillator': has_oscillator,
                    'checksum': checksum,
                    'download_method': 'astroquery.nist'
                }
        
        print()
    
    # Save registry
    output_path = '../../data/processed/atomic_data_registry.json'
    with open(output_path, 'w') as f:
        json.dump(atomic_data_registry, f, indent=2)
    
    print("=" * 60)
    print(f"Atomic data registry saved to {output_path}")
    print("=" * 60)
    print()
    print("Note: This uses astroquery.nist for programmatic access to NIST.")
    print("Some transitions may not be found or may have N/A oscillator strengths.")
    print("Please verify the downloaded data against the NIST web interface.")
    print("=" * 60)
    
    return atomic_data_registry

if __name__ == '__main__':
    download_atomic_data()
