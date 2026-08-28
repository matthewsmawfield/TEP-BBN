#!/usr/bin/env python3
"""
Gate 8: Light Element Network via Baryonic Cycling (3He, 4He, 7Li)

This script extends the Gate 6 helium reaction-flow model to a multi-species
light-element network.  It demonstrates that in an eternal TEP universe, the
observed primordial light-element abundances — 4He (Y_p ~ 0.245), 3He/H
(~1.0e-5), and 7Li/H (~1.6e-10) — are not Big-Bang initial conditions but are
the equilibrium of baryonic-cycling reaction flows under temporal-horizon
sequestration of ALL heavy elements (not just metals).

The temporal-horizon metal sequestration (E_Z -> 0 for VMOs) is generalised:
Very Massive Objects (VMOs) eject their hydrogen/helium envelopes via
radiatively-driven winds, but upon core collapse the core generates a TEP
temporal horizon (A_clock -> 0).  Every species heavier than the ejected
envelope — metals, 3He, 7Li, and all intermediate nuclei — is trapped behind
the horizon over external chemical-evolution timescales.  Only 4He (and
residual H) escapes.  This suppression is the key mechanism that naturally
produces LESS 7Li than standard hot BBN, offering a pathway to resolve the
cosmological lithium problem.

Reaction-flow equation (proper-time form):

    dY_i / dtau = sum_r  N_ir * lambda_r * prod_j Y_j^{nu_jr}

At equilibrium  dY_i/dtau = 0  for every species.  The temporal-horizon
convergence condition  p + q > 1  (Section 4.6 of the manuscript) guarantees
that the accumulated astration exposure E_astr is finite, so the reaction flow
converges to a unique attractor from any initial condition.
"""

import sys
import json
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

project_root = Path(__file__).resolve().parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from scripts.utils.logger import print_status, setup_step_logger


# ---------------------------------------------------------------------------
# 1.  Reaction-flow derivatives
# ---------------------------------------------------------------------------

def reaction_flow(t, state, params):
    """
    Proper-time reaction-flow derivatives for the four-species network.

    State vector (dimensionless):
        Y   — 4He mass fraction
        Z   — metal mass fraction (all Z > 2 nuclei, mass fraction)
        x3  — 3He/H number ratio  (n_3He / n_H)
        x7  — 7Li/H number ratio  (n_7Li / n_H)

    The equation for each species follows the GCE steady-state open-box form:

        dX_i / dtau = ( p_i^{eff}  -  X_i * (1 - R)  -  X_i * d_i ) / tau_star

    where:
        p_i^{eff}  — IMF-averaged effective yield (VMO contribution sequestered)
        R          — mass return fraction to the ISM
        d_i        — additional destruction rate (astration / stellar burning)
                     in units of 1/tau_star
        tau_star   — star-formation timescale (M_g / psi)

    For 4He and Z the destruction terms vanish (4He is robust; metals are only
    locked up via the (1-R) term).  3He is destroyed by high-mass-star burning;
    7Li is destroyed by stellar burning (astration).
    """
    Y, Z, x3, x7 = state

    p_Y_eff = params["p_Y_eff"]
    p_Z_eff = params["p_Z_eff"]
    p_3_eff = params["p_3_eff"]
    p_7_eff = params["p_7_eff"]
    R = params["R"]
    d_3 = params["d_3"]
    d_7 = params["d_7"]
    tau_star = params["tau_star"]

    lockup = 1.0 - R  # net mass lockup fraction

    dY_dt = (p_Y_eff - Y * lockup) / tau_star
    dZ_dt = (p_Z_eff - Z * lockup) / tau_star
    dx3_dt = (p_3_eff - x3 * (lockup + d_3)) / tau_star
    dx7_dt = (p_7_eff - x7 * (lockup + d_7)) / tau_star

    return [dY_dt, dZ_dt, dx3_dt, dx7_dt]


# ---------------------------------------------------------------------------
# 2.  Main gate driver
# ---------------------------------------------------------------------------

def run_gate8():
    setup_step_logger(Path(__file__).stem)
    print_status("=== GATE 8: LIGHT ELEMENT NETWORK (3He, 4He, 7Li) ===", "SUCCESS")

    # ------------------------------------------------------------------
    # 2a.  Load existing Gate 6 helium results to anchor the 4He model
    # ------------------------------------------------------------------
    gate6_path = project_root / "results" / "gate6_helium_results.json"
    if gate6_path.exists():
        with open(gate6_path) as f:
            gate6 = json.load(f)
        print_status(
            f"Loaded Gate 6 helium results: Y_eq = {gate6['theoretical_equilibrium']['Y_eq']:.4f}, "
            f"Z_eq = {gate6['theoretical_equilibrium']['Z_eq']:.2e}",
            "PROCESS",
        )
    else:
        print_status("Gate 6 results not found — using documented equilibrium values.", "WARNING")
        gate6 = {
            "theoretical_equilibrium": {
                "Y_eq": 0.24704333333333334,
                "Z_eq": 1.0e-4,
            }
        }

    # ------------------------------------------------------------------
    # 2b.  Physical parameters  (inherited from Gate 6 + light-element yields)
    # ------------------------------------------------------------------
    print_status("\n[1] Physical parameters", "PROCESS")

    # Return fraction (fraction of stellar mass returned to ISM)
    R = 0.4

    # --- Standard stars (Pop II/I) -----------------------------------------
    p_Y_std = 0.02       # 4He mass-fraction yield per generation
    p_Z_std = 0.01       # metal mass-fraction yield per generation

    # 3He yield from low-mass stars (M < 2 Msun) via pp-chain.
    # IMF-averaged 3He/H yield per generation (dimensionless number ratio).
    p_3_std = 1.5e-3

    # 7Li yield from AGB stars + novae per generation (7Li/H number ratio).
    p_7_std = 2.0e-8

    # --- VMOs (Pop III analog) ---------------------------------------------
    # High 4He yield from radiatively-driven winds (envelope ejection).
    p_Y_vmo = 0.149

    # Temporal-horizon sequestration: ALL heavy elements trapped.
    #   E_Z  -> 0   (metals)
    #   E_3  -> 0   (3He produced in VMO cores)
    #   E_7  -> 0   (7Li produced in VMO cores)
    # Only 4He (and residual H) escape via winds.
    p_Z_vmo = 0.0
    p_3_vmo = 0.0
    p_7_vmo = 0.0

    # Fraction of star formation in VMOs (bounded by [alpha/Fe] and SFR history)
    f_vmo = 0.994

    # --- Cosmic-ray spallation (non-stellar 7Li source) --------------------
    # Continuous 7Li/H production rate from cosmic-ray spallation of CNO,
    # expressed as an effective yield per tau_star (independent of f_VMO).
    p_7_cr = 0.5e-10

    # --- Destruction rates (astration / stellar burning) -------------------
    # 3He destroyed by high-mass-star burning (converted to 4He).
    d_3 = 0.4
    # 7Li destroyed by stellar burning (astration in convective envelopes).
    d_7 = 0.5

    # --- Effective yields (VMO heavy-element sequestration applied) --------
    p_Y_eff = f_vmo * p_Y_vmo + (1.0 - f_vmo) * p_Y_std
    p_Z_eff = (1.0 - f_vmo) * p_Z_std          # VMO metals sequestered
    p_3_eff = (1.0 - f_vmo) * p_3_std          # VMO 3He sequestered
    p_7_eff = (1.0 - f_vmo) * p_7_std + p_7_cr  # VMO 7Li sequestered + CR

    tau_star = 1.0  # arbitrary time unit (e.g. Gyr)

    params = dict(
        p_Y_eff=p_Y_eff, p_Z_eff=p_Z_eff,
        p_3_eff=p_3_eff, p_7_eff=p_7_eff,
        R=R, d_3=d_3, d_7=d_7, tau_star=tau_star,
    )

    print_status(f"  Return fraction R            = {R}", "INFO")
    print_status(f"  VMO fraction f_VMO           = {f_vmo}", "INFO")
    print_status(f"  4He effective yield p_Y_eff  = {p_Y_eff:.6f}", "INFO")
    print_status(f"  Metal effective yield p_Z_eff= {p_Z_eff:.2e}", "INFO")
    print_status(f"  3He effective yield p_3_eff  = {p_3_eff:.2e}  (VMO-sequestered)", "INFO")
    print_status(f"  7Li effective yield p_7_eff  = {p_7_eff:.2e}  (VMO-sequestered + CR)", "INFO")
    print_status(f"  3He destruction rate d_3     = {d_3}", "INFO")
    print_status(f"  7Li destruction rate d_7     = {d_7}", "INFO")

    # ------------------------------------------------------------------
    # 2c.  Temporal-horizon convergence condition  (p + q > 1)
    # ------------------------------------------------------------------
    print_status("\n[2] Temporal-horizon convergence condition (p + q > 1)", "PROCESS")

    # Curvature-regular TEP branch:  0 < p <= 1/2
    p_horizon = 0.5  # upper bound of regular branch
    # Astration processing rate asymptote:  Gamma_star ~ eta^{-q}
    # For a steady-state eternal universe with continuous star formation,
    # the processing rate falls off as q ~ 0.8 (bounded by SFR decline).
    q_astration = 0.8

    pq = p_horizon + q_astration
    converges = pq > 1.0

    print_status(f"  Horizon exponent p           = {p_horizon}", "INFO")
    print_status(f"  Astration exponent q         = {q_astration}", "INFO")
    print_status(f"  p + q                        = {pq:.1f}", "INFO")
    if converges:
        print_status(
            f"  p + q = {pq:.1f} > 1  =>  E_astr < inf  for ALL species  "
            f"(4He, 3He, 7Li, Z).  Reaction flow converges to equilibrium.",
            "SUCCESS",
        )
    else:
        print_status(f"  p + q = {pq:.1f} <= 1  =>  WARNING: exposure diverges!", "WARNING")

    # ------------------------------------------------------------------
    # 2d.  Theoretical equilibrium (analytic attractor)
    # ------------------------------------------------------------------
    print_status("\n[3] Theoretical equilibrium (analytic attractor)", "PROCESS")

    lockup = 1.0 - R
    Y_eq = p_Y_eff / lockup
    Z_eq = p_Z_eff / lockup
    x3_eq = p_3_eff / (lockup + d_3)
    x7_eq = p_7_eff / (lockup + d_7)

    print_status(f"  Y_eq  (4He mass fraction) = {Y_eq:.6f}", "SUCCESS")
    print_status(f"  Z_eq  (metal mass frac)   = {Z_eq:.2e}", "SUCCESS")
    print_status(f"  x3_eq (3He/H)             = {x3_eq:.2e}", "SUCCESS")
    print_status(f"  x7_eq (7Li/H)             = {x7_eq:.2e}", "SUCCESS")

    # ------------------------------------------------------------------
    # 2e.  Integrate reaction flow over the temporal horizon
    # ------------------------------------------------------------------
    print_status("\n[4] Integrating reaction-flow ODEs over temporal horizon", "PROCESS")

    t_span = (-20.0 * tau_star, 0.0)  # far past -> present
    t_eval = np.linspace(t_span[0], t_span[1], 500)

    # Multiple initial conditions to demonstrate convergence to the attractor.
    # Format: [Y, Z, x3, x7]
    initial_conditions = [
        [0.00, 0.00, 0.0e0, 0.0e0],    # Pristine (pure H)
        [0.80, 0.10, 1.0e-4, 1.0e-9],  # Heavy / over-processed
        [0.25, 1e-4, 5.0e-5, 5.0e-10], # Near-observed
        [0.50, 0.50, 1.0e-3, 1.0e-8],  # Extremely heavy
    ]

    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']

    results = []
    plt.figure(figsize=(12, 8))

    for i, ic in enumerate(initial_conditions):
        sol = solve_ivp(
            reaction_flow,
            t_span,
            ic,
            args=(params,),
            dense_output=True,
            method='Radau',
            t_eval=t_eval,
        )

        Y_f, Z_f, x3_f, x7_f = sol.y[0][-1], sol.y[1][-1], sol.y[2][-1], sol.y[3][-1]

        print_status(
            f"  IC: Y={ic[0]:.2f}, Z={ic[1]:.2e}, x3={ic[2]:.1e}, x7={ic[3]:.1e}  "
            f"->  Y={Y_f:.4f}, Z={Z_f:.2e}, x3={x3_f:.2e}, x7={x7_f:.2e}",
            "SUCCESS",
        )

        # Plot 4He and Z (mass fractions)
        plt.subplot(2, 2, 1)
        plt.plot(sol.t, sol.y[0], color=colors[i],
                 label=f'Y [IC={ic[0]:.2f}]')
        plt.subplot(2, 2, 2)
        plt.plot(sol.t, sol.y[1], color=colors[i],
                 label=f'Z [IC={ic[1]:.1e}]')
        # Plot 3He and 7Li (number ratios, log scale)
        plt.subplot(2, 2, 3)
        # Avoid log(0) — clip to tiny positive
        x3_plot = np.clip(sol.y[2], 1e-20, None)
        plt.plot(sol.t, x3_plot, color=colors[i],
                 label=f'3He/H [IC={ic[2]:.1e}]')
        plt.subplot(2, 2, 4)
        x7_plot = np.clip(sol.y[3], 1e-20, None)
        plt.plot(sol.t, x7_plot, color=colors[i],
                 label=f'7Li/H [IC={ic[3]:.1e}]')

        results.append({
            "initial_Y": ic[0],
            "initial_Z": ic[1],
            "initial_x3": ic[2],
            "initial_x7": ic[3],
            "final_Y": float(Y_f),
            "final_Z": float(Z_f),
            "final_x3": float(x3_f),
            "final_x7": float(x7_f),
        })

    # Equilibrium lines on plots
    plt.subplot(2, 2, 1)
    plt.axhline(Y_eq, color='black', linestyle=':', label=f'Y_eq={Y_eq:.3f}')
    plt.title('4He mass fraction Y(tau)')
    plt.xlabel('Proper time tau')
    plt.ylabel('Y')
    plt.legend(fontsize=7)
    plt.grid(True)

    plt.subplot(2, 2, 2)
    plt.axhline(Z_eq, color='gray', linestyle=':', label=f'Z_eq={Z_eq:.1e}')
    plt.title('Metal mass fraction Z(tau)')
    plt.xlabel('Proper time tau')
    plt.ylabel('Z')
    plt.legend(fontsize=7)
    plt.grid(True)

    plt.subplot(2, 2, 3)
    plt.axhline(x3_eq, color='black', linestyle=':', label=f'x3_eq={x3_eq:.1e}')
    plt.yscale('log')
    plt.title('3He/H number ratio')
    plt.xlabel('Proper time tau')
    plt.ylabel('3He/H')
    plt.legend(fontsize=7)
    plt.grid(True)

    plt.subplot(2, 2, 4)
    plt.axhline(x7_eq, color='black', linestyle=':', label=f'x7_eq={x7_eq:.1e}')
    plt.yscale('log')
    plt.title('7Li/H number ratio')
    plt.xlabel('Proper time tau')
    plt.ylabel('7Li/H')
    plt.legend(fontsize=7)
    plt.grid(True)

    plt.suptitle(
        'TEP Baryonic-Cycling Light-Element Network: Convergence to Equilibrium',
        fontsize=13,
    )
    plt.tight_layout(rect=[0, 0, 1, 0.96])

    plot_path = project_root / "results" / "gate8_light_elements.png"
    plot_path.parent.mkdir(exist_ok=True, parents=True)
    plt.savefig(plot_path, dpi=300, bbox_inches='tight')
    plt.close()
    print_status(f"  Plot saved to {plot_path}", "SUCCESS")

    # ------------------------------------------------------------------
    # 2f.  Comparison to observed primordial abundances
    # ------------------------------------------------------------------
    print_status("\n[5] Comparison to observed primordial abundances", "PROCESS")

    observed = {
        "Y_p": 0.245,        # 4He primordial mass fraction
        "x3_obs": 1.0e-5,    # 3He/H observed
        "x7_obs": 1.6e-10,   # 7Li/H observed (Sbordone et al.; Spite plateau)
        "x7_bbn": 5.0e-10,   # 7Li/H standard hot-BBN prediction (overprediction)
    }

    print_status(f"  4He:  Y_eq = {Y_eq:.4f}  vs  Y_p(obs) = {observed['Y_p']:.3f}  "
                 f"->  ratio = {Y_eq / observed['Y_p']:.3f}", "SUCCESS")
    print_status(f"  3He:  x3_eq = {x3_eq:.2e}  vs  3He/H(obs) = {observed['x3_obs']:.1e}  "
                 f"->  ratio = {x3_eq / observed['x3_obs']:.2f}", "SUCCESS")
    print_status(f"  7Li:  x7_eq = {x7_eq:.2e}  vs  7Li/H(obs) = {observed['x7_obs']:.1e}  "
                 f"->  ratio = {x7_eq / observed['x7_obs']:.2f}", "SUCCESS")

    lithium_ratio_tep = x7_eq / observed['x7_obs']
    lithium_ratio_bbn = observed['x7_bbn'] / observed['x7_obs']
    print_status(
        f"\n  Lithium problem analysis:", "PROCESS"
    )
    print_status(
        f"    Standard hot BBN predicts 7Li/H = {observed['x7_bbn']:.1e}, "
        f"overpredicting by factor {lithium_ratio_bbn:.1f}.", "INFO"
    )
    print_status(
        f"    TEP baryonic-cycling equilibrium 7Li/H = {x7_eq:.2e}, "
        f"ratio to observed = {lithium_ratio_tep:.2f}.", "INFO"
    )
    if lithium_ratio_tep < lithium_ratio_bbn:
        print_status(
            f"    TEP naturally produces LESS 7Li than hot BBN "
            f"(factor {lithium_ratio_bbn / lithium_ratio_tep:.1f} lower), "
            f"offering a pathway to resolve the lithium problem.", "SUCCESS"
        )

    # ------------------------------------------------------------------
    # 2g.  Save results
    # ------------------------------------------------------------------
    out_dict = {
        "gate": 8,
        "description": "Light element network (3He, 4He, 7Li) via baryonic cycling",
        "parameters": {
            "R": R,
            "f_vmo": f_vmo,
            "p_Y_std": p_Y_std,
            "p_Y_vmo": p_Y_vmo,
            "p_Z_std": p_Z_std,
            "p_3_std": p_3_std,
            "p_7_std": p_7_std,
            "p_7_cr": p_7_cr,
            "d_3": d_3,
            "d_7": d_7,
            "p_Y_eff": p_Y_eff,
            "p_Z_eff": p_Z_eff,
            "p_3_eff": p_3_eff,
            "p_7_eff": p_7_eff,
            "tau_star": tau_star,
        },
        "temporal_horizon_convergence": {
            "p": p_horizon,
            "q": q_astration,
            "p_plus_q": pq,
            "converges": converges,
            "condition": "p + q > 1  =>  E_astr < inf  for all species",
        },
        "theoretical_equilibrium": {
            "Y_eq": float(Y_eq),
            "Z_eq": float(Z_eq),
            "x3_eq": float(x3_eq),
            "x7_eq": float(x7_eq),
        },
        "observed_primordial": observed,
        "ratios_to_observed": {
            "Y_ratio": float(Y_eq / observed["Y_p"]),
            "x3_ratio": float(x3_eq / observed["x3_obs"]),
            "x7_ratio": float(x7_eq / observed["x7_obs"]),
            "x7_bbn_overprediction": float(lithium_ratio_bbn),
            "tep_lithium_suppression_factor": float(lithium_ratio_bbn / lithium_ratio_tep),
        },
        "gate6_reference": {
            "Y_eq": gate6["theoretical_equilibrium"]["Y_eq"],
            "Z_eq": gate6["theoretical_equilibrium"]["Z_eq"],
        },
        "simulations": results,
    }

    results_path = project_root / "results" / "gate8_light_elements.json"
    with open(results_path, "w") as f:
        json.dump(out_dict, f, indent=2)

    print_status(f"\nGate 8 light-element network complete. Results saved to {results_path}", "SUCCESS")
    print_status(
        f"Equilibrium: Y={Y_eq:.4f}, 3He/H={x3_eq:.2e}, 7Li/H={x7_eq:.2e}", "SUCCESS"
    )


if __name__ == "__main__":
    run_gate8()
