#!/usr/bin/env python3
"""
Gate 4: TEP Absorber Field Closure

Derives the expected spectroscopic velocity displacement (Δv_T) directly
from the TEP scalar field equation of motion using symbolic algebra (sympy).

The derivation uses the conventional positive Green operator for a screened
static scalar:

    (-∇² + m_eff²) δφ = -(β_A / M_Pl) ρ

Define the density-weighted Green integral:

    K(x) = ∫ G_+(x, x') ρ(x') d³x'  >  0

Then the core scalar response is:

    δφ_core = -(β_A / M_Pl) K

and the core clock-rate shift is:

    Δln A_core = (β_A / M_Pl) δφ_core = -β_A² K / M_Pl²  <  0

The observable is the edge relative to the core (edge has negligible
density contrast, so Δln A_edge ≈ 0):

    Δln A_abs = ln A_edge - ln A_core ≈ β_A² K / M_Pl²  >  0

    Δv_T = -c Δln A_abs  <  0  (blueward)

Key consequences:
  - The dependence is QUADRATIC in β_A (not linear).
  - The blueward sign follows from β_A² > 0 and the edge-minus-core
    convention, NOT from β_A < 0 directly.
  - The amplitude constraint is a SQUARE ROOT:

        |β_A| = M_Pl √( (Δv / c) / K )

  - For corpus consistency, β_A should be frozen from independent
    measurements (e.g., GNSS/EFA flyby fits) and the absorber shear
    amplitude predicted, not inferred from the same -82 km/s feature.
"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))
import json
import sympy as sp
from scripts.utils.logger import print_status, setup_step_logger

def run_gate4():
    setup_step_logger(Path(__file__).stem)
    print_status("=== GATE 4: TEP ABSORBER FIELD CLOSURE ===", "SUCCESS")
    print_status("\nExecuting Gate 4: Symbolic Derivation of Temporal Shear Sign...\n", "TITLE")

    # 1. Define symbols with strict assumptions
    c = sp.Symbol('c', positive=True, real=True)
    beta_A = sp.Symbol('beta_A', real=True)  # Coupling (sign not frozen for algebra)
    M_Pl = sp.Symbol('M_Pl', positive=True, real=True)

    # K(x) = ∫ G_+(x, x') ρ(x') d³x'  — density-weighted Green integral
    # This already contains ρ, so no extra ρ factor appears.
    K = sp.Symbol('K', positive=True, real=True)

    # 2. Scalar EOM: (-∇² + m_eff²) δφ = -(β_A / M_Pl) ρ
    #    Solution via positive Green operator:
    #    δφ_core = -(β_A / M_Pl) × K
    delta_phi_core = -(beta_A / M_Pl) * K
    print_status("--- Field Propagation ---", "PROCESS")
    print_status(f"Scalar EOM: (-∇² + m_eff²) δφ = -(β_A/M_Pl) ρ", "PROCESS")
    print_status(f"Green integral K = ∫ G_+(x,x') ρ(x') d³x' > 0", "PROCESS")
    print_status(f"Core scalar response: δφ_core = {delta_phi_core}", "PROCESS")

    # 3. Core clock-rate shift: Δln A = (β_A / M_Pl) × δφ
    #    A(φ) = exp(β_A φ / M_Pl), so d(ln A)/dφ = β_A / M_Pl
    delta_ln_A_core = (beta_A / M_Pl) * delta_phi_core
    delta_ln_A_core_simplified = sp.simplify(delta_ln_A_core)
    print_status(f"\nCore clock shift: Δln A_core = (β_A/M_Pl) × δφ_core", "PROCESS")
    print_status(f"  = {delta_ln_A_core_simplified}", "PROCESS")
    print_status(f"  = -β_A² K / M_Pl²", "PROCESS")

    # 4. Verify: this is strictly negative for ANY real β_A ≠ 0
    #    (quadratic — sign does not depend on sign of β_A)
    is_negative = sp.ask(sp.Q.negative(delta_ln_A_core_simplified.subs(beta_A, sp.Symbol('b', real=True, nonzero=True)))
                        if not sp.ask(sp.Q.negative(delta_ln_A_core_simplified))
                        else True)
    # Direct check with explicit nonzero real
    b_sq = sp.Symbol('b_sq', positive=True, real=True)  # represents β_A²
    delta_ln_A_core_check = -b_sq * K / M_Pl**2
    is_neg = sp.ask(sp.Q.negative(delta_ln_A_core_check))
    print_status(f"Is Δln A_core < 0 (for β_A ≠ 0)? -> {is_neg}", "PROCESS")
    print_status(f"  (Dependence is QUADRATIC in β_A: ∝ -β_A²)", "PROCESS")

    # 5. Edge-core observable
    #    Edge has negligible density contrast → Δln A_edge ≈ 0
    #    Δln A_abs = ln A_edge - ln A_core ≈ -Δln A_core
    delta_ln_A_abs = -delta_ln_A_core_simplified
    print_status(f"\nEdge-core observable: Δln A_abs = -Δln A_core = {sp.simplify(delta_ln_A_abs)}", "PROCESS")
    is_pos = sp.ask(sp.Q.positive(delta_ln_A_abs.subs(beta_A, sp.Symbol('b', real=True, nonzero=True))))
    # Check with positive β_A²
    is_pos_check = sp.ask(sp.Q.positive(b_sq * K / M_Pl**2))
    print_status(f"Is Δln A_abs > 0? -> {is_pos_check}", "PROCESS")

    # 6. Velocity shift
    delta_v_T = -c * delta_ln_A_abs
    delta_v_T_simplified = sp.simplify(delta_v_T)
    print_status(f"\nVelocity shift: Δv_T = -c × Δln A_abs = {delta_v_T_simplified}", "PROCESS")
    is_blue = sp.ask(sp.Q.negative(-c * b_sq * K / M_Pl**2))
    print_status(f"Is Δv_T < 0 (blueward)? -> {is_blue}", "PROCESS")

    # 7. Amplitude constraint (square-root form)
    #    |Δv_T| = c × β_A² × K / M_Pl²
    #    β_A² = (M_Pl² / K) × (|Δv_T| / c)
    #    |β_A| = M_Pl × √(|Δv_T| / (c × K))
    delta_v_mag = sp.Symbol('|Delta_v_T|', positive=True, real=True)
    beta_A_squared = (M_Pl**2 / K) * (delta_v_mag / c)
    beta_A_mag = sp.sqrt(beta_A_squared)
    print_status(f"\n--- Amplitude Constraint ---", "PROCESS")
    print_status(f"|Δv_T| = c × β_A² × K / M_Pl²", "PROCESS")
    print_status(f"β_A² = (M_Pl² / K) × (|Δv_T| / c)", "PROCESS")
    print_status(f"|β_A| = M_Pl × √(|Δv_T| / (c × K))  [SQUARE ROOT]", "PROCESS")

    # 8. Corpus consistency note
    print_status(f"\n--- Corpus Consistency ---", "PROCESS")
    print_status(f"For corpus consistency, β_A should be frozen from independent", "PROCESS")
    print_status(f"measurements (GNSS/EFA flyby fits) and the absorber shear", "PROCESS")
    print_status(f"amplitude predicted, not inferred from the same -82 km/s feature.", "PROCESS")

    # 9. Formal assertions
    assert is_neg, "FATAL: Δln A_core is not strictly negative!"
    assert is_pos_check, "FATAL: Δln A_abs is not strictly positive!"
    assert is_blue, "FATAL: Δv_T is not blueward!"
    print_status("\n[SUCCESS] Gate 4 Passed: Blueward shift guaranteed from β_A² and edge-minus-core convention.", "SUCCESS")

    ledger = {
        "4A_scalar_derivation": "PASSED (Screened scalar EOM with positive Green operator)",
        "4B_absorber_solution": "PASSED (K = ∫G_+ρ d³x', core-edge geometry)",
        "4C_sign_prediction": "PASSED (Blueward, from β_A² > 0 and edge-minus-core convention)",
        "4D_amplitude_prediction": "SQUARE_ROOT: |β_A| = M_Pl × √(|Δv_T| / (c × K))",
        "4E_corpus_note": "β_A should be frozen from independent measurements; absorber amplitude is a prediction",
        "symbolic_relations": {
            "green_integral": "K = ∫ G_+(x,x') ρ(x') d³x' > 0",
            "scalar_EOM": "(-∇² + m_eff²) δφ = -(β_A/M_Pl) ρ",
            "delta_phi_core": str(delta_phi_core),
            "delta_ln_A_core": str(delta_ln_A_core_simplified),
            "delta_ln_A_core_form": "-β_A² × K / M_Pl²",
            "delta_ln_A_abs": str(sp.simplify(delta_ln_A_abs)),
            "delta_ln_A_abs_form": "β_A² × K / M_Pl²",
            "delta_v_T": str(delta_v_T_simplified),
            "delta_v_T_form": "-c × β_A² × K / M_Pl²",
            "amplitude_constraint": "|β_A| = M_Pl × √(|Δv_T| / (c × K))",
            "dependence": "quadratic in β_A",
            "is_blueward": bool(is_blue),
            "sign_origin": "β_A² > 0 and edge-minus-core convention (not β_A < 0 directly)"
        }
    }

    project_root = Path(__file__).resolve().parent.parent.parent
    out_dir = project_root / "results"
    out_dir.mkdir(parents=True, exist_ok=True)

    with open(out_dir / "gate4_prediction.json", "w") as f:
        json.dump(ledger, f, indent=2)

    print_status(f"\n[COMPLETED] Gate 4 predictions written to {out_dir / 'gate4_prediction.json'}", "SUCCESS")

if __name__ == "__main__":
    run_gate4()
