#!/usr/bin/env python3
"""
Build VPFIT .26 model file for PKS1937-101 (z_abs=3.572) from Cooke et al. 2024
(arXiv:2402.05586, MNRAS stae452).

Parses Model.tex and TransitionUnrelated.tex from the paper source to extract
all H I, D I, and metal components, then writes a .26 file with proper VPFIT
tie structure.

Regions are matched to the PKS1937-101_union_manifest.json coadds key
'PKS1937-101_ESPRESSO' with ESPRESSO R=70000 (vsig ~4.28 km/s).
"""

import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from collections import OrderedDict

project_root = Path(__file__).resolve().parent.parent.parent
SOURCE_DIR = project_root / "data" / "raw" / "literature_source" / "2402.05586"
OUTPUT_PATH = project_root / "data" / "literature_components" / "PKS1937-101_z3.572_vpfit_model.26"
MANIFEST_PATH = project_root / "data" / "processed" / "PKS1937-101_union_manifest.json"

Z_ABS = 3.572
C_KMS = 299792.458
ESPRESSO_R = 70000
VSIG = C_KMS / (2.35482 * ESPRESSO_R)  # ~1.82 km/s (sigma, not FWHM)


def parse_model_tex(filepath):
    """Parse Model.tex to extract components from the longtable."""
    with open(filepath, "r") as f:
        content = f.read()

    # Remove LaTeX formatting
    content = content.replace(r"\ion{", "").replace("{", "").replace("}", "")
    content = content.replace(r"\kms", "")
    content = content.replace(r"\log(", "")
    content = content.replace(r"\Delta ", "")
    content = content.replace(r"\rm ", "")
    content = content.replace(r"\label{tab:modelTransition}", "")
    content = content.replace(r"\caption", "% ")
    content = content.replace(r"\toprule", "")
    content = content.replace(r"\midrule", "")
    content = content.replace(r"\bottomrule", "")
    content = content.replace(r"\\", "\n")
    content = content.replace(r"\begin{longtable}", "")
    content = content.replace(r"\end{longtable}", "")

    components = []
    for line in content.split("\n"):
        line = line.strip()
        if not line or line.startswith("%") or line.startswith("&"):
            continue
        parts = line.split("&")
        if len(parts) < 5:
            continue
        # Clean parts
        parts = [p.strip().rstrip(".") for p in parts]
        ion_str = parts[0].strip()
        logN_str = parts[1].strip()
        z_str = parts[3].strip()
        b_str = parts[5].strip()
        b_turb_str = parts[7].strip() if len(parts) > 7 else "////"
        T_str = parts[9].strip() if len(parts) > 9 else "////"

        # Skip header rows
        if ion_str in ("Transition", "") or not ion_str:
            continue
        if logN_str == "" or z_str == "":
            continue
        try:
            logN = float(logN_str)
            z = float(z_str)
            b = float(b_str)
        except ValueError:
            continue

        b_turb = None
        T = None
        if b_turb_str != "////" and b_turb_str != "":
            try:
                b_turb = float(b_turb_str)
            except ValueError:
                pass
        if T_str != "////" and T_str != "":
            try:
                T = float(T_str)
            except ValueError:
                pass

        # Determine ion
        if ion_str.startswith("H") and "I" in ion_str:
            ion = "H_I"
        elif ion_str.startswith("D") and "I" in ion_str:
            ion = "D_I"
        elif ion_str.startswith("C") and "II" in ion_str:
            ion = "C_II"
        elif ion_str.startswith("C") and "III" in ion_str:
            ion = "C_III"
        elif ion_str.startswith("C") and "IV" in ion_str:
            ion = "C_IV"
        elif ion_str.startswith("Si") and "II" in ion_str:
            ion = "Si_II"
        elif ion_str.startswith("Si") and "IV" in ion_str:
            ion = "Si_IV"
        elif ion_str.startswith("Fe") and "III" in ion_str:
            ion = "Fe_III"
        elif ion_str.startswith("??") or ion_str == "Unknown":
            ion = "H_I"  # Treated as H I by VPFIT default
        else:
            continue

        components.append({
            "ion": ion,
            "logN": logN,
            "z": z,
            "b": b,
            "b_turb": b_turb,
            "T": T,
        })

    return components


def parse_transition_unrelated_tex(filepath):
    """Parse TransitionUnrelated.tex for interloper H I components."""
    with open(filepath, "r") as f:
        content = f.read()

    # Remove LaTeX formatting
    content = content.replace(r"\ion{", "").replace("{", "").replace("}", "")
    content = content.replace(r"\kms", "")
    content = content.replace(r"\label{tab:UnrelatedInterlopers}", "")
    content = content.replace(r"\caption", "% ")
    content = content.replace(r"\toprule", "")
    content = content.replace(r"\midrule", "")
    content = content.replace(r"\bottomrule", "")
    content = content.replace(r"\\", "\n")
    content = content.replace(r"\begin{longtable}", "")
    content = content.replace(r"\end{longtable}", "")

    components = []
    for line in content.split("\n"):
        line = line.strip()
        if not line or line.startswith("%") or line.startswith("&"):
            continue
        parts = line.split("&")
        if len(parts) < 4:
            continue
        parts = [p.strip().rstrip(".") for p in parts]

        # This table has two sets of columns side by side
        # Left: Transition, logN, z, b_tot | Right: Transition, logN, z, b_tot
        for start_idx in [0, 4]:
            if start_idx + 3 >= len(parts):
                continue
            ion_str = parts[start_idx].strip()
            logN_str = parts[start_idx + 1].strip()
            z_str = parts[start_idx + 2].strip()
            b_str = parts[start_idx + 3].strip()

            if not ion_str or ion_str == "Transition":
                continue
            try:
                logN = float(logN_str)
                z = float(z_str)
                b = float(b_str)
            except ValueError:
                continue

            ion = "H_I"  # All interlopers treated as H I
            components.append({
                "ion": ion,
                "logN": logN,
                "z": z,
                "b": b,
                "b_turb": None,
                "T": None,
            })

    # Deduplicate: the source table has duplicate entries on the right
    # side of some rows (LaTeX typesetting artefact). Remove exact
    # (z, logN, b) duplicates.
    seen = set()
    unique = []
    for c in components:
        key = (round(c["z"], 7), c["logN"], c["b"])
        if key in seen:
            continue
        seen.add(key)
        unique.append(c)

    return unique


def assign_ties(components):
    """Assign VPFIT tie letters to components.

    Components at the same redshift get the same z tie letter.
    D I components get % N tie (tied to corresponding H I).
    Metals at D/H absorber redshifts share z ties with H I.
    """
    # Find unique redshifts and assign tie letters
    z_tie_letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    z_map = {}  # z_value -> tie_letter
    z_tie_idx = 0

    # First pass: assign z ties for D/H absorber components (z=3.5721324, 3.5722725, 3.5724591)
    dh_absorber_zs = [3.5721324, 3.5722725, 3.5724591]
    for z in dh_absorber_zs:
        if z_tie_idx < len(z_tie_letters):
            z_map[z] = z_tie_letters[z_tie_idx]
            z_tie_idx += 1

    # Second pass: assign z ties for all other unique redshifts
    for c in components:
        z = c["z"]
        # Round to 7 decimal places for matching
        z_key = round(z, 7)
        if z_key not in z_map:
            if z_tie_idx < len(z_tie_letters):
                z_map[z_key] = z_tie_letters[z_tie_idx]
                z_tie_idx += 1
            else:
                z_map[z_key] = ""  # No tie (free)

    # Assign ties to components
    for c in components:
        z_key = round(c["z"], 7)
        c["z_tie"] = z_map.get(z_key, "")

    # Assign b and N ties
    # D/H absorber H I: thermal blocks with b_turb/T
    # For H I at D/H absorber with no b_turb/T, use simple b ties
    b_tie_letters = "abcdefghijklmnopqrstuvwxyz"
    N_tie_letters = "xyzabcdefghijklmnopqrstuvw"
    b_tie_idx = 0
    N_tie_idx = 0

    # Group components by z_tie
    by_z_tie = OrderedDict()
    for c in components:
        zt = c["z_tie"]
        if zt not in by_z_tie:
            by_z_tie[zt] = []
        by_z_tie[zt].append(c)

    # Assign b ties: components at the same z get the same b tie (lowercase)
    # Metals with thermal blocks share b ties
    for zt, comps in by_z_tie.items():
        if not zt:
            # Free z, assign unique b and N
            for c in comps:
                c["b_tie"] = ""
                c["N_tie"] = ""
            continue

        # Assign b tie for this z group
        b_tie = b_tie_letters[b_tie_idx] if b_tie_idx < len(b_tie_letters) else ""
        b_tie_idx += 1

        for c in comps:
            if c["ion"] == "D_I":
                # D I b tie: uppercase W + lowercase letter
                c["b_tie"] = "W" + b_tie
            else:
                c["b_tie"] = b_tie

            # N ties
            if c["ion"] == "D_I":
                c["N_tie"] = "%"
            else:
                N_tie = N_tie_letters[N_tie_idx] if N_tie_idx < len(N_tie_letters) else ""
                N_tie_idx += 1
                c["N_tie"] = N_tie

    return components


def format_component_line(c):
    """Format a component as a VPFIT .26 line."""
    ion_str = c["ion"].replace("_", " ")
    z_str = f"{c['z']:.10f}{c['z_tie']}"
    z_tie_val = "0.0000000000"
    b_str = f"{c['b']:.5f}{c['b_tie']}"
    b_tie_val = "0.00000"
    N_str = f"{c['logN']:.6f}{c['N_tie']}"
    N_tie_val = "0.000000"

    # Thermal block
    if c["b_turb"] is not None and c["T"] is not None:
        thermal = f"[  {c['b_turb']:.3f}   0.000 {c['T']:.4e} 0.000e+00"
        line = f" {ion_str:<6s} {z_str:>18s}   {z_tie_val}    {b_str:>14s}    {b_tie_val}  {N_str:>14s}   {N_tie_val}  0 {thermal}"
    elif c["ion"] == "D_I":
        line = f" {ion_str:<6s} {z_str:>18s}   {z_tie_val}    {b_str:>14s}    {b_tie_val}  {N_str:>14s}   {N_tie_val}  0 ! "
    else:
        line = f" {ion_str:<6s} {z_str:>18s}   {z_tie_val}    {b_str:>14s}    {b_tie_val}  {N_str:>14s}   {N_tie_val}  0 ! "

    return line


def build_regions():
    """Build region lines from the manifest, resolving overlaps between
    adjacent chunks by narrowing boundaries so each pixel appears in at
    most one region."""
    with open(MANIFEST_PATH, "r") as f:
        manifest = json.load(f)

    coadd_key = list(manifest["coadds"].keys())[0]
    chunks = manifest["coadds"][coadd_key]

    # Compute raw boundaries
    raw_bounds = []
    for chunk in chunks:
        w = chunk["wave"]
        raw_bounds.append((min(w), max(w)))

    # Sort by w_min (ascending) to resolve overlaps consistently
    indexed = sorted(enumerate(raw_bounds), key=lambda x: x[1][0])
    sorted_bounds = [b for _, b in indexed]
    orig_indices = [i for i, _ in indexed]

    # Resolve overlaps in ascending order
    bounds = list(sorted_bounds)
    for i in range(len(bounds) - 1):
        lo_i, hi_i = bounds[i]
        lo_j, hi_j = bounds[i + 1]
        if hi_i >= lo_j:
            # Overlap: set upper bound of lower-wavelength chunk to just
            # below the lower bound of the higher-wavelength chunk
            bounds[i] = (lo_i, lo_j - 0.01)

    # Restore original order
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
    print("Building PKS1937-101 VPFIT model from Cooke et al. 2024...")
    print(f"  Source: {SOURCE_DIR}")
    print(f"  Output: {OUTPUT_PATH}")
    print(f"  z_abs = {Z_ABS}")
    print(f"  ESPRESSO R = {ESPRESSO_R}, vsig = {VSIG:.2f} km/s")

    # Parse components
    model_components = parse_model_tex(SOURCE_DIR / "Model.tex")
    interloper_components = parse_transition_unrelated_tex(SOURCE_DIR / "TransitionUnrelated.tex")

    print(f"  Model.tex components: {len(model_components)}")
    print(f"  TransitionUnrelated.tex components: {len(interloper_components)}")

    # Combine: model components first, then interlopers
    all_components = model_components + interloper_components

    # Assign ties
    all_components = assign_ties(all_components)

    # Count by ion
    from collections import Counter
    ion_counts = Counter(c["ion"] for c in all_components)
    print(f"  Ion counts: {dict(ion_counts)}")

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

    # Load arxiv provenance if available
    arxiv_prov_path = SOURCE_DIR / "arxiv_provenance.json"
    arxiv_sha256 = ""
    if arxiv_prov_path.exists():
        with open(arxiv_prov_path, "r") as f:
            arxiv_prov = json.load(f)
        arxiv_sha256 = arxiv_prov.get("sha256", "")

    gen_timestamp = datetime.now(timezone.utc).isoformat()

    # Write .26 file
    lines = []
    lines.append("% VPFIT model for PKS1937-101 z_abs=3.572")
    lines.append("% Source: Cooke et al. 2024 (MNRAS, stae452) - arXiv:2402.05586")
    lines.append("% Generated by scripts/steps/build_pks1937_model.py")
    lines.append(f"% Generated at: {gen_timestamp}")
    if arxiv_sha256:
        lines.append(f"% arXiv source SHA256: {arxiv_sha256}")
    lines.append("% ESPRESSO R=70000, vsig={:.2f} km/s".format(VSIG))
    lines.append(f"% H I components: {ion_counts.get('H_I', 0)}")
    lines.append(f"% D I components: {ion_counts.get('D_I', 0)}")
    lines.append("% Reproduce: python scripts/steps/build_pks1937_model.py")
    lines.append("")

    # Region lines
    for r in regions:
        lines.append(
            f"%% {r['filename']}     {r['idx']}   {r['w_min']:.4f}   {r['w_max']:.4f} vsig={r['vsig']:.2f}  !  {r['comment']}"
        )

    lines.append("")

    # Component lines
    for c in all_components:
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

    # Check data blocks match
    with open(MANIFEST_PATH, "r") as f:
        manifest = json.load(f)

    n_blocks = 0
    n_pixels = 0
    for r in regions_parsed:
        coadd = r["filename"]
        if coadd not in manifest["coadds"]:
            continue
        for chunk in manifest["coadds"][coadd]:
            import numpy as np
            wave = np.array(chunk["wave"])
            flux = np.array(chunk["flux"])
            err = np.array(chunk["err"])
            mask = (
                (np.isfinite(flux))
                & (np.isfinite(err))
                & (err > 0)
                & (wave >= r["w_min"])
                & (wave <= r["w_max"])
            )
            if np.sum(mask) > 0:
                n_blocks += 1
                n_pixels += int(np.sum(mask))

    print(f"    Data blocks (matched): {n_blocks}")
    print(f"    Data pixels (matched): {n_pixels}")


if __name__ == "__main__":
    main()
