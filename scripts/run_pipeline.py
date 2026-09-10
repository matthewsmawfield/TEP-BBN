#!/usr/bin/env python3
"""TEP-BBN complete isotopic analysis pipeline runner.

Runs all gates and analyses that validate the Temporal Equivalence Principle.
Each step writes outputs to results/ and logs to logs/.

Pipeline phases:
  Phase 1 — Core Gates (1–8): Atomic embedding, spectroscopic fit, MC calibration,
            TEP sign closure, amplitude, thermodynamics, helium, opacity, light elements
  Phase 2 — Disformal Transport (Gate 4B closure + screening plot)
  Phase 3 — Secondary Robustness Analyses (C2 scaffold, C3 perturbed MC, C4 kinematic)
  Phase 4 — Manuscript Number Finalization + SHA-256 checksum manifest

Supports multiple sightlines via per-sightline configs in configs/sightlines/.
By default, runs the Q1009+2956 sightline (backward compatible).
Use --sightline to specify a different sightline, or --all-sightlines to
run all available sightlines that have ingested data.

Usage:
    python scripts/run_pipeline.py                    # Full pipeline (Q1009, 1000 MC)
    python scripts/run_pipeline.py --quick            # Quick mode (50 MC, skip C3)
    python scripts/run_pipeline.py --sightline PKS1937-101
    python scripts/run_pipeline.py --all-sightlines
    python scripts/run_pipeline.py --skip-secondary   # Skip C2/C3/C4
"""

import argparse
import hashlib
import json
import sys
import time
import traceback
from datetime import datetime
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from scripts.utils.logger import print_status, setup_step_logger
from scripts.lib.sightline_config import load_sightline_config, list_sightlines, SightlineConfigError

# ─── Pipeline Definition ───────────────────────────────────────────────────

# Steps that are sightline-dependent (accept sightline parameter)
SIGHTLINE_STEPS = {"step_02_q1009", "step_03_significance", "secondary_analyses"}

# Phase 1: Core Gates (sightline-dependent steps get sightline kwarg)
CORE_STEPS = [
    ("step_01_embedding", "run_gate1", "Gate 1R: Physical Atomic-Data Embedding", "core"),
    ("step_02_q1009", "run_gate2", "Gate 2R: Spectroscopic Fit Verification", "core"),
    ("step_03_significance", "run_gate3", "Gate 3R: Genuine Monte Carlo Calibration", "core"),
    ("step_04_prior", "run_gate4", "Gate 4: TEP Absorber Field Sign Closure", "core"),
    ("step_04b_amplitude", "run_gate4b", "Gate 4B: TEP Absorber Amplitude Test", "core"),
    ("step_05_thermodynamics", "run_gate5", "Gate 5: Matter-Frame Temporal Thermodynamics", "core"),
    ("step_06_helium", "run_gate6", "Gate 6: Primordial Helium Synthesis", "core"),
    ("step_07_global_opacity", "run_step_07", "Gate 7: Global Opacity Boundary", "core"),
    ("step_08_light_elements", "run_gate8", "Gate 8: Light-Element Network", "core"),
]

# Phase 2: Disformal Transport
DISFORMAL_STEPS = [
    ("step_09_disformal_transport", "run_gate4b_closure", "Gate 4B Closure: Disformal Transport Solver", "disformal"),
    ("step_04h_disformal_clock", "run_disformal_clock", "Gate 4B-IV: Disformal Clock Closure (cosmological d0phi)", "disformal"),
    ("step_09b_screening_plot", "main", "Gate 4B: Screening Function Plot", "disformal"),
]

# Phase 3: Secondary Robustness Analyses
SECONDARY_STEPS = [
    ("secondary_analyses", "run_all_secondary_analyses", "Secondary Analyses (C2 + C3 + C4)", "secondary"),
]

# Phase 4: Finalization
FINALIZE_STEPS = [
    ("finalize_manuscript_numbers", "main", "Manuscript Number Finalization", "finalize"),
]


def _run_step(step_module, func_name, description, phase, sightline, quick, n_sims, n_free):
    """Execute a single pipeline step with timing and error handling.

    Returns (success: bool, elapsed: float, output_json: str or None).
    """
    print_status(f"[RUN] {step_module}: {description}", "PROCESS")
    start = time.time()

    try:
        module_path = f"scripts.steps.{step_module}"
        if step_module == "finalize_manuscript_numbers":
            module_path = "scripts.finalize_manuscript_numbers"
        module = __import__(module_path, fromlist=[func_name])
        run_func = getattr(module, func_name)

        # Build kwargs based on step type
        kwargs = {}
        if step_module in SIGHTLINE_STEPS:
            kwargs["sightline"] = sightline

        # MC simulation count: --n-sims overrides, else quick=50, else full=1000
        if step_module == "step_03_significance":
            kwargs["n_sims"] = n_sims
        if step_module == "secondary_analyses":
            kwargs["n_sims"] = n_sims
            kwargs["n_free_components"] = n_free

        # Execute
        result = run_func(**kwargs)
        elapsed = time.time() - start
        print_status(f"  [OK] {elapsed:.1f}s", "SUCCESS")
        return True, elapsed, result

    except Exception as exc:
        elapsed = time.time() - start
        print_status(f"  [FAIL] {elapsed:.1f}s: {str(exc)}", "ERROR")
        print_status(traceback.format_exc(), "ERROR")
        return False, elapsed, None


def _generate_checksum_manifest():
    """Generate SHA-256 checksum manifest for all results and atomic data."""
    project_root = Path(__file__).resolve().parent.parent
    out_dir = project_root / "results"
    manifest_data = {}

    raw_files = [
        project_root / "data" / "raw" / "atomic" / "H_I" / "H_I_lines.txt",
        project_root / "data" / "raw" / "atomic" / "D_I" / "D_I_lines.txt",
    ]

    for f in raw_files:
        if f.exists():
            with open(f, "rb") as fb:
                manifest_data[str(f.relative_to(project_root))] = hashlib.sha256(fb.read()).hexdigest()

    for f in sorted(out_dir.glob("*.json")):
        if f.name != "checksums_sha256.json":
            with open(f, "rb") as fb:
                manifest_data[f"results/{f.name}"] = hashlib.sha256(fb.read()).hexdigest()

    manifest_path = out_dir / "checksums_sha256.json"
    with open(manifest_path, "w") as jf:
        json.dump(manifest_data, jf, indent=2)

    print_status(f"SHA-256 manifest: {manifest_path} ({len(manifest_data)} files)", "SUCCESS")
    return manifest_path


def _generate_pipeline_summary(sightline, completed, failed, skipped, step_timings, quick):
    """Write a comprehensive pipeline summary JSON to results/."""
    project_root = Path(__file__).resolve().parent.parent
    out_dir = project_root / "results"

    # Collect all result JSON files
    result_files = {}
    for f in sorted(out_dir.glob("*.json")):
        if f.name in ("checksums_sha256.json", "pipeline_summary.json"):
            continue
        try:
            with open(f) as fh:
                data = json.load(fh)
            result_files[f.name] = {
                "size_bytes": f.stat().st_size,
                "keys": list(data.keys()) if isinstance(data, dict) else f"<{type(data).__name__}>",
            }
        except (json.JSONDecodeError, Exception):
            result_files[f.name] = {"size_bytes": f.stat().st_size, "keys": "<unreadable>"}

    summary = {
        "pipeline_run": {
            "timestamp": datetime.now().isoformat(),
            "sightline": sightline or "Q1009+2956",
            "mode": "quick" if quick else "full",
            "total_steps": len(completed) + len(failed) + len(skipped),
            "completed": len(completed),
            "failed": len(failed),
            "skipped": len(skipped),
            "all_passed": len(failed) == 0,
        },
        "step_results": {
            "completed": completed,
            "failed": failed,
            "skipped": skipped,
        },
        "step_timings": step_timings,
        "result_files": result_files,
    }

    summary_path = out_dir / "pipeline_summary.json"
    with open(summary_path, "w") as f:
        json.dump(summary, f, indent=2)
    print_status(f"Pipeline summary: {summary_path}", "SUCCESS")
    return summary_path


def run_pipeline(sightline=None, quick=False, skip_secondary=False, skip_disformal=False,
                 n_sims=None, n_free=5):
    """Run the complete TEP-BBN pipeline.

    Args:
        sightline: Sightline ID (default: Q1009+2956)
        quick: If True, use reduced MC (50 sims) for faster testing
        skip_secondary: If True, skip C2/C3/C4 robustness checks
        skip_disformal: If True, skip Gate 4B closure and screening plot
        n_sims: Override MC simulation count (default: from config or 1000)
        n_free: C2 number of freed components (default: 5)
    """
    setup_step_logger("run_pipeline")

    sightline_label = sightline if sightline else "Q1009+2956 (default)"
    mode_label = "QUICK" if quick else "FULL"
    print_status(
        f"TEP-BBN ISOTOPIC ANALYSIS PIPELINE — Sightline: {sightline_label} — Mode: {mode_label}",
        "TITLE",
    )

    completed = []
    failed = []
    skipped = []
    step_timings = {}

    # Determine MC simulation count
    if n_sims is None:
        n_sims = 50 if quick else 1000

    # ─── Phase 1: Core Gates ───────────────────────────────────────────────
    print_status("PHASE 1: CORE GATES (1–8)", "TITLE")

    for step_module, func_name, description, phase in CORE_STEPS:
        success, elapsed, _ = _run_step(
            step_module, func_name, description, phase, sightline, quick, n_sims, n_free
        )
        step_timings[step_module] = {"elapsed": elapsed, "status": "OK" if success else "FAIL"}
        if success:
            completed.append(step_module)
        else:
            failed.append(step_module)
            print_status(f"Pipeline stopped at {step_module}", "ERROR")
            _generate_pipeline_summary(sightline, completed, failed, skipped, step_timings, quick)
            print_status(f"PIPELINE FAILED: {', '.join(failed)}", "ERROR")
            sys.exit(1)

    # ─── Phase 2: Disformal Transport ──────────────────────────────────────
    if skip_disformal:
        print_status("PHASE 2: DISFORMAL TRANSPORT — SKIPPED", "TITLE")
        for step_module, _, description, _ in DISFORMAL_STEPS:
            skipped.append(step_module)
            step_timings[step_module] = {"elapsed": 0, "status": "SKIPPED"}
            print_status(f"  [SKIP] {step_module}: {description}", "PROCESS")
    else:
        print_status("PHASE 2: DISFORMAL TRANSPORT", "TITLE")
        for step_module, func_name, description, phase in DISFORMAL_STEPS:
            success, elapsed, _ = _run_step(
                step_module, func_name, description, phase, sightline, quick, n_sims, n_free
            )
            step_timings[step_module] = {"elapsed": elapsed, "status": "OK" if success else "FAIL"}
            if success:
                completed.append(step_module)
            else:
                failed.append(step_module)
                print_status(f"Pipeline stopped at {step_module}", "ERROR")
                _generate_pipeline_summary(sightline, completed, failed, skipped, step_timings, quick)
                print_status(f"PIPELINE FAILED: {', '.join(failed)}", "ERROR")
                sys.exit(1)

    # ─── Phase 3: Secondary Robustness Analyses ────────────────────────────
    if skip_secondary:
        print_status("PHASE 3: SECONDARY ROBUSTNESS — SKIPPED", "TITLE")
        for step_module, _, description, _ in SECONDARY_STEPS:
            skipped.append(step_module)
            step_timings[step_module] = {"elapsed": 0, "status": "SKIPPED"}
            print_status(f"  [SKIP] {step_module}: {description}", "PROCESS")
    else:
        print_status("PHASE 3: SECONDARY ROBUSTNESS ANALYSES (C2 + C3 + C4)", "TITLE")
        for step_module, func_name, description, phase in SECONDARY_STEPS:
            success, elapsed, _ = _run_step(
                step_module, func_name, description, phase, sightline, quick, n_sims, n_free
            )
            step_timings[step_module] = {"elapsed": elapsed, "status": "OK" if success else "FAIL"}
            if success:
                completed.append(step_module)
            else:
                failed.append(step_module)
                print_status(f"Secondary analysis {step_module} failed, continuing...", "WARNING")

    # ─── Phase 4: Finalization ─────────────────────────────────────────────
    print_status("PHASE 4: MANUSCRIPT FINALIZATION", "TITLE")
    for step_module, func_name, description, phase in FINALIZE_STEPS:
        success, elapsed, _ = _run_step(
            step_module, func_name, description, phase, sightline, quick, n_sims, n_free
        )
        step_timings[step_module] = {"elapsed": elapsed, "status": "OK" if success else "FAIL"}
        if success:
            completed.append(step_module)
        else:
            failed.append(step_module)
            print_status(f"Finalization {step_module} failed, continuing to checksums...", "WARNING")

    # ─── Checksum Manifest ─────────────────────────────────────────────────
    print_status("GENERATING SHA-256 CHECKSUM MANIFEST", "TITLE")
    _generate_checksum_manifest()

    # ─── Pipeline Summary ──────────────────────────────────────────────────
    print_status("GENERATING PIPELINE SUMMARY", "TITLE")
    _generate_pipeline_summary(sightline, completed, failed, skipped, step_timings, quick)

    # ─── Final Report ──────────────────────────────────────────────────────
    total = len(completed) + len(failed) + len(skipped)
    print_status(
        f"PIPELINE COMPLETE: {len(completed)}/{total} succeeded, "
        f"{len(failed)} failed, {len(skipped)} skipped",
        "TITLE",
    )

    # Print timing table
    print_status("", "INFO")
    print_status("Step Timings:", "INFO")
    print_status(f"  {'Step':<40} {'Status':<10} {'Time':>10}", "INFO")
    print_status(f"  {'-'*40} {'-'*10} {'-'*10}", "INFO")
    for step, info in step_timings.items():
        print_status(
            f"  {step:<40} {info['status']:<10} {info['elapsed']:>8.1f}s",
            "INFO",
        )
    total_time = sum(info["elapsed"] for info in step_timings.values())
    print_status(f"  {'-'*40} {'-'*10} {'-'*10}", "INFO")
    print_status(f"  {'TOTAL':<40} {'':<10} {total_time:>8.1f}s", "INFO")

    if not failed:
        print_status(
            "All gates and analyses passed. Repository is fully locked.",
            "SUCCESS",
        )
    else:
        print_status(
            f"Completed with failures: {', '.join(failed)}",
            "WARNING",
        )

    if failed:
        sys.exit(1)


def run_all_sightlines(quick=False, skip_secondary=False, skip_disformal=False):
    """Run the pipeline for all sightlines that have ingested data."""
    available = list_sightlines()
    if not available:
        print_status("No sightline configs found.", "ERROR")
        sys.exit(1)

    print_status(f"Available sightlines: {available}", "TITLE")

    all_ok = True
    for sl in available:
        try:
            cfg = load_sightline_config(sl)
            if cfg["_data_available"]:
                print_status(f"\n{'='*60}", "TITLE")
                print_status(f"Running pipeline for: {sl}", "TITLE")
                print_status(f"{'='*60}", "TITLE")
                run_pipeline(
                    sightline=sl,
                    quick=quick,
                    skip_secondary=skip_secondary,
                    skip_disformal=skip_disformal,
                )
            else:
                print_status(f"Skipping '{sl}' — data not yet ingested", "PROCESS")
        except SightlineConfigError as e:
            print_status(f"Config error for '{sl}': {e}", "ERROR")
            all_ok = False

    if not all_ok:
        sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="TEP-BBN Pipeline Runner — Complete analysis pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/run_pipeline.py                    # Full pipeline (Q1009, 1000 MC)
  python scripts/run_pipeline.py --quick            # Quick mode (50 MC, faster testing)
  python scripts/run_pipeline.py --sightline PKS1937-101
  python scripts/run_pipeline.py --all-sightlines
  python scripts/run_pipeline.py --skip-secondary   # Skip C2/C3/C4
  python scripts/run_pipeline.py --skip-disformal   # Skip Gate 4B closure/plot
  python scripts/run_pipeline.py --n-sims 500       # Custom MC count
        """,
    )
    parser.add_argument(
        "--sightline",
        default=None,
        help="Sightline ID (default: Q1009+2956)",
    )
    parser.add_argument(
        "--all-sightlines",
        action="store_true",
        help="Run pipeline for all sightlines with ingested data",
    )
    parser.add_argument(
        "--quick",
        action="store_true",
        help="Quick mode: reduced MC (50 sims) for faster testing",
    )
    parser.add_argument(
        "--skip-secondary",
        action="store_true",
        help="Skip C2/C3/C4 robustness analyses",
    )
    parser.add_argument(
        "--skip-disformal",
        action="store_true",
        help="Skip Gate 4B closure and screening plot",
    )
    parser.add_argument(
        "--n-sims",
        type=int,
        default=None,
        help="Override MC simulation count (default: 1000, or 50 in --quick)",
    )
    parser.add_argument(
        "--n-free",
        type=int,
        default=5,
        help="C2: Number of H I components to free (default: 5)",
    )
    args = parser.parse_args()

    if args.all_sightlines:
        run_all_sightlines(
            quick=args.quick,
            skip_secondary=args.skip_secondary,
            skip_disformal=args.skip_disformal,
        )
    else:
        run_pipeline(
            sightline=args.sightline,
            quick=args.quick,
            skip_secondary=args.skip_secondary,
            skip_disformal=args.skip_disformal,
            n_sims=args.n_sims,
            n_free=args.n_free,
        )
