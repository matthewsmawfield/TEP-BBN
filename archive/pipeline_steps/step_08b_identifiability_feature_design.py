"""
Step 08b: Identifiability Feature Design for TEP-BBN

Defines an independently predicted proper-time feature that is not degenerate with velocity structure.
Replaces the deprecated step_08.
"""

import json
from pathlib import Path
from datetime import datetime
import sys

script_dir = Path(__file__).parent
project_root = script_dir.parent.parent
sys.path.insert(0, str(project_root))

def identifiability_feature_design():
    print("Step 08b: Identifiability Feature Design")
    print("=" * 60)
    
    # Check for DLA structure
    structure_path = project_root / 'data/processed/dla_structure_characterization.json'
    if not structure_path.exists():
        print("ERROR: DLA structure characterization not found")
        return None
        
    with open(structure_path, 'r') as f:
        dla_structure = json.load(f)
        
    # Analyze Candidate Features
    candidate_features = [
        {
            "name": "column_density",
            "independent": "Partial",
            "degeneracy_break": "Weak",
            "ready_for_mode_b": "Not alone"
        },
        {
            "name": "metal_line_coherence",
            "independent": "Yes",
            "degeneracy_break": "Stronger",
            "ready_for_mode_b": "Yes, if metals available"
        },
        {
            "name": "multi_lyman_coherence",
            "independent": "Yes",
            "degeneracy_break": "Medium/strong",
            "ready_for_mode_b": "Yes"
        },
        {
            "name": "environment_feature",
            "independent": "Yes",
            "degeneracy_break": "Strong in sample",
            "ready_for_mode_b": "Later"
        }
    ]

    results = {
        "gate": "Gate -1",
        "status": "feature_design",
        "claim_allowed": False,
        "candidate_features": candidate_features,
        "pass_conditions": [
            "Independent constraint on g_i from non-spectral data or metal lines",
            "Physical prediction of proper-time amplitude",
            "Must not use arbitrary free shear parameters"
        ],
        "blocking_issue": "Need an independently predicted proper-time feature not degenerate with velocity."
    }
    
    output_path = project_root / 'data/processed/gate_minus1_identifiability.json'
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)
        
    print("Gate -1 status: feature_design")
    print("Blocking issue: Need an independently predicted proper-time feature not degenerate with velocity.")
    print("Claim allowed: False")
    print(f"Results saved to {output_path}")
    
    return results

if __name__ == '__main__':
    identifiability_feature_design()
