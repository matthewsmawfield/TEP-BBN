#!/usr/bin/env python3
"""TEP-BBN complete isotopic analysis pipeline runner.

Runs the eight final gates that validate the Temporal Equivalence Principle.
Each step writes outputs to results/.

Supports multiple sightlines via per-sightline configs in configs/sightlines/.
By default, runs the Q1009+2956 sightline (backward compatible).
Use --sightline to specify a different sightline, or --all-sightlines to
run all available sightlines that have ingested data.
"""

import argparse
import hashlib
import json
import sys
import time
import traceback
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from scripts.utils.logger import print_status, setup_step_logger
from scripts.lib.sightline_config import load_sightline_config, list_sightlines, SightlineConfigError

# Steps that are sightline-dependent (accept sightline parameter)
SIGHTLINE_STEPS = {"step_02_q1009", "step_03_significance"}

PIPELINE_STEPS = [
    ("step_01_embedding", "run_gate1", "Gate 1R: Physical Atomic-Data Embedding"),
    ("step_02_q1009", "run_gate2", "Gate 2R: Spectroscopic Fit Verification"),
    ("step_03_significance", "run_gate3", "Gate 3R: Genuine Monte Carlo Calibration"),
    ("step_04_prior", "run_gate4", "Gate 4: TEP Absorber Field Sign Closure"),
    ("step_04b_amplitude", "run_gate4b", "Gate 4B: TEP Absorber Amplitude Test"),
    (
        "step_05_thermodynamics",
        "run_gate5",
        "Gate 5: Matter-Frame Temporal Thermodynamics",
    ),
    ("step_06_helium", "run_gate6", "Gate 6: Primordial Helium Synthesis"),
    ("step_07_global_opacity", "run_step_07", "Gate 7: Global Opacity Boundary"),
    ("step_08_light_elements", "run_gate8", "Gate 8: Light-Element Network"),
]


def run_pipeline(sightline=None):
    setup_step_logger("run_pipeline")

    sightline_label = sightline if sightline else "Q1009+2956 (default)"
    print_status(f"TEP-BBN ISOTOPIC ANALYSIS PIPELINE — Sightline: {sightline_label}", "TITLE")

    completed = []
    failed = []

    for step_module, func_name, description in PIPELINE_STEPS:
        print_status(f"[RUN] {step_module}: {description}", "PROCESS")
        start = time.time()

        try:
            # Import dynamically
            module_path = f"scripts.steps.{step_module}"
            module = __import__(module_path, fromlist=[func_name])
            run_func = getattr(module, func_name)

            # Execute the step — pass sightline to sightline-dependent steps
            if step_module in SIGHTLINE_STEPS:
                run_func(sightline=sightline)
            else:
                run_func()
            elapsed = time.time() - start
            print_status(f"  [OK] {elapsed:.1f}s", "SUCCESS")
            completed.append(step_module)

        except Exception as exc:
            elapsed = time.time() - start
            print_status(f"  [FAIL] {elapsed:.1f}s: {str(exc)}", "ERROR")
            print_status(traceback.format_exc(), "ERROR")
            failed.append(step_module)
            break  # Stop the pipeline on failure

    print_status(
        f"PIPELINE COMPLETE: {len(completed)}/{len(PIPELINE_STEPS)} steps succeeded",
        "TITLE",
    )

    if not failed:
        print_status("Generating SHA-256 Checksum Manifest...", "PROCESS")
        out_dir = Path("results")
        manifest_data = {}

        raw_files = [
            Path("data/raw/atomic/H_I/H_I_lines.txt"),
            Path("data/raw/atomic/D_I/D_I_lines.txt"),
        ]

        for f in raw_files:
            if f.exists():
                with open(f, "rb") as fb:
                    manifest_data[str(f)] = hashlib.sha256(fb.read()).hexdigest()

        for f in sorted(out_dir.glob("*.json")):
            if f.name != "checksums_sha256.json":
                with open(f, "rb") as fb:
                    manifest_data[f"results/{f.name}"] = hashlib.sha256(
                        fb.read()
                    ).hexdigest()

        with open(out_dir / "checksums_sha256.json", "w") as jf:
            json.dump(manifest_data, jf, indent=2)

        print_status(
            "All 8 Gates passed verification perfectly. Repository is fully locked.",
            "SUCCESS",
        )

    if failed:
        print_status(f"FAILED: {', '.join(failed)}", "ERROR")
        sys.exit(1)


def run_all_sightlines():
    """Run the pipeline for all sightlines that have ingested data."""
    available = list_sightlines()
    if not available:
        print_status("No sightline configs found.", "ERROR")
        sys.exit(1)

    print_status(f"Available sightlines: {available}", "TITLE")

    for sl in available:
        try:
            cfg = load_sightline_config(sl)
            if cfg["_data_available"]:
                print_status(f"\n{'='*60}", "TITLE")
                print_status(f"Running pipeline for: {sl}", "TITLE")
                print_status(f"{'='*60}", "TITLE")
                run_pipeline(sightline=sl)
            else:
                print_status(f"Skipping '{sl}' — data not yet ingested", "PROCESS")
        except SightlineConfigError as e:
            print_status(f"Config error for '{sl}': {e}", "ERROR")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="TEP-BBN Pipeline Runner")
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
    args = parser.parse_args()

    if args.all_sightlines:
        run_all_sightlines()
    else:
        run_pipeline(sightline=args.sightline)
