#!/usr/bin/env python3
"""Step 21: acceleration-proxy screening table and legacy comparisons.

The selected kinetic sector and distinct amplitude/gradient responses are
already derived in Paper 0, with nonlinear profiles in steps 53/58 and
embedded solves in steps 56/59/75. This script evaluates inverse stiffness
on assigned accelerations, using xi_proxy=(g/g_t)^2. That is not the action
invariant xi=|X|/Lambda_X^4 of a solved source field.

Its step-54 table reproduction verifies a shared proxy convention. The
legacy solar gamma columns retain their numerical values for comparison;
they are not verified Cassini bounds. Absorber potential-depth transfer
remains a declared prescription. Source profiles and observational transfer
must be matched before proxy values are promoted to physical predictions.

Output: results/step_21_canonical_projection.json
"""

import sys
import json
from pathlib import Path

import numpy as np

project_root = Path(__file__).resolve().parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from scripts.utils.logger import print_status, setup_step_logger
from scripts.lib.canonical_screening import (
    G_T, K_STAR, A0, S_Sigma_canonical, dphi_dr_sun_eV2_canonical,
)

# ============================================================================
# Canonical constants (TEP step_54_master_sector_admissibility.json)
# ============================================================================
C_SI = 2.99792458e8          # m/s
G_SI = 6.674e-11           # m^3 kg^-1 s^-2
BETA_A = -1.0

# Solar/absorber parameters
M_SUN = 1.989e30           # kg
R_SUN = 6.96e8             # m
AU = 1.496e11              # m
KPC = 3.086e19             # m
U_SUN_SURF = 2.12e-6       # |Phi|/c^2 at solar surface
M_PL_EV = 1.2209e28 / np.sqrt(8.0 * np.pi)  # reduced Planck mass, eV
HBAR_C_EV_M = 1.9733e-7    # eV*m

# Absorber benchmark (paper's adopted halo model)
M_HALO = 1.0e10 * M_SUN
R_HALO = 30.0 * KPC

# Cassini / PPN
GAMMA_PPN_BOUND = 2.3e-5
S_SIGMA_CASSINI_CEILING = 5.8e-6

# Paper 29 ansatz parameters (absorber-amplitude transfer prescription)
PHI_HALF = 1.59e-7
N_SCREEN = 3.56

# Step_27 amplitude-sector law
RHO_T_GCC = 20.0           # g/cm^3

# Per-sightline conformal baselines (gas-column Poisson, R = 30 kpc;
# table in manuscript section 3.3 / gate4b results)
DV_CONF_POISSON_KMS = {
    "Q1009+2956":   0.009,
    "PKS1937-101":  0.017,
    "J1332+0052":   0.077,
}


def S_Sigma_g(g_si, branch="two_branch"):
    """Derived source-charge/inverse-stiffness projection at ambient g."""
    return S_Sigma_canonical(g_si, branch)


def S_A_ansatz(phi_c2):
    """Paper-29 absorber amplitude prescription (potential-depth form)."""
    return 1.0 / (1.0 + (phi_c2 / PHI_HALF) ** N_SCREEN)


def main():
    setup_step_logger(Path(__file__).stem)
    print_status("=== STEP 21: CANONICAL SCREENING-PROJECTION AUDIT ===", "SUCCESS")
    print_status("Canonical operator: S_Sigma = 1/P_X, P_X = k*sqrt(xi) + 2*xi,", "PROCESS")
    print_status(f"  xi=(g/g_t)^2, k={K_STAR:.4f}, g_t={G_T:.6e} m/s^2 (Paper 0 v0.15 sec.7 / step_54)", "PROCESS")

    out = {
        "step": "21",
        "purpose": "Tabulate the selected-sector acceleration proxy and retain "
                   "legacy diagnostics, distinguishing them from existing solved profiles.",
        "operator": {
            "form": "S_Sigma(g) = 1/[k*(g/g_t) + 2*(g/g_t)^2]",
            "kinetic_argument_convention": "xi_proxy=(g/g_t)^2 reproduces the step-54 environment benchmark; xi_action=|X|/Lambda_X^4 on a solved field is distinct",
            "reduced_planck_mass_eV": float(M_PL_EV),
            "k_star": float(K_STAR),
            "g_t_ms2": float(G_T),
            "provenance": "Paper 0 v0.15 sec.7; TEP step_54 master-sector "
                          "admissibility (two-branch selected, unit-term rejected)",
            "baseline_form": "S_Sigma_baseline(g) = 1/[1 + 2*(g/g_t)^2]",
        },
    }

    # ------------------------------------------------------------------
    # 0. Cross-check against the corpus tabulation (step_54 environment rows)
    # ------------------------------------------------------------------
    print_status("\n--- 0. Cross-check vs TEP step_54 tabulation ---", "TITLE")
    corpus_checks = [
        ("Sun 1 AU",            5.93e-3,  1.6438717051381377e-15),
        ("Cassini limb 1.6 Rs", 107.0,    5.0490532523857e-24),
        ("MW solar circle",     2e-10,    0.09881371372504827),
        ("Void/cosmic web",     1e-12,    21.205421714450488),
    ]
    checks = []
    max_rel = 0.0
    for name, g, ref in corpus_checks:
        val = S_Sigma_g(g)
        rel = abs(val - ref) / ref
        max_rel = max(max_rel, rel)
        checks.append({"name": name, "g": g, "S_Sigma": float(val),
                       "step54_ref": ref, "rel_err": float(rel)})
        print_status(f"  {name:<22} g={g:.2e}  S_Sigma={val:.4e}  "
                     f"(step54: {ref:.4e}, rel err {rel:.1e})", "PROCESS")
    assert max_rel < 1e-9, "canonical operator reproduction failed"
    print_status("  operator reproduces step_54 tabulation to <1e-9", "SUCCESS")
    out["corpus_crosscheck"] = {"rows": checks, "max_rel_err": float(max_rel)}

    # ------------------------------------------------------------------
    # 1. Solar-system projection (the Cassini side of the relation)
    # ------------------------------------------------------------------
    print_status("\n--- 1. Solar-system projection ---", "TITLE")
    g_surf = G_SI * M_SUN / R_SUN**2                       # 274 m/s^2
    solar_rows = {
        "Sun surface": g_surf,
        "Sun field at 1 AU": G_SI * M_SUN / AU**2,
        "Cassini conjunction 1.6 Rsun": G_SI * M_SUN / (1.6 * R_SUN)**2,
        "Sun field at Saturn 9.5 AU": G_SI * M_SUN / (9.5 * AU)**2,
    }
    solar = {}
    for name, g in solar_rows.items():
        s = S_Sigma_g(g)
        s_base = S_Sigma_g(g, "baseline")
        solar[name] = {"g_ms2": float(g), "S_Sigma_two_branch": float(s),
                       "S_Sigma_baseline": float(s_base)}
        print_status(f"  {name:<28} g={g:.3e}  S_Sigma={s:.3e} (baseline {s_base:.3e})",
                     "PROCESS")
    s_1au = solar["Sun field at 1 AU"]["S_Sigma_two_branch"]
    gamma_ppn_canonical = abs(-4.0 * BETA_A**2 * s_1au / (1 + 2 * BETA_A**2 * s_1au))
    print_status(f"  -> gamma_PPN-1 = {gamma_ppn_canonical:.3e} vs bound "
                 f"{GAMMA_PPN_BOUND:.1e} (margin {GAMMA_PPN_BOUND/gamma_ppn_canonical:.1e}x)",
                 "SUCCESS")
    out["solar_projection"] = {
        "environments": solar,
        "S_Sigma_1AU": float(s_1au),
        "gamma_ppn_minus_1": float(gamma_ppn_canonical),
        "cassini_bound": GAMMA_PPN_BOUND,
        "cassini_margin": float(GAMMA_PPN_BOUND / gamma_ppn_canonical),
        "adopted_illustrative": 1.9e-6,
        "note": "Values are inverse-stiffness evaluations on assigned "
                "Newtonian accelerations. The gamma and margin columns are "
                "legacy proxy diagnostics, not solved-field Cassini bounds.",
        "scope": "acceleration_proxy_not_solved_source_response",
        "cassini_bound_verified": False,
    }

    # ------------------------------------------------------------------
    # 2. Absorber projection (the LLS side of the relation)
    # ------------------------------------------------------------------
    print_status("\n--- 2. Absorber projection (ambient semantics) ---", "TITLE")
    g_halo = G_SI * M_HALO / R_HALO**2                     # ~1.55e-12 m/s^2
    a_eff = A0  # deep-tail scalar acceleration scale = a_0 by construction
    g_deeptail = np.sqrt(a_eff * g_halo)                   # sqrt(a_0 g_N) ~1.36e-11
    ambient_choices = {
        "host_halo_newtonian": g_halo,
        "host_halo_deep_tail_scalar": g_deeptail,
        "cosmic_web_floor": 1.0e-12,
    }
    absorber = {}
    for name, g in ambient_choices.items():
        s = S_Sigma_g(g)
        s_base = S_Sigma_g(g, "baseline")
        absorber[name] = {"g_ms2": float(g), "S_Sigma_two_branch": float(s),
                          "S_Sigma_baseline": float(s_base)}
        print_status(f"  {name:<32} g={g:.3e}  S_Sigma={s:.3f} (baseline {s_base:.4f})",
                     "PROCESS")

    # ansatz comparison at the same potentials
    phi_halo_c2 = G_SI * M_HALO / (R_HALO * C_SI**2)       # ~8.6e-9
    s_ansatz = S_A_ansatz(phi_halo_c2)
    print_status(f"  ansatz S_A^abs(Phi_halo={phi_halo_c2:.2e}) = {s_ansatz:.5f}",
                 "PROCESS")

    fid = absorber["host_halo_newtonian"]["S_Sigma_two_branch"]
    lo = absorber["host_halo_deep_tail_scalar"]["S_Sigma_two_branch"]
    hi = absorber["cosmic_web_floor"]["S_Sigma_two_branch"]

    # Solved drift-branch evaluation: the LLS ambient rides the z~2.5-3.6
    # cosmological drift (spatial/temporal gradient ratio ~ 2.4e-4), so the
    # correct invariant is the timelike action value xi = |X|/Lambda_X^4 =
    # E^2(z)/2 on the ambient solution - not the static-branch acceleration
    # proxy above. P_X(xi) = k*sqrt(xi) + 2 xi with k = 16.03 (canonical).
    def _E2_descent(z):
        return 1.0 / (1.0 + z)
    _k = 16.03                       # canonical k = 4 sqrt2 |b_A| g_t/1.2e-10
    _c3, _c4 = np.sqrt(2.0) * _k / 3.0, 0.75
    def _E2_tracking(z):
        # fixed-point map of the selected tracking branch (see step_10c)
        u = np.log1p(z)
        e = np.exp(-u / 3.0)
        for _ in range(60):
            f = _c3 * e**3 + _c4 * e**4 - (_c3 + _c4) * np.exp(-u)
            d = 3 * _c3 * e**2 + 4 * _c4 * e**3
            e = e - f / d
        return e * e
    def _P_X(xi):
        return _k * np.sqrt(xi) + 2.0 * xi
    drift_branch = {}
    for zl, zv in [('z2.50', 2.50), ('z3.42', 3.42), ('z3.57', 3.57)]:
        for mdl, E2f in [('descent', _E2_descent), ('tracking', _E2_tracking)]:
            E2 = E2f(zv)
            px = _P_X(E2 / 2.0)
            drift_branch[f'{mdl}_{zl}'] = {
                'E2': float(E2), 'xi_drift': float(E2 / 2.0),
                'P_X': float(px), 'S_Sigma': float(1.0 / px)}

    dv_conf_canonical = {
        sid: {"poisson_kms": dv,
              "canonical_fiducial_kms": dv * fid,
              "canonical_range_kms": [dv * lo, dv * hi]}
        for sid, dv in DV_CONF_POISSON_KMS.items()
    }
    for sid, row in dv_conf_canonical.items():
        print_status(f"  {sid:<14} dv_conf: {row['poisson_kms']:.3f} -> "
                     f"{row['canonical_fiducial_kms']:.3f} km/s "
                     f"(range {row['canonical_range_kms'][0]:.3f}-"
                     f"{row['canonical_range_kms'][1]:.3f})", "PROCESS")

    out["absorber_projection"] = {
        "ambient_semantics": "X_env is the embedding-hierarchy ambient field "
                             "(host halo / cosmic web), excluding the absorber's "
                             "own co-generated response (Paper 0 sec.7 rule)",
        "ambient_choices": absorber,
        "ansatz_S_A_abs_at_halo_potential": float(s_ansatz),
        "S_Sigma_fiducial": float(fid),
        "S_Sigma_range": [float(lo), float(hi)],
        "S_Sigma_drift_branch": drift_branch,
        "dv_conf_canonical": dv_conf_canonical,
        "interpretation": (
            "Two branch conventions must be distinguished. On the "
            "static-branch acceleration proxy the LLS ambient returns "
            "S_Sigma ~ 1.5-21 (fiducial host-halo ~14). The solved field "
            "at z ~ 2.5-3.6 is instead drift-dominated (spatial/temporal "
            "gradient ratio ~ 2.4e-4): evaluated on the ambient action "
            "invariant xi = E^2(z)/2, the same operator gives P_X ~ "
            "5.5-8.0, i.e. S_Sigma ~ 0.13-0.18 — the absorber source-charge "
            "response is ~6x screened, not anti-screened. The proxy "
            "column is retained as the step-54 convention benchmark; the "
            "drift-branch value is the physical one for the LLS ambient. "
            "Either way the conformal channel stays below the spectral "
            "systematic floor (the disformal potential-depth gate carries "
            "the ~80 km/s amplitude), so no reported conclusion changes."
        ),
    }

    # ------------------------------------------------------------------
    # 3. Amplitude sector S_A (step_27 quartic-minimum law)
    # ------------------------------------------------------------------
    print_status("\n--- 3. Amplitude sector S_A ---", "TITLE")
    rho_gas = 1.673e-24 * 0.35    # g/cm^3, n_H ~ 0.35 cm^-3 at N_H~1e20.6 / 30 kpc
    s_a_absorber = min(1.0, (rho_gas / RHO_T_GCC) ** (1.0 / 3.0))
    print_status(f"  rho_gas ~ {rho_gas:.1e} g/cm^3, rho_T = {RHO_T_GCC} g/cm^3",
                 "PROCESS")
    print_status(f"  S_A(absorber) = (rho/rho_T)^(1/3) = {s_a_absorber:.2e} "
                 f"(far below saturation -> field excursion ambient-set)", "PROCESS")
    out["amplitude_sector"] = {
        "S_A_absorber": float(s_a_absorber),
        "rho_gas_gcc": float(rho_gas),
        "rho_T_gcc": RHO_T_GCC,
        "law": "S_A = min[1, (rho_bar/rho_T)^(1/3)] (step_27, quartic minimum)",
    }

    # ------------------------------------------------------------------
    # 4. Disformal constraint chain under canonical solar screening
    # ------------------------------------------------------------------
    print_status("\n--- 4. Disformal constraint chain ---", "TITLE")
    # spatial gradient at solar surface: dphi/dr = M_Pl * 2|beta| (g/c^2)
    dphi_dr_unscr = M_PL_EV * 2.0 * abs(BETA_A) * (g_surf / C_SI**2) * HBAR_C_EV_M  # eV^2
    s_surf = solar["Sun surface"]["S_Sigma_two_branch"]
    dphi_dr_canonical = dphi_dr_sun_eV2_canonical()
    dphi_dr_adopted = 156.0   # eV^2, adopted ansatz-screened profile (step_04h)
    print_status(f"  dphi_dr(surface): unscreened {dphi_dr_unscr:.3e} eV^2, "
                 f"canonical {dphi_dr_canonical:.3e} eV^2, adopted profile {dphi_dr_adopted} eV^2",
                 "PROCESS")

    disformal = {"dphi_dr_sun_unscreened_eV2": float(dphi_dr_unscr),
                 "dphi_dr_sun_canonical_eV2": float(dphi_dr_canonical),
                 "dphi_dr_sun_adopted_eV2": dphi_dr_adopted,
                 "gamma_dis": {}}
    # gamma_dis = B(phi_sun)*(dphi_dr)^2 / (2 U_sun); phi_sun/M_Pl = 2.26e-10
    phi_sun = 2.26e-10
    for tag, B0, n in [("powerlaw_n2_Q1009", 2.88e8, 2),
                       ("powerlaw_n5_Q1009", 2.49e12, 5),
                       ("descent_joint", 7.5579e10, 4)]:
        B_sun = B0 * phi_sun**n if tag != "descent_joint" else \
            B0 * (phi_sun**4 / (0.1**4 + phi_sun**4)) * np.exp(-phi_sun)
        g_adopted = B_sun * dphi_dr_adopted**2 / (2 * U_SUN_SURF)
        g_canon = B_sun * dphi_dr_canonical**2 / (2 * U_SUN_SURF)
        disformal["gamma_dis"][tag] = {
            "B0_eVinv4": B0, "n_eff": n, "B_phi_sun_eVinv4": float(B_sun),
            "gamma_dis_adopted_profile": float(g_adopted),
            "gamma_dis_canonical": float(g_canon),
            "cassini_pass_canonical": bool(abs(g_canon) < GAMMA_PPN_BOUND),
        }
        print_status(f"  {tag:<20} gamma_dis: adopted {g_adopted:.2e} -> "
                     f"canonical {g_canon:.2e} (bound {GAMMA_PPN_BOUND:.1e})",
                     "PROCESS")
    print_status("  Legacy solar columns use an acceleration-proxy gradient; "
                 "they are not a solved source-field or Cassini test.", "INFO")
    disformal["scope"] = {
        "calculation": "inverse stiffness on Newtonian acceleration proxy",
        "solved_solar_profile": False,
        "cassini_bound_verified": False,
        "field_amplitude_and_gradient_from_same_solution": False,
        "existing_solver": "TEP/scripts/steps/step_53_unified_profile.py",
        "existing_selected_result": "TEP/results/step_53_unified_profile_two_branch.json",
        "reconciliation": "notes/solar-coupling-exploration-2026-10-11/review.md",
    }
    out["disformal_solar_chain"] = disformal

    # ------------------------------------------------------------------
    # 5. Verdict
    # ------------------------------------------------------------------
    out["verdict"] = (
        "The corpus derives distinct amplitude and gradient projections and "
        "already supplies selected-sector nonlinear profiles (Paper 0 steps "
        "53/58) and embedded calculations. This step tabulates inverse "
        "stiffness on an acceleration proxy; its agreement with step 54 is a "
        "proxy-table check, not a solution of the source equation. The legacy "
        "solar gamma columns combine that proxy with an assigned field value "
        "and do not certify Cassini compliance. The potential-depth absorber "
        "law remains a declared transfer prescription, not automatically the "
        "response of a solved absorber. Consistent-profile exploration retains "
        "strong solar suppression for quartic-tapered tracking candidates; "
        "ambient lapse and three-sightline activation must be checked on the "
        "same physical coupling and background. Spectroscopy fits are unchanged."
    )

    op = project_root / "results" / "step_21_canonical_projection.json"
    op.write_text(json.dumps(out, indent=2))
    print_status(f"\nwrote {op}", "SUCCESS")
    return str(op)


if __name__ == "__main__":
    main()
