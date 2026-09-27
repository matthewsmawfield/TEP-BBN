#!/usr/bin/env python3
"""
Step 11: Steady-State Timescale and Thermalization Budget

Closes the quantitative ledger for the eternal-universe equilibrium claims
inherited by Paper 0 §8:

  (A) Chemical-equilibrium convergence: the linear GCE map of Gate 6/8,
      dY/dt = (p_Y - (1-R)Y)/tau*, has contraction rate (1-R)/tau*.
      Reports the e-folding time and the number of star-formation
      timescales required to reach 1% and 0.1% of the asymptotic
      abundances from the extreme initial conditions used in Gate 6.

  (B) Thermalization depth: in the static spatial geometry the absorbing
      column is unbounded (Step 07 path-length divergence). With the
      corpus baryon density n_b = 0.251 m^-3 and per-gas-mass absorptivity
      kappa spanning the observationally constrained interstellar-dust
      range at mm/sub-mm wavelengths, the temporal depth z_therm at which
      tau_abs = 1 is computed under both horizon path-length laws tested
      in Step 07 (exponential and power-law p = 0.5).

  (C) Sequestration ledger: per-generation lockup fraction, metal escape
      accounting, and the astration-exposure convergence condition
      p + q > 1 from Gate 8.

Outputs: results/gate11_steady_state_budget.json
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
# Physical constants and corpus conventions (SI)
# ---------------------------------------------------------------------------
C_KM_S = 299792.458
H0_KM_S_MPC = 70.0                    # corpus convention (TEP-TH th_common)
MPC_CM = 3.085677581e24
M_P_G = 1.67262192369e-24             # proton mass, g
N_B0_M3 = 0.251                       # baryon density today, m^-3 (TEP-TH)
SIGMA_T_OVER_MP = 0.397               # Thomson opacity per gas mass, cm^2/g

# Gate 6/8 chemical-evolution parameters (single source of truth)
R = 0.4                               # return fraction
P_Y_STD, P_Z_STD = 0.02, 0.01
P_Y_VMO, P_Z_VMO = 0.149, 0.0
F_VMO = 0.994
TAU_STAR = 1.0                        # star-formation timescale unit

# Dust absorptivity per gas mass at CMB-peak wavelengths (mm/sub-mm).
# Range brackets Planck-collaboration dust emissivity scaled by a
# Galactic-order dust-to-gas ratio: ~1e-2 cm^2/g at 250 um down to
# ~1e-4 cm^2/g toward the Rayleigh-Jeans tail of a 2.7 K spectrum.
KAPPA_RANGE = [1e-2, 1e-3, 1e-4]


def run_step_11():
    setup_step_logger(Path(__file__).stem)
    print_status("=== STEP 11: STEADY-STATE TIMESCALE & THERMALIZATION BUDGET ===",
                 "SUCCESS")

    # ------------------------------------------------------------------
    # (A) Equilibrium convergence ledger
    # ------------------------------------------------------------------
    p_Y_eff = F_VMO * P_Y_VMO + (1 - F_VMO) * P_Y_STD
    p_Z_eff = (1 - F_VMO) * P_Z_STD
    Y_eq = p_Y_eff / (1 - R)
    Z_eq = p_Z_eff / (1 - R)

    rate = (1 - R) / TAU_STAR                      # contraction rate
    t_efold = 1.0 / rate                           # tau* units

    # Worst-case initial residual across the Gate-6 initial conditions
    ic_resid = max(abs(0.80 - Y_eq), abs(0.50 - Y_eq), abs(0.00 - Y_eq))

    def t_to_residual(frac):
        """tau* units for residual to fall to frac x Y_eq."""
        target = frac * Y_eq
        return np.log(ic_resid / target) / rate

    ledger_A = {
        'fixed_point': {'Y_eq': Y_eq, 'Z_eq': Z_eq,
                        'Y_observed': 0.245,
                        'Y_over_observed': Y_eq / 0.245},
        'contraction_rate_per_tau_star': rate,
        'e_folding_tau_star': t_efold,
        'worst_initial_residual': ic_resid,
        'tau_star_to_1pct': float(t_to_residual(0.01)),
        'tau_star_to_0p1pct': float(t_to_residual(0.001)),
        'tau_star_to_1pct_Gyr_at_1Gyr': float(t_to_residual(0.01)),
        'note': ('Linear map contracts every species at rate (1-R)/tau*. '
                 'The equilibrium is reached in ~9 tau* to 1% from the '
                 'extremes tested in Gate 6; in an eternal universe the '
                 'required processing time is unbounded, so the attractor '
                 'is reached with exponential certainty.')
    }

    # ------------------------------------------------------------------
    # (B) Thermalization depth: tau_abs(z) = rho_b * kappa * ell(z)
    # ------------------------------------------------------------------
    rho_b = N_B0_M3 * 1e-6 * M_P_G                    # g/cm^3
    ell_0_cm = C_KM_S / H0_KM_S_MPC * MPC_CM          # c/H0
    col_per_ell0 = rho_b * ell_0_cm                   # g/cm^2 per Hubble radius

    rows = []
    for kappa in KAPPA_RANGE + [SIGMA_T_OVER_MP]:
        tau_per_ell0 = col_per_ell0 * kappa           # tau per Hubble radius
        ell_req = 1.0 / tau_per_ell0                  # in ell_0 units
        # power-law horizon law (Step 07): ell = ell0 [(1+z)^(1/p) - 1], p=0.5
        p = 0.5
        z_pl = (1.0 + ell_req) ** p - 1.0
        # exponential law: ell = ell0 ln(1+z)  (ln(1+z) required = ell_req)
        z_exp = float(np.exp(ell_req)) if ell_req < 700 else float('inf')
        rows.append({
            'kappa_cm2_per_g': kappa,
            'tau_per_Hubble_radius': tau_per_ell0,
            'ell_req_Hubble_radii': ell_req,
            'z_therm_powerlaw_p0p5': float(z_pl),
            'z_therm_exponential': z_exp,
            'z_therm_exponential_ln1pz': float(ell_req)
        })

    ledger_B = {
        'n_b0_m^-3': N_B0_M3,
        'rho_b_g_cm^-3': rho_b,
        'ell_0_cm_c_over_H0': ell_0_cm,
        'column_per_Hubble_radius_g_cm^-2': col_per_ell0,
        'channels': rows,
        'note': ('tau_abs accumulates along the divergent comoving path of '
                 'Step 07. For the interstellar-dust absorptivity range '
                 '(1e-4..1e-2 cm^2/g at mm wavelengths) the unit-optical-'
                 'depth surface sits at z ~ 130-1300 under the power-law '
                 'horizon law (p = 0.5); the exponential law reaches the '
                 'same column at exponentially larger but finite z. In '
                 'all cases tau -> infinity at the horizon, so full '
                 'reprocessing of distributed starlight into a blackbody '
                 'is a theorem of the path geometry, with the timescale '
                 'free because coordinate time is unbounded.')
    }

    # ------------------------------------------------------------------
    # (C) Sequestration / baryon ledger
    # ------------------------------------------------------------------
    ledger_C = {
        'return_fraction_R': R,
        'locked_fraction_per_tau_star': 1 - R,
        'metal_escape_fraction_E_Z': P_Z_VMO,
        'effective_metal_yield': p_Z_eff,
        'Z_eq': Z_eq,
        'astration_convergence': {
            'p': 0.5, 'q': 0.8, 'p_plus_q': 1.3,
            'condition': 'p + q > 1 => E_astr finite',
            'satisfied': True},
        'note': ('Baryon exhaustion is prevented by the open-box steady '
                 'state (infall/sequestration balance, M_g constant); '
                 'metal overproduction is prevented by temporal-horizon '
                 'sequestration of VMO yields (E_Z = 0 in the dominant '
                 'f_VMO = 0.994 channel); total astration exposure is '
                 'finite by the p + q > 1 condition of Gate 8.')
    }

    # ------------------------------------------------------------------
    # Ledger output
    # ------------------------------------------------------------------
    ledger = {
        'step': 'step_11_steady_state_budget',
        'A_equilibrium_convergence': ledger_A,
        'B_thermalization_depth': ledger_B,
        'C_sequestration_ledger': ledger_C,
        'verdict': ('Steady-state budget closes: abundances converge to '
                    'Y_eq = 0.2470, Z_eq = 1.0e-4 in ~9 star-formation '
                    'timescales; absorption optical depth reaches unity '
                    'at finite temporal depth (z ~ 130-1300, power-law '
                    'branch) and diverges at the horizon; sequestration '
                    'keeps the metal asymptote at the observed floor.')
    }

    out = project_root / 'results' / 'gate11_steady_state_budget.json'
    with open(out, 'w') as f:
        json.dump(ledger, f, indent=2)

    print_status(f"\n[A] Equilibrium: Y_eq={Y_eq:.4f} (obs 0.245), "
                 f"Z_eq={Z_eq:.1e}; 1% convergence in "
                 f"{ledger_A['tau_star_to_1pct']:.1f} tau*", "SUCCESS")
    for r in rows:
        print_status(f"[B] kappa={r['kappa_cm2_per_g']:.0e} cm^2/g -> "
                     f"z_therm (p=0.5) = {r['z_therm_powerlaw_p0p5']:.0f}, "
                     f"ln(1+z) exp-law = {r['z_therm_exponential_ln1pz']:.0f}",
                     "PROCESS")
    print_status("[C] Sequestration: E_Z=0 in dominant channel; "
                 "p+q=1.3>1 satisfied", "SUCCESS")
    print_status(f"[WRITE] {out}", "SUCCESS")
    return ledger


if __name__ == "__main__":
    run_step_11()
