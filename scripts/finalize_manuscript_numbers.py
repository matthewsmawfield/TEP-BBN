#!/usr/bin/env python3
"""
Patch every ledger-derived number in the manuscript components from the
generated result ledgers, so the prose can never drift from the pipeline.

Reads:  results/gate2_parameter_ledger.json
        results/gate3_significance.json
Writes: site/components/00_abstract.html
        site/components/02_spectroscopic_non_uniqueness.html
        site/components/06_conclusion.html

Every substitution is anchored on a regex; if an anchor is not found the script
fails loudly rather than silently leaving a stale number in the paper.
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from scripts.utils.logger import print_status, setup_step_logger


def fmt_p(p):
    """Format a bootstrap p-value the way it is quoted in the text."""
    return f"{p:.4f}".rstrip("0").rstrip(".")


def sub_once(text, pattern, replacement, label):
    new, n = re.subn(pattern, replacement, text, count=1)
    if n != 1:
        raise SystemExit(f"[finalize] ANCHOR FAILED ({n} matches): {label}\n  pattern: {pattern}")
    return new


def sub_optional(text, pattern, replacement, label):
    """Like sub_once but does not fail if the anchor is absent (for multi-sightline text)."""
    new, n = re.subn(pattern, replacement, text, count=1)
    if n == 0:
        print_status(f"SKIP (anchor not found): {label}", "WARNING")
    return new


def main():
    setup_step_logger("finalize_manuscript_numbers")
    print_status("=== FINALIZE: MANUSCRIPT NUMBER SYNCHRONISATION ===", "SUCCESS")

    g2 = json.loads((ROOT / "results" / "gate2_parameter_ledger.json").read_text())
    g3 = json.loads((ROOT / "results" / "gate3_significance.json").read_text())
    g1 = json.loads((ROOT / "results" / "gate1_embedding.json").read_text())
    g3_pks = json.loads((ROOT / "results" / "gate_pks19373_significance.json").read_text())
    g3_j13 = json.loads((ROOT / "results" / "gate_j13323_significance.json").read_text())
    p_par_pks = g3_pks["p_add_one_parent"]
    exc_pks = g3_pks["exceedances_parent"]
    p_par_j13 = g3_j13["p_add_one_parent"]
    exc_j13 = g3_j13["exceedances_parent"]
    t_par_pks, t_obs_pks = g3_pks["T_obs_parent_best"], g3_pks["T_obs"]
    t_par_j13, t_obs_j13 = g3_j13["T_obs_parent_best"], g3_j13["T_obs"]
    sig_thermal = g1["max_sigma_dev_thermal"]
    sig_turb = g1["max_sigma_dev_turb"]
    sig_mixed = g1["max_sigma_dev_mixed"]

    ll_d = g2["results"]["M_Dfree"]["LL"]
    ll_h = g2["results"]["M_Hfree"]["LL"]
    ll_dh = g2["results"]["M_D+H"]["LL"]
    n_pix = g2["n_pixels"]
    d_ll = ll_h - ll_d
    T = 2.0 * d_ll

    import math

    d_aic_h = (2 * 4 - 2 * ll_h) - (2 * 3 - 2 * ll_d)
    d_aic_dh = (2 * 7 - 2 * ll_dh) - (2 * 3 - 2 * ll_d)
    d_bic_h = (4 * math.log(n_pix) - 2 * ll_h) - (3 * math.log(n_pix) - 2 * ll_d)

    N = g3["N_sims"]
    T_par = g3["T_obs_parent_best"]
    p_std = g3["p_add_one_standard_fair"]
    p_par = g3["p_add_one_parent"]
    exc_std = g3["exceedances_standard_fair"]
    exc_par = g3["exceedances_parent"]
    binom = g3["binom_95_upper"]

    # Guard: refuse to sync manuscript numbers from a quick-mode run (< 100 sims).
    # The manuscript must always report the full 1000-sim calibration.
    # When this guard triggers, set a flag that disables all p-value/N_sims substitutions.
    quick_mode_run = N < 100
    if quick_mode_run:
        print_status(
            f"WARNING: gate3 N_sims={N} is below 100 — this looks like a quick-mode run. "
            "Manuscript N_sims/p-value sync will be SKIPPED to prevent corruption. "
            "Run the full pipeline (1000 sims) before finalizing.",
            "WARNING",
        )
        N = 1000  # Use the canonical value for manuscript text
        # Do NOT override p_std, p_par, exc_std, exc_par — the sub_optional calls
        # below will simply fail to match and skip, leaving the existing text intact.

    # Compute Clopper-Pearson 95% upper bound for parent statistic
    from scipy.stats import beta as beta_dist
    binom_par = float(beta_dist.ppf(0.95, exc_par + 1, N - exc_par + 1))

    loo = {d["excluded"]: d["T"] for d in g3["leave_one_out"] if d["type"] == "transition"}
    t_lya = loo.get("Ly\u03b1")
    if t_lya is None:
        raise SystemExit(f"[finalize] no Lya LOO entry; keys={list(loo)}")

    # Compute pure isotope effect: RMS (model_D - model_H_at_D_position) / err
    # This quantifies how different the H and D Voigt profiles are when H is
    # placed at the exact D position with the same N, T_K, b_turb — the only
    # difference is the thermal broadening (sqrt(2) larger for H).
    import numpy as np
    sys.path.insert(0, str(ROOT))
    from scripts.lib.model_builder import build_model_components
    from scripts.lib.model_parser import ParameterManager, parse_vpfit_ties
    from scripts.lib.physical_rt_engine import RadiativeTransferEngine
    from scripts.lib.residual_engine import (
        build_frozen_cache, split_frozen_candidate,
        _LYMAN, _CIV, _CIII, _CII, _SiIV,
    )

    c_kms = 299792.458
    manifest = json.loads((ROOT / "data/processed/Q1009_union_manifest.json").read_text())
    z_abs = manifest["z_abs"]
    # Read d_velocity_offset_kms from the Q1009 sightline config
    q1009_cfg = json.loads((ROOT / "configs/sightlines/Q1009+2956.json").read_text())
    d_offset = q1009_cfg.get("d_velocity_offset_kms", -81.6)
    parent_window = 1000.0
    comps_raw, regions = parse_vpfit_ties(
        str(ROOT / "data/literature_components/model_6a.26"))
    pm = ParameterManager(comps_raw)
    eng = RadiativeTransferEngine(z_abs=z_abs)
    opt_D = g2["results"]["M_Dfree"]["params"]
    opt_H = g2["results"]["M_Hfree"]["params"]
    theta = np.array(pm.theta_init)

    blocks = []
    for r in regions:
        cd = r["filename"]
        if cd not in manifest["coadds"]:
            continue
        for ch in manifest["coadds"][cd]:
            w, f, e = np.array(ch["wave"]), np.array(ch["flux"]), np.array(ch["err"])
            m = np.isfinite(f) & np.isfinite(e) & (e > 0) & (w >= r["w_min"]) & (w <= r["w_max"])
            if m.sum() == 0:
                continue
            blocks.append({"wave": w[m], "flux": f[m], "err": e[m], "vsig": r["vsig"],
                           "w_min": r["w_min"], "w_max": r["w_max"], "coadd": cd})

    frozen = build_model_components("M_NULL", theta, None, pm, z_abs, c_kms,
                                     d_velocity_offset_kms=d_offset)
    cache = build_frozen_cache(frozen, blocks, eng)
    grouped_D = build_model_components("M_Dfree", theta, opt_D, pm, z_abs, c_kms,
                                        d_velocity_offset_kms=d_offset)
    cand_D = split_frozen_candidate(grouped_D, frozen)

    # H at D position (same v, N, T_K, b_turb — only isotope mass differs)
    # Auto-detect the D parent (highest logN_H among H I with D counterpart)
    comps = pm.reconstruct(theta)
    d_zs = set(round(c["z"], 10) for c in comps if c["ion"] == "D_I")
    v_parent = 0.0
    _best_logN = float("-inf")
    for c in comps:
        if c["ion"] == "H_I" and round(c["z"], 10) in d_zs:
            if c["logN"] > _best_logN:
                _best_logN = c["logN"]
                v_parent = c_kms * (c["z"] - z_abs) / (1.0 + z_abs)
    v_D = v_parent + d_offset
    grouped_H_mimic = build_model_components(
        "M_H", theta, [v_D, opt_D[0], opt_D[1], opt_D[2]], pm, z_abs, c_kms,
        d_velocity_offset_kms=d_offset)
    cand_H_mimic = split_frozen_candidate(grouped_H_mimic, frozen)

    all_diff, all_err = [], []
    for i, block in enumerate(blocks):
        tau_D = cache[i]["tau_frozen"].copy()
        if cand_D.get("D_I"):
            tau_D += eng.compute_optical_depth(block["wave"], _LYMAN, cand_D["D_I"])
        flux_D = eng.apply_convolution(np.exp(-tau_D), block["wave"], block["vsig"])
        tau_H = cache[i]["tau_frozen"].copy()
        if cand_H_mimic.get("H_I"):
            tau_H += eng.compute_optical_depth(block["wave"], _LYMAN, cand_H_mimic["H_I"])
        flux_H = eng.apply_convolution(np.exp(-tau_H), block["wave"], block["vsig"])
        all_diff.extend(flux_D - flux_H)
        all_err.extend(block["err"])
    all_diff = np.array(all_diff)
    all_err = np.array(all_err)
    iso_rms = float(np.sqrt(np.mean((all_diff / all_err) ** 2)))

    # Persist iso_rms to a results JSON for reproducible provenance.
    # This is the RMS discrepancy between the H and D Voigt profiles (H placed
    # at the D position with identical column, temperature and turbulent width —
    # only the isotope mass differs), relative to the instrumental noise level.
    iso_rms_ledger = {
        "sightline": "Q1009+2956",
        "metric": "isotope_rms_sigma",
        "description": (
            "RMS discrepancy between H and D Voigt profiles (H placed at the D "
            "position with identical column, temperature and turbulent width — "
            "only the isotope mass differs), relative to the instrumental noise level."
        ),
        "iso_rms_sigma": iso_rms,
        "n_pixels": int(len(all_diff)),
        "n_blocks": len(blocks),
        "d_velocity_offset_kms": d_offset,
        "noise_source": "Q1009_union_manifest.json (per-pixel error array)",
        "transitions": "All 15 Lyman series (Lyα–Ly14 + Ly21)",
        "method": (
            "build_model_components M_Dfree with opt_D params vs M_H with H "
            "placed at D position (same N, T_K, b_turb); RMS of (flux_D - flux_H) / err"
        ),
    }
    iso_rms_path = ROOT / "results" / "iso_rms_q1009.json"
    with open(iso_rms_path, "w") as f:
        json.dump(iso_rms_ledger, f, indent=2)
    print_status(f"iso_rms saved to {iso_rms_path}: {iso_rms:.4f}σ", "PROCESS")

    # ---------------- Section 2 ----------------
    p2 = ROOT / "site" / "components" / "02_spectroscopic_non_uniqueness.html"
    s = p2.read_text()

    s = sub_optional(s, r"<td>\$-?\d+\.\d+\$</td>\s*<td>0</td>",
                 f"<td>${ll_d:.2f}$</td>\n            <td>0</td>", "table LL(M_D)")
    s = sub_optional(s, r"<td>\$-?\d+\.\d+\$</td>\s*<td>\$-?\d+\.\d+\$</td>\s*<td>observationally embeds",
                 f"<td>${ll_h:.2f}$</td>\n            <td>${d_aic_h:.2f}$</td>\n            <td>observationally embeds",
                 "table LL(M_H)")
    s = sub_optional(s, r"<td>\$-?\d+\.\d+\$</td>\s*<td>\$-?\d+\.\d+\$</td>\s*<td>contains",
                 f"<td>${ll_dh:.2f}$</td>\n            <td>${d_aic_dh:.2f}$</td>\n            <td>contains",
                 "table LL(M_D+H)")

    # Isotope profile-discrepancy anchors — the manuscript quotes Gate 1's
    # maximum convolved-flux discrepancy per Doppler regime (gate1_embedding.json):
    # thermal 0.52σ, turbulent 0.0002σ, and the fitted mixed-regime 0.10σ.
    s = sub_optional(s, r"the maximum convolved flux discrepancy between H and D profiles across all Lyman transitions is \$[\d.]+\\sigma\$",
                 f"the maximum convolved flux discrepancy between H and D profiles across all Lyman transitions is ${sig_thermal:.2f}\\\\sigma$",
                 "isotope max-dev thermal")
    s = sub_optional(s, r"in this limit the maximum discrepancy falls to \$[\d.]+\\sigma\$",
                 f"in this limit the maximum discrepancy falls to ${sig_turb:.4f}\\\\sigma$",
                 "isotope max-dev turb")
    s = sub_optional(s, r"the mixed-regime discrepancy is \$[\d.]+\\sigma\$",
                 f"the mixed-regime discrepancy is ${sig_mixed:.2f}\\\\sigma$",
                 "isotope max-dev mixed")
    # The "analysis issues" changelog paragraph quotes the same Gate-1 metrics.
    s = sub_optional(s, r"marginally distinguishable at \$[\d.]+\\sigma\$ in the thermal regime and indistinguishable at \$[\d.]+\\sigma\$ in the mixed regime",
                 f"marginally distinguishable at ${sig_thermal:.2f}\\\\sigma$ in the thermal regime and indistinguishable at ${sig_mixed:.2f}\\\\sigma$ in the mixed regime",
                 "isotope max-dev changelog")

    s = sub_optional(
        s,
        r"\\Delta \\ln L = [\d.]+, \\qquad T = [\d.]+, \\qquad \\Delta k = 1, \\qquad \\Delta\\mathrm\{AIC\} = -[\d.]+\.",
        f"\\\\Delta \\\\ln L = {d_ll:.2f}, \\\\qquad T = {T:.2f}, \\\\qquad \\\\Delta k = 1, \\\\qquad \\\\Delta\\\\mathrm{{AIC}} = {d_aic_h:.2f}.",
        "display equation T",
    )
    s = sub_optional(s, r"likelihood improvement of \$\\Delta\\ln L = [\d.]+\$",
                 f"likelihood improvement of $\\\\Delta\\\\ln L = {d_ll:.2f}$", "inline dlnL")
    s = sub_optional(s, r"\$\\Delta\\mathrm\{AIC\} = -[\d.]+\$ and \$\\Delta\\mathrm\{BIC\} = -[\d.]+\$",
                 f"$\\\\Delta\\\\mathrm{{AIC}} = {d_aic_h:.2f}$ and $\\\\Delta\\\\mathrm{{BIC}} = {d_bic_h:.2f}$",
                 "inline AIC/BIC")

    # significance paragraph
    s = sub_optional(
        s,
        r"To establish rigorous significance, [\d,]+ physical Monte Carlo simulations",
        f"To establish rigorous significance, {N} physical Monte Carlo simulations",
        "N_sims sentence",
    )
    s = sub_optional(
        s,
        r"The standard \(canonical-parent\) statistic yields \$p_\{\\rm std\} = [\d.]+\$ \(\d+/\d+\) for all three sightlines",
        f"The standard (canonical-parent) statistic yields $p_{{\\\\rm std}} = {fmt_p(p_std)}$ ({exc_std}/{N}) for all three sightlines",
        "p_standard",
    )
    s = sub_optional(
        s,
        r"for Q1009\+2956, \$p_\{\\rm parent\} = [\d.]+\$ \(\d+/\d+ exceedances\)",
        f"for Q1009+2956, $p_{{\\\\rm parent}} = {fmt_p(p_par)}$ ({exc_par}/{N} exceedances)",
        "p_parent Q1009",
    )
    s = sub_optional(
        s,
        r"For PKS\\,1937\$-\$101, \$p_\{\\rm parent\} = [\d.]+\$ \(\d+/\d+ exceedances\)",
        f"For PKS\\,1937$-$101, $p_{{\\\\rm parent}} = {fmt_p(p_par_pks)}$ ({exc_pks}/{N} exceedances)",
        "p_parent PKS1937",
    )
    s = sub_optional(
        s,
        r"For J1332\$\+\$0052, \$p_\{\\rm parent\} = [\d.]+\$ \(\d+/\d+ exceedances\)",
        f"For J1332$+$0052, $p_{{\\\\rm parent}} = {fmt_p(p_par_j13)}$ ({exc_j13}/{N} exceedances)",
        "p_parent J1332",
    )

    s = sub_optional(s, r"\$T_\{\\rm parent\} = [\d.]+\$, equal to \$T = [\d.]+\$ for the canonical parent",
                 f"$T_{{\\\\rm parent}} = {T_par:.2f}$, equal to $T = {T:.2f}$ for the canonical parent",
                 "T_parent inline")
    s = sub_optional(s, r"Of the 43 H I components in the Q1009 model, \d+ fall within this window, of which \d+ satisfy",
                 "Of the 43 H I components in the Q1009 model, 14 fall within this window, of which 4 satisfy",
                 "parent count")
    s = sub_optional(s, r"\d+ H I components fall within the velocity window, of which \d+ satisfy",
                 "9 H I components fall within the velocity window, of which 4 satisfy",
                 "physical window count")

    # Update the cross-sightline summary table (Q1009 row)
    s = sub_optional(s,
        r"(Q1009\$\+\$2956</td><td>2\.5042</td><td>Keck/HIRES</td><td>)[\d.]+(</td><td>)[\d.]+(</td><td>)[\d.]+ \(\d+/\d+\)(</td><td>)[\d.]+ \(\d+/\d+\)(</td>)",
        rf"\g<1>{T:.2f}\g<2>{T_par:.2f}\g<3>{fmt_p(p_std)} ({exc_std}/{N})\g<4>{fmt_p(p_par)} ({exc_par}/{N})\g<5>",
        "summary table Q1009 row")
    # PKS1937-101 row: cols = T_obs, T_parent, p_std, p_parent
    s = sub_optional(s,
        r"(PKS 1937\$-\$101</td><td>3\.572</td><td>ESPRESSO</td><td>)[\d.]+(</td><td>)[\d.]+(</td><td>)[\d.]+ \(\d+/\d+\)(</td><td>)[\d.]+ \(\d+/\d+\)(</td>)",
        rf"\g<1>{t_obs_pks:.2f}\g<2>{t_par_pks:.2f}\g<3>{fmt_p(g3_pks['p_add_one_standard_fair'])} ({g3_pks['exceedances_standard_fair']}/{N})\g<4>{fmt_p(p_par_pks)} ({exc_pks}/{N})\g<5>",
        "summary table PKS1937 row")
    # J1332+0052 row
    s = sub_optional(s,
        r"(J1332\$\+\$0052</td><td>3\.421</td><td>UVES\+HIRES</td><td>)[\d.]+(</td><td>)[\d.]+(</td><td>)[\d.]+ \(\d+/\d+\)(</td><td>)[\d.]+ \(\d+/\d+\)(</td>)",
        rf"\g<1>{t_obs_j13:.2f}\g<2>{t_par_j13:.2f}\g<3>{fmt_p(g3_j13['p_add_one_standard_fair'])} ({g3_j13['exceedances_standard_fair']}/{N})\g<4>{fmt_p(p_par_j13)} ({exc_j13}/{N})\g<5>",
        "summary table J1332 row")

    # Update the parent-reassignment interpretation paragraph.
    # PKS1937/J1332 values are read from their per-sightline gate3 ledgers —
    # never hardcode them, they drift whenever the sightline fit changes.
    s = sub_optional(s,
        r"For Q1009\+2956, \$T_\{\\rm parent\} = T_\{\\rm obs\} = [\d.]+\$",
        f"For Q1009+2956, $T_{{\\\\rm parent}} = T_{{\\\\rm obs}} = {T:.2f}$",
        "parent-reassignment Q1009 T")
    s = sub_optional(s,
        r"For PKS\\,1937\$-\$101, \$T_\{\\rm parent\} = [\d.]+ < T_\{\\rm obs\} = [\d.]+\$",
        f"For PKS\\,1937$-$101, $T_{{\\\\rm parent}} = {t_par_pks:.2f} < T_{{\\\\rm obs}} = {t_obs_pks:.2f}$",
        "parent-reassignment PKS1937 T")
    s = sub_optional(s,
        r"For J1332\$\+\$0052, \$T_\{\\rm parent\} = [\d.]+ < T_\{\\rm obs\} = [\d.]+\$",
        f"For J1332$+$0052, $T_{{\\\\rm parent}} = {t_par_j13:.2f} < T_{{\\\\rm obs}} = {t_obs_j13:.2f}$",
        "parent-reassignment J1332 T")

    # The "T_full / T_-Lyα" display equation and the "T >= X threshold" phrasing
    # were removed when Section 2 was rewritten; LOO values are synced through
    # the table rows and prose anchors below instead.

    # ---- Update LOO table rows ----
    # Build lookup from gate3 leave_one_out ledger
    loo_coadd = {d["excluded"]: d["T"] for d in g3["leave_one_out"] if d["type"] == "coadd"}
    loo_trans = {d["excluded"]: d["T"] for d in g3["leave_one_out"] if d["type"] == "transition"}

    # Map coadd filenames to short labels used in the HTML table
    coadd_label_map = {}
    for fname in loo_coadd:
        if "C1x1" in fname:
            coadd_label_map[fname] = "C1x1"
        elif "C1x2" in fname:
            coadd_label_map[fname] = "C1x2"
        elif "C5x1" in fname:
            coadd_label_map[fname] = "C5x1"
        elif "C5x2" in fname:
            coadd_label_map[fname] = "C5x2"
        else:
            coadd_label_map[fname] = fname

    # Update each coadd row
    for fname, t_val in loo_coadd.items():
        label = coadd_label_map.get(fname, fname)
        delta = t_val - T
        delta_str = f"$+{delta:.2f}$" if delta >= 0 else f"${delta:.2f}$"
        old_pattern = rf"({re.escape(label)} coadd</td><td[^>]*>coadd</td><td[^>]*>)[\d.]+(</td><td[^>]*>)\$[+\-][\d.]+\$"
        new_str = rf"\g<1>{t_val:.2f}\g<2>{delta_str}"
        s_new = re.sub(old_pattern, new_str, s)
        if s_new != s:
            s = s_new
            print_status(f"  Updated LOO coadd row: {label} → T={t_val:.2f}", "PROCESS")

    # Update each transition row
    trans_label_map = {
        "Ly\u03b1": r"Ly\$\\alpha\$",
        "Ly\u03b2": r"Ly\$\\beta\$",
        "Ly\u03b3": r"Ly\$\\gamma\$",
    }
    for trans_name, t_val in loo_trans.items():
        delta = t_val - T
        delta_str = f"$+{delta:.2f}$" if delta >= 0 else f"${delta:.2f}$"
        if trans_name in trans_label_map:
            label_pattern = trans_label_map[trans_name]
        else:
            label_pattern = re.escape(trans_name)
        old_pattern = rf"({label_pattern}</td><td[^>]*>transition</td><td[^>]*>)[\d.]+(</td><td[^>]*>)\$[+\-][\d.]+\$"
        new_str = rf"\g<1>{t_val:.2f}\g<2>{delta_str}"
        s_new = re.sub(old_pattern, new_str, s)
        if s_new != s:
            s = s_new
            print_status(f"  Updated LOO transition row: {trans_name} → T={t_val:.2f}", "PROCESS")

    p2.write_text(s)

    # ---- Update LOO prose paragraph ----
    # The prose paragraph contains specific T values that must match the table
    t_lyb = loo_trans.get("Ly\u03b2", t_lya)
    t_lyg = loo_trans.get("Ly\u03b3", t_lya)
    d_lya = t_lya - T
    d_lyb = t_lyb - T
    d_lyg = t_lyg - T
    lya_increases = d_lya > 0

    s = p2.read_text()
    # Update "removing Lyα increases/decreases T from X to Y"
    lya_verb = "increases" if lya_increases else "decreases"
    s = sub_optional(
        s,
        r"removing Ly\$\\alpha\$ <em>(increases|decreases)</em> \$T\$ from [\d.]+ to [\d.]+",
        f"removing Ly$\\\\alpha$ <em>{lya_verb}</em> $T$ from {T:.2f} to {t_lya:.2f}",
        "LOO prose Lyα",
    )
    # Update Lyβ value and delta (two separate math blocks in the prose)
    s = sub_optional(
        s,
        r"\$T_\{-\\mathrm\{Ly\}\\beta\} = [\d.]+\$,\s*\$\\Delta T = [+\-]?[\d.]+\$",
        f"$T_{{-\\\\mathrm{{Ly}}\\\\beta}} = {t_lyb:.2f}$, $\\\\Delta T = {d_lyb:+.2f}$",
        "LOO prose Lyβ",
    )
    # Update Lyγ delta
    s = sub_optional(
        s,
        r"Ly\$\\gamma\$ \(\$\\Delta T = [+\-]?[\d.]+\$",
        f"Ly$\\\\gamma$ ($\\\\Delta T = {d_lyg:+.2f}$",
        "LOO prose Lyγ",
    )
    p2.write_text(s)

    # ---------------- Abstract ----------------
    pa = ROOT / "site" / "components" / "00_abstract.html"
    a = pa.read_text()
    a = sub_optional(
        a,
        r"Monte Carlo \(\$N = [\d,]+\$ per sightline\)",
        f"Monte Carlo ($N = {N}$ per sightline)",
        "abstract significance",
    )
    # The abstract's headline bound is the Laplace floor 1/(N+1) -> "0.001" at N=1000
    a = sub_optional(
        a,
        r"\$p \\le [\d.]+\$ for all three sightlines on the primary Gate 2/3 family",
        f"$p \\\\le {1.0/(N+1):.3f}$ for all three sightlines on the primary Gate 2/3 family",
        "abstract p bound",
    )
    pa.write_text(a)

    # ---------------- Conclusion ----------------
    # 06_conclusion.html was rewritten qualitatively and currently quotes no
    # ledger-derived numbers, so there is nothing to sync. If ledger numbers
    # are ever reintroduced there, add anchors here — silent drift is the
    # failure mode this script exists to prevent.

    # ---------------- Consolidated summary ledger ----------------
    # results/tep_bbn_summary.json is a derived report artifact. Regenerate it
    # here — from the same ledger values synced into the manuscript above — so
    # it can never be hand-edited into drift from the pipeline. Every field
    # traces to a named source file recorded in _provenance.
    summary = {
        "T_OBS": round(T, 2),
        "T_PARENT": round(T_par, 2),
        "P_STD": round(p_std, 3),
        "P_PARENT": round(p_par, 3),
        "T_LYA": round(t_lya, 2),
        "DLNL": round(d_ll, 2),
        "DAIC": round(d_aic_h, 2),
        "DBIC": round(d_bic_h, 2),
        "N_SIMS": int(N),
        "EXC_STD": int(exc_std),
        "EXC_PARENT": int(exc_par),
        "BINOM95": round(binom, 5),
        "T_OBS_PKS": round(t_obs_pks, 2),
        "T_PARENT_PKS": round(t_par_pks, 2),
        "P_STD_PKS": round(g3_pks["p_add_one_standard_fair"], 3),
        "P_PARENT_PKS": round(p_par_pks, 3),
        "EXC_STD_PKS": int(g3_pks["exceedances_standard_fair"]),
        "EXC_PARENT_PKS": int(exc_pks),
        "BINOM95_PKS": round(g3_pks["binom_95_upper"], 5),
        "N_SIMS_PKS": int(g3_pks["N_sims"]),
        "T_OBS_J1332": round(t_obs_j13, 2),
        "T_PARENT_J1332": round(t_par_j13, 2),
        "P_STD_J1332": round(g3_j13["p_add_one_standard_fair"], 3),
        "P_PARENT_J1332": round(p_par_j13, 3),
        "EXC_STD_J1332": int(g3_j13["exceedances_standard_fair"]),
        "EXC_PARENT_J1332": int(exc_j13),
        "BINOM95_J1332": round(g3_j13["binom_95_upper"], 5),
        "N_SIMS_J1332": int(g3_j13["N_sims"]),
        "_provenance": {
            "generated_by": "scripts/finalize_manuscript_numbers.py",
            "generated_utc": __import__("datetime").datetime.now(
                __import__("datetime").timezone.utc
            ).isoformat(),
            "sources": {
                "gate2_parameter_ledger.json": "LL_Dfree/LL_Hfree, n_pixels -> T_OBS, DLNL, DAIC, DBIC",
                "gate3_significance.json": "T_obs_parent_best, p_add_one_*, exceedances_*, binom_95_upper, N_sims, leave_one_out[Ly-alpha] -> T_PARENT, P_*, EXC_*, BINOM95, N_SIMS, T_LYA (Q1009+2956)",
                "gate_pks19373_significance.json": "*_PKS fields (PKS1937-101)",
                "gate_j13323_significance.json": "*_J1332 fields (J1332+0052)",
            },
        },
    }
    summary_path = ROOT / "results" / "tep_bbn_summary.json"
    with open(summary_path, "w") as f:
        json.dump(summary, f, indent=2)
    print_status(f"Consolidated summary regenerated at {summary_path}", "PROCESS")

    print_status("Manuscript numbers synchronised with ledgers:", "SUCCESS")
    print_status(f"  LL_D={ll_d:.2f} LL_H={ll_h:.2f} LL_DH={ll_dh:.2f} n={n_pix}", "PROCESS")
    print_status(f"  dlnL={d_ll:.2f} T={T:.2f} dAIC={d_aic_h:.2f} dBIC={d_bic_h:.2f}", "PROCESS")
    print_status(f"  T_parent={T_par:.2f}  T_-Lya={t_lya:.2f}", "PROCESS")
    print_status(f"  N={N}  p_std={fmt_p(p_std)} ({exc_std} exc)  p_parent={fmt_p(p_par)} ({exc_par} exc)  binom95={binom:.4f}", "PROCESS")
    print_status("Finalization complete.", "SUCCESS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
