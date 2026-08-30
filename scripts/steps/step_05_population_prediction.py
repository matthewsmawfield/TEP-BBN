#!/usr/bin/env python3
"""
Gate 6-II: Orphan Feature Population Prediction

Quantitative estimate of the expected surface density of "orphan" narrow
components (edge-shear features at offsets other than -81.6 km/s) in
existing high-S/N LLS samples.

The velocity-selection theorem (Gate 6) predicts that the D-identification
protocol filters for features at |Δv - v_iso| < ε, so any edge-shear feature
at other offsets is absorbed into the H I component structure and never
flagged as D. This script estimates:

1. The expected number of orphan features per sightline, given:
   - The TEP prediction that edge-shear features have a broad velocity
     distribution (set by the core-edge geometry), not concentrated at v_iso
   - The observed narrow-component statistics in existing LLS surveys
   - The selection function of the D-search protocol

2. The surface density of orphan features in high-S/N LLS samples,
   given the number of sightlines with sufficient S/N and spectral resolution

3. A quantitative forecast for a companion population study
"""

import sys
from pathlib import Path
import json
import numpy as np

project_root = Path(__file__).resolve().parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from scripts.utils.logger import print_status, setup_step_logger


def run_population_prediction():
    setup_step_logger(Path(__file__).stem)
    print_status("=== GATE 6-II: ORPHAN FEATURE POPULATION PREDICTION ===", "SUCCESS")

    # ---- Parameters ----
    # D-search protocol selection function
    v_iso = 81.6  # km/s, exact isotope shift
    epsilon_search = 5.0  # km/s, typical search tolerance for D identification

    # Velocity prior range for narrow components in LLS
    # (from observed velocity spreads of H I components in D/H sightlines)
    v_prior = 500.0  # km/s, half-width of plausible narrow-component velocities

    # TEP prediction: edge-shear features are distributed broadly
    # The shear amplitude |Δv_T| depends on core-edge geometry
    # The deviations from v_iso are read from the Gate 8 evidence file
    # (which reads from Gate 2 fitted M_Hfree velocities).

    evidence_path = project_root / "results" / "gate8_evidence.json"
    if evidence_path.exists():
        with open(evidence_path) as f:
            evidence = json.load(f)
        odc = evidence["results"]["offset_deviation_correlation"]
        observed_deviations = np.array(odc["deviations"])
        print_status(f"  Read deviations from gate8_evidence.json: {observed_deviations}", "PROCESS")
    else:
        # Fallback to hardcoded values
        observed_deviations = np.array([2.7, 5.7, -37.6])  # km/s
        print_status(f"  WARNING: gate8_evidence.json not found, using hardcoded deviations", "WARN")
    sigma_shear = np.std(observed_deviations, ddof=1)  # sample std

    print_status(f"\n--- Input Parameters ---", "TITLE")
    print_status(f"  v_iso = {v_iso} km/s", "PROCESS")
    print_status(f"  Search tolerance epsilon = {epsilon_search} km/s", "PROCESS")
    print_status(f"  Velocity prior half-width = {v_prior} km/s", "PROCESS")
    print_status(f"  Observed deviations from v_iso: {observed_deviations} km/s", "PROCESS")
    print_status(f"  Inferred shear spread sigma = {sigma_shear:.1f} km/s", "PROCESS")

    # ---- 1. Selection fraction ----
    # The D-search protocol identifies features within ±epsilon of v_iso
    # The fraction of edge-shear features that fall in this window:
    # f_sel = P(|Δv - v_iso| < epsilon) = 2*Phi(epsilon/sigma_shear) - 1
    # (assuming Gaussian distribution of shear offsets around v_iso)

    from scipy.stats import norm
    f_sel = 2 * norm.cdf(epsilon_search / sigma_shear) - 1
    f_orphan = 1 - f_sel  # fraction that are "orphans" (not identified as D)

    print_status(f"\n--- 1. Selection Fraction ---", "TITLE")
    print_status(f"  f_sel (identified as D) = {f_sel:.3f}", "PROCESS")
    print_status(f"  f_orphan (absorbed into H I) = {f_orphan:.3f}", "PROCESS")
    print_status(f"  Ratio orphan/identified = {f_orphan/f_sel:.1f}", "PROCESS")

    # ---- 2. Expected orphan count per sightline ----
    # If TEP predicts that EVERY LLS with sufficient core-edge contrast
    # produces an edge-shear feature, then the number of orphans per
    # sightline is approximately:
    # N_orphan ~ f_orphan / f_sel * N_identified
    #
    # For the 3 benchmark sightlines, 3 D features are identified
    # Expected orphans = 3 * f_orphan/f_sel

    n_identified = 3  # the three benchmark sightlines
    n_orphan_expected = n_identified * f_orphan / f_sel

    print_status(f"\n--- 2. Expected Orphans in Benchmark Sample ---", "TITLE")
    print_status(f"  N_identified (benchmark) = {n_identified}", "PROCESS")
    print_status(f"  N_orphan expected = {n_orphan_expected:.1f}", "PROCESS")
    print_status(f"  These are narrow H I components at non-isotope offsets", "PROCESS")
    print_status(f"  that are actually edge-shear features misidentified as H I", "PROCESS")

    # ---- 3. Surface density in existing LLS samples ----
    # Number of high-S/N LLS spectra with R > 30000 and S/N > 20
    # that have been surveyed for D/H:
    # - SQUAD DR1 (Zavarygin et al. 2018): ~100 LLS at z > 2
    # - Cooke et al. 2014+2018 sample: ~15 pristine D/H sightlines
    # - ESPRESSO D/H survey (Cooke et al. 2024): ~10 systems
    # - Total high-quality LLS with Lyman series coverage: ~50-100

    n_lls_surveyed = 80  # conservative estimate of high-S/N LLS with full Lyman coverage
    # Fraction with sufficient core-edge contrast to produce detectable shear
    # (not all LLS have the right geometry — need unscreened edge + dense core)
    f_detectable_geometry = 0.3  # ~30% of LLS have suitable core-edge contrast

    n_shear_features = n_lls_surveyed * f_detectable_geometry
    n_identified_survey = n_shear_features * f_sel
    n_orphan_survey = n_shear_features * f_orphan

    print_status(f"\n--- 3. Surface Density in Existing LLS Samples ---", "TITLE")
    print_status(f"  N_LLS surveyed (high-S/N, R>30000) ~ {n_lls_surveyed}", "PROCESS")
    print_status(f"  Fraction with detectable core-edge geometry ~ {f_detectable_geometry}", "PROCESS")
    print_status(f"  N_shear features expected ~ {n_shear_features:.0f}", "PROCESS")
    print_status(f"  N_identified as D ~ {n_identified_survey:.0f}", "PROCESS")
    print_status(f"  N_orphan (misidentified as H I) ~ {n_orphan_survey:.0f}", "PROCESS")

    # ---- 4. Observational signature of orphans ----
    # Orphan features are narrow H I components with:
    # - b-values smaller than typical H I (because edge gas is cool)
    # - velocity offsets from the main complex NOT at v_iso
    # - columns tracking the edge-gas prediction (log N_HI ~ 12-14)
    # - anomalously narrow for their column (thermal, low-T)

    print_status(f"\n--- 4. Observational Signature of Orphan Features ---", "TITLE")
    print_status(f"  Orphan features are predicted to have:", "PROCESS")
    print_status(f"    - Narrow b-values (edge gas is cool, b ~ 5-15 km/s)", "PROCESS")
    print_status(f"    - Velocity offsets NOT at ±{v_iso} km/s from parent", "PROCESS")
    print_status(f"    - Low columns (log N_HI ~ 12-14, edge gas)", "PROCESS")
    print_status(f"    - Thermal Doppler parameters (low turbulence)", "PROCESS")
    print_status(f"  The predicted velocity distribution of orphans is:", "PROCESS")
    print_status(f"    Gaussian centered on v_iso with sigma ~ {sigma_shear:.0f} km/s", "PROCESS")
    print_status(f"    (broader than the isotope shift, set by geometry variation)", "PROCESS")

    # ---- 5. Quantitative forecast ----
    # In a sample of N sightlines, the expected number of orphan features
    # at velocity offset |Δv - v_iso| > delta_v is:
    # N_orphan(>delta_v) = N_shear * P(|Δv - v_iso| > delta_v)

    delta_v_values = np.array([5, 10, 20, 30, 50])
    print_status(f"\n--- 5. Quantitative Forecast ---", "TITLE")
    print_status(f"  In a sample of {n_lls_surveyed} high-S/N LLS sightlines:", "PROCESS")
    print_status(f"  {'delta_v (km/s)':<15} {'P(>delta_v)':<12} {'N_orphan':<10} {'N_per_10_sightlines':<20}", "PROCESS")
    print_status(f"  {'-'*15} {'-'*12} {'-'*10} {'-'*20}", "PROCESS")

    forecast = []
    for dv in delta_v_values:
        p_gt = 2 * (1 - norm.cdf(dv / sigma_shear))
        n_orph = n_shear_features * p_gt
        n_per_10 = n_orph / (n_lls_surveyed / 10)
        print_status(f"  {dv:<15} {p_gt:<12.3f} {n_orph:<10.1f} {n_per_10:<20.2f}", "PROCESS")
        forecast.append({
            "delta_v_kms": float(dv),
            "probability": float(p_gt),
            "n_orphan_total": float(n_orph),
            "n_per_10_sightlines": float(n_per_10),
        })

    # ---- 6. Testable prediction ----
    print_status(f"\n--- 6. Testable Prediction ---", "TITLE")
    print_status(f"  In a re-analysis of existing high-S/N LLS spectra:", "PROCESS")
    print_status(f"  1. Identify all narrow H I components (b < 15 km/s) at", "PROCESS")
    print_status(f"     |v - v_main| < {v_prior:.0f} km/s in each sightline", "PROCESS")
    print_status(f"  2. Exclude components at |Δv - v_iso| < {epsilon_search} km/s", "PROCESS")
    print_status(f"     (these are the identified D candidates)", "PROCESS")
    print_status(f"  3. The remaining narrow components are orphan candidates", "PROCESS")
    print_status(f"  4. Predicted count: ~{n_orphan_survey:.0f} across {n_lls_surveyed} sightlines", "PROCESS")
    print_status(f"     (~{n_orphan_survey/n_lls_surveyed:.1f} per sightline)", "PROCESS")
    print_status(f"  5. Under the isotope-D null, orphan candidates should show", "PROCESS")
    print_status(f"     no excess at low b-values beyond the normal H I population", "PROCESS")
    print_status(f"  6. Under TEP, orphan candidates should show:", "PROCESS")
    print_status(f"     - An excess of narrow (b < 10 km/s) components", "PROCESS")
    print_status(f"     - A velocity distribution broader than v_iso", "PROCESS")
    print_status(f"     - Columns tracking the edge-gis prediction (log N ~ 12-14)", "PROCESS")
    print_status(f"  This is a targetable observational program using", "SUCCESS")
    print_status(f"  existing archival data (SQUAD, UVES SLS, ESPRESSO D/H survey).", "SUCCESS")

    # ---- Build ledger ----
    ledger = {
        "gate": "6-II",
        "title": "Orphan Feature Population Prediction",
        "input_parameters": {
            "v_iso_kms": v_iso,
            "epsilon_search_kms": epsilon_search,
            "v_prior_kms": v_prior,
            "observed_deviations_kms": observed_deviations.tolist(),
            "sigma_shear_kms": float(sigma_shear),
        },
        "selection_fraction": {
            "f_sel": float(f_sel),
            "f_orphan": float(f_orphan),
            "ratio_orphan_to_identified": float(f_orphan / f_sel),
        },
        "benchmark_sample": {
            "n_identified": n_identified,
            "n_orphan_expected": float(n_orphan_expected),
        },
        "survey_forecast": {
            "n_lls_surveyed": n_lls_surveyed,
            "f_detectable_geometry": f_detectable_geometry,
            "n_shear_features": float(n_shear_features),
            "n_identified_as_D": float(n_identified_survey),
            "n_orphan": float(n_orphan_survey),
            "n_orphan_per_sightline": float(n_orphan_survey / n_lls_surveyed),
        },
        "forecast_by_delta_v": forecast,
        "observational_signature": {
            "b_range_kms": "5-15 (cool edge gas)",
            "column_range": "log N_HI ~ 12-14 (edge gas)",
            "doppler_regime": "thermal (low turbulence)",
            "velocity_distribution": f"Gaussian centered on v_iso with sigma ~ {sigma_shear:.0f} km/s",
        },
        "testable_prediction": (
            f"In a re-analysis of {n_lls_surveyed} high-S/N LLS spectra, "
            f"~{n_orphan_survey:.0f} orphan narrow H I components at |Δv - v_iso| > {epsilon_search} km/s "
            f"are predicted. Under the isotope-D null, no excess of narrow components "
            f"at non-isotope offsets is expected. Under TEP, an excess of narrow (b < 10 km/s) "
            f"components with low columns (log N ~ 12-14) and a velocity distribution broader "
            f"than the isotope shift is predicted. This is testable with existing archival data."
        ),
    }

    out_dir = project_root / "results"
    out_dir.mkdir(parents=True, exist_ok=True)
    with open(out_dir / "gate6_population_prediction.json", "w") as f:
        json.dump(ledger, f, indent=2)
    print_status(
        f"\n[COMPLETED] Gate 6-II results written to {out_dir / 'gate6_population_prediction.json'}",
        "SUCCESS",
    )


if __name__ == "__main__":
    run_population_prediction()
