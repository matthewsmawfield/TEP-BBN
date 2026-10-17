import numpy as np

# Physical constants in SI / CGS / astronomical units
# Boltzmann constant in (km/s)^2 * g / K or standard units
# m_p: proton mass in kg
# k_B: 1.380649e-23 J/K
# m_p: 1.67262192e-27 kg
# k_B / m_p in (km/s)^2 / K:
# (1.380649e-23 J/K) / (1.67262192e-27 kg) = 8254.96 m^2 / (s^2 * K) = 0.00825496 (km/s)^2 / K

KB_OVER_MP = 0.008254958  # (km/s)^2 / K

def compute_doppler_b(T_K, b_turb_kms, isotope='H'):
    """
    Computes Doppler parameter b_i in km/s.
    
    Standard relation:
        b_i^2 = b_turb^2 + 2 * k_B * T / m_i
        
    For Hydrogen (m_H ~ m_p):
        b_H^2 = b_turb^2 + 2 * (k_B * T / m_p)
        
    For Deuterium (m_D ~ 2 * m_p):
        b_D^2 = b_turb^2 + k_B * T / m_p
        
    Guarantees b_D < b_H for non-zero temperature T_K > 0.
    """
    b_turb_sq = b_turb_kms ** 2
    if isotope == 'H':
        b_thermal_sq = 2.0 * KB_OVER_MP * T_K
    elif isotope == 'D':
        b_thermal_sq = KB_OVER_MP * T_K
    else:
        raise ValueError(f"Unknown isotope: {isotope}")
        
    return np.sqrt(b_turb_sq + b_thermal_sq)
