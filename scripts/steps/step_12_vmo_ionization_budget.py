#!/usr/bin/env python3
"""
Step 12: Steady-State Ionization Budget of the VMO Branch

Closes the consistency question raised against the f_VMO ~ 0.994
low-metallicity IMF: its consequences for reionization, the CMB
electron-scattering optical depth (tau_reion ~ 0.054 under the LambdaCDM
decomposition), the star-formation history, and the background light.

In the eternal steady state there is no reionization epoch: the question
"did the stellar population reionize the universe in time" reduces to a
maintained rate balance — the ionizing emissivity that reaches the
diffuse medium must exceed the recombination rate, per baryon:

    supply   = xi * f_esc * N_gamma_eff     [photons per ISM baryon / Gyr]
    demand   = alpha_B(T) * n_e             [recombinations per baryon / Gyr]

with xi the fraction of gas cycled through stars per Gyr, f_esc the
Lyman-continuum escape fraction, and N_gamma_eff the IMF-weighted
ionizing yield per cycled baryon.

  (A) Ionizing yields per cycled baryon: metal-free very massive stars
      emit ~1e5 H-ionizing photons per stellar baryon (Tumlinson & Shull
      2000; Schaerer 2002), a standard metal-enriched IMF ~4e3; the
      f_VMO = 0.994 mixture gives N_gamma_eff ~ 1.0e5.
  (B) Recombination demand at the three fiducial electron densities of
      the opacity three-point requirement (n_e/n_b0 = 1, 14, 500).
  (C) Supply/demand margins over the (xi, f_esc) plane and the
      ionization-saturation density n_e,crit at which balance fails —
      the depth to which the ionized column required by the Global
      Opacity Theorem is actually sustained by the stellar budget.
  (D) Minimum f_VMO required to sustain ionization at each depth —
      quantifies whether the helium-driven requirement is excluded,
      unconstrained, or mildly favoured by the ionization sector.
  (E) The Thomson approach wing: under the corpus p = 0.5 horizon law
      at constant n_e = n_b0, the unit-optical-depth surface sits at
      z ~ 20 (Step 11 sigma_T row). The partial column accumulated in
      the optically thin approach — the TEP analogue of the LambdaCDM
      tau_reion datum — is tabulated, including mild density-rise
      profiles n_e ~ (1+z)^m, as the illustrative ordering pending the
      absorber-statistics inversion of the opacity programme.

VMO ionizing photons are emitted during the ~2-3 Myr main sequence,
before temporal-horizon formation sequesters the remnant; the horizon
traps the metal yield, not the already-emitted radiation. All processed
starlight enters the Step-11 thermalization bath regardless of spectral
hardness (achromatic shear invariance), so no separate background-light
budget arises. In the local f_VMO(Z) picture the branch shares no global
chronology, so no cosmic star-formation history is contradicted.

Outputs: results/gate12_vmo_ionization_budget.json
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
# Physical constants and corpus conventions (SI unless noted)
# ---------------------------------------------------------------------------
M_SUN_G = 1.98892e33                  # g
M_P_G = 1.67262192369e-24             # g
BARYONS_PER_MSUN = M_SUN_G / M_P_G    # 1.189e57
S_PER_GYR = 3.15576e16

N_B0_M3 = 0.251                       # corpus baryon density today (TEP-TH)
N_B0_CM3 = N_B0_M3 * 1e-6             # 2.51e-7 cm^-3
ALPHA_B = 2.59e-13                    # Case B, T = 1e4 K (Osterbrock & Ferland)

# Ionizing photon yields per stellar baryon (literature-anchored)
N_GAMMA_VMO = 1.0e5                   # metal-free VMOs: Tumlinson & Shull 2000,
                                      # Schaerer 2002 (top-heavy Z=0 IMFs)
N_GAMMA_VMO_LOW = 3.0e4               # conservative lower edge
N_GAMMA_STD = 4.0e3                   # standard metal-enriched IMF

F_VMO = 0.994                         # corpus requirement (Gate 6/8)
F_VMO_RANGE = (0.975, 0.995)          # helium-compatible range (step_06 scan)

# Steady-state processing parameters (scanned, not fitted)
XI_GRID = [1e-3, 1e-2, 1e-1, 1.0]     # gas-cycling fraction per Gyr
F_ESC_GRID = [0.01, 0.1, 0.5]         # Lyman-continuum escape fraction

# Three-point electron-density requirement (opacity section):
# n_e rises ~14x by z ~ 7 and ~500x by the last-scattering-depth scale.
DEPTH_REQUIREMENTS = {'today': 1.0, 'z~7': 14.0, 'LSS_depth': 500.0}

# Thomson column per Hubble-radius unit path at constant n_b0
# (Step 11, sigma_T/m_p = 0.397 cm^2/g row of the thermalization ledger)
TAU_PER_L0 = 2.2026e-3


def n_gamma_eff(f_vmo):
    """IMF-mixed ionizing yield per cycled baryon."""
    return f_vmo * N_GAMMA_VMO + (1.0 - f_vmo) * N_GAMMA_STD


def run_step_12():
    setup_step_logger(Path(__file__).stem)
    print_status("=== STEP 12: VMO-BRANCH IONIZATION-EQUILIBRIUM BUDGET ===",
                 "SUCCESS")

    # ------------------------------------------------------------------
    # (A) Ionizing yields
    # ------------------------------------------------------------------
    yields = {
        'N_gamma_VMO_per_baryon': N_GAMMA_VMO,
        'N_gamma_VMO_per_baryon_low_edge': N_GAMMA_VMO_LOW,
        'N_gamma_VMO_per_Msun': N_GAMMA_VMO * BARYONS_PER_MSUN,
        'N_gamma_std_per_baryon': N_GAMMA_STD,
        'N_gamma_std_per_Msun': N_GAMMA_STD * BARYONS_PER_MSUN,
        'yield_ratio_VMO_over_std': N_GAMMA_VMO / N_GAMMA_STD,
        'N_gamma_eff_at_f_vmo_0p994': n_gamma_eff(F_VMO),
        'N_gamma_eff_at_f_vmo_0p975': n_gamma_eff(F_VMO_RANGE[0]),
        'note': ('H-ionizing photons emitted per stellar baryon over the '
                 'main sequence, before temporal-horizon formation '
                 'sequesters the remnant: ~1e5 for metal-free very '
                 'massive stars (Tumlinson & Shull 2000; Schaerer 2002, '
                 'top-heavy Z=0 IMFs; conservative low edge 3e4) versus '
                 '~4e3 for a standard metal-enriched IMF. At f_VMO = '
                 '0.994 the effective yield is dominated by the VMO '
                 'channel: ~9.96e4 photons per cycled baryon.')
    }

    # ------------------------------------------------------------------
    # (B) Recombination demand per baryon at fiducial depths
    # ------------------------------------------------------------------
    demand = {}
    for tag, mult in DEPTH_REQUIREMENTS.items():
        n_e = N_B0_CM3 * mult
        per_s = ALPHA_B * n_e
        demand[tag] = {
            'n_e_over_n_b0': mult,
            'n_e_cm^-3': n_e,
            'recomb_per_baryon_per_s': per_s,
            'recomb_per_baryon_per_Gyr': per_s * S_PER_GYR,
        }

    # ------------------------------------------------------------------
    # (C) Margin grid and ionization-saturation depth
    # ------------------------------------------------------------------
    def margins(f_vmo):
        n_eff = n_gamma_eff(f_vmo)
        grid = []
        for xi in XI_GRID:
            for f_esc in F_ESC_GRID:
                supply = xi * f_esc * n_eff            # per baryon per Gyr
                n_e_crit = supply / (ALPHA_B * S_PER_GYR)
                grid.append({
                    'xi_per_Gyr': xi,
                    'f_esc': f_esc,
                    'supply_per_baryon_per_Gyr': supply,
                    'margin_at_1x': supply / demand['today']['recomb_per_baryon_per_Gyr'],
                    'margin_at_14x': supply / demand['z~7']['recomb_per_baryon_per_Gyr'],
                    'margin_at_500x': supply / demand['LSS_depth']['recomb_per_baryon_per_Gyr'],
                    'n_e_crit_cm^-3': n_e_crit,
                    'n_e_crit_over_n_b0': n_e_crit / N_B0_CM3,
                })
        return grid

    grid_vmo = margins(F_VMO)
    grid_std = margins(0.0)

    def summary(grid):
        crits = [g['n_e_crit_over_n_b0'] for g in grid]
        m500 = [g['margin_at_500x'] for g in grid]
        return {
            'n_e_crit_over_n_b0_min': min(crits),
            'n_e_crit_over_n_b0_max': max(crits),
            'margin_500x_min': min(m500),
            'margin_500x_max': max(m500),
            'cells_above_500x_requirement': int(sum(c >= 500.0 for c in crits)),
            'n_cells': len(crits),
        }

    ledger_C = {
        'vmo_branch_grid': grid_vmo,
        'standard_branch_grid': grid_std,
        'vmo_branch_summary': summary(grid_vmo),
        'standard_branch_summary': summary(grid_std),
        'note': ('supply = xi f_esc N_gamma_eff per ISM baryon per Gyr; '
                 'demand = alpha_B n_e. The balance point n_e,crit is the '
                 'depth to which the diffuse column stays ionized. The '
                 'VMO branch sustains ionization to ~5e2-2e7 x n_b0 '
                 'across the scanned plane, straddling the ~500x rise '
                 'required at the opacity-boundary depth; the standard '
                 'branch saturates ~25x shallower, failing the deepest '
                 'requirement at the conservative corner. Ionization is '
                 'a maintained equilibrium, not an epoch: the ionized '
                 'column the opacity theorem requires is supplied by the '
                 'same stellar budget, with the VMO-enhanced yield the '
                 'factor that reaches the required depth under '
                 'pessimistic escape/cycling.')
    }

    # ------------------------------------------------------------------
    # (D) Minimum f_VMO to sustain ionization at the 500x depth
    # ------------------------------------------------------------------
    f_min_rows = []
    for xi in XI_GRID:
        for f_esc in F_ESC_GRID:
            n_req = (demand['LSS_depth']['recomb_per_baryon_per_Gyr']
                     / (xi * f_esc))
            f_min = (n_req - N_GAMMA_STD) / (N_GAMMA_VMO - N_GAMMA_STD)
            f_min_rows.append({
                'xi_per_Gyr': xi,
                'f_esc': f_esc,
                'N_gamma_required_per_baryon': n_req,
                'f_VMO_min_at_500x': float(np.clip(f_min, 0.0, np.inf)),
                'sustainable_even_at_f_VMO_1': bool(n_req <= N_GAMMA_VMO),
                'standard_suffices': bool(N_GAMMA_STD >= n_req),
            })

    ledger_D = {
        'requirement_depth': 'n_e = 500 x n_b0 (opacity-boundary depth)',
        'grid': f_min_rows,
        'note': ('f_VMO_min solves xi f_esc [f N_VMO + (1-f) N_std] = '
                 'alpha_B n_e. Over most of the plane the standard yield '
                 'already suffices at this depth (f_VMO_min = 0): the '
                 'ionization sector adds no countervailing bound on the '
                 'helium requirement. Toward the conservative corner '
                 '(xi <= 1e-2/Gyr and f_esc <= 0.1) f_VMO_min rises to '
                 '~0.07-1.0, and at the extreme corner (xi = 1e-3/Gyr, '
                 'f_esc = 0.01) the 500x depth is marginal even at '
                 'f_VMO = 1 (97% of the requirement). The constraint '
                 'therefore directionally favours the high-VMO branch '
                 'the helium fixed point requires — supportive, not '
                 'exclusionary.')
    }

    # ------------------------------------------------------------------
    # (E) Thomson approach wing (illustrative baseline)
    # ------------------------------------------------------------------
    def tau_wing(z, m):
        """tau_Th(z) = sigma_T n_b0 (1+z)^m ell0 [(1+z)^2 - 1] law,
        i.e. tau = TAU_PER_L0 * 2/(m+2) * [(1+z)^(m+2) - 1]."""
        return TAU_PER_L0 * 2.0 / (m + 2.0) * ((1.0 + z) ** (m + 2.0) - 1.0)

    wing_rows = []
    for m in [0.0, 0.5, 1.0]:
        # surface depth z_L where tau = 1 under this profile
        z_L = (1.0 + (m + 2.0) / (2.0 * TAU_PER_L0)) ** (1.0 / (m + 2.0)) - 1.0
        wing_rows.append({
            'density_rise_m': m,
            'z_surface_tau_1': float(z_L),
            'tau_at_z_1': float(tau_wing(1.0, m)),
            'tau_at_z_3': float(tau_wing(3.0, m)),
            'tau_at_z_4': float(tau_wing(4.0, m)),
            'tau_at_z_5': float(tau_wing(5.0, m)),
            'tau_at_z_7': float(tau_wing(7.0, m)),
        })

    ledger_E = {
        'tau_per_Hubble_radius_constant_n_b0': TAU_PER_L0,
        'observed_tau_reion_LCDM': 0.054,
        'profiles': wing_rows,
        'note': ('Under the p = 0.5 horizon law at constant n_e = n_b0 '
                 'the Thomson tau = 1 surface sits at z ~ 20 (the Step-11 '
                 'sigma_T row), and the partial column accumulated in '
                 'the optically thin approach is ~0.053 by z ~ 4 — the '
                 'Planck tau_reion = 0.054 magnitude. A mild density '
                 'rise (m = 0.5) reaches the same wing amplitude by '
                 'z ~ 3 with the tau = 1 surface at z ~ 11.6; the '
                 'observed wing therefore selects a near-flat to '
                 'mildly-rising approach profile. The low-EE wing is '
                 'the approach column of the single opacity boundary, '
                 'not evidence of a discrete reionization epoch; its '
                 'precise amplitude is a datum on the n_e(ell) approach '
                 'profile, owned by the absorber-statistics inversion '
                 'of the opacity programme (three-point requirement).')
    }

    # ------------------------------------------------------------------
    # (F) Qualitative closures
    # ------------------------------------------------------------------
    ledger_F = {
        'star_formation_history': ('None to contradict: the VMO branch is '
                                   'a metallicity-selected channel '
                                   '(Z < Z_crit ~ 1e-4) that is local and '
                                   'asynchronous across patches; in the '
                                   'eternal steady state there is no '
                                   'global Pop III chronology.'),
        'background_light': ('All processed starlight — including the '
                             'hard VMO spectrum — enters the Step-11 '
                             'thermalization bath; the divergent column '
                             'reprocesses any input spectrum into the '
                             'blackbody (achromatic shear invariance), '
                             'so no separate EBL budget arises.'),
        'photon_escape': ('VMO ionizing radiation is emitted over the '
                          '~2-3 Myr main sequence before core collapse '
                          'forms the temporal horizon; the horizon '
                          'sequesters the metal-bearing remnant, not '
                          'the emitted radiation field.'),
        'depth_correlation': ('Where the demand is highest (deep, dense '
                              'sightlines), patches are youngest and '
                              'most metal-poor, so the local f_VMO(Z) '
                              'transition concentrates the enhanced '
                              'VMO yield exactly where the 500x '
                              'recombination demand applies.')
    }

    verdict = ('Steady-state ionization balance closes: the f_VMO = 0.994 '
               'branch sustains the ionized diffuse column to '
               'n_e ~ 5e2-2e7 x n_b0 across the scanned (xi, f_esc) '
               'plane — bracketing the ~500x rise the opacity boundary '
               'requires — so the reionization/optical-depth sector adds '
               'no countervailing bound on the helium-driven VMO '
               'fraction and mildly favours it at the conservative '
               'corner. The tau_reion = 0.054 datum is the approach '
               'wing of the single opacity boundary (constant-density '
               'baseline: tau ~ 0.05 accumulated by z ~ 4), with its '
               'profile-shape content assigned to the absorber '
               'inversion, not an epoch budget the VMO population must '
               'meet.')

    ledger = {
        'step': 'step_12_vmo_ionization_budget',
        'A_ionizing_yields': yields,
        'B_recombination_demand': demand,
        'C_margin_grid': ledger_C,
        'D_f_vmo_min': ledger_D,
        'E_thomson_wing': ledger_E,
        'F_qualitative_closures': ledger_F,
        'verdict': verdict,
    }

    out = project_root / 'results' / 'gate12_vmo_ionization_budget.json'
    with open(out, 'w') as f:
        json.dump(ledger, f, indent=2)

    sv = ledger_C['vmo_branch_summary']
    ss = ledger_C['standard_branch_summary']
    print_status(f"[A] N_gamma_eff(f_VMO=0.994) = "
                 f"{yields['N_gamma_eff_at_f_vmo_0p994']:.2e}/baryon "
                 f"(std-only {N_GAMMA_STD:.1e})", "SUCCESS")
    for tag, d in demand.items():
        print_status(f"[B] n_e={d['n_e_over_n_b0']:.0f}x n_b0 -> demand "
                     f"{d['recomb_per_baryon_per_Gyr']:.2e}/baryon/Gyr",
                     "PROCESS")
    print_status(f"[C] VMO branch ionized to "
                 f"({sv['n_e_crit_over_n_b0_min']:.1e}.."
                 f"{sv['n_e_crit_over_n_b0_max']:.1e}) x n_b0; "
                 f"cells meeting 500x requirement: "
                 f"{sv['cells_above_500x_requirement']}/{sv['n_cells']}",
                 "SUCCESS")
    print_status(f"[C] Standard branch ionized to "
                 f"({ss['n_e_crit_over_n_b0_min']:.1e}.."
                 f"{ss['n_e_crit_over_n_b0_max']:.1e}) x n_b0; "
                 f"cells meeting 500x requirement: "
                 f"{ss['cells_above_500x_requirement']}/{ss['n_cells']}",
                 "PROCESS")
    print_status(f"[E] Wing: tau(z<4)={wing_rows[0]['tau_at_z_4']:.3f}, "
                 f"tau=1 surface z={wing_rows[0]['z_surface_tau_1']:.1f} "
                 f"(m=0 baseline; Planck tau_reion = 0.054)", "SUCCESS")
    print_status(f"[WRITE] {out}", "SUCCESS")
    return ledger


if __name__ == "__main__":
    run_step_12()
