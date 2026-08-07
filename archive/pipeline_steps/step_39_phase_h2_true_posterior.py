"""
Step 39: Phase H2 True Local Posterior Generation (Q1009)

Calculates the deterministic MAP log-likelihoods and Bayesian Information Criterion 
(BIC) for the three physical unblending models on Q1009:
- M_D (Pure Standard D, f_D = 1)
- M_H (Pure TEP Interloper, f_D = 0)
- M_D+H (Free Mixture, f_D free)
"""

import os
import json
import numpy as np
from pathlib import Path
import sys
import scipy.linalg

script_dir = Path(__file__).parent
project_root = script_dir.parent.parent
sys.path.insert(0, str(project_root))

from scripts.lib.q1009_primary_test_engine import (
    precompute_spectrum_matrices,
    fit_deterministic_model,
    BOUNDS,
    MODEL_PARAMS
)
from scripts.steps.step_37_phase_h2_active_posterior import load_q1009_spectra

def main():
    spectra = load_q1009_spectra()
    
    # ---------------------------------------------------------
    # Monkey-patch the evaluation types to correctly map models
    # ---------------------------------------------------------
    import scripts.lib.q1009_primary_test_engine
    
    # Define our three strict models
    # H_MD: Pure standard D (f_D = 1, no alpha)
    MODEL_PARAMS['H_MD'] = ['v_shift', 'B_abs'] 
    
    # H_MH: Pure TEP (f_D = 0, alpha active)
    MODEL_PARAMS['H_MH'] = ['v_shift', 'B_abs', 'alpha']
    
    # H_MIX: Mixture (f_D free, alpha active, interloper profile active)
    MODEL_PARAMS['H_MIX'] = ['v_shift', 'B_abs', 'f_D', 'alpha', 'int_v', 'int_n', 'int_b']
    
    BOUNDS['f_D'] = (0.0, 1.0)
    BOUNDS['int_v'] = (-10.0, 10.0)
    BOUNDS['int_n'] = (0.0, 1e-4)
    BOUNDS['int_b'] = (4.0, 12.0)
    
    def get_model_eval_type_mod(model_name):
        if model_name == 'H_MD': return 'M1_primary_only'
        if model_name == 'H_MH': return 'M2_primary_only'
        if model_name == 'H_MIX': return 'M3_centroid'
        return 'M1_primary_only'
    
    scripts.lib.q1009_primary_test_engine.get_model_eval_type = get_model_eval_type_mod
    
    orig_eval = scripts.lib.q1009_primary_test_engine.evaluate_logL_profiled
    def mod_eval(spectra_list, precomps, shared_params, model_name):
        eval_type = get_model_eval_type_mod(model_name)
        eval_params = shared_params.copy()
        
        # Manually assign fixed parameters based on model
        if model_name == 'H_MD':
            eval_params['f_D'] = 1.0
            eval_params['alpha'] = 0.0
        elif model_name == 'H_MH':
            eval_params['f_D'] = 0.0
            
        total_logl = 0.0
        c_opts = []
        for i, spec in enumerate(spectra_list):
            pc = precomps[i]
            if pc['chol_masked'] is None:
                return -1e100, []
                
            from scripts.lib.joint_spectrum_likelihood import evaluate_frozen_model
            flux_zero_c = evaluate_frozen_model(spec['v'], eval_params, {'c0':0.0, 'c1':0.0, 'c2':0.0}, eval_type, spec['sigma_v_kms'])
            A_theta_masked = -flux_zero_c[pc['mask']]
            r_theta_masked = pc['flux_masked'] + A_theta_masked
            b_theta_masked = pc['Phi_masked'].T @ (pc['W_masked'] * r_theta_masked)
            try:
                c_hat = scipy.linalg.cho_solve(pc['chol_masked'], b_theta_masked)
            except np.linalg.LinAlgError:
                return -1e100, []
                
            c_opt = np.clip(c_hat, [0.9, -0.1, -0.1], [1.1, 0.1, 0.1])
            residuals = r_theta_masked - (pc['Phi_masked'] @ c_opt)
            chi2 = np.sum(pc['W_masked'] * residuals**2)
            total_logl += pc['C_0_masked'] - 0.5 * chi2
            c_opts.append(c_opt)
        return total_logl, c_opts
        
    scripts.lib.q1009_primary_test_engine.evaluate_logL_profiled = mod_eval
    
    # ---------------------------------------------------------
    # Execute Model Fits
    # ---------------------------------------------------------
    print("=" * 80)
    print("PHASE H2: TRUE LOCAL POSTERIOR COMPARISON (Q1009)")
    print("=" * 80)
    
    n_data = sum(np.sum(s['train_mask']) for s in spectra)
    
    results = {}
    for mod in ['H_MD', 'H_MH', 'H_MIX']:
        print(f"\nFitting {mod}...")
        res = fit_deterministic_model(spectra, mod)
        k = len(MODEL_PARAMS[mod])
        bic = k * np.log(n_data) - 2 * res['logL_train']
        results[mod] = {
            'logL': res['logL_train'],
            'k': k,
            'bic': bic,
            'params': {k: float(v) for k, v in res['physical_parameters'].items()}
        }
        print(f"  logL: {res['logL_train']:.2f} | k: {k} | BIC: {bic:.2f}")
        print(f"  Params: {results[mod]['params']}")

    # Calculate Weights
    bics = np.array([results['H_MD']['bic'], results['H_MH']['bic'], results['H_MIX']['bic']])
    delta_bic = bics - np.min(bics)
    weights = np.exp(-0.5 * delta_bic)
    weights /= np.sum(weights)
    
    print("\n=== FINAL MODEL PREFERENCE ===")
    print(f"M_D (Standard D):  Weight = {weights[0]:.4f} (BIC={bics[0]:.2f})")
    print(f"M_H (Pure TEP):    Weight = {weights[1]:.4f} (BIC={bics[1]:.2f})")
    print(f"M_D+H (Mixture):   Weight = {weights[2]:.4f} (BIC={bics[2]:.2f})")
    
    winning_model = ['M_D', 'M_H', 'M_D+H'][np.argmax(weights)]
    print(f"\nConclusion: {winning_model} is statistically preferred.")
    if winning_model == 'M_H':
        print("Because the pure TEP interloper (f_D=0) wins, the inferred D/H for Q1009 drops identically to zero.")
    
    out_path = project_root / 'data/processed/phase_h2_true_posterior.json'
    with open(out_path, 'w') as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    main()
