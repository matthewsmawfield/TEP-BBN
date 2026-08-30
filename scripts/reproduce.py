#!/usr/bin/env python3
"""
TEP-BBN Pipeline Reproducibility Entry Point.

Verifies provenance chains and/or reproduces results for all sightlines.

Usage:
    python scripts/reproduce.py --all --verify-only
    python scripts/reproduce.py --sightline PKS1937-101
    python scripts/reproduce.py --all
    python scripts/reproduce.py --sightline Q1009+2956 --skip-download
"""

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent

SIGHTLINES = {
    "Q1009+2956": {
        "config": "configs/sightlines/Q1009+2956.json",
        "manifest": "data/processed/Q1009_union_manifest.json",
        "vpfit_model": "data/literature_components/model_6a.26",
        "build_script": None,  # pre-existing model
        "gate2_prefix": "gate",
        "gate3_prefix": "gate",
    },
    "PKS1937-101": {
        "config": "configs/sightlines/PKS1937-101.json",
        "manifest": "data/processed/PKS1937-101_union_manifest.json",
        "vpfit_model": "data/literature_components/PKS1937-101_z3.572_vpfit_model.26",
        "build_script": "scripts/steps/build_pks1937_model.py",
        "arxiv_source": "data/raw/literature_source/2402.05586",
        "gate2_prefix": "gate_pks1937",
        "gate3_prefix": "gate_pks1937",
    },
    "J1332+0052": {
        "config": "configs/sightlines/J1332+0052.json",
        "manifest": "data/processed/J1332+0052_union_manifest.json",
        "vpfit_model": "data/literature_components/J1332+0052_z3.420_vpfit_model.26",
        "build_script": "scripts/steps/build_j1332_model.py",
        "arxiv_source": "data/raw/literature_source/2401.12797",
        "gate2_prefix": "gate_j1332",
        "gate3_prefix": "gate_j1332",
    },
}


def sha256_file(filepath):
    """Compute SHA256 of a file."""
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def verify_sightline(sightline_id, verbose=True):
    """Verify provenance chain for a single sightline."""
    info = SIGHTLINES[sightline_id]
    errors = []
    warnings = []
    checks = []

    # 1. Config file exists
    config_path = project_root / info["config"]
    if config_path.exists():
        checks.append(f"  ✓ Config: {info['config']}")
    else:
        errors.append(f"  ✗ Config missing: {info['config']}")

    # 2. Manifest exists with provenance
    manifest_path = project_root / info["manifest"]
    if manifest_path.exists():
        with open(manifest_path) as f:
            manifest = json.load(f)
        prov = manifest.get("provenance", {})
        if prov:
            checks.append(f"  ✓ Manifest with provenance: {info['manifest']}")
            if "raw_fits_provenance" in prov:
                checks.append(f"    - {len(prov['raw_fits_provenance'])} raw FITS files recorded")
            if "ingestion_timestamp" in prov:
                checks.append(f"    - Ingested: {prov['ingestion_timestamp']}")
        else:
            warnings.append(f"  ⚠ Manifest missing provenance section: {info['manifest']}")
    else:
        errors.append(f"  ✗ Manifest missing: {info['manifest']}")

    # 3. VPFIT model exists
    vpfit_path = project_root / info["vpfit_model"]
    if vpfit_path.exists():
        checks.append(f"  ✓ VPFIT model: {info['vpfit_model']}")
    else:
        errors.append(f"  ✗ VPFIT model missing: {info['vpfit_model']}")

    # 4. arXiv source SHA256 (if applicable)
    if "arxiv_source" in info:
        arxiv_dir = project_root / info["arxiv_source"]
        prov_file = arxiv_dir / "arxiv_provenance.json"
        if prov_file.exists():
            with open(prov_file) as f:
                arxiv_prov = json.load(f)
            recorded_sha = arxiv_prov.get("sha256", "")
            tarball = arxiv_dir / "source.tar.gz"
            if tarball.exists() and recorded_sha:
                actual_sha = sha256_file(tarball)
                if actual_sha == recorded_sha:
                    checks.append(f"  ✓ arXiv source SHA256 verified: {info['arxiv_source']}")
                else:
                    errors.append(f"  ✗ arXiv source SHA256 mismatch: {info['arxiv_source']}")
                    errors.append(f"    Recorded: {recorded_sha}")
                    errors.append(f"    Actual:   {actual_sha}")
            else:
                warnings.append(f"  ⚠ arXiv source tarball or provenance missing: {info['arxiv_source']}")
        else:
            warnings.append(f"  ⚠ arXiv provenance file missing: {prov_file}")

    # 5. Gate 2 results
    gate2_path = project_root / f"results/{info['gate2_prefix']}2_parameter_ledger.json"
    if gate2_path.exists():
        with open(gate2_path) as f:
            gate2 = json.load(f)
        t_obs = gate2.get("likelihood_ratio", {}).get("T_obs", gate2.get("T_obs", "N/A"))
        checks.append(f"  ✓ Gate 2 results: T_obs = {t_obs}")
    else:
        warnings.append(f"  ⚠ Gate 2 results missing: {gate2_path.name}")

    # 6. Gate 3 results
    gate3_path = project_root / f"results/{info['gate3_prefix']}3_significance.json"
    if gate3_path.exists():
        with open(gate3_path) as f:
            gate3 = json.load(f)
        p_val = gate3.get("p_add_one_parent", "N/A")
        n_sims = gate3.get("N_sims", "N/A")
        checks.append(f"  ✓ Gate 3 results: p_parent = {p_val}, N_sims = {n_sims}")
    else:
        warnings.append(f"  ⚠ Gate 3 results missing: {gate3_path.name}")

    if verbose:
        print(f"\n{'='*60}")
        print(f"  Sightline: {sightline_id}")
        print(f"{'='*60}")
        for c in checks:
            print(c)
        for w in warnings:
            print(w)
        for e in errors:
            print(e)

    return len(errors) == 0, errors, warnings


def reproduce_sightline(sightline_id, skip_download=False):
    """Full reproduction of a single sightline."""
    info = SIGHTLINES[sightline_id]
    print(f"\n{'='*60}")
    print(f"  Reproducing: {sightline_id}")
    print(f"{'='*60}")

    # Step 1: Build VPFIT model (if build script exists)
    if info.get("build_script"):
        print(f"\n[1/4] Building VPFIT model...")
        result = subprocess.run(
            [sys.executable, str(project_root / info["build_script"])],
            cwd=str(project_root),
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            print(f"  ✗ FAILED: {result.stderr[-500:]}")
            return False
        print(f"  ✓ Model built")

    # Step 2: Verify manifest exists
    manifest_path = project_root / info["manifest"]
    if not manifest_path.exists():
        print(f"\n[2/4] Manifest missing: {info['manifest']}")
        print(f"  Run: python scripts/ingest_sightline.py --sightline {sightline_id}")
        return False
    print(f"\n[2/4] ✓ Manifest exists")

    # Step 3: Gate 2
    print(f"\n[3/4] Running Gate 2 (spectroscopic fit verification)...")
    result = subprocess.run(
        [sys.executable, "scripts/steps/step_02_q1009.py", "--sightline", sightline_id],
        cwd=str(project_root),
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(f"  ✗ FAILED: {result.stderr[-500:]}")
        return False
    # Extract T_obs from output
    for line in result.stdout.split("\n"):
        if "T_obs" in line and "=" in line:
            print(f"  {line.strip()}")
            break
    print(f"  ✓ Gate 2 complete")

    # Step 4: Gate 3
    print(f"\n[4/4] Running Gate 3 (Monte Carlo calibration)...")
    result = subprocess.run(
        [sys.executable, "scripts/steps/step_03_significance.py", "--sightline", sightline_id],
        cwd=str(project_root),
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(f"  ✗ FAILED: {result.stderr[-500:]}")
        return False
    for line in result.stdout.split("\n"):
        if "p_add_one" in line.lower() or "exceedance" in line.lower():
            print(f"  {line.strip()}")
            break
    print(f"  ✓ Gate 3 complete")

    print(f"\n  ✓ Reproduction complete for {sightline_id}")
    return True


def main():
    parser = argparse.ArgumentParser(
        description="TEP-BBN Pipeline Reproducibility Tool"
    )
    parser.add_argument(
        "--sightline",
        choices=list(SIGHTLINES.keys()),
        help="Reproduce a single sightline",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Reproduce/verify all sightlines",
    )
    parser.add_argument(
        "--verify-only",
        action="store_true",
        help="Only verify provenance chains, do not run pipeline",
    )
    parser.add_argument(
        "--skip-download",
        action="store_true",
        help="Skip ESO archive download (use existing raw FITS)",
    )
    args = parser.parse_args()

    if not args.all and not args.sightline:
        parser.print_help()
        sys.exit(1)

    sightlines = list(SIGHTLINES.keys()) if args.all else [args.sightline]

    if args.verify_only:
        print("\nTEP-BBN Pipeline — Provenance Verification")
        print("=" * 60)
        all_ok = True
        for sl in sightlines:
            ok, errors, warnings = verify_sightline(sl)
            if not ok:
                all_ok = False
        print(f"\n{'='*60}")
        if all_ok:
            print("  ALL CHECKS PASSED ✓")
        else:
            print("  SOME CHECKS FAILED ✗")
        sys.exit(0 if all_ok else 1)
    else:
        print("\nTEP-BBN Pipeline — Full Reproduction")
        print("=" * 60)
        all_ok = True
        for sl in sightlines:
            ok = reproduce_sightline(sl, skip_download=args.skip_download)
            if not ok:
                all_ok = False
        print(f"\n{'='*60}")
        if all_ok:
            print("  ALL SIGHTLINES REPRODUCED ✓")
        else:
            print("  SOME SIGHTLINES FAILED ✗")
        sys.exit(0 if all_ok else 1)


if __name__ == "__main__":
    main()
