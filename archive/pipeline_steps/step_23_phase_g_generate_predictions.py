"""
Step 23: Phase G Prediction Generation

Generates sealed predictions for ALL systems (Development, Retrospective, Untouched)
using the sealed rule, strictly before candidate window unblinding.
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
    components = system_manifest.get("components", [])
    if not components:
        return {
            "predicted_component": None,
            "predicted_velocity_kms": None,
            "sign": None,
            "p_null": 1.0,
            "rank_score": 0.0,
            "prediction_level": 2,
            "rule_class": "DEVELOPMENT_CALIBRATED_TEP_RULE"
        }
        
    best_comp = max(components, key=lambda c: c.get("g_i", 0.0))
    max_gi = best_comp.get("g_i", 0.0)
    
    p_null = 0.0 if max_gi >= 0.01 else 1.0
        
    return {
        "predicted_component": best_comp.get("component_id"),
        "predicted_velocity_kms": best_comp.get("velocity_kms"),
        "sign": "BLUEWARD",
        "p_null": p_null,
        "rank_score": max_gi,
        "prediction_level": 2,
        "rule_class": "DEVELOPMENT_CALIBRATED_TEP_RULE"
    }

def main():
    print("Generating Sealed Predictions for All Systems...")
    
    roles_path = project_root / "data/processed/phase_g_system_roles.json"
    with open(roles_path, "r") as f:
        roles = json.load(f)
        
    predictions_dir = project_root / "data/processed/phase_g/predictions"
    predictions_dir.mkdir(parents=True, exist_ok=True)
    
    # Read script hash (predictor hash)
    with open(__file__, "r") as f:
        predictor_code = f.read()
    predictor_hash = hashlib.sha256(predictor_code.encode()).hexdigest()
    
    all_systems = []
    for role, sys_list in roles["system_roles"].items():
        for sys_id in sys_list:
            all_systems.append((sys_id, role))
            
    for sys_id, role in all_systems:
        manifest_path = project_root / f"data/processed/measured_feature_vector_{sys_id}.json"
        
        if not manifest_path.exists():
            print(f"Skipping {sys_id}: Manifest not found.")
            continue
            
        with open(manifest_path, "r") as f:
            manifest = json.load(f)
            
        prediction_core = apply_tep_rule(manifest)
        
        manifest_str = json.dumps(manifest, sort_keys=True)
        input_hash = hashlib.sha256(manifest_str.encode()).hexdigest()
        
        sealed_time = datetime.now(timezone.utc).isoformat()
        
        full_prediction = {
            "system_id": sys_id,
            "role": role,
            "predicted_component": prediction_core["predicted_component"],
            "predicted_velocity_kms": prediction_core["predicted_velocity_kms"],
            "predicted_sign": prediction_core["sign"],
            "null_probability": prediction_core["p_null"],
            "rank_score": prediction_core["rank_score"],
            "input_hash": input_hash,
            "predictor_hash": predictor_hash,
            "sealed_at": sealed_time
        }
        
        out_file = predictions_dir / f"{sys_id}_prediction.json"
        with open(out_file, "w") as f:
            json.dump(full_prediction, f, indent=2)
            
        print(f"Sealed prediction for {sys_id} ({role}) -> {out_file.name}")

if __name__ == "__main__":
    main()
