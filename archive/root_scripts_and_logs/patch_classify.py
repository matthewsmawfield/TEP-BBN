import re

with open("scripts/steps/step_13c_nested_synthetic_adversarial_validation.py", "r") as f:
    code = f.read()

# Define the classify_result function
classify_result_code = """
def classify_result(logZs, logZerrs, posteriors):
    \"\"\"
    Applies the frozen adversarial Stage 13 gate to evaluate whether the 
    data exhibits a decisive, non-spurious TEP signature.
    Returns: (is_tep_win, classification_string, interpretation_string)
    \"\"\"
    best_TEP = max(['M1_full', 'M2_full'], key=lambda k: logZs.get(k, -1e9))
    best_non_TEP = max(['Mnull', 'M0', 'M3_global', 'M3_Dlocal', 'M3_centroid', 'M4_secondary_local'], key=lambda k: logZs.get(k, -1e9))
    
    delta_tep = logZs.get(best_TEP, 0) - logZs.get(best_non_TEP, 0)
    combined_err_tep = (logZerrs.get(best_TEP, 0)**2 + logZerrs.get(best_non_TEP, 0)**2)**0.5
    
    is_tep_win = (delta_tep > 2.0) and (delta_tep > combined_err_tep)
    reason = "TEP models decisively preferred over all non-TEP models."
    
    if is_tep_win:
        if best_TEP == 'M2_full':
            pdiag = posteriors.get('M2_full', {})
            pdiag_free = posteriors.get('M2_free_alpha', {})
            delta_sec = logZs.get('M2_full', 0) - logZs.get('M2_primary_only', 0)
            err_sec = (logZerrs.get('M2_full', 0)**2 + logZerrs.get('M2_primary_only', 0)**2)**0.5
            delta_m4 = logZs.get('M2_full', 0) - logZs.get('M4_secondary_local', 0)
            err_m4 = (logZerrs.get('M2_full', 0)**2 + logZerrs.get('M4_secondary_local', 0)**2)**0.5
            
            if pdiag.get('P_f_D_lt_0p5', 0) <= 0.95 or pdiag.get('alpha_at_lower_edge', True) or pdiag.get('alpha_at_upper_edge', True):
                is_tep_win = False
                reason = "M2_full preferred, but fails parameter posterior constraints (f_D or alpha edges)."
            elif pdiag_free.get('P_alpha_in_prior', 0) <= 0.95:
                is_tep_win = False
                reason = "M2_full preferred, but unconstrained alpha escapes the theoretical prior."
            elif delta_sec <= 2.0 or delta_sec <= err_sec:
                is_tep_win = False
                reason = "M2_full preferred, but secondary features are not decisively supported over primary-only."
            elif delta_m4 <= 2.0 or delta_m4 <= err_m4:
                is_tep_win = False
                reason = "M2_full preferred, but does not decisively beat local secondary interloper (M4)."
            elif posteriors.get('held_out_diff', 0.0) <= 0.0:
                is_tep_win = False
                reason = "M2_full preferred, but held-out secondary flux prediction performs worse than null."
        
        elif best_TEP == 'M1_full':
            pdiag_free = posteriors.get('M2_free_alpha', {})
            delta_sec = logZs.get('M1_full', 0) - logZs.get('M1_primary_only', logZs.get('M1_full', 0))
            err_sec = (logZerrs.get('M1_full', 0)**2 + logZerrs.get('M1_primary_only', 0)**2)**0.5
            delta_m4 = logZs.get('M1_full', 0) - logZs.get('M4_secondary_local', 0)
            err_m4 = (logZerrs.get('M1_full', 0)**2 + logZerrs.get('M4_secondary_local', 0)**2)**0.5
            
            if pdiag_free.get('P_alpha_in_prior', 0) <= 0.95:
                is_tep_win = False
                reason = "M1_full preferred, but unconstrained alpha escapes the theoretical prior."
            elif delta_sec <= 2.0 or delta_sec <= err_sec:
                is_tep_win = False
                reason = "M1_full preferred, but secondary features are not decisively supported over primary-only."
            elif delta_m4 <= 2.0 or delta_m4 <= err_m4:
                is_tep_win = False
                reason = "M1_full preferred, but does not decisively beat local secondary interloper (M4)."
            elif posteriors.get('held_out_diff', 0.0) <= 0.0:
                is_tep_win = False
                reason = "M1_full preferred, but held-out secondary flux prediction performs worse than null."
    
    if not is_tep_win:
        if delta_tep <= 0.0:
            reason = "Standard D / non-TEP models dominate or tie; TEP replacement criteria not satisfied."
        
    classification = "TEP_CANDIDATE" if is_tep_win else "REAL_NEGATIVE"
    return is_tep_win, classification, reason
"""

# Find where to insert it: before `def process_task`
if "def process_task" in code and "def classify_result" not in code:
    code = code.replace("def process_task", classify_result_code + "\n\ndef process_task")
    with open("scripts/steps/step_13c_nested_synthetic_adversarial_validation.py", "w") as f:
        f.write(code)
    print("Injected classify_result successfully.")

