import numpy as np
import json
import math
from dynesty import NestedSampler
import sys
import warnings
import concurrent.futures
from pathlib import Path
warnings.filterwarnings('ignore')

from step_13c_nested_synthetic_adversarial_validation import base_model, fit_model_nested, v_grid

def process_task(args):
    truth_name, snr, seed = args
    np.random.seed(seed * 1000 + snr)
    
    truth_params_base = {'c0': 1.0, 'c1': 0.0, 'c2': 0.0, 'v_shift': 0.0, 'lsf_scale': 1.0}
    truth_flux = base_model({**truth_params_base, 'int_v': -82.0, 'int_n': 2.5e-5, 'int_b': 8.0}, apply_misspecification=True)
    
    noise = 1.0 / snr
    noisy_data = truth_flux + np.random.normal(0, noise, len(v_grid))
    
    models = ['Mnull', 'M0', 'M1_full', 'M1_primary_only', 'M2_full', 'M2_primary_only', 'M2_free_alpha', 'M3_global', 'M3_Dlocal']
    logZs = {}
    logZerrs = {}
    posteriors = {}
    
    for m in models:
        lz, lzerr, pdiag = fit_model_nested(noisy_data, m, noise)
        logZs[m] = lz
        logZerrs[m] = lzerr
        posteriors[m] = pdiag
        
    v_int_samples = np.array(posteriors['M3_Dlocal']['v_int_samples'])
    v_int_weights = np.array(posteriors['M3_Dlocal']['weights'])
    v_hat = np.average(v_int_samples, weights=v_int_weights)
    sigma_v = np.sqrt(np.average((v_int_samples - v_hat)**2, weights=v_int_weights))
    half_width = max(1.0, 3 * sigma_v)
    centroid_bounds = [v_hat - half_width, v_hat + half_width]
    
    lz, lzerr, pdiag = fit_model_nested(noisy_data, 'M3_centroid', noise, centroid_bounds=centroid_bounds)
    logZs['M3_centroid'] = lz
    logZerrs['M3_centroid'] = lzerr
    posteriors['M3_centroid'] = pdiag
    
    best_TEP = max(['M1_full', 'M2_full'], key=lambda k: logZs[k])
    best_non_TEP = max(['Mnull', 'M0', 'M3_global', 'M3_Dlocal', 'M3_centroid'], key=lambda k: logZs[k])
    
    delta_tep = logZs[best_TEP] - logZs[best_non_TEP]
    combined_err_tep = math.sqrt(logZerrs[best_TEP]**2 + logZerrs[best_non_TEP]**2)
    
    is_tep_win = (delta_tep > 2.0) and (delta_tep > combined_err_tep)
    
    if is_tep_win:
        if best_TEP == 'M2_full':
            pdiag = posteriors['M2_full']
            pdiag_free = posteriors['M2_free_alpha']
            delta_sec = logZs['M2_full'] - logZs['M2_primary_only']
            err_sec = math.sqrt(logZerrs['M2_full']**2 + logZerrs['M2_primary_only']**2)
            
            if pdiag['P_f_D_lt_0p5'] <= 0.95 or pdiag['alpha_at_lower_edge'] or pdiag['alpha_at_upper_edge']:
                is_tep_win = False
            elif pdiag_free['P_alpha_in_prior'] <= 0.95:
                is_tep_win = False
            elif delta_sec <= 2.0 or delta_sec <= err_sec:
                is_tep_win = False
        elif best_TEP == 'M1_full':
            delta_sec = logZs['M1_full'] - logZs['M1_primary_only']
            err_sec = math.sqrt(logZerrs['M1_full']**2 + logZerrs['M1_primary_only']**2)
            if delta_sec <= 2.0 or delta_sec <= err_sec:
                is_tep_win = False
                
    if is_tep_win:
        out = {
            "seed": seed,
            "truth": "M3_exact_D",
            "M2_full_logZ": logZs.get('M2_full'),
            "M2_primary_only_logZ": logZs.get('M2_primary_only'),
            "M3_centroid_logZ": logZs.get('M3_centroid'),
            "best_non_TEP": best_non_TEP,
            "best_non_TEP_logZ": logZs.get(best_non_TEP),
            "delta_M2full_minus_primary": logZs.get('M2_full', 0) - logZs.get('M2_primary_only', 0),
            "delta_M2full_minus_M3centroid": logZs.get('M2_full', 0) - logZs.get('M3_centroid', 0),
            "f_D_mean": posteriors.get('M2_full', {}).get('f_D_mean'),
            "P_f_D_lt_0p5": posteriors.get('M2_full', {}).get('P_f_D_lt_0p5'),
            "alpha_mean": posteriors.get('M2_full', {}).get('alpha_mean'),
            "P_alpha_blind": posteriors.get('M2_free_alpha', {}).get('P_alpha_in_prior')
        }
        return out
    return None

def main():
    snr = 50
    seeds = range(60)
    tasks = [('M3_exact_D', snr, seed) for seed in seeds]
    
    print(f"Running M3_exact_D debug for {len(tasks)} seeds...")
    with concurrent.futures.ProcessPoolExecutor() as executor:
        futures = {executor.submit(process_task, t): t for t in tasks}
        for future in concurrent.futures.as_completed(futures):
            res = future.result()
            if res is not None:
                print(json.dumps(res, indent=2))

if __name__ == '__main__':
    main()
