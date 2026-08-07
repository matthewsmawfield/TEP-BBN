import numpy as np
from scripts.lib.q1009_primary_test_engine import *
from scripts.steps.step_37_phase_h2_active_posterior import load_q1009_spectra

def run_free():
    spectra = load_q1009_spectra()
    
    # Define a new model H3 where f_D is free and int_n is free
    MODEL_PARAMS['H3'] = ['v_shift', 'B_abs', 'f_D', 'alpha', 'int_v', 'int_n', 'int_b']
    
    precomps_train = [precompute_spectrum_matrices(s, 'train_mask') for s in spectra]
    
    # We will test f_D = 0 (interloper replaces D)
    params_D0 = {'v_shift': 0.5, 'B_abs': 1.5e-5, 'f_D': 0.0, 'alpha': 0.0, 'int_v': 0.0, 'int_n': 1e-5, 'int_b': 8.0}
    logL_D0, _ = evaluate_logL_profiled(spectra, precomps_train, params_D0, 'H0') 
    # wait H0 sets f_D=1.0 internally. I need to bypass get_model_eval_type and evaluate_logL_profiled logic.
    
run_free()
