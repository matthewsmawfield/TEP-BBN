from astropy.io import fits
import numpy as np
import matplotlib.pyplot as plt

def prepare_spectrum_from_adp():
    with fits.open('data/processed/Q0913+072_ADP.fits') as hdul:
        data = hdul[1].data
        wave = data['WAVE'][0]
        flux = data['FLUX'][0]
        err = data['ERR'][0]

    # Convert to velocity relative to Lyman alpha at z=2.61843
    z = 2.61843
    lya_rest = 1215.67
    lya_obs = lya_rest * (1 + z)
    c_kms = 299792.458
    
    v_grid = c_kms * (wave - lya_obs) / lya_obs

    # Select window [-500, 300] for continuum fitting
    mask = (v_grid >= -500) & (v_grid <= 300)
    v_mask = v_grid[mask]
    f_mask = flux[mask]
    e_mask = err[mask]

    # Simple linear continuum fit using edges
    # We use regions slightly outside the D/H window
    edge_mask = ((v_mask >= -500) & (v_mask <= -350)) | ((v_mask >= 150) & (v_mask <= 300))
    if np.sum(edge_mask) > 10:
        p = np.polyfit(v_mask[edge_mask], f_mask[edge_mask], 1)
        continuum = np.polyval(p, v_mask)
    else:
        continuum = np.ones_like(v_mask) * np.median(f_mask)

    f_norm = f_mask / continuum
    e_norm = e_mask / continuum

    # Restrict to [-300, 100] for nested sampling
    final_mask = (v_mask >= -300) & (v_mask <= 100)
    v_final = v_mask[final_mask]
    f_final = f_norm[final_mask]
    e_final = e_norm[final_mask]

    output_path = 'data/processed/Q0913+072_1D_spectrum.txt'
    np.savetxt(output_path, np.column_stack([v_final, f_final, e_final]), 
               header="velocity_kms flux error", fmt="%.5f")
    print(f"Saved {len(v_final)} pixels to {output_path}")

if __name__ == '__main__':
    prepare_spectrum_from_adp()
