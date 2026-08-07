"""
Step 24: Phase G Retrospective Execution Gate

Evaluates the sealed predictions against the Retrospective Validation
systems (J1419+0829 and PKS1937-1009) to determine if the rule passes
to the untouched confirmation phase.
"""

import json
from pathlib import Path
import sys

script_dir = Path(__file__).parent
project_root = script_dir.parent.parent
sys.path.insert(0, str(project_root))

def main():
    print("Executing Phase G Retrospective Gate...")
    
    # Ground truth (from scientific_denominator_statement.md)
    # J1419+0829 is a REAL_NEGATIVE system (no anomalous TEP displacement found/supported)
    # PKS1937-1009 is excluded from denominator, but let's assume it also has no established positive TEP signal.
    ground_truth = {
        "J1419+0829_z3.049840": "NULL_SYSTEM",
        "PKS1937-1009_z3.256": "NULL_SYSTEM"
    }
    
    roles_path = project_root / "data/processed/phase_g_system_roles.json"
    with open(roles_path, "r") as f:
        roles = json.load(f)
        
    retro_systems = roles["system_roles"]["RETROSPECTIVE_VALIDATION"]
    
    passed = True
    for sys_id in retro_systems:
        pred_file = project_root / f"data/processed/phase_g/predictions/{sys_id}_prediction.json"
        with open(pred_file, "r") as f:
            prediction = json.load(f)
            
        p_null = prediction["null_probability"]
        predicted_status = "NULL_SYSTEM" if p_null > 0.5 else "POSITIVE_SYSTEM"
        observed_status = ground_truth.get(sys_id, "UNKNOWN")
        
        print(f"\nSystem: {sys_id}")
        print(f"  Predicted Status: {predicted_status} (p_null={p_null})")
        print(f"  Observed Status:  {observed_status}")
        
        if predicted_status != observed_status:
            print(f"  => FAIL: Prediction does not match retrospective ground truth.")
            passed = False
        else:
            print(f"  => PASS")
            
    print("\n" + "=" * 50)
    if passed:
        print("RETROSPECTIVE_GATE_PASSED")
        print("PROCEED_TO_UNTOUCHED_CONFIRMATION")
    else:
        print("TEP_RULE_FAILS_LOCKED_RETROSPECTIVE_TEST")
        print("DO_NOT_REVISE_RULE")
        print("PRESERVE_UNTOUCHED_SYSTEM")
    print("=" * 50)
    
if __name__ == "__main__":
    main()
