"""
Step 07: Literature D/H import for TEP-BBN

Imports published D/H values from literature for TEP-BBN analysis.

Note: This step does NOT perform actual Voigt profile fitting.
It imports literature D/H values for literature-feasibility mode analysis.
For spectral evidence mode, real Voigt fitting with VPFIT is required.
"""

import json
from pathlib import Path
from datetime import datetime
import sys

# Add parent directory to path for imports
script_dir = Path(__file__).parent
project_root = script_dir.parent.parent
sys.path.insert(0, str(project_root))

def import_literature_dh():
    """
    Import literature D/H values for TEP-BBN analysis.
    
    This step:
    1. Loads literature registry
    2. Imports literature D/H value from published results
    3. Provides D/H for literature-feasibility mode analysis
    4. Does NOT perform actual Voigt profile fitting
    """
    print("Step 07: Literature D/H import")
    print("=" * 60)
    print("CRITICAL: This step imports literature D/H values.")
    print("No placeholder or synthetic data is allowed.")
    print("NOTE: This does NOT perform actual Voigt profile fitting.")
    print("For spectral evidence mode, use VPFIT or real fitter.")
    print("=" * 60)
    print()
    
    # Load literature registry for D/H values
    registry_path = project_root / 'data/processed/dh_literature_registry.json'
    if not registry_path.exists():
        print("ERROR: Literature registry not found")
        print("Expected: data/processed/dh_literature_registry.json")
        print("Run step_01 to create literature registry")
        return None
    
    with open(registry_path, 'r') as f:
        registry = json.load(f)
    
    # Get Q0913+072 D/H value from literature
    system = next((s for s in registry['systems'] if s['system_id'] == 'Q0913+072_z2.618'), None)
    if not system:
        print("ERROR: Q0913+072 not found in literature registry")
        return None
    
    redshift = system['redshift']
    literature_dh = system['dh_ratio']
    print(f"System: Q0913+072 (z={redshift})")
    print(f"Literature D/H: {literature_dh:.2e}")
    print(f"Source: Cooke et al. (2016)")
    print()
    
    # Create results
    results = {
        'import_date': datetime.now().isoformat(),
        'system_id': 'Q0913+072_z2.618',
        'redshift': redshift,
        'status': 'literature_import_complete',
        'literature_dh': literature_dh,
        'literature_source': 'Cooke et al. (2016)',
        'analysis_mode': 'literature_feasibility',
        'evidence_level': 'literature_only',
        'claim_allowed': False,
        'notes': 'This is literature D/H import, not actual Voigt fitting. For spectral evidence mode, real Voigt fitting with VPFIT is required.'
    }
    
    # Save results
    output_path = project_root / 'data/processed/literature_dh_import.json'
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"Literature D/H import saved to {output_path}")
    print()
    print("=" * 60)
    print("STATUS: Literature D/H import complete")
    print("Analysis mode: literature_feasibility")
    print("Evidence level: literature_only")
    print("Claim allowed: False (requires spectral evidence mode)")
    print("=" * 60)
    
    return results

if __name__ == '__main__':
    import_literature_dh()
