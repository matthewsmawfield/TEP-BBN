import numpy as np
import json
import math
from dynesty import NestedSampler
from dynesty.utils import resample_equal
import sys
import warnings
import concurrent.futures
from pathlib import Path
warnings.filterwarnings('ignore')

def voigt_profile(x, center, sigma, gamma):
    from scipy.special import wofz
    z = ((x - center) + 1j * gamma) / (sigma * np.sqrt(2.0))
    v = wofz(z).real / (sigma * np.sqrt(2.0 * np.pi))
    return v

script_dir = Path(__file__).parent
project_root = script_dir.parent.parent


def set_system_feature_vector(fv_data):
    global components, hi_comps, primary_idx
    components = fv_data['components']
    hi_comps = []
    for comp in components:
        v = comp['velocity_kms']
        n_hi = 1.0 * comp['metal_alignment_strength'] 
        hi_comps.append({'v': v, 'n': n_hi, 'b': 12.0, 'g_i': comp['g_i']})
        
    primary_idx = 0
    for i, comp in enumerate(components):
        if comp.get('column_feature', 0.0) == 1.0:
            primary_idx = i
            break

# Initialize with Q0913+072 to avoid breaking scripts that run step_13c directly
import json
with open(project_root / 'data/processed/measured_feature_vector_Q0913+072.json', 'r') as f:
    set_system_feature_vector(json.load(f))
c_kms = 299792.458
alpha_prior = [0.0005, 0.0009]
v_grid = np.linspace(-300, 100, 800)
x_norm = (v_grid - v_grid[0]) / (v_grid[-1] - v_grid[0]) * 2.0 - 1.0

def base_model(params_dict, apply_misspecification=False, tep_primary_only=False):
    c0 = params_dict.get('c0', 1.0)
    c1 = params_dict.get('c1', 0.0)
    c2 = params_dict.get('c2', 0.0)
    flux = c0 + c1 * x_norm + c2 * (x_norm**2)
    if apply_misspecification:
        flux += 0.01 * np.sin(2.0 * np.pi * x_norm) 
        
    v_shift = params_dict.get('v_shift', 0.0)
    lsf_scale = params_dict.get('lsf_scale', 1.0)
    v_eval = v_grid - v_shift
    scale_hi = 20.0  
    scale_di = 1.0e5 
        
    for hc in hi_comps:
        b_eff = hc['b'] * lsf_scale
        if apply_misspecification:
            b_eff *= 1.05 
        flux -= hc['n'] * voigt_profile(v_eval, hc['v'], b_eff, 0.1) * scale_hi
        
    if 'B_abs' in params_dict:
        B_abs = params_dict['B_abs']
        f_D = params_dict.get('f_D', 1.0)
        alpha = params_dict.get('alpha', 0.0)
        primary_comp = next((c for c in components if c.get('column_feature', 0.0) == 1.0), components[0])
        g_primary = primary_comp['g_i']
        
        for i, hc in enumerate(hi_comps):
            g_i = components[i]['g_i']
            b_d = (hc['b'] / math.sqrt(2)) * lsf_scale
            margin = max(3 * b_d, 2 * 10.0)
            if f_D > 0:
                v_d = hc['v'] - 82.0
                n_d = hc['n'] * B_abs * f_D
                if (v_grid[0] + margin) <= v_d <= (v_grid[-1] - margin):
                    flux -= n_d * voigt_profile(v_eval, v_d, b_d, 0.1) * scale_di
            if f_D < 1.0:
                if tep_primary_only and i != primary_idx:
                    continue
                v_p = hc['v'] - 82.0 + c_kms * alpha * (g_i - g_primary)
                n_p = hc['n'] * B_abs * (1.0 - f_D)
                if (v_grid[0] + margin) <= v_p <= (v_grid[-1] - margin):
                    flux -= n_p * voigt_profile(v_eval, v_p, b_d, 0.1) * scale_di
                    
    if 'int_v' in params_dict:
        v_int = params_dict['int_v']
        n_int = params_dict['int_n']
        b_int = params_dict['int_b'] * lsf_scale
        flux -= n_int * voigt_profile(v_eval, v_int, b_int, 0.1) * scale_di
        
    if 'sec_v' in params_dict:
        v_sec = params_dict['sec_v']
        n_sec = params_dict['sec_n']
        b_sec = params_dict['sec_b'] * lsf_scale
        flux -= n_sec * voigt_profile(v_eval, v_sec, b_sec, 0.1) * scale_di
        
    if apply_misspecification:
        flux -= 2.5e-6 * voigt_profile(v_eval, -110.0, 5.0, 0.1) * scale_di
    return flux

def fit_model_nested(truth_data, model_type, noise_level, centroid_bounds=None, sec_windows=None):
    base_bounds = [(0.90, 1.10), (-0.1, 0.1), (-0.1, 0.1), (-1.0, 1.0), (0.9, 1.1)]
    
    if model_type == 'Mnull':
        bounds = base_bounds
        def ptform(u):
            x = np.array(u)
            for i, b in enumerate(bounds): x[i] = u[i] * (b[1] - b[0]) + b[0]
            return x
        def logl(x):
            p = {'c0': x[0], 'c1': x[1], 'c2': x[2], 'v_shift': x[3], 'lsf_scale': x[4]}
            return -0.5 * np.sum(((truth_data - base_model(p)) / noise_level)**2)
        ndim = 5
    elif model_type == 'M0':
        bounds = base_bounds + [(0, 1e-4)]
        def ptform(u):
            x = np.array(u)
            for i, b in enumerate(bounds): x[i] = u[i] * (b[1] - b[0]) + b[0]
            return x
        def logl(x):
            p = {'c0': x[0], 'c1': x[1], 'c2': x[2], 'v_shift': x[3], 'lsf_scale': x[4], 'B_abs': x[5], 'f_D': 1.0}
            return -0.5 * np.sum(((truth_data - base_model(p)) / noise_level)**2)
        ndim = 6
    elif model_type == 'M1_full':
        bounds = base_bounds + [(0, 1e-4), alpha_prior]
        def ptform(u):
            x = np.array(u)
            for i, b in enumerate(bounds): x[i] = u[i] * (b[1] - b[0]) + b[0]
            return x
        def logl(x):
            p = {'c0': x[0], 'c1': x[1], 'c2': x[2], 'v_shift': x[3], 'lsf_scale': x[4], 'B_abs': x[5], 'f_D': 0.0, 'alpha': x[6]}
            return -0.5 * np.sum(((truth_data - base_model(p, tep_primary_only=False)) / noise_level)**2)
        ndim = 7
    elif model_type == 'M1_primary_only':
        bounds = base_bounds + [(0, 1e-4), alpha_prior]
        def ptform(u):
            x = np.array(u)
            for i, b in enumerate(bounds): x[i] = u[i] * (b[1] - b[0]) + b[0]
            return x
        def logl(x):
            p = {'c0': x[0], 'c1': x[1], 'c2': x[2], 'v_shift': x[3], 'lsf_scale': x[4], 'B_abs': x[5], 'f_D': 0.0, 'alpha': x[6]}
            return -0.5 * np.sum(((truth_data - base_model(p, tep_primary_only=True)) / noise_level)**2)
        ndim = 7
    elif model_type == 'M2_full':
        bounds = base_bounds + [(0, 1e-4), (0.0, 1.0), alpha_prior]
        def ptform(u):
            x = np.array(u)
            for i, b in enumerate(bounds): x[i] = u[i] * (b[1] - b[0]) + b[0]
            return x
        def logl(x):
            p = {'c0': x[0], 'c1': x[1], 'c2': x[2], 'v_shift': x[3], 'lsf_scale': x[4], 'B_abs': x[5], 'f_D': x[6], 'alpha': x[7]}
            return -0.5 * np.sum(((truth_data - base_model(p, tep_primary_only=False)) / noise_level)**2)
        ndim = 8
    elif model_type == 'M2_primary_only':
        bounds = base_bounds + [(0, 1e-4), (0.0, 1.0), alpha_prior]
        def ptform(u):
            x = np.array(u)
            for i, b in enumerate(bounds): x[i] = u[i] * (b[1] - b[0]) + b[0]
            return x
        def logl(x):
            p = {'c0': x[0], 'c1': x[1], 'c2': x[2], 'v_shift': x[3], 'lsf_scale': x[4], 'B_abs': x[5], 'f_D': x[6], 'alpha': x[7]}
            return -0.5 * np.sum(((truth_data - base_model(p, tep_primary_only=True)) / noise_level)**2)
        ndim = 8
    elif model_type == 'M2_free_alpha':
        bounds = base_bounds + [(0, 1e-4), (0.0, 1.0), (0.0, 0.005)]
        def ptform(u):
            x = np.array(u)
            for i, b in enumerate(bounds): x[i] = u[i] * (b[1] - b[0]) + b[0]
            return x
        def logl(x):
            p = {'c0': x[0], 'c1': x[1], 'c2': x[2], 'v_shift': x[3], 'lsf_scale': x[4], 'B_abs': x[5], 'f_D': x[6], 'alpha': x[7]}
            return -0.5 * np.sum(((truth_data - base_model(p, tep_primary_only=False)) / noise_level)**2)
        ndim = 8
    elif model_type == 'M3_global':
        bounds = base_bounds + [(-300, 100), (0, 1e-4), (4.0, 12.0)]
        def ptform(u):
            x = np.array(u)
            for i, b in enumerate(bounds): x[i] = u[i] * (b[1] - b[0]) + b[0]
            return x
        def logl(x):
            p = {'c0': x[0], 'c1': x[1], 'c2': x[2], 'v_shift': x[3], 'lsf_scale': x[4], 'int_v': x[5], 'int_n': x[6], 'int_b': x[7]}
            return -0.5 * np.sum(((truth_data - base_model(p)) / noise_level)**2)
        ndim = 8
    elif model_type == 'M3_Dlocal':
        bounds = base_bounds + [(-110, -70), (0, 1e-4), (4.0, 12.0)]
        def ptform(u):
            x = np.array(u)
            for i, b in enumerate(bounds): x[i] = u[i] * (b[1] - b[0]) + b[0]
            return x
        def logl(x):
            p = {'c0': x[0], 'c1': x[1], 'c2': x[2], 'v_shift': x[3], 'lsf_scale': x[4], 'int_v': x[5], 'int_n': x[6], 'int_b': x[7]}
            return -0.5 * np.sum(((truth_data - base_model(p)) / noise_level)**2)
        ndim = 8
    elif model_type == 'M3_centroid':
        bounds = base_bounds + [centroid_bounds, (0, 1e-4), (4.0, 12.0)]
        def ptform(u):
            x = np.array(u)
            for i, b in enumerate(bounds): x[i] = u[i] * (b[1] - b[0]) + b[0]
            return x
        def logl(x):
            p = {'c0': x[0], 'c1': x[1], 'c2': x[2], 'v_shift': x[3], 'lsf_scale': x[4], 'int_v': x[5], 'int_n': x[6], 'int_b': x[7]}
            return -0.5 * np.sum(((truth_data - base_model(p)) / noise_level)**2)
        ndim = 8
    elif model_type == 'M4_secondary_local':
        bounds = base_bounds + [centroid_bounds, (0, 1e-4), (4.0, 12.0), (0.0, 1.0), (0, 1e-4), (4.0, 12.0)]
        lengths = [w[1] - w[0] for w in sec_windows]
        total_L = sum(lengths)
        def ptform(u):
            x = np.array(u)
            for i, b in enumerate(bounds): x[i] = u[i] * (b[1] - b[0]) + b[0]
            return x
        def logl(x):
            target = x[8] * total_L
            mapped_sec_v = sec_windows[-1][1]
            for w in sec_windows:
                L = w[1] - w[0]
                if target <= L:
                    mapped_sec_v = w[0] + target
                    break
                target -= L
            p = {'c0': x[0], 'c1': x[1], 'c2': x[2], 'v_shift': x[3], 'lsf_scale': x[4], 
                 'int_v': x[5], 'int_n': x[6], 'int_b': x[7],
                 'sec_v': mapped_sec_v, 'sec_n': x[9], 'sec_b': x[10]}
            return -0.5 * np.sum(((truth_data - base_model(p)) / noise_level)**2)
        ndim = 11

    sampler = NestedSampler(logl, ptform, ndim, bound='single', sample='slice', nlive=100, bootstrap=0)
    sampler.run_nested(dlogz=0.5, maxcall=50000, print_progress=False)
    res = sampler.results
    
    post_diag = {}
    if model_type == 'M3_Dlocal':
        weights = np.exp(res.logwt - res.logz[-1])
        v_int_samples = res.samples[:, 5]
        post_diag = {'v_int_samples': v_int_samples.tolist(), 'weights': weights.tolist()}
        
    if model_type.startswith('M2'):
        weights = np.exp(res.logwt - res.logz[-1])
        f_D_samples = res.samples[:, 6]
        alpha_samples = res.samples[:, 7]
        
        p_lt_05 = float(np.sum(weights[f_D_samples < 0.5]))
        p_alpha_prior = float(np.sum(weights[(alpha_samples >= alpha_prior[0]) & (alpha_samples <= alpha_prior[1])]))
        
        alpha_mean = np.average(alpha_samples, weights=weights)
        alpha_std = np.sqrt(np.average((alpha_samples - alpha_mean)**2, weights=weights))
        
        edge_threshold = 0.00002
        at_lower = (alpha_mean - alpha_std) < (bounds[-1][0] + edge_threshold)
        at_upper = (alpha_mean + alpha_std) > (bounds[-1][1] - edge_threshold)
        
        post_diag = {
            'f_D_mean': float(np.average(f_D_samples, weights=weights)),
            'P_f_D_lt_0p5': p_lt_05,
            'P_alpha_in_prior': p_alpha_prior,
            'alpha_mean': float(alpha_mean),
            'alpha_std': float(alpha_std),
            'alpha_at_lower_edge': bool(at_lower),
            'alpha_at_upper_edge': bool(at_upper)
        }
    if model_type == 'M2_primary_only':
        ml_idx = np.argmax(res.logl)
        post_diag['ml_sample'] = res.samples[ml_idx].tolist()
        
    return res.logz[-1], res.logzerr[-1], post_diag


def classify_result(logZs, logZerrs, posteriors):
    """
    Applies the frozen adversarial Stage 13 gate to evaluate whether the 
    data exhibits a decisive, non-spurious TEP signature.
    Returns: (is_tep_win, classification_string, interpretation_string)
    """
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
        if delta_tep <= 2.0 or delta_tep <= combined_err_tep:
            reason = "Standard D / non-TEP models dominate or tie; TEP replacement criteria not satisfied."
        
    classification = "TEP_CANDIDATE" if is_tep_win else "REAL_NEGATIVE"
    return is_tep_win, classification, reason


def process_task(args):
    truth_name, snr, seed = args
    np.random.seed(seed * 1000 + snr)
    
    truth_params_base = {'c0': 1.0, 'c1': 0.0, 'c2': 0.0, 'v_shift': 0.0, 'lsf_scale': 1.0}
    
    if truth_name == 'Mnull':
        truth_flux = base_model(truth_params_base, apply_misspecification=True)
    elif truth_name == 'M0':
        truth_flux = base_model({**truth_params_base, 'B_abs': 2.5e-5, 'f_D': 1.0}, apply_misspecification=True)
    elif truth_name == 'M3_exact_D':
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
    
    # Calculate secondary TEP windows for M4 and held-out test
    alpha_blind_interval = [0.0005, 0.0009]
    g_primary = components[primary_idx]['g_i']
    sec_windows_raw = []
    w_sec = max(1.0, 3 * sigma_v, 3.0)
    for i, hc in enumerate(hi_comps):
        if i == primary_idx: continue
        g_i = components[i]['g_i']
        s1 = c_kms * alpha_blind_interval[0] * (g_i - g_primary)
        s2 = c_kms * alpha_blind_interval[1] * (g_i - g_primary)
        v_base = hc['v'] - 82.0
        v_min = v_base + min(s1, s2)
        v_max = v_base + max(s1, s2)
        sec_windows_raw.append([v_min - w_sec, v_max + w_sec])
    
    sec_windows_raw.sort(key=lambda x: x[0])
    merged_windows = []
    for w in sec_windows_raw:
        if not merged_windows:
            merged_windows.append(w)
        else:
            last = merged_windows[-1]
            if w[0] <= last[1]:
                merged_windows[-1] = [last[0], max(last[1], w[1])]
            else:
                merged_windows.append(w)
    
    lz, lzerr, pdiag = fit_model_nested(noisy_data, 'M3_centroid', noise, centroid_bounds=centroid_bounds)
    logZs['M3_centroid'] = lz
    logZerrs['M3_centroid'] = lzerr
    posteriors['M3_centroid'] = pdiag
    
    lz, lzerr, pdiag = fit_model_nested(noisy_data, 'M4_secondary_local', noise, centroid_bounds=centroid_bounds, sec_windows=merged_windows)
    logZs['M4_secondary_local'] = lz
    logZerrs['M4_secondary_local'] = lzerr
    posteriors['M4_secondary_local'] = pdiag
    
    # Held-out validation
    held_out_diff = 0.0
    if 'M2_primary_only' in posteriors:
        ml_sample = posteriors['M2_primary_only']['ml_sample']
        p_ml = {'c0': ml_sample[0], 'c1': ml_sample[1], 'c2': ml_sample[2], 
                'v_shift': ml_sample[3], 'lsf_scale': ml_sample[4],
                'B_abs': ml_sample[5], 'f_D': ml_sample[6], 'alpha': ml_sample[7]}
        flux_null = base_model(p_ml, tep_primary_only=True)
        flux_pred = base_model(p_ml, tep_primary_only=False)
        sec_mask = np.zeros(len(v_grid), dtype=bool)
        for w in merged_windows:
            sec_mask |= (v_grid >= w[0]) & (v_grid <= w[1])
        logL_null_sec = -0.5 * np.sum(((noisy_data[sec_mask] - flux_null[sec_mask]) / noise)**2)
        logL_pred_sec = -0.5 * np.sum(((noisy_data[sec_mask] - flux_pred[sec_mask]) / noise)**2)
        held_out_diff = logL_pred_sec - logL_null_sec
        posteriors['held_out_diff'] = float(held_out_diff)
    
    return {
        'truth_name': truth_name,
        'snr': snr,
        'seed': seed,
        'logZs': logZs,
        'logZerrs': logZerrs,
        'posteriors': posteriors
    }

def run_grid():
    snr_grid = [50]
    seeds_per_truth = 60
    models_out = ['Mnull', 'M0', 'M1_full', 'M2_full', 'M3_global', 'M3_Dlocal', 'M3_centroid', 'M4_secondary_local']
    truth_cases = ['Mnull', 'M0', 'M3_exact_D']
    
    tasks = []
    for truth_name in truth_cases:
        for snr in snr_grid:
            for seed in range(seeds_per_truth):
                tasks.append((truth_name, snr, seed))
                
    raw_matrix = {snr: {tc: {m: 0 for m in models_out} for tc in truth_cases} for snr in snr_grid}
    class_matrix = {snr: {tc: {m: 0 for m in models_out + ['Tie']} for tc in truth_cases} for snr in snr_grid}
    counters = {
        'decisive_false_TEP_Mnull': 0,
        'decisive_false_TEP_M0': 0,
        'decisive_false_TEP_M3_exact_D': 0,
        'weak_TEP_preference': 0,
        'tie_count': 0
    }
    
    total_tasks = len(tasks)
    print(f"Starting Multiprocessing Nested Sampling Validation (Total fits: {total_tasks * 10})")
    print(f"Running across max CPU cores...")
    
    completed = 0
    
    all_seed_results = []
    
    with concurrent.futures.ProcessPoolExecutor() as executor:
        futures = {executor.submit(process_task, t): t for t in tasks}
        
        for future in concurrent.futures.as_completed(futures):
            res = future.result()
            truth_name = res['truth_name']
            snr = res['snr']
            logZs = res['logZs']
            logZerrs = res['logZerrs']
            posteriors = res['posteriors']
            
            seed_data = {
                'truth_name': truth_name,
                'snr': snr,
                'logZs': logZs,
                'logZerrs': logZerrs,
                'held_out_diff': posteriors.get('held_out_diff', 0.0),
                'p_f_D_lt_0p5': posteriors.get('M2_full', {}).get('P_f_D_lt_0p5', 0),
                'alpha_edge': posteriors.get('M2_full', {}).get('alpha_at_lower_edge', False) or posteriors.get('M2_full', {}).get('alpha_at_upper_edge', False),
                'p_alpha_in_prior': posteriors.get('M2_free_alpha', {}).get('P_alpha_in_prior', 0)
            }
            all_seed_results.append(seed_data)
            
            import json
            with open('data/processed/stage2_v1_results.json', 'w') as f:
                json.dump(all_seed_results, f, indent=2)
            
            completed += 1
            sys.stdout.write(f"\rCompleted {completed}/{total_tasks} truth seeds...")
            sys.stdout.flush()
            
            # Raw winner (only among main models, exclude diagnostics)
            main_logZs = {k: v for k, v in logZs.items() if k in models_out}
            raw_winner = max(main_logZs, key=main_logZs.get)
            raw_matrix[snr][truth_name][raw_winner] += 1
            
            # Pairwise classification
            sorted_models = sorted(main_logZs.keys(), key=lambda k: main_logZs[k], reverse=True)
            best = sorted_models[0]
            runner_up = sorted_models[1]
            
            delta = main_logZs[best] - main_logZs[runner_up]
            combined_err = math.sqrt(logZerrs[best]**2 + logZerrs[runner_up]**2)
            
            if delta <= 1.0 or delta <= combined_err:
                classified_result = 'Tie'
            elif delta > 2.0 and delta > combined_err:
                classified_result = best
            else:
                classified_result = 'Tie'
                if best in ['M1_full', 'M2_full']:
                    counters['weak_TEP_preference'] += 1
            
            class_matrix[snr][truth_name][classified_result] += 1
            if classified_result == 'Tie':
                counters['tie_count'] += 1
            
            # Decisive false TEP
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
                        
            if is_tep_win:
                if truth_name == 'Mnull': counters['decisive_false_TEP_Mnull'] += 1
                elif truth_name == 'M0': counters['decisive_false_TEP_M0'] += 1
                elif truth_name == 'M3_exact_D': counters['decisive_false_TEP_M3_exact_D'] += 1

    print("\n\n============================================================")
    print("NESTED SAMPLING STRESS RECOVERY MATRIX (S/N STRATIFIED)")
    for snr in snr_grid:
        print(f"\n--- SNR = {snr} ---")
        print("RAW WINNER MATRIX:")
        for t in truth_cases: print(f"Truth {t}: {raw_matrix[snr][t]}")
        print("\nCLASSIFIED WINNER MATRIX:")
        for t in truth_cases: print(f"Truth {t}: {class_matrix[snr][t]}")
    print("\nFALSE TEP COUNTERS:")
    print(json.dumps(counters, indent=2))
    
if __name__ == '__main__':
    run_grid()
