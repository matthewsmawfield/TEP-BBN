"""Numerically stable ionization balance; no new physical assumptions."""
import numpy as np


def ionized_fraction(ratio):
    """Positive root of x**2 = ratio * (1-x), including neutral/full limits."""
    q = np.asarray(ratio, dtype=float)
    if np.any(np.isnan(q)) or np.any(q < 0):
        raise ValueError("Ionization balance ratio must be nonnegative")
    out = np.ones_like(q)
    low = q < 1.0
    root = np.sqrt(q[low])
    out[low] = 2.0 * root / (root + np.sqrt(q[low] + 4.0))
    high = ~low
    out[high] = 2.0 / (1.0 + np.sqrt(1.0 + 4.0 / q[high]))
    return float(out) if out.ndim == 0 else out
