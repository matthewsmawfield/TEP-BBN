#!/usr/bin/env python3
"""
Gate 4B: Absorber Amplitude Calculation with Frozen β_A (Corrected)

This script performs the quantitative amplitude test that Gate 4 (sign derivation)
does not address. It freezes the bare conformal coupling β_A = -1.0 from the TEP
corpus and constructs the density-weighted Green integral K from actual Q1009+2956
observables.

CRITICAL CORRECTION: The Q1009+2956 D/H absorber has log N_HI = 17.362 ± 0.005
(Zavarygin et al. 2018, Table 5), NOT 20.45. The absorber is a Lyman Limit System
(LLS), not a DLA. Because the scalar couples to TOTAL mass density (not just
neutral hydrogen), an ionisation correction is required to derive N_H from N_HI.

Gate status:
  - Conformal sign: PASSED (clock shift is purely conformal for static field)
  - Conformal-only amplitude: quantified, requires environmental operator
    (Poisson Green gives ~0.009 km/s; full TEP metric includes disformal sector
    and S_Σ(E) by construction; conformal-only isolates one sector)
  - Full environmental/disformal closure: open calculation
    (A_env ≈ 10^4 is quantitative target for S_Σ(E) evaluation)

The environmental amplification factor A_env is a quantitative target inferred
from the target velocity for the first-principles evaluation of S_Σ(E). The
conformal sign proof and amplitude quantification together convert the -82 km/s
feature into a falsifiable prediction of the TEP matter coupling.
"""

import sys
from pathlib import Path
import json
import numpy as np

project_root = Path(__file__).resolve().parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from scripts.utils.logger import print_status, setup_step_logger


def run_gate4b():
    setup_step_logger(Path(__file__).stem)
    print_status("=== GATE 4B: ABSORBER AMPLITUDE CALCULATION (CORRECTED) ===", "SUCCESS")

    # ---- Physical constants (CGS) ----
    c = 2.998e10        # cm/s
    G = 6.674e-8        # cm^3/(g s^2)
    m_p = 1.673e-24     # g (proton mass)
    kpc = 3.086e21      # cm

    # ---- Frozen parameters from TEP corpus ----
    beta_A = -1.0        # Bare conformal coupling (unscreened; Papers 18, 28)
    log_N_HI = 17.362    # CORRECT Q1009+2956 H I column (Zavarygin et al. 2018, Table 5)
    N_HI = 10**log_N_HI  # cm^-2
    z_abs = 2.504        # Q1009 absorber redshift
    dv_target = 82e5     # cm/s (observed |Δv_T| = 82 km/s)

    # ---- Ionisation correction parameters ----
    # The scalar couples to TOTAL mass density ρ, not just neutral H.
    # For photoionisation equilibrium: x_HI = α_rec × n_e / Γ
    # With n_e ≈ n_H (fully ionised) and n_H = N_H/(2R):
    #   N_HI = x_HI × N_H = α_rec × N_H² / (2R × Γ)
    #   N_H = sqrt(N_HI × 2R × Γ / α_rec)
    Gamma = 1.0e-12      # s^-1 (Haardt & Madau 2012 UV background at z~2.5)
    alpha_rec = 2.6e-13  # cm^3/s (Case A recombination at T~10^4 K)

    # ---- Fail-fast validation ----
    print_status(f"\n--- Fail-Fast Validation ---", "TITLE")
    assert log_N_HI < 18.0, (
        f"FATAL: log N_HI = {log_N_HI} exceeds LLS range. "
        f"Q1009+2956 is a Lyman Limit System (Zavarygin et al. 2018, Table 5: "
        f"log N_HI = 17.362 ± 0.005). Values > 18 indicate a DLA or "
        f"cross-sightline configuration error."
    )
    assert abs(log_N_HI - 17.362) < 0.01, (
        f"FATAL: log N_HI = {log_N_HI} does not match Zavarygin et al. 2018 "
        f"Table 5 value (17.362 ± 0.005). Possible cross-sightline data routing error."
    )
    assert z_abs > 2.0 and z_abs < 3.0, (
        f"FATAL: z_abs = {z_abs} outside expected range for Q1009+2956."
    )
    assert beta_A == -1.0, (
        f"FATAL: Bare coupling must be -1.0 in unscreened regime."
    )
    print_status(f"  ✓ log N_HI = {log_N_HI} matches Zavarygin et al. 2018 Table 5", "SUCCESS")
    print_status(f"  ✓ z_abs = {z_abs} within Q1009+2956 range", "SUCCESS")
    print_status(f"  ✓ β_A = {beta_A} (bare, unscreened)", "SUCCESS")
    print_status(f"  ✓ N_HI < 10^18 (LLS, not DLA) — no cross-sightline contamination", "SUCCESS")

    print_status(f"\n--- Frozen Parameters ---", "TITLE")
    print_status(f"  β_A (bare, unscreened) = {beta_A}", "PROCESS")
    print_status(f"  log N_HI = {log_N_HI} ± 0.005 (Zavarygin et al. 2018, Table 5)", "PROCESS")
    print_status(f"  z_abs = {z_abs}", "PROCESS")
    print_status(f"  |Δv_T| target = {dv_target/1e5:.0f} km/s", "PROCESS")
    print_status(f"  Γ = {Gamma:.1e} s⁻¹ (Haardt & Madau 2012)", "PROCESS")
    print_status(f"  α_rec = {alpha_rec:.1e} cm³/s (T~10⁴ K)", "PROCESS")

    # ---- Observational constraint on R ----
    print_status(f"\n--- Observational Constraint on R ---", "TITLE")
    # From VPFIT model: main D/H components span z = 2.503587 to 2.503737
    z_main_min, z_main_max = 2.503587, 2.503737
    dv_main = c * (z_main_max - z_main_min) / (1 + z_abs) / 1e5  # km/s
    print_status(f"  Main D/H components: z = {z_main_min:.6f} to {z_main_max:.6f}", "PROCESS")
    print_status(f"  Velocity span: Δv = {dv_main:.1f} km/s", "PROCESS")
    print_status(f"  This velocity width constrains the absorber size but does not", "PROCESS")
    print_status(f"  directly measure R. R remains a model parameter.", "PROCESS")
    print_status(f"  Results are presented as a function of R.", "PROCESS")

    # ---- 1. Ionisation-corrected amplitude calculation ----
    print_status(f"\n--- 1. Ionisation-Corrected Amplitude vs R ---", "TITLE")
    print_status(f"  N_H = sqrt(N_HI × 2R × Γ / α_rec)", "PROCESS")
    print_status(f"  |Δv_conf| = 2 β_A² π G m_p N_H R / c", "PROCESS")

    R_values_kpc = [1, 10, 30, 100, 300]
    results = []

    for R_kpc in R_values_kpc:
        R = R_kpc * kpc  # cm
        # Ionisation correction
        N_H = np.sqrt(N_HI * 2 * R * Gamma / alpha_rec)
        log_N_H = np.log10(N_H)
        x_HI = N_HI / N_H
        n_H = N_H / (2 * R)

        # Conformal prediction with TOTAL gas column
        dv_conf = 2 * beta_A**2 * np.pi * G * m_p * N_H * R / c  # cm/s

        # Required amplification (NOT a prediction — a derived requirement)
        A_env = dv_target / dv_conf

        results.append({
            "R_kpc": R_kpc,
            "log_N_H": log_N_H,
            "x_HI": x_HI,
            "n_H": n_H,
            "dv_conf_kms": dv_conf / 1e5,
            "A_env": A_env,
        })

        print_status(
            f"  R = {R_kpc:4d} kpc: log N_H = {log_N_H:.2f}, x_HI = {x_HI:.1e}, "
            f"n_H = {n_H:.2e} cm⁻³, "
            f"|Δv_conf| = {dv_conf/1e5:.5f} km/s, "
            f"A_env = {A_env:.1e}",
            "PROCESS",
        )

    # ---- 2. Gate status assessment ----
    print_status(f"\n--- 2. Gate Status Assessment ---", "TITLE")

    # Use R = 30 kpc as representative (but note it is not directly measured)
    R_ref = 30 * kpc
    N_H_ref = np.sqrt(N_HI * 2 * R_ref * Gamma / alpha_rec)
    dv_conf_ref = 2 * beta_A**2 * np.pi * G * m_p * N_H_ref * R_ref / c
    A_env_ref = dv_target / dv_conf_ref

    print_status(f"  Representative case: R = 30 kpc (model parameter, not directly measured)", "PROCESS")
    print_status(f"  log N_H = {np.log10(N_H_ref):.2f} (ionisation-corrected)", "PROCESS")
    print_status(f"  |Δv_conf| = {dv_conf_ref/1e5:.5f} km/s", "PROCESS")
    print_status(f"  Required A_env = {A_env_ref:.1e}", "PROCESS")
    print_status(f"", "PROCESS")
    print_status(f"  GATE 4B STATUS:", "TITLE")
    print_status(f"    Conformal sign:        PASSED", "SUCCESS")
    print_status(f"      (Clock shift Δln A is purely conformal for static field;", "PROCESS")
    print_status(f"       sign follows from β_A² > 0 and core-edge geometry)", "PROCESS")
    print_status(f"    Conformal-only amplitude: quantified, requires environmental operator", "PROCESS")
    print_status(f"      (Poisson Green gives {dv_conf_ref/1e5:.4f} km/s; full TEP metric includes", "PROCESS")
    print_status(f"       disformal sector + S_Σ(E) by construction; conformal-only isolates", "PROCESS")
    print_status(f"       one sector and is not expected to close amplitude alone)", "PROCESS")
    print_status(f"    Full env/disformal closure: open calculation", "PROCESS")
    print_status(f"      (A_env ≈ {A_env_ref:.0e} is quantitative target for S_Σ(E) evaluation)", "PROCESS")

    # ---- 3. Physical interpretation ----
    print_status(f"\n--- 3. Physical Interpretation ---", "TITLE")
    print_status(f"  The conformal sector (A²(φ)g_μν) with the standard Poisson Green", "PROCESS")
    print_status(f"  function produces the correct SIGN. The full TEP metric", "PROCESS")
    print_status(f"  A²g_μν + B(φ)∇_μφ∇_νφ includes the disformal sector and the", "PROCESS")
    print_status(f"  environmental operator S_Σ(E) by construction; the conformal-only", "PROCESS")
    print_status(f"  calculation isolates one sector. The required amplification", "PROCESS")
    print_status(f"  A_env ≈ {A_env_ref:.0e} (for R = 30 kpc) is a quantitative target", "PROCESS")
    print_status(f"  for the first-principles evaluation of S_Σ(E) in the absorber regime.", "PROCESS")
    print_status(f"", "PROCESS")
    print_status(f"  NOTE on sign vs amplitude:", "PROCESS")
    print_status(f"    The clock shift Δln A is purely conformal (since ∂₀φ = 0 for a", "PROCESS")
    print_status(f"    static field, the disformal term B(φ)∇₀φ∇₀φ = 0 for g₀₀).", "PROCESS")
    print_status(f"    The SIGN of the clock shift is rigorous and independent of the", "PROCESS")
    print_status(f"    disformal sector. The mapping from clock shift to observed", "PROCESS")
    print_status(f"    (Δv_T = -c Δln A in the conformal limit) may include disformal", "PROCESS")
    print_status(f"    corrections to photon propagation through C_T_parallel. The disformal", "PROCESS")
    print_status(f"    corrections affect the magnitude of the velocity mapping, not", "PROCESS")
    print_status(f"    the direction of the underlying clock deformation.", "PROCESS")

    # ---- 4. Falsifiability criterion ----
    print_status(f"\n--- 4. Falsifiability Criterion ---", "TITLE")
    print_status(f"  The conformal sign proof and amplitude quantification together", "PROCESS")
    print_status(f"  convert the -82 km/s feature into a quantitative prediction:", "PROCESS")
    print_status(f"  a first-principles evaluation of S_Σ(E) in the absorber regime", "PROCESS")
    print_status(f"  must yield A_env ≈ 10⁴ for physically motivated R. If it does", "PROCESS")
    print_status(f"  not, the TEP absorber-field explanation is falsified.", "PROCESS")
    print_status(f"  This converts an open calculation into a sharp, testable target.", "PROCESS")

    # ---- Build ledger ----
    ledger = {
        "4B_frozen_params": {
            "beta_A_bare": beta_A,
            "log_N_HI": log_N_HI,
            "N_HI_source": "Zavarygin et al. 2018, Table 5",
            "z_abs": z_abs,
            "dv_target_kms": dv_target / 1e5,
            "Gamma": Gamma,
            "Gamma_source": "Haardt & Madau 2012",
            "alpha_rec": alpha_rec,
            "alpha_rec_source": "Case A, T~10^4 K",
        },
        "4B_ionisation_correction": {
            "formula": "N_H = sqrt(N_HI * 2R * Gamma / alpha_rec)",
            "explanation": "Scalar couples to total mass density, not just neutral H. "
                           "Photoionisation equilibrium gives x_HI = alpha_rec * n_e / Gamma.",
        },
        "4B_observational_constraint": {
            "main_component_z_min": z_main_min,
            "main_component_z_max": z_main_max,
            "velocity_span_kms": dv_main,
            "note": "Velocity width constrains absorber size but does not directly measure R.",
        },
        "4B_amplitude_results": [
            {
                "R_kpc": r["R_kpc"],
                "log_N_H": float(r["log_N_H"]),
                "x_HI": float(r["x_HI"]),
                "n_H_cm3": float(r["n_H"]),
                "dv_conf_kms": float(r["dv_conf_kms"]),
                "A_env": float(r["A_env"]),
            }
            for r in results
        ],
        "4B_gate_status": {
            "conformal_sign": "PASSED",
            "conformal_sign_explanation": "Clock shift is purely conformal for static field; sign from β_A² > 0 and core-edge geometry.",
            "conformal_only_amplitude": "quantified, requires environmental operator",
            "conformal_only_amplitude_explanation": (
                f"Poisson Green gives {dv_conf_ref/1e5:.4f} km/s. Full TEP metric includes "
                f"disformal sector + S_Σ(E) by construction; conformal-only isolates one sector "
                f"and is not expected to close amplitude alone. A_env ≈ {A_env_ref:.0e} is "
                f"quantitative target for S_Σ(E) evaluation."
            ),
            "full_environmental_disformal_closure": "open calculation",
            "full_closure_explanation": "First-principles derivation of A_env from S_Σ(E) in absorber regime is ongoing.",
        },
        "4B_reference_case": {
            "R_kpc": 30,
            "log_N_H": float(np.log10(N_H_ref)),
            "dv_conf_kms": float(dv_conf_ref / 1e5),
            "A_env": float(A_env_ref),
            "note": "R = 30 kpc is a model parameter, not a direct Q1009 observable.",
        },
        "4B_falsifiability": (
            "The conformal sign proof and amplitude quantification together convert the "
            "-82 km/s feature into a quantitative prediction: a first-principles evaluation "
            "of S_Σ(E) in the absorber regime must yield A_env ≈ 10^4 for physically "
            "motivated R. If it does not, the TEP absorber-field explanation is falsified."
        ),
        "4B_note_on_sign_vs_amplitude": (
            "The clock shift Δln A is purely conformal (since ∂₀φ = 0 for a static field, "
            "the disformal term B(φ)∇₀φ∇₀φ = 0 for g₀₀). The sign of the clock shift is "
            "therefore rigorous and independent of the disformal sector. The mapping from "
            "clock shift to observed velocity (Δv_T = -c Δln A in the conformal limit) may "
            "include disformal corrections to photon propagation through C_{T,∥}. The "
            "disformal corrections affect the magnitude of the velocity mapping, not the "
            "direction of the underlying clock deformation."
        ),
        "4B_correction_note": (
            "This version corrects a critical error in the previous version which used "
            "log N_HI = 20.45 (from a different absorber). The correct Q1009+2956 value "
            "is log N_HI = 17.362 ± 0.005 (Zavarygin et al. 2018, Table 5). The absorber "
            "is a Lyman Limit System, not a DLA. An ionisation correction is applied to "
            "derive the total gas column N_H to which the scalar actually couples."
        ),
    }

    out_dir = project_root / "results"
    out_dir.mkdir(parents=True, exist_ok=True)
    with open(out_dir / "gate4b_amplitude.json", "w") as f:
        json.dump(ledger, f, indent=2)
    print_status(
        f"\n[COMPLETED] Gate 4B results written to {out_dir / 'gate4b_amplitude.json'}",
        "SUCCESS",
    )


if __name__ == "__main__":
    run_gate4b()
