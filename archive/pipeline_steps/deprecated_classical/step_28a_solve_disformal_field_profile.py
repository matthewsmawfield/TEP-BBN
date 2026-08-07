import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_bvp

def solve_field_profile(N_H=1e20, n_H=1e-3, M_pl=2.435e18, m_scalar=1e-33, beta=1.0):
    """
    Solve the 1D field profile for a dark energy scalar field coupled to matter.
    We approximate the LLS as a 1D slab of hydrogen with uniform density.
    
    Equation: d^2 phi / dx^2 = m^2 phi + (beta / M_pl) rho
    We use natural units (hbar = c = 1).
    m_scalar: scalar mass in eV. 1 eV = 5.06e4 cm^-1.
    rho: matter density in eV^4. 
    1 g/cm^3 = 4.3e15 eV^4.
    """
    # Unit conversions
    cm_to_eVinv = 5.06e4
    eV_to_g = 1.783e-33
    eV_to_cm_inv = 1.0 / cm_to_eVinv
    
    # LLS density
    rho_cgs = n_H * 1.67e-24 # g/cm^3
    rho_eV4 = rho_cgs / (eV_to_g * cm_to_eVinv**3)
    
    # LLS size
    L_cm = N_H / n_H
    L_eVinv = L_cm * cm_to_eVinv
    
    print(f"LLS Physical Size: {L_cm:e} cm ({L_cm / 3.086e21:.2f} kpc)")
    print(f"LLS Density: {rho_cgs:e} g/cm^3 ({rho_eV4:e} eV^4)")
    
    # The source term is (beta / M_pl) * rho.
    # We solve d^2 phi / dz^2 = m^2 phi + J, where z is in eV^-1
    # Actually, for a massive scalar field, the solution is analytic!
    # Inside the slab (|z| < L/2):
    # phi(z) = -J/m^2 + A cosh(m z)
    # Outside the slab (|z| > L/2):
    # phi(z) = B exp(-m |z|)
    # Matching phi and dphi/dz at z = L/2 gives A and B.
    
    M_pl_eV = M_pl * 1e9
    J = beta * rho_eV4 / M_pl_eV
    m_eV = m_scalar
    
    phi_infty = -J / m_eV**2
    print(f"Source J: {J:e} eV^3")
    print(f"Phi asymptotic deep inside: {phi_infty:e} eV")
    
    # The spectral offset from a disformal coupling is delta z = B(phi) * (nabla phi)^2 / 2
    # In the static limit, the energy of a photon shifts due to the effective metric.
    # As derived in Stage 2.5: delta E / E = 1/2 B(phi) (dphi/dz)^2.
    # To get 81.6 km/s, delta z = v / c = 81.6 / 3e5 = 2.7e-4.
    # We need 1/2 B(phi) (dphi/dz)^2 ~ 2.7e-4.
    
    # Let's calculate the max gradient:
    # dphi/dz = m A sinh(m L/2) = m (-phi_infty) * (1 - exp(-m L/2))
    # Approximation if m L >> 1 (deep slab): max gradient is ~ m * |phi_infty| / 2
    # If m L << 1 (thin slab): max gradient is ~ J * L / 2
    
    grad_max_eV2 = J * L_eVinv / 2.0
    grad_max_cgs = grad_max_eV2 * cm_to_eVinv**2 / 1.783e-33 # Very rough conversion
    
    print(f"Max gradient (dphi/dz): {grad_max_eV2:e} eV^2")
    
    # Required B(phi) to get 2.7e-4 shift
    B_req = 2 * 2.7e-4 / (grad_max_eV2**2)
    print(f"Required B(phi) for 81.6 km/s shift: {B_req:e} eV^-4")
    
    # B(phi) is usually dimensionful, parameterized as 1/M^4.
    M_scale = (1.0 / B_req)**0.25
    print(f"Corresponding Disformal Mass Scale M: {M_scale:e} eV")

if __name__ == '__main__':
    # Try different parameter sets to bracket the realistic profile
    print("--- Fiducial LLS ---")
    solve_field_profile(N_H=1e20, n_H=1e-3, m_scalar=1e-33, beta=1.0)
    
    print("\n--- Dense Core ---")
    solve_field_profile(N_H=1e17, n_H=1.0, m_scalar=1e-33, beta=1.0)
    
    print("\n--- Low mass scalar ---")
    solve_field_profile(N_H=1e20, n_H=1e-3, m_scalar=1e-39, beta=1.0)

