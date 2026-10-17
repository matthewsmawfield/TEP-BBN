import math

import numpy as np
import scipy.linalg
import scipy.ndimage
from dynesty import NestedSampler

try:
    import scripts.steps.step_13c_nested_synthetic_adversarial_validation as step13c
except ModuleNotFoundError:
    step13c = None


def evaluate_frozen_model(velocity, shared_params, local_params, model_type, sigma_v_kms):
    """
    Evaluates the frozen base_model from step_13c on the given velocity grid.
    Monkeypatches step_13c.v_grid and x_norm to allow evaluation on native grids.
    """
    if step13c is None:
        raise ModuleNotFoundError(
            "step_13c_nested_synthetic_adversarial_validation is not available. "
            "This legacy module requires the deprecated step_13c pipeline."
        )
    step13c.v_grid = velocity
    step13c.x_norm = (velocity - velocity[0]) / (velocity[-1] - velocity[0]) * 2.0 - 1.0
    
    params = {**shared_params, **local_params}
    
    # Evaluate the frozen model (unconvolved intrinsic flux)
    # The frozen model calculates absorption.
    # Note: The original frozen model treats lsf_scale as a simple multiplier.
    # To truly convolve, pass lsf_scale=1.0, get intrinsic flux, and convolve.
    params['lsf_scale'] = 1.0
    
    is_primary_only = (model_type == 'M2_primary_only')
    flux = step13c.base_model(params, apply_misspecification=False, tep_primary_only=is_primary_only)
    
    # Convolve with Gaussian LSF
    # Native grid must be approximately uniform in velocity for fast 1D convolution.
    dv = np.median(np.diff(velocity))
    sigma_pixels = sigma_v_kms / dv
    
    # scipy.ndimage.gaussian_filter1d handles the convolution
    # But note: flux is 1.0 - absorption. The absorption should be convolved,
    # or just convolve the flux. Since continuum is just a quadratic polynomial, 
    # convolving it slightly smears it but it's very smooth anyway.
    convolved_flux = scipy.ndimage.gaussian_filter1d(flux, sigma_pixels, mode='nearest')
    
    return convolved_flux

def fit_model_nested_joint(spectra, model_type, nlive=100, centroid_bounds=None, sec_windows=None, rstate=None):
    """
    Joint likelihood across multiple spectra.
    spectra: list of dicts with 'v', 'flux', 'err', 'sigma_v_kms'
    """
    # Base bounds for shared physical parameters and one global v_shift
    # (c0, c1, c2) are independent per spectrum
    # Shared: v_shift (-1.0, 1.0)
    
    shared_bounds = [(-1.0, 1.0)] # v_shift
    shared_names = ['v_shift']
    
    # Add model-specific shared bounds
    if model_type in ['M1_full', 'M2_full', 'M2_primary_only']:
        shared_bounds.append((0, 1e-4)) # B_abs
        shared_names.append('B_abs')
    if model_type == 'M1_full':
        shared_bounds.append((0.0, 1.0)) # f_D
        shared_names.append('f_D')
    elif model_type == 'M2_full':
        shared_bounds.extend([(0.0, 1.0), (step13c.alpha_prior[0], step13c.alpha_prior[1])]) # f_D, alpha
        shared_names.extend(['f_D', 'alpha'])
    elif model_type == 'M2_primary_only':
        shared_bounds.extend([(0.0, 1.0), (step13c.alpha_prior[0], step13c.alpha_prior[1])])
        shared_names.extend(['f_D', 'alpha'])
    elif model_type == 'M2_free_alpha':
        shared_bounds.extend([(0.0, 1.0), (-0.005, 0.005)])
        shared_names.extend(['f_D', 'alpha'])
        
    if model_type in ['M3_global', 'M3_Dlocal', 'M3_centroid']:
        shared_bounds.extend([(0, 1e-4), (0.0, 1.0)]) # B_abs, f_D
        shared_names.extend(['B_abs', 'f_D'])
        if model_type == 'M3_centroid':
            shared_bounds.extend([centroid_bounds, (0, 1e-4), (4.0, 12.0)])
            shared_names.extend(['int_v', 'int_n', 'int_b'])
            
    if model_type == 'M4_secondary_local':
        shared_bounds.extend([(0, 1e-4), (0.0, 1.0)])
        shared_names.extend(['B_abs', 'f_D'])
        shared_bounds.extend([centroid_bounds, (0, 1e-4), (4.0, 12.0)]) # int
        shared_names.extend(['int_v', 'int_n', 'int_b'])
        shared_bounds.extend([(0.0, 1.0), (0, 1e-4), (4.0, 12.0)]) # sec
        shared_names.extend(['sec_v_fraction', 'sec_n', 'sec_b'])

    total_bounds = shared_bounds.copy()
        
    ndim = len(total_bounds)
    
    total_L = 0
    if sec_windows is not None:
        lengths = [w[1] - w[0] for w in sec_windows]
        total_L = sum(lengths)
        
    def ptform(u):
        x = np.array(u)
        for i, b in enumerate(total_bounds): 
            x[i] = u[i] * (b[1] - b[0]) + b[0]
        return x
        
    precomp = []
    for spec in spectra:
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
        
        precomp.append({
            'Phi': Phi, 'W': W, 'chol': chol, 'H_inv': H_inv,
            'logdet_H': logdet_H, 'C_0': C_0, 'y': spec['flux']
        })

    def logl(x):
        shared_params = {}
        for idx, name in enumerate(shared_names):
            shared_params[name] = x[idx]
            
        if 'sec_v_fraction' in shared_params and sec_windows is not None:
            target = shared_params['sec_v_fraction'] * total_L
            mapped_sec_v = sec_windows[-1][1]
            for w in sec_windows:
                L = w[1] - w[0]
                if target <= L:
                    mapped_sec_v = w[0] + target
                    break
                target -= L
            shared_params['sec_v'] = mapped_sec_v
            del shared_params['sec_v_fraction']

        total_logl = 0.0
        import itertools

        from scipy.stats import multivariate_normal
        
        lower_bound = np.array([0.9, -0.1, -0.1])
        upper_bound = np.array([1.1, 0.1, 0.1])
        V_prior = 0.008
        
        for i, spec in enumerate(spectra):
            pc = precomp[i]
            local_params = {'c0': 0.0, 'c1': 0.0, 'c2': 0.0}
            # The negative of this is the purely additive absorption component A(theta)
            flux_zero_c = evaluate_frozen_model(
                velocity=spec['v'],
                shared_params=shared_params,
                local_params=local_params,
                model_type=model_type,
                sigma_v_kms=spec['sigma_v_kms']
            )
            A_theta = -flux_zero_c
            
            r_theta = pc['y'] + A_theta
            b_theta = pc['Phi'].T @ (pc['W'] * r_theta)
            
            try:
                c_hat = scipy.linalg.cho_solve(pc['chol'], b_theta)
            except np.linalg.LinAlgError:
                return -1e100
                
            chi2_min = np.sum(pc['W'] * r_theta**2) - np.dot(b_theta, c_hat)
            
            dist = multivariate_normal(c_hat, pc['H_inv'], allow_singular=True)
            P = 0.0
            for signs in itertools.product([0, 1], repeat=3):
                x_pt = np.where(signs, upper_bound, lower_bound)
                sign = (-1)**(3 - sum(signs))
                P += sign * dist.cdf(x_pt)
                
            if P <= 1e-300:
                return -1e100
                
            log_L_marg = pc['C_0'] - 0.5 * chi2_min + 1.5 * math.log(2*math.pi) - 0.5 * pc['logdet_H'] + math.log(P) - math.log(V_prior)
            total_logl += log_L_marg
            
        return total_logl
        
    sampler = NestedSampler(logl, ptform, ndim, bound='single', sample='slice', nlive=nlive, bootstrap=0, rstate=rstate)
    sampler.run_nested(dlogz=0.5, maxcall=50000, print_progress=False)
    res = sampler.results
    
    post_diag = {}
    if model_type in ['M3_centroid', 'M3_Dlocal']:
        v_shift_idx = shared_names.index('v_shift')
        weights = np.exp(res.logwt - res.logz[-1])
        v_shift_samples = res.samples[:, v_shift_idx]
        v_shift_mean = np.average(v_shift_samples, weights=weights)
        post_diag['v_shift_mean'] = v_shift_mean
        
    if model_type.startswith('M2'):
        weights = np.exp(res.logwt - res.logz[-1])
        f_D_idx = shared_names.index('f_D')
        alpha_idx = shared_names.index('alpha')
        
        f_D_samples = res.samples[:, f_D_idx]
        alpha_samples = res.samples[:, alpha_idx]
        
        p_lt_05 = float(np.sum(weights[f_D_samples < 0.5]))
        p_alpha_prior = float(np.sum(weights[(alpha_samples >= step13c.alpha_prior[0]) & (alpha_samples <= step13c.alpha_prior[1])]))
        
        alpha_mean = np.average(alpha_samples, weights=weights)
        alpha_std = math.sqrt(np.average((alpha_samples - alpha_mean)**2, weights=weights))
        
        post_diag['P_f_D_lt_0p5'] = p_lt_05
        post_diag['P_alpha_in_prior'] = p_alpha_prior
        post_diag['alpha_mean'] = alpha_mean
        post_diag['alpha_std'] = alpha_std
        
        edge_threshold = 0.00002
        at_lower = (alpha_mean - alpha_std) < (step13c.alpha_prior[0] + edge_threshold)
        at_upper = (alpha_mean + alpha_std) > (step13c.alpha_prior[1] - edge_threshold)
        
        if model_type == 'M2_full':
            post_diag['alpha_at_lower_edge'] = bool(at_lower)
            post_diag['alpha_at_upper_edge'] = bool(at_upper)
            
    if model_type == 'M2_primary_only':
        ml_idx = np.argmax(res.logl)
        post_diag['ml_sample'] = res.samples[ml_idx].tolist()
        post_diag['shared_names'] = shared_names
        post_diag['alpha_at_upper_edge'] = bool((alpha_mean + alpha_std) > step13c.alpha_prior[1])
        
    post_diag['max_logl'] = float(np.max(res.logl))
    post_diag['eff_samples'] = float(res.eff)
    post_diag['ncall'] = int(np.sum(res.ncall))
        
    return res.logz[-1], res.logzerr[-1], post_diag
