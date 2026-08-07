import json
import numpy as np
import copy
from dynesty import NestedSampler
import scripts.steps.step_13c_nested_synthetic_adversarial_validation as step13c
import scripts.lib.joint_spectrum_likelihood as jsl

from scripts.steps.step_14c_joint_power_triage_screen import load_joint_spectra

def load_q1009_data():
    return load_joint_spectra('data/processed/Q1009+2956_z2.504_HIRES_spectrum_manifest.json')

def get_injected_flux(spectra, alpha_inject, f_D_inject):
    shared_inj = {'v_shift': 0.0, 'B_abs': 1.5e-5, 'f_D': f_D_inject, 'alpha': alpha_inject}
    
    synth_spectra = []
    for spec in spectra:
        local_params = {
            'c0': 1.0,
            'c1': 0.0,
            'c2': 0.0
        }
        
        flux = jsl.evaluate_frozen_model(spec['v'], shared_inj, local_params, 'M2_full', spec['sigma_v_kms'])
        
        synth_spec = copy.deepcopy(spec)
        synth_spec['flux'] = flux
        synth_spectra.append(synth_spec)
        
    return synth_spectra, shared_inj

def calculate_logl_M2_full(synth_spectra, shared_params, local_c0, local_c1, local_c2):
    total_logl = 0.0
    for spec in synth_spectra:
        local_params = {'c0': local_c0, 'c1': local_c1, 'c2': local_c2}
        model_flux = jsl.evaluate_frozen_model(spec['v'], shared_params, local_params, 'M2_full', spec['sigma_v_kms'])
        residual = spec['flux'] - model_flux
        error = spec['err']
        total_logl += -0.5 * np.sum((residual / error)**2 + np.log(2.0 * np.pi * error**2))
    return total_logl

def run_likelihood_closure():
    print("Loading data...")
    spectra = load_q1009_data()
    
    print("Generating synthetic dataset (alpha=0.0007, f_D=0.0)...")
    synth_spectra, shared_inj = get_injected_flux(spectra, 0.0007, 0.0)
    
    # Apply standard noise realization
    np.random.seed(42)
    for spec in synth_spectra:
        spec['flux'] += np.random.normal(0, spec['err'])
        
    print("1. Likelihood at exact injected parameters:")
    logl_inj = calculate_logl_M2_full(synth_spectra, shared_inj, 1.0, 0.0, 0.0)
    print(f"  logL(Injected) = {logl_inj:.2f}")
    
    print("\n2. Direct alpha profile grid:")
    print("  Evaluating alpha grid fixing other parameters to injected values...")
    alphas = np.linspace(0.0005, 0.0009, 11)
    for a in alphas:
        p = shared_inj.copy()
        p['alpha'] = a
        ll = calculate_logl_M2_full(synth_spectra, p, 1.0, 0.0, 0.0)
        print(f"  alpha = {a:.5f} -> logL = {ll:.2f} (diff = {ll - logl_inj:.2f})")
        
    print("\n3. MAP Evaluation via Nested Sampling...")
    print("  Running M3_centroid (null)...")
    v_hat = 0.0 # Approximate centroid for M3
    centroid_bounds = [v_hat - 3.0, v_hat + 3.0]
    
    null_logz, null_logzerr, null_pdiag = jsl.fit_model_nested_joint(synth_spectra, 'M3_centroid', nlive=100, centroid_bounds=centroid_bounds)
    print(f"  M3_centroid logZ = {null_logz:.2f}")
    
    print("  Running M2_full (TEP)...")
    full_logz, full_logzerr, full_pdiag = jsl.fit_model_nested_joint(synth_spectra, 'M2_full', nlive=100)
    print(f"  M2_full logZ = {full_logz:.2f}")
    print(f"  M2_full alpha_mean = {full_pdiag.get('alpha_mean', 0.0):.5f}")
    print(f"  M2_full edges = {full_pdiag.get('alpha_at_lower_edge')}, {full_pdiag.get('alpha_at_upper_edge')}")
    
    print("\n4. Noiseless / Extreme SNR Test")
    print("  Generating noiseless spectra (SNR = 1,000,000)...")
    noiseless_spectra, _ = get_injected_flux(spectra, 0.0007, 0.0)
    for spec in noiseless_spectra:
        # Scale errors down by 10,000x to simulate ultra-high SNR without changing data structures
        spec['err'] = spec['err'] / 10000.0
        
    print("  Running M2_full on noiseless data...")
    nl_logz, nl_logzerr, nl_pdiag = jsl.fit_model_nested_joint(noiseless_spectra, 'M2_full', nlive=100)
    print(f"  Noiseless M2_full alpha_mean = {nl_pdiag.get('alpha_mean', 0.0):.6f}")
    print(f"  Noiseless edges = {nl_pdiag.get('alpha_at_lower_edge')}, {nl_pdiag.get('alpha_at_upper_edge')}")
    print(f"  Noiseless f_D P<0.5 = {nl_pdiag.get('P_f_D_lt_0p5')}")
    
    print("\n5. Tightly Bounded Noiseless Test (Proving Dimensionality Curse)")
    print("  Running M2_full with all priors artificially tightened around the true injected values...")
    jsl.local_bounds = [(0.99, 1.01), (-0.01, 0.01), (-0.01, 0.01)] # Tighten continuum
    jsl.shared_bounds = [(-0.01, 0.01), (1.4e-5, 1.6e-5), (0.0, 0.1), (0.00065, 0.00075)]
    tb_logz, tb_logzerr, tb_pdiag = jsl.fit_model_nested_joint(noiseless_spectra, 'M2_full', nlive=100)
    print(f"  Tightly Bounded M2_full logZ = {tb_logz:.2f}")
    print(f"  Tightly Bounded alpha_mean = {tb_pdiag.get('alpha_mean', 0.0):.6f}")

if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(line_buffering=True)
    with open('data/processed/measured_feature_vector_Q1009+2956_z2.504.json') as f:
        step13c.set_system_feature_vector(json.load(f))
    run_likelihood_closure()
