import numpy as np
from astropy.io import fits
import json
import sys
from pathlib import Path
from scipy.signal import correlate

script_dir = Path(__file__).parent
project_root = script_dir.parent.parent
sys.path.insert(0, str(project_root))

def parse_squad_fits(filepath):
    with fits.open(filepath) as hdul:
        header = hdul[0].header
        array = np.asarray(hdul[0].data)
        
        flux = array[0]
        error = array[1]
        continuum = array[3]
        
        crval1 = header['CRVAL1']
        cdelt1 = header['CDELT1']
        crpix1 = header['CRPIX1']
        
        pixel = np.arange(flux.shape[0]) + 1
        log_wave = crval1 + (pixel - crpix1) * cdelt1
        wavelength = 10**log_wave
        
        # normalize
        valid = (continuum > 0)
        norm_flux = np.ones_like(flux)
        norm_err = np.zeros_like(error)
        norm_flux[valid] = flux[valid] / continuum[valid]
        norm_err[valid] = error[valid] / continuum[valid]
        
        return wavelength, norm_flux, norm_err

def calc_velocity(wl, rest_wl):
    c_kms = 299792.458
    return c_kms * (wl - rest_wl) / rest_wl
    
def extract_window(wl, fl, er, rest_wl, vmin, vmax):
    v = calc_velocity(wl, rest_wl)
    mask = (v >= vmin) & (v <= vmax)
    return v[mask], fl[mask], er[mask]

def build_template(v_grid):
    # A=0.0, B=10.863, C=14.713
    # Use simple gaussians for the absorption lines
    def g(v, v0, b, depth):
        return depth * np.exp(-((v - v0)/b)**2)
        
    t = np.zeros_like(v_grid)
    t += g(v_grid, 0.0, 6.0, 0.8)
    t += g(v_grid, 10.863, 5.0, 0.4)
    t += g(v_grid, 14.713, 5.0, 0.2)
    return t

def main():
    print("Step 20: UVES-to-HIRES Metal Registration (Q1009+2956)")
    print("=" * 60)
    
    fits_path = project_root / "data/raw/reduced_products/Q1009+2956_z2.504/J101155+294141/J101155+294141.fits"
    if not fits_path.exists():
        print(f"Error: Could not find {fits_path}")
        return
        
    wl, fl, er = parse_squad_fits(fits_path)
    z_ref_hires = 2.5035873411
    
    transitions = {
        "CII_1334": 1334.5323,
        "SiIV_1393": 1393.7550,
        "SiIV_1402": 1402.7700,
        "CIV_1548": 1548.1950,
        "CIV_1550": 1550.7700
    }
    
    results = {}
    offsets = []
    
    # Common velocity grid for interpolation
    v_grid = np.linspace(-150, 150, 301) # 1 km/s steps
    template = build_template(v_grid)
    
    for name, rest_wl in transitions.items():
        obs_wl = rest_wl * (1.0 + z_ref_hires)
        v_win, f_win, e_win = extract_window(wl, fl, er, obs_wl, -200, 200)
        
        if len(v_win) < 10:
            print(f"  {name}: insufficient coverage")
            results[name] = {"status": "insufficient_coverage"}
            continue
            
        valid = ~np.isnan(f_win) & (e_win > 0)
        if np.sum(valid) < 10:
            continue
            
        f_interp = np.interp(v_grid, v_win[valid], f_win[valid])
        
        # absorption depth
        obs_depth = 1.0 - f_interp
        obs_depth[obs_depth < 0] = 0
        
        # cross correlate
        corr = correlate(obs_depth, template, mode='same')
        
        # The peak of corr gives the shift
        # center of correlate array is at index len(v_grid)//2
        center_idx = len(v_grid)//2
        peak_idx = np.argmax(corr)
        shift_bins = peak_idx - center_idx
        # since dv = 1 km/s step, shift_bins is the shift in km/s
        # If template is shifted right, peak_idx > center_idx, means obs_depth is shifted right by shift_bins relative to template
        dv = float(shift_bins)
        
        # Check signal strength
        max_corr = np.max(corr)
        if max_corr > 10.0 and abs(dv) < 40.0:
            print(f"  {name}: dv = {dv:+.3f} km/s")
            results[name] = {"dv_kms": dv, "dv_err_kms": 1.0, "status": "fitted"}
            offsets.append(dv)
        else:
            print(f"  {name}: low SNR or poor fit")
            results[name] = {"status": "poor_fit"}

    combined = float(np.median(offsets)) if offsets else None
    scatter = float(np.std(offsets)) if len(offsets) > 1 else None
    
    out = {
        "per_transition_offsets_kms": results,
        "combined_offset_kms": combined,
        "combined_uncertainty_kms": scatter,
        "between_line_scatter_kms": scatter,
        "registration_pass": len(offsets) >= 3,
        "D_window_used": False
    }
    
    with open(project_root / "data/processed/Q1009+2956_UVES_HIRES_registration.json", "w") as f:
        json.dump(out, f, indent=2)
        
    if combined is not None:
        print(f"\nFinal UVES-HIRES Offset: {combined:+.3f} km/s (Used {len(offsets)} lines)")
    else:
        print("\nFinal UVES-HIRES Offset: FAILED (No lines could be fitted)")

if __name__ == "__main__":
    main()
