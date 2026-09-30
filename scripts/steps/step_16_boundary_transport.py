#!/usr/bin/env python3
"""
Step 16: Eternal-Native Boundary Transport (Opacity Programme II)

Step 14 supplied an imposed three-zone electron profile; its 'wall'
zone is the concentrated-column parametrization of the ionization
front — the Stroemgren edge between the neutral foreground and the
deep thermalized zone — not a physical density shell. This step
computes its visibility, conditional geometric scales, equilibrium
sensitivity, and source-budget inequalities. None of these calculations
solves a native Boltzmann hierarchy or places the front dynamically.
Saha equilibrium is conditional on a local LTE temperature; observed
redshift alone does not set local gas temperature in static TEP.

Outputs: results/step_16_boundary_transport.json
"""
import sys
import json
from pathlib import Path

import numpy as np

project_root = Path(__file__).resolve().parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from scripts.utils.logger import print_status, setup_step_logger

# Corpus constants (Step 11 / Step 14)
N_B0 = 2.51e-7            # cm^-3
L0 = 1.3215e28            # cm  (c/H0)
TAU_PER_L0 = 2.2026e-3    # Thomson tau per L0 at n_e = n_b0
SIGMA_LYC = 6.3e-18       # cm^2
ALPHA_B = 2.59e-13        # cm^3/s case-B ~1e4 K
ALPHA_A = 4.2e-13         # cm^3/s
T0 = 2.725                # K
Z_EDGE = 1080.0
Z_T = 6.0

# Saha constants (cgs)
K_B = 1.380649e-16        # erg/K
H_PL = 6.62607015e-27     # erg s
M_E = 9.1093837e-28       # g
E_ION = 2.1787e-11        # erg (13.6 eV)


def ell_pl(z):
    return (1.0 + z) ** 2 - 1.0


def dldz_pl(z):
    return 2.0 * (1.0 + z)


def saha_x(n_b_cm3, T):
    """Hydrogen ionization fraction from Saha equilibrium (cgs)."""
    coeff = (2.0 * np.pi * M_E * K_B * T / H_PL ** 2) ** 1.5 \
        * np.exp(-E_ION / (K_B * T)) / n_b_cm3
    return (-coeff + np.sqrt(coeff ** 2 + 4.0 * coeff)) / 2.0


def run_step_16():
    setup_step_logger(Path(__file__).stem)
    print_status("=== STEP 16: ETERNAL-NATIVE BOUNDARY TRANSPORT ===",
                 "SUCCESS")

    # Rebuild the Step-14 admissible profile
    f_w = 0.054 / (TAU_PER_L0 * ell_pl(Z_T))
    x_tr = 1e-5
    f_wall = 500.0
    dwall_l0 = 0.92 / (TAU_PER_L0 * f_wall)
    # ell(z) = (1+z)^2 - 1 inverts as z = sqrt(ell + 1) - 1
    z_wall_inner = (ell_pl(Z_EDGE) - dwall_l0 + 1.0) ** 0.5 - 1.0

    def n_e_over_nb0(z):
        z = np.asarray(z, dtype=float)
        return np.where(z <= Z_T, f_w,
               np.where(z < z_wall_inner, x_tr,
               np.where(z <= Z_EDGE, f_wall, f_wall * 10.0)))

    # ------------------------------------------------------------------
    # (A) Visibility function
    # ------------------------------------------------------------------
    zgrid = np.unique(np.concatenate((
        np.linspace(0.0, Z_EDGE - 0.01, 100_001),
        np.linspace(Z_EDGE - 0.01, Z_EDGE + 0.01, 10_001),
        np.linspace(Z_EDGE + 0.01, 4.0 * Z_EDGE, 100_001))))
    ne = n_e_over_nb0(zgrid)
    dtau = TAU_PER_L0 * ne * dldz_pl(zgrid)
    tau = np.zeros_like(zgrid)
    tau[1:] = np.cumsum((dtau[1:] + dtau[:-1]) * np.diff(zgrid) / 2)
    transmission = np.exp(-tau)
    g = dtau * transmission
    norm = np.trapezoid(g, zgrid)
    i_pk = int(np.argmax(g))
    z_pk = float(zgrid[i_pk])
    half = 0.5 * g[i_pk]
    above = np.where(g > half)[0]
    z_lo, z_hi = float(zgrid[above[0]]), float(zgrid[above[-1]])
    # effective width: variance of g normalised
    gn = g / norm
    zbar = float(np.trapezoid(gn * zgrid, zgrid))
    zrms = float(np.sqrt(np.trapezoid(gn * (zgrid - zbar) ** 2, zgrid)))
    wall_fraction = float(np.trapezoid(g[(zgrid >= z_wall_inner) & (zgrid <= Z_EDGE)],
                                       zgrid[(zgrid >= z_wall_inner) & (zgrid <= Z_EDGE)]) / norm)

    vis = {
        "z_peak": z_pk,
        "fwhm_z": [z_lo, z_hi, z_hi - z_lo],
        "z_mean": zbar, "z_rms": zrms,
        "integral": float(norm), "wall_fraction": wall_fraction,
        "monotonic_tau": bool(np.all(np.diff(tau) >= 0)),
        "comparison_standard": (
            f"Imposed-profile visibility has rms width {zrms:.1f} in z; "
            f"only {wall_fraction:.1%} of its probability lies in the "
            "wall. The narrow peak is not a narrow normalized visibility "
            "distribution. Compare the full function to data before "
            "claiming a last-scattering solution."),
    }

    # ------------------------------------------------------------------
    # (B) Diffusion (Silk-analogue) scale
    # ------------------------------------------------------------------
    mfp_l0 = 1.0 / (f_wall * TAU_PER_L0)           # 1/(n_e sigma_T)
    n_scat = 0.92                                   # ~tau across wall
    r_diff = mfp_l0 * np.sqrt(n_scat)               # transverse random walk
    D_A = ell_pl(Z_EDGE) / (1.0 + Z_EDGE)           # angular-size distance
    ell_d = D_A / r_diff
    # deeper thermalized zone: photons fully isotropize; the escape
    # diffusion above is the blurring of the emission surface itself.
    diff = {
        "mfp_wall_L0": mfp_l0,
        "mfp_wall_mpc": mfp_l0 * L0 / 3.0857e24,
        "n_scatter_wall": n_scat,
        "r_diff_L0": r_diff,
        "D_A_over_L0": D_A,
        "ell_damping_geometric": ell_d,
        "comparison": (
            f"Toy angular ratio {ell_d:.0f}, obtained using assumed "
            "D_A = ell/(1+z), a wall of imposed Thomson depth 0.9 and "
            "one mean-free-path random walk. This is not a Silk diffusion "
            "calculation: the diffusion integral needs a time-dependent "
            "scattering rate, photon-baryon coupling, sound speed and "
            "native perturbation transfer function. Numerical proximity "
            "to a CMB damping multipole is not a prediction."),
    }

    # ------------------------------------------------------------------
    # (C) Wall ionization state — Saha at the edge temperature
    # ------------------------------------------------------------------
    T_edge = T0 * (1.0 + Z_EDGE)                    # ~2945 K
    saha_rows = []
    for fw in [100.0, 300.0, 500.0, 800.0, 2000.0]:
        x = float(saha_x(fw * N_B0, T_edge))
        # required photoionization rate to hold x against alpha_B
        gam_req = ALPHA_B * (fw * N_B0) * x / max(1.0 - x, 1e-12)
        saha_rows.append({
            "f_wall": fw, "n_b_cm^-3": fw * N_B0,
            "x_e_saha_T_edge": x,
            "Gamma_required_s^-1": float(gam_req),
        })
    saha = {
        "T_edge_K_assumed": T_edge,
        "rows": saha_rows,
        "statement": (
            f"Conditional LTE at assumed local gas temperature {T_edge:.0f} K "
            f"gives x_e = {saha_rows[0]['x_e_saha_T_edge']:.3f} to "
            f"{saha_rows[-1]['x_e_saha_T_edge']:.3f}. The TEP clock "
            "redshift does not independently set local gas temperature. "
            "Saha equilibrium requires a verified thermalizing ionizing "
            "radiation field and equilibration time. Gamma_required is "
            "an alternative photoionization rate for this ionization "
            "fraction, not a supplement to LTE; neither it nor the "
            "density or radial placement is derived here."),
    }

    # ------------------------------------------------------------------
    # (D) Wall placement — maintained-ionization balance
    # ------------------------------------------------------------------
    n_e_w = f_wall * N_B0                            # cm^-3
    del_ell_cm = dwall_l0 * L0
    # recombinations per cm^2 per s in the wall
    rec_per_area = ALPHA_B * n_e_w ** 2 * del_ell_cm
    # Gate-12 supply at the wall depth: VMO yield N_gamma ~ 1e5 per
    # cycled baryon over ~3 Myr; cycling fraction xi per Gyr.
    n_gamma = 1e5
    seconds_per_gyr = 1e9 * 3.15576e7
    supply_rows = []
    for xi in [1e-3, 1e-6, 1e-9]:
        baryon_col = f_wall * N_B0 * del_ell_cm       # baryons/cm^2
        phot_supply = baryon_col * xi * n_gamma / seconds_per_gyr
        supply_rows.append({
            "xi_per_Gyr": xi,
            "photon_supply_cm^-2_s^-1": float(phot_supply),
            "demand_cm^-2_s^-1": float(rec_per_area),
            "margin_before_escape_or_absorption": float(phot_supply / rec_per_area),
        })
    # LyC mean free path in neutral gas at mean density
    mfp_lyc_cm = 1.0 / (N_B0 * SIGMA_LYC)
    place = {
        "recombination_demand_cm^-2_s^-1": float(rec_per_area),
        "supply_rows": supply_rows,
        "lyc_mfp_cm": mfp_lyc_cm,
        "lyc_mfp_pc": mfp_lyc_cm / 3.0857e18,
        "statement": (
            f"At assumed mean neutral density the threshold LyC mean "
            f"free path is {mfp_lyc_cm/3.0857e24:.2f} Mpc, not parsecs. "
            f"The imposed wall requires {rec_per_area:.2e} recombinations "
            "cm^-2 s^-1. Uniform in-situ emissivity would exceed this "
            "for some trial cycling rates before escape, dust absorption "
            "and geometry; other trial rates fail. The calculation "
            "does not locate the edge, determine source distribution, "
            "or show that a neutral trough can coexist with the wall."),
    }

    # ------------------------------------------------------------------
    # (E) Gamma(ell): three local equilibria
    # ------------------------------------------------------------------
    gam_wing = ALPHA_A * (f_w * N_B0) * 0.9 ** 2 / 0.1  # x=0.9 in wing
    gam_trough = ALPHA_A * N_B0 * x_tr ** 2 / (1.0 - x_tr)
    gamma = {
        "wing_Gamma_needed_s^-1": float(gam_wing),
        "trough_residual_Gamma_s^-1": float(gam_trough),
        "lyc_mfp_pc_neutral_IGM": mfp_lyc_cm / 3.0857e18,
        "required_gamma_drop": float(gam_wing / gam_trough),
        "statement": (
            f"For assumed x_e=0.9 in the wing and x_e=1e-5 in the "
            f"trough, local photoionization balance requires Gamma "
            f"{gam_wing:.2e} versus {gam_trough:.2e} s^-1, a drop "
            f"of {gam_wing/gam_trough:.1e}. The neutral mean-density "
            f"LyC mean free path is {mfp_lyc_cm/3.0857e24:.2f} Mpc. "
            "No coupled emissivity/attenuation solution is provided; "
            "the sharp transition remains a physical requirement."),
    }

    ledger = {
        "step": "step_16_boundary_transport",
        "profile_used": {"f_wing": f_w, "x_trough": x_tr,
                         "f_wall": f_wall, "dwall_L0": dwall_l0,
                         "z_edge": Z_EDGE},
        "A_visibility": vis,
        "B_diffusion_scale": diff,
        "C_wall_ionization_saha": saha,
        "D_wall_placement": place,
        "E_gamma_local_equilibria": gamma,
        "checks": {
            "visibility_normalized": bool(abs(norm - (1 - transmission[-1])) < 0.005),
            "visibility_peak_in_imposed_wall": bool(
                z_wall_inner - 0.01 <= z_pk <= Z_EDGE + 0.01),
            "optical_depth_monotonic": vis["monotonic_tau"],
            "wall_dominates_visibility": bool(wall_fraction > 0.5),
            "wall_placement_derived": False,
            "native_acoustic_spectrum_computed": False,
        },
        "verdict": (
            f"An imposed profile produces a peak at z={z_pk:.3f}, but "
            f"only {wall_fraction:.1%} of normalized visibility lies in "
            f"the wall (rms width {zrms:.1f}). Geometric angular ratio "
            f"{ell_d:.0f} is not a damping-tail prediction. Conditional "
            "LTE Saha balance and a local photon budget do not determine "
            "temperature, wall location or the ionizing background. "
            "Native acoustic modes and dynamical placement remain open."),
    }

    out = project_root / "results" / "step_16_boundary_transport.json"
    out.write_text(json.dumps(ledger, indent=2))

    print_status(f"[A] imposed-wall peak z={z_pk:.3f}, "
                 f"wall probability={wall_fraction:.1%}, rms={zrms:.1f}", "PROCESS")
    print_status(f"[B] conditional angular ratio {ell_d:.0f}; "
                 "not a Silk damping prediction", "PROCESS")
    print_status(f"[C] conditional LTE x_e: "
                 f"{saha_rows[0]['x_e_saha_T_edge']:.3f}-"
                 f"{saha_rows[-1]['x_e_saha_T_edge']:.3f}", "PROCESS")
    print_status(f"[D] wall demand {rec_per_area:.1e}/cm2/s; "
                 f"trial supply margins {[round(r['margin_before_escape_or_absorption'], 5) for r in supply_rows]}", "PROCESS")
    print_status(f"[E] required Gamma drop {gam_wing/gam_trough:.1e}; "
                 f"neutral LyC mfp {mfp_lyc_cm/3.0857e24:.2f} Mpc", "PROCESS")
    print_status(f"[WRITE] {out}", "SUCCESS")
    return ledger


if __name__ == "__main__":
    run_step_16()
