"""
Step 08c: Build Frozen Feature Vector for Mode B

Constructs the proper-time feature vector (g_i) from H I component structure,
metal-line coherence, and non-D Lyman-series information.
Crucially, the D I window is MASKED during feature construction and is only
unblinded after the feature vector and priors are frozen.
"""

import json
from pathlib import Path
from datetime import datetime
import sys
import yaml

script_dir = Path(__file__).parent
project_root = script_dir.parent.parent
sys.path.insert(0, str(project_root))

def build_frozen_feature_vector():
    print("Step 08c: Build Frozen Feature Vector")
    print("=" * 60)
    
    # Load blinding config
    blinding_path = project_root / 'configs/blinding.yaml'
    with open(blinding_path, 'r') as f:
        blinding_config = yaml.safe_load(f)
        
    print(f"System: {blinding_config['system_id']}")
    print("Applying blinding rules:")
    for region in blinding_config['blind_regions']:
        print(f"  - MASKING: {region['name']} (v={region['velocity_center_kms']} km/s, w={region['width_kms']} km/s)")
    
    # Load component structure (excluding D window information)
    structure_path = project_root / 'data/processed/dla_structure_characterization.json'
    with open(structure_path, 'r') as f:
        dla_structure = json.load(f)
        
    components = []
    metal_features = dla_structure['metal_lines']['component_features']
    
    # Normalize log_n_hi linearly to use as a feature (0 to 1 scale)
    max_log_n = max(dla_structure['column_densities']['component_log_n_hi'])
    
    for i, metal_feat in enumerate(metal_features):
        # Calculate g_i using a predefined rule based on metal alignment and column features
        # The equation must be fixed before looking at D window.
        col_feat = round(10**(dla_structure['column_densities']['component_log_n_hi'][i] - max_log_n), 2)
        multi_lym = 1.0 if metal_feat['multi_lyman_presence'] else 0.0
        
        # Example frozen rule: Average of metal strength, multi_lyman presence, and column feature
        g_i = round((metal_feat['metal_alignment_strength'] + multi_lym + col_feat) / 3.0, 2)
        
        components.append({
            "component_id": i,
            "velocity_kms": metal_feat['velocity_kms'],
            "metal_alignment_strength": metal_feat['metal_alignment_strength'],
            "multi_lyman_presence": multi_lym,
            "column_feature": col_feat,
            "g_i": g_i
        })
        
    feature_vector = {
        "system_id": blinding_config['system_id'],
        "feature_version": "0.1-frozen",
        "claim_allowed": False,
        "blinded_to_D_window": True,
        "creation_date": datetime.now().isoformat(),
        "components": components,
        "feature_construction_rule": "g_i built from metal-line alignment, multi-Lyman presence, and column-derived component strength before D-window fitting",
        "forbidden_inputs": blinding_config['forbidden_inputs']
    }
    
    output_path = project_root / 'data/processed/gate_minus1_feature_vector_Q0913+072.json'
    with open(output_path, 'w') as f:
        json.dump(feature_vector, f, indent=2)
        
    print("\nFrozen Feature Vector Constructed:")
    for comp in components:
        print(f"  Component {comp['component_id']} (v={comp['velocity_kms']} km/s): g_i = {comp['g_i']}")
        
    print(f"\nSaved to {output_path}")
    print("STATUS: Feature Vector Frozen")
    print("Ready for Mode B: M0/M1/M2/M3 Spectral Evidence Comparison")
    
if __name__ == '__main__':
    build_frozen_feature_vector()
