#!/usr/bin/env python3
"""
Gate 4B-0: Cavity-vs-Loop Profile

Compares scalar-field transport along an open cavity (single sightline
through the absorber) versus a closed loop (two parallel sightlines
at different impact parameters, connected tangentially).

Two distinct observables are separated:

  1. Conformal clock shift (spectroscopic observable, g̃₀₀).
     Δln A = ln A(edge) − ln A(core) is an endpoint difference — an
     exact differential. It is nonzero for a cavity (open path) and
     vanishes on any closed loop: ∮ d(ln A) = 0.

  2. Disformal transport (optical time-transfer observable, spatial metric).
     C_{T,∥} = B(φ) (∂_ℓ φ)² is a path integral of a squared derivative
     — always positive, never an exact differential. It is nonzero for
     a cavity and ACCUMULATES on a closed loop: both legs contribute
     positively, so ∮ C_{T,∥} dℓ = I_dis(b₁) + I_dis(b₂) + I_tangential.

For a static field (∂₀φ = 0) the disformal term B(φ)(∂₀φ)² = 0 in g̃₀₀,
so the disformal sector does not affect clock rates — it affects photon
propagation through the spatial metric. The two observables are physically
distinct: the conformal part is a clock-rate shift (km/s), the disformal
part is a photon transport phase (cm⁻¹ per B_eff, where B_eff has units
of cm so that c × B_eff × I_dis has units of cm/s).

The cavity-vs-loop profile quantifies:
  1. The conformal profile ln A(φ(r)) along each sightline
  2. The disformal transport profile along each sightline
  3. How the loop isolates the disformal transport by canceling
     the conformal clock shift, while the disformal part accumulates
  4. The loop-to-cavity ratio for the disformal transport

Absorber model: uniform-density sphere, Q1009+2956 parameters.
"""

import sys
from pathlib import Path
import json
import numpy as np

project_root = Path(__file__).resolve().parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from scripts.utils.logger import print_status, setup_step_logger
from scripts.lib.canonical_screening import s_transfer_depth, PHI_HALF_C2, N_SCREEN


def run_cavity_loop_profile():
    setup_step_logger(Path(__file__).stem)
    print_status("=== GATE 4B-0: CAVITY-VS-LOOP PROFILE ===", "SUCCESS")

    # ---- Physical constants (CGS) ----
    c = 2.998e10        # cm/s
    G = 6.674e-8        # cm^3/(g s^2)
    m_p = 1.673e-24     # g
    kpc = 3.086e21      # cm

    # ---- Frozen parameters (from step_04b) ----
    beta_A = -1.0
    log_N_HI = 17.362
    N_HI = 10**log_N_HI
    z_abs = 2.5042
    dv_target = 81.6  # km/s

    # Ionisation correction
    Gamma = 1.0e-12      # s^-1
    alpha_rec = 2.6e-13  # cm^3/s

    # Absorber geometry
    R_kpc = 30
    R = R_kpc * kpc  # cm

    # Total hydrogen column and density
    N_H = np.sqrt(N_HI * 2 * R * Gamma / alpha_rec)
    log_N_H = np.log10(N_H)
    n_H = N_H / (2 * R)  # cm^-3
    rho = n_H * m_p      # g/cm^3

    # Absorber mass and potential
    M_abs = (4.0 / 3.0) * np.pi * R**3 * rho
    Phi_abs_c2 = G * M_abs / (R * c**2)

    # Screening
    Phi_half = PHI_HALF_C2
    n_screen = N_SCREEN
    Phi_gal_c2 = 5.38e-7

    S_abs = s_transfer_depth(Phi_abs_c2)
    S_gal = s_transfer_depth(Phi_gal_c2)

    # Conformal-only amplitude (center vs. background, full Poisson Green)
    dv_conf = 2 * beta_A**2 * np.pi * G * m_p * N_H * R / c  # cm/s
    dv_conf_kms = dv_conf / 1e5
    A_env_target = dv_target * 1e5 / dv_conf

    print_status(f"\n--- Absorber Parameters ---", "TITLE")
    print_status(f"  R = {R_kpc} kpc, log N_H = {log_N_H:.2f}", "PROCESS")
    print_status(f"  rho = {rho:.2e} g/cm³, n_H = {n_H:.2e} cm⁻³", "PROCESS")
    print_status(f"  |Phi_abs|/c² = {Phi_abs_c2:.2e} (S = {S_abs:.4f})", "PROCESS")
    print_status(f"  |Phi_gal|/c² = {Phi_gal_c2:.2e} (S = {S_gal:.4f})", "PROCESS")
    print_status(f"  |dv_conf| (center vs. background) = {dv_conf_kms:.5f} km/s", "PROCESS")
    print_status(f"  A_env target = {A_env_target:.2e}", "PROCESS")

    # =====================================================================
    # SCALAR FIELD PROFILE IN UNIFORM SPHERE
    # =====================================================================
    # Poisson equation: ∇²δφ = (β_A/M_Pl) ρ
    # Solution inside uniform sphere (r < R):
    #   K(r) = 2πGρ(R² - r²/3)    [density-weighted Green integral]
    #   δφ(r) = -(β_A/M_Pl) K(r)
    #   Δln A(r) = (β_A/M_Pl) δφ(r) = -(β_A²/M_Pl²) K(r) = -β_A² × 2|Φ(r)|/c²
    #
    # K(0) = 2πGρR²           (maximum at center)
    # K(R) = 4πGρR²/3         (at surface)
    #
    # The conformal clock shift is deepest at the center, shallowest at the edge.

    Phi_0_c2 = 2 * np.pi * G * rho * R**2 / c**2  # |Φ(center)|/c²
    Phi_R_c2 = 2 * np.pi * G * rho * (2 * R**2 / 3) / c**2  # |Φ(surface)|/c²

    print_status(f"\n--- Scalar Field Profile (Uniform Sphere) ---", "TITLE")
    print_status(f"  |Φ(0)|/c² = {Phi_0_c2:.2e} (center)", "PROCESS")
    print_status(f"  |Φ(R)|/c² = {Phi_R_c2:.2e} (surface)", "PROCESS")
    print_status(f"  Δln A(0) = -β_A² × 2|Φ(0)|/c² = {-beta_A**2 * 2 * Phi_0_c2:.2e}", "PROCESS")
    print_status(f"  Δln A(R) = -β_A² × 2|Φ(R)|/c² = {-beta_A**2 * 2 * Phi_R_c2:.2e}", "PROCESS")

    # Differential edge-core conformal shift (spectroscopic observable)
    dlnA_conf = beta_A**2 * 2 * (Phi_0_c2 - Phi_R_c2)  # positive = edge faster than core
    dv_conf_edge_core = c * dlnA_conf / 1e5  # km/s

    print_status(f"  Δln A(edge-core) = {dlnA_conf:.2e}", "PROCESS")
    print_status(f"  |Δv_conf(edge-core)| = {abs(dv_conf_edge_core):.5f} km/s", "PROCESS")
    print_status(f"  (This is 1/3 of the full conformal amplitude, since |Φ(R)| = (2/3)|Φ(0)|)", "PROCESS")

    # =====================================================================
    # CAVITY PROFILE: Line-of-sight at impact parameter b
    # =====================================================================
    # For a sightline at impact parameter b through a uniform sphere:
    #   r² = b² + s²,  r < R when |s| < s_max = sqrt(R² - b²)
    #   |Φ(r)|/c² = (2πGρ/3c²)(3R² - r²) = (2πGρ/3c²)(3R² - b² - s²)
    #   Δln A(s) = -β_A² × 2|Φ(r(s))|/c²  (parabolic in s)
    #
    # Cavity conformal integral (edge minus core):
    #   ∫ d(ln A) = ln A(s_max) - ln A(0) = Δln A(edge) - Δln A(core)
    #   For b=0: edge = s=±R (surface), core = s=0 (center)
    #   For b>0: edge = s=±s_max (surface), core = s=0 (closest approach, r=b)
    #
    # Disformal transport along sightline:
    #   ∂_r(δφ/M_Pl) = -β_A × 4πGρr/(3c²)
    #   [∂_r(δφ/M_Pl)]² = β_A² × (4πGρ/(3c²))² × r²
    #   r̂·ℓ̂ = s/r  (projection of radial unit vector onto LOS)
    #   C_{T,∥}(s) = B_eff × [∂_r(δφ/M_Pl)]² × (r̂·ℓ̂)²
    #              = B_eff × β_A² × (4πGρ/(3c²))² × s²
    #
    #   The r² from the gradient cancels with (s/r)² from the projection,
    #   leaving s². The disformal transport per unit length is independent
    #   of impact parameter b — only the integration range s_max(b) depends
    #   on b.
    #
    #   I_dis(b) = B_eff × β_A² × (4πGρ/(3c²))² × 2s_max³/3
    #
    # Units: I_dis has units of cm⁻¹ (per B_eff). B_eff has units of cm
    # (so that B_eff × [∂_r(δφ/M_Pl)]² is dimensionless, matching the
    # metric perturbation h_{ij}^{dis}). The velocity equivalent is
    # Δv_dis = c × B_eff × I_dis (cm/s), which is dimensionally consistent.

    print_status(f"\n--- Cavity Profile: Sightline at Impact Parameter b ---", "TITLE")
    print_status(f"  Conformal: clock shift (endpoint difference, spectroscopic)", "PROCESS")
    print_status(f"  Disformal: transport integral (path integral, time-transfer)", "PROCESS")
    print_status(f"  B_eff has units of cm; I_dis has units of cm⁻¹ per B_eff", "PROCESS")

    b_values = [0, 0.1, 0.3, 0.5, 0.7, 0.9]  # fraction of R
    n_points = 1000

    print_status(f"\n  {'b/R':<8} {'s_max/R':<10} {'Δln A(cavity)':<15} "
                 f"{'Δv_conf(km/s)':<15} {'I_dis/B(cm⁻¹)':<15} {'Δv_dis/B(km/s)':<15}",
                 "PROCESS")
    print_status(f"  {'-'*8} {'-'*10} {'-'*15} {'-'*15} {'-'*15} {'-'*15}", "PROCESS")

    cavity_results = []
    for b_frac in b_values:
        b = b_frac * R
        s_max = np.sqrt(R**2 - b**2) if b < R else 0

        if s_max == 0:
            continue

        # Conformal cavity integral: edge (s=s_max) minus core (s=0)
        dlnA_core = -beta_A**2 * 2 * (2 * np.pi * G * rho / (3 * c**2)) * (3 * R**2 - b**2)
        dlnA_edge = -beta_A**2 * 2 * (2 * np.pi * G * rho / (3 * c**2)) * (3 * R**2 - R**2)
        dlnA_cavity = dlnA_edge - dlnA_core  # edge minus core
        dv_cavity = abs(c * dlnA_cavity / 1e5)  # km/s

        # Disformal transport integral (per B_eff, units of cm⁻¹)
        coeff_dimless = beta_A**2 * (4 * np.pi * G * rho / (3 * c**2))**2  # cm⁻⁴
        I_dis_per_B = coeff_dimless * (2 * s_max**3 / 3)  # cm⁻¹ per B_eff(cm)
        # Velocity equivalent: c × B_eff × I_dis → cm/s; divide by 1e5 for km/s
        # Here per B_eff = 1 cm:
        dv_dis_per_B = c * I_dis_per_B / 1e5  # km/s per B_eff(cm)

        result = {
            "b_fraction": b_frac,
            "b_cm": float(b),
            "s_max_cm": float(s_max),
            "s_max_fraction": float(s_max / R),
            "dlnA_cavity": float(dlnA_cavity),
            "dv_conf_cavity_kms": float(dv_cavity),
            "I_dis_per_B_cm_inv": float(I_dis_per_B),
            "dv_dis_per_B_kms": float(dv_dis_per_B),
        }
        cavity_results.append(result)

        print_status(
            f"  {b_frac:<8.1f} {s_max/R:<10.3f} {dlnA_cavity:<15.2e} "
            f"{dv_cavity:<15.5f} {I_dis_per_B:<15.2e} {dv_dis_per_B:<15.2e}",
            "PROCESS",
        )

    # =====================================================================
    # LOOP PROFILE: Two parallel sightlines forming a closed loop
    # =====================================================================
    # Loop = sightline at b₁ (forward) + tangential connection
    #       + sightline at b₂ (backward) + tangential connection
    #
    # Conformal loop integral:
    #   ∮ d(ln A) = 0  (exact differential — vanishes on any closed path)
    #
    # Disformal loop integral:
    #   C_{T,∥} = B(φ)(∂_ℓ φ)² is always positive (squared derivative).
    #   Traversing a leg backward flips ∂_ℓ φ → -∂_ℓ φ, but
    #   (∂_ℓ φ)² → (∂_ℓ φ)² (unchanged). dℓ is the positive path element.
    #   So the backward integral equals the forward integral.
    #
    #   ∮ C_{T,∥} dℓ = I_dis(b₁) + I_dis(b₂) + I_tangential
    #
    #   The tangential legs have r̂·ℓ̂ ≈ 0 (perpendicular to radial
    #   direction at the absorber edge), so C_{T,∥} ≈ 0 there.
    #
    #   The loop integral is the SUM of both legs, not the difference.
    #   The disformal transport ACCUMULATES around the loop.
    #
    #   The loop isolates the disformal transport by canceling the
    #   conformal clock shift. The disformal signal in the loop is
    #   the total accumulated transport from both legs.

    print_status(f"\n--- Loop Profile: Two Parallel Sightlines ---", "TITLE")
    print_status(f"  Loop = sightline at b₁ (forward) + sightline at b₂ (backward)", "PROCESS")
    print_status(f"  Conformal loop integral = 0 (exact differential)", "PROCESS")
    print_status(f"  Disformal loop integral = I_dis(b₁) + I_dis(b₂) (accumulates, not cancels)", "PROCESS")
    print_status(f"  (∂_ℓ φ)² is always positive — backward traversal does not change sign", "PROCESS")

    b1_result = cavity_results[0]  # b=0

    loop_results = []
    print_status(f"\n  {'b₂/R':<8} {'Δv_conf(loop)':<15} {'I_dis/B(loop)':<15} "
                 f"{'Δv_dis/B(loop)':<15} {'Loop/cavity ratio':<18}", "PROCESS")
    print_status(f"  {'-'*8} {'-'*15} {'-'*15} {'-'*15} {'-'*18}", "PROCESS")

    for res in cavity_results[1:]:  # skip b=0
        b2_frac = res["b_fraction"]

        # Conformal loop integral = 0 (always, exact differential)
        dv_conf_loop = 0.0

        # Disformal loop integral = I_dis(b₁) + I_dis(b₂) (SUM, not difference)
        I_dis_loop = b1_result["I_dis_per_B_cm_inv"] + res["I_dis_per_B_cm_inv"]
        dv_dis_loop_per_B = c * I_dis_loop / 1e5  # km/s per B_eff(cm)

        # Loop-to-cavity ratio: how much larger is the loop signal than
        # the single-leg cavity signal?
        cavity_dis = b1_result["I_dis_per_B_cm_inv"]
        loop_ratio = I_dis_loop / cavity_dis if cavity_dis > 0 else 0

        # Analytical: loop/cavity = 1 + (s_max₂/R)³ = 1 + (1 - b₂²/R²)^{3/2}
        loop_ratio_analytical = 1 + (1 - b2_frac**2)**1.5

        loop_res = {
            "b1_fraction": 0.0,
            "b2_fraction": b2_frac,
            "dv_conf_loop_kms": 0.0,
            "I_dis_loop_per_B_cm_inv": float(I_dis_loop),
            "dv_dis_loop_per_B_kms": float(dv_dis_loop_per_B),
            "loop_to_cavity_ratio": float(loop_ratio),
            "loop_to_cavity_ratio_analytical": float(loop_ratio_analytical),
        }
        loop_results.append(loop_res)

        print_status(
            f"  {b2_frac:<8.1f} {dv_conf_loop:<15.1f} {I_dis_loop:<15.2e} "
            f"{dv_dis_loop_per_B:<15.2e} {loop_ratio:<18.4f}",
            "PROCESS",
        )

    # =====================================================================
    # KEY RESULT: Cavity vs Loop
    # =====================================================================
    print_status(f"\n--- Key Result ---", "TITLE")

    b2_ref = 0.5
    ref_loop = next(l for l in loop_results if abs(l["b2_fraction"] - b2_ref) < 0.01)

    print_status(f"  Conformal cavity signal (b=0): |Δv_conf| = {b1_result['dv_conf_cavity_kms']:.5f} km/s", "PROCESS")
    print_status(f"    (clock shift — endpoint difference, spectroscopic observable)", "PROCESS")
    print_status(f"  Conformal loop signal: 0 (exact differential — cancels on any closed loop)", "PROCESS")
    print_status(f"  Disformal cavity signal (b=0, per B_eff=1 cm): |Δv_dis| = {b1_result['dv_dis_per_B_kms']:.2e} km/s", "PROCESS")
    print_status(f"    (photon transport — path integral, time-transfer observable)", "PROCESS")
    print_status(f"  Disformal loop signal (b₁=0, b₂={b2_ref}, per B_eff=1 cm): |Δv_dis| = {ref_loop['dv_dis_loop_per_B_kms']:.2e} km/s", "PROCESS")
    print_status(f"  Loop/cavity ratio: {ref_loop['loop_to_cavity_ratio']:.4f} (analytical: {ref_loop['loop_to_cavity_ratio_analytical']:.4f})", "PROCESS")
    print_status(f"", "PROCESS")
    print_status(f"  The conformal clock shift is a cavity-only signal.", "SUCCESS")
    print_status(f"  It vanishes on any closed loop (exact differential).", "SUCCESS")
    print_status(f"  The disformal transport accumulates around the loop:", "SUCCESS")
    print_status(f"  both legs contribute positively ((∂_ℓ φ)² is always positive),", "PROCESS")
    print_status(f"  so the loop signal is {ref_loop['loop_to_cavity_ratio']:.1%} of the", "PROCESS")
    print_status(f"  single-leg cavity signal for b₂/R = {b2_ref}.", "PROCESS")
    print_status(f"", "PROCESS")
    print_status(f"  The loop ISOLATES the disformal transport by canceling", "SUCCESS")
    print_status(f"  the conformal clock shift. The conformal part is removed", "SUCCESS")
    print_status(f"  cleanly; the disformal part is the accumulated transport", "PROCESS")
    print_status(f"  from both legs.", "PROCESS")
    print_status(f"", "PROCESS")
    print_status(f"  Gate 4B-0 assessment:", "TITLE")
    print_status(f"  The differential edge-core observable (conformal clock shift)", "PROCESS")
    print_status(f"  is a cavity-only signal that does not survive loop closure.", "PROCESS")
    print_status(f"  The disformal transport integral accumulates on a closed loop", "PROCESS")
    print_status(f"  and is the only nonzero residue. Its magnitude depends on", "PROCESS")
    print_status(f"  B_eff (with units of cm) and the impact parameters of both legs.", "PROCESS")
    print_status(f"  For a static field, the disformal sector does not affect g̃₀₀", "PROCESS")
    print_status(f"  (clock rates) — it affects photon propagation (spatial metric).", "PROCESS")
    print_status(f"  The two observables are physically distinct: the conformal", "PROCESS")
    print_status(f"  part is a spectroscopic velocity shift; the disformal part", "PROCESS")
    print_status(f"  is an optical time-transfer phase delay.", "PROCESS")

    # =====================================================================
    # PROFILE DATA: ln A(s) and C_{T,∥}(s) along sightlines
    # =====================================================================
    profiles = {}
    for b_frac in [0.0, 0.5]:
        b = b_frac * R
        s_max = np.sqrt(R**2 - b**2) if b < R else 0
        s_arr = np.linspace(-s_max, s_max, 200)
        r_arr = np.sqrt(b**2 + s_arr**2)
        Phi_arr = (2 * np.pi * G * rho / (3 * c**2)) * (3 * R**2 - r_arr**2)
        dlnA_arr = -beta_A**2 * 2 * Phi_arr
        C_dis_arr = beta_A**2 * (4 * np.pi * G * rho / (3 * c**2))**2 * s_arr**2  # per B_eff

        profiles[f"b_{b_frac:.1f}"] = {
            "s_fraction": (s_arr / R).tolist(),
            "r_fraction": (r_arr / R).tolist(),
            "dlnA": dlnA_arr.tolist(),
            "C_dis_per_B": C_dis_arr.tolist(),
        }

    # =====================================================================
    # BUILD LEDGER
    # =====================================================================
    ledger = {
        "gate": "4B-0",
        "title": "Cavity-vs-Loop Profile",
        "description": (
            "Compares scalar-field transport along open cavities (single sightlines) "
            "versus closed loops (paired sightlines). The conformal clock shift is an "
            "exact differential and vanishes on any closed loop. The disformal transport "
            "is a squared derivative (always positive) and accumulates on a closed loop: "
            "both legs contribute positively. The loop isolates the disformal transport "
            "by canceling the conformal clock shift."
        ),
        "observable_separation": {
            "conformal": {
                "type": "clock shift (g̃₀₀, endpoint difference)",
                "observable": "spectroscopic velocity offset",
                "units": "km/s",
                "cavity": "nonzero (edge minus core)",
                "loop": "zero (exact differential)",
            },
            "disformal": {
                "type": "photon transport (spatial metric, path integral)",
                "observable": "optical time-transfer phase delay",
                "units": "cm⁻¹ per B_eff (B_eff in cm); c × B_eff × I_dis in cm/s",
                "cavity": "nonzero (path integral)",
                "loop": "accumulates (sum of both legs, always positive)",
                "static_field_note": "For ∂₀φ = 0, disformal term B(φ)(∂₀φ)² = 0 in g̃₀₀; "
                                     "disformal affects spatial metric only, not clock rates.",
            },
        },
        "absorber_params": {
            "R_kpc": R_kpc,
            "log_N_H": float(log_N_H),
            "rho_cgs": float(rho),
            "Phi_0_c2": float(Phi_0_c2),
            "Phi_R_c2": float(Phi_R_c2),
            "S_abs": float(S_abs),
            "S_gal": float(S_gal),
            "dv_conf_kms": float(dv_conf_kms),
            "A_env_target": float(A_env_target),
        },
        "cavity_results": cavity_results,
        "loop_results": loop_results,
        "key_result": {
            "conformal_cavity_signal_kms": float(b1_result["dv_conf_cavity_kms"]),
            "conformal_loop_signal_kms": 0.0,
            "conformal_survives_loop": False,
            "disformal_cavity_per_B_kms": float(b1_result["dv_dis_per_B_kms"]),
            "disformal_loop_per_B_kms_ref": float(ref_loop["dv_dis_loop_per_B_kms"]),
            "disformal_loop_to_cavity_ratio_ref": float(ref_loop["loop_to_cavity_ratio"]),
            "ref_b2_fraction": b2_ref,
            "assessment": (
                "The conformal clock shift is a cavity-only signal that vanishes on any "
                "closed loop (exact differential). The disformal transport integral "
                "accumulates on a closed loop — both legs contribute positively because "
                "(∂_ℓ φ)² is always positive regardless of traversal direction. The loop "
                "isolates the disformal transport by canceling the conformal part. For a "
                "static field, the disformal sector does not affect clock rates (g̃₀₀); "
                "it affects photon propagation through the spatial metric. The two "
                "observables are physically distinct: conformal is a spectroscopic "
                "velocity shift, disformal is an optical time-transfer phase delay. "
                "Gate 4B-0: the edge-core differential does not survive loop closure in "
                "the conformal sector; the disformal transport is the only nonzero loop "
                "residue, and it accumulates (sum), not partially cancels (difference)."
            ),
        },
        "profiles": profiles,
    }

    out_dir = project_root / "results"
    out_dir.mkdir(parents=True, exist_ok=True)
    with open(out_dir / "gate4b0_cavity_loop_profile.json", "w") as f:
        json.dump(ledger, f, indent=2)
    print_status(
        f"\n[COMPLETED] Gate 4B-0 results written to {out_dir / 'gate4b0_cavity_loop_profile.json'}",
        "SUCCESS",
    )


if __name__ == "__main__":
    run_cavity_loop_profile()
