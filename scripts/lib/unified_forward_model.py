"""
Unified Forward Model for TEP-BBN Q1009 Analysis.

This module provides a SINGLE forward-model function used by both the
observational likelihood (step_02) and the Monte Carlo simulation
(step_03).  This guarantees that simulation and observation pass through
the same optical-depth, LSF-convolution, continuum, zero-level, masking,
pixelization, and noise pipeline.

The key design choice is that the FULL parameter vector
    theta_full = [theta_shared (141), theta_cand (0-5)]
is passed to a single objective.  The BlockCoordinateOptimizer profiles
shared parameters under every hypothesis, eliminating the asymmetry where
a free-H candidate could absorb frozen-model errors.
"""

import numpy as np
from scipy.stats import t as student_t

from scripts.lib.residual_engine import likelihood_residuals
from scripts.lib.model_builder import build_model_components
from scripts.lib.physical_rt_engine import RadiativeTransferEngine
from scripts.lib.residual_engine import compute_residuals

# Canonical transition list — must match residual_engine._LYMAN
LYMAN_TRANSITIONS = [
    "HI_Lya", "HI_Lyb", "HI_Lyg", "HI_Lyd", "HI_Lye",
    "HI_Ly6", "HI_Ly7", "HI_Ly8", "HI_Ly9", "HI_Ly10",
    "HI_Ly11", "HI_Ly12", "HI_Ly13", "HI_Ly14", "HI_Ly21",
]
METAL_TRANSITIONS = {
    "C_IV": ["CIV_1548", "CIV_1550"],
    "C_III": ["CIII_977"],
    "C_II": ["CII_1334"],
    "Si_IV": ["SiIV_1393", "SiIV_1402"],
}


def compute_total_tau(grouped_comps, wave, engine):
    """Compute total optical depth for a single wavelength array."""
    tau = np.zeros_like(wave)
    if grouped_comps["H_I"]:
        tau += engine.compute_optical_depth(wave, LYMAN_TRANSITIONS, grouped_comps["H_I"])
    if grouped_comps["D_I"]:
        tau += engine.compute_optical_depth(wave, LYMAN_TRANSITIONS, grouped_comps["D_I"])
    for ion, trans in METAL_TRANSITIONS.items():
        if grouped_comps.get(ion):
            tau += engine.compute_optical_depth(wave, trans, grouped_comps[ion])
    return tau


def generate_model_flux(theta_shared, theta_cand, model_name, pm,
                        z_abs_ref, c_kms, data_blocks, engine):
    """
    Generate the absorption template flux (before continuum fitting)
    for every data block.  This is the function used by the MC simulator
    to produce noiseless base fluxes, and by the likelihood to compute
    residuals.  Same code path in both cases.
    """
    grouped = build_model_components(
        model_name, theta_shared, theta_cand, pm, z_abs_ref, c_kms
    )
    fluxes = []
    for block in data_blocks:
        tau = compute_total_tau(grouped, block["wave"], engine)
        flux = engine.apply_convolution(np.exp(-tau), block["wave"], block["vsig"])
        fluxes.append(flux)
    return fluxes


def unified_objective(theta_full, model_name, n_shared, pm,
                      z_abs_ref, c_kms, data_blocks, engine, noise_cfg):
    """
    Single objective function for all hypotheses.

    theta_full = [theta_shared (n_shared), theta_cand (0-5)]
    Returns negative log-likelihood under the student-t noise model.

    The continuum (3-basis polynomial per block) and zero level are
    profiled analytically inside compute_residuals — identical for
    observation and simulation.
    """
    theta_shared = theta_full[:n_shared]
    theta_cand = theta_full[n_shared:] if len(theta_full) > n_shared else None

    grouped = build_model_components(
        model_name, theta_shared, theta_cand, pm, z_abs_ref, c_kms
    )
    res = compute_residuals(grouped, data_blocks, engine)
    v_res = likelihood_residuals(res)
    ll = np.sum(
        student_t.logpdf(
            v_res, noise_cfg["nu"], noise_cfg["location"], noise_cfg["scale"]
        )
    )
    return -float(ll)


def make_objective(model_name, n_shared, pm, z_abs_ref, c_kms,
                   data_blocks, engine, noise_cfg):
    """Return a closure over the unified objective for a given hypothesis."""
    def obj(theta_full):
        return unified_objective(
            theta_full, model_name, n_shared, pm,
            z_abs_ref, c_kms, data_blocks, engine, noise_cfg
        )
    return obj


def make_bounds_shared(pm):
    """Return (lower, upper) bounds for the shared parameter vector."""
    return list(zip(pm.bounds_lower, pm.bounds_upper))


def make_bounds_full(pm, cand_bounds):
    """
    Return full bounds = shared bounds + candidate bounds.
    cand_bounds is a list of (low, high) tuples for the candidate params.
    """
    return make_bounds_shared(pm) + list(cand_bounds)
