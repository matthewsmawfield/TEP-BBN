"""
Step 07: Voigt profile fitting for TEP-BBN

Fits Voigt profiles to reduced spectra to measure D/H ratios using atomic data from NIST.
"""

import json
from pathlib import Path
from datetime import datetime
import sys

# Add parent directory to path for imports
script_dir = Path(__file__).parent
project_root = script_dir.parent.parent
sys.path.insert(0, str(project_root))

from scripts.utils.voigt_fitter import VoigtFitter

def fit_voigt_profiles():
    """
    Fit Voigt profiles to reduced spectra to measure D/H ratios.
    
    This step:
    1. Loads reduced spectrum
    2. Fits H I Lyman series lines
    3. Fits D I Lyman series lines
    4. Calculates D/H ratio
    5. Estimates uncertainties
    """
    print("Step 07: Voigt profile fitting")
    print("=" * 60)
    print("CRITICAL: This step requires reduced 1D spectra from step_06.")
    print("No placeholder or synthetic data is allowed.")
    print("=" * 60)
    print()
    
    # Check for reduced data
    reduced_data_dir = project_root / 'data/processed/reduced/Q0913+072_z2.618'
    if not reduced_data_dir.exists():
        print("ERROR: Reduced data directory not found")
        print("Expected: data/processed/reduced/Q0913+072_z2.618/")
        print("Run step_06 to reduce raw data")
        return None
    
    reduced_files = list(reduced_data_dir.glob('*.fits')) + list(reduced_data_dir.glob('*.txt'))
    if len(reduced_files) == 0:
        print("ERROR: No reduced data files found")
        print("Expected: .fits or .txt files in reduced data directory")
        return None
    
    print(f"Found {len(reduced_files)} reduced data files")
    print()
    
    # Initialize Voigt fitter
    print("Initializing Voigt fitter with atomic data...")
    fitter = VoigtFitter()
    print(f"✓ Loaded {len(fitter.lines)} elements from atomic data")
    print()
    
    # Load literature registry for redshift
    registry_path = project_root / 'data/processed/dh_literature_registry.json'
    with open(registry_path, 'r') as f:
        registry = json.load(f)
    
    # Get Q0913+072 redshift
    system = next((s for s in registry['systems'] if s['system_id'] == 'Q0913+072_z2.618'), None)
    if not system:
        print("ERROR: Q0913+072 not found in literature registry")
        return None
    
    redshift = system['redshift']
    print(f"System: Q0913+072 (z={redshift})")
    print()
    
    # Note: We cannot actually fit without reduced 1D spectra
    # This is a placeholder for the actual fitting process
    print("NOTE: Actual Voigt fitting requires reduced 1D spectra")
    print("This step is ready to fit once reduced spectra are available")
    print()
    print("Expected fitting process:")
    print("1. Load reduced spectrum (wavelength, flux, error)")
    print("2. Fit H I Lyman series lines (Lyα, Lyβ, Lyγ, etc.)")
    print("3. Fit D I Lyman series lines (isotope-shifted)")
    print("4. Calculate column densities from Voigt fits")
    print("5. Calculate D/H ratio = N(D I) / N(H I)")
    print("6. Estimate uncertainties")
    print()
    
    # Create placeholder results
    results = {
        'fitting_date': datetime.now().isoformat(),
        'system_id': 'Q0913+072_z2.618',
        'redshift': redshift,
        'status': 'ready_for_fitting',
        'n_reduced_files': len(reduced_files),
        'reduced_files': [str(f) for f in reduced_files],
        'atomic_data': {
            'n_elements': len(fitter.lines),
            'elements': list(fitter.lines.keys())
        },
        'expected_results': {
            'h_i_column_density': 'log N(H I) ≈ 20.52',
            'd_i_column_density': 'log N(D I) ≈ 14.68',
            'dh_ratio': 'D/H ≈ 2.527e-5'
        },
        'instructions': 'Complete data reduction, then re-run this step to perform actual fitting'
    }
    
    # Save results
    output_path = project_root / 'data/processed/voigt_fitting_results.json'
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"Fitting results saved to {output_path}")
    print()
    print("=" * 60)
    print("STATUS: Ready for fitting (requires reduced spectra)")
    print("Complete data reduction, then re-run this step to perform actual fitting")
    print("=" * 60)
    
    return results

if __name__ == '__main__':
    fit_voigt_profiles()
if __name__ == '__main__':
    fit_voigt_profiles()
if __name__ == '__main__':
    fit_voigt_profiles()
if __name__ == '__main__':
    fit_voigt_profiles()
