#!/usr/bin/env python3
"""
Gate 8 Wavelength-Systematics Sensitivity Estimate

Quantifies how the calibrated velocity-deviation p-values change when
residual wavelength-calibration systematics (0.5--1 km/s) are folded
into the true-D injection Monte Carlo spread.

Method:
  The existing Gate 8 calibration (step_08b) produced simulation
  deviation distributions with known std (sigma_fit). Wavelength-
  calibration systematics add an independent Gaussian velocity offset
  with sigma_sys. The combined spread is

      sigma_total = sqrt(sigma_fit^2 + sigma_sys^2).

  Calibrated p-values are computed two ways:
    (a) Gaussian tail: p = 2 * (1 - Phi(|obs| / sigma_total))
    (b) Monte Carlo: draw N=100000 from N(0, sigma_total^2), count
        exceedances of |obs|.

  Both use the real sigma_fit and observed deviation from the existing
  calibration results in results/gate8_calibration_*.json.
"""

import json
from pathlib import Path

import numpy as np
from scipy.stats import norm

project_root = Path(__file__).resolve().parent.parent.parent

SIGHTLINES = {
    "Q1009+2956": "gate8_calibration_Q10092956.json",
    "PKS1937-101": "gate8_calibration_PKS1937101.json",
}

SIGMA_SYS_VALUES = [0.0, 0.5, 1.0]  # km/s
N_MC = 100_000
SEED = 42


def load_calibration(filename):
    path = project_root / "results" / filename
    with open(path) as f:
        return json.load(f)


def gaussian_p(obs_abs, sigma_total):
    return 2.0 * (1.0 - norm.cdf(obs_abs / sigma_total))


def monte_carlo_p(obs_abs, sigma_total, n=N_MC, seed=SEED):
    rng = np.random.default_rng(seed)
    draws = rng.normal(0.0, sigma_total, size=n)
    return float(np.mean(np.abs(draws) >= obs_abs))


def main():
    results = {}

    for sightline, filename in SIGHTLINES.items():
        cal = load_calibration(filename)
        obs_dev = abs(cal["observed"]["deviation"])
        sigma_fit = cal["simulated_stats"]["deviation_std"]

        sightline_results = {
            "observed_deviation_kms": cal["observed"]["deviation"],
            "observed_abs_deviation_kms": obs_dev,
            "sigma_fit_kms": sigma_fit,
            "original_calibrated_p": cal["calibrated_p_values"]["velocity_deviation"],
            "original_nominal_sigma": cal["nominal_sigmas"]["velocity_deviation"],
            "systematic_cases": {},
        }

        for sigma_sys in SIGMA_SYS_VALUES:
            sigma_total = np.sqrt(sigma_fit**2 + sigma_sys**2)
            sigma_eff = obs_dev / sigma_total
            p_gauss = gaussian_p(obs_dev, sigma_total)
            p_mc = monte_carlo_p(obs_dev, sigma_total)

            sightline_results["systematic_cases"][f"sigma_sys_{sigma_sys}"] = {
                "sigma_sys_kms": sigma_sys,
                "sigma_total_kms": float(sigma_total),
                "effective_sigma": float(sigma_eff),
                "p_gaussian": float(p_gauss),
                "p_monte_carlo": p_mc,
                "n_mc": N_MC,
            }

        results[sightline] = sightline_results

        print(f"\n=== {sightline} ===")
        print(f"  |obs| = {obs_dev:.3f} km/s, sigma_fit = {sigma_fit:.4f} km/s")
        print(f"  {'sigma_sys':>10} {'sigma_total':>12} {'sigma_eff':>10} "
              f"{'p_gauss':>12} {'p_mc':>12}")
        for sigma_sys in SIGMA_SYS_VALUES:
            sc = sightline_results["systematic_cases"][f"sigma_sys_{sigma_sys}"]
            print(f"  {sigma_sys:>10.1f} {sc['sigma_total_kms']:>12.4f} "
                  f"{sc['effective_sigma']:>10.2f} "
                  f"{sc['p_gaussian']:>12.2e} {sc['p_monte_carlo']:>12.2e}")

    out = {
        "gate": "8-wavelength-systematics",
        "description": "Sensitivity of Gate 8 velocity-deviation p-values to "
                       "residual wavelength-calibration systematics",
        "method": "sigma_total = sqrt(sigma_fit^2 + sigma_sys^2); "
                  "p from Gaussian tail and Monte Carlo (N=100000)",
        "source_files": list(SIGHTLINES.values()),
        "n_mc": N_MC,
        "results": results,
    }

    out_path = project_root / "results" / "gate8_wavelength_systematics.json"
    with open(out_path, "w") as f:
        json.dump(out, f, indent=2)
    print(f"\n[COMPLETED] {out_path}")


if __name__ == "__main__":
    main()
