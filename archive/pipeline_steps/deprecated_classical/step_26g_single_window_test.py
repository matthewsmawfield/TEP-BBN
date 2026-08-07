import json
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import sys

script_dir = Path(__file__).parent
project_root = script_dir.parent.parent
sys.path.insert(0, str(project_root))

from scripts.lib.physical_rt_engine import RadiativeTransferEngine
from step_26c_load_vpfit_model import parse_vpfit

def test_single_window():
    manifest_path = project_root / 'data' / 'processed' / 'Q1009_union_manifest.json'
    vpfit_path = project_root / 'data' / 'literature_components' / 'model_1a.26'
    
    with open(manifest_path, 'r') as f:
        manifest = json.load(f)
        
    z_abs_ref = manifest['z_abs']
    c_kms = 299792.458
    
    # We want to isolate the Lya window of C1x1
    target_coadd = 'q1011p2941_C1x1.dat'
    chunk_data = None
    
    for chunk in manifest['coadds'][target_coadd]:
        w_center = 0.5 * (chunk['wave'][0] + chunk['wave'][-1])
        if 4250 < w_center < 4270:
            chunk_data = chunk
            break
            
    if not chunk_data:
        raise ValueError("Lya chunk not found in C1x1")
        
    wave = np.array(chunk_data['wave'])
    flux_obs = np.array(chunk_data['flux'])
    err = np.array(chunk_data['err'])
    mask = err > 0
    
    # 1. Principal HI Components (A, B, C)
    # Looking at step_26f table, component 0 is D I. 
    # Component 1 (z=2.50434), Comp 2 (z=2.50021), Comp 3 (z=2.50076)... wait.
    # The actual primary component A is tied to 2.5036379403A. 
    # Let's read the parsed table directly to separate them.
    components = parse_vpfit(vpfit_path)
    
    # Filter for components around z=2.50
    comps_250 = [c for c in components if 2.49 < c['z'] < 2.51]
    
    # Primary A is the one with logN ~ 17.36
    primary_A = next(c for c in comps_250 if abs(c['logN'] - 17.36) < 0.1)
    # DI is the only D I
    comp_DI = next(c for c in comps_250 if c['ion'] == 'D_I')
    
    # Other HI interlopers at z=2.50
    other_hi_250 = [c for c in comps_250 if c['ion'] == 'H_I' and c != primary_A]
    
    engine = RadiativeTransferEngine(z_abs=z_abs_ref)
    
    def convert_to_comps(c_list, is_di=False):
        res = []
        for c in c_list:
            v = c_kms * (c['z'] - z_abs_ref) / (1.0 + z_abs_ref)
            if is_di:
                v -= 81.6
            res.append({'N': 10**c['logN'], 'b': c['b'], 'v': v})
        return res
        
    # Steps
    # Step 1: Principal H I
    tau_1 = engine.compute_optical_depth(wave, ['HI_Lya'], convert_to_comps([primary_A]))
    # Step 2: Add D I
    tau_2 = tau_1 + engine.compute_optical_depth(wave, ['HI_Lya'], convert_to_comps([comp_DI], is_di=True))
    # Step 3: Add relevant interlopers
    tau_3 = tau_2 + engine.compute_optical_depth(wave, ['HI_Lya'], convert_to_comps(other_hi_250))
    
    # Step 4: Continuum. Let's just fit a degree 1 chebyshev to the final tau for demonstration.
    w_min, w_max = wave[0], wave[-1]
    x_norm = 2.0 * (wave - w_min) / (w_max - w_min) - 1.0
    P = np.zeros((len(wave), 2))
    P[:, 0] = 1.0
    P[:, 1] = x_norm
    
    X = P * np.exp(-tau_3)[:, np.newaxis]
    X_mask = X[mask]
    W = 1.0 / err**2
    W_mask = W[mask]
    y_mask = flux_obs[mask]
    
    c_opt = np.linalg.solve(X_mask.T @ (W_mask[:, np.newaxis] * X_mask), X_mask.T @ (W_mask * y_mask))
    
    flux_mod_4 = (P @ c_opt) * np.exp(-tau_3)
    
    # Step 6: Convolution
    flux_mod_6 = engine.apply_convolution(flux_mod_4, wave, 3.0)
    
    fig, axes = plt.subplots(3, 1, figsize=(10, 10))
    ax = axes[0]
    ax.step(wave, flux_obs, color='k', alpha=0.5, label='Data')
    ax.plot(wave, (P @ c_opt) * np.exp(-tau_1), label='1. Primary HI')
    ax.plot(wave, (P @ c_opt) * np.exp(-tau_2), label='2. + DI')
    ax.legend()
    ax.set_title("Steps 1-2: Primary + DI")
    
    ax = axes[1]
    ax.step(wave, flux_obs, color='k', alpha=0.5)
    ax.plot(wave, flux_mod_4, label='3-4. + Interlopers + Cont', color='green')
    ax.plot(wave, flux_mod_6, label='6. + Convol', color='red')
    ax.legend()
    ax.set_title("Steps 3-6: Interlopers & Convolution")
    
    ax = axes[2]
    res = (flux_obs - flux_mod_6) / err
    ax.step(wave[mask], res[mask], color='k', alpha=0.5)
    ax.axhline(0, color='r', linestyle='--')
    ax.set_title(f"Residuals (Step 6) - RMS: {np.sqrt(np.mean(res[mask]**2)):.2f}")
    
    plt.tight_layout()
    out_path = project_root / 'data' / 'processed' / 'step3c_single_window.png'
    plt.savefig(out_path)
    print(f"Saved single window test to {out_path}")
    print(f"Step 6 RMS residual: {np.sqrt(np.mean(res[mask]**2)):.2f}")
    print(f"Step 6 Reduced Chi2: {np.sum(res[mask]**2) / (np.sum(mask) - 2):.2f}")

if __name__ == '__main__':
    test_single_window()
