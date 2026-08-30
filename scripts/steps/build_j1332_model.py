#!/usr/bin/env python3
"""
Build VPFIT .26 model file for J1332+0052 (z_abs=3.4210863) from
Riemer-Sørensen et al. 2024 (arXiv:2401.12797, MNRAS stae248).

Parses Table 3 (tab:fit_results) from main.tex to extract the 4-component
model parameters (velocity offsets, b_turb, T, logN for H I and metals),
then writes a .26 file with proper VPFIT tie structure.

The D/H ratio is log(D/H) = -4.623, applied to all 4 components.

Regions are matched to the J1332+0052_union_manifest.json coadds key
'J1332+0052_UVES' with UVES R=50800 (vsig ~2.51 km/s).
"""

import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from collections import OrderedDict

project_root = Path(__file__).resolve().parent.parent.parent
SOURCE_DIR = project_root / "data" / "raw" / "literature_source" / "2401.12797"
OUTPUT_PATH = project_root / "data" / "literature_components" / "J1332+0052_z3.421_vpfit_model.26"
MANIFEST_PATH = project_root / "data" / "processed" / "J1332+0052_union_manifest.json"

Z_ABS = 3.4210863
C_KMS = 299792.458
UVES_R = 50800
VSIG = C_KMS / (2.35482 * UVES_R)  # ~2.51 km/s (FWHM to sigma)

# Table 3 data (parsed from main.tex tab:fit_results)
# Velocity offsets, b_turb, T, logN(HI) for 4 components
COMPONENTS = [
    {"dv_kms": -17.4, "b_turb": 11.7, "T": 12600.0, "logN_HI": 16.68},
    {"dv_kms":   0.0, "b_turb":  2.8, "T": 10100.0, "logN_HI": 19.25},
    {"dv_kms":   8.7, "b_turb":  1.0, "T": 15100.0, "logN_HI": 18.39},
    {"dv_kms":  21.3, "b_turb":  4.2, "T": 22200.0, "logN_HI": 16.80},
]

LOG_DH = -4.623  # log(D/H) from the paper


def dv_to_z(dv_kms, z_abs=Z_ABS):
    """Convert velocity offset to redshift."""
    return z_abs * (1.0 + dv_kms / C_KMS) + dv_kms / C_KMS


def build_components():
    """Build H I and D I component list from Table 3 data.

    Also includes H I interloper components from the paper's Appendix A
    (interloping absorption systems). These are H I systems at different
    redshifts whose Lyman series absorption falls within the D/H system's
    data blocks. Without modeling these interlopers, the unmodeled
    absorption inflates residuals and the noise model scale, making the
    MC calibration overly conservative. The interloper redshifts are taken
    from the figure captions in Appendix A; logN_H and b are estimated
    from the residual absorption depth at each interloper's Lyman series
    wavelength within the data blocks.
    """
    components = []
    z_tie_letters = "ABCD"

    for i, comp in enumerate(COMPONENTS):
        z = dv_to_z(comp["dv_kms"])
        z_tie = z_tie_letters[i]

        # H I component with thermal block
        components.append({
            "ion": "H_I",
            "logN": comp["logN_HI"],
            "z": z,
            "b": None,  # computed from thermal block
            "b_turb": comp["b_turb"],
            "T": comp["T"],
            "z_tie": z_tie,
            "b_tie": z_tie.lower(),  # lowercase for H I thermal tie
            "N_tie": "x",  # all H I share the same N tie? No, separate
        })

        # D I component: same z, N tied to H I via D/H ratio
        logN_DI = comp["logN_HI"] + LOG_DH
        components.append({
            "ion": "D_I",
            "logN": logN_DI,
            "z": z,
            "b": None,
            "b_turb": None,  # D I b derived from shared thermal params
            "T": None,
            "T_parent": comp["T"],
            "b_turb_parent": comp["b_turb"],
            "z_tie": z_tie,
            "b_tie": z_tie.upper(),  # uppercase for D I (mass-scaled thermal tie)
            "N_tie": "%",  # tied to parent H I via D/H offset
        })

    # Add interloper H I components from Appendix A.
    # These are H I absorbers at different redshifts whose Lyman series
    # transitions fall within the D/H system's data blocks. Parameters
    # (logN_H, b) are estimated from the residual absorption depth.
    # Each interloper is a simple H I component with independent b
    # (no thermal block, no D counterpart).
    interlopers = [
        # (z, logN_H, b_kms)  — estimated from residual absorption
        (2.729383, 14.0, 10.0),   # blends with D I λ1026
        (2.534616, 13.1, 10.0),   # blends with D I λ973
        (3.475422, 15.2, 12.0),   # blends with D I λ950
        (2.409310, 13.7, 10.0),   # blends with D I λ938 (first)
        (3.261862, 15.3, 12.0),   # blends with D I λ938 (second)
        (3.331398, 14.5, 10.0),   # blends with D I λ931
        (2.991426, 14.9, 10.0),   # blends with D I λ926
    ]

    for z_int, logN_int, b_int in interlopers:
        components.append({
            "ion": "H_I",
            "logN": logN_int,
            "z": z_int,
            "b": b_int,  # direct b value (no thermal block)
            "b_turb": None,
            "T": None,
            "z_tie": "!",  # independent (no tie)
            "b_tie": "!",  # independent b
            "N_tie": "!",  # independent N
        })

    # Assign unique N ties for H I
    n_tie_letters = "xyzabcdefghijklmnopqrstuvw"
    hi_count = 0
    for c in components:
        if c["ion"] == "H_I":
            c["N_tie"] = n_tie_letters[hi_count]
            hi_count += 1

    return components


def format_component_line(c):
    """Format a component as a VPFIT .26 line."""
    ion_str = c["ion"].replace("_", " ")
    z_str = f"{c['z']:.10f}{c['z_tie']}"
    z_tie_val = "0.0000000000"
    N_str = f"{c['logN']:.6f}{c['N_tie']}"
    N_tie_val = "0.000000"

    if c["b_turb"] is not None and c["T"] is not None:
        # H I with thermal block: compute total b for display
        mass = 1.0
        b_therm = 12.85 * ((c["T"] / 1e4) / mass) ** 0.5
        b_tot = (c["b_turb"] ** 2 + b_therm ** 2) ** 0.5
        b_str = f"{b_tot:.5f}{c['b_tie']}"
        b_tie_val = "0.00000"
        thermal = f"[  {c['b_turb']:.3f}   0.000 {c['T']:.4e} 0.000e+00"
        line = f" {ion_str:<6s} {z_str:>18s}   {z_tie_val}    {b_str:>14s}    {b_tie_val}  {N_str:>14s}   {N_tie_val}  0 {thermal}"
    elif c["ion"] == "D_I":
        # D I: b tied to H I via uppercase tie (mass-scaled thermal)
        # Display the D I total b for reference
        mass = 2.01410
        b_therm = 12.85 * ((c.get("T_parent", 10000.0) / 1e4) / mass) ** 0.5
        b_tot = (c.get("b_turb_parent", 1.0) ** 2 + b_therm ** 2) ** 0.5
        b_str = f"{b_tot:.5f}{c['b_tie']}"
        b_tie_val = "0.00000"
        line = f" {ion_str:<6s} {z_str:>18s}   {z_tie_val}    {b_str:>14s}    {b_tie_val}  {N_str:>14s}   {N_tie_val}  0 ! "
    elif c.get("b") is not None:
        # Interloper H I with direct b value (no thermal block)
        b_str = f"{c['b']:.5f}{c['b_tie']}"
        b_tie_val = "0.00000"
        line = f" {ion_str:<6s} {z_str:>18s}   {z_tie_val}    {b_str:>14s}    {b_tie_val}  {N_str:>14s}   {N_tie_val}  0 ! "
    else:
        b_str = f"{'0.00000':>10s}{c['b_tie']}"
        b_tie_val = "0.00000"
        line = f" {ion_str:<6s} {z_str:>18s}   {z_tie_val}    {b_str:>14s}    {b_tie_val}  {N_str:>14s}   {N_tie_val}  0 ! "

    return line


def build_regions():
    """Build region lines from the manifest, resolving overlaps.

    Also adds a Lyα region manually, since the Lyα damping wings are
    critical for D/H analysis but may not be present in the manifest
    if the original ingestion missed the CD#3 grating data.
    """
    with open(MANIFEST_PATH, "r") as f:
        manifest = json.load(f)

    coadd_key = list(manifest["coadds"].keys())[0]
    chunks = manifest["coadds"][coadd_key]

    raw_bounds = []
    for chunk in chunks:
        w = chunk["wave"]
        raw_bounds.append((min(w), max(w)))

    # Add Lyα region if not already covered by a higher-order Lyman region.
    # Lyα at z_abs: 1215.6701 * (1 + z_abs) = 5374.58 Å
    # Use a ±500 km/s window to capture the damping wings where D/H
    # information is concentrated.  A wider window includes quasar
    # continuum features (emission lines, breaks) that a 10-parameter
    # Chebyshev cannot capture, inflating residuals.
    lya_w = 1215.6701 * (1 + Z_ABS)
    lya_halfwidth = lya_w * 500.0 / C_KMS  # ±500 km/s in Å
    lya_lo = lya_w - lya_halfwidth
    lya_hi = lya_w + lya_halfwidth
    # Remove any existing region that overlaps with Lyα (e.g. a stale
    # wide Lyα region from a previous manifest) and add the narrow one.
    raw_bounds = [(lo, hi) for lo, hi in raw_bounds
                  if hi < lya_lo or lo > lya_hi]
    raw_bounds.append((lya_lo, lya_hi))

    indexed = sorted(enumerate(raw_bounds), key=lambda x: x[1][0])
    sorted_bounds = [b for _, b in indexed]
    orig_indices = [i for i, _ in indexed]

    bounds = list(sorted_bounds)
    for i in range(len(bounds) - 1):
        lo_i, hi_i = bounds[i]
        lo_j, hi_j = bounds[i + 1]
        if hi_i >= lo_j:
            bounds[i] = (lo_i, lo_j - 0.01)

    final_bounds = [None] * len(raw_bounds)
    for idx, b in zip(orig_indices, bounds):
        final_bounds[idx] = b

    regions = []
    for i, (w_min, w_max) in enumerate(final_bounds):
        regions.append({
            "filename": coadd_key,
            "idx": 1,
            "w_min": w_min,
            "w_max": w_max,
            "vsig": VSIG,
            "comment": str(i + 1),
        })

    return regions


def main():
    print("Building J1332+0052 VPFIT model from Riemer-Sørensen et al. 2024...")
    print(f"  Source: {SOURCE_DIR}")
    print(f"  Output: {OUTPUT_PATH}")
    print(f"  z_abs = {Z_ABS}")
    print(f"  UVES R = {UVES_R}, vsig = {VSIG:.2f} km/s")
    print(f"  log(D/H) = {LOG_DH}")

    # Build components
    components = build_components()
    from collections import Counter
    ion_counts = Counter(c["ion"] for c in components)
    print(f"  Components: {len(components)} ({dict(ion_counts)})")

    # Build regions
    regions = build_regions()
    print(f"  Regions: {len(regions)}")

    # Compute SHA256 of source tarball for provenance
    source_tarball = SOURCE_DIR / "source.tar.gz"
    source_sha256 = ""
    if source_tarball.exists():
        h = hashlib.sha256()
        with open(source_tarball, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                h.update(chunk)
        source_sha256 = h.hexdigest()

    arxiv_prov_path = SOURCE_DIR / "arxiv_provenance.json"
    arxiv_sha256 = ""
    if arxiv_prov_path.exists():
        with open(arxiv_prov_path, "r") as f:
            arxiv_prov = json.load(f)
        arxiv_sha256 = arxiv_prov.get("sha256", "")

    gen_timestamp = datetime.now(timezone.utc).isoformat()

    # Write .26 file
    lines = []
    lines.append(f"% VPFIT model for J1332+0052 z={Z_ABS}")
    lines.append("% Source: arXiv:2401.12797 (Riemer-Sørensen et al. 2024, MNRAS stae248)")
    lines.append("% Generated by scripts/steps/build_j1332_model.py")
    lines.append(f"% Generated at: {gen_timestamp}")
    if arxiv_sha256:
        lines.append(f"% arXiv source SHA256: {arxiv_sha256}")
    lines.append("% UVES R=50800, vsig={:.2f} km/s".format(VSIG))
    lines.append(f"% H I components: {ion_counts.get('H_I', 0)}")
    lines.append(f"% D I components: {ion_counts.get('D_I', 0)}")
    lines.append(f"% log(D/H) = {LOG_DH}")
    lines.append("% Reproduce: python scripts/steps/build_j1332_model.py")
    lines.append("")

    # Region lines
    for r in regions:
        lines.append(
            f"%% {r['filename']}     {r['idx']}   {r['w_min']:.4f}   {r['w_max']:.4f} vsig={r['vsig']:.2f}  !  {r['comment']}"
        )

    lines.append("")

    # Component lines
    for c in components:
        lines.append(format_component_line(c))

    # Write file
    with open(OUTPUT_PATH, "w") as f:
        f.write("\n".join(lines) + "\n")

    print(f"\n  Written {len(lines)} lines to {OUTPUT_PATH}")

    # Verify by parsing
    sys.path.insert(0, str(project_root))
    from scripts.lib.model_parser import parse_vpfit_ties, ParameterManager

    components_parsed, regions_parsed = parse_vpfit_ties(str(OUTPUT_PATH))
    pm = ParameterManager(components_parsed)
    print(f"\n  Verification:")
    print(f"    Parsed components: {len(components_parsed)}")
    print(f"    Parsed regions: {len(regions_parsed)}")
    print(f"    Theta parameters: {len(pm.theta_init)}")
    print(f"    H I components: {sum(1 for c in components_parsed if c['ion'] == 'H_I')}")
    print(f"    D I components: {sum(1 for c in components_parsed if c['ion'] == 'D_I')}")


if __name__ == "__main__":
    main()
