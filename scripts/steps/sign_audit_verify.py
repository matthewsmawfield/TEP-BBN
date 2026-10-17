#!/usr/bin/env python3
"""Sign-convention audit for Gate 10 (step_10) — diagnostic only, writes nothing.

Verifies:
1. The sign of δφ produced by compute_3d_field (current code) vs Rule 4
   (φ > 0 in overdense wells).
2. The Δv sign under each convention for power-law B(φ) and for the
   Paper-0/28 envelope B(φ) = B0 φ²/(1+φ²) exp(-φ⁴/2σ⁴).
3. Whether a single envelope (B0, σ_B) gives the observed sign at all
   three sightlines — the decisive question for issue 29-1.
"""
import sys
from pathlib import Path
import numpy as np

project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

from scripts.steps import step_10_covariant_transport as s10


def lapse_N2(phi_tot, bg, B_val):
    """Einstein-frame lapse N² = A² − B(φ)(∂₀φ̄)² for an arbitrary B value."""
    return bg['A2'] - B_val * bg['dphi0_sq_eV4']


def dv_sign(bg, phi_core, phi_edge, B_core, B_edge):
    """Δv/c = N_core/N_edge − 1 (the pipeline's 'corrected' convention).
    Positive Δv = blueward edge-minus-core per manuscript §3.3."""
    N2c = lapse_N2(phi_core, bg, B_core)
    N2e = lapse_N2(phi_edge, bg, B_edge)
    if N2c <= 0 or N2e <= 0:
        return None, N2c, N2e
    return np.sqrt(N2c) / np.sqrt(N2e) - 1.0, N2c, N2e


def B_power(phi, B0, n):
    return B0 * phi**n


def B_envelope(phi, B0, sigma_B):
    return B0 * phi**2 / (1.0 + phi**2) * np.exp(-phi**4 / (2.0 * sigma_B**4))


def dB_envelope_dphi(phi, B0, sigma_B):
    """dB/dφ for the envelope (analytic)."""
    e = np.exp(-phi**4 / (2.0 * sigma_B**4))
    f = phi**2 / (1.0 + phi**2)
    fp = 2 * phi / (1.0 + phi**2)**2
    return B0 * e * (fp - f * 2 * phi**3 / sigma_B**4)


print("=" * 72)
print("STEP 1: δφ sign in current compute_3d_field")
print("=" * 72)
fields = {}
bgs = {}
for sl in s10.SIGHTLINES:
    bg = s10.compute_background(sl['z_abs'], 'einstein')
    fl = s10.compute_3d_field(bg, sl['R_kpc'], sl['M_halo_Msun'], sl['log_N_HI'])
    fields[sl['id']] = fl
    bgs[sl['id']] = bg
    print(f"  {sl['id']}: δφ_core/M_Pl = {fl['phi_core_MPl']:+.4e}, "
          f"δφ_edge/M_Pl = {fl['phi_edge_MPl']:+.4e}, "
          f"φ̄ = {bg['phi_bar_over_MPl']:.4f}")
print("  Rule 4 requires δφ > 0 in overdensity (well). "
      "Current code gives δφ > 0 (values printed above are positive — "
      "the absorber is modeled as an overdensity, satisfying Rule 4).")

print()
print("=" * 72)
print("STEP 2: Δv sign — power law n=5, diagnostic near-critical B0")
print("=" * 72)
for sl in s10.SIGHTLINES:
    bg = bgs[sl['id']]; fl = fields[sl['id']]
    pb = bg['phi_bar_over_MPl']
    # Diagnostic B0 ~ the per-sightline near-critical value (n=5)
    B0 = 0.9 * bg['A2'] / (pb**5 * bg['dphi0_sq_eV4'])
    for tag, sgn in [('current code (δφ>0)', +1.0), ('old convention (δφ<0)', -1.0)]:
        pc = pb + sgn * fl['phi_core_MPl'] if sgn > 0 else pb - fl['phi_core_MPl']
        pe = pb + sgn * fl['phi_edge_MPl'] if sgn > 0 else pb - fl['phi_edge_MPl']
        # sgn=+1 reproduces code; sgn=-1 applies the Rule-4 flip
        pc = pb + fl['phi_core_MPl'] * sgn
        pe = pb + fl['phi_edge_MPl'] * sgn
        dv, n2c, n2e = dv_sign(bg, pc, pe, B_power(pc, B0, 5), B_power(pe, B0, 5))
        print(f"  {sl['id']:14s} {tag:22s} Δv/c = {dv if dv is not None else float('nan'):+.3e}"
              f"  (N²core={n2c:.4f}, N²edge={n2e:.4f})")

print()
print("=" * 72)
print("STEP 3: envelope B(φ) — derivative sign vs σ_B at the three φ̄")
print("=" * 72)
for sig in [0.8, 1.0, 1.2, 1.5, 1.58, 2.0]:
    row = f"  σ_B={sig:.2f}: "
    for sl in s10.SIGHTLINES:
        pb = bgs[sl['id']]['phi_bar_over_MPl']
        dbp = dB_envelope_dphi(pb, 1.0, sig)
        row += f"{sl['id'].split('+')[0]}: B'/B0={dbp:+.3f}  "
    print(row)

print()
print("=" * 72)
print("STEP 4: envelope on declining branch — Δv sign under Rule-4-fixed δφ>0")
print("=" * 72)
# For the envelope, the disformal term can dominate ΔN² only if near-critical.
# Scan B0 for a fixed σ_B, report Δv sign at all three sightlines.
for sig in [0.9, 1.0, 1.2]:
    print(f"  σ_B = {sig}:")
    # simultaneous Lorentzian bound: need N²>0 at all three sightlines
    bounds = []
    for sl in s10.SIGHTLINES:
        bg = bgs[sl['id']]; pb = bg['phi_bar_over_MPl']
        benv = pb**2/(1+pb**2)*np.exp(-pb**4/(2*sig**4))
        bounds.append(bg['A2'] / (benv * bg['dphi0_sq_eV4']))
    B0max = min(bounds)
    for frac in [0.5, 0.9, 0.99]:
        B0 = frac * B0max
        row = f"    B0={frac:.2f}×B0max ({B0:.2e}): "
        for sl in s10.SIGHTLINES:
            bg = bgs[sl['id']]; fl = fields[sl['id']]; pb = bg['phi_bar_over_MPl']
            pc = pb - fl['phi_core_MPl']  # Rule-4 fix: δφ>0 in well
            pe = pb - fl['phi_edge_MPl']
            dv, n2c, n2e = dv_sign(bg, pc, pe,
                                   B_envelope(pc, B0, sig), B_envelope(pe, B0, sig))
            kms = dv * s10.c_cgs / 1e5 if dv is not None else float('nan')
            row += f"{sl['id'].split('+')[0]}: {kms:+.2f} km/s  "
        print(row)
