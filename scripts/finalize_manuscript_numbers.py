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


def fmt_p(p):
    """Format a bootstrap p-value the way it is quoted in the text."""
    return f"{p:.4f}".rstrip("0").rstrip(".")


def sub_once(text, pattern, replacement, label):
    new, n = re.subn(pattern, replacement, text, count=1)
    if n != 1:
        raise SystemExit(f"[finalize] ANCHOR FAILED ({n} matches): {label}\n  pattern: {pattern}")
    return new


def main():
    g2 = json.loads((ROOT / "results" / "gate2_parameter_ledger.json").read_text())
    g3 = json.loads((ROOT / "results" / "gate3_significance.json").read_text())

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

    frozen = build_model_components("M_NULL", theta, None, pm, z_abs, c_kms)
    cache = build_frozen_cache(frozen, blocks, eng)
    grouped_D = build_model_components("M_Dfree", theta, opt_D, pm, z_abs, c_kms)
    cand_D = split_frozen_candidate(grouped_D, frozen)

    # H at D position (same v, N, T_K, b_turb — only isotope mass differs)
    # Compute the actual D velocity from parent 0
    comps = pm.reconstruct(theta)
    h_comps = [c for c in comps if c["ion"] == "H_I"]
    v_parent0 = c_kms * (h_comps[0]["z"] - z_abs) / (1.0 + z_abs)
    v_D = v_parent0 - 81.6
    grouped_H_mimic = build_model_components(
        "M_H", theta, [v_D, opt_D[0], opt_D[1], opt_D[2]], pm, z_abs, c_kms)
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

    # ---------------- Section 2 ----------------
    p2 = ROOT / "site" / "components" / "02_spectroscopic_non_uniqueness.html"
    s = p2.read_text()

    s = sub_once(s, r"<td>\$-?\d+\.\d+\$</td>\s*<td>0</td>",
                 f"<td>${ll_d:.2f}$</td>\n            <td>0</td>", "table LL(M_D)")
    s = sub_once(s, r"<td>\$-?\d+\.\d+\$</td>\s*<td>\$-?\d+\.\d+\$</td>\s*<td>observationally embeds",
                 f"<td>${ll_h:.2f}$</td>\n            <td>${d_aic_h:.2f}$</td>\n            <td>observationally embeds",
                 "table LL(M_H)")
    s = sub_once(s, r"<td>\$-?\d+\.\d+\$</td>\s*<td>\$-?\d+\.\d+\$</td>\s*<td>contains",
                 f"<td>${ll_dh:.2f}$</td>\n            <td>${d_aic_dh:.2f}$</td>\n            <td>contains",
                 "table LL(M_D+H)")

    # isotope effect RMS (pure mass difference, H at D position)
    s = sub_once(s, r"(?:the maximum discrepancy between the best-fit free-H model and the exact true-D model|the RMS discrepancy between the H and D Voigt profiles \(H placed at the D position with identical column, temperature and turbulent width — only the isotope mass differs\)),? relative to the instrumental noise level, was found to be only \$0\.[\d]+\\sigma\$",
                 f"the RMS discrepancy between the H and D Voigt profiles (H placed at the D position with identical column, temperature and turbulent width — only the isotope mass differs), relative to the instrumental noise level, was found to be only ${iso_rms:.4f}\\\\sigma$",
                 "isotope RMS")

    s = sub_once(
        s,
        r"\\Delta \\ln L = [\d.]+, \\qquad T = [\d.]+, \\qquad \\Delta k = 1, \\qquad \\Delta\\mathrm\{AIC\} = -[\d.]+\.",
        f"\\\\Delta \\\\ln L = {d_ll:.2f}, \\\\qquad T = {T:.2f}, \\\\qquad \\\\Delta k = 1, \\\\qquad \\\\Delta\\\\mathrm{{AIC}} = {d_aic_h:.2f}.",
        "display equation T",
    )
    s = sub_once(s, r"likelihood improvement of \$\\Delta\\ln L = [\d.]+\$",
                 f"likelihood improvement of $\\\\Delta\\\\ln L = {d_ll:.2f}$", "inline dlnL")
    s = sub_once(s, r"\$\\Delta\\mathrm\{AIC\} = -[\d.]+\$ and \$\\Delta\\mathrm\{BIC\} = -[\d.]+\$",
                 f"$\\\\Delta\\\\mathrm{{AIC}} = {d_aic_h:.2f}$ and $\\\\Delta\\\\mathrm{{BIC}} = {d_bic_h:.2f}$",
                 "inline AIC/BIC")

    # significance paragraph
    s = sub_once(
        s,
        r"To establish rigorous significance, [\d,]+ physical Monte Carlo simulations",
        f"To establish rigorous significance, {N} physical Monte Carlo simulations",
        "N_sims sentence",
    )
    s = sub_once(
        s,
        r"yielding \$p_\{\\rm add-one\} = [\d.]+\$ \(\d+ exceedances out of [\d,]+ realizations\)\.",
        f"yielding $p_{{\\\\rm add-one}} = {fmt_p(p_std)}$ ({exc_std} exceedances out of {N} realizations).",
        "p_standard",
    )
    s = sub_once(
        s,
        r"yielding \$p_\{\\rm parent\} = [\d.]+\$ \(\d+ exceedances out of [\d,]+ realizations, one-sided 95% binomial upper bound [\d.]+\)\.",
        f"yielding $p_{{\\\\rm parent}} = {fmt_p(p_par)}$ ({exc_par} exceedances out of {N} realizations, "
        f"one-sided 95% binomial upper bound {binom_par:.4f}).",
        "p_parent",
    )

    s = sub_once(s, r"\$T_\{\\rm parent\} = [\d.]+\$, compared with \$T = [\d.]+\$",
                 f"$T_{{\\\\rm parent}} = {T_par:.2f}$, compared with $T = {T:.2f}$", "T_parent inline")
    s = sub_once(s, r"the \$T \\ge [\d.]+\$ threshold",
                 f"the $T \\\\ge {T_par:.2f}$ threshold", "T_parent threshold")
    s = sub_once(s, r"allows D to select the most favorable parent from (?:all 43 H components|the \d+ H I components within ±\d+ km/s of the absorber systemic velocity)",
                 "allows D to select the most favorable parent from the 14 H I components within "
                 "±1000 km/s of the absorber systemic velocity", "parent count")

    s = sub_once(
        s,
        r"T_\{\\rm full\} = [\d.]+, \\qquad T_\{-\\mathrm\{Ly\}\\alpha\} = [\d.]+\.",
        f"T_{{\\\\rm full}} = {T:.2f}, \\\\qquad T_{{-\\\\mathrm{{Ly}}\\\\alpha}} = {t_lya:.2f}.",
        "LOO equation",
    )
    p2.write_text(s)

    # ---------------- Abstract ----------------
    pa = ROOT / "site" / "components" / "00_abstract.html"
    a = pa.read_text()
    a = sub_once(a, r"improved by \$\\Delta\\ln L=[\d.]+\$ \(\$T=[\d.]+\$\)",
                 f"improved by $\\\\Delta\\\\ln L={d_ll:.2f}$ ($T={T:.2f}$)", "abstract dlnL/T")
    a = sub_once(a, r"the margin falls to \$T_\{\\rm parent\}=[\d.]+\$",
                 f"the margin falls to $T_{{\\\\rm parent}}={T_par:.2f}$", "abstract T_parent")
    a = sub_once(a, r"differs from true D by only \$0\.[\d]+\\sigma\$",
                 f"differs from true D by only ${iso_rms:.4f}\\\\sigma$", "abstract iso_rms")
    a = sub_once(
        a,
        r"calibration against [\d,]+ true-D Monte Carlo realizations of the identical statistic yields \$p_\{\\rm parent\} = [\d.]+\$.*?transition \(\$T_\{-\\mathrm\{Ly\}\\alpha\} = [\d.]+\$\)\.",
        f"calibration against {N} true-D Monte Carlo realizations of the identical statistic yields "
        f"$p_{{\\\\rm parent}} = {fmt_p(p_par)}$, with the discrimination concentrated in the Ly$\\\\alpha$ "
        f"transition ($T_{{-\\\\mathrm{{Ly}}\\\\alpha}} = {t_lya:.2f}$).",
        "abstract significance",
    )
    pa.write_text(a)

    # ---------------- Conclusion ----------------
    pc = ROOT / "site" / "components" / "06_conclusion.html"
    c = pc.read_text()
    c = sub_once(c, r"likelihood improvement of \$\\Delta \\ln L = [\d.]+\$ \(\$T=[\d.]+\$\)",
                 f"likelihood improvement of $\\\\Delta \\\\ln L = {d_ll:.2f}$ ($T={T:.2f}$)", "concl dlnL/T")
    c = sub_once(c, r"falling to \$T_\{\\rm parent\}=[\d.]+\$",
                 f"falling to $T_{{\\\\rm parent}}={T_par:.2f}$", "concl T_parent")
    c = sub_once(
        c,
        r"Monte Carlo calibration of the identical statistic on [\d,]+ true-D spectra yields \$p_\{\\rm parent\} = [\d.]+\$",
        f"Monte Carlo calibration of the identical statistic on {N} true-D spectra yields "
        f"$p_{{\\\\rm parent}} = {fmt_p(p_par)}$",
        "concl significance",
    )
    pc.write_text(c)

    print("[finalize] manuscript numbers synchronised with ledgers:")
    print(f"  LL_D={ll_d:.2f} LL_H={ll_h:.2f} LL_DH={ll_dh:.2f} n={n_pix}")
    print(f"  dlnL={d_ll:.2f} T={T:.2f} dAIC={d_aic_h:.2f} dBIC={d_bic_h:.2f}")
    print(f"  T_parent={T_par:.2f}  T_-Lya={t_lya:.2f}")
    print(f"  N={N}  p_std={fmt_p(p_std)} ({exc_std} exc)  p_parent={fmt_p(p_par)} ({exc_par} exc)  binom95={binom:.4f}")


if __name__ == "__main__":
    sys.exit(main())
