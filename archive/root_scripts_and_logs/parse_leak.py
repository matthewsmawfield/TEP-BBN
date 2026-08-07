import json, math

with open('data/processed/stage1_v8_results.json', 'r') as f:
    results = json.load(f)

leaks = 0
for i, res in enumerate(results):
    logZs = res['logZs']
    logZerrs = res['logZerrs']
    best_TEP = max(['M1_full', 'M2_full'], key=lambda k: logZs[k])
    best_non_TEP = max(['Mnull', 'M0', 'M3_global', 'M3_Dlocal', 'M3_centroid', 'M4_secondary_local'], key=lambda k: logZs[k])
    
    delta_tep = logZs[best_TEP] - logZs[best_non_TEP]
    combined_err_tep = math.sqrt(logZerrs[best_TEP]**2 + logZerrs[best_non_TEP]**2)
    
    is_tep_win = (delta_tep > 2.0) and (delta_tep > combined_err_tep)
    
    if is_tep_win:
        pdiag_free_p_alpha = res['p_alpha_in_prior']
        if best_TEP == 'M2_full':
            delta_sec = logZs['M2_full'] - logZs.get('M2_primary_only', logZs['M2_full'])
            err_sec = math.sqrt(logZerrs['M2_full']**2 + logZerrs.get('M2_primary_only', 0)**2)
            delta_m4 = logZs['M2_full'] - logZs['M4_secondary_local']
            err_m4 = math.sqrt(logZerrs['M2_full']**2 + logZerrs['M4_secondary_local']**2)
            
            p_f_D_lt_0p5 = res['p_f_D_lt_0p5']
            alpha_edge = res['alpha_edge']
            
            if p_f_D_lt_0p5 <= 0.95 or alpha_edge:
                is_tep_win = False
            elif pdiag_free_p_alpha <= 0.95:
                is_tep_win = False
            elif delta_sec <= 2.0 or delta_sec <= err_sec:
                is_tep_win = False
            elif delta_m4 <= 2.0 or delta_m4 <= err_m4:
                is_tep_win = False
            elif res['held_out_diff'] <= 0.0:
                is_tep_win = False
        elif best_TEP == 'M1_full':
            delta_sec = logZs['M1_full'] - logZs.get('M1_primary_only', logZs['M1_full'])
            err_sec = math.sqrt(logZerrs['M1_full']**2 + logZerrs.get('M1_primary_only', 0)**2)
            delta_m4 = logZs['M1_full'] - logZs['M4_secondary_local']
            err_m4 = math.sqrt(logZerrs['M1_full']**2 + logZerrs['M4_secondary_local']**2)
            
            if pdiag_free_p_alpha <= 0.95:
                is_tep_win = False
            elif delta_sec <= 2.0 or delta_sec <= err_sec:
                is_tep_win = False
            elif delta_m4 <= 2.0 or delta_m4 <= err_m4:
                is_tep_win = False
            elif res['held_out_diff'] <= 0.0:
                is_tep_win = False

    if is_tep_win:
        leaks += 1
        print(f"Leaked Seed ID {i}!")
        print(f"  Best TEP: {best_TEP} ({logZs[best_TEP]:.2f})")

print(f"Total leaks: {leaks}")
