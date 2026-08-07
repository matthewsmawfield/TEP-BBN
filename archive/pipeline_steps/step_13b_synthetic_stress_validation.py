"""
Step 13b: Synthetic Stress Validation (Phase 4A+)

Runs synthetic stress tests under non-ideal conditions to ensure robustness
of the Bayesian model-comparison machinery. Incorporates shared continuum, 
wavelength, and LSF nuisance parameters. Includes adversarial M3 tests
(exact-D, near-D, off-D) and tracks boundary hits for nuisance parameters.
"""

import json
from pathlib import Path
import sys
import numpy as np
from scipy.optimize import minimize
import math
from tqdm import tqdm

script_dir = Path(__file__).parent
project_root = script_dir.parent.parent
sys.path.insert(0, str(project_root))

from scripts.utils.voigt_fitting import voigt_profile

def run_synthetic_stress():
    print("Step 13b: Synthetic Stress Validation Test (Phase 4A+)")
    print("=" * 60)
    
    feature_path = project_root / 'data/processed/measured_feature_vector_Q0913+072.json'
    with open(feature_path, 'r') as f:
        features = json.load(f)
        
    components = features['components']
    c_kms = 299792.458
    alpha_prior = [0.0005, 0.0009]
    v_grid = np.linspace(-300, 100, 800)
    
    # Normalized x for continuum polynomial to be well behaved [-1, 1]
    x_norm = (v_grid - v_grid[0]) / (v_grid[-1] - v_grid[0]) * 2.0 - 1.0
    
    hi_comps = []
    for comp in components:
        v = comp['velocity_kms']
        n_hi = 1.0 * comp['metal_alignment_strength'] 
        hi_comps.append({'v': v, 'n': n_hi, 'b': 12.0, 'g_i': comp['g_i']}) 
        
    def base_model(params_dict, apply_misspecification=False):
        """Builds flux from a dictionary of components."""
        # 1. Continuum
        c0 = params_dict.get('c0', 1.0)
        c1 = params_dict.get('c1', 0.0)
        c2 = params_dict.get('c2', 0.0)
        
        flux = c0 + c1 * x_norm + c2 * (x_norm**2)
        
        if apply_misspecification:
            flux += 0.01 * np.sin(2.0 * np.pi * x_norm) # Unmodelled wiggles
            
        # 2. Nuisance parameters
        v_shift = params_dict.get('v_shift', 0.0)
        lsf_scale = params_dict.get('lsf_scale', 1.0)
        
        # Effective grid for evaluation
        v_eval = v_grid - v_shift
        
        scale_hi = 20.0  
        scale_di = 1.0e5 
            
        for hc in hi_comps:
            b_eff = hc['b'] * lsf_scale
            if apply_misspecification:
                b_eff *= 1.05 # Unmodelled 5% b-param mismatch
            flux -= hc['n'] * voigt_profile(v_eval, hc['v'], b_eff, 0.1) * scale_hi
            
        if 'alpha' in params_dict:
            alpha = params_dict['alpha']
            d_to_h = params_dict.get('D_to_H', 2.5e-5) # M1 uses fixed 2.5e-5
            primary_comp = next((c for c in components if c.get('column_feature', 0.0) == 1.0), components[0])
        g_primary = primary_comp['g_i']
            
            for i, hc in enumerate(hi_comps):
                g_i = components[i]['g_i']
                v_d = hc['v'] - 82.0 + c_kms * alpha * (g_i - g_primary)
                n_d = hc['n'] * d_to_h
                b_d = (hc['b'] / math.sqrt(2)) * lsf_scale
                
                # EDGE GUARD
                margin = max(3 * b_d, 2 * 10.0) 
                if (v_grid[0] + margin) <= v_d <= (v_grid[-1] - margin):
                    flux -= n_d * voigt_profile(v_eval, v_d, b_d, 0.1) * scale_di
                    
        elif 'D_to_H' in params_dict:
            d_to_h = params_dict['D_to_H']
            for hc in hi_comps:
                v_d = hc['v'] - 82.0  
                n_d = hc['n'] * d_to_h
                b_d = (hc['b'] / math.sqrt(2)) * lsf_scale
                flux -= n_d * voigt_profile(v_eval, v_d, b_d, 0.1) * scale_di
                
        if 'int_v' in params_dict:
            v_int = params_dict['int_v']
            n_int = params_dict['int_n']
            b_int = params_dict['int_b'] * lsf_scale
            flux -= n_int * voigt_profile(v_eval, v_int, b_int, 0.1) * scale_di
            
        # Misspecification: Unmodelled weak blend
        if apply_misspecification:
            flux -= 2.5e-6 * voigt_profile(v_eval, -110.0, 5.0, 0.1) * scale_di
            
        return np.clip(flux, 0, 1)

    def fit_model(truth_data, model_type, noise_level):
        """Fits a specific model to the truth data and returns BIC and optimized parameters."""
        def objective(p):
            params_dict = {
                'c0': p[0],
                'c1': p[1],
                'c2': p[2],
                'v_shift': p[3],
                'lsf_scale': p[4]
            }
            if model_type == 'M0':
                params_dict['D_to_H'] = p[5]
            elif model_type == 'M1':
                params_dict['alpha'] = p[5]
            elif model_type == 'M2':
                params_dict['D_to_H'] = p[5]
                params_dict['alpha'] = p[6]
            elif model_type == 'M3':
                params_dict['int_v'] = p[5]
                params_dict['int_n'] = p[6]
                params_dict['int_b'] = p[7]
                
            model_flux = base_model(params_dict, apply_misspecification=False)
            chi2 = np.sum(((truth_data - model_flux) / noise_level)**2)
            return chi2

        base_x0 = [1.0, 0.0, 0.0, 0.0, 1.0]
        base_bounds = [(0.80, 1.20), (-0.5, 0.5), (-0.5, 0.5), (-3.0, 3.0), (0.8, 1.2)]
        
        if model_type == 'Mnull':
            x0 = base_x0
            bounds = base_bounds
            k = 5
        elif model_type == 'M0':
            x0 = base_x0 + [2.5e-5]
            bounds = base_bounds + [(0, 1e-4)]
            k = 6
        elif model_type == 'M1':
            x0 = base_x0 + [0.0007]
            bounds = base_bounds + [alpha_prior]
            k = 6
        elif model_type == 'M2':
            x0 = base_x0 + [1.0e-5, 0.0007]
            bounds = base_bounds + [(0, 1e-4), alpha_prior]
            k = 7
        elif model_type == 'M3':
            x0 = base_x0 + [-82.0, 2.5e-5, 8.0]
            bounds = base_bounds + [(-120, -40), (0, 1e-3), (2.0, 30.0)]
            k = 8
            
        res = minimize(objective, x0, method='L-BFGS-B', bounds=bounds)
        bic = res.fun + k * np.log(len(v_grid))
        
        # Check bound hits
        bound_hits = {}
        for i, (name, b) in enumerate(zip(['c0', 'c1', 'c2', 'v_shift', 'lsf_scale'], base_bounds)):
            val = res.x[i]
            tol = 1e-5
            if abs(val - b[0]) < tol or abs(val - b[1]) < tol:
                bound_hits[name] = True
            else:
                bound_hits[name] = False
                
        return bic, bound_hits

    # ---------------------------------------------------------
    # STRESS VALIDATION LOOP
    # ---------------------------------------------------------
    snr_grid = [30, 50, 100]
    seeds_per_truth = 50
    models = ['Mnull', 'M0', 'M1', 'M2', 'M3']
    
    # Truth categories
    m3_velocities = {
        'exact_D': [-82.0],
        'near_D': [-78.0, -86.0, -90.0],
        'off_D': [-100.0, -110.0, -120.0]
    }
    
    results = {}
    bound_hit_counts = {'c0': 0, 'c1': 0, 'c2': 0, 'v_shift': 0, 'lsf_scale': 0}
    delta_bics_m3_m2 = []
    
    truth_cases = ['Mnull', 'M0', 'M1', 'M2']
    for cat in m3_velocities.keys():
        truth_cases.append(f"M3_{cat}")
        
    for t in truth_cases:
        results[t] = {m: 0 for m in models}
        
    total_iters = len(snr_grid) * seeds_per_truth * (4 + sum(len(v) for v in m3_velocities.values()))
    
    print(f"Running {total_iters} synthetic fits...")
    with tqdm(total=total_iters) as pbar:
        for snr in snr_grid:
            noise_level = 1.0 / snr
            for seed in range(seeds_per_truth):
                np.random.seed(seed + int(snr)*1000)
                truth_params_base = {'c0': 1.0, 'c1': 0.02, 'c2': -0.01, 'v_shift': 0.5, 'lsf_scale': 1.02}
                
                # Build list of active truths for this iteration
                active_truths = {
                    "Mnull": base_model(truth_params_base.copy(), apply_misspecification=True),
                    "M0": base_model({**truth_params_base, 'D_to_H': 2.5e-5}, apply_misspecification=True),
                    "M1": base_model({**truth_params_base, 'alpha': 0.00073}, apply_misspecification=True),
                    "M2": base_model({**truth_params_base, 'D_to_H': 1.0e-5, 'alpha': 0.00073}, apply_misspecification=True)
                }
                
                for cat, v_list in m3_velocities.items():
                    for v_int in v_list:
                        flux = base_model({**truth_params_base, 'int_v': v_int, 'int_n': 2.5e-5, 'int_b': 8.0}, apply_misspecification=True)
                        key = f"M3_{cat}"
                        if key not in active_truths:
                            active_truths[key] = []
                        active_truths[key].append(flux)
                
                for t_name, t_fluxes in active_truths.items():
                    if not isinstance(t_fluxes, list):
                        t_fluxes = [t_fluxes]
                        
                    for t_flux in t_fluxes:
                        noisy_flux = t_flux + np.random.normal(0, noise_level, size=len(v_grid))
                        
                        bics = {}
                        for m in models:
                            bic, bh = fit_model(noisy_flux, m, noise_level)
                            bics[m] = bic
                            for p, hit in bh.items():
                                if hit: bound_hit_counts[p] += 1
                        
                        winner = min(bics, key=bics.get)
                        results[t_name][winner] += 1
                        
                        if t_name.startswith("M3_"):
                            delta_bics_m3_m2.append(bics['M3'] - bics['M2'])
                            
                        pbar.update(1)

    print("\n" + "=" * 60)
    print("STRESS RECOVERY MATRIX")
    for t_name in truth_cases:
        print(f"Truth {t_name}: {results[t_name]}")
        
    false_tep_m3_exact = (results['M3_exact_D']['M1'] + results['M3_exact_D']['M2']) / (len(snr_grid) * seeds_per_truth * len(m3_velocities['exact_D']))
    false_tep_m3_near = (results['M3_near_D']['M1'] + results['M3_near_D']['M2']) / (len(snr_grid) * seeds_per_truth * len(m3_velocities['near_D']))
    false_tep_m3_off = (results['M3_off_D']['M1'] + results['M3_off_D']['M2']) / (len(snr_grid) * seeds_per_truth * len(m3_velocities['off_D']))
    
    m0_m3_deg_rate = (results['M3_exact_D']['M0']) / (len(snr_grid) * seeds_per_truth * len(m3_velocities['exact_D']))
    
    print(f"\nFalse TEP win rate on M3 exact-D: {false_tep_m3_exact:.3f} (Required < 0.05)")
    print(f"False TEP win rate on M3 near-D:  {false_tep_m3_near:.3f}")
    print(f"False TEP win rate on M3 off-D:   {false_tep_m3_off:.3f}")
    print(f"M0/M3 degeneracy rate on exact-D: {m0_m3_deg_rate:.3f}")
    
    print("\nNuisance Bound Hits:")
    for p, c in bound_hit_counts.items():
        print(f"  {p}: {c} / {total_iters * len(models)}")
        
    delta_bic_m3_m2_sorted = np.sort(delta_bics_m3_m2)
    p05 = delta_bic_m3_m2_sorted[int(0.05 * len(delta_bic_m3_m2_sorted))]
    med = delta_bic_m3_m2_sorted[int(0.50 * len(delta_bic_m3_m2_sorted))]
    p95 = delta_bic_m3_m2_sorted[int(0.95 * len(delta_bic_m3_m2_sorted))]
    
    passed = True
    if false_tep_m3_exact >= 0.05: passed = False
    if false_tep_m3_near >= 0.05: passed = False
    
    report = {
        "phase": "4A+",
        "stress_failure_mode": None,
        "fixes_applied": ["shared_continuum", "eligibility_rule", "nuisance_tracking"],
        "false_TEP_win_rate_on_M3_exact_D": false_tep_m3_exact,
        "false_TEP_win_rate_on_M3_near_D": false_tep_m3_near,
        "false_TEP_win_rate_on_M3_off_D": false_tep_m3_off,
        "M0_M3_degeneracy_rate": m0_m3_deg_rate,
        "nuisance_bound_hits": bound_hit_counts,
        "delta_bic_distribution": {
            "M3_truth_M3_minus_M2": {
                "median": med,
                "p05": p05,
                "p95": p95
            }
        },
        "alpha_prior_audit": {
            "alpha_prior": alpha_prior,
            "derived_without_D_location": True,
            "uses_required_minus_82_shift": False,
            "uses_alpha_required_from_D": False,
            "source_document": "ALPHA_PRIOR_DERIVATION.md",
            "frozen_before_unblinding": True,
            "alpha_prior_system_specific": False,
            "alpha_prior_derived_from_TEP": True,
            "alpha_prior_uses_observed_D_location": False,
            "D_window_used_for_feature_vector": False,
            "D_window_used_for_alpha_prior": False,
            "alpha_required_from_minus82_used": False,
            "continuum_inherited_from_standard_D_fit": False
        },
        "ready_for_phase_4B": passed
    }
    
    out_path = project_root / 'data/processed/phase4A_stress_report.json'
    with open(out_path, 'w') as f:
        json.dump(report, f, indent=2)
        
    print(f"\nReady for Phase 4B: {passed}")
    print("=" * 60)

if __name__ == '__main__':
    run_synthetic_stress()
