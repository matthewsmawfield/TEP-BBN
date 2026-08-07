"""
Voigt profile fitting utilities for TEP-BBN analysis.

This module implements standard, temporal-shear, and hybrid Voigt profile
models for fitting D/H absorption systems.
"""

import numpy as np
from scipy.special import wofz

from .isotopic_shift import temporal_shear_shift


def voigt_profile(x, center, fwhm, shape):
    """
    Compute Voigt profile.

    Parameters
    ----------
    x : array
        Wavelength or velocity grid
    center : float
        Line center position
    fwhm : float
        Full width at half maximum
    shape : float
        Voigt shape parameter (ratio of Lorentzian to Gaussian width)

    Returns
    -------
    array
        Voigt profile normalized to unit area
    """
    sigma = fwhm / 2.3548  # Convert FWHM to sigma
    gamma = fwhm * shape / 2.0

    z = (x - center + 1j * gamma) / (sigma * np.sqrt(2))
    return np.real(wofz(z)) / (sigma * np.sqrt(2 * np.pi))


def standard_dh_model(x, hi_params, di_params):
    """
    Standard H I + D I Voigt model (M0).

    Parameters
    ----------
    x : array
        Wavelength or velocity grid
    hi_params : dict
        H I line parameters (center, fwhm, shape, column_density)
    di_params : dict
        D I line parameters (center, fwhm, shape, column_density)

    Returns
    -------
    array
        Combined H I + D I profile
    """
    hi_profile = hi_params["column_density"] * voigt_profile(
        x, hi_params["center"], hi_params["fwhm"], hi_params["shape"]
    )

    di_profile = di_params["column_density"] * voigt_profile(
        x, di_params["center"], di_params["fwhm"], di_params["shape"]
    )

    return hi_profile + di_profile


def temporal_shear_model(x, hi_params, shear_params):
    """
    H I only + temporal-shear shifted component (M1).

    This model tests whether apparent D I can be explained as H I
    shifted by temporal shear.

    Parameters
    ----------
    x : array
        Wavelength or velocity grid
    hi_params : dict
        Primary H I line parameters
    shear_params : dict
        Temporal shear parameters (delta_ln_A, fwhm, shape, column_density)

    Returns
    -------
    array
        H I + temporal-shear shifted H I profile
    """
    # Primary H I component
    hi_profile = hi_params["column_density"] * voigt_profile(
        x, hi_params["center"], hi_params["fwhm"], hi_params["shape"]
    )

    # Temporal-shear shifted component (phantom D)
    velocity_shift = temporal_shear_shift(shear_params["delta_ln_A"])
    shear_center = hi_params["center"] + velocity_shift

    shear_profile = shear_params["column_density"] * voigt_profile(
        x, shear_center, shear_params["fwhm"], shear_params["shape"]
    )

    return hi_profile + shear_profile


def hybrid_model(x, hi_params, di_params, shear_params):
    """
    Hybrid: real D/H plus temporal-shear nuisance field (M2).

    This model allows for both real deuterium and temporal-shear contamination.

    Parameters
    ----------
    x : array
        Wavelength or velocity grid
    hi_params : dict
        H I line parameters
    di_params : dict
        D I line parameters
    shear_params : dict
        Temporal shear parameters

    Returns
    -------
    array
        H I + D I + temporal-shear shifted component
    """
    # Standard H I + D I
    standard = standard_dh_model(x, hi_params, di_params)

    # Additional temporal-shear component
    velocity_shift = temporal_shear_shift(shear_params["delta_ln_A"])
    shear_center = hi_params["center"] + velocity_shift

    shear_profile = shear_params["column_density"] * voigt_profile(
        x, shear_center, shear_params["fwhm"], shear_params["shape"]
    )

    return standard + shear_profile


def h_interloper_model(x, hi_primary_params, hi_interloper_params):
    """
    H I-only ordinary velocity-interloper model (M3).

    This model tests whether apparent D can be explained as ordinary
    H I velocity structure rather than temporal shear.

    Parameters
    ----------
    x : array
        Wavelength or velocity grid
    hi_primary_params : dict
        Primary H I line parameters
    hi_interloper_params : dict
        Interloper H I line parameters (velocity-shifted component)

    Returns
    -------
    array
        H I primary + H I interloper profile
    """
    # Primary H I component
    hi_primary = hi_primary_params["column_density"] * voigt_profile(
        x,
        hi_primary_params["center"],
        hi_primary_params["fwhm"],
        hi_primary_params["shape"],
    )

    # Interloper H I component (velocity-shifted)
    hi_interloper = hi_interloper_params["column_density"] * voigt_profile(
        x,
        hi_interloper_params["center"],
        hi_interloper_params["fwhm"],
        hi_interloper_params["shape"],
    )

    return hi_primary + hi_interloper


def multi_component_model(x, components, model_type="standard"):
    """
    Multi-component Voigt model for complex absorbers.

    Parameters
    ----------
    x : array
        Wavelength or velocity grid
    components : list of dict
        List of component parameters
    model_type : str
        'standard', 'temporal_shear', or 'hybrid'

    Returns
    -------
    array
        Multi-component profile
    """
    profile = np.zeros_like(x)

    for comp in components:
        if model_type == "standard":
            profile += standard_dh_model(x, comp["hi"], comp["di"])
        elif model_type == "temporal_shear":
            profile += temporal_shear_model(x, comp["hi"], comp["shear"])
        elif model_type == "hybrid":
            profile += hybrid_model(x, comp["hi"], comp["di"], comp["shear"])

    return profile


def chi_squared(observed, model, uncertainty):
    """
    Compute chi-squared statistic.

    Parameters
    ----------
    observed : array
        Observed flux or optical depth
    model : array
        Model prediction
    uncertainty : array
        Measurement uncertainties

    Returns
    -------
    float
        Chi-squared value
    """
    return np.sum(((observed - model) / uncertainty) ** 2)


def reduced_chi_squared(observed, model, uncertainty, dof):
    """
    Compute reduced chi-squared statistic.

    Parameters
    ----------
    observed : array
        Observed flux or optical depth
    model : array
        Model prediction
    uncertainty : array
        Measurement uncertainties
    dof : int
        Degrees of freedom (n_data - n_parameters)

    Returns
    -------
    float
        Reduced chi-squared value
    """
    return chi_squared(observed, model, uncertainty) / dof
