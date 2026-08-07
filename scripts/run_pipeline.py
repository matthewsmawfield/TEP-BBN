#!/usr/bin/env python3
"""TEP-BBN complete isotopic analysis pipeline runner.

Runs the seven final gates that validate the Temporal Equivalence Principle.
Each step writes outputs to results/.
"""

import hashlib
import json
import sys
import time
import traceback
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from scripts.utils.logger import print_status, setup_step_logger

PIPELINE_STEPS = [
    ("step_01_embedding", "run_gate1", "Gate 1R: Physical Atomic-Data Embedding"),
    ("step_02_q1009", "run_gate2", "Gate 2R: Immutable Q1009 Fit Verification"),
    ("step_03_significance", "run_gate3", "Gate 3R: Genuine Monte Carlo Calibration"),
    ("step_04_prior", "run_gate4", "Gate 4: TEP Absorber Field Closure"),
    (
        "step_05_thermodynamics",
        "run_gate5",
        "Gate 5: Matter-Frame Temporal Thermodynamics",
    ),
    ("step_06_helium", "run_gate6", "Gate 6: Primordial Helium Synthesis"),
    ("step_07_global_opacity", "run_step_07", "Gate 7: Global Opacity Theorem"),
]


def run_pipeline():
    setup_step_logger("run_pipeline")
    print_status("TEP-BBN FINAL ISOTOPIC ANALYSIS PIPELINE", "TITLE")

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

            # Execute the step
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
            "All 7 Gates passed verification perfectly. Repository is fully locked.",
            "SUCCESS",
        )

    if failed:
        print_status(f"FAILED: {', '.join(failed)}", "ERROR")
        sys.exit(1)


if __name__ == "__main__":
    run_pipeline()
