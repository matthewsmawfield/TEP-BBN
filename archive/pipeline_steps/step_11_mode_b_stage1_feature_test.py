"""
Step 11: Mode B Identifiability Gate Execution

Tests whether the measured proper-time feature vector (g_i), combined with a
frozen TEP prior, correctly predicts an interval that contains the apparent
D feature location. Uses exact permutation enumeration for small N.
"""

import json
from pathlib import Path
from datetime import datetime
import sys
import yaml
import itertools

script_dir = Path(__file__).parent
project_root = script_dir.parent.parent
sys.path.insert(0, str(project_root))

def run_identifiability_gate():
    print("Step 11: Mode B Identifiability Gate")
    print("=" * 60)
    
    # 1. Load measured feature vector
    feature_path = project_root / 'data/processed/measured_feature_vector_Q0913+072.json'
    if not feature_path.exists():
        print("ERROR: Measured feature vector not found.")
        return
        
    with open(feature_path, 'r') as f:
        features = json.load(f)
        
    # 2. Load frozen derived prior
    prior_path = project_root / 'configs/tep_priors.yaml'
    with open(prior_path, 'r') as f:
        tep_priors = yaml.safe_load(f)
        
    prior_info = tep_priors['priors']['proper_time_shear']
    alpha_lower = prior_info['alpha_shear_lower']
    alpha_upper = prior_info['alpha_shear_upper']
    prior_status = prior_info.get('status', 'unknown')
    
    print(f"System: {features['system_id']}")
    print(f"Feature version: {features['feature_version']}")
    print(f"D Window Used: {features['D_window_used']}")
    print(f"Prior Status: {prior_status}")
    print(f"Frozen Prior [alpha_lower, alpha_upper]: [{alpha_lower}, {alpha_upper}]")
    print()
    
    if prior_status != 'derived' or features['D_window_used'] != False:
        print("FAIL: Identifiability rules violated. Prior must be derived and feature must be blinded.")
        return

    components = features['components']
    
    # Identify primary (dense) and secondary (sparse) components
    max_diff = -1
    primary, secondary = None, None
    for i in range(len(components)):
        for j in range(len(components)):
            if components[i]['g_i'] > components[j]['g_i']:
                diff = components[i]['g_i'] - components[j]['g_i']
                if diff > max_diff:
                    max_diff = diff
                    primary = components[i]
                    secondary = components[j]

    # --- Test 1: Prior-Predictive Location Interval ---
    print("Test 1: Prior-Predictive Location Interval")
    c = 299792.0
    v_kin_diff = secondary['velocity_kms'] - primary['velocity_kms']
    g_diff = secondary['g_i'] - primary['g_i']
    
    v_pred_1 = v_kin_diff + c * alpha_lower * g_diff
    v_pred_2 = v_kin_diff + c * alpha_upper * g_diff
    interval_min, interval_max = min(v_pred_1, v_pred_2), max(v_pred_1, v_pred_2)
    
    actual_D_shift = -82.0 # Unblinded for evaluation only
    location_pass = (interval_min <= actual_D_shift <= interval_max)
    print(f"Predicted interval: [{interval_min:.2f}, {interval_max:.2f}] km/s")
    print(f"Location pass: {location_pass}\n")
    
    # --- Test 2: Information Content (Coverage Fraction) ---
    print("Test 2: Information Content (Coverage Fraction)")
    allowed_search_window = 150.0 # Plausible velocity span for high-z lines
    interval_width = abs(interval_max - interval_min)
    coverage_fraction = interval_width / allowed_search_window
    coverage_pass = (coverage_fraction < 0.25)
    print(f"Coverage fraction: {coverage_fraction:.3f} (Limit: 0.25)")
    print(f"Coverage pass: {coverage_pass}\n")

    # --- Test 3: Null Feature Test (Exact Permutation) ---
    print("Test 3: Null Feature Test (Exact Permutation)")
    g_values = [c['g_i'] for c in components]
    unique_perms = list(set(itertools.permutations(g_values)))
    hits = 0
    
    for perm in unique_perms:
        t_primary = max(zip(components, perm), key=lambda x: x[1])
        t_secondary = min(zip(components, perm), key=lambda x: x[1])
        
        t_v_kin_diff = t_secondary[0]['velocity_kms'] - t_primary[0]['velocity_kms']
        t_g_diff = t_secondary[1] - t_primary[1]
        
        t_v_pred_1 = t_v_kin_diff + c * alpha_lower * t_g_diff
        t_v_pred_2 = t_v_kin_diff + c * alpha_upper * t_g_diff
        t_min, t_max = min(t_v_pred_1, t_v_pred_2), max(t_v_pred_1, t_v_pred_2)
        
        if t_min <= actual_D_shift <= t_max:
            hits += 1
            
    n_perms = len(unique_perms)
    false_positive_rate = hits / n_perms
    resolution_limit = 1.0 / n_perms
    print(f"Null test type: exact_permutation")
    print(f"N unique permutations: {n_perms}")
    print(f"Hits: {hits}")
    print(f"False positive rate: {false_positive_rate:.3f}")
    print(f"Single-system resolution limit: {resolution_limit:.3f}")
    
    # We do NOT artificially lower the threshold. 
    # If the system cannot pass p < 0.05, it cannot pass as a final gate.
    null_test_pass = (false_positive_rate < 0.05)
    print(f"Null test pass: {null_test_pass}\n")

    overall_pass = location_pass and coverage_pass and null_test_pass
    
    # Reclassify Q0913+072 as a prototype if it has too few components
    system_role = "final_discovery_gate" if null_test_pass else "prototype_single_system"
    can_proceed = True if (location_pass and coverage_pass) else False
    
    # Save results
    results = {
        "system_id": features['system_id'],
        "timestamp": datetime.now().isoformat(),
        "feature_vector_frozen": True,
        "alpha_prior_status": prior_status,
        "D_window_used_for_feature": features['D_window_used'],
        "system_classification": {
            "system_role": system_role,
            "can_pass_identifiability_gate_alone": overall_pass,
            "can_proceed_to_model_comparison": can_proceed,
            "claim_scope": "one-system exploratory evidence only" if not overall_pass else "final_discovery"
        },
        "tests": {
            "D_inside_predicted_interval": location_pass,
            "coverage_fraction": coverage_fraction,
            "null_test": {
                "type": "exact_permutation",
                "n_unique_permutations": n_perms,
                "hits": hits,
                "false_positive_rate": false_positive_rate,
                "single_system_resolution_limit": resolution_limit
            }
        },
        "overall_pass": overall_pass,
        "claim_allowed": False
    }
    
    output_path = project_root / 'data/processed/identifiability_gate_results.json'
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)

    print("=" * 60)
    print(f"SYSTEM ROLE: {system_role.upper()}")
    if can_proceed:
        print("Model is authorized to proceed to evidence testing (M0/M1/M2/M3)")
        print("as ONE-SYSTEM EXPLORATORY EVIDENCE ONLY.")
    else:
        print("Model fails basic coverage or location tests. Do not proceed.")
    print("=" * 60)

if __name__ == '__main__':
    run_identifiability_gate()
