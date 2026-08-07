import numpy as np
from scripts.lib.q1009_primary_test_engine import *
from scripts.steps.step_37_phase_h2_active_posterior import load_q1009_spectra

spectra = load_q1009_spectra()
MODEL_PARAMS['H3'] = ['v_shift', 'B_abs', 'f_D', 'alpha', 'int_v', 'int_n', 'int_b']
BOUNDS['f_D'] = (0.0, 1.0)
BOUNDS['int_v'] = (-10.0, 10.0)
BOUNDS['int_n'] = (0.0, 1e-4)
BOUNDS['int_b'] = (4.0, 12.0)

def get_model_eval_type_mod(model_name):
    if model_name == 'H1': return 'M2_primary_only'
    if model_name == 'H3': return 'M3_centroid'
    return get_model_eval_type(model_name)

import scripts.lib.q1009_primary_test_engine
scripts.lib.q1009_primary_test_engine.get_model_eval_type = get_model_eval_type_mod

# Monkey patch evaluate_logL_profiled to not force f_D=1.0 for H3
orig_eval = scripts.lib.q1009_primary_test_engine.evaluate_logL_profiled
def mod_eval(spectra, precomps, shared_params, model_name):
    eval_type = get_model_eval_type_mod(model_name)
    eval_params = shared_params.copy()
    total_logl = 0.0
    c_opts = []
    for i, spec in enumerate(spectra):
        pc = precomps[i]
        from scripts.lib.joint_spectrum_likelihood import evaluate_frozen_model
        flux_zero_c = evaluate_frozen_model(spec['v'], eval_params, {'c0':0.0, 'c1':0.0, 'c2':0.0}, eval_type, spec['sigma_v_kms'])
        A_theta_masked = -flux_zero_c[pc['mask']]
        r_theta_masked = pc['flux_masked'] + A_theta_masked
        b_theta_masked = pc['Phi_masked'].T @ (pc['W_masked'] * r_theta_masked)
        c_hat = scipy.linalg.cho_solve(pc['chol_masked'], b_theta_masked)
        c_opt = np.clip(c_hat, [0.9, -0.1, -0.1], [1.1, 0.1, 0.1])
        residuals = r_theta_masked - (pc['Phi_masked'] @ c_opt)
        chi2 = np.sum(pc['W_masked'] * residuals**2)
        total_logl += pc['C_0_masked'] - 0.5 * chi2
    return total_logl, []
scripts.lib.q1009_primary_test_engine.evaluate_logL_profiled = mod_eval

res_H1 = fit_deterministic_model(spectra, 'H1')
print("H1 (M_D) MAP logL:", res_H1['logL_train'])
print("H1 Params:", res_H1['physical_parameters'])

res_H3 = fit_deterministic_model(spectra, 'H3')
print("H3 (M_D+H free) MAP logL:", res_H3['logL_train'])
print("H3 Params:", res_H3['physical_parameters'])

