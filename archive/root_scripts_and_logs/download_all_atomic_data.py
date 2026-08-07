"""
Download all required atomic data from NIST using astroquery.nist
"""

import sys
sys.path.insert(0, '/Users/matthewsmawfield/www/Temporal Equivalence Principle/TEP-BBN')

from astroquery.nist import Nist
import astropy.units as u
import json
from datetime import datetime
from pathlib import Path

print("=" * 60)
print("Downloading All Atomic Data from NIST using astroquery.nist")
print("=" * 60)
print()

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
atomic_data_dir = Path('/Users/matthewsmawfield/www/Temporal Equivalence Principle/TEP-BBN/data/raw/atomic')
atomic_data_dir.mkdir(parents=True, exist_ok=True)

atomic_data_registry = {
    'download_date': datetime.now().isoformat(),
    'download_method': 'astroquery.nist (programmatic access to NIST ASD)',
    'nist_version': '5.11.1',
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
    
    print(f"  ✓ Saved data file: {data_file}")
    print(f"  ✓ Total lines: {len(all_lines)}")
    
    # Check for placeholder data
    if len(all_lines) == 0:
        print(f"  ⚠ WARNING: No lines found")
        atomic_data_registry['data'][element_key] = {
            'status': 'no_data',
            'file': str(data_file),
            'n_lines': len(all_lines),
            'warning': 'No lines found'
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
                'warning': f'Only {has_oscillator}/{len(all_lines)} lines have oscillator strengths'
            }
        else:
            print(f"  ✓ Real atomic data obtained: {len(all_lines)} lines with oscillator strengths")
            atomic_data_registry['data'][element_key] = {
                'status': 'real_data',
                'file': str(data_file),
                'n_lines': len(all_lines),
                'n_with_oscillator': has_oscillator,
                'download_method': 'astroquery.nist'
            }
    
    print()

# Save registry
output_path = '/Users/matthewsmawfield/www/Temporal Equivalence Principle/TEP-BBN/data/processed/atomic_data_registry.json'
Path('/Users/matthewsmawfield/www/Temporal Equivalence Principle/TEP-BBN/data/processed').mkdir(parents=True, exist_ok=True)
with open(output_path, 'w') as f:
    json.dump(atomic_data_registry, f, indent=2)

print("=" * 60)
print(f"Atomic data registry saved to {output_path}")
print("=" * 60)
