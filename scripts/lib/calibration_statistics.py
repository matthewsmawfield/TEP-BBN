"""Predictive calibration against retained true-D simulation vectors."""
import numpy as np
from scipy.stats import beta


def empirical_tail(observed_score, simulated_scores):
    scores = np.asarray(simulated_scores, dtype=float)
    if not np.isfinite(observed_score) or not np.all(np.isfinite(scores)) or not len(scores):
        raise ValueError('Calibration scores must be finite and nonempty')
    n = len(scores)
    k = int(np.count_nonzero(scores >= observed_score))
    return {'exceedances': k, 'n': n, 'p_add_one': (k + 1) / (n + 1),
            'empirical_frequency': k / n,
            'tail_upper_95': float(beta.ppf(.95, k + 1, n - k)) if k < n else 1.0}


def covariance_metric(diff, covariance, ridge=1e-6):
    """Mahalanobis metric with dimensionless correlation regularization."""
    scale = np.sqrt(np.diag(covariance))
    if not np.all(np.isfinite(scale)) or np.any(scale <= 0):
        raise ValueError('Every calibration statistic must have positive finite variance')
    corr = covariance / np.outer(scale, scale)
    corr = (corr + corr.T) / 2
    eigenvalues, vectors = np.linalg.eigh(corr + ridge * np.eye(len(scale)))
    if eigenvalues.min() <= 0:
        raise ValueError('Regularized correlation is not positive definite')
    z = diff / scale
    return float(np.sum((vectors.T @ z) ** 2 / eigenvalues)), corr


def calibrate_vectors(observed, simulated, ridge=1e-6):
    """Use empirical null means consistently; leave each calibration draw out
    of the mean/covariance used to score that draw. Observations never enter
    the estimated null. All probabilities retain finite-sampling metadata.
    """
    x = np.asarray(simulated, dtype=float)
    obs = np.asarray(observed, dtype=float)
    n, d = x.shape
    if n < 20 or obs.shape != (d,) or not np.all(np.isfinite(x)) or not np.all(np.isfinite(obs)):
        raise ValueError('Require >=20 finite simulation vectors matching the observation')
    mean = np.mean(x, axis=0)
    cov = np.cov(x, rowvar=False)
    centered = x - mean
    loo_diffs = n / (n - 1) * centered
    marginal = [empirical_tail(abs(obs[j] - mean[j]), abs(loo_diffs[:, j])) for j in range(d)]
    observed_distance, corr = covariance_metric(obs - mean, cov, ridge)
    null_distances = []
    for delta, diff in zip(centered, loo_diffs):
        loo_cov = ((n - 1) * cov - n / (n - 1) * np.outer(delta, delta)) / (n - 2)
        null_distances.append(covariance_metric(diff, loo_cov, ridge)[0])
    return {'mean': mean.tolist(), 'covariance': cov.tolist(), 'correlation': corr.tolist(),
            'dimensionless_ridge': ridge, 'correlation_eigenvalues': np.linalg.eigvalsh(corr).tolist(),
            'centered_sigmas': (abs(obs - mean) / np.std(x, axis=0, ddof=1)).tolist(),
            'marginal': marginal, 'joint': empirical_tail(observed_distance, null_distances),
            'observed_mahalanobis_squared': observed_distance,
            'null_mahalanobis_squared': null_distances,
            'scope': 'Empirical-null-centered, leave-one-out predictive scores; fixed input pixel mask.'}
