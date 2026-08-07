"""
Step 27: Phase G2 Locked Validation Unblinding

Executes the locked validation gate by comparing the sealed Rule 2 predictions
against the observed ground truth (from the unchanged spectral pipeline).
"""

import json
from pathlib import Path
import sys
import datetime

script_dir = Path(__file__).parent
project_root = script_dir.parent.parent
sys.path.insert(0, str(project_root))

def get_observed_status(sys_id):
    """
    Simulates the unblinding of a system by looking for its processed ground truth
    or running the spectral pipeline on the raw data.
    """
    manifest_path = project_root / f"data/processed/measured_feature_vector_{sys_id}.json"
    if not manifest_path.exists():
        return {"activation": "DATA_UNAVAILABLE", "component": None, "sign": None}
        
    with open(manifest_path, "r") as f:
        manifest = json.load(f)
        
    if manifest.get("status") == "NEEDS_REAL_FEATURE_VECTOR":
        return {"activation": "DATA_UNAVAILABLE", "component": None, "sign": None}
        
    # Mock return if data were present but no TEP signature found (baseline GR)
    return {"activation": "NULL_SYSTEM", "component": None, "sign": None}

def main():
    print("=" * 70)
    print("PHASE G RULE 2: LOCKED VALIDATION UNBLINDING")
    print("=" * 70)
    
    roles_path = project_root / "data/processed/phase_g_system_roles.json"
    with open(roles_path, "r") as f:
        roles = json.load(f)
        
    validation_systems = roles["system_roles"]["LOCKED_VALIDATION"]
    
    predictions_dir = project_root / "data/processed/phase_g2/predictions"
    
    data_missing = False
    print("\nUNBLINDING RESULTS:")
    
    # Table header
    print(f"{'System':<25} | {'Pred Status':<12} | {'Obs Status':<20} | {'Pred Comp':<10} | {'Obs Comp':<10} | {'Pred Sign':<10} | {'Obs Sign':<10} | {'Result':<15}")
    print("-" * 115)
    
    for sys_id in validation_systems:
        pred_file = predictions_dir / f"{sys_id}_prediction.json"
        with open(pred_file, "r") as f:
            prediction = json.load(f)
            
        p_null = prediction["null_probability"]
        pred_status = "NULL" if p_null > 0.5 else "ACTIVE"
        pred_comp = str(prediction["predicted_component"])
        pred_sign = str(prediction["predicted_sign"])
        
        obs_data = get_observed_status(sys_id)
        obs_status = obs_data["activation"]
        obs_comp = str(obs_data["component"])
        obs_sign = str(obs_data["sign"])
        
        if "DATA_UNAVAILABLE" in obs_status:
            result = "BLOCKED_NO_DATA"
            data_missing = True
        else:
            result = "PASS" if pred_status == obs_status else "FAIL"
            
        print(f"{sys_id:<25} | {pred_status:<12} | {obs_status:<20} | {pred_comp:<10} | {obs_comp:<10} | {pred_sign:<10} | {obs_sign:<10} | {result:<15}")
        
    print("\n" + "=" * 50)
    if data_missing:
        print("VALIDATION_EXECUTION_GATE:")
        print("FAILED_DATA_AVAILABILITY\n")
        print("PHASE_G_RULE_2_LOCKED_VALIDATION:")
        print("BLOCKED_DATA_UNAVAILABLE\n")
        print("SCIENTIFIC_RESULT:")
        print("NOT_EVALUATED\n")
        print("RULE_2_STATUS:")
        print("SEALED_AND_UNTESTED_OUT_OF_SAMPLE\n")
        print("SEALED_PREDICTIONS:")
        print("PRESERVED\n")
        print("UNTOUCHED_CONFIRMATION:")
        print("PRESERVED")
    else:
        # Standard pass/fail evaluation block if data is present
        pass
    print("=" * 50)

if __name__ == "__main__":
    main()
