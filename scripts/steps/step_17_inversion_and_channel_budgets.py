#!/usr/bin/env python3
"""
Step 17: Absorber-Statistics Inversion (Literature Inputs) +
Deuterium Channel Budgets

This step audits quantitative requirements and model assumptions of
Steps 14/15. It does not ingest a complete absorber catalogue or solve
TEP stellar structure, reservoir evolution, or temporal-well collapse.

Part A — Absorber-statistics inversion on published incidence
functions (flagged literature inputs; the in-repo 26-system
KODIAQ list remains the catalog-level pilot of Step 14).

  Inputs (documented, flagged):
    * LLS incidence   dN/dz ~ 2.8   (N_HI >~ 17.2, z ~ 2-4;
                                     Prochaska+10, Songaila&Cowie10)
    * Forest tau_eff(z)             (Becker+13 / Faucher-Giguere+08
                                     rounded values, reused from
                                     Step 14)
    * LyC mean free path lambda_mfp ~ 45 pMpc at z ~ 3
                                     (Worseck+14)
    * UVB Gamma ~ 0.5-1.5e-12/s at z < 5.5, collapsing > z ~ 6
                                     (FG08, Becker+13, Worseck+14)

  Machinery: the TEP path Jacobian maps each statistic per unit
  path; the photoionization balance x_HI = alpha_A n_p / Gamma
  inverts the forest opacity to the diffuse density locus
  n_b(Gamma).  Output: whether literature absorber statistics
  recover the admissible wing density and what they imply for
  the trough and wall.  Honest limits are stated: the trough is
  the Gunn-Peterson-saturated regime — no resolvable absorber
  distribution exists there by definition — so the inversion
  constrains the wing directly and the trough via saturation.

Part B — Collapse neutrino irradiation budget (Step-15 channel 2
made quantitative).
    For an M_sms collapse, the nubar_e fluence through an envelope
    shell at radius r gives neutron yield per proton
    y_n(r) = F_nu sigma_nubar(E).  The strongly-irradiated mass
    fraction — shells reaching y_n >~ 1e-3, the level needed for
    D/H ~ 1e-4 after capture competition — is evaluated for a
    polytropic (n = 3) envelope over the FWW86/FS97 neutrino-
    energy range.  Output: the mass-weighted enrichment for a
    static-envelope geometry, and the statement of what the
    collapse-transient geometry (envelope traversing the
    irradiated zone during descent — the FS97 case) changes.
    This is the honest check of whether the channel is viable
    with the A2 transport fixed or whether it stays conditional.

Part C — VMO ejecta closure region.
    The (f_ej, eps_D) closure plane for the partial-burning
    channel: required ejecta share f_req = p_req/eps_D across the
    documented enrichment range, against the ejected fraction
    implied by the helium channel's own E_Y > 0 requirement.
    Output: the overlap region — at f_ej ~ 0.5 the required
    enrichment is eps_D ~ 4e-5 (D/H ~ 2e-5, marginally above
    ISM), deep inside the documented 1e-5..2e-4 window.

Part D — Protected-reservoir mixing bound.
    f_mix = p_req / X_D,res with X_D,res = GCR yield x N_exp;
    the two-sided longevity condition (reservoir must survive
    N_exp exposure-equivalents to accumulate, and mix at f_mix
    of replenishment) and the shared observational signature
    with the collapse-ejecta channel (metal-poor high-D/H gas,
    the FS97 LLS-mimic prediction).

Outputs: results/step_17_inversion_and_channel_budgets.json
"""
import sys
import json
from pathlib import Path

import numpy as np

project_root = Path(__file__).resolve().parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from scripts.utils.logger import print_status, setup_step_logger

# Corpus constants
N_B0 = 2.51e-7            # cm^-3
L0 = 1.3215e28            # cm
TAU_PER_L0 = 2.2026e-3
SIGMA_GP = 4.48e-18       # cm^2
SIGMA_LYC = 6.3e-18       # cm^2
ALPHA_A = 4.2e-13         # cm^3/s
TAU_REION = 0.054
Z_T = 6.0

# Gate-13 demand
P_REQ = 2.04e-5
GCR_YIELD = 1.7e-7
X_D_ISM = 3.4e-5


def ell_pl(z):
    return (1.0 + z) ** 2 - 1.0


def dldz_pl(z):
    return 2.0 * (1.0 + z)


def run_step_17():
    setup_step_logger(Path(__file__).stem)
    print_status("=== STEP 17: LITERATURE INVERSION + D BUDGETS ===",
                 "SUCCESS")

    # ------------------------------------------------------------------
    # (A) Literature-statistics absorber inversion
    # ------------------------------------------------------------------
    # LLS/sub-LLS LyC opacity per unit path
    dn_dz_lls = 2.8                     # literature input (z~2-4)
    mean_nhi_lls = 10.0 ** 17.2         # characteristic LLS column
    tau_per_lls = mean_nhi_lls * SIGMA_LYC
    dtau_lyc_dz = dn_dz_lls * (1.0 - np.exp(-tau_per_lls))
    dldz_3 = dldz_pl(3.0)
    dz_per_mfp = 1.0 / dtau_lyc_dz      # redshift span per LyC mfp
    mfp_lyc_l0 = dz_per_mfp * dldz_3    # TEP path per LyC mean free path

    # Forest inversion: n_b(Gamma) locus per redshift
    tau_eff_lit = {2.4: 0.22, 3.0: 0.37, 3.7: 0.65,
                   4.2: 1.0, 4.8: 1.8, 5.4: 2.9}
    forest_rows = [{"z": zt, "tau_eff_illustrative": tef}
                   for zt, tef in tau_eff_lit.items()]

    # Wing datum confrontation: admissible wing density 0.51 n_b0
    f_w_req = TAU_REION / (TAU_PER_L0 * ell_pl(Z_T))
    wing_gammas = []
    for zt, tef in tau_eff_lit.items():
        # Gamma at which the diffuse density equals the wing value
        wing_gammas.append({"z": zt, "Gamma_for_wing_density_s^-1": None,
                            "reason": "Requires a calibrated line-profile and density-PDF likelihood"})

    inv = {
        "lls_inputs": {
            "dN_dz_LLS_lit_assumed": dn_dz_lls,
            "N_HI_cm^-2_assumed": mean_nhi_lls,
            "effective_dtau_LyC_per_dz_z3_poisson": float(dtau_lyc_dz),
            "lyc_mfp_dz_z3": float(dz_per_mfp),
            "lyc_mfp_L0_z3": float(mfp_lyc_l0),
            "note": (
                f"Assuming a Poisson population of identical LLS with "
                f"N_HI=10^17.2 cm^-2 gives effective opacity "
                f"{dtau_lyc_dz:.2f} per unit z at z~3 and "
                f"Delta z={dz_per_mfp:.2f}; this is not a measured "
                "high-z trough mean free path. Frequency evolution, "
                "column distribution and selection are omitted."),
        },
        "forest_rows": forest_rows,
        "wing_confrontation": {
            "admissible_wing_density_n_b0": f_w_req,
            "gamma_for_wing_per_z": wing_gammas,
            "note": "No density or UVB rate is inferred: tau_eff=-ln(<F>) "
                    "is not equal to a monochromatic cross section "
                    "times a mean neutral column. Saturated pixels, "
                    "line profiles, covering factors and the density "
                    "distribution require a forward forest likelihood.",
        },
        "trough_statement": (
            "Forest saturation limits inference of neutral fraction "
            "and cannot establish the 10^-5 residual ionization "
            "assumed in the Step-14 trough, or a wall at z=1080."),
        "completeness_caveat": (
            "Inputs are rounded literature-scale placeholders, not a "
            "complete or selection-corrected catalogue. The available "
            "26-system KODIAQ pilot is not complete; the KOA match "
            "list is empty. No forward reconstruction or selection "
            "function can be checked with these inputs."),
        "checks": {"complete_catalogue_ingested": False,
                   "selection_function_applied": False,
                   "forest_forward_reconstructed": False},
    }

    # ------------------------------------------------------------------
    # (B) Collapse neutrino irradiation budget
    # ------------------------------------------------------------------
    # Documented collapse energy scale: SMS binding release into
    # neutrinos ~ 1e57-1e59 erg (FWW86/FS97 range); neutrino mean
    # energy ~ 10 MeV; sigma_nubar_p ~ 9.4e-42 cm^2 at 10 MeV.
    results_nu = []
    for e_nu in [1e57, 1e58, 1e59]:
        n_nu = e_nu / 1.602e-5                     # 10 MeV in erg
        for r_shell_cm in [1e12, 1e13, 1e14]:
            fluence = n_nu / (4.0 * np.pi * r_shell_cm ** 2)
            y_n = fluence * 9.4e-42
            results_nu.append({
                "E_nu_erg": e_nu, "r_shell_cm": r_shell_cm,
                "fluence_cm^-2": float(fluence),
                "y_n_per_proton": float(y_n),
            })
    # Strongly-irradiated mass for n=3 polytrope: f_mass ~ 18.1 (r/R)^3
    nu_mass_rows = []
    for e_nu in [1e57, 1e58, 1e59]:
        n_nu = e_nu / 1.602e-5
        # radius where y_n = 1e-3 (needed for D/H ~ 1e-4)
        r_crit = np.sqrt(n_nu * 9.4e-42 / (1e-3 * 4.0 * np.pi))
        for r_star in [1e13, 1e14]:
            nu_mass_rows.append({
                "E_nu_erg_assumed_nubar_e": e_nu, "R_star_cm": r_star,
                "r_crit_y_n_1e-3_cm": float(r_crit),
                "r_crit_over_R": float(r_crit / r_star),
            })
    nu_budget = {
        "inputs": ("Illustrative antineutrino energy 1e57-1e59 erg, "
                   "all assigned to 10 MeV antineutrinos; cross section "
                   "9.4e-42 cm^2 is a toy value requiring threshold and "
                   "spectrum validation; no collapse model is used."),
        "fluence_rows": results_nu,
        "radius_threshold_rows": nu_mass_rows,
        "assessment": (
            "Inverse-square fluence and the radius where assumed capture "
            "probability exceeds 1e-3 are computed. The fraction of "
            "ejected envelope mass inside that radius is not known: "
            "an n=3 central mass fraction cannot represent processed "
            "ejecta. Standard neutrinos propagate on the matter metric "
            "during a TEP temporal-well formation transient, not through "
            "a conventional black-hole horizon. A time-dependent "
            "neutrino luminosity, spectrum, metric and envelope trajectory "
            "are required before a yield can be claimed."),
        "checks": {"fluence_inverse_square": bool(np.isclose(
            results_nu[0]["y_n_per_proton"] / results_nu[1]["y_n_per_proton"], 100)),
                   "dynamical_collapse_solved": False},
    }

    # ------------------------------------------------------------------
    # (C) VMO ejecta closure region
    # ------------------------------------------------------------------
    eps_grid = [1e-5, 2e-5, 4e-5, 1e-4, 2e-4, 4e-4]
    closure_rows = []
    for eps in eps_grid:
        closure_rows.append({
            "ejecta_X_D_assumed": eps,
            "ejecta_D_over_H_approx": eps / 2.0,
            "net_eps_D_if_ambient_feed": max(0.0, eps - X_D_ISM),
            "f_required_if_D_free_feed": P_REQ / eps,
            "f_required_if_ambient_feed": (P_REQ / (eps - X_D_ISM)
                                           if eps > X_D_ISM else None),
        })
    ejecta = {
        "closure_rows": closure_rows,
        "required_net_eps_D_at_f_0p5": P_REQ / 0.5,
        "minimum_ejecta_X_D_at_f_0p5_if_ambient_feed": X_D_ISM + P_REQ / 0.5,
        "key_point": (
            "At assumed f_ej=0.5 the required NET yield is 4.08e-5. "
            "If feed gas begins at ISM X_D=3.4e-5, the ejecta must "
            "reach at least X_D=7.48e-5 (~D/H 3.74e-5) before losses; "
            "returning gas at ISM D/H is not net production. If incoming "
            "gas is D-free the earlier gross threshold applies instead. "
            "Neither the returned mass fraction nor the freezeout yield "
            "is computed from a TEP stellar structure solution."),
        "checks": {"net_yield_not_gross": True,
                   "tep_stellar_structure_solved": False},
    }

    # ------------------------------------------------------------------
    # (D) Protected-reservoir mixing bound
    # ------------------------------------------------------------------
    res_rows = []
    for n_exp in [3e2, 1e3, 3e3, 1e4]:
        x_res = GCR_YIELD * n_exp
        res_rows.append({
            "N_exp": n_exp, "X_D_res_from_zero": x_res,
            "f_mix_required_if_D_free_feed": P_REQ / x_res,
            "f_mix_required_if_ambient_feed": (
                P_REQ / (x_res - X_D_ISM) if x_res > X_D_ISM else None),
        })
    reservoir = {
        "rows": res_rows,
        "two_sided_bound": (
            "The 120/N_exp mixing relation holds only for D-free feed. "
            "For ambient feed subtract initial X_D before calculating "
            "net production. N_exp is a dimensionless assumed cosmic-ray "
            "fluence multiplier, not a duration: longevity cannot be "
            "deduced without a rate per year. Convergent astration "
            "exposure alone does not guarantee 300-10000 cosmic-ray "
            "exposure equivalents or survival against mixing."),
        "checks": {"mixing_arithmetic": bool(np.isclose(
            res_rows[1]["f_mix_required_if_D_free_feed"]
            * res_rows[1]["X_D_res_from_zero"], P_REQ)),
                   "longevity_from_rate_verified": False},
        "signature": (
            "Metal-poor gas with super-ISM D/H — identical to the "
            "Fuller & Shi 1997 prediction for supermassive-star "
            "ejecta masquerading as Lyman-limit systems: the "
            "collapse-ejecta and reservoir channels share one "
            "observational discriminator."),
    }

    ledger = {
        "step": "step_17_inversion_and_channel_budgets",
        "A_literature_inversion": inv,
        "B_nu_irradiation_budget": nu_budget,
        "C_vmo_ejecta_closure": ejecta,
        "D_reservoir_mixing": reservoir,
        "verdict": (
            "Audit status: no catalogue-level absorber inversion is "
            "performed. Rounded literature tau_eff values cannot be "
            "mapped to mean neutral columns because tau_eff=-ln<F> is "
            "nonlinear and saturated; the wing-density confrontation "
            "is therefore not an inference. The assumed Poisson LLS "
            "opacity at z~3 gives Delta z~0.57 per LyC mean free path "
            "(illustrative only). On the deuterium side: closure "
            "requires NET enrichment. At assumed f_ej=0.5 the net "
            "requirement is eps_D=4.08e-5; with ambient-IS feed the "
            "ejecta must reach X_D>=7.48e-5 (D/H~3.7e-5), inside the "
            "documented window but requiring a TEP VMO structure "
            "solution. The antineutrino budget computes only "
            "inverse-square fluence and a capture-radius threshold — "
            "the irradiated ejecta mass is undetermined pending the "
            "dynamical temporal-well collapse solution. The reservoir "
            "channel's f_mix values hold for D-free feed and are "
            "dimensionless exposure bookkeeping; longevity requires a "
            "rate model."),
    }

    out = project_root / "results" / "step_17_inversion_and_channel_budgets.json"
    out.write_text(json.dumps(ledger, indent=2))

    print_status("[A] no catalogue inversion performed; tau_eff is "
                 "nonlinear — wing-density confrontation withheld",
                 "WARNING")
    print_status(f"[A] assumed LLS Poisson opacity -> Delta_z = "
                 f"{dz_per_mfp:.2f} ({mfp_lyc_l0:.1f} L0 path)", "PROCESS")
    rc = [r['r_crit_over_R'] for r in nu_mass_rows]
    print_status(f"[B] nu: capture radius r_crit/R computed "
                 f"({min(rc):.3f}-{max(rc):.3f}); "
                 "ejecta mass undetermined", "PROCESS")
    print_status(f"[C] net eps_D req = {P_REQ/0.5:.1e} at f_ej=0.5; "
                 f"ambient feed needs ejecta X_D >= "
                 f"{X_D_ISM + P_REQ/0.5:.1e}", "PROCESS")
    print_status(f"[D] reservoir f_mix (D-free feed) = "
                 f"{res_rows[1]['f_mix_required_if_D_free_feed']:.2f}"
                 f"-{res_rows[-1]['f_mix_required_if_D_free_feed']:.3f}",
                 "PROCESS")
    print_status(f"[WRITE] {out}", "SUCCESS")
    return ledger


if __name__ == "__main__":
    run_step_17()
