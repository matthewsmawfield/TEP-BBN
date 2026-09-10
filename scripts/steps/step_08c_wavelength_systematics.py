#!/usr/bin/env python3
"""
Gate 8 Wavelength-Systematics Sensitivity Estimate

Quantifies how the calibrated velocity-deviation p-values change when
residual wavelength-calibration systematics are folded into the true-D
injection Monte Carlo spread.

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

Literature-based sigma_sys per sightline:
  The relevant systematic is the intra-spectrum wavelength distortion
  that can shift the apparent velocity of one component relative to
  another within the same echelle order, since the Gate 8 observable
  is a *relative* velocity offset (free-H vs isotope-shifted position),
  not an absolute wavelength measurement. Absolute wavelength offsets
  and inter-night drifts cancel in the relative measurement.

  Q1009+2956 (Keck/HIRES, ThAr, no supercalibration):
    sigma_sys = 0.25 km/s
    Griest et al. (2009), ApJ 708, 158: intra-order distortions ~250 m/s
    measured via iodine-cell supercalibration of HIRES ThAr pipeline.

  PKS1937-101 (VLT/ESPRESSO, ThAr+Fabry-Perot):
    sigma_sys = 0.05 km/s
    Schmidt et al. (2021), A&A 646, A104: wavelength-dependent
    discrepancies between ThAr+FP and laser frequency comb up to 24 m/s;
    50 m/s adopted as conservative upper bound.

  J1332+0052 (VLT/UVES + Keck/HIRES):
    sigma_sys = 0.20 km/s
    Whitmore & Murphy (2014), MNRAS 444, 2: long-range distortions
    ~200 m/s per 1000 A for UVES/HIRES archival spectra via
    solar-twin/asteroid supercalibration.
"""

import json
from pathlib import Path

import numpy as np
from scipy.stats import norm

project_root = Path(__file__).resolve().parent.parent.parent

SIGHTLINES = {
    "Q1009+2956": {
        "calibration_file": "gate8_calibration_Q10092956.json",
        "instrument": "Keck/HIRES",
        "calibration": "ThAr (no supercalibration)",
        "sigma_sys_literature_kms": 0.25,
        "sigma_sys_reference": "Griest et al. (2009), ApJ 708, 158",
        "sigma_sys_basis": "Intra-order distortion ~250 m/s measured via iodine-cell supercalibration of HIRES ThAr pipeline",
    },
    "PKS1937-101": {
        "calibration_file": "gate8_calibration_PKS1937101.json",
        "instrument": "VLT/ESPRESSO",
        "calibration": "ThAr + Fabry-Perot",
        "sigma_sys_literature_kms": 0.05,
        "sigma_sys_reference": "Schmidt et al. (2021), A&A 646, A104",
        "sigma_sys_basis": "Wavelength-dependent discrepancies up to 24 m/s between ThAr+FP and laser frequency comb; 50 m/s adopted as conservative upper bound",
    },
    "J1332+0052": {
        "calibration_file": "gate8_calibration_J13320052.json",
        "instrument": "VLT/UVES + Keck/HIRES",
        "calibration": "ThAr (no supercalibration)",
        "sigma_sys_literature_kms": 0.20,
        "sigma_sys_reference": "Whitmore & Murphy (2014), MNRAS 444, 2",
        "sigma_sys_basis": "Long-range distortions ~200 m/s per 1000 A for UVES/HIRES archival spectra via solar-twin/asteroid supercalibration",
    },
}

# Sensitivity scan grid (km/s) — common to all sightlines for transparency
SIGMA_SYS_SCAN = [0.0, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.50, 1.00]

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

    for sightline, config in SIGHTLINES.items():
        cal = load_calibration(config["calibration_file"])
        obs_dev = abs(cal["observed"]["deviation"])
        sigma_fit = cal["simulated_stats"]["deviation_std"]
        sigma_sys_lit = config["sigma_sys_literature_kms"]

        sightline_results = {
            "instrument": config["instrument"],
            "calibration": config["calibration"],
            "observed_deviation_kms": cal["observed"]["deviation"],
            "observed_abs_deviation_kms": obs_dev,
            "sigma_fit_kms": sigma_fit,
            "original_calibrated_p": cal["calibrated_p_values"]["velocity_deviation"],
            "original_nominal_sigma": cal["nominal_sigmas"]["velocity_deviation"],
            "sigma_sys_literature": {
                "value_kms": sigma_sys_lit,
                "reference": config["sigma_sys_reference"],
                "basis": config["sigma_sys_basis"],
                "systematic_type": "intra-spectrum relative velocity distortion (not absolute offset)",
            },
            "systematic_cases": {},
        }

        # Build scan grid: literature value + common scan points
        scan_values = sorted(set(SIGMA_SYS_SCAN + [sigma_sys_lit]))

        for sigma_sys in scan_values:
            sigma_total = np.sqrt(sigma_fit**2 + sigma_sys**2)
            sigma_eff = obs_dev / sigma_total
            p_gauss = gaussian_p(obs_dev, sigma_total)
            p_mc = monte_carlo_p(obs_dev, sigma_total)

            case_key = f"sigma_sys_{sigma_sys:.2f}"
            sightline_results["systematic_cases"][case_key] = {
                "sigma_sys_kms": sigma_sys,
                "sigma_total_kms": float(sigma_total),
                "effective_sigma": float(sigma_eff),
                "p_gaussian": float(p_gauss),
                "p_monte_carlo": p_mc,
                "n_mc": N_MC,
                "is_literature_value": bool(abs(sigma_sys - sigma_sys_lit) < 1e-9),
            }

        # Highlight the literature-based result
        lit_key = f"sigma_sys_{sigma_sys_lit:.2f}"
        lit_case = sightline_results["systematic_cases"][lit_key]
        sightline_results["literature_result"] = {
            "sigma_sys_kms": sigma_sys_lit,
            "sigma_total_kms": lit_case["sigma_total_kms"],
            "effective_sigma": lit_case["effective_sigma"],
            "p_gaussian": lit_case["p_gaussian"],
            "p_monte_carlo": lit_case["p_monte_carlo"],
            "reference": config["sigma_sys_reference"],
        }

        results[sightline] = sightline_results

        print(f"\n=== {sightline} ({config['instrument']}) ===")
        print(f"  |obs| = {obs_dev:.3f} km/s, sigma_fit = {sigma_fit:.4f} km/s")
        print(f"  Literature sigma_sys = {sigma_sys_lit:.2f} km/s ({config['sigma_sys_reference']})")
        print(f"  {'sigma_sys':>10} {'sigma_total':>12} {'sigma_eff':>10} "
              f"{'p_gauss':>12} {'p_mc':>12} {'lit?':>5}")
        for sigma_sys in scan_values:
            case_key = f"sigma_sys_{sigma_sys:.2f}"
            sc = sightline_results["systematic_cases"][case_key]
            lit_flag = "*" if sc["is_literature_value"] else ""
            print(f"  {sigma_sys:>10.2f} {sc['sigma_total_kms']:>12.4f} "
                  f"{sc['effective_sigma']:>10.2f} "
                  f"{sc['p_gaussian']:>12.2e} {sc['p_monte_carlo']:>12.2e} {lit_flag:>5}")

    out = {
        "gate": "8-wavelength-systematics",
        "description": "Sensitivity of Gate 8 velocity-deviation p-values to "
                       "residual wavelength-calibration systematics, with "
                       "literature-based sigma_sys per sightline",
        "method": "sigma_total = sqrt(sigma_fit^2 + sigma_sys^2); "
                  "p from Gaussian tail and Monte Carlo (N=100000)",
        "systematic_model": "Intra-spectrum relative velocity distortion (not absolute offset). "
                            "The Gate 8 observable is a relative velocity offset between "
                            "free-H and isotope-shifted position within the same spectrum; "
                            "absolute wavelength offsets and inter-night drifts cancel.",
        "source_files": [SIGHTLINES[s]["calibration_file"] for s in SIGHTLINES],
        "n_mc": N_MC,
        "results": results,
    }

    out_path = project_root / "results" / "gate8_wavelength_systematics.json"
    with open(out_path, "w") as f:
        json.dump(out, f, indent=2)
    print(f"\n[COMPLETED] {out_path}")


if __name__ == "__main__":
    main()
