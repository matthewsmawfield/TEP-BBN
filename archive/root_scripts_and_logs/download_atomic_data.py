"""
Download atomic data from NIST using astroquery.nist
"""

import sys
sys.path.insert(0, '/Users/matthewsmawfield/www/Temporal Equivalence Principle/TEP-BBN')

print("=" * 60)
print("Downloading Atomic Data from NIST using astroquery.nist")
print("=" * 60)
print()

# Check if astroquery is available
try:
    from astroquery.nist import Nist
    import astropy.units as u
    print("✓ astroquery is available")
except ImportError:
    print("✗ astroquery is not installed")
    print("Attempting to install...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "astroquery"])
    from astroquery.nist import Nist
    import astropy.units as u
    print("✓ astroquery installed")

print()

# Download H I Lyman series
print("Downloading H I Lyman series data...")
h_i_lines = []
for i, (transition, wavelength_range) in enumerate([
    ('Lyα', (1215.0, 1216.0)),
    ('Lyβ', (1025.0, 1026.0)),
    ('Lyγ', (972.0, 973.0)),
    ('Lyδ', (949.0, 950.0)),
    ('Lyε', (937.0, 938.0))
]):
    print(f"  Querying {transition} ({wavelength_range[0]}-{wavelength_range[1]} Å)...")
    try:
        table = Nist.query(wavelength_range[0] * u.AA, wavelength_range[1] * u.AA, linename="H I")
        print(f"    Found {len(table)} lines")
        if len(table) > 0:
            print(f"    Columns: {table.colnames}")
            print(f"    First line: {table[0]}")
            h_i_lines.append(table)
    except Exception as e:
        print(f"    Error: {e}")

print()
print(f"Total H I lines downloaded: {len(h_i_lines)}")

# Save data
import json
from datetime import datetime
from pathlib import Path

atomic_data_dir = Path('/Users/matthewsmawfield/www/Temporal Equivalence Principle/TEP-BBN/data/raw/atomic')
atomic_data_dir.mkdir(parents=True, exist_ok=True)

h_i_dir = atomic_data_dir / 'H_I'
h_i_dir.mkdir(parents=True, exist_ok=True)

data_file = h_i_dir / 'H_I_lines.txt'
with open(data_file, 'w') as f:
    f.write(f"# Atomic data for Hydrogen I\n")
    f.write(f"# Source: NIST ASD 5.11.1\n")
    f.write(f"# URL: https://physics.nist.gov/ASD\n")
    f.write(f"# Downloaded: {datetime.now().isoformat()}\n")
    f.write(f"# Method: astroquery.nist (programmatic access)\n")
    f.write("#\n")
    f.write("# Format: wavelength (Å)  oscillator_strength  transition\n")
    f.write("#\n")
    
    for table in h_i_lines:
        for row in table:
            wavelength = float(row['Observed']) if 'Observed' in row.colnames else None
            oscillator_strength = float(row['Aki']) if 'Aki' in row.colnames else None
            
            if wavelength is not None:
                f.write(f"{wavelength:.4f}  ")
                if oscillator_strength is not None:
                    f.write(f"{oscillator_strength:.4e}")
                else:
                    f.write("N/A")
                f.write("\n")

print(f"✓ Saved H I data to {data_file}")

print()
print("=" * 60)
print("Atomic data download complete")
print("=" * 60)
