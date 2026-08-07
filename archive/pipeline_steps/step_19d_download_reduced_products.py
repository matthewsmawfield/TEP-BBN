import os
import sys
import json
import tarfile
import hashlib
import numpy as np
from pathlib import Path
from astropy.io import fits
from astropy.wcs import WCS
import requests
import argparse
import shutil

CANDIDATES_PATH = Path("data/processed/reduced_product_candidates.json")
RAW_REDUCED_DIR = Path("data/raw/reduced_products")
PROCESSED_DIR = Path("data/processed")
IMPORT_REPORT_PATH = Path("data/processed/reduced_product_import_report.json")

# Create dirs
RAW_REDUCED_DIR.mkdir(parents=True, exist_ok=True)

def calculate_velocity_kms(wavelength_obs, wavelength_rest):
    c = 299792.458 # km/s
    return c * (wavelength_obs - wavelength_rest) / wavelength_rest

def safe_extract(tar, destination):
    destination = destination.resolve()
    for member in tar.getmembers():
        target = (destination / member.name).resolve()
        if destination not in target.parents and target != destination:
            raise RuntimeError(f"Unsafe tar member: {member.name}")
    tar.extractall(destination)

def parse_squad_fits(filepath):
    """
    Parses SQUAD Final Spectrum FITS.
    Primary HDU is a 9xN array.
    """
    with fits.open(filepath) as hdul:
        header = hdul[0].header
        array = np.asarray(hdul[0].data)
        
        flux = array[0]
        error = array[1]
        continuum = array[3]
        pixel_status = array[4]
        
        crval1 = header['CRVAL1']
        crpix1 = header['CRPIX1']
        cdelt1 = header.get('CD1_1', header.get('CDELT1'))
        
        n_pixels = array.shape[1]
        pixel = np.arange(n_pixels) + 1.0
        log_wave = crval1 + (pixel - crpix1) * cdelt1
        wavelength = 10.0 ** log_wave
        
        valid = (
            np.isfinite(flux)
            & np.isfinite(error)
            & (error > 0)
            & (pixel_status == 1)
        )
        
        return wavelength[valid], flux[valid], error[valid], header

def parse_kodiaq_fits(filepath):
    """
    Parses KODIAQ FITS spectra.
    Typically they are simple 1D arrays or BINTABLEs.
    """
    with fits.open(filepath) as hdul:
        # Check if BINTABLE
        if len(hdul) > 1 and isinstance(hdul[1], fits.BinTableHDU):
            data = hdul[1].data
            header = hdul[0].header
            wavelength = data['WAVELENGTH']
            flux = data['FLUX']
            error = data['ERROR']
        else:
            # Try simple 1D array WCS
            header = hdul[0].header
            data = hdul[0].data
            if len(data.shape) == 2:
                # Might be flux and error in rows
                flux = data[0]
                error = data[1] if data.shape[0] > 1 else np.zeros_like(flux)
            else:
                flux = data
                error = np.zeros_like(flux) # Needs _e.fits file usually
            
            wcs = WCS(header)
            n_pixels = len(flux)
            pixel = np.arange(n_pixels)
            wavelength = wcs.pixel_to_world_values(pixel)[0]
            
        valid = np.isfinite(flux) & np.isfinite(error) & (error > 0)
        return wavelength[valid], flux[valid], error[valid], header

def extract_window(wavelength, flux, error, req_lya, vmin, vmax):
    v = calculate_velocity_kms(wavelength, req_lya)
    mask = (v >= vmin) & (v <= vmax)
    return v[mask], wavelength[mask], flux[mask], error[mask]

def get_sha256(filepath):
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def process_candidate(cand):
    sys_id = cand['system_id']
    target_dir = RAW_REDUCED_DIR / sys_id
    target_dir.mkdir(parents=True, exist_ok=True)
    
    archive = cand['archive']
    req_lya = cand['required_lya_angstrom']
    
    c_kms = 299792.458
    kinematic_reference_redshift_hires = None
    kinematic_reference_redshift_uves = None
    uves_hires_registration_kms = None

    if sys_id == "Q1009+2956_z2.504":
        reg_file = PROCESSED_DIR / "Q1009+2956_UVES_HIRES_registration.json"
        if reg_file.exists():
            with open(reg_file, "r") as f:
                reg_data = json.load(f)
            uves_hires_registration_kms = reg_data.get("combined_offset_kms")
            if uves_hires_registration_kms is not None:
                kinematic_reference_redshift_hires = 2.5035873411
                delta_v = uves_hires_registration_kms
                z_ref_uves = kinematic_reference_redshift_hires + (delta_v / c_kms) * (1.0 + kinematic_reference_redshift_hires)
                kinematic_reference_redshift_uves = z_ref_uves
                req_lya = 1215.67 * (1.0 + z_ref_uves)
                print(f"  Applied UVES registration offset: {delta_v:+.3f} km/s. New req_lya={req_lya:.4f}")
    
    print(f"Processing {sys_id} from {archive}...")
    
    fits_path = None
    
    # Check for manual individual tarball or fits
    expected = cand['expected_filename']
    if expected:
        local_expected = target_dir / expected
        if local_expected.exists():
            if expected.endswith('.tar.gz'):
                with tarfile.open(local_expected, 'r:gz') as tar:
                    safe_extract(tar, target_dir)
                # Find the fits
                for f in target_dir.glob("*.fits"):
                    fits_path = f
                    break
            elif expected.endswith('.fits'):
                fits_path = local_expected
            
    # Check full archive fallback for SQUAD
    if not fits_path and archive == "SQUAD_DR1" and expected:
        full_archive = RAW_REDUCED_DIR / "DR1_Final_Spectra.tar.gz"
        if full_archive.exists():
            print(f"  Extracting {expected} from full DR1 archive...")
            with tarfile.open(full_archive, 'r:gz') as tar:
                # Find the specific tarball inside the master tarball, or the fits itself
                for member in tar.getmembers():
                    if expected in member.name or (cand['archive_object_id'] in member.name and member.name.endswith('.fits')):
                        target_member = (target_dir / member.name).resolve()
                        if target_dir not in target_member.parents and target_member != target_dir:
                            continue
                        tar.extract(member, path=target_dir)
                        if member.name.endswith('.fits'):
                            fits_path = target_dir / member.name
                        elif member.name.endswith('.tar.gz'):
                            sub_tar_path = target_dir / member.name
                            with tarfile.open(sub_tar_path, 'r:gz') as sub_tar:
                                safe_extract(sub_tar, target_dir)
                            for f in target_dir.glob("*.fits"):
                                fits_path = f
                                break
                        break
                        
    if not fits_path:
        # Recursive fallback discovery, especially for KODIAQ without exact filename
        candidate_files = [
            *target_dir.rglob("*.fits"),
            *target_dir.rglob("*.fits.gz")
        ]
        if candidate_files:
            fits_path = candidate_files[0] # Picking the first one; robust header matching is done during import
            
    if not fits_path:
        print(f"  [!] MANUAL_DOWNLOAD_REQUIRED: Could not find {expected} or extracted FITS in {target_dir}")
        return
        
    print(f"  Found FITS: {fits_path.name}")
    
    try:
        if archive == "SQUAD_DR1":
            wl, fl, er, hdr = parse_squad_fits(fits_path)
        else:
            wl, fl, er, hdr = parse_kodiaq_fits(fits_path)
            
        # Extract science window [-300, +100]
        v_sci, wl_sci, fl_sci, er_sci = extract_window(wl, fl, er, req_lya, -300, 100)
        
        # Extract aux window [-500, +300]
        v_aux, wl_aux, fl_aux, er_aux = extract_window(wl, fl, er, req_lya, -500, 300)
        
        if len(v_sci) == 0:
            print(f"  [!] Error: No data found in the [-300, +100] km/s window around {req_lya} A.")
            return
            
        # S/N sideband calculation
        sideband = (
            ((v_aux >= -500) & (v_aux < -350))
            | ((v_aux > 150) & (v_aux <= 300))
        )
        
        valid_snr = sideband & np.isfinite(er_aux) & (er_aux > 0) & np.isfinite(fl_aux)
        if np.any(valid_snr):
            snr = np.nanmedian(fl_aux[valid_snr] / er_aux[valid_snr])
        else:
            snr = -1.0 # Indeterminate local SNR
            
        print(f"  Extracted {len(v_sci)} pixels. Local sideband SNR: {snr:.1f}")
        
        out_sci = PROCESSED_DIR / f"{sys_id}_1D_spectrum.txt"
        out_aux = PROCESSED_DIR / f"{sys_id}_1D_spectrum_aux.txt"
        
        # Save Sci
        with open(out_sci, "w") as f:
            f.write("velocity_kms flux_normalized error\n")
            for i in range(len(v_sci)):
                f.write(f"{v_sci[i]:.4f} {fl_sci[i]:.4f} {er_sci[i]:.4f}\n")
                
        # Save Aux
        with open(out_aux, "w") as f:
            f.write("velocity_kms flux_normalized error\n")
            for i in range(len(v_aux)):
                f.write(f"{v_aux[i]:.4f} {fl_aux[i]:.4f} {er_aux[i]:.4f}\n")
                
        prov = {
            "system_id": sys_id,
            "archive": archive,
            "archive_object_id": cand['archive_object_id'],
            "source_file": fits_path.name,
            "sha256": get_sha256(fits_path),
            "extraction_window_kms": [-300, 100],
            "required_lya_angstrom": req_lya,
            "median_snr": float(snr),
            "status": "LOW_SNR_OUTSIDE_VALIDATED_DOMAIN" if snr < 30 else "READY_FOR_FEATURE_VECTOR"
        }
        
        if sys_id == "Q1009+2956_z2.504":
            prov.update({
                "literature_measurement": {
                    "instrument": "Keck/HIRES",
                    "reference": "Zavarygin et al.",
                    "arxiv": "1706.09512"
                },
                "tep_bbn_spectrum": {
                    "archive": "SQUAD_DR1",
                    "instrument": "VLT/UVES",
                    "archive_object_id": cand['archive_object_id']
                },
                "kinematic_prior": {
                    "instrument": "Keck/HIRES",
                    "source_type": "METALS_ONLY_VPFIT"
                },
                "kinematic_reference_redshift_hires": kinematic_reference_redshift_hires,
                "uves_hires_registration_kms": uves_hires_registration_kms,
                "kinematic_reference_redshift_uves": kinematic_reference_redshift_uves
            })
            
        with open(PROCESSED_DIR / f"{sys_id}_spectrum_provenance.json", "w") as f:
            json.dump(prov, f, indent=2)
            
        print(f"  [+] Saved {out_sci.name} and provenance.")
        
    except Exception as e:
        print(f"  [!] Error parsing/extracting {fits_path.name}: {e}")

def import_downloads(import_dir, candidates):
    import_dir = Path(import_dir).expanduser().resolve()
    print(f"Scanning {import_dir} for potential FITS/tarballs...")
    
    candidate_files = [
        *import_dir.rglob("*.fits"),
        *import_dir.rglob("*.fits.gz"),
        *import_dir.rglob("*.tar.gz")
    ]
    
    report = []
    
    for fpath in candidate_files:
        status = "RAW_PRODUCT_REJECTED"
        matched_cand = None
        
        # Check against expected SQUAD tarballs
        if fpath.name.endswith(".tar.gz"):
            for cand in candidates:
                if cand['expected_filename'] and cand['expected_filename'] == fpath.name:
                    matched_cand = cand
                    status = "IMPORTED_AND_VALIDATED"
                    break
        else:
            # Check FITS headers
            try:
                hdr = fits.getheader(fpath)
                obj = str(hdr.get("OBJECT", hdr.get("TARGNAME", ""))).upper()
                instr = str(hdr.get("INSTRUME", "")).upper()
                
                if "HIRES" in instr or "UVES" in instr:
                    for cand in candidates:
                        cand_obj = cand['archive_object_id'].upper()
                        sys_id_base = cand['system_id'].split('_')[0].upper()
                        if obj and (cand_obj in obj or sys_id_base in obj):
                            matched_cand = cand
                            status = "IMPORTED_AND_VALIDATED"
                            break
                    if not matched_cand:
                        status = "ARCHIVE_RECOGNIZED_BUT_TARGET_UNCERTAIN"
            except Exception:
                status = "FITS_STRUCTURE_INVALID"
                
        if matched_cand and status == "IMPORTED_AND_VALIDATED":
            sys_id = matched_cand['system_id']
            target_dir = RAW_REDUCED_DIR / sys_id
            target_dir.mkdir(parents=True, exist_ok=True)
            
            dest_path = target_dir / fpath.name
            if not dest_path.exists():
                shutil.copy2(fpath, dest_path)
                print(f"  [+] Imported {fpath.name} to {sys_id}")
            
            report.append({
                "source_file": str(fpath),
                "system_id": sys_id,
                "status": status,
                "sha256": get_sha256(dest_path)
            })
        else:
            report.append({
                "source_file": str(fpath),
                "system_id": None,
                "status": status,
                "sha256": None
            })
            
    with open(IMPORT_REPORT_PATH, "w") as f:
        json.dump(report, f, indent=2)
    print(f"Import scan complete. Report written to {IMPORT_REPORT_PATH.name}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--import-downloads", type=str, help="Directory to scan for manually downloaded products")
    args = parser.parse_args()

    if not CANDIDATES_PATH.exists():
        print(f"No candidates file found at {CANDIDATES_PATH}. Run step 19c first.")
        return
        
    with open(CANDIDATES_PATH, "r") as f:
        candidates = json.load(f)
        
    if args.import_downloads:
        import_downloads(args.import_downloads, candidates)
        
    for cand in candidates:
        process_candidate(cand)

if __name__ == "__main__":
    main()
