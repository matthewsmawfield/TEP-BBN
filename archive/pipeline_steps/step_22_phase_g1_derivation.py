"""
Step 22: Phase G1 Prediction Rule Derivation

Develops and freezes a simple, executable TEP prediction rule (Level 2)
using ONLY permitted non-D observables from the development systems.

Rule Class: DEVELOPMENT_CALIBRATED_TEP_RULE
"""

import json
from pathlib import Path
import sys
import hashlib
from datetime import datetime, timezone

script_dir = Path(__file__).parent
project_root = script_dir.parent.parent
sys.path.insert(0, str(project_root))

def apply_tep_rule(system_manifest):
    """
    Executable TEP Level-2 Prediction Rule.
    Maps non-D inputs to {predicted_component, sign, null_prob, rank_score}
    
    Rules:
    - Rule A (Component & Null): The component with the highest environmental 
      proxy 'g_i' is designated the 'least screened eligible component'.
      If the maximum g_i is extremely low (< 0.01), it is flagged as a null system.
    - Rule B (Sign & Rank): TEP conformal endpoint convention dictates a BLUEWARD 
      apparent shift for deeper potentials. Systems are cross-ranked by max g_i.
    - Rule C: (Omitted - bounded displacement velocity is not yet rigorously 
      supported without further modeling. Restricting to Level-2).
    """
    
    components = system_manifest.get("components", [])
    if not components:
        return {
            "predicted_component": None,
            "sign": None,
            "p_null": 1.0,
            "rank_score": 0.0,
            "prediction_level": 2,
            "rule_class": "DEVELOPMENT_CALIBRATED_TEP_RULE"
        }
        
    # Find the component with the highest g_i
    best_comp = max(components, key=lambda c: c.get("g_i", 0.0))
    max_gi = best_comp.get("g_i", 0.0)
    
    p_null = 0.0
    if max_gi < 0.01:
        p_null = 1.0
        
    return {
        "predicted_component": best_comp.get("component_id"),
        "predicted_velocity_kms": best_comp.get("velocity_kms"),
        "sign": "BLUEWARD",
        "p_null": p_null,
        "rank_score": max_gi, # Used for cross-system ranking
        "prediction_level": 2,
        "rule_class": "DEVELOPMENT_CALIBRATED_TEP_RULE"
    }

def main():
    print("=" * 60)
    print("Phase G1: Bounded Derivation Sprint")
    print("=" * 60)
    
    # Load development systems
    roles_path = project_root / "data/processed/phase_g_system_roles.json"
    with open(roles_path, "r") as f:
        roles = json.load(f)
        
    dev_systems = roles["system_roles"]["DEVELOPMENT"]
    print(f"Development Systems: {dev_systems}")
    
    results = {}
    for sys_id in dev_systems:
        # Load non-D feature vector
        # Account for possible suffixes in file name based on existing structures
        manifest_path = project_root / f"data/processed/measured_feature_vector_{sys_id}.json"
        
        if not manifest_path.exists():
            print(f"Warning: Manifest for {sys_id} not found at {manifest_path}")
            continue
            
        with open(manifest_path, "r") as f:
            manifest = json.load(f)
            
        prediction = apply_tep_rule(manifest)
        
        # Calculate a pseudo input hash to log
        manifest_str = json.dumps(manifest, sort_keys=True)
        input_hash = hashlib.sha256(manifest_str.encode()).hexdigest()
        
        prediction["allowed_input_hash"] = input_hash
        
        print(f"\nSystem: {sys_id}")
        print(f"  Predicted Component ID: {prediction['predicted_component']} (v={prediction.get('predicted_velocity_kms')} km/s)")
        print(f"  Predicted Sign: {prediction['sign']}")
        print(f"  Null Probability: {prediction['p_null']}")
        print(f"  Rank Score (g_i): {prediction['rank_score']}")
        
        results[sys_id] = prediction
        
    # Stress test check (Did it produce non-nulls and select components?)
    if all(res['p_null'] > 0.5 for res in results.values()):
        print("\nSTATUS: TEP_ABSORBER_PREDICTION_RULE_NOT_YET_DERIVED")
        print("Reason: Rule failed to identify any positive development signals.")
    else:
        print("\nSTATUS: TEP_PREDICTION_RULE_DERIVED")
        
        out_path = project_root / "data/processed/phase_g_dev_predictions.json"
        with open(out_path, "w") as f:
            json.dump(results, f, indent=2)
        print(f"\nRule outputs and input hashes saved to {out_path}.")
        print("Proceed to seal TEP_BBN_PHASE_G_PREDICTION_CONTRACT.md.")

if __name__ == "__main__":
    main()
