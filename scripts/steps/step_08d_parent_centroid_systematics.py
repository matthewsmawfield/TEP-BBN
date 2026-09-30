#!/usr/bin/env python3
"""
Gate 8 Parent-Centroid Blend-Bias Sensitivity Estimate

Quantifies how the calibrated velocity-deviation p-values change when
blend-induced bias of the fitted *parent* centroid is folded into the
true-D injection Monte Carlo spread.

Method:
  The Gate 8 observable is a relative velocity offset measured against
  the isotope-shifted position anchored to the fitted parent component:

      dev_measured = dev_true - delta_v_blend

  where delta_v_blend is the blend-induced bias of the parent's fitted
  centroid (components vs blend centre-of-light). step_08c folds the
  intra-spectrum wavelength systematic into sigma_total; this step adds
  the independent parent-centroid term:

      sigma_total = sqrt(sigma_fit^2 + sigma_sys^2 + sigma_blend^2)

  Two evaluations are reported:
    (a) Conservative null (MC): draw dev_true ~ N(0, sigma_fit^2 +
        sigma_sys^2) and delta_v_blend ~ N(0, sigma_blend^2) inside the
        same MC loop; count |dev_true - delta_v_blend| >= |obs|.
    (b) Blend-alone scenario: the delta_v_blend draw alone is asked to
        supply the whole observed deviation, p = 2(1-Phi(|obs|/sigma_blend)).
        The sigma_blend at which this reaches p = 0.05 is sigma_req =
        |obs| / 1.96 — the centroid-drag amplitude the fake-D
        interpretation requires.

  Both use the real sigma_fit and observed deviation from the existing
  calibration results in results/gate8_calibration_*.json, the
  literature sigma_sys adopted by step_08c, and b_parent / logN_HI from
  results/gate8_evidence.json.

Plausibility bound on sigma_blend:
  VPFIT centroid errors on the parent columns (logN_HI = 17.36, 17.92)
  are far below 1 km/s, so the required drag must come from an
  unresolved companion, not fit noise. For a companion inside the
  parent linewidth the centroid drag is approximately f * dv with f the
  companion's optical-depth-weighted flux fraction; a companion beyond
  ~b_parent/2 is resolved as a separate component in the fit. The
  minimum companion fraction f_min = 2|obs|/b_parent required for a
  centroid drag of |obs| is reported per sightline — a fraction of
  order unity would be visible as profile asymmetry in the residual
  spectrum and is excluded by the existing fits.

  Sign coherence: the two free-H-preferred deviations (Q1009+2956,
  PKS1937-101) are both positive. Blend bias is sign-random, so the
  blend-alone interpretation must supply same-sign drags on both
  sightlines; the joint one-sided tail is reported.

Output: results/gate8_parent_centroid_systematics.json
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
        "sigma_sys_kms": 0.25,  # step_08c literature value
    },
    "PKS1937-101": {
        "calibration_file": "gate8_calibration_PKS1937101.json",
        "instrument": "VLT/ESPRESSO",
        "sigma_sys_kms": 0.05,  # step_08c literature value
    },
    "J1332+0052": {
        "calibration_file": "gate8_calibration_J13320052.json",
        "instrument": "VLT/UVES + Keck/HIRES",
        "sigma_sys_kms": 0.20,  # step_08c literature value
    },
}

SIGMA_BLEND_SCAN = [0.0, 0.1, 0.25, 0.5, 1.0, 1.5, 2.0, 3.0, 5.0]

N_MC = 100_000
SEED = 42


def load_calibration(filename):
    with open(project_root / "results" / filename) as f:
        return json.load(f)


def gaussian_p(obs_abs, sigma_total):
    return 2.0 * (1.0 - norm.cdf(obs_abs / sigma_total))


def monte_carlo_p(obs_abs, sigma_base, sigma_blend, n=N_MC, seed=SEED):
    """dev_true ~ N(0, sigma_base) and parent-centroid drag ~ N(0, sigma_blend);
    measured deviation = dev_true - drag."""
    rng = np.random.default_rng(seed)
    dev_true = rng.normal(0.0, sigma_base, size=n)
    drag = rng.normal(0.0, sigma_blend, size=n)
    return float(np.mean(np.abs(dev_true - drag) >= obs_abs))


def main():
    evidence = json.load(open(project_root / "results" / "gate8_evidence.json"))
    bvt = evidence["results"]["b_value_test"]

    results = {}
    joint_signed = {}  # one-sided (sign-matched) blend-alone tails per sightline

    for sightline, config in SIGHTLINES.items():
        cal = load_calibration(config["calibration_file"])
        obs_dev = float(cal["observed"]["deviation"])
        obs_abs = abs(obs_dev)
        sigma_fit = float(cal["simulated_stats"]["deviation_std"])
        sigma_sys = config["sigma_sys_kms"]
        sigma_base = float(np.sqrt(sigma_fit**2 + sigma_sys**2))
        b_parent = float(bvt[sightline]["b_parent"])

        # blend-alone required amplitude
        sigma_req = obs_abs / 1.959964  # p = 0.05 two-sided
        f_min = 2.0 * obs_abs / b_parent  # companion inside b/2

        cases = {}
        for sb in SIGMA_BLEND_SCAN:
            sigma_total = float(np.sqrt(sigma_base**2 + sb**2))
            p_mc = monte_carlo_p(obs_abs, sigma_base, sb)
            p_gauss = gaussian_p(obs_abs, sigma_total)
            p_blend_alone = gaussian_p(obs_abs, sb) if sb > 0 else 0.0
            cases[f"sigma_blend_{sb:.2f}"] = {
                "sigma_blend_kms": sb,
                "sigma_total_kms": sigma_total,
                "p_monte_carlo": p_mc,
                "p_gaussian": float(p_gauss),
                "p_blend_alone_twosided": float(p_blend_alone),
                "effective_sigma_vs_null": float(obs_abs / sigma_total),
            }

        # signed blend-alone tail for the observed sign
        def signed_tail(sb):
            if sb <= 0:
                return 0.0
            return float(1.0 - norm.cdf(obs_dev / sb)) if obs_dev > 0 else float(
                norm.cdf(obs_dev / sb)
            )

        joint_signed[sightline] = {f"sigma_blend_{sb:.2f}": signed_tail(sb) for sb in SIGMA_BLEND_SCAN}

        results[sightline] = {
            "instrument": config["instrument"],
            "observed_deviation_kms": obs_dev,
            "observed_abs_deviation_kms": obs_abs,
            "sigma_fit_kms": sigma_fit,
            "sigma_sys_kms": sigma_sys,
            "sigma_base_kms": sigma_base,
            "b_parent_kms": b_parent,
            "blend_alone_required_sigma_kms": float(sigma_req),
            "required_drag_fraction_of_b_parent": float(obs_abs / b_parent),
            "min_companion_flux_fraction_at_half_linewidth": float(f_min),
            "systematic_cases": cases,
        }

        print(f"\n=== {sightline} ({config['instrument']}) ===")
        print(f"  |obs| = {obs_abs:.3f} km/s, sigma_base = {sigma_base:.4f} km/s, b_parent = {b_parent:.2f} km/s")
        print(f"  blend-alone needs sigma_blend >= {sigma_req:.2f} km/s; "
              f"drag = {obs_abs/b_parent:.0%} of b_parent; f_min = {f_min:.2f}")
        print(f"  {'sigma_blend':>11} {'sigma_total':>12} {'sigma_eff':>10} "
              f"{'p_gauss':>12} {'p_mc':>12} {'p_blend_alone':>14}")
        for sb in SIGMA_BLEND_SCAN:
            k = f"sigma_blend_{sb:.2f}"
            sc = cases[k]
            print(f"  {sb:>11.2f} {sc['sigma_total_kms']:>12.4f} "
                  f"{sc['effective_sigma_vs_null']:>10.2f} "
                  f"{sc['p_gaussian']:>12.2e} {sc['p_monte_carlo']:>12.2e} "
                  f"{sc['p_blend_alone_twosided']:>14.2e}")

    # joint same-sign blend-alone probability for the two free-H-preferred
    # sightlines (J1332 deviation is already consistent with isotope-D)
    joint = {}
    for sb in SIGMA_BLEND_SCAN:
        k = f"sigma_blend_{sb:.2f}"
        jp = joint_signed["Q1009+2956"][k] * joint_signed["PKS1937-101"][k]
        joint[k] = {
            "sigma_blend_kms": sb,
            "joint_onesided_p_Q1009_x_PKS1937": float(jp),
        }

    out = {
        "gate": "8-parent-centroid-systematics",
        "description": "Sensitivity of Gate 8 velocity-deviation p-values to "
                       "blend-induced bias of the fitted parent centroid, "
                       "perturbing the parent velocity by its blend "
                       "uncertainty inside the MC loop",
        "method": "dev_measured = dev_true - delta_v_blend; "
                  "sigma_total = sqrt(sigma_fit^2 + sigma_sys^2 + sigma_blend^2); "
                  "MC N=100000; blend-alone and joint sign-matched tails reported",
        "plausibility_bound": (
            "VPFIT centroid errors on logN_HI = 17.36-17.92 columns are far "
            "below 1 km/s; a centroid drag of |obs| requires an unresolved "
            "companion at f >= 2|obs|/b_parent inside half a linewidth — "
            "visible as residual asymmetry for f of order tens of percent. "
            "Blend bias is sign-random; the two free-H-preferred sightlines "
            "additionally require same-sign drags."
        ),
        "source_files": [SIGHTLINES[s]["calibration_file"] for s in SIGHTLINES]
        + ["gate8_evidence.json"],
        "n_mc": N_MC,
        "results": results,
        "joint_sign_matched": joint,
    }

    out_path = project_root / "results" / "gate8_parent_centroid_systematics.json"
    with open(out_path, "w") as f:
        json.dump(out, f, indent=2)
    print(f"\n[COMPLETED] {out_path}")


if __name__ == "__main__":
    main()
