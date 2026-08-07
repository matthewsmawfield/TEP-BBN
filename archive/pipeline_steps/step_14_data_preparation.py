import glob
from astropy.io import fits
import numpy as np
from scipy.interpolate import interp1d

def prepare_spectrum():
    files = glob.glob('data/processed/reduced/Q0913+072_z2.618/reduced_UVES*.fits')
    
    # Common grid from the first file
    with fits.open(files[0]) as hdul:
        w_grid = hdul['WAVELENGTH'].data
        
    flux_sum = np.zeros_like(w_grid)
    ivar_sum = np.zeros_like(w_grid)

    for f in files:
        with fits.open(f) as hdul:
            flux = hdul[0].data
            err = hdul['ERROR'].data
            w = hdul['WAVELENGTH'].data
            
            # Interpolate to common grid
            f_interp = interp1d(w, flux, bounds_error=False, fill_value=0.0)(w_grid)
            e_interp = interp1d(w, err, bounds_error=False, fill_value=np.inf)(w_grid)
            
            e_interp[e_interp == 0] = np.inf
            ivar = 1.0 / (e_interp**2)
            
            flux_sum += f_interp * ivar
            ivar_sum += ivar

    # Avoid div zero
    mask_valid = ivar_sum > 0
    coadd_flux = np.zeros_like(w_grid)
    coadd_err = np.ones_like(w_grid) * np.inf
    
    coadd_flux[mask_valid] = flux_sum[mask_valid] / ivar_sum[mask_valid]
    coadd_err[mask_valid] = np.sqrt(1.0 / ivar_sum[mask_valid])

    # Convert to velocity relative to Lyman alpha at z=2.61843
    z = 2.61843
    lya_rest = 1215.67
    lya_obs = lya_rest * (1 + z)
    c_kms = 299792.458
    
    v_grid = c_kms * (w_grid - lya_obs) / lya_obs

    # Select window [-400, 200]
    mask = (v_grid >= -400) & (v_grid <= 200) & mask_valid
    v_mask = v_grid[mask]
    f_mask = coadd_flux[mask]
    e_mask = coadd_err[mask]

    # Simple linear continuum fit using edges
    edge_mask = ((v_mask >= -400) & (v_mask <= -300)) | ((v_mask >= 100) & (v_mask <= 200))
    if np.sum(edge_mask) > 10:
        p = np.polyfit(v_mask[edge_mask], f_mask[edge_mask], 1)
        continuum = np.polyval(p, v_mask)
    else:
        continuum = np.ones_like(v_mask) * np.median(f_mask)

    f_norm = f_mask / continuum
    e_norm = e_mask / continuum

    # Restrict to [-300, 100]
    final_mask = (v_mask >= -300) & (v_mask <= 100)
    v_final = v_mask[final_mask]
    f_final = f_norm[final_mask]
    e_final = e_norm[final_mask]

    output_path = 'data/processed/Q0913+072_1D_spectrum.txt'
    np.savetxt(output_path, np.column_stack([v_final, f_final, e_final]), 
               header="velocity_kms flux error", fmt="%.5f")
    print(f"Saved {len(v_final)} pixels to {output_path}")

if __name__ == '__main__':
    prepare_spectrum()
