#!/usr/bin/env python3
"""
Step 14: Species-Resolved Opacity Three-Point Test (Opacity Programme)

The Section 4.2 requirement — reproduce the reionization wing
tau(z <~ 6) ~= 0.054, a last-scattering surface at tau ~ 1 at the
LSS depth, and the Gunn-Peterson/Lyman-continuum trough onset — is
derived here as a species-resolved statement about n_e(ell) and
n_HI(ell) rather than as an asserted density rise.  The original
"rise ~14x by z ~ 7 and ~500x by the LSS" fiducials are recovered
as derived quantities:

  * "14x" is the wing electron density required under the
    EXPONENTIAL path law (ell = ell0 ln(1+z)); under the canonical
    curvature-regular p = 0.5 power law the same wing datum
    requires only n_e ~ 0.5 n_b0.
  * "500x" is the electron column of the ionization front at the
    boundary depth under the p = 0.5 law — parametrized here as a
    concentrated column of thickness ~1 Hubble radius; it is the
    front's Thomson column (a phase boundary in the ambient
    radiation field), not a physical density shell.

Under p = 0.5 the three points admit a unique morphology —
ionized wing (z <~ 6), neutral trough (z ~ 6 -> edge), sharp
ionization front at the boundary — because a monotonic electron
rise overshoots the wing by ~30x (constant n_b0 alone reaches
tau = 1 at z ~ 20).  The neutral trough is therefore a DERIVED
necessity of the power-law branch, not an assumption, and it is
the same object as the observed Gunn-Peterson saturation.  Under
the exponential branch the front column at z ~ 1100 coexists with
an absorption edge pushed to z ~ 10^197-10^8000 (Gate 11 rows), so
the power-law branch is the branch on which the observed boundary
depth lives; the three-point test thus discriminates the temporal
law itself.

Part A derives the requirement vector (f_wing, x_trough,
n_e,front x Delta_ell_front, z_edge) for both branches.
Part B constructs an explicit admissible profile and
forward-integrates tau_Thomson(ell) and the LyC opacity,
demonstrating simultaneous satisfaction of all three points.
Part C performs the pilot absorber-statistics inversion on the
26-object KODIAQ LLS catalogue in-repo: incidence remapped per
unit TEP path length, LyC column accumulation, and the
photoionization-inverted wing density locus n_b(Gamma).  The
pilot demonstrates the machinery; a statistically complete
inversion requires an enlarged LLS/forest catalogue (HD-LLS /
SQUAD / XQ-100 scale).

Literature inputs are flagged as such.  Outputs:
results/step_14_opacity_three_point.json
"""
import sys
import json
from pathlib import Path

import numpy as np

project_root = Path(__file__).resolve().parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from scripts.utils.logger import print_status, setup_step_logger

# ---------------------------------------------------------------------------
# Corpus constants (Step 11 thermalization ledger / TEP-TH density)
# ---------------------------------------------------------------------------
N_B0 = 2.51e-7            # cm^-3  corpus baryon density today
L0 = 1.3215e28            # cm     c/H0 path unit
TAU_PER_L0 = 2.2026e-3    # Thomson tau per L0 at n_e = n_b0 (Step 11 kappa=0.397 row)
SIGMA_GP = 4.48e-18       # cm^2   effective Ly-alpha Gunn-Peterson cross-section
SIGMA_LYC = 6.3e-18       # cm^2   hydrogen Lyman-continuum edge cross-section
ALPHA_A = 4.2e-13         # cm^3/s case-A recombination, T ~ 2e4 K forest gas
TAU_REION = 0.054         # Planck electron-scattering wing target

Z_T = 6.0                 # trough onset fiducial (GP saturation z ~ 6)
Z_EDGE = 1080.0           # LSS-depth fiducial (screened z* target; Gate-11B
                          # dust-edge range z ~ 130-1340 brackets it)


def ell_pl(z):
    """Comoving path length in L0 units, power-law branch p = 0.5."""
    return (1.0 + z) ** 2 - 1.0


def ell_exp(z):
    """Comoving path length in L0 units, exponential branch A(x) = e^{-x}."""
    return np.log(1.0 + z)


def dldz_pl(z):
    return 2.0 * (1.0 + z)


def dldz_exp(z):
    return 1.0 / (1.0 + z)


def run_step_14():
    setup_step_logger(Path(__file__).stem)
    print_status("=== STEP 14: SPECIES-RESOLVED OPACITY THREE-POINT TEST ===",
                 "SUCCESS")

    # ------------------------------------------------------------------
    # (A) Derived requirement vector, both temporal-law branches
    # ------------------------------------------------------------------
    # Wing: tau(z_t) = TAU_PER_L0 * f_w * ell(z_t) = TAU_REION
    f_w_pl = TAU_REION / (TAU_PER_L0 * ell_pl(Z_T))
    f_w_exp = TAU_REION / (TAU_PER_L0 * ell_exp(Z_T))

    # Trough thinness (power-law): residual column to the edge must not
    # close tau before the wall — bound mean electron density z_t -> edge.
    tau_allow_trough = 1.0 - TAU_REION
    n_tr_max_pl = tau_allow_trough / (
        TAU_PER_L0 * (ell_pl(Z_EDGE) - ell_pl(Z_T)))
    n_tr_max_exp = tau_allow_trough / (
        TAU_PER_L0 * (ell_exp(Z_EDGE) - ell_exp(Z_T)))

    # Wall: Delta_tau_wall ~ 0.9 accumulated over a shell of thickness
    # Delta_ell (L0 units) at density f_wall x n_b0:
    #     f_wall = Delta_tau / (TAU_PER_L0 * Delta_ell)
    wall_rows = []
    for d_ell in [0.5, 1.0, 2.0]:
        wall_rows.append({
            "wall_thickness_L0": d_ell,
            "f_wall_for_dtau_0p9": 0.9 / (TAU_PER_L0 * d_ell),
        })

    req = {
        "wing_tau_target": TAU_REION,
        "wing_density_powerlaw": f_w_pl,
        "wing_density_exponential": f_w_exp,
        "trough_mean_ne_ceiling_powerlaw": n_tr_max_pl,
        "trough_mean_ne_ceiling_exponential": n_tr_max_exp,
        "wall_density_grid": wall_rows,
        "note": (
            "Species-resolved requirement.  Wing datum selects "
            f"n_e ~ {f_w_pl:.2f} n_b0 (p = 0.5) or ~{f_w_exp:.0f} n_b0 "
            "(exponential) — the earlier '14x' fiducial is recovered as "
            "the exponential-branch wing density.  Under p = 0.5 the "
            "column z_t -> edge is ~1.7e6 L0, so a continuous electron "
            "column is forbidden: the mean electron density there must "
            f"stay below ~{n_tr_max_pl:.1e} n_b0 — i.e. the trough "
            "medium is derived to be neutral (the Gunn-Peterson "
            "saturation IS this requirement).  The '500x' fiducial is "
            "recovered as the concentrated front column at the boundary depth "
            "(f_wall ~ 400-800 n_b0 over ~1 L0 for Delta_tau ~ 0.9) "
            "parametrizing the ionization front, coincident with the "
            "Gate-11B dust absorption edge.  Under the exponential branch the wing "
            "requires the 14x density and a smooth rise works, but the "
            "Gate-11 absorption edge recedes to z ~ 10^197-10^8000; the "
            "observed z* ~ 10^3 boundary therefore selects the "
            "power-law branch, and the trough-collapse prediction is "
            "branch-forced."
        ),
    }

    # ------------------------------------------------------------------
    # (B) Explicit admissible profile (canonical p = 0.5 branch)
    # ------------------------------------------------------------------
    # Zones:
    #   wing   0 < z < Z_T        : n_e = f_w_pl n_b0   (ionized IGM)
    #   trough Z_T < z < Z_EDGE   : n_e = x_tr n_b0     (neutral IGM)
    #   wall   z_w0 < z < Z_EDGE  : n_e = f_wall n_b0   (re-ionized wall)
    x_tr = 1e-5          # trough residual electron fraction (neutral IGM)
    f_wall = 500.0       # wall electron density (n_b0 units)
    # wall thickness chosen so cumulative tau reaches ~1 at the edge
    # (wing 0.054 + trough ~0.026 -> wall supplies ~0.92)
    dwall_l0 = 0.92 / (TAU_PER_L0 * f_wall)
    # translate wall thickness to a redshift shell just below the edge;
    # ell(z) = (1+z)^2 - 1 inverts as z = sqrt(ell + 1) - 1
    z_wall_inner = (ell_pl(Z_EDGE) - dwall_l0 + 1.0) ** 0.5 - 1.0

    # Exact optical depth: the profile is piecewise constant in z, so
    # integrate in ell analytically — the wall is far thinner than any
    # practical z-grid spacing and grid integration under-resolves it.
    zone_edges = [(0.0, Z_T, f_w_pl),
                  (Z_T, z_wall_inner, x_tr),
                  (z_wall_inner, Z_EDGE, f_wall)]

    def tau_exact(zp):
        t = 0.0
        for z0, z1, nfrac in zone_edges:
            lo, hi = min(z0, zp), min(z1, zp)
            if hi > lo:
                t += nfrac * (ell_pl(hi) - ell_pl(lo))
        return TAU_PER_L0 * t

    z_probe = [1, 3, 4, 6, 7, 20, 100, 500, 1000, Z_EDGE]
    tau_probe = {f"tau_at_z_{zp:g}": float(tau_exact(zp))
                 for zp in z_probe}
    # tau = 1 surface: crossed inside the wall — solve analytically
    tau_enter_wall = TAU_PER_L0 * (
        f_w_pl * ell_pl(Z_T)
        + x_tr * (ell_pl(z_wall_inner) - ell_pl(Z_T)))
    ell_at_tau1 = ell_pl(z_wall_inner) + (
        (1.0 - tau_enter_wall) / (TAU_PER_L0 * f_wall))
    z_surface = float(np.sqrt(ell_at_tau1 + 1.0) - 1.0)

    # Trough LyC opacity: neutral column at n_HI ~ n_b0 over
    # the trough path gives the saturation depth of the trough.
    tau_lyc_trough = SIGMA_LYC * N_B0 * (
        ell_pl(Z_EDGE) - ell_pl(Z_T)) * L0
    tau_lya_trough = SIGMA_GP * N_B0 * (
        ell_pl(Z_EDGE) - ell_pl(Z_T)) * L0

    profile = {
        "morphology": ("ionized wing -> neutral trough -> ionization "
                       "front (concentrated-column parametrization)"),
        "parameters": {
            "f_wing": f_w_pl,
            "x_trough_residual": x_tr,
            "f_wall": f_wall,
            "wall_thickness_L0": dwall_l0,
            "z_wall_inner": z_wall_inner,
            "z_edge": Z_EDGE,
        },
        "tau_probe": tau_probe,
        "tau_1_surface_z": z_surface,
        "tau_reion_wing_z6": tau_probe["tau_at_z_6"],
        "tau_lyc_trough": tau_lyc_trough,
        "tau_lya_trough": tau_lya_trough,
        "checks": {
            "wing_matches_tau_reion": abs(tau_probe["tau_at_z_6"]
                                          - TAU_REION) < 0.01,
            "thin_column_preserved": tau_probe["tau_at_z_1000"] < 0.1,
            "tau1_surface_at_edge": abs(z_surface - Z_EDGE) / Z_EDGE < 0.05,
            "trough_saturated": tau_lyc_trough > 1e3,
        },
        "note": (
            "Explicit admissible n_e(ell): f_wing = "
            f"{f_w_pl:.3f} n_b0 out to z = {Z_T:g}, neutral trough "
            f"(residual x_e = {x_tr:g}) to the boundary depth, and a "
            f"{f_wall:.0f}x n_b0 ionization-front column of equivalent "
            f"thickness {dwall_l0:.2f} L0 at z ~ {Z_EDGE:g}.  The wing column "
            f"reproduces tau_reion = {tau_probe['tau_at_z_6']:.3f} "
            "(Planck 0.054), the trough contributes ~zero Thomson "
            "depth while the LyC column saturates at "
            f"{tau_lyc_trough:.1e} (the GP trough), and the front column "
            f"places the tau = 1 surface at z = {z_surface:.0f} — "
            "coincident with the absorption edge by construction "
            "(the front IS the ionized skin of the Gate-11B "
            "opacity boundary: a Strömgren edge in the ambient "
            "radiation field, not a material shell).  This is an existence demonstration "
            "of a profile satisfying all three points; its profile "
            "shape is the datum the population-scale absorber "
            "inversion (Part C) must recover."
        ),
    }

    # ------------------------------------------------------------------
    # (C) Pilot absorber inversion — 26-object in-repo KODIAQ LLS list
    # ------------------------------------------------------------------
    try:
        cat = json.load(open(project_root / "data"
                             / "kodiaq_z_lls_catalog.json"))
    except Exception:
        cat = []

    pilot = {"n_systems": len(cat), "status": "no catalogue"}
    if cat:
        zs = np.array([s["z_abs"] for s in cat])
        nhis = np.array([s["log_nhi"] for s in cat])
        z_lo, z_hi = float(zs.min()), float(zs.max())

        # Incidence remapped per unit path (geometric — no microphysics)
        dz = z_hi - z_lo
        dN_dz = len(zs) / dz
        dldz_pl_3 = dldz_pl(3.0)      # L0 per dz at z~3, power-law
        dldz_exp_3 = dldz_exp(3.0)
        pilot["incidence"] = {
            "z_range": [z_lo, z_hi],
            "dN_dz_observed": dN_dz,
            "dN_dL0_powerlaw": dN_dz / dldz_pl_3,
            "dN_dL0_exponential": dN_dz / dldz_exp_3,
            "note": "TEP path Jacobian: at z~3 one dz spans "
                    f"{dldz_pl_3:.0f} L0 (p=0.5) — the same absorber "
                    "population maps to ~8x lower incidence per unit "
                    "path than a Euclidean reading.",
        }

        # LyC column accumulation rate from the observed systems
        mean_NHI = float(np.mean(10.0 ** nhis))
        dtau_lyc_dz = mean_NHI * SIGMA_LYC * dN_dz
        dtau_lyc_dL0 = dtau_lyc_dz / dldz_pl_3
        pilot["lyc_column"] = {
            "mean_NHI_cm^-2": mean_NHI,
            "dtau_LyC_per_dz": dtau_lyc_dz,
            "dtau_LyC_per_L0": dtau_lyc_dL0,
            "note": "Observed LLS/sub-LLS systems alone accumulate "
                    "LyC depth; the diffuse trough column (Part B) "
                    "dominates by orders of magnitude.",
        }

        # Photoionization inversion of the wing: the observed forest
        # mean opacity per unit z maps to n_HI via the TEP Jacobian;
        # equilibrium n_b = sqrt(Gamma * n_HI / alpha_A) then gives
        # the wing-density locus as a function of the maintained UVB.
        # Literature anchors (flagged): forest effective opacity
        # tau_eff(z) ~ Becker+2013 / Faucher-Giguere+2008 rounded
        # values; local photoionization rate Gamma_12 = 1 (1e-12/s).
        tau_eff_lit = {2.4: 0.22, 3.0: 0.37, 3.7: 0.65,
                       4.2: 1.0, 4.8: 1.8, 5.4: 2.9}
        inv_rows = []
        for zt, tef in tau_eff_lit.items():
            n_hi = tef / (SIGMA_GP * dldz_pl(zt) * L0)
            row = {"z": zt, "tau_eff_lit": tef,
                   "n_HI_implied_cm^-3": n_hi}
            for gam in [1e-14, 1e-12]:
                row[f"n_b_at_Gamma_{gam:g}"] = float(
                    np.sqrt(gam * n_hi / ALPHA_A) / N_B0)
            inv_rows.append(row)
        pilot["forest_inversion"] = {
            "rows": inv_rows,
            "gamma_locus": {
                "note": "n_b ∝ sqrt(Gamma): the wing requirement "
                        "n_b ~ f_wing n_b0 selects a maintained UVB "
                        "level per redshift; the (n_b, Gamma) pair is "
                        "the degeneracy the Gate-12 emissivity budget "
                        "and an enlarged catalogue jointly break.",
            },
            "method": ("tau_eff(z) = sigma_GP n_HI dL/dz inverts to "
                       "n_HI(ell); photoionization equilibrium "
                       "x_HI = alpha_A n_p / Gamma gives "
                       "n_b = sqrt(Gamma n_HI / alpha_A)."),
        }
        pilot["status"] = "pilot complete — 26-system catalog"

    ledger = {
        "step": "step_14_opacity_three_point",
        "A_derived_requirement": req,
        "B_admissible_profile": profile,
        "C_pilot_inversion": pilot,
        "verdict": (
            "The three-point opacity requirement is restated in "
            "species-resolved form and shown satisfiable: under the "
            "canonical p = 0.5 path law an explicit admissible profile "
            f"(wing n_e ~ {f_w_pl:.2f} n_b0 for z <~ {Z_T:g}; neutral "
            f"trough x_e <~ 1e-4 for z ~ {Z_T:g}-{Z_EDGE:g}; ionization-front "
            f"column ~{f_wall:.0f}x n_b0 over ~{dwall_l0:.1f} L0 at "
            f"the edge) gives tau(z<6) = {tau_probe['tau_at_z_6']:.3f} "
            "(target 0.054), a saturated trough (tau_LyC ~ "
            f"{tau_lyc_trough:.0e}), and tau = 1 at z = "
            f"{z_surface:.0f} coincident with the Gate-11B absorption "
            "edge.  The trough collapse is a derived necessity of the "
            "power-law branch — the Gunn-Peterson saturation IS the "
            "requirement, not an extra datum.  The earlier 14x/500x "
            "fiducials are recovered as the exponential-branch wing "
            "density and the power-law front column respectively.  The "
            "pilot inversion demonstrates the absorber-statistics "
            "machinery on the in-repo 26-system KODIAQ list; closure at "
            "population scale requires an enlarged LLS/forest "
            "catalogue."),
    }

    out = project_root / "results" / "step_14_opacity_three_point.json"
    out.write_text(json.dumps(ledger, indent=2))

    print_status(f"[A] Wing requirement: n_e = {f_w_pl:.2f} n_b0 "
                 f"(p=0.5) / {f_w_exp:.0f} n_b0 (exp)", "PROCESS")
    print_status(f"[A] Trough ceiling (p=0.5): mean n_e < "
                 f"{n_tr_max_pl:.1e} n_b0 — neutral", "PROCESS")
    print_status(f"[B] tau(z<6) = {tau_probe['tau_at_z_6']:.3f}; "
                 f"tau=1 surface at z = {z_surface:.0f}", "SUCCESS")
    print_status(f"[B] Trough LyC tau ~ {tau_lyc_trough:.1e} "
                 "(saturated)", "SUCCESS")
    checks = profile["checks"]
    for k, v in checks.items():
        print_status(f"  check {k}: {v}",
                     "SUCCESS" if v else "WARNING")
    print_status(f"[WRITE] {out}", "SUCCESS")
    return ledger


if __name__ == "__main__":
    run_step_14()
