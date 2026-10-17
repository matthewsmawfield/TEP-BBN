"""Conditional uncertainty propagation for an adopted power-law conversion."""
import math


def density_interval(central_density, log10_column_sigma, exponent=2/3):
    if not math.isfinite(central_density) or central_density <= 0:
        raise ValueError('Central density must be finite and positive')
    if not math.isfinite(log10_column_sigma) or log10_column_sigma < 0:
        raise ValueError('Log-column sigma must be finite and nonnegative')
    if not math.isfinite(exponent):
        raise ValueError('Exponent must be finite')
    factor = 10**abs(exponent*log10_column_sigma)
    return central_density/factor, central_density*factor
