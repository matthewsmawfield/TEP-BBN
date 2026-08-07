"""
Isotopic shift formalism for TEP-BBN analysis.

This module implements the temporal-shear line-shift formalism for testing
whether deuterium isotope identification can be contaminated by temporal shear.
"""

import sys

sys.path.insert(0, "../../")
from core.constants import c_kms


def temporal_shear_shift(delta_ln_A):
    """
    Convert temporal shear to velocity shift.

    Parameters
    ----------
    delta_ln_A : float
        Temporal shear amplitude (dimensionless)

    Returns
    -------
    float
        Velocity shift in km/s
    """
    return c_kms * delta_ln_A


def deuterium_gate_velocity():
    """
    Return the target velocity shift to mimic deuterium isotope offset.

    The deuterium isotope shift is approximately 82 km/s, corresponding
    to the D/H abundance ratio offset in absorption-line spectroscopy.

    Returns
    -------
    float
        Target velocity shift in km/s
    """
    return 82.0  # km/s


def required_delta_ln_A():
    """
    Return the required temporal shear to mimic deuterium isotope shift.

    Delta ln A ≈ Delta v / c ≈ 82 / 299792 ≈ 2.7×10^-4

    Returns
    -------
    float
        Required temporal shear amplitude (dimensionless)
    """
    return deuterium_gate_velocity() / c_kms


def isotopic_shift_formula(delta_ln_A):
    """
    Full isotopic shift formula for temporal shear.

    Δν/ν ≈ Δ ln A_cloud
    Δv_T ≈ c Δ ln A_cloud

    Parameters
    ----------
    delta_ln_A : float
        Temporal shear amplitude (dimensionless)

    Returns
    -------
    dict
        Dictionary with shift parameters:
        - 'delta_ln_A': temporal shear
        - 'velocity_shift_kms': velocity shift in km/s
        - 'fractional_frequency_shift': Δν/ν
    """
    return {
        "delta_ln_A": delta_ln_A,
        "velocity_shift_kms": temporal_shear_shift(delta_ln_A),
        "fractional_frequency_shift": delta_ln_A,
    }


def compare_to_deuterium_gate(delta_ln_A):
    """
    Compare a given temporal shear to the deuterium gate requirement.

    Parameters
    ----------
    delta_ln_A : float
        Temporal shear amplitude to test

    Returns
    -------
    dict
        Dictionary with comparison results:
        - 'delta_ln_A': tested value
        - 'required_delta_ln_A': gate requirement
        - 'ratio': tested/required
        - 'velocity_shift_kms': tested velocity shift
        - 'required_velocity_kms': gate velocity shift
        - 'matches_gate': boolean if within 10% of requirement
    """
    required = required_delta_ln_A()
    ratio = delta_ln_A / required
    matches = 0.9 <= ratio <= 1.1

    return {
        "delta_ln_A": delta_ln_A,
        "required_delta_ln_A": required,
        "ratio": ratio,
        "velocity_shift_kms": temporal_shear_shift(delta_ln_A),
        "required_velocity_kms": deuterium_gate_velocity(),
        "matches_gate": matches,
    }
