"""Checked interpolation of a resolved peak on a uniformly spaced grid."""
import numpy as np


def interpolated_peak(x, values):
    x, values = np.asarray(x, dtype=float), np.asarray(values, dtype=float)
    if x.ndim != 1 or values.shape != x.shape or len(x) < 3:
        raise ValueError('Peak interpolation needs matching 1D arrays with at least three samples')
    if not np.all(np.isfinite(x)) or not np.all(np.isfinite(values)):
        raise ValueError('Peak samples must be finite')
    spacing = np.diff(x)
    if spacing[0] <= 0 or not np.allclose(spacing, spacing[0], rtol=1e-10, atol=0):
        raise ValueError('Peak grid must be increasing and uniformly spaced')
    i = int(np.argmax(values))
    if i == 0 or i == len(values) - 1:
        raise ValueError('Peak is unresolved at search-window boundary; expand the window')
    left, middle, right = values[i-1:i+2]
    if middle <= left or middle <= right:
        raise ValueError('Peak is not a unique local maximum')
    curvature = left - 2 * middle + right
    offset = 0.5 * (left - right) / curvature
    return float(x[i] + spacing[0] * offset)
