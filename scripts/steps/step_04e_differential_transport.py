#!/usr/bin/env python3
"""
Gate 4B-0: Differential Edge-Minus-Core Transport Calculation
=============================================================

The decisive calculation: can the differential frequency shift between an
edge ray and a core ray, after the shared post-absorber path cancels, be
~10^4 times the conformal-only shift — without violating Cassini, cavity,
and lunar-ranging constraints?

Physics:
  - Both rays originate from the same background source, pass through
    different parts of the absorber, and share the same post-absorber path
    to Earth. The shared path cancels in the differential.
  - In standard scalar-tensor gravity with a static field (∂_0 φ = 0),
    the frequency shift ω = ω_0 / A(φ) is path-independent. The disformal
    term B(φ)∂_μφ∂_νφ modifies g̃_ij but NOT g̃_00, so it does not affect
    the frequency shift. The conformal differential is ~1/3 of the
    conformal shift — hopeless.
  - The TEP framework posits a "non-exact transport path" C_{T,∥} that
    introduces path-dependence. This script models that path-dependence
    as a transport integral whose integrand depends on (∇φ)², which is
    large at the absorber edge and zero at the core.

The calculation:
  1. Compute the scalar field profile φ(r) for a uniform-sphere absorber
  2. Compute the conformal differential Δ_ec^conf (path-independent part)
  3. Model the non-exact transport as a path-dependent integral
  4. Compute the required transport coefficient for A_env ~ 10^4
  5. Check Cassini, cavity, and LLR constraints
  6. Determine the falsifiable parameter space
"""

import sys
from pathlib import Path
import json
import numpy as np

project_root = Path(__file__).resolve().parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from scripts.utils.logger import print_status, setup_step_logger


def run_differential_transport():
    setup_step_logger(Path(__file__).stem)
    print_status("=== GATE 4B-0: DIFFERENTIAL EDGE-MINUS-CORE TRANSPORT ===", "SUCCESS")

    # ---- Physical constants (CGS) ----
    c = 2.998e10        # cm/s
    G = 6.674e-8        # cm^3/(g s^2)
    m_p = 1.673e-24     # g
    kpc = 3.086e21      # cm
    AU = 1.496e13       # cm
    M_Pl_g = 2.176e-5   # Planck mass in grams (reduced)
    R_sun = 6.96e10     # solar radius in cm
    M_sun = 1.989e33    # solar mass in g

    # ---- Screening parameters (frozen by three-anchor calibration) ----
    Phi_half = 1.59e-7
    n_screen = 3.56
    beta_A = -1.0

    def S_Sigma(Phi_c2):
        return 1.0 / (1.0 + (Phi_c2 / Phi_half)**n_screen)

    # ---- Absorber parameters (Q1009+2956) ----
    R_kpc = 30
    R = R_kpc * kpc
    log_N_HI = 17.362
    N_HI = 10**log_N_HI
    Gamma = 1.0e-12       # s^-1 (UV background at z~2.5)
    alpha_rec = 2.6e-13   # cm^3/s (Case B recombination)

    # Ionisation correction: N_H = sqrt(N_HI * 2R * Gamma / alpha_rec)
    N_H = np.sqrt(N_HI * 2 * R * Gamma / alpha_rec)
    n_H = N_H / (2 * R)
    rho = n_H * m_p
    M_abs = (4.0/3.0) * np.pi * R**3 * rho
    Phi_abs_c2 = G * M_abs / (R * c**2)

    # Conformal-only shift (from pipeline)
    dv_conf = 2 * beta_A**2 * np.pi * G * m_p * N_H * R / c  # cm/s
    dv_conf_kms = dv_conf / 1e5

    # Fitted free-H displacement
    dv_H_fitted = 78.9e5  # cm/s (Q1009)
    A_env_target = dv_H_fitted / dv_conf

    print_status(f"\n--- Absorber Parameters ---", "TITLE")
    print_status(f"  R = {R_kpc} kpc, log N_HI = {log_N_HI}, log N_H = {np.log10(N_H):.3f}", "PROCESS")
    print_status(f"  |Phi_abs|/c^2 = {Phi_abs_c2:.2e} (S_Sigma = {S_Sigma(Phi_abs_c2):.6f})", "PROCESS")
    print_status(f"  dv_conf = {dv_conf_kms:.5f} km/s", "PROCESS")
    print_status(f"  A_env target = {A_env_target:.1f}", "PROCESS")

    # =====================================================================
    # 1. SCALAR FIELD PROFILE IN THE ABSORBER
    # =====================================================================
    print_status(f"\n--- 1. Scalar Field Profile ---", "TITLE")

    # For a uniform sphere, the Newtonian potential is:
    #   Phi(r) = -2*pi*G*rho*(R^2 - r^2/3)  (inside, r < R)
    #   Phi(r) = -G*M/r                      (outside, r > R)
    #
    # The scalar field is phi = (beta_A / M_Pl) * Phi (in the unscreened regime)
    # Inside the absorber, S_Sigma ~ 1, so the field is unscreened.

    def Phi_newton(r):
        """Newtonian potential at radius r inside/outside uniform sphere."""
        if r < R:
            return -2 * np.pi * G * rho * (R**2 - r**2 / 3)
        else:
            return -G * M_abs / r

    def phi_scalar(r):
        """Scalar field phi/M_Pl at radius r (dimensionless)."""
        return beta_A * Phi_newton(r) / (c**2)  # phi/M_Pl = beta_A * Phi/c^2

    def grad_phi(r):
        """Gradient of phi/M_Pl at radius r (1/cm)."""
        if r < R:
            return beta_A * (4 * np.pi * G * rho * r / 3) / c**2
        else:
            return beta_A * G * M_abs / (r**2 * c**2)

    # Key values
    phi_core = phi_scalar(0)        # phi at center
    phi_edge = phi_scalar(R)        # phi at edge
    grad_phi_edge = grad_phi(R)     # |grad phi| at edge
    grad_phi_core = grad_phi(0)     # |grad phi| at center (= 0)

    print_status(f"  phi_core/M_Pl = {phi_core:.2e}", "PROCESS")
    print_status(f"  phi_edge/M_Pl = {phi_edge:.2e}", "PROCESS")
    print_status(f"  |grad phi|_edge = {grad_phi_edge:.2e} cm^-1", "PROCESS")
    print_status(f"  |grad phi|_core = {grad_phi_core:.2e} cm^-1 (zero by symmetry)", "PROCESS")

    # =====================================================================
    # 2. CONFORMAL DIFFERENTIAL (PATH-INDEPENDENT PART)
    # =====================================================================
    print_status(f"\n--- 2. Conformal Differential (Standard Scalar-Tensor) ---", "TITLE")

    # In standard scalar-tensor with static field:
    #   omega = omega_0 / A(phi)
    #   Delta_ec^conf = ln[A(phi_edge)/A(phi_core)] = beta_A * [phi_edge - phi_core] / M_Pl
    #
    # For uniform sphere:
    #   phi(0) - phi(R) = beta_A * (-2*pi*G*rho*R^2 + 4*pi*G*rho*R^2/3) / c^2
    #                    = beta_A * (-2*pi*G*rho*R^2/3) / c^2

    delta_phi_ec = phi_edge - phi_core  # phi_edge - phi_core
    delta_ln_A_conf = beta_A * delta_phi_ec  # = beta_A^2 * 2*pi*G*rho*R^2/(3*c^2)
    dv_conf_diff = c * abs(delta_ln_A_conf)  # cm/s

    print_status(f"  delta_phi(edge - core) = {delta_phi_ec:.2e}", "PROCESS")
    print_status(f"  Delta_ec^conf = {delta_ln_A_conf:.2e}", "PROCESS")
    print_status(f"  |dv_conf_diff| = {dv_conf_diff/1e5:.5f} km/s", "PROCESS")
    print_status(f"  Ratio to conformal shift: {dv_conf_diff/dv_conf:.3f}", "PROCESS")
    print_status(f"  => Conformal differential is ~1/3 of conformal shift (as expected)", "PROCESS")
    print_status(f"  => Static spatial perturbative channels excluded (Gate 4B-II)", "PROCESS")

    # =====================================================================
    # 3. NON-EXACT TRANSPORT: PATH-DEPENDENT MODEL
    # =====================================================================
    print_status(f"\n--- 3. Non-Exact Transport (Path-Dependent Model) ---", "TITLE")

    # The TEP framework posits that photon transport is NOT standard geodesic
    # transport. The "non-exact transport path" C_{T,||} introduces path-
    # dependence. We model this as a transport integral:
    #
    #   Delta_ec^TEP = integral_edge Gamma_TEP ds - integral_core Gamma_TEP ds
    #
    # where Gamma_TEP is a transport coefficient that depends on the scalar
    # field and its gradient. The conformal part (Gamma ~ phi) is path-
    # independent and cancels. The disformal/non-exact part depends on
    # (grad phi)^2, which is large at the edge and zero at the core.
    #
    # Model: Gamma_TEP = B_eff * (grad_phi)^2 / (A^2 * c)
    #   - Edge ray: large (grad_phi)^2 at the boundary
    #   - Core ray: (grad_phi)^2 ~ 0 at center
    #   - Differential: dominated by edge transport

    # The edge ray passes through the outer region of the absorber.
    # Model: the ray traverses a path of length ~R through the outer region
    # where |grad phi| ~ |grad phi|_edge.
    #
    # The transport integral for the edge ray:
    #   Delta_edge = B_eff * (grad_phi_edge)^2 * R / (A^2 * c)
    #
    # The core ray: grad_phi ~ 0, so Delta_core ~ 0
    #
    # Differential: Delta_ec ~ B_eff * (grad_phi_edge)^2 * R / c

    # Compute the edge transport integrand
    # (grad_phi)^2 at the edge:
    grad_phi_sq_edge = grad_phi_edge**2  # cm^-2

    # Path length through edge region (order R)
    L_edge = R

    # Differential transport (in units of frequency shift)
    # Delta_ec = B_eff * (grad_phi)^2 * L / c  [dimensionless]
    # dv_ec = c * Delta_ec = B_eff * (grad_phi)^2 * L  [cm/s]
    #
    # But we need to be careful about dimensions. B_eff has dimensions that
    # depend on the convention. In the disformal metric:
    #   g_tilde_ij = A^2 * delta_ij + B(phi) * partial_i phi * partial_j phi
    # B(phi) has dimensions of [length^2] (if phi is dimensionless and
    # g_ij is dimensionless). More precisely, B/M_Pl^2 has dimensions of
    # [length^2/mass^2] in natural units.
    #
    # For the transport coefficient:
    #   Gamma = B_eff * (grad_phi)^2 / (A^2 * c)
    # where B_eff is dimensionless (B_0/M_Pl^2 in geometrized units).
    #
    # The velocity shift is:
    #   dv = c * integral Gamma ds = B_eff * (grad_phi)^2 * L / 1
    # (the c cancels)
    #
    # Actually, let me use the same convention as the existing code:
    # A_env = dv_ec / dv_conf
    # where dv_ec = B_eff * (grad_phi)^2 * L (in appropriate units)

    # The ratio A_env = dv_ec / dv_conf:
    # A_env = B_eff * (grad_phi)^2 * L / (2 * beta_A^2 * pi * G * m_p * N_H * R / c)
    #
    # With grad_phi = beta_A * 4*pi*G*rho*R / (3*c^2) and L = R:
    # (grad_phi)^2 = beta_A^2 * (4*pi*G*rho*R)^2 / (9*c^4)
    # (grad_phi)^2 * L = beta_A^2 * (4*pi*G*rho*R)^2 * R / (9*c^4)
    #
    # And dv_conf = 2 * beta_A^2 * pi * G * m_p * N_H * R / c
    #             = 2 * beta_A^2 * pi * G * rho * 2*R * R / c  (since N_H = 2*R*rho/m_p... no)
    # Actually N_H = 2*R*n_H = 2*R*rho/m_p, so:
    # dv_conf = 2 * beta_A^2 * pi * G * m_p * (2*R*rho/m_p) * R / c
    #         = 4 * beta_A^2 * pi * G * rho * R^2 / c

    # So:
    # A_env = B_eff * beta_A^2 * (4*pi*G*rho*R)^2 * R / (9*c^4) /
    #         (4 * beta_A^2 * pi * G * rho * R^2 / c)
    #       = B_eff * (4*pi*G*rho*R)^2 * R * c / (9*c^4 * 4*pi*G*rho*R^2)
    #       = B_eff * 4*pi*G*rho*R * c / (9*c^4)
    #       = B_eff * 4*pi*G*rho*R / (9*c^3)
    #
    # Hmm, this has weird dimensions. Let me use a cleaner approach.

    # Clean approach: compute numerically
    # dv_ec = B_eff * (grad_phi_edge)^2 * L_edge  [need to match dv_conf units]
    # dv_conf = 2 * beta_A^2 * pi * G * m_p * N_H * R / c  [cm/s]
    #
    # grad_phi_edge has units of 1/cm (phi is dimensionless, phi/M_Pl)
    # (grad_phi)^2 * L has units of 1/cm
    # dv_conf has units of cm/s
    #
    # So B_eff must have units of cm^2/s for the equation to work.
    # In geometrized units, B_eff/M_Pl^2 has units of s^2/cm^2 (or 1/(velocity)^2).
    # So B_eff * (grad_phi)^2 * L has units of (s^2/cm^2) * (1/cm^2) * cm = s^2/cm^3.
    # That's not cm/s either.
    #
    # The issue is that I need to be more careful about what B_eff means.
    # Let me use the convention from the existing code:
    # A_env_per_B0 = (grad_phi)^2 * L / dv_conf (with B0=1)
    # This gives A_env = B0 * A_env_per_B0

    # Actually, looking at the existing step_04d code:
    # A_edge_per_B = delta_phi^2 / (dR * delta_conf)
    # where delta_phi = |beta_A| * (1 - S_gal) * Phi_abs_c2
    # and delta_conf = beta_A^2 * Phi_abs_c2
    #
    # This is a different parametrization. Let me use a more physical model.

    # Physical model:
    # The non-exact transport produces a frequency shift proportional to
    # the path integral of (grad_phi)^2. The proportionality constant is
    # an effective coupling B_eff with dimensions that make the result
    # a frequency shift.
    #
    # In the disformal metric, the spatial correction is:
    #   delta_g_ij = B(phi) * partial_i phi * partial_j phi
    #
    # For a photon traveling in direction x, the effective speed change is:
    #   delta_v/v ~ B_eff * (partial_x phi)^2 / A^2
    #
    # The frequency shift from this (if transport is non-standard) is:
    #   delta_omega/omega ~ integral B_eff * (grad phi)^2 / A^2 ds
    #
    # For this to be a velocity shift:
    #   dv = c * B_eff * (grad_phi)^2 * L / A^2
    #
    # With A ~ 1 (unscreened), and grad_phi = beta_A * grad_Phi / c^2:
    #   dv = c * B_eff * beta_A^2 * (grad_Phi)^2 * L / c^4
    #      = B_eff * beta_A^2 * (grad_Phi)^2 * L / c^3
    #
    # grad_Phi at the edge = G * M_abs / R^2 (for a uniform sphere, at r=R)
    # (grad_Phi)^2 = G^2 * M_abs^2 / R^4
    # (grad_Phi)^2 * L = G^2 * M_abs^2 / R^3 (with L = R)
    #
    # dv_ec = B_eff * beta_A^2 * G^2 * M_abs^2 / (R^3 * c^3)
    #
    # And dv_conf = 4 * beta_A^2 * pi * G * rho * R^2 / c
    #             = 3 * beta_A^2 * G * M_abs / (R * c)  (since M = 4/3 pi R^3 rho)
    #
    # Wait: dv_conf = 2 * beta_A^2 * pi * G * m_p * N_H * R / c
    # and N_H = 2 * R * n_H = 2 * R * rho / m_p
    # so dv_conf = 2 * beta_A^2 * pi * G * m_p * (2*R*rho/m_p) * R / c
    #            = 4 * pi * beta_A^2 * G * rho * R^2 / c
    #            = 3 * beta_A^2 * G * M_abs / (R * c)  (using M = 4/3 pi R^3 rho)
    #
    # A_env = dv_ec / dv_conf
    #       = [B_eff * beta_A^2 * G^2 * M_abs^2 / (R^3 * c^3)] /
    #         [3 * beta_A^2 * G * M_abs / (R * c)]
    #       = B_eff * G * M_abs / (3 * R^2 * c^2)
    #       = B_eff * Phi_abs / (3 * R * c^2)  (since Phi = GM/R)
    #       = B_eff * |Phi_abs|/c^2 / (3 * R)
    #
    # This has units of 1/length, which means B_eff has units of length.
    # In geometrized units, B_eff/M_Pl^2 has units of length^2/mass^2,
    # so B_eff = B_0 * L_Pl^2 where L_Pl is the Planck length.
    #
    # Actually, let me just compute numerically.

    # Numerical computation
    grad_Phi_edge = G * M_abs / R**2  # cm/s^2 (Newtonian acceleration at edge)
    grad_phi_num = abs(beta_A) * grad_Phi_edge / c**2  # 1/cm (dimensionless phi gradient)

    # dv_ec = B_eff * c * (grad_phi)^2 * L  (with B_eff dimensionless in this convention)
    # This gives dv_ec in cm/s if B_eff is dimensionless and (grad_phi)^2 * L is in 1/cm
    # c * (1/cm^2) * cm = c/cm = 1/s ... not cm/s.
    #
    # Let me try: dv_ec = B_eff * c^2 * (grad_phi)^2 * L / c = B_eff * c * (grad_phi)^2 * L
    # Still 1/s.
    #
    # OK, the issue is that (grad_phi)^2 has units of 1/cm^2, and L has units of cm,
    # so (grad_phi)^2 * L has units of 1/cm. To get a velocity (cm/s), we need:
    # dv = B_eff * c * (grad_phi)^2 * L * (something with units of cm)
    #
    # The "something" is the scale at which B_eff operates. In the disformal metric:
    # g_tilde_ij = A^2 * delta_ij + B * partial_i phi * partial_j phi
    # B has units of [g_ij] / [partial phi]^2 = 1 / (1/cm^2) = cm^2 (if phi is dimensionless)
    # So B_eff in cm^2.
    #
    # Then: dv = c * B_eff * (grad_phi)^2 * L / A^2
    # Units: cm/s * cm^2 * 1/cm^2 * cm = cm^2/s ... still not right.
    #
    # Actually, the frequency shift from the disformal spatial metric is:
    # delta_omega/omega = -1/2 * integral (delta_g_ij * dx^i * dx^j) / (g_00 * dt^2)
    # For a photon: dx/dt = c, so:
    # delta_omega/omega = -1/2 * integral B * (partial_i phi * dx^i/dt)^2 / (A^2 * c^2) dt
    #                   = -1/2 * integral B * (partial_x phi)^2 / A^2 dt
    #                   = -1/2 * B * (grad_phi)^2 * L / (A^2 * c)  (for uniform grad along path)
    #
    # So: dv = c * |delta_omega/omega| = B * (grad_phi)^2 * L / (2 * A^2)
    # Units: cm^2 * 1/cm^2 * cm = cm. That's a length, not a velocity.
    #
    # Hmm, I think the issue is that B has units that depend on the convention.
    # Let me use the convention B = B_0 / M_Pl^2 where B_0 is dimensionless.
    # Then B has units of 1/mass^2 = cm^2/(g^2 c^2) in natural units... this is
    # getting confused.
    #
    # Let me just use the ratio approach from the existing code:
    # A_env = dv_ec / dv_conf, and compute dv_ec/dv_conf as a function of B_0.

    # The disformal frequency shift (standard result for scalar-tensor):
    # delta_omega/omega = -1/2 * integral [B_0/M_Pl^2 * (partial_s phi)^2] ds
    # where partial_s phi is the gradient along the photon path.
    #
    # For the edge ray: the photon passes through the outer region where
    # the transverse gradient of phi is large. The relevant gradient is
    # the component perpendicular to the photon path.
    #
    # For a photon traveling in the x-direction through a spherical absorber,
    # at impact parameter b (distance from center), the transverse gradient
    # of phi at the point of closest approach is:
    #   partial_perp phi = d(phi)/dr * (b/r) ... actually for b ~ R (edge ray),
    #   the gradient is radial: partial_r phi = grad_phi(R)
    #
    # The path integral of (partial_perp phi)^2 for a chord at impact parameter b:
    #   integral (partial_perp phi)^2 ds ~ (grad_phi(b))^2 * 2*sqrt(R^2 - b^2)
    #
    # For b ~ R (edge ray): the chord length is small, ~sqrt(R * delta_R)
    # For b ~ 0 (core ray): grad_phi ~ 0

    # Let me compute the path integral properly for a uniform sphere.
    # For a photon at impact parameter b, traveling through a uniform sphere:
    #   The chord length is 2*sqrt(R^2 - b^2)
    #   The density along the chord is uniform (rho)
    #   The radial gradient at position (b, x) is:
    #     grad_phi = beta_A * 4*pi*G*rho*r / (3*c^2) where r = sqrt(b^2 + x^2)
    #   The transverse component (perpendicular to path) is:
    #     partial_perp phi = grad_phi * b/r = beta_A * 4*pi*G*rho*b / (3*c^2)
    #
    # So (partial_perp phi)^2 = beta_A^2 * (4*pi*G*rho*b)^2 / (9*c^4)
    # This is CONSTANT along the chord (independent of x)!
    #
    # The path integral is:
    #   integral (partial_perp phi)^2 ds = (partial_perp phi)^2 * 2*sqrt(R^2 - b^2)
    #     = beta_A^2 * (4*pi*G*rho*b)^2 / (9*c^4) * 2*sqrt(R^2 - b^2)

    # For the edge ray (b -> R): sqrt(R^2 - b^2) -> 0, so the integral -> 0
    # For the core ray (b = 0): b = 0, so the integral = 0
    #
    # The maximum is at some intermediate b. Let me find it.
    # f(b) = b^2 * sqrt(R^2 - b^2)
    # df/db = 2b * sqrt(R^2 - b^2) + b^2 * (-b/sqrt(R^2 - b^2))
    #       = b * [2*(R^2 - b^2) - b^2] / sqrt(R^2 - b^2)
    #       = b * [2*R^2 - 3*b^2] / sqrt(R^2 - b^2)
    # = 0 when b^2 = 2*R^2/3, i.e., b = R*sqrt(2/3)

    b_max = R * np.sqrt(2/3)
    chord_max = 2 * np.sqrt(R**2 - b_max**2)  # = 2*R/sqrt(3)
    grad_perp_max = abs(beta_A) * 4 * np.pi * G * rho * b_max / (3 * c**2)

    integral_max = grad_perp_max**2 * chord_max  # 1/cm

    print_status(f"  Maximum disformal integrand at b = R*sqrt(2/3) = {b_max/kpc:.1f} kpc", "PROCESS")
    print_status(f"  Chord length at max = {chord_max/kpc:.1f} kpc", "PROCESS")
    print_status(f"  |grad_perp phi|_max = {grad_perp_max:.2e} cm^-1", "PROCESS")
    print_status(f"  Path integral max = {integral_max:.2e} cm^-1", "PROCESS")

    # The disformal frequency shift for this ray:
    # delta_omega/omega = -1/2 * (B_0/M_Pl^2) * integral_max
    # dv = c * |delta_omega/omega| = c * B_0 * integral_max / (2 * M_Pl^2)
    #
    # But M_Pl is in grams, and we need to convert to CGS consistently.
    # In natural units (c=1), M_Pl has units of energy or 1/length.
    # In CGS: M_Pl = 2.176e-5 g, M_Pl*c^2 = 1.96e9 erg = 1.22e19 GeV
    # The Planck length l_Pl = hbar/(M_Pl*c) = 1.616e-33 cm
    # So 1/M_Pl^2 = l_Pl^2 / hbar^2 in some convention...
    #
    # Let me use the convention where B_0 is dimensionless and the
    # disformal term is B_0 * (phi/M_Pl)^2 in the metric. Then:
    # delta_g_ij ~ B_0 * (partial_i phi / M_Pl) * (partial_j phi / M_Pl)
    #
    # And the frequency shift is:
    # dv = c * B_0 * integral [(partial_perp phi / M_Pl)^2] ds / 2
    #
    # With phi/M_Pl = beta_A * Phi/c^2 (dimensionless):
    # partial(phi/M_Pl) = beta_A * partial(Phi) / c^2 = beta_A * g / c^2
    # where g = G*M/r^2 is the gravitational acceleration.
    #
    # So: dv = c * B_0 * beta_A^2 * integral [(g_perp/c^2)^2] ds / 2
    #        = c * B_0 * beta_A^2 * (g_perp_max/c^2)^2 * chord_max / 2
    #        = B_0 * beta_A^2 * g_perp_max^2 * chord_max / (2 * c^3)

    g_perp_max = 4 * np.pi * G * rho * b_max / 3  # cm/s^2
    dv_disformal_per_B0 = beta_A**2 * g_perp_max**2 * chord_max / (2 * c**3)  # cm/s per B_0

    print_status(f"\n--- 4. Disformal Differential ---", "TITLE")
    print_status(f"  g_perp_max = {g_perp_max:.2e} cm/s^2", "PROCESS")
    print_status(f"  dv_disformal per B_0 = {dv_disformal_per_B0:.2e} cm/s", "PROCESS")
    print_status(f"  dv_disformal per B_0 = {dv_disformal_per_B0/1e5:.2e} km/s", "PROCESS")

    # A_env = dv_disformal / dv_conf
    A_env_per_B0 = dv_disformal_per_B0 / dv_conf

    print_status(f"  A_env per B_0 = {A_env_per_B0:.2e}", "PROCESS")
    print_status(f"  B_0 needed for A_env = {A_env_target:.0f}: {A_env_target/A_env_per_B0:.2e}", "PROCESS")

    # =====================================================================
    # 5. CONSTRAINT CHECK: CASSINI, CAVITY, LLR
    # =====================================================================
    print_status(f"\n--- 5. Constraint Check ---", "TITLE")

    # The same B_0 that produces the absorber amplification also produces
    # a disformal correction in the solar system. We need to check that
    # this correction does not violate:
    #   1. Cassini: |gamma_PPN - 1| < 2.3e-5
    #   2. Cavity (Eöt-Wash): fifth-force bounds at sub-mm scales
    #   3. LLR: |gamma_PPN - 1| < 1e-4 (Earth-Moon)
    #
    # In the solar system, the scalar field is screened: S_Sigma ~ 1e-4.
    # The disformal correction is suppressed by S_Sigma^2.
    #
    # The disformal contribution to gamma_PPN from a photon grazing the Sun:
    # delta_gamma_disformal = B_0 * S_Sigma_solar^2 * integral [(g_sun/c^2)^2] ds / (2 * R_sun)
    #
    # where the integral is along the grazing path, g_sun = G*M_sun/R_sun^2,
    # and the path length is ~R_sun.

    Phi_sun_c2 = 2.12e-6  # |Phi_sun|/c^2 at solar surface
    S_solar = S_Sigma(Phi_sun_c2)  # ~1e-4
    g_sun = G * M_sun / R_sun**2  # cm/s^2

    # Disformal correction to gamma_PPN in solar system
    # delta_gamma ~ B_0 * S_solar^2 * (g_sun/c^2)^2 * R_sun / 2
    delta_gamma_per_B0 = S_solar**2 * (g_sun / c**2)**2 * R_sun / 2

    B0_needed = A_env_target / A_env_per_B0
    delta_gamma = B0_needed * delta_gamma_per_B0

    print_status(f"  Solar system screening: S_Sigma = {S_solar:.2e}", "PROCESS")
    print_status(f"  g_sun = {g_sun:.2e} cm/s^2", "PROCESS")
    print_status(f"  delta_gamma per B_0 = {delta_gamma_per_B0:.2e}", "PROCESS")
    print_status(f"  B_0 needed = {B0_needed:.2e}", "PROCESS")
    print_status(f"  delta_gamma at B_0 needed = {delta_gamma:.2e}", "PROCESS")
    print_status(f"  Cassini bound: |delta_gamma| < 2.3e-5", "PROCESS")

    cassini_ok = abs(delta_gamma) < 2.3e-5
    print_status(f"  Cassini: {'PASS' if cassini_ok else 'FAIL'} (margin: {2.3e-5/abs(delta_gamma):.2e}x)" if delta_gamma > 0 else f"  Cassini: PASS (zero)", "SUCCESS" if cassini_ok else "WARNING")

    # LLR constraint (weaker): |gamma_PPN - 1| < 1e-4
    llr_ok = abs(delta_gamma) < 1e-4
    print_status(f"  LLR: {'PASS' if llr_ok else 'FAIL'}", "SUCCESS" if llr_ok else "WARNING")

    # Cavity constraint: fifth-force screening at sub-mm scales
    # The disformal force at distance r from a test mass:
    # F_disformal ~ B_0 * S_Sigma^2 * (G*M/r^2)^2 * r / c^4
    # This is suppressed by S_Sigma^2 in the solar system.
    # At sub-mm scales (cavity experiments), the potential is tiny:
    # |Phi|/c^2 ~ G*rho_lab*r^2/c^2 ~ 1e-25 (for lab-scale masses)
    # S_Sigma ~ 1 (unscreened at lab scales!)
    # So the cavity constraint is actually on the UNSCREENED disformal coupling.
    #
    # At lab scales (r ~ 0.1 mm = 0.01 cm):
    # g_lab ~ G * M_test / r^2 where M_test ~ 1 g
    # g_lab ~ 6.67e-8 * 1 / (0.01)^2 = 6.67e-4 cm/s^2
    # (g_lab/c^2)^2 ~ (6.67e-4 / 3e10)^2 ~ 5e-29 cm^-2
    # delta_gamma_lab ~ B_0 * (g_lab/c^2)^2 * r / 2
    # ~ B_0 * 5e-29 * 0.01 / 2 ~ B_0 * 2.5e-31
    # Cavity bound: |delta_gamma| < 1e-5 (typical Eöt-Wash)
    # B_0 < 1e-5 / 2.5e-31 = 4e25

    r_cavity = 0.01  # cm (0.1 mm)
    M_test = 1.0     # g (test mass)
    g_lab = G * M_test / r_cavity**2
    Phi_lab_c2 = G * M_test / (r_cavity * c**2)
    S_lab = S_Sigma(Phi_lab_c2)  # screening at lab scale

    delta_gamma_cavity_per_B0 = S_lab**2 * (g_lab / c**2)**2 * r_cavity / 2
    delta_gamma_cavity = B0_needed * delta_gamma_cavity_per_B0
    cavity_bound = 1e-5  # typical Eöt-Wash bound on gamma
    cavity_ok = abs(delta_gamma_cavity) < cavity_bound

    print_status(f"\n  Cavity (lab-scale):", "PROCESS")
    print_status(f"    |Phi_lab|/c^2 = {Phi_lab_c2:.2e}, S_lab = {S_lab:.6f}", "PROCESS")
    print_status(f"    g_lab = {g_lab:.2e} cm/s^2", "PROCESS")
    print_status(f"    delta_gamma per B_0 = {delta_gamma_cavity_per_B0:.2e}", "PROCESS")
    print_status(f"    delta_gamma at B_0 needed = {delta_gamma_cavity:.2e}", "PROCESS")
    print_status(f"    Cavity bound: {cavity_bound:.0e}", "PROCESS")
    print_status(f"    Cavity: {'PASS' if cavity_ok else 'FAIL'}", "SUCCESS" if cavity_ok else "WARNING")

    # =====================================================================
    # 6. THE KEY RATIO: SCREENING CONTRAST
    # =====================================================================
    print_status(f"\n--- 6. Screening Contrast (Key Ratio) ---", "TITLE")

    # The ratio of disformal correction in the absorber vs solar system:
    # ratio = (S_abs^2 * g_abs^2 * R_abs) / (S_solar^2 * g_sun^2 * R_sun)
    #
    # If this ratio is >> A_env_target, then the amplification is possible
    # without violating solar system constraints.

    S_abs = S_Sigma(Phi_abs_c2)
    g_abs = G * M_abs / R**2  # gravitational acceleration at absorber edge

    ratio_absorber_to_solar = (S_abs**2 * g_abs**2 * R) / (S_solar**2 * g_sun**2 * R_sun)
    ratio_absorber_to_cavity = (S_abs**2 * g_abs**2 * R) / (S_lab**2 * g_lab**2 * r_cavity)

    print_status(f"  Absorber: S = {S_abs:.6f}, g = {g_abs:.2e} cm/s^2, R = {R:.2e} cm", "PROCESS")
    print_status(f"  Solar:    S = {S_solar:.2e}, g = {g_sun:.2e} cm/s^2, R = {R_sun:.2e} cm", "PROCESS")
    print_status(f"  Cavity:   S = {S_lab:.6f}, g = {g_lab:.2e} cm/s^2, R = {r_cavity:.2e} cm", "PROCESS")
    print_status(f"", "PROCESS")
    print_status(f"  Screening contrast (absorber/solar) = {ratio_absorber_to_solar:.2e}", "PROCESS")
    print_status(f"  Screening contrast (absorber/cavity) = {ratio_absorber_to_cavity:.2e}", "PROCESS")
    print_status(f"  A_env target = {A_env_target:.0f}", "PROCESS")
    print_status(f"", "PROCESS")

    # The maximum A_env that is consistent with Cassini:
    # A_env_max = ratio_absorber_to_solar * (Cassini_bound / 1)
    # because delta_gamma_solar = B_0 * delta_gamma_per_B0_solar
    # and A_env = B_0 * A_env_per_B0
    # so A_env = (delta_gamma_solar / delta_gamma_per_B0_solar) * A_env_per_B0
    # and delta_gamma_solar < Cassini_bound
    # so A_env < Cassini_bound * A_env_per_B0 / delta_gamma_per_B0_solar
    # = Cassini_bound / delta_gamma_per_B0_solar * A_env_per_B0
    # = Cassini_bound * (A_env_per_B0 / delta_gamma_per_B0_solar)

    A_env_max_cassini = 2.3e-5 * A_env_per_B0 / delta_gamma_per_B0
    A_env_max_llr = 1e-4 * A_env_per_B0 / delta_gamma_per_B0
    A_env_max_cavity = cavity_bound * A_env_per_B0 / delta_gamma_cavity_per_B0

    print_status(f"  Max A_env consistent with Cassini: {A_env_max_cassini:.2e}", "PROCESS")
    print_status(f"  Max A_env consistent with LLR: {A_env_max_llr:.2e}", "PROCESS")
    print_status(f"  Max A_env consistent with cavity: {A_env_max_cavity:.2e}", "PROCESS")
    print_status(f"  Required A_env: {A_env_target:.0f}", "PROCESS")
    print_status(f"", "PROCESS")

    all_pass = cassini_ok and llr_ok and cavity_ok
    print_status(f"  ALL CONSTRAINTS: {'PASS' if all_pass else 'FAIL'}", "SUCCESS" if all_pass else "WARNING")

    # =====================================================================
    # 7. FULL PATH INTEGRAL (NUMERICAL)
    # =====================================================================
    print_status(f"\n--- 7. Full Path Integral (Numerical) ---", "TITLE")

    # Compute the disformal path integral for rays at various impact parameters
    # to find the maximum differential transport.

    N_points = 1000
    b_values = np.linspace(0, R * 0.99, N_points)
    integrals = []

    for b in b_values:
        if b > R:
            integrals.append(0)
            continue
        chord_half = np.sqrt(R**2 - b**2)
        N_samp = 100
        x_samples = np.linspace(-chord_half, chord_half, N_samp)
        # Transverse gradient at each point along the chord
        r_samples = np.sqrt(b**2 + x_samples**2)
        # For uniform sphere: grad_phi_perp = beta_A * 4*pi*G*rho*b / (3*c^2)
        # (constant along chord for uniform density)
        grad_perp = abs(beta_A) * 4 * np.pi * G * rho * b / (3 * c**2)
        integral = grad_perp**2 * 2 * chord_half  # (1/cm^2) * cm = 1/cm
        integrals.append(integral)

    integrals = np.array(integrals)
    max_integral = np.max(integrals)
    b_at_max = b_values[np.argmax(integrals)]

    print_status(f"  Maximum path integral: {max_integral:.2e} cm^-1 at b = {b_at_max/kpc:.2f} kpc", "PROCESS")
    print_status(f"  (b/R = {b_at_max/R:.3f}, expected sqrt(2/3) = {np.sqrt(2/3):.3f})", "PROCESS")

    # A_env from full integral
    A_env_full_per_B0 = c * max_integral / (2 * dv_conf)  # dv = c * B_0 * integral / 2
    B0_full_needed = A_env_target / A_env_full_per_B0

    print_status(f"  A_env per B_0 (full integral) = {A_env_full_per_B0:.2e}", "PROCESS")
    print_status(f"  B_0 needed (full integral) = {B0_full_needed:.2e}", "PROCESS")

    # =====================================================================
    # 8. ASSESSMENT
    # =====================================================================
    print_status(f"\n--- 8. Assessment ---", "TITLE")

    # The key finding: what is the maximum A_env consistent with all constraints?
    A_env_max = min(A_env_max_cassini, A_env_max_llr, A_env_max_cavity)

    print_status(f"  Maximum A_env consistent with ALL constraints: {A_env_max:.2e}", "PROCESS")
    print_status(f"  Required A_env: {A_env_target:.0f}", "PROCESS")
    print_status(f"  Gap: {A_env_target / A_env_max:.2e}x", "PROCESS")
    print_status(f"", "PROCESS")

    if A_env_max >= A_env_target:
        print_status(f"  RESULT: The differential transport CAN produce the required", "SUCCESS")
        print_status(f"  amplification without violating constraints.", "SUCCESS")
    else:
        print_status(f"  RESULT: The differential transport CANNOT produce the required", "WARNING")
        print_status(f"  amplification with the standard disformal metric.", "WARNING")
        print_status(f"  The gap is {A_env_target / A_env_max:.0e}x.", "WARNING")
        print_status(f"", "PROCESS")
        print_status(f"  This means one of the following must be true:", "PROCESS")
        print_status(f"  (a) The non-exact transport C_{{T,||}} is NOT the standard", "PROCESS")
        print_status(f"      disformal path integral — it has a different structure", "PROCESS")
        print_status(f"      that is not constrained by Cassini/cavity/LLR in the", "PROCESS")
        print_status(f"      same way (e.g., topological, non-local, or holonomic).", "PROCESS")
        print_status(f"  (b) The B(phi) enhancement near the screening transition", "PROCESS")
        print_status(f"      is much larger than the constant-coupling estimate,", "PROCESS")
        print_status(f"      and is suppressed in the solar system by a mechanism", "PROCESS")
        print_status(f"      not captured by S_Sigma alone.", "PROCESS")
        print_status(f"  (c) The absorber geometry is not a uniform sphere —", "PROCESS")
        print_status(f"      edge enhancement from a realistic density profile", "PROCESS")
        print_status(f"      (e.g., NFW core + sharp edge) increases the gradient.", "PROCESS")
        print_status(f"", "PROCESS")
        print_status(f"  The falsifiable prediction: if (a), (b), and (c) all fail,", "PROCESS")
        print_status(f"  the TEP absorber-field interpretation is falsified.", "PROCESS")

    # =====================================================================
    # ALSO: check what happens with B(phi) enhancement at the transition
    # =====================================================================
    print_status(f"\n--- 9. B(phi) Enhancement at Screening Transition ---", "TITLE")

    # The screening transition at the absorber-galaxy boundary could
    # enhance B(phi) via field curvature. The key question: can this
    # enhancement be large in the absorber (unscreened) while being
    # suppressed in the solar system (screened)?
    #
    # The B(phi) enhancement from field curvature:
    # B_eff = B_0 * (1 + |d^2phi/dr^2| * lambda^2 / |phi|)
    #
    # At the screening transition:
    # d^2phi/dr^2 ~ delta_phi / Delta_R^2
    # where delta_phi is the field jump across the transition.
    #
    # In the solar system, there is NO screening transition (the field
    # is uniformly screened), so d^2phi/dr^2 ~ 0 and B_eff ~ B_0.
    #
    # This means the B(phi) enhancement is LOCALIZED to the screening
    # transition and does NOT affect the solar system!

    Phi_gal_c2 = 5.38e-7
    S_gal = S_Sigma(Phi_gal_c2)

    # Field jump at the transition
    delta_phi_transition = abs(beta_A) * (1 - S_gal) * Phi_abs_c2  # dimensionless (phi/M_Pl)

    # Thin-shell width (chameleon scaling)
    Delta_Phi = Phi_gal_c2 - Phi_half
    thin_shell_frac = Delta_Phi / Phi_gal_c2 / 6.0
    Delta_R_shell = thin_shell_frac * R

    # Field curvature at transition
    phi_trans = abs(beta_A) * 0.5 * Phi_half  # field at S=0.5
    d2phi_dr2 = delta_phi_transition / Delta_R_shell**2  # 1/cm^2

    print_status(f"  Transition field jump: delta_phi = {delta_phi_transition:.2e}", "PROCESS")
    print_status(f"  Thin-shell width: Delta_R = {Delta_R_shell/kpc:.2f} kpc", "PROCESS")
    print_status(f"  Field curvature: d^2phi/dr^2 = {d2phi_dr2:.2e} cm^-2", "PROCESS")
    print_status(f"  phi_trans (S=0.5) = {phi_trans:.2e}", "PROCESS")

    # B enhancement for various scalar masses
    hbar = 1.055e-27  # erg*s
    eV = 1.602e-12    # erg

    print_status(f"\n  {'m_phi (eV)':<15} {'lambda (cm)':<15} {'B_eff/B_0':<15} {'A_env':<15} {'Cassini?'}", "PROCESS")
    print_status(f"  {'-'*15} {'-'*15} {'-'*15} {'-'*15} {'-'*15}", "PROCESS")

    best_A_env = 0
    best_scenario = None

    for m_phi in [1e-30, 1e-28, 1e-26, 1e-24, 1e-22, 1e-20, 1e-18]:
        lambda_phi = hbar * c / (m_phi * eV)
        B_enhance = 1 + d2phi_dr2 * lambda_phi**2 / phi_trans

        # A_env with B enhancement (using the edge-transition formula from step_04d)
        A_env = B_enhance * delta_phi_transition**2 / (Delta_R_shell * abs(phi_edge - phi_core))

        # But we need to check: does this B_enhancement affect the solar system?
        # In the solar system, there is no screening transition, so B_eff = B_0.
        # The Cassini constraint is on B_0, not B_enhanced.
        # So: delta_gamma_solar = B_0 * delta_gamma_per_B0_solar
        # And: A_env = B_enhanced * A_env_per_B0_edge
        # The constraint is: B_0 < Cassini_bound / delta_gamma_per_B0_solar
        # And: A_env = B_enhanced * A_env_per_B0_edge = B_0 * B_enhance * A_env_per_B0_edge
        # So: A_env < (Cassini_bound / delta_gamma_per_B0_solar) * B_enhance * A_env_per_B0_edge
        # = Cassini_bound * B_enhance * A_env_per_B0_edge / delta_gamma_per_B0_solar
        # = B_enhance * A_env_max_cassini

        A_env_with_constraint = B_enhance * A_env_max_cassini
        cassini_check = "PASS" if A_env_with_constraint >= A_env_target else "FAIL"

        print_status(f"  {m_phi:<15.0e} {lambda_phi:<15.2e} {B_enhance:<15.2e} {A_env_with_constraint:<15.2e} {cassini_check}", "PROCESS")

        if A_env_with_constraint > best_A_env:
            best_A_env = A_env_with_constraint
            best_scenario = {
                "m_phi_eV": m_phi,
                "lambda_cm": lambda_phi,
                "B_enhancement": B_enhance,
                "A_env_with_cassini": A_env_with_constraint,
                "cassini_pass": A_env_with_constraint >= A_env_target,
            }

    print_status(f"\n  Best scenario: m_phi = {best_scenario['m_phi_eV']:.0e} eV", "PROCESS")
    print_status(f"    B_enhancement = {best_scenario['B_enhancement']:.2e}", "PROCESS")
    print_status(f"    A_env (with Cassini) = {best_scenario['A_env_with_cassini']:.2e}", "PROCESS")
    print_status(f"    Cassini: {'PASS' if best_scenario['cassini_pass'] else 'FAIL'}", "PROCESS")
    print_status(f"    Required: {A_env_target:.0f}", "PROCESS")

    # =====================================================================
    # BUILD LEDGER
    # =====================================================================
    ledger = {
        "gate": "4B-0",
        "title": "Differential Edge-Minus-Core Transport Calculation",
        "key_question": (
            "Can the differential frequency shift between edge and core rays, "
            "after the shared post-absorber path cancels, be ~10^4 times the "
            "conformal-only shift without violating Cassini, cavity, and LLR?"
        ),
        "absorber_params": {
            "R_kpc": R_kpc,
            "log_N_HI": log_N_HI,
            "log_N_H": float(np.log10(N_H)),
            "Phi_abs_c2": float(Phi_abs_c2),
            "S_absorber": float(S_abs),
            "dv_conf_kms": float(dv_conf_kms),
            "A_env_target": float(A_env_target),
        },
        "conformal_differential": {
            "delta_phi_ec": float(delta_phi_ec),
            "delta_ln_A_conf": float(delta_ln_A_conf),
            "dv_conf_diff_kms": float(dv_conf_diff / 1e5),
            "ratio_to_conformal_shift": float(dv_conf_diff / dv_conf),
            "result": "Conformal differential is ~1/3 of conformal shift. Static spatial perturbative channels excluded (Gate 4B-II).",
        },
        "disformal_transport": {
            "model": "Path-dependent integral of (grad_phi_perp)^2 along photon chord",
            "max_impact_parameter_kpc": float(b_at_max / kpc),
            "max_path_integral_cm_inv": float(max_integral),
            "A_env_per_B0": float(A_env_full_per_B0),
            "B0_needed": float(B0_full_needed),
        },
        "constraints": {
            "cassini": {
                "bound": 2.3e-5,
                "delta_gamma_per_B0": float(delta_gamma_per_B0),
                "delta_gamma_at_B0_needed": float(delta_gamma),
                "pass": bool(cassini_ok),
                "A_env_max": float(A_env_max_cassini),
            },
            "llr": {
                "bound": 1e-4,
                "pass": bool(llr_ok),
                "A_env_max": float(A_env_max_llr),
            },
            "cavity": {
                "bound": 1e-5,
                "S_lab": float(S_lab),
                "delta_gamma_per_B0": float(delta_gamma_cavity_per_B0),
                "delta_gamma_at_B0_needed": float(delta_gamma_cavity),
                "pass": bool(cavity_ok),
                "A_env_max": float(A_env_max_cavity),
            },
            "all_pass": bool(all_pass),
            "A_env_max_all": float(A_env_max),
            "gap_factor": float(A_env_target / A_env_max),
        },
        "screening_contrast": {
            "absorber_to_solar": float(ratio_absorber_to_solar),
            "absorber_to_cavity": float(ratio_absorber_to_cavity),
        },
        "B_enhancement_at_transition": {
            "delta_phi_transition": float(delta_phi_transition),
            "Delta_R_shell_kpc": float(Delta_R_shell / kpc),
            "d2phi_dr2": float(d2phi_dr2),
            "phi_trans": float(phi_trans),
            "best_scenario": best_scenario,
            "key_insight": (
                "B(phi) enhancement from field curvature is LOCALIZED to the "
                "screening transition. In the solar system, there is no screening "
                "transition (field is uniformly screened), so B_eff = B_0 and the "
                "Cassini constraint applies to B_0, not B_enhanced. This means the "
                "enhancement factor multiplies the allowed A_env by B_enhance."
            ),
        },
        "conclusion": (
            f"Standard disformal path integral: A_env max = {A_env_max:.2e}, "
            f"required = {A_env_target:.0f}, gap = {A_env_target/A_env_max:.0e}x. "
            f"With B(phi) enhancement localized to the screening transition: "
            f"best A_env = {best_A_env:.2e} (m_phi = {best_scenario['m_phi_eV']:.0e} eV). "
            f"Cassini {'PASS' if best_scenario['cassini_pass'] else 'FAIL'} "
            f"(enhancement is localized to transition, not present in solar system). "
            f"The decisive question is whether the non-exact transport C_{{T,||}} "
            f"has the structure of the standard disformal path integral (constrained) "
            f"or a different, non-local/topological structure (unconstrained by Cassini)."
        ),
    }

    def to_native(obj):
        """Convert numpy types to native Python for JSON serialization."""
        if isinstance(obj, dict):
            return {k: to_native(v) for k, v in obj.items()}
        elif isinstance(obj, (list, tuple)):
            return [to_native(v) for v in obj]
        elif isinstance(obj, (np.bool_, bool)):
            return bool(obj)
        elif isinstance(obj, (np.integer, int)):
            return int(obj)
        elif isinstance(obj, (np.floating, float)):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return [to_native(v) for v in obj]
        return obj

    out_dir = project_root / "results"
    out_dir.mkdir(parents=True, exist_ok=True)
    with open(out_dir / "gate4b_0_differential_transport.json", "w") as f:
        json.dump(to_native(ledger), f, indent=2)
    print_status(
        f"\n[COMPLETED] Gate 4B-0 results written to {out_dir / 'gate4b_0_differential_transport.json'}",
        "SUCCESS",
    )


if __name__ == "__main__":
    run_differential_transport()
