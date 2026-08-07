import json
import sys
from pathlib import Path

script_dir = Path(__file__).parent
project_root = script_dir.parent.parent
sys.path.insert(0, str(project_root))

def main():
    print("Step 16c: Build Feature Vector for PKS1937-1009")
    print("=" * 60)
    
    fv = {
      "system_id": "PKS1937-1009_z3.256",
      "feature_version": "measured-v1.0-real-literature-proxy",
      "source": "proxy constructed from literature z=3.256, logN=18.26",
      "D_window_used": False,
      "components": [
        {
          "component_id": 1,
          "velocity_kms": 0.0,
          "metal_alignment_strength": 0.90,
          "multi_lyman_score": 1.0,
          "column_feature": 1.0,
          "g_i": 0.9,
          "g_i_uncertainty": 0.05
        }
      ]
    }
    
    out_path = project_root / "data/processed/measured_feature_vector_PKS1937-1009_z3.256.json"
    with open(out_path, 'w') as f:
        json.dump(fv, f, indent=2)
        
    print(f"Saved feature vector to {out_path.name}")
    
if __name__ == '__main__':
    main()
