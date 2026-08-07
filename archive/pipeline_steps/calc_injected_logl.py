import sys
import json
import numpy as np
from pathlib import Path

script_dir = Path(__file__).parent
project_root = script_dir.parent.parent
sys.path.append(str(project_root))

from scripts.lib.joint_spectrum_likelihood import fit_model_nested_joint
from scripts.steps.step_14c_joint_power_triage_screen import load_joint_spectra, generate_synthetic_joint_flux
import scripts.steps.step_13c_nested_synthetic_adversarial_validation as step13c
import multiprocessing

def calc_injected_logl(data_seed):
    np.random.seed(data_seed)
    manifest_path = project_root / 'data/processed/Q1009+2956_z2.504_HIRES_spectrum_manifest.json'
    spectra = load_joint_spectra(str(manifest_path))
    
    alpha_inject = 0.0007
    f_D_inject = 0.0
    shared_params_inject = {'v_shift': 0.0, 'B_abs': 1.5e-5, 'f_D': f_D_inject, 'alpha': alpha_inject}
    
    # The audit used model_type=0.0007 and inject_alpha=0.0
    synth_spectra = generate_synthetic_joint_flux(spectra, shared_params_inject, 0.0007)
    
    # We want to compute logL of M2_full AT the exact injected parameters
    # The continuum c_opt is calculated inside logL
    from scripts.lib.joint_spectrum_likelihood import evaluate_frozen_model
    import scipy.ndimage
    import scipy.linalg
    from scipy.stats import multivariate_normal
    import math
    import itertools
    
    total_logl = 0.0
    for spec in synth_spectra:
        v = spec['v']
        sigma_v_kms = spec['sigma_v_kms']
        dv = np.median(np.diff(v))
        sigma_pixels = sigma_v_kms / dv
        x_n = (v - v[0]) / (v[-1] - v[0]) * 2.0 - 1.0
        phi_0 = scipy.ndimage.gaussian_filter1d(np.ones_like(x_n), sigma_pixels, mode='nearest')
        phi_1 = scipy.ndimage.gaussian_filter1d(x_n, sigma_pixels, mode='nearest')
        phi_2 = scipy.ndimage.gaussian_filter1d(x_n**2, sigma_pixels, mode='nearest')
        Phi = np.column_stack([phi_0, phi_1, phi_2])
        W = 1.0 / (spec['err']**2)
        H = Phi.T @ (W[:, None] * Phi)
        chol = scipy.linalg.cho_factor(H, lower=True)
        logdet_H = 2.0 * np.sum(np.log(np.diag(chol[0])))
        H_inv = scipy.linalg.cho_solve(chol, np.eye(3))
        C_0 = -0.5 * np.sum(np.log(2.0 * np.pi * spec['err']**2))
        
        actual_injected_params = {'v_shift': 0.0, 'B_abs': 1.5e-5, 'f_D': 0.0, 'alpha': 0.0}
        
        flux_zero_c = evaluate_frozen_model(
            velocity=spec['v'],
            shared_params=actual_injected_params,
            local_params={'c0': 0.0, 'c1': 0.0, 'c2': 0.0},
            model_type='M2_full',
            sigma_v_kms=spec['sigma_v_kms']
        )
        A_theta = -flux_zero_c
        r_theta = spec['flux'] + A_theta
        b_theta = Phi.T @ (W * r_theta)
        c_hat = scipy.linalg.cho_solve(chol, b_theta)
        chi2_min = np.sum(W * r_theta**2) - np.dot(b_theta, c_hat)
        
        dist = multivariate_normal(c_hat, H_inv, allow_singular=False, seed=42)
        lower_bound = np.array([0.9, -0.1, -0.1])
        upper_bound = np.array([1.1, 0.1, 0.1])
        P = 0.0
        for signs in itertools.product([0, 1], repeat=3):
            x_pt = np.where(signs, upper_bound, lower_bound)
            sign = (-1)**(3 - sum(signs))
            P += sign * dist.cdf(x_pt)
        V_prior = 0.008
        if P <= 0: P = 1e-300
        log_L_marg = C_0 - 0.5 * chi2_min + 1.5 * math.log(2*math.pi) - 0.5 * logdet_H + math.log(P) - math.log(V_prior)
        total_logl += log_L_marg
        
    return data_seed, total_logl

def main():
    feature_vector_path = project_root / 'data/processed/measured_feature_vector_Q1009+2956_z2.504.json'
    with open(feature_vector_path) as f:
        step13c.set_system_feature_vector(json.load(f))
        
    for ds in [1001, 1002, 1008]:
        seed, logl = calc_injected_logl(ds)
        print(f"Data seed {seed}: injected logL = {logl:.2f}")

if __name__ == '__main__':
    main()
