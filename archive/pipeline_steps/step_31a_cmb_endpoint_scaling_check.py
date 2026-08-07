import numpy as np
from scipy import integrate

def planck_intensity(nu, T):
    """
    Planck specific intensity B_nu(T)
    nu in Hz, T in K.
    Returns intensity in W / (m^2 sr Hz)
    """
    h = 6.62607015e-34 # J s
    c = 299792458 # m/s
    k_B = 1.380649e-23 # J/K
    
    # Avoid overflow
    x = (h * nu) / (k_B * T)
    x = np.clip(x, 1e-10, 700) 
    
    return (2 * h * nu**3 / c**2) / (np.exp(x) - 1.0)

def photon_number_density(T):
    """
    Total photon number density n_gamma proportional to T^3
    """
    return T**3

def total_intensity(T):
    """
    Total intensity proportional to T^4
    """
    return T**4

def run_phase_2a_transport(T_em, A_em, A_obs=1.0):
    print(f"--- Transport Test: T_em = {T_em:.3f} K ---")
    
    # The conformal metric gives a frequency shift:
    # nu_obs = nu_em * (A_em / A_obs)
    # The phase-space distribution function f(x, p) is invariant along photon trajectories
    # Intensity B_nu = (2hnu^3 / c^2) * f
    # Because nu scales by (A_em/A_obs), B_nu scales by (A_em/A_obs)^3
    # Therefore, the observed spectrum is exactly a Planck spectrum with temperature:
    
    T_obs = T_em * (A_em / A_obs)
    
    print(f"Expected Observer Temperature (T_obs): {T_obs:.6f} K")
    print(f"Observed Intensity scaling (relative to T_em): (T_obs/T_em)^4 = {(T_obs/T_em)**4:.3e}")
    print(f"Observed Photon Number scaling (relative to T_em): (T_obs/T_em)^3 = {(T_obs/T_em)**3:.3e}")
    
    if np.isclose(T_obs, 2.725, rtol=1e-3):
        print("Verdict: MATCHES FIRAS OBSERVATION (2.725 K)")
    else:
        print("Verdict: FAILS FIRAS OBSERVATION")
    print("")

if __name__ == '__main__':
    print("TEP-BBN Phase 2A: Bounded CMB Phase-Space Transport\n")
    
    A_em = 1.0 / 1101.0
    A_obs = 1.0
    
    print(f"Conformal Endpoints: A_em = {A_em:.5f}, A_obs = {A_obs:.1f}\n")
    
    # Test 1: Cold Source
    run_phase_2a_transport(2.725, A_em, A_obs)
    
    # Test 2: Standard Hot Source
    run_phase_2a_transport(3000.0, A_em, A_obs)
    
    # Test 3: TEP Required Source
    run_phase_2a_transport(2.725 / A_em, A_em, A_obs)
    
    print("Conclusion: To observe a 2.725 K spectrum today under the A_clock convention,")
    print("the local emission temperature MUST be 2.725 / A_em (approx 3000 K).")
    print("A locally cold source (2.725 K) will transport to an undetectable 0.002 K spectrum.")
