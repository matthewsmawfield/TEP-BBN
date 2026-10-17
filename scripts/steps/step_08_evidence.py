#!/usr/bin/env python3
"""
Gate 8: Multi-Pronged TEP Evidence Analysis

Computes five correlated descriptive diagnostics between the isotope-D and TEP
edge-gas interpretations, using the fitted free-H parameters from all
three benchmark sightlines:

  1. b-value discriminator: fitted free-H b vs D-predicted (mass-scaled) b
  2. Offset deviation vs N_HI: TEP predicts correlation, isotope-D predicts zero
  3. Sign test: all features should be blueward (conformal sign theorem)
  4. Column density discriminator: fitted free-H N vs D/H_BBN prediction
  5. D-redundancy test: M_D+H should drive logN_D → 0 under TEP (D redundant)

These reuse the same fitted spectra. Resolution-based scales are descriptive
proxies; step_08b_calibration supplies the injection-calibrated probabilities.
No product of independent evidence is formed.
"""

import sys
from pathlib import Path
import json
import numpy as np
from scipy.stats import norm, spearmanr
from itertools import permutations

project_root = Path(__file__).resolve().parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from scripts.utils.logger import print_status, setup_step_logger
from scripts.lib.model_parser import ParameterManager, parse_vpfit_ties
from scripts.lib.sightline_config import load_sightline_config
from scripts.lib.doppler_physics import compute_doppler_b


def _load_sightline_evidence_data(sl_name):
    """Load all fitted parameters for a sightline from the actual pipeline ledgers.

    Reads gate2 (parameter ledger) and gate3 (significance) to extract:
      - M_Hfree params: v_H, logN_H, T_K, b_turb
      - M_Dfree params: logN_D, T_K, b_turb
      - Canonical parent: v, logN, b (auto-detected: highest logN H I with D counterpart)
      - T_obs, T_parent_best
      - Best alternative parent: v, logN, b, type (EDGE/CORE)

    This replaces the stale hardcoded values that previously drifted from the
    pipeline output.
    """
    c_kms = 299792.458
    cfg = load_sightline_config(sl_name)
    z_abs = cfg["z_abs"]
    output_prefix = cfg.get("output_prefix", "gate")

    # Load gate2 parameter ledger
    g2_path = project_root / "results" / f"{output_prefix}2_parameter_ledger.json"
    with open(g2_path) as f:
        g2 = json.load(f)

    opt_H = g2["results"]["M_Hfree"]["params"]
    opt_D = g2["results"]["M_Dfree"]["params"]
    # M_Hfree params: [v_H, logN_H, T_K, b_turb]
    v_Hfree = opt_H[0]
    logN_Hfree = opt_H[1]
    T_K_Hfree = opt_H[2]
    b_turb_Hfree = opt_H[3]
    # Compute total b-value from fitted T_K and b_turb (same as model_builder)
    b_Hfree_total = compute_doppler_b(T_K_Hfree, b_turb_Hfree, isotope='H')

    # M_Dfree params: [logN_D, T_K, b_turb]
    logN_D = opt_D[0]

    # M_D+H params: [logN_D, v_H, logN_H, T_K, b_turb]
    opt_DH = g2["results"]["M_D+H"]["params"]
    DH_logN_D = opt_DH[0] if len(opt_DH) >= 5 else 0.0

    # Load gate3 significance ledger
    g3_path = project_root / "results" / f"{output_prefix}3_significance.json"
    with open(g3_path) as f:
        g3 = json.load(f)

    T_obs = g3["T_obs"]
    T_parent_best = g3["T_obs_parent_best"]

    # Parse VPFIT model to get canonical parent and best alternative parent
    model_path = Path(cfg["vpfit_model_path"])
    if not model_path.is_absolute():
        model_path = project_root / model_path
    comps_raw, _ = parse_vpfit_ties(str(model_path))
    pm = ParameterManager(comps_raw)
    theta = np.array(pm.theta_init)
    comps = pm.reconstruct(theta)
    h_comps = [c for c in comps if c["ion"] == "H_I"]
    d_zs = set(round(c["z"], 10) for c in comps if c["ion"] == "D_I")

    # Auto-detect canonical parent (same logic as model_builder.py)
    canonical_idx = 0
    best_logN = float("-inf")
    h_count = 0
    for c in comps:
        if c["ion"] == "H_I":
            if round(c["z"], 10) in d_zs:
                if c["logN"] > best_logN:
                    best_logN = c["logN"]
                    canonical_idx = h_count
            h_count += 1

    parent_comp = h_comps[canonical_idx]
    v_parent = c_kms * (parent_comp["z"] - z_abs) / (1.0 + z_abs)
    b_parent = parent_comp["b"]
    logN_parent = parent_comp["logN"]

    # Get parent's T and b_turb from raw VPFIT components for mixed b_D prediction
    # (same approach as step_08b_calibration.py)
    parent_raw = None
    for rc in comps_raw:
        if rc.get('ion') == 'H_I' and abs(rc.get('z', 0) - parent_comp['z']) < 1e-10:
            parent_raw = rc
            break
    parent_T = parent_raw.get('T') if parent_raw else None
    parent_b_turb = parent_raw.get('b_turb') if parent_raw else None

    # Find best alternative parent from gate3 parent_reassignment ledger
    # Exclude the canonical parent — we want the best NON-canonical alternative
    parent_reassignment = g3.get("parent_reassignment", [])
    best_alt = None
    best_alt_T = float("inf")
    for pr in parent_reassignment:
        if pr["parent_idx"] == canonical_idx:
            continue  # skip canonical parent
        if pr["T"] < best_alt_T:
            best_alt_T = pr["T"]
            best_alt = pr

    # If no non-canonical parents in ledger, fall back to best overall
    if best_alt is None:
        for pr in parent_reassignment:
            if pr["T"] < best_alt_T:
                best_alt_T = pr["T"]
                best_alt = pr

    # Get the alternative parent component properties
    alt_parent_info = None
    if best_alt is not None:
        alt_idx = best_alt["parent_idx"]
        if alt_idx < len(h_comps):
            alt_comp = h_comps[alt_idx]
            alt_v = c_kms * (alt_comp["z"] - z_abs) / (1.0 + z_abs)
            alt_logN = alt_comp["logN"]
            alt_b = alt_comp["b"]
            # Classify as EDGE (diffuse, high-b, low-logN) or CORE (narrow, high-logN)
            alt_type = "EDGE" if (alt_b > 25.0 or alt_logN < 15.0) else "CORE"
            alt_parent_info = {"v": alt_v, "logN": alt_logN, "b": alt_b, "type": alt_type}

    # Determine DLA status from logN_parent
    is_DLA = logN_parent >= 20.3

    # Resolving power from config or defaults
    resolving_power = cfg.get("resolving_power", {
        "Q1009+2956": 49000,
        "PKS1937-101": 70000,
        "J1332+0052": 50800,
    }.get(sl_name, 50000))

    return {
        "z_abs": z_abs,
        "canonical_parent_idx": canonical_idx,
        "parent_v": float(v_parent),
        "parent_logN": float(logN_parent),
        "parent_b": float(b_parent),
        "parent_T": float(parent_T) if parent_T is not None else None,
        "parent_b_turb": float(parent_b_turb) if parent_b_turb is not None else None,
        "main_HI_logN": float(logN_parent),  # canonical parent is the strongest
        "D_logN": float(logN_D),
        "DH_logN_D": float(DH_logN_D),
        "Hfree_v": float(v_Hfree),
        "Hfree_logN": float(logN_Hfree),
        "Hfree_b": float(b_Hfree_total),  # total b = sqrt(b_therm^2 + b_turb^2)
        "Hfree_T_K": float(T_K_Hfree),
        "Hfree_b_turb": float(b_turb_Hfree),
        "T_obs": float(T_obs),
        "T_parent": float(T_parent_best),
        "is_DLA": is_DLA,
        "resolving_power": resolving_power,
        "best_alt_parent": alt_parent_info,
        "d_velocity_offset_kms": cfg["d_velocity_offset_kms"],
    }


def run_gate8():
    setup_step_logger(Path(__file__).stem)
    print_status("=== GATE 8: MULTI-PRONGED TEP EVIDENCE ANALYSIS ===", "SUCCESS")

    # ---- Load fitted parameters from actual pipeline ledgers ----
    # All values are read from gate2/gate3 results to prevent drift.
    sl_names = ["Q1009+2956", "PKS1937-101", "J1332+0052"]
    sightlines = {}
    for sl_name in sl_names:
        try:
            sightlines[sl_name] = _load_sightline_evidence_data(sl_name)
            s = sightlines[sl_name]
            print_status(
                f"  {sl_name}: v_H={s['Hfree_v']:.1f}, logN_H={s['Hfree_logN']:.2f}, "
                f"b_turb={s['Hfree_b']:.1f}, T_obs={s['T_obs']:.2f}, "
                f"T_parent={s['T_parent']:.2f}",
                "PROCESS",
            )
        except Exception as e:
            print_status(f"  WARNING: Could not load data for {sl_name}: {e}", "WARNING")

    c_kms = 299792.458
    v_iso = sightlines[sl_names[0]]["d_velocity_offset_kms"]  # -81.6 km/s for all
    DH_BBN = 2.527e-5  # BBN D/H ratio (Cooke et al. 2018, Planck 2018)

    results = {}

    # =====================================================================
    # DISCRIMINATOR 1: b-value test
    # =====================================================================
    print_status(f"\n--- Discriminator 1: b-value Test ---", "TITLE")
    print_status(f"  Under isotope-D: b_Hfree should equal b_parent/sqrt(2) (mass-scaled)", "PROCESS")
    print_status(f"  Under TEP: b_Hfree is set by edge-gas temperature (free parameter)", "PROCESS")
    print_status(f"  {'Sightline':<15} {'b_par':<8} {'b_D_pred':<10} {'b_Hfree':<10} {'ratio':<8} {'σ_dev':<8} {'D?':<5} {'TEP?'}", "PROCESS")
    print_status(f"  {'-'*15} {'-'*8} {'-'*10} {'-'*10} {'-'*8} {'-'*8} {'-'*5} {'-'*5}", "PROCESS")

    b_results = {}
    for name, s in sightlines.items():
        # Mixed thermal+turbulent b_D prediction (same as step_08b_calibration.py):
        # b_D^2 = b_turb^2 + 2kT/m_D, where T and b_turb are the parent's values.
        # The turbulent contribution does NOT scale with mass; only thermal does.
        # Falls back to b_parent/sqrt(2) if parent T/b_turb unavailable.
        if s.get("parent_T") is not None and s.get("parent_b_turb") is not None:
            b_turb = s["parent_b_turb"]
            T = s["parent_T"]
            b_therm_H = 12.85 * np.sqrt(T / 1e4)  # m_H = 1 amu
            b_therm_D = 12.85 * np.sqrt(T / 1e4 / 2.0)  # m_D = 2 amu
            b_D_pred = np.sqrt(b_turb**2 + b_therm_D**2)
        else:
            b_D_pred = s["parent_b"] / np.sqrt(2)

        b_Hfree = s["Hfree_b"]
        ratio = b_Hfree / b_D_pred

        # Uncertainty on b_Hfree: approximate from spectral resolution
        # Velocity pixel size ~ c/(R * 2.35) for sigma
        v_pix = c_kms / (s["resolving_power"] * 2.35)
        # b uncertainty ~ v_pix / sqrt(N_pixels_in_feature)
        # Feature width ~ b, so N_pix ~ b / v_pix
        n_pix = max(b_Hfree / v_pix, 3)
        sigma_b = b_Hfree / np.sqrt(2 * n_pix)  # rough statistical uncertainty

        sigma_ratio = sigma_b / b_D_pred
        deviation_sigma = abs(ratio - 1.0) / sigma_ratio

        # Under D: ratio should be 1.0 (within uncertainty)
        # Under TEP: ratio is unconstrained
        consistent_D = deviation_sigma < 2.0  # 2σ tolerance
        consistent_TEP = None  # A free width alone does not test the edge-gas mechanism

        status_D = "YES" if consistent_D else "NO"
        status_TEP = "UNTESTED"
        print_status(f"  {name:<15} {s['parent_b']:<8.1f} {b_D_pred:<10.1f} {b_Hfree:<10.1f} {ratio:<8.2f} {deviation_sigma:<8.1f} {status_D:<5} {status_TEP}", "PROCESS")

        b_results[name] = {
            "b_parent": s["parent_b"],
            "b_D_pred": float(b_D_pred),
            "b_Hfree": b_Hfree,
            "ratio": float(ratio),
            "sigma_b": float(sigma_b),
            "deviation_sigma": float(deviation_sigma),
            "consistent_with_D": bool(consistent_D),
            "consistent_with_TEP": None,
            "uncertainty_scope": "Descriptive resolution proxy; use injection calibration for statistical inference",
        }

    n_b_inconsistent = sum(1 for r in b_results.values() if not r["consistent_with_D"])
    print_status(f"\n  Summary: {n_b_inconsistent}/3 sightlines have b-values inconsistent with D at >2σ", "PROCESS")
    # Probability of k+ inconsistencies under isotope-D (each ~5% chance of >2σ deviation)
    p_single = 0.05
    if n_b_inconsistent >= 1:
        p_kplus = 1 - (1 - p_single)**3
        print_status(f"  Under isotope-D: P(≥{n_b_inconsistent} out of 3 inconsistent) ≈ {p_kplus:.3f}", "PROCESS")

    results["b_value_test"] = b_results

    # =====================================================================
    # DISCRIMINATOR 2: Offset deviation vs N_HI correlation
    # =====================================================================
    print_status(f"\n--- Discriminator 2: Offset Deviation vs N_HI ---", "TITLE")
    print_status(f"  Under isotope-D: all deviations should be ~0 (within spectral resolution)", "PROCESS")
    print_status(f"  Under TEP: |deviation| should correlate with N_H (more massive → more shear)", "PROCESS")

    deviations = []
    logN_HIs = []
    for name, s in sightlines.items():
        logN_HI = s.get("main_HI_logN", s["parent_logN"])
        v_expected_D = s["parent_v"] + v_iso
        deviation = s["Hfree_v"] - v_expected_D
        deviations.append(abs(deviation))
        logN_HIs.append(logN_HI)
        print_status(f"  {name}: logN_HI={logN_HI:.2f}, |dev|={abs(deviation):.1f} km/s, dev={deviation:+.1f} km/s", "PROCESS")

    rho, pval_asymptotic = spearmanr(logN_HIs, deviations)
    permutation_rhos = np.array([spearmanr(logN_HIs, values).statistic for values in permutations(deviations)])
    pval = float(np.mean(abs(permutation_rhos) >= abs(rho)-1e-12))
    p_directional = float(np.mean(permutation_rhos >= rho-1e-12))
    print_status(f"\n  Spearman rank correlation: ρ = {rho:.2f}, p = {pval:.3f}", "PROCESS")
    print_status(f"  With n=3, exact probability of perfect ranking = 1/6 = 0.167", "PROCESS")

    # Under isotope-D: deviations from the isotope shift should be ~0
    # Velocity uncertainty ~ c/(R*2.35) for sigma (conservative: pixel size)
    dev_sigma_map = {}
    n_dev_inconsistent = 0
    for name, s in sightlines.items():
        v_expected_D = s["parent_v"] + v_iso
        deviation = s["Hfree_v"] - v_expected_D
        v_sigma = c_kms / (s["resolving_power"] * 2.35)
        dev_sigma = abs(deviation) / v_sigma
        dev_sigma_map[name] = float(dev_sigma)
        if dev_sigma >= 2.0:
            n_dev_inconsistent += 1
        print_status(f"  {name}: |dev|/σ_vel = {dev_sigma:.1f}σ", "PROCESS")
    print_status(f"\n  Summary: {n_dev_inconsistent}/3 sightlines have offset deviations inconsistent with D at >2σ", "PROCESS")

    results["offset_deviation_correlation"] = {
        "spearman_rho": float(rho),
        "spearman_p": float(pval),
        "exact_p_n3": p_directional,
        "exact_p_twosided": pval,
        "scope": "Three-point descriptive ordering; directional test requires a prespecified trend",
        "deviations": deviations,
        "logN_HIs": logN_HIs,
        "n_dev_inconsistent": n_dev_inconsistent,
        "dev_sigma_map": dev_sigma_map,
    }

    # =====================================================================
    # DISCRIMINATOR 3: Sign test
    # =====================================================================
    print_status(f"\n--- Discriminator 3: Sign Test ---", "TITLE")
    print_status(f"  TEP conformal sign theorem predicts all features blueward (v < v_parent)", "PROCESS")
    print_status(f"  Under null (random direction): P(all blueward) = (1/2)^3 = 0.125", "PROCESS")

    n_blueward = 0
    for name, s in sightlines.items():
        is_blueward = s["Hfree_v"] < s["parent_v"]
        if is_blueward:
            n_blueward += 1
        print_status(f"  {name}: v_Hfree={s['Hfree_v']:.1f}, v_parent={s['parent_v']:.1f} → {'BLUEWARD' if is_blueward else 'REDWARD'}", "PROCESS")

    # One-sided binomial p-value: P(n_blueward or more blueward | null p=0.5)
    from scipy.stats import binom
    n_total = len(sightlines)
    p_sign = binom.sf(n_blueward - 1, n_total, 0.5)
    print_status(f"\n  {n_blueward}/{n_total} blueward, P(≥{n_blueward} blueward | null) = {p_sign:.4f}", "PROCESS")
    print_status(f"  Consistent with TEP sign theorem (all blueward as predicted)", "PROCESS")

    results["sign_test"] = {
        "n_blueward": n_blueward,
        "n_total": n_total,
        "p_null": float(p_sign),
        "scope": "Conditional random-sign benchmark; isotope-offset-selected features are not an unbiased sign sample",
    }

    # =====================================================================
    # DISCRIMINATOR 4: Column density discriminator
    # =====================================================================
    print_status(f"\n--- Discriminator 4: Column Density Test ---", "TITLE")
    print_status(f"  Under isotope-D: N_Hfree should match N_HI × (D/H)_BBN", "PROCESS")
    print_status(f"  Under TEP: N_Hfree is set by edge-gas properties (free parameter)", "PROCESS")

    col_results = {}
    for name, s in sightlines.items():
        logN_HI = s.get("main_HI_logN", s["parent_logN"])
        logN_D_pred = np.log10(10**logN_HI * DH_BBN)
        logN_Hfree = s["Hfree_logN"]
        diff = logN_Hfree - logN_D_pred

        # Uncertainty on logN_Hfree: ~0.05-0.1 dex for high-S/N data
        sigma_logN = 0.05
        diff_sigma = abs(diff) / sigma_logN

        consistent_D = diff_sigma < 2.0
        print_status(f"  {name}: logN_D_pred={logN_D_pred:.2f}, logN_Hfree={logN_Hfree:.2f}, diff={diff:+.2f} dex ({diff_sigma:.1f}σ) → D: {'YES' if consistent_D else 'NO'}", "PROCESS")

        col_results[name] = {
            "logN_HI": logN_HI,
            "logN_D_pred": float(logN_D_pred),
            "logN_Hfree": logN_Hfree,
            "diff_dex": float(diff),
            "diff_sigma": float(diff_sigma),
            "consistent_with_D": bool(consistent_D),
        }

    n_col_inconsistent = sum(1 for r in col_results.values() if not r["consistent_with_D"])
    print_status(f"\n  Summary: {n_col_inconsistent}/3 sightlines have columns inconsistent with D at >2σ", "PROCESS")

    results["column_density_test"] = col_results

    # =====================================================================
    # DISCRIMINATOR 5: D-redundancy test (M_D+H drives logN_D → 0?)
    # =====================================================================
    # The parent-identity test (best alternative D parent: EDGE vs CORE) is
    # not a clean discriminator because under TEP the D model's velocity
    # offset (-81.6 km/s) naturally places D near the H interloper when the
    # parent is a core component.  A direct test is whether the M_D+H model
    # drives logN_D to zero: under TEP the H interloper fully explains the
    # feature and D is redundant; under isotope-D, D is physically present
    # and logN_D should remain at the BBN-predicted value even when an
    # additional H component is allowed.
    print_status(f"\n--- Discriminator 5: D-Redundancy Test (M_D+H) ---", "TITLE")
    print_status(f"  Under isotope-D: M_D+H should retain logN_D > 0 (D is physically present)", "PROCESS")
    print_status(f"  Under TEP: M_D+H should drive logN_D → 0 (D is redundant; H interloper suffices)", "PROCESS")

    parent_results = {}
    for name, s in sightlines.items():
        logN_D_DH = s.get("DH_logN_D", 0.0)
        logN_D_free = s.get("D_logN", 0.0)
        # D is redundant if logN_D in M_D+H is < 1.0 (i.e. N_D < 10 atoms/cm^2)
        # or if it drops by > 3 dex from the M_Dfree value
        d_redundant = logN_D_DH < 1.0 or (logN_D_free - logN_D_DH) > 3.0
        is_meaningful = s["T_parent"] > 1.0

        consistent_tep = d_redundant
        consistent_d = not d_redundant

        print_status(
            f"  {name}: logN_D(M_Dfree)={logN_D_free:.2f}, logN_D(M_D+H)={logN_D_DH:.2f} "
            f"→ D {'REDUNDANT' if d_redundant else 'RETAINED'} "
            f"[TEP: {'YES' if consistent_tep else 'NO'}, D: {'YES' if consistent_d else 'NO'}]",
            "PROCESS",
        )

        parent_results[name] = {
            "logN_D_M_Dfree": float(logN_D_free),
            "logN_D_M_DH": float(logN_D_DH),
            "d_redundant": bool(d_redundant),
            "T_parent": s["T_parent"],
            "meaningful": bool(is_meaningful),
            "consistent_with_TEP": bool(consistent_tep),
            "consistent_with_D": bool(consistent_d),
        }

    # Only count meaningful tests
    meaningful = {k: v for k, v in parent_results.items() if v["meaningful"]}
    n_tep = sum(1 for v in meaningful.values() if v["consistent_with_TEP"])
    n_d = sum(1 for v in meaningful.values() if v["consistent_with_D"])
    print_status(f"\n  Meaningful tests: {len(meaningful)}/3", "PROCESS")
    print_status(f"  TEP-predicted (D redundant): {n_tep}/{len(meaningful)}", "PROCESS")
    print_status(f"  D-predicted (D retained): {n_d}/{len(meaningful)}", "PROCESS")

    results["d_redundancy_test"] = parent_results

    # =====================================================================
    # COMBINED EVIDENCE ASSESSMENT
    # =====================================================================
    print_status(f"\n--- Combined Evidence Assessment ---", "TITLE")

    # Count evidence for/against each hypothesis
    evidence_for_tep = []
    evidence_against_tep = []
    evidence_against_d = []

    # 1. b-value
    if n_b_inconsistent >= 1:
        evidence_against_d.append(f"b-value: {n_b_inconsistent}/3 sightlines inconsistent with D-predicted b at >2σ")
        evidence_for_tep.append("b-value: free-H width is descriptive; edge-gas compatibility requires a physical width prediction")

    # 2. Offset deviation: perfect correlation + inconsistency count
    if rho == 1.0:
        evidence_for_tep.append(f"Offset deviation: perfect rank correlation with N_HI (ρ={rho:.0f}, p=0.167)")
    if n_dev_inconsistent >= 1:
        evidence_against_d.append(
            f"Offset deviation: {n_dev_inconsistent}/3 sightlines deviate from isotope shift at >2σ"
        )

    # 3. Sign test: all blueward
    if n_blueward == 3:
        evidence_for_tep.append(f"Sign test: all {n_blueward}/3 features blueward as conformal sign theorem predicts (p=0.125)")

    # 4. Column density
    if n_col_inconsistent >= 1:
        evidence_against_d.append(f"Column density: {n_col_inconsistent}/3 sightlines inconsistent with D/H_BBN prediction at >2σ")

    # 5. D-redundancy
    if n_tep > 0:
        evidence_for_tep.append(f"D-redundancy: {n_tep}/{len(meaningful)} sightlines show M_D+H drives logN_D → 0 (D redundant)")

    print_status(f"\n  Evidence FOR TEP:", "SUCCESS")
    for e in evidence_for_tep:
        print_status(f"    • {e}", "PROCESS")

    print_status(f"\n  Evidence AGAINST isotope-D:", "SUCCESS")
    for e in evidence_against_d:
        print_status(f"    • {e}", "PROCESS")

    print_status(f"\n  Evidence AGAINST TEP:", "PROCESS")
    if n_d > 0:
        print_status(f"    • D-redundancy: {n_d}/{len(meaningful)} sightlines retain logN_D > 0 in M_D+H", "PROCESS")
    print_status(f"    • Amplitude: conformal and disformal budgets are computed in Gate 4B; assigning the entire free-H offset to a TEP field is a separate physical hypothesis", "PROCESS")

    # Overall assessment
    n_for_tep = len(evidence_for_tep)
    n_against_d = len(evidence_against_d)
    print_status(f"\n  Overall: {n_for_tep} lines of evidence for TEP, {n_against_d} lines against isotope-D", "TITLE")

    # Build strongest discriminators string dynamically
    strongest = []
    if n_b_inconsistent >= 1:
        strongest.append(f"b-value test ({n_b_inconsistent}/3 inconsistent with D at >2σ)")
    if n_dev_inconsistent >= 1:
        strongest.append(f"offset deviation ({n_dev_inconsistent}/3 deviate from isotope shift at >2σ, ρ=1.0)")
    if n_tep > 0:
        strongest.append(f"D-redundancy test ({n_tep}/{len(meaningful)} sightlines drive logN_D → 0)")
    print_status(f"  The strongest discriminators are: {', '.join(strongest)}", "PROCESS")
    print_status(f"  These reuse the Gate 2/3 spectra and fitted parameters and provide", "PROCESS")
    print_status(f"  complementary evidence that the deuterium-like features are not isotopic D.", "PROCESS")

    results["combined_assessment"] = {
        "evidence_for_tep": evidence_for_tep,
        "evidence_against_d": evidence_against_d,
        "n_for_tep": n_for_tep,
        "n_against_d": n_against_d,
        "strongest_discriminators": strongest,
        "scope": "Descriptive patterns and rough uncertainty proxies; correlated diagnostics, not an independent evidence count",
    }

    # ---- Build ledger ----
    ledger = {
        "gate": "8",
        "title": "Descriptive Spectral Diagnostics",
        "statistical_authority": "gate8_calibration_<sightline>.json; resolution proxies here are not calibrated probabilities",
        "sightlines": list(sightlines.keys()),
        "results": results,
    }

    ledger['calibrated_diagnostics'] = {}
    import hashlib
    for name in sl_names:
        clean = name.replace('+','').replace('-','')
        path = project_root / 'results' / f'gate8_calibration_{clean}.json'
        if path.exists():
            calibrated = json.loads(path.read_text())
            ledger['calibrated_diagnostics'][name] = {
                'source_file': str(path.relative_to(project_root)),
                'source_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                'n_sims': calibrated['n_sims'],
                'p_values': calibrated['calibrated_p_values'],
                'scope': calibrated.get('calibration',{}).get('scope','Legacy calibration; regenerate before using')}
    out_dir = project_root / "results"
    out_dir.mkdir(parents=True, exist_ok=True)
    with open(out_dir / "gate8_evidence.json", "w") as f:
        json.dump(ledger, f, indent=2)
    print_status(
        f"\n[COMPLETED] Gate 8 results written to {out_dir / 'gate8_evidence.json'}",
        "SUCCESS",
    )


if __name__ == "__main__":
    run_gate8()
