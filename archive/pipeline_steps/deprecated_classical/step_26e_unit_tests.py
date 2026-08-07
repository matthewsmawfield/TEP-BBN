import numpy as np
from pathlib import Path
import sys

script_dir = Path(__file__).parent
project_root = script_dir.parent.parent
sys.path.insert(0, str(project_root))

from scripts.lib.physical_rt_engine import RadiativeTransferEngine

def test_optically_thin():
    z = 0.0
    engine = RadiativeTransferEngine(z_abs=z)
    
    lam_rest, f_osc, gamma = engine.atomic.get('HI_Lya')
    
    # Optically thin component
    logN = 12.0
    b = 10.0
    N = 10**logN
    
    comps = [{'N': N, 'b': b, 'v': 0.0}]
    
    # Wavelength grid (dense)
    wave = np.linspace(lam_rest - 5, lam_rest + 5, 10000)
    dlam = wave[1] - wave[0]
    
    tau = engine.compute_optical_depth(wave, ['HI_Lya'], comps)
    
    # Calculate analytic integral of tau d(nu)
    # Integral tau d(nu) = N * (pi e^2 / m_e c) * f
    # nu = c / lam -> dnu = (c / lam^2) dlam
    # Integral tau (c / lam^2) dlam = N * (pi e^2 / m_e c) * f
    # Integral tau dlam = N * (pi e^2 / m_e c^2) * f * lam_rest^2
    
    e = 4.8032e-10
    me = 9.10938e-28
    c = 2.9979e10
    
    analytic_W = N * (np.pi * e**2 / (me * c**2)) * f_osc * (lam_rest * 1e-8)**2 * 1e8 # in Angstroms
    
    numeric_W = np.sum(tau) * dlam
    
    print("--- Test 1: Optically Thin Integral (tau) ---")
    print(f"Analytic Int(tau dlam): {analytic_W:.6e} Angstroms")
    print(f"Numeric  Int(tau dlam): {numeric_W:.6e} Angstroms")
    print(f"Ratio: {numeric_W / analytic_W:.5f}")
    assert np.isclose(numeric_W, analytic_W, rtol=1e-3), "Optical depth integral does not match analytic expectation."

def test_damping_wings():
    z = 0.0
    engine = RadiativeTransferEngine(z_abs=z)
    lam_rest, f_osc, gamma = engine.atomic.get('HI_Lya')
    
    # Damped component
    logN = 20.0
    b = 10.0
    comps = [{'N': 10**logN, 'b': b, 'v': 0.0}]
    
    # Far wing at delta_lam = 10 A
    wave = np.array([lam_rest + 10.0])
    tau = engine.compute_optical_depth(wave, ['HI_Lya'], comps)
    
    # Analytic wing tau:
    # tau(delta_lam) = N * (e^2 / m c^3) * f * (lam^4 * Gamma / (4 pi delta_lam^2))
    e = 4.8032e-10
    me = 9.10938e-28
    c = 2.9979e10
    
    delta_lam = 10.0 * 1e-8
    lam_cm = lam_rest * 1e-8
    
    analytic_tau_wing = (10**logN) * (e**2 / (me * c**3)) * f_osc * (lam_cm**4 * gamma / (4 * np.pi * delta_lam**2))
    
    print("\n--- Test 2: Damping Wing Optical Depth ---")
    print(f"Analytic tau at 10 A: {analytic_tau_wing:.6e}")
    print(f"Numeric  tau at 10 A: {tau[0]:.6e}")
    print(f"Ratio: {tau[0] / analytic_tau_wing:.5f}")
    assert np.isclose(tau[0], analytic_tau_wing, rtol=1e-2), "Damping wings do not match analytic expectation."

if __name__ == '__main__':
    test_optically_thin()
    test_damping_wings()
    print("\nAll physical RT engine unit tests passed.")
