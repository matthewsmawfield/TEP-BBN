def classify_result(logZs, logZerrs, posteriors):
    """
    Applies the frozen adversarial Stage 13 gate to evaluate whether the 
    data exhibits a decisive, non-spurious TEP signature.
    Returns: (is_tep_win, classification_string, interpretation_string)
    """
    best_TEP = max(['M1_full', 'M2_full'], key=lambda k: logZs[k])
    best_non_TEP = max(['Mnull', 'M0', 'M3_global', 'M3_Dlocal', 'M3_centroid', 'M4_secondary_local'], key=lambda k: logZs[k])
    
    delta_tep = logZs[best_TEP] - logZs[best_non_TEP]
    combined_err_tep = math.sqrt(logZerrs[best_TEP]**2 + logZerrs[best_non_TEP]**2)
    
    is_tep_win = (delta_tep > 2.0) and (delta_tep > combined_err_tep)
    reason = "TEP models decisively preferred over all non-TEP models."
    
    if is_tep_win:
        if best_TEP == 'M2_full':
            pdiag = posteriors.get('M2_full', {})
            pdiag_free = posteriors.get('M2_free_alpha', {})
            delta_sec = logZs['M2_full'] - logZs['M2_primary_only']
            err_sec = math.sqrt(logZerrs['M2_full']**2 + logZerrs['M2_primary_only']**2)
            delta_m4 = logZs['M2_full'] - logZs['M4_secondary_local']
            err_m4 = math.sqrt(logZerrs['M2_full']**2 + logZerrs['M4_secondary_local']**2)
            
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
            delta_sec = logZs['M1_full'] - logZs.get('M1_primary_only', logZs['M1_full'])
            err_sec = math.sqrt(logZerrs['M1_full']**2 + logZerrs.get('M1_primary_only', 0)**2)
            delta_m4 = logZs['M1_full'] - logZs['M4_secondary_local']
            err_m4 = math.sqrt(logZerrs['M1_full']**2 + logZerrs['M4_secondary_local']**2)
            
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

def process_task(args):","StartLine":263,"TargetContent":"    if model_type == 'M2_primary_only':
        ml_idx = np.argmax(res.logl)
        post_diag['ml_sample'] = res.samples[ml_idx].tolist()
        
    return res.logz[-1], res.logzerr[-1], post_diag

def process_task(args):"},{"AllowMultiple":false,"EndLine":496,"ReplacementContent":"            # Decisive false TEP
            is_tep_win, classification, reason = classify_result(logZs, logZerrs, posteriors)
            
            if is_tep_win:","StartLine":453,"TargetContent":"            # Decisive false TEP
            best_TEP = max(['M1_full', 'M2_full'], key=lambda k: logZs[k])
            best_non_TEP = max(['Mnull', 'M0', 'M3_global', 'M3_Dlocal', 'M3_centroid', 'M4_secondary_local'], key=lambda k: logZs[k])
            
            delta_tep = logZs[best_TEP] - logZs[best_non_TEP]
            combined_err_tep = math.sqrt(logZerrs[best_TEP]**2 + logZerrs[best_non_TEP]**2)
            
            is_tep_win = (delta_tep > 2.0) and (delta_tep > combined_err_tep)
            
            if is_tep_win:
                if best_TEP == 'M2_full':
                    pdiag = posteriors['M2_full']
                    pdiag_free = posteriors['M2_free_alpha']
                    delta_sec = logZs['M2_full'] - logZs['M2_primary_only']
                    err_sec = math.sqrt(logZerrs['M2_full']**2 + logZerrs['M2_primary_only']**2)
                    delta_m4 = logZs['M2_full'] - logZs['M4_secondary_local']
                    err_m4 = math.sqrt(logZerrs['M2_full']**2 + logZerrs['M4_secondary_local']**2)
                    
                    if pdiag['P_f_D_lt_0p5'] <= 0.95 or pdiag['alpha_at_lower_edge'] or pdiag['alpha_at_upper_edge']:
                        is_tep_win = False
                    elif pdiag_free['P_alpha_in_prior'] <= 0.95:
                        is_tep_win = False
                    elif delta_sec <= 2.0 or delta_sec <= err_sec:
                        is_tep_win = False
                    elif delta_m4 <= 2.0 or delta_m4 <= err_m4:
                        is_tep_win = False
                    elif posteriors.get('held_out_diff', 0.0) <= 0.0:
                        is_tep_win = False
                elif best_TEP == 'M1_full':
                    pdiag_free = posteriors['M2_free_alpha']
                    delta_sec = logZs['M1_full'] - logZs.get('M1_primary_only', logZs['M1_full'])
                    err_sec = math.sqrt(logZerrs['M1_full']**2 + logZerrs.get('M1_primary_only', 0)**2)
                    delta_m4 = logZs['M1_full'] - logZs['M4_secondary_local']
                    err_m4 = math.sqrt(logZerrs['M1_full']**2 + logZerrs['M4_secondary_local']**2)
                    
                    if pdiag_free['P_alpha_in_prior'] <= 0.95:
                        is_tep_win = False
                    elif delta_sec <= 2.0 or delta_sec <= err_sec:
                        is_tep_win = False
                    elif delta_m4 <= 2.0 or delta_m4 <= err_m4:
                        is_tep_win = False
                    elif posteriors.get('held_out_diff', 0.0) <= 0.0:
                        is_tep_win = False
                        
            if is_tep_win:"}],"TargetFile":"/Users/matthewsmawfield/www/Temporal Equivalence Principle/TEP-BBN/scripts/steps/step_13c_nested_synthetic_adversarial_validation.py","toolAction":"Patching step 13c","toolSummary":"Expose classify_result from 13c"}}]}
