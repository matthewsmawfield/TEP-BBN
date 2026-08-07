"""
Step 25: Phase G2 Rule 2 Derivation

Develops the Rule 2 executable prediction rule with a strict Stage A (Activation) gate.
Uses the 4 development systems (Q1009, Q0913, J1419, PKS1937) to derive a screening
law based on g_i.

Structure:
Stage A: System-level Activation/Null Gate
Stage B: Component Selection (conditional on Stage A)
Stage C: Sign and Ranking (conditional on Stage A)
"""

import json
from pathlib import Path
import sys
import hashlib
from datetime import datetime, timezone

script_dir = Path(__file__).parent
project_root = script_dir.parent.parent
sys.path.insert(0, str(project_root))

def apply_tep_rule_2(system_manifest):
    components = system_manifest.get("components", [])
    if not components:
        return {
            "predicted_component": None,
            "predicted_velocity_kms": None,
            "sign": None,
            "p_null": 1.0,
            "rank_score": 0.0,
            "prediction_level": 3,
            "rule_class": "CHAMELEON_SCREENING_GATE"
        }
        
    best_comp = max(components, key=lambda c: c.get("g_i", 0.0))
    max_gi = best_comp.get("g_i", 0.0)
    
    # Stage A: Activation Gate
    # Chameleon screening: highly dense/deep potential environments screen the TEP fifth-force effect.
    # Therefore, if max_gi is too high (> 0.75), the system is strongly screened (NULL).
    # If max_gi <= 0.75, the system is weakly screened (ACTIVE).
    if max_gi > 0.75:
        p_null = 1.0
    else:
        p_null = 0.0
        
    if p_null == 1.0:
        return {
            "predicted_component": None,
            "predicted_velocity_kms": None,
            "sign": None,
            "p_null": 1.0,
            "rank_score": 0.0,
            "prediction_level": 3,
            "rule_class": "CHAMELEON_SCREENING_GATE"
        }
        
    # Stage B & C: Conditional Component and Sign/Ranking
    return {
        "predicted_component": best_comp.get("component_id"),
        "predicted_velocity_kms": best_comp.get("velocity_kms"),
        "sign": "BLUEWARD",
        "p_null": p_null,
        "rank_score": max_gi, 
        "prediction_level": 3,
        "rule_class": "CHAMELEON_SCREENING_GATE"
    }

def main():
    print("=" * 60)
    print("Phase G2: Rule 2 Derivation (Activation Gate)")
    print("=" * 60)
    
    roles_path = project_root / "data/processed/phase_g_system_roles.json"
    with open(roles_path, "r") as f:
        roles = json.load(f)
        
    dev_systems = roles["system_roles"]["DEVELOPMENT"]
    
    results = {}
    for sys_id in dev_systems:
        manifest_path = project_root / f"data/processed/measured_feature_vector_{sys_id}.json"
        
        if not manifest_path.exists():
            print(f"Warning: Manifest for {sys_id} not found at {manifest_path}")
            continue
            
        with open(manifest_path, "r") as f:
            manifest = json.load(f)
            
        prediction = apply_tep_rule_2(manifest)
        
        manifest_str = json.dumps(manifest, sort_keys=True)
        input_hash = hashlib.sha256(manifest_str.encode()).hexdigest()
        prediction["allowed_input_hash"] = input_hash
        
        print(f"\nSystem: {sys_id}")
        if prediction["p_null"] < 0.5:
            print("  Stage A: ACTIVE")
            print(f"  Stage B: Predicted Component ID: {prediction['predicted_component']} (v={prediction.get('predicted_velocity_kms')} km/s)")
            print(f"  Stage C: Sign={prediction['sign']}, Rank={prediction['rank_score']}")
        else:
            print("  Stage A: NULL")
            
        results[sys_id] = prediction
        
    # Derivation gate check
    # Q1009 -> ACTIVE
    # Q0913 -> NULL
    # J1419 -> NULL
    # PKS1937 -> NULL
    q1009_active = results["Q1009+2956_z2.504"]["p_null"] == 0.0
    q0913_null = results["Q0913+072"]["p_null"] == 1.0
    j1419_null = results["J1419+0829_z3.049840"]["p_null"] == 1.0
    pks1937_null = results["PKS1937-1009_z3.256"]["p_null"] == 1.0
    
    if q1009_active and q0913_null and j1419_null and pks1937_null:
        print("\nSTATUS: TEP_ACTIVATION_LAW_DERIVED")
        print("Rule 2 perfectly separates the 4 development systems according to the screening hypothesis.")
        
        out_path = project_root / "data/processed/phase_g_dev2_predictions.json"
        with open(out_path, "w") as f:
            json.dump(results, f, indent=2)
            
        print("Proceed to seal Rule 2 and predict for new Validation tier.")
    else:
        print("\nSTATUS: TEP_ABSORBER_ACTIVATION_LAW_NOT_DERIVED")
        print("Rule 2 failed to match the mandatory development state matrix.")

if __name__ == "__main__":
    main()
