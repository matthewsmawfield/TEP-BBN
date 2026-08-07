import numpy as np

def calculate_gamow_suppression(T_loc, Z1=1, Z2=1, mu_amu=0.5):
    """
    Calculate the logarithmic suppression factor for nuclear tunneling (Gamow peak).
    T_loc in Kelvin. Z1, Z2 are atomic numbers. mu_amu is reduced mass in amu.
    Returns ln(suppression) which is proportional to - (E_G / kT)^(1/3)
    """
    # Gamow energy E_G = 2 * mu * pi^2 * (alpha * Z1 * Z2)^2 * m_p * c^2
    # Simplified calculation for scaling purposes:
    # E_G ~ 493 keV for p+p
    E_G = 493e3 # eV
    k_B = 8.617e-5 # eV/K
    kT = k_B * T_loc
    
    # Exponent is approx -3 * (E_G / (4 * kT))^(1/3)
    exponent = -3.0 * (E_G / (4.0 * kT))**(1/3)
    return exponent

def run_thermodynamic_audit():
    print("TEP Proper-Time Thermodynamics: Phase 1 Evaluation\n")
    print("Hypothesis: T_loc = 2.725 K, Plasma is cold and neutral.")
    print("Hypothesis: Temporal Scaling Factor A(z=1100) = 1/1101\n")
    
    # Fundamental constants (invariant)
    k_B = 8.617333e-5 # eV / K
    E_ion_H = 13.6 # eV
    T_loc = 2.725 # K
    
    # 1. Thermal kinetic energy
    kT = k_B * T_loc
    print(f"Local Thermal Energy (kT): {kT:.3e} eV")
    
    # 2. Invariant Ionization Ratio
    ion_ratio = E_ion_H / kT
    print(f"Ionization Energy / kT: {ion_ratio:.1f}")
    
    if ion_ratio > 1:
        print("Result: Local plasma is overwhelmingly neutral.\n")
    
    # 3. Nuclear Fusion Logarithmic Bounds
    # T_BBN ~ 10^9 K. kT ~ 86 keV.
    log_supp_hot = calculate_gamow_suppression(1e9)
    log_supp_cold = calculate_gamow_suppression(2.725)
    
    print(f"Log(suppression) at 10^9 K: {log_supp_hot:.1f}")
    print(f"Log(suppression) at 2.7 K:  {log_supp_cold:.1f}")
    print(f"Ratio of tunneling probabilities (Cold/Hot) ~ exp({log_supp_cold - log_supp_hot:.1f})")
    print("Result: Reaction rate Gamma_tau is highly suppressed, but non-zero.\n")
    
    # 4. Integrated reaction count invariance
    print("Integrated reaction count: N = integral(Gamma_tau * dtau)")
    print("Coordinate scaling A(t) changes dt, but does not increase Gamma_tau.")
    print("To achieve N_required, the total physical proper-time interval integral(dtau) must be immense (eternal cosmology).")
    print("Result: Simple coordinate parameterization fails. Genuinely extended chronology is required.\n")
    
    # 5. Emitter to Observer Frequency Scaling
    A_em = 1.0 / 1101.0
    A_obs = 1.0
    T_obs = T_loc * (A_em / A_obs)
    
    print(f"Emission Frame Local Temperature: {T_loc} K")
    print(f"Observed Temperature Today: {T_obs:.6f} K")
    print("Result: A 2.7 K local source is received as a 0.002 K spectrum (redshift).\n")
    
    print("Phase 1 Verdict: SIMPLE_UNIVERSAL_CONFORMAL_NO_HOT_MECHANISM_REJECTED")

if __name__ == '__main__':
    run_thermodynamic_audit()
