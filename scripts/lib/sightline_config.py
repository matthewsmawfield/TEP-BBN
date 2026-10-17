#!/usr/bin/env python3
"""Per-sightline configuration loader for the TEP-BBN pipeline.

Each sightline (e.g., Q1009+2956, PKS 1937-1009, HS 0105+1619) has a
JSON config in configs/sightlines/ that specifies:
  - Data manifest path (processed union manifest)
  - VPFIT model path (literature components)
  - Noise model path (per-sightline Student-t profile)
  - Absorber redshift
  - Candidate parameter bounds (velocity, column, temperature, turbulence)
  - Multi-start initial points for M_H and M_D
  - Monte Carlo settings (N_sims, seed base)

The Q1009 config reproduces the exact hardcoded values from the
pre-refactor pipeline, ensuring bit-identical results.
"""

import json
from pathlib import Path
from typing import Any, Dict, Optional

project_root = Path(__file__).resolve().parent.parent.parent

# Registry of available sightline configs
SIGHTLINE_CONFIG_DIR = project_root / "configs" / "sightlines"

# Default sightline (backward compatibility)
DEFAULT_SIGHTLINE = "Q1009+2956"


class SightlineConfigError(Exception):
    """Raised when a sightline config is missing or invalid."""


def load_sightline_config(sightline: Optional[str] = None) -> Dict[str, Any]:
    """Load and validate a sightline configuration.

    Args:
        sightline: Sightline identifier (e.g., "Q1009+2956").
                   If None, uses DEFAULT_SIGHTLINE.

    Returns:
        Validated config dict with resolved absolute paths.

    Raises:
        SightlineConfigError: If config file is missing or invalid.
    """
    if sightline is None:
        sightline = DEFAULT_SIGHTLINE

    config_path = SIGHTLINE_CONFIG_DIR / f"{sightline}.json"

    if not config_path.exists():
        available = sorted(
            f.stem for f in SIGHTLINE_CONFIG_DIR.glob("*.json")
        )
        raise SightlineConfigError(
            f"Sightline config not found: {config_path}\n"
            f"Available sightlines: {available}"
        )

    with open(config_path, "r") as f:
        config = json.load(f)

    # Validate required fields
    required = [
        "sightline_id",
        "manifest_path",
        "vpfit_model_path",
        "noise_model_path",
        "z_abs",
        "candidate_bounds",
        "multistart",
        "monte_carlo",
    ]
    missing = [k for k in required if k not in config]
    if missing:
        raise SightlineConfigError(
            f"Sightline config '{sightline}' missing fields: {missing}"
        )

    # Validate candidate_bounds structure
    cb = config["candidate_bounds"]
    for model in ("M_Dfree", "M_Hfree", "M_D+H"):
        if model not in cb:
            raise SightlineConfigError(
                f"candidate_bounds missing model '{model}' in '{sightline}'"
            )
        for param in ("init", "bounds", "n"):
            if param not in cb[model]:
                raise SightlineConfigError(
                    f"candidate_bounds.{model} missing '{param}' in '{sightline}'"
                )

    # Validate multistart
    ms = config["multistart"]
    for key in ("M_Dfree", "M_Hfree"):
        if key not in ms or not isinstance(ms[key], list):
            raise SightlineConfigError(
                f"multistart missing '{key}' list in '{sightline}'"
            )

    # Validate monte_carlo
    mc = config["monte_carlo"]
    for key in ("n_sims", "seed_base"):
        if key not in mc:
            raise SightlineConfigError(
                f"monte_carlo missing '{key}' in '{sightline}'"
            )

    # Resolve paths to absolute
    config["_manifest_abs"] = str(project_root / config["manifest_path"])
    config["_vpfit_abs"] = str(project_root / config["vpfit_model_path"])
    config["_noise_abs"] = str(project_root / config["noise_model_path"])

    # Check data availability
    config["_data_available"] = (
        Path(config["_manifest_abs"]).exists()
        and Path(config["_vpfit_abs"]).exists()
        and Path(config["_noise_abs"]).exists()
    )

    return config


def list_sightlines() -> list:
    """List all available sightline configs."""
    if not SIGHTLINE_CONFIG_DIR.exists():
        return []
    return sorted(f.stem for f in SIGHTLINE_CONFIG_DIR.glob("*.json"))
