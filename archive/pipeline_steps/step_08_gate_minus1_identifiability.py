"""
Step 08: Gate -1 Identifiability for TEP-BBN

Determines whether the proposed TEP proper-time observable is distinguishable from ordinary velocity structure.

This is a critical gate before any spectral evidence can be claimed.
"""

import json
from pathlib import Path
from datetime import datetime
import sys

# Add parent directory to path for imports
script_dir = Path(__file__).parent
project_root = script_dir.parent.parent
sys.path.insert(0, str(project_root))

def gate_minus1_identifiability():
    """
    Gate -1: Identifiability test for TEP proper-time observable.
    
    This step:
    1. Tests whether TEP proper-time shear is distinguishable from velocity
    2. Checks for degeneracy with ordinary H I velocity blending
    3. Determines if the observable is physically meaningful
    """
    print("Step 08: Gate -1 Identifiability")
    print("=" * 60)
    print("CRITICAL: This step tests TEP proper-time identifiability.")
    print("No placeholder or synthetic data is allowed.")
    print("=" * 60)
    print()
    
    print("Gate -1 Question:")
    print("  Can the proposed TEP proper-time observable be distinguished")
    print("  from ordinary velocity/redshift structure?")
    print()
    
    # Load DLA structure characterization
    structure_path = project_root / 'data/processed/dla_structure_characterization.json'
    if not structure_path.exists():
        print("ERROR: DLA structure characterization not found")
        print("Run step_09 to characterize DLA structure")
        return None
    
    with open(structure_path, 'r') as f:
        dla_structure = json.load(f)
    
    print(f"System: {dla_structure['system_id']}")
    print()
    
    # Core identifiability analysis
    print("Identifiability Analysis:")
    print()
    
    print("Problem:")
    print("  A component-level proper-time shift is almost exactly")
    print("  degenerate with an ordinary velocity shift unless constrained")
    print("  independently.")
    print()
    
    print("Mathematical degeneracy:")
    print("  v_obs,i = v_kin,i + c * δa_i")
    print("  where δa_i = ln A_i - ln A_bar")
    print()
    print("  A free δa_i can be absorbed into a redefined z_i.")
    print("  So if the pipeline simply adds a free ΔlnA_i, it has not")
    print("  discovered proper-time shear. It has just renamed velocity.")
    print()
    
    print("Requirement for identifiability:")
    print("  The TEP model must NOT use arbitrary free shear parameters.")
    print("  It must predict them from absorber/environment features:")
    print("  δa_i = α * g_i")
    print("  where g_i is fixed from non-spectral or independently")
    print("  constrained absorber properties.")
    print()
    
    # Current assessment
    print("Current Pipeline Assessment:")
    print()
    
    print("Feature models tested:")
    print("  - S1: Density gradient (g_i = ln(ρ_i/ρ₀))")
    print("  - S2: Column density gradient (g_i = ln(N_i/N₀))")
    print("  - Toy: Power law (g_i = (ρ/ρ₀)^β (L/L₀)^γ)")
    print()
    
    print("Identifiability status:")
    print("  - Feature models use component structure")
    print("  - No independent observable separating proper-time shear")
    print("  from velocity blending")
    print("  - Currently NOT identifiable against ordinary H I interlopers")
    print()
    
    # Gate decision
    print("Gate -1 Decision:")
    print()
    print("  Status: NOT_YET_IDENTIFIABLE")
    print("  Reason: Current feature model uses component structure but")
    print("          no independent observable separating proper-time")
    print("          shear from velocity blending.")
    print()
    print("  Claim allowed: False")
    print()
    
    print("Required for identifiability:")
    print("  1. Independent constraint on g_i from non-spectral data")
    print("  2. Physical prediction of proper-time amplitude")
    print("  3. Test against M3 (H I interloper model)")
    print("  4. Correlation with absorber environment")
    print()
    
    # Create results
    results = {
        'gate': 'Gate -1',
        'gate_name': 'Identifiability',
        'analysis_date': datetime.now().isoformat(),
        'system_id': dla_structure['system_id'],
        'question': 'Can the proposed TEP proper-time observable be distinguished from ordinary velocity structure?',
        'status': 'not_yet_identifiable',
        'reason': 'Current feature model uses component structure but no independent observable separating proper-time shear from velocity blending.',
        'claim_allowed': False,
        'analysis_mode': 'literature_feasibility',
        'evidence_level': 'toy_only',
        
        'identifiability_analysis': {
            'degeneracy_warning': 'Component-level proper-time shift is degenerate with velocity shift unless independently constrained',
            'mathematical_form': 'v_obs,i = v_kin,i + c * δa_i',
            'requirement': 'δa_i must be predicted from absorber/environment features, not fitted freely',
            'current_status': 'Feature models use component structure but lack independent constraints'
        },
        
        'required_for_identifiability': [
            'Independent constraint on g_i from non-spectral data',
            'Physical prediction of proper-time amplitude',
            'Test against M3 (H I interloper model)',
            'Correlation with absorber environment'
        ],
        
        'notes': 'Gate -1 must pass before Gate 0 can be interpreted as physically meaningful. Currently fails identifiability test.'
    }
    
    # Save results
    output_path = project_root / 'data/processed/gate_minus1_identifiability.json'
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"Gate -1 identifiability results saved to {output_path}")
    print()
    print("=" * 60)
    print("STATUS: Gate -1 - NOT_YET_IDENTIFIABLE")
    print("Claim allowed: False")
    print("Next step: Required coupling calculation (Step 10)")
    print("Note: Gate 0 results cannot be interpreted as physically")
    print("      meaningful until Gate -1 passes identifiability test.")
    print("=" * 60)
    
    return results

if __name__ == '__main__':
    gate_minus1_identifiability()
