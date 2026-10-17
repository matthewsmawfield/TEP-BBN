#!/usr/bin/env python3
"""
Canonical TEP screening operator (Paper 0 v0.15 sec.7; TEP steps 27/54/56/57).

The corpus-selected kinetic sector is the two-branch form

    P_{,X} = k * sqrt(xi) + 2*xi,     xi = |X|/Lambda_X^4.

The environment-tabulation benchmark evaluates xi_proxy = (g/g_t)^2.
This reproduces step 54; it is not the exact action identity for a solved
scalar gradient, whose Paper-0 convention includes the factor 1/2.
The input g here is an acceleration proxy, not a newly solved field.

with k = 4 sqrt(2) |beta_A| g_t / a_0 = 16.0287 fixed by the empirical
acceleration anchor a_0 = 1.2e-10 m/s^2, and g_t = c H0 / (2 beta_A^2) =
3.4001944264e-10 m/s^2.  The inverse stiffness S_Sigma = 1/P_{,X} is the
source-charge / shear response projection of the solved nonlinear field,
evaluated at the embedding ambient kinetic value X_env (the object's own
co-generated field is excluded — Paper 0 sec.7 two-body convention).

The legacy unit-term baseline P_{,X} = 1 + 2*xi is retained as a
cross-check column only; it reverts to a Keplerian tail and is rejected
by the master-sector admissibility scan (step_54).

Reproduction of the step_54 environment tabulation (rel. err < 1e-9):
  Sun 1 AU          g=5.93e-3   -> S_Sigma = 1.644e-15
  Cassini limb      g=107       -> S_Sigma = 5.049e-24
  MW solar circle   g=2e-10     -> S_Sigma = 9.88e-2
  Void/cosmic web   g=1e-12     -> S_Sigma = 21.2   (anti-screening branch)
"""

import numpy as np

G_T = 3.4001944264419963e-10   # m/s^2, c H0 / (2 beta_A^2)
K_STAR = 16.02867024193226     # 4 sqrt(2) |beta_A| g_t / a_0
A0 = 1.2e-10                   # m/s^2, empirical acceleration anchor


def P_X(g_si, branch="two_branch"):
    """Kinetic stiffness at ambient Newtonian-scale gradient g (m/s^2)."""
    xi = (np.asarray(g_si, dtype=float) / G_T) ** 2
    if branch == "two_branch":
        return K_STAR * np.sqrt(xi) + 2.0 * xi
    return 1.0 + 2.0 * xi


def S_Sigma_canonical(g_si, branch="two_branch"):
    """Derived source-charge projection S_Sigma = 1/P_{,X} at ambient g."""
    return 1.0 / P_X(g_si, branch)


# Solar-system convenience constants
G_SI = 6.674e-11      # m^3 kg^-1 s^-2
C_SI = 2.99792458e8   # m/s
M_SUN_KG = 1.989e30


# ---------------------------------------------------------------------------
# Absorber-regime amplitude transfer ansatz (Paper 29 phenomenological sector)
# ---------------------------------------------------------------------------
# This is the calibrated potential-depth transfer prescription used by the
# Gate-4 transport steps.  It is NOT the canonical kinetic operator above:
# S_A(Phi) and S_Sigma(E) are distinct projections of the common nonlinear
# field (Paper 0 sec.7) and are not numerically interchangeable.  The ansatz
# parameters were fixed by the three-anchor calibration (absorber unscreened,
# solar ~1e-4, galactic ~0.013); the canonical operator independently returns
# the same screened/unscreened assignments at both ends (step_21).

PHI_HALF_C2 = 1.59e-7   # dimensionless potential-depth half-transition
N_SCREEN = 3.56         # transfer slope


def s_transfer_depth(Phi_c2):
    """Paper 29 absorber-regime amplitude transfer ansatz in |Phi|/c^2."""
    return 1.0 / (1.0 + (np.asarray(Phi_c2, dtype=float) / PHI_HALF_C2) ** N_SCREEN)
R_SUN_M = 6.96e8
AU_M = 1.496e11


def dphi_dr_sun_eV2_canonical():
    """Solved solar-surface scalar gradient under the canonical operator.

    Unscreened gradient: dphi/dr = M_Pl * 2|beta_A| (g/c^2) in eV^2 units;
    the canonical screening suppresses it by S_Sigma(g_surf).
    """
    hbarc_eV_m = 1.9733e-7
    M_Pl_eV = 1.2209e28 / np.sqrt(8.0 * np.pi)  # reduced Planck mass, eV
    g_surf = G_SI * M_SUN_KG / R_SUN_M**2
    dphi_dr_unscr = M_Pl_eV * 2.0 * (g_surf / C_SI**2) * hbarc_eV_m
    return S_Sigma_canonical(g_surf) * dphi_dr_unscr
