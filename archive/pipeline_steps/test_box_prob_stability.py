import sys
from pathlib import Path
import json
import numpy as np

script_dir = Path(__file__).parent
project_root = script_dir.parent.parent
sys.path.append(str(project_root))

from scripts.lib.joint_spectrum_likelihood import fit_model_nested_joint
import scripts.steps.step_13c_nested_synthetic_adversarial_validation as step13c
from scripts.steps.step_14c_joint_power_triage_screen import load_joint_spectra

def main():
    print("--- Testing Multivariate Normal Box Probability Stability ---")
    manifest_path = project_root / 'data/processed/Q1009+2956_z2.504_HIRES_spectrum_manifest.json'
    spectra = load_joint_spectra(str(manifest_path))
    
    feature_vector_path = project_root / 'data/processed/measured_feature_vector_Q1009+2956_z2.504.json'
    with open(feature_vector_path) as f:
        step13c.set_system_feature_vector(json.load(f))
        
    # We will instantiate the likelihood function from fit_model_nested_joint using a dummy nested sampler hook
    import itertools
    import scipy.ndimage
    import scipy.linalg
    from scipy.stats import multivariate_normal
    import math

    # Re-implement the marginalisation piece directly for a test
    shared_params = {'v_shift': 0.0, 'B_abs': 1.5e-5, 'f_D': 0.0, 'alpha': 0.0007}
    
    spec = spectra[0] # Test on first spectrum
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
    
    # Calculate condition number of H
    cond_H = np.linalg.cond(H)
    print(f"Condition number of H: {cond_H:.2e}")
    if cond_H > 1e12:
        print("WARNING: Matrix is ill-conditioned.")
    else:
        print("Matrix is well-conditioned. Singular Hessian is mathematically impossible post-Cholesky.")

    # frozen evaluate
    from scripts.lib.joint_spectrum_likelihood import evaluate_frozen_model
    flux_zero_c = evaluate_frozen_model(
        velocity=spec['v'],
        shared_params=shared_params,
        local_params={'c0': 0.0, 'c1': 0.0, 'c2': 0.0},
        model_type='M2_full',
        sigma_v_kms=spec['sigma_v_kms']
    )
    A_theta = -flux_zero_c
    r_theta = spec['flux'] + A_theta
    b_theta = Phi.T @ (W * r_theta)
    
    c_hat = np.array([0.900, -0.099, -0.099])
    chi2_min = 100.0
    
    print("\nRepeatedly calculating MVN CDF:")
    lower_bound = np.array([0.9, -0.1, -0.1])
    upper_bound = np.array([1.1, 0.1, 0.1])
    
    P_vals = []
    logL_vals = []
    
    for i in range(10):
        # We explicitly recreate the distribution object to test if it has jitter
        dist = multivariate_normal(c_hat, H_inv, allow_singular=False)
        P = 0.0
        for signs in itertools.product([0, 1], repeat=3):
            x_pt = np.where(signs, upper_bound, lower_bound)
            sign = (-1)**(3 - sum(signs))
            P += sign * dist.cdf(x_pt)
            
        V_prior = 0.008
        P_vals.append(P)
        if P > 0:
            log_L_marg = C_0 - 0.5 * chi2_min + 1.5 * math.log(2*math.pi) - 0.5 * logdet_H + math.log(P) - math.log(V_prior)
            logL_vals.append(log_L_marg)
        
    p_spread = max(P_vals) - min(P_vals)
    if logL_vals:
        logl_spread = max(logL_vals) - min(logL_vals)
    else:
        logl_spread = float('nan')
        
    print(f"c_hat: {c_hat}")
    print(f"H_inv diagonals: {np.diag(H_inv)}")
    
    print(f"10 iterations. P values range: {min(P_vals):.12e} to {max(P_vals):.12e}")
    print(f"Spread in P: {p_spread:.12e}")
    print(f"Spread in logL: {logl_spread:.12e}")
    if p_spread < 1e-15 and min(P_vals) > 0:
        print("-> Passed (Deterministic and numerically stable)")
    else:
        print("-> Failed (Numerical instability or underflow detected)")
        
if __name__ == '__main__':
    main()
