import json
import sys
import os
import requests
from pathlib import Path
import numpy as np
from astropy.io.votable import parse_single_table
from astropy.io import fits
import io

script_dir = Path(__file__).parent
project_root = script_dir.parent.parent
sys.path.insert(0, str(project_root))

def resolve_eso_datalink(access_url):
    print(f"  [*] Resolving datalink: {access_url}")
    xml_data = requests.get(access_url).content
    table = parse_single_table(io.BytesIO(xml_data))
    for row in table.array:
        sem = row['semantics']
        if isinstance(sem, bytes):
            sem = sem.decode('utf-8')
        if '#this' in sem:
            fits_url = row['access_url']
            if isinstance(fits_url, bytes):
                fits_url = fits_url.decode('utf-8')
            return fits_url
    return None

def main():
    print("Step 16a: Download Public Candidates")
    print("=" * 60)
    
    candidates_file = project_root / "data/processed/public_dh_target_candidates.json"
    if not candidates_file.exists():
        print("No public candidates file found.")
        return
        
    with open(candidates_file, 'r') as f:
        candidates = json.load(f)
        
    for c in candidates:
        if c['status'] == 'PUBLIC_SPECTRUM_FOUND':
            qso = c['qso_name']
            z_abs = c['absorber_redshift']
            system_id = c['system_id']
            url = c.get('access_url')
            
            if not url:
                print(f"Skipping {system_id}: No access_url")
                continue
                
            print(f"Processing {system_id}...")
            
            # 1. Resolve Datalink if it's ESO
            if 'datalink' in url:
                fits_url = resolve_eso_datalink(url)
                if not fits_url:
                    print(f"  [!] Could not resolve FITS URL from datalink.")
                    continue
            else:
                fits_url = url
                
            print(f"  [*] Downloading FITS from {fits_url} ...")
            r = requests.get(fits_url)
            fits_path = project_root / f"data/processed/temp_{system_id}.fits"
            with open(fits_path, 'wb') as f_out:
                f_out.write(r.content)
                
            # 2. Parse FITS
            print(f"  [*] Extracting 1D spectrum...")
            try:
                with fits.open(fits_path) as hdul:
                    # Find BINTABLE
                    table_hdu = None
                    for hdu in hdul:
                        if isinstance(hdu, fits.BinTableHDU):
                            table_hdu = hdu
                            break
                            
                    if not table_hdu:
                        print(f"  [!] No BINTABLE found in FITS.")
                        continue
                        
                    data = table_hdu.data
                    
                    # Columns might be WAVE, FLUX, ERR (or WAVELENGTH, FLUX_REDUCED, ERR_REDUCED)
                    wave_col = next((c for c in data.columns.names if 'WAVE' in c.upper()), None)
                    flux_col = next((c for c in data.columns.names if 'FLUX' in c.upper()), None)
                    err_col = next((c for c in data.columns.names if 'ERR' in c.upper()), None)
                    
                    if not wave_col or not flux_col:
                        print(f"  [!] Missing wave or flux columns: {data.columns.names}")
                        continue
                        
                    wave = data[wave_col]
                    flux = data[flux_col]
                    err = data[err_col] if err_col else np.ones_like(flux)
                    
                    # Check units
                    tunit = table_hdu.header.get(f"TUNIT{data.columns.names.index(wave_col)+1}", "Angstrom")
                    if 'nm' in tunit.lower() or np.max(wave) < 2000:
                        wave = wave * 10.0 # Convert to Angstroms
                        
                    # Calculate velocity and cut window
                    lya_rest = 1215.67
                    lya_obs = lya_rest * (1 + z_abs)
                    c_kms = 299792.458
                    
                    vel = c_kms * (wave - lya_obs) / lya_obs
                    
                    mask = (vel >= -350) & (vel <= 150) # Keep slightly wider window for normalization
                    v_cut = vel[mask]
                    f_cut = flux[mask]
                    e_cut = err[mask]
                    
                    if len(v_cut) == 0:
                        print("  [!] No data inside the Ly-alpha window after extraction.")
                        continue
                        
                    # Simple linear continuum normalization based on edges
                    # We will use [-320, -280] and [80, 120] to anchor the continuum
                    edge_mask = ((v_cut >= -320) & (v_cut <= -280)) | ((v_cut >= 80) & (v_cut <= 120))
                    if np.sum(edge_mask) > 5:
                        p = np.polyfit(v_cut[edge_mask], f_cut[edge_mask], 1)
                        cont = np.polyval(p, v_cut)
                        f_norm = f_cut / cont
                        e_norm = e_cut / cont
                    else:
                        # Fallback normalization
                        med = np.median(f_cut)
                        f_norm = f_cut / med
                        e_norm = e_cut / med
                        
                    # Cut exactly to [-300, 100]
                    final_mask = (v_cut >= -300) & (v_cut <= 100)
                    v_final = v_cut[final_mask]
                    f_final = f_norm[final_mask]
                    e_final = e_norm[final_mask]
                    
                    out_txt = project_root / f"data/processed/{system_id}_1D_spectrum.txt"
                    np.savetxt(out_txt, np.column_stack((v_final, f_final, e_final)), 
                               fmt="%.4f %.4e %.4e", header="velocity_kms flux_normalized error")
                               
                    prov = {
                        "source": "ESO Phase 3",
                        "access_url": url,
                        "fits_url": fits_url,
                        "archive_target_name": c.get('archive_target_name'),
                        "absorber_redshift": z_abs,
                        "lya_observed_wavelength_angstrom": lya_obs,
                        "wavelength_unit": tunit,
                        "velocity_window": [-300, 100],
                        "normalization_method": "linear_edge_fit",
                        "input_fits_columns": data.columns.names,
                        "output_path": str(out_txt.relative_to(project_root))
                    }
                    
                    prov_file = project_root / f"data/processed/{system_id}_spectrum_provenance.json"
                    with open(prov_file, 'w') as f_prov:
                        json.dump(prov, f_prov, indent=2)
                        
                    print(f"  [✓] Successfully saved 1D spectrum and provenance to {out_txt.name}")
                    
            except Exception as e:
                print(f"  [!] Error processing FITS: {e}")
                
            finally:
                if fits_path.exists():
                    os.remove(fits_path)

if __name__ == '__main__':
    main()
