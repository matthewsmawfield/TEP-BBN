#!/usr/bin/env python3
"""
Generate the S_Σ vs |Φ|/c² screening plot for Gate 4B.

Shows the smooth, continuous transition from the unscreened absorber
regime (~10⁻⁸) through the dwarf galaxy transition (~10⁻⁷) into the
heavily screened galactic/solar regime (~10⁻⁶).
"""

import sys
from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

project_root = Path(__file__).resolve().parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from scripts.utils.logger import print_status, setup_step_logger


def main():
    setup_step_logger(Path(__file__).stem)
    project_root = Path(__file__).resolve().parent.parent.parent

    # Frozen parameters from Gate 4B (absorber-regime ansatz calibration)
    # Anchors:
    # 1. Absorber: |Φ_abs|/c² = 1e-8 → S_Σ > 0.999 (unscreened)
    # 2. Galactic halo: |Φ_gal|/c² = 5.38e-7 → S_Σ ≈ 0.013 (corpus value)
    # Solution: Phi_half = 1.59e-7, n = 3.56
    # NB: solar source charge is the microscopic completion's projection
    # (Paper 0 §7: S_Σ(⊙) < 5.75e-6 under the canonical linear PPN mapping),
    # not this ansatz's solar extrapolation — see step_09 docstring.
    Phi_half = 1.59e-7
    n = 3.56
    beta_A = -1.0
    Phi_sun = 2.12e-6    # solar system (Cassini grazing ray at R_⊙)
    Phi_gal = 5.38e-7    # galactic halo (v_circ = 220 km/s)
    S_solar = 1.0 / (1.0 + (Phi_sun / Phi_half)**n)  # ~1e-4
    S_galactic = 1.0 / (1.0 + (Phi_gal / Phi_half)**n)  # ~0.013

    # Logarithmic sweep
    log_Phi = np.linspace(-12, -4, 2000)
    Phi = 10**log_Phi
    S = 1.0 / (1.0 + (Phi / Phi_half)**n)
    beta_eff_sq = beta_A**2 * S**2
    product = beta_eff_sq * Phi

    # Create figure with two panels
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 7), sharex=True,
                                    gridspec_kw={'height_ratios': [2, 1.2],
                                                 'hspace': 0.08})

    # --- Panel 1: S_Σ(|Φ|/c²) ---
    ax1.semilogx(Phi, S, 'b-', linewidth=2.5, label=r'$\mathcal{S}_\Sigma(|\Phi|/c^2)$')
    ax1.axhline(y=S_solar, color='gray', linestyle='--', alpha=0.5, linewidth=1)
    ax1.axhline(y=1.0, color='gray', linestyle=':', alpha=0.3, linewidth=1)

    # Boundary condition markers
    regimes = [
        (1e-8,  1.0 / (1.0 + (1e-8 / Phi_half)**n),   'Absorber\n(unscreened)', 'green'),
        (1e-7,  1.0 / (1.0 + (1e-7 / Phi_half)**n),   'Dwarf galaxy\n(transition)', 'orange'),
        (Phi_gal, S_galactic,                          'Galactic halo\n(β_eff≈0.013)', 'purple'),
        (Phi_sun, S_solar,                             'Solar system\n(Cassini)', 'red'),
    ]

    for phi_val, s_val, label, color in regimes:
        ax1.plot(phi_val, s_val, 'o', color=color, markersize=8, zorder=5)
        ax1.annotate(label, xy=(phi_val, s_val),
                     xytext=(phi_val * 3, s_val + 0.08 if s_val < 0.5 else s_val - 0.12),
                     fontsize=8, color=color, fontweight='bold',
                     arrowprops=dict(arrowstyle='->', color=color, lw=1.2),
                     ha='left')

    # Half-suppression point
    ax1.plot(Phi_half, 0.5, 'D', color='purple', markersize=7, zorder=5)
    ax1.annotate(r'$\Phi_{\rm half} = 1.59 \times 10^{-7}$' + '\n' + r'$\mathcal{S}_\Sigma = 0.5$',
                 xy=(Phi_half, 0.5), xytext=(Phi_half * 0.05, 0.35),
                 fontsize=8, color='purple', fontweight='bold',
                 arrowprops=dict(arrowstyle='->', color='purple', lw=1.2),
                 ha='center')

    ax1.set_ylabel(r'$\mathcal{S}_\Sigma(|\Phi|/c^2)$', fontsize=13)
    ax1.set_ylim(0.0, 1.15)
    ax1.legend(loc='center right', fontsize=10, framealpha=0.9)
    ax1.set_title(r'Environmental Screening Operator: $\mathcal{S}_\Sigma = 1/(1 + (|\Phi|/c^2 / \Phi_{\rm half})^n)$'
                  + '\n' + r'$\Phi_{\rm half} = 1.59 \times 10^{-7}$, $n = 3.56$ (three-anchor calibration)',
                  fontsize=11, pad=10)
    ax1.grid(True, which='both', alpha=0.3)
    ax1.xaxis.set_major_formatter(mticker.ScalarFormatter())
    ax1.xaxis.set_minor_formatter(mticker.NullFormatter())

    # --- Panel 2: β_eff² × |Φ|/c² (fifth force strength) ---
    ax2.loglog(Phi, product, 'r-', linewidth=2.5, label=r'$\beta_{\rm eff}^2 \times |\Phi|/c^2$')

    # Peak marker
    idx_peak = np.argmax(product)
    ax2.plot(Phi[idx_peak], product[idx_peak], 'r*', markersize=12, zorder=5)
    ax2.annotate(f'Peak at\n' + r'$|\Phi|/c^2 \sim 10^{-7}$' + '\n(unscreened regime)',
                 xy=(Phi[idx_peak], product[idx_peak]),
                 xytext=(Phi[idx_peak] * 0.01, product[idx_peak] * 3),
                 fontsize=8, color='red', fontweight='bold',
                 arrowprops=dict(arrowstyle='->', color='red', lw=1.2),
                 ha='center')

    # Regime shading
    ax2.axvspan(1e-9, 1e-8, alpha=0.1, color='green', label='Absorber')
    ax2.axvspan(1e-8, 1e-7, alpha=0.08, color='orange', label='Dwarf')
    ax2.axvspan(1e-7, 1e-5, alpha=0.08, color='red', label='Galaxy/Solar')

    ax2.set_xlabel(r'$|\Phi|/c^2$ (gravitational potential depth)', fontsize=12)
    ax2.set_ylabel(r'$\beta_{\rm eff}^2 \times |\Phi|/c^2$', fontsize=12)
    ax2.legend(loc='upper left', fontsize=9, framealpha=0.9)
    ax2.grid(True, which='both', alpha=0.3)
    ax2.set_xlim(1e-12, 1e-4)

    # Format x-axis labels
    ax2.xaxis.set_major_formatter(mticker.FuncFormatter(
        lambda x, _: f'$10^{{{int(np.log10(x))}}}$' if x > 0 else ''))

    plt.tight_layout()

    # Save to both results and site/assets
    out_results = project_root / "results" / "gate4b_screening.png"
    out_assets = project_root / "site" / "assets" / "gate4b_screening.png"
    out_assets.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_results, dpi=150, bbox_inches='tight')
    fig.savefig(out_assets, dpi=150, bbox_inches='tight')
    plt.close(fig)

    print_status(f"Saved: {out_results}", "SUCCESS")
    print_status(f"Saved: {out_assets}", "SUCCESS")

    # Print key values
    S_abs = 1.0/(1.0+(1e-8/Phi_half)**n)
    S_dwarf = 1.0/(1.0+(1e-7/Phi_half)**n)
    print_status(f"\nKey screening values:", "PROCESS")
    print_status(f"  Absorber  (|Φ|/c²=1e-8):  S_Σ = {S_abs:.6f}", "PROCESS")
    print_status(f"  Dwarf     (|Φ|/c²=1e-7):  S_Σ = {S_dwarf:.6f}", "PROCESS")
    print_status(f"  Galactic  (|Φ|/c²=5.38e-7): S_Σ = {S_galactic:.6f}", "PROCESS")
    print_status(f"  Solar     (|Φ|/c²=2.12e-6): S_Σ = {S_solar:.6f}", "PROCESS")
    print_status(f"  Peak β_eff²×|Φ|/c² at |Φ|/c² = {Phi[idx_peak]:.1e}", "PROCESS")

    # Write JSON ledger
    ledger_path = project_root / "results" / "gate4b_screening_plot.json"
    ledger = {
        "Phi_half": float(Phi_half),
        "n": float(n),
        "beta_A": float(beta_A),
        "S_absorber": float(S_abs),
        "S_dwarf": float(S_dwarf),
        "S_solar": float(S_solar),
        "S_galactic": float(S_galactic),
        "peak_Phi": float(Phi[idx_peak]),
        "peak_beta_eff_sq_Phi": float(product[idx_peak]),
        "plot_file": "results/gate4b_screening.png",
        "assets_copy": "site/assets/gate4b_screening.png",
    }
    with open(ledger_path, "w") as f:
        json.dump(ledger, f, indent=2)
    print_status(f"Saved: {ledger_path}", "SUCCESS")


if __name__ == "__main__":
    main()
