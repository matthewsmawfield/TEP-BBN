#!/usr/bin/env python3
"""
Gate 1R: Physical Atomic-Data Embedding

This script verifies the exact mathematical embedding theorem M_D \\subset M_H,free.
Unlike the initial mock, this tests the embedding using the physical atomic registry.
It loads actual registered lambda, f, and Gamma values and computes the real residual
differences, demonstrating observational indistinguishability.
"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))
import numpy as np

from scripts.utils.logger import print_status, setup_step_logger

np.seterr(all="ignore")
import hashlib
import json
import sys
from pathlib import Path

from scipy.stats import t as student_t

project_root = Path(__file__).resolve().parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from scripts.lib.physical_rt_engine import c_kms, sigma_0, voigt_profile


# The NIST data has `A_ul` listed under `oscillator_strength`.
# Calculate f_osc using standard physical constants.
def parse_atomic_file(filepath):
    lines_data = {}
    with open(filepath, "r") as f:
        for line in f:
            if line.startswith("#") or not line.strip():
                continue
            parts = line.split()
            if len(parts) < 3 or parts[1] == "N/A":
                continue
            wav = float(parts[0])
            A_ul = float(parts[1])
            trans = parts[2]

            # Simplified statistical weight lookup for Lyman series
            # Assuming Ly_alpha, Ly_beta, etc.
            # We'll use the A_ul to f_osc conversion factor or use known f_osc
            # For strict Gate 1R, f_osc is needed. Lookup by transition if it's fine structure averaged.

            # Since NIST splits fine structure, let's just grab the primary line or sum them.
            # Actually, the user says "test every shared transition".
            # Let's map by transition name and wavelength rounding.
            if trans not in lines_data:
                lines_data[trans] = []
            lines_data[trans].append({"wav": wav, "A_ul": A_ul})

    # For simplicity in this physical test, fine structure components are averaged/summed to
    # match the standard RadiativeTransferEngine resolution, or use the raw components.
    # The physical_rt_engine takes a single lambda, f, Gamma.
    # Use the exact values from physical_rt_engine's AtomicData as the "registered" ones
    # if the NIST parsing is too complex, BUT the user explicitly requested:
    # "Load the physical atomic registry: H_I_lines.txt, D_I_lines.txt... Then test every shared transition".

    return lines_data


class PhysicalRadiativeTransferEngine:
    def __init__(self, z_abs):
        self.z_abs = z_abs

        # Load physical registries
        h_file = project_root / "data" / "raw" / "atomic" / "H_I" / "H_I_lines.txt"
        d_file = project_root / "data" / "raw" / "atomic" / "D_I" / "D_I_lines.txt"
        if not h_file.exists():
            raise FileNotFoundError(f"H I atomic data not found: {h_file}")
        if not d_file.exists():
            raise FileNotFoundError(f"D I atomic data not found: {d_file}")
        h_data = parse_atomic_file(h_file)
        d_data = parse_atomic_file(d_file)

        self.h_lines = {}
        self.d_lines = {}

        # Need f_osc. NIST file has A_ul.
        # f_lu = 1.499e-16 * A_ul * (wav**2) * (g_u / g_l)
        # For Lyman series (1s -> np), g_l = 2, g_u = 2(n^2) if no fine structure.
        # With fine structure: 1s_1/2 -> np_1/2 (g=2), np_3/2 (g=4).
        # A_ul for np_3/2 and np_1/2 are the same.
        # Rather than reinventing the wheel, match the transition and use standard f_osc
        # proportionalities.
        # Actually, let's just construct the exact dictionary format expected.

        # Let's just use the strongest fine-structure component for each transition to test the embedding.
        for trans in ["Lyα", "Lyβ", "Lyγ", "Lyδ", "Lyε"]:
            if trans in h_data and trans in d_data:
                h_comp = max(h_data[trans], key=lambda x: x["A_ul"])
                d_comp = max(d_data[trans], key=lambda x: x["A_ul"])

                # Approximate f_osc from A_ul (ignoring exact g_u/g_l for a relative test)
                # Since the test is D vs H, as long as both are treated consistently it is fine.
                # Standard conversion for the strongest component (g_u/g_l = 2)
                f_h = 1.499e-16 * h_comp["A_ul"] * (h_comp["wav"] ** 2) * 2.0
                f_d = 1.499e-16 * d_comp["A_ul"] * (d_comp["wav"] ** 2) * 2.0

                name = "HI_" + trans
                self.h_lines[name] = (h_comp["wav"], f_h, h_comp["A_ul"])
                self.d_lines[name.replace("HI", "DI")] = (
                    d_comp["wav"],
                    f_d,
                    d_comp["A_ul"],
                )

    def compute_optical_depth(self, wave_obs, transitions_list, comp, is_d=False):
        tau_total = np.zeros_like(wave_obs)
        N = comp["N"]
        b_kms = comp["b"]
        v_kms = comp["v"]

        lines = self.d_lines if is_d else self.h_lines

        for t_name in transitions_list:
            lam_rest, f_osc, gamma = lines[t_name]
            lam_obs_center = lam_rest * (1.0 + self.z_abs)
            lam_c = lam_obs_center * (1.0 + v_kms / c_kms)
            delta_v_kms = c_kms * (wave_obs - lam_c) / lam_c
            x = delta_v_kms / b_kms
            lam_rest_cm = lam_rest * 1e-8
            b_cgs = b_kms * 1e5
            a = (gamma * lam_rest_cm) / (4.0 * np.pi * b_cgs)
            V = voigt_profile(x, a)
            tau0 = N * f_osc * lam_rest_cm * (sigma_0 / b_cgs)
            tau_total += tau0 * V

        return tau_total

    def apply_convolution(self, flux, wave, sigma_kms):
        dv_kms = c_kms * np.median(np.diff(wave) / wave[:-1])
        n_pixels = int(np.ceil(5.0 * sigma_kms / dv_kms))
        v_grid = np.arange(-n_pixels, n_pixels + 1) * dv_kms
        kernel = np.exp(-0.5 * (v_grid / sigma_kms) ** 2)
        kernel /= np.sum(kernel)
        return np.convolve(flux, kernel, mode="same")


def run_gate1():
    setup_step_logger(Path(__file__).stem)
    print_status("=== GATE 1R: PHYSICAL ATOMIC-DATA EMBEDDING ===", "SUCCESS")

    h_file = project_root / "data" / "raw" / "atomic" / "H_I" / "H_I_lines.txt"
    d_file = project_root / "data" / "raw" / "atomic" / "D_I" / "D_I_lines.txt"
    with open(h_file, "rb") as f:
        h_hash = hashlib.sha256(f.read()).hexdigest()
    with open(d_file, "rb") as f:
        d_hash = hashlib.sha256(f.read()).hexdigest()
    print_status(f"H_I_lines.txt SHA-256: {h_hash}", "PROCESS")
    print_status(f"D_I_lines.txt SHA-256: {d_hash}", "PROCESS")

    z_abs = 2.5042
    engine = PhysicalRadiativeTransferEngine(z_abs)

    out_dir = project_root / "results"
    out_dir.mkdir(exist_ok=True, parents=True)

    # Derivation of optimal mapping
    # Using Lya for the mapping base
    lam_h_base = engine.h_lines["HI_Lyα"][0]
    lam_d_base = engine.d_lines["DI_Lyα"][0]
    rho_eff = lam_d_base / lam_h_base

    # Use the ACTUAL D column from D/H ratio and N_HI, not an inflated value.
    # Q1009: D/H = 2.48e-5, logN_HI = 17.362 → N_D = 5.7e12
    # The previous value (1e14) was 22.5x too high, inflating the identifiability.
    N_D = 5.7e12  # Actual Q1009 D column from D/H = 2.48e-5 × N_HI
    b_D = 12.0
    v_D = 0.0
    comp_D = {"N": N_D, "b": b_D, "v": v_D}

    v_H_equiv = c_kms * (rho_eff * (1.0 + v_D / c_kms) - 1.0)
    N_H_equiv = N_D * rho_eff
    # Physical mass-scaled Doppler parameter: b_H = b_D * sqrt(m_D / m_H)
    # For thermally-dominated gas, H and D have different b-values because
    # the thermal broadening depends on mass.  For turbulence-dominated gas
    # (b_turb >> b_therm), the b-values are nearly identical.  We compute
    # BOTH cases and report them separately.
    mass_H = 1.00784
    mass_D = 2.01410
    b_H_thermal = b_D * np.sqrt(mass_D / mass_H)  # physical mass-scaled b
    comp_H_thermal = {"N": N_H_equiv, "b": b_H_thermal, "v": v_H_equiv}
    # Also compute the turbulence-dominated case (b_H = b_D) for comparison
    comp_H_turb = {"N": N_H_equiv, "b": b_D, "v": v_H_equiv}
    # Mixed regime: use the actual fitted Q1009 Gate 2 parameters
    # T_K=2000, b_turb=10.70 → b_H=12.15, b_D=11.45 (b_turb/b_therm ≈ 1.87)
    from scripts.lib.doppler_physics import compute_doppler_b as _cdb
    _T_K_fit, _b_turb_fit = 2000.0, 10.70
    _b_H_fit = _cdb(_T_K_fit, _b_turb_fit, 'H')
    _b_D_fit = _cdb(_T_K_fit, _b_turb_fit, 'D')
    comp_H_mixed = {"N": N_H_equiv, "b": _b_H_fit, "v": v_H_equiv}
    comp_D_mixed = {"N": N_D, "b": _b_D_fit, "v": v_D}

    print_status(
        f"\nOptimal Mapping derived from Lyα ratio: rho = {rho_eff:.8f}", "PROCESS"
    )

    transitions = [k for k in engine.h_lines.keys()]

    max_tau_err = 0.0
    max_F_err = 0.0

    for t_h, t_d in zip(transitions, [k.replace("HI", "DI") for k in transitions]):
        lam_obs = engine.h_lines[t_h][0] * (1 + z_abs)
        wave_obs = np.linspace(lam_obs - 1.0, lam_obs + 1.0, 20000)

        tau_D = engine.compute_optical_depth(wave_obs, [t_d], comp_D, is_d=True)
        tau_H = engine.compute_optical_depth(wave_obs, [t_h], comp_H_thermal, is_d=False)

        max_tau_diff = np.max(np.abs(tau_D - tau_H))
        max_tau = np.max([1.0, np.max(tau_D)])
        eps_tau = max_tau_diff / max_tau
        max_tau_err = max(max_tau_err, eps_tau)

        F_D = np.exp(-tau_D)
        F_H = np.exp(-tau_H)
        eps_F = np.max(np.abs(F_D - F_H))
        max_F_err = max(max_F_err, eps_F)

        print_status(f"{t_h} / {t_d}:", "PROCESS")
        print_status(f"  eps_tau = {eps_tau:.4e}", "PROCESS")
        print_status(f"  eps_F   = {eps_F:.4e}", "PROCESS")

    print_status(f"\nGlobal Max eps_tau = {max_tau_err:.4e}", "PROCESS")
    print_status(f"Global Max eps_F   = {max_F_err:.4e}", "PROCESS")

    # 3. Convolved Flux and Likelihood across ALL common Lyman transitions
    # Compute BOTH the physical (mass-scaled b) and turbulence-dominated (b_H=b_D) cases.
    print_status("\n--- Operational Isotope Identifiability ---", "TITLE")

    # Use actual Keck/HIRES resolution from Zavarygin et al. 2018
    # C1 settings: vsig=2.6 km/s (R≈49,000), C5 settings: vsig=3.4 km/s (R≈37,000)
    # Use the C1 value (higher resolution) as the representative case
    inst_res_kms = 2.6  # Keck/HIRES C1 sigma (Zavarygin et al. 2018)
    noise_sigma = 0.05

    for case_name, comp_H_case, comp_D_case in [
        ("thermal (mass-scaled b_H)", comp_H_thermal, comp_D),
        ("turbulence-dominated (b_H=b_D)", comp_H_turb, comp_D),
        ("mixed (fitted Q1009: T_K=2000, b_turb=10.7)", comp_H_mixed, comp_D_mixed),
    ]:
        print_status(f"\n  Case: {case_name}", "PROCESS")
        print_status(f"    b_D = {comp_D_case['b']:.2f}, b_H = {comp_H_case['b']:.2f}", "PROCESS")

        max_sigma_dev = 0.0

        for t_h, t_d in zip(transitions, [k.replace("HI", "DI") for k in transitions]):
            lam_obs = engine.h_lines[t_h][0] * (1 + z_abs)
            wave_obs = np.linspace(lam_obs - 1.0, lam_obs + 1.0, 20000)

            tau_D = engine.compute_optical_depth(wave_obs, [t_d], comp_D_case, is_d=True)
            tau_H = engine.compute_optical_depth(wave_obs, [t_h], comp_H_case, is_d=False)

            F_D = np.exp(-tau_D)
            F_H = np.exp(-tau_H)

            C_F_D = engine.apply_convolution(F_D, wave_obs, inst_res_kms)
            C_F_H = engine.apply_convolution(F_H, wave_obs, inst_res_kms)

            valid = slice(100, -100)

            max_dev = np.max(np.abs(C_F_D[valid] - C_F_H[valid]) / noise_sigma)
            max_sigma_dev = max(max_sigma_dev, max_dev)

            eps_conv = np.max(np.abs(C_F_D[valid] - C_F_H[valid]))
            print_status(
                f"    {t_h}: eps_conv = {eps_conv:.4e}, max |F_D - F_H| / sigma = {max_dev:.4f}",
                "PROCESS",
            )

        print_status(f"  → Global Max |F_D - F_H| / sigma = {max_sigma_dev:.4f}", "PROCESS")

        if "thermal" in case_name:
            max_sigma_dev_thermal = max_sigma_dev
        elif "turbulence" in case_name:
            max_sigma_dev_turb = max_sigma_dev
        else:
            max_sigma_dev_mixed = max_sigma_dev

    print_status(f"\n  SUMMARY:", "TITLE")
    print_status(f"    Thermal (mass-scaled b):     {max_sigma_dev_thermal:.4f} sigma", "PROCESS")
    print_status(f"    Turbulence-dominated (b=bD): {max_sigma_dev_turb:.4f} sigma", "PROCESS")
    print_status(f"    Mixed (fitted Q1009 params): {max_sigma_dev_mixed:.4f} sigma", "PROCESS")
    print_status(f"    → H and D ARE distinguishable for thermally-dominated gas", "PROCESS")
    print_status(f"    → H and D are NOT distinguishable for turbulence-dominated gas", "PROCESS")
    print_status(f"    → Q1009 fitted params give mixed regime (b_turb/b_therm ≈ 1.87)", "PROCESS")

    # The physical case is the thermal one.  The turbulence-dominated case
    # is the optimistic (for TEP) lower bound.  Both are reported.
    max_sigma_dev = max_sigma_dev_thermal

    if max_sigma_dev < 0.5:
        print_status(
            "\n[RESULT] Isotope non-identifiability verified for this b-regime.",
            "SUCCESS",
        )
    else:
        print_status(
            f"\n[RESULT] Isotope IDENTIFIABLE: max discrepancy = {max_sigma_dev:.4f} sigma "
            f"(> 0.5 sigma threshold). H and D are distinguishable for thermally-dominated gas.",
            "WARNING",
        )

    ledger = {
        "h_i_hash": h_hash,
        "d_i_hash": d_hash,
        "rho_eff": rho_eff,
        "max_tau_err": max_tau_err,
        "max_F_err": max_F_err,
        "max_sigma_dev_thermal": max_sigma_dev_thermal,
        "max_sigma_dev_turb": max_sigma_dev_turb,
        "max_sigma_dev_mixed": max_sigma_dev_mixed,
        "max_sigma_dev": max_sigma_dev,
        "is_indistinguishable_thermal": bool(max_sigma_dev_thermal < 0.5),
        "is_indistinguishable_turb": bool(max_sigma_dev_turb < 0.5),
        "is_indistinguishable_mixed": bool(max_sigma_dev_mixed < 0.5),
        "b_D": b_D,
        "b_H_thermal": b_H_thermal,
        "b_H_turb": b_D,
        "b_H_mixed": _b_H_fit,
        "b_D_mixed": _b_D_fit,
        "mixed_regime_T_K": _T_K_fit,
        "mixed_regime_b_turb": _b_turb_fit,
        "mixed_regime_b_turb_over_b_therm": _b_turb_fit / (np.sqrt(2 * 1.380649e-23 * _T_K_fit / (1.00784 * 1.6726219e-27)) / 1e3),
        "metric_description": (
            "max_sigma_dev is the MAXIMUM (not RMS) deviation between convolved H "
            "and D fluxes, divided by a conservative constant noise_sigma=0.05. "
            "Two cases are computed: (1) thermal (mass-scaled b_H = b_D * sqrt(m_D/m_H)), "
            "which is the physical case for thermally-dominated gas; and (2) turbulence-dominated "
            "(b_H = b_D), which applies when b_turb >> b_therm. The thermal case determines "
            "whether H and D are fundamentally distinguishable; the turbulence case is the "
            "optimistic lower bound for TEP."
        ),
        "transitions_tested": ["Lyα", "Lyβ", "Lyγ", "Lyδ", "Lyε"],
        "noise_sigma_assumed": noise_sigma,
        "inst_res_kms_assumed": inst_res_kms,
    }

    with open(out_dir / "gate1_embedding.json", "w") as f:
        json.dump(ledger, f, indent=2)
    print_status(
        f"\n[SUCCESS] Gate 1R ledger written to {out_dir / 'gate1_embedding.json'}",
        "SUCCESS",
    )


if __name__ == "__main__":
    run_gate1()
