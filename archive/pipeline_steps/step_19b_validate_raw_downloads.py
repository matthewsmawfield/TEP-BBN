import os
import json
import hashlib
import pandas as pd
from pathlib import Path
from astropy.io import fits

RAW_DIR = Path("data/raw/spectra")
MANIFEST_PATH = Path("data/processed/manual_spectrum_request_pack.csv")
REPORT_PATH = Path("data/processed/raw_download_validation_report.json")

def get_sha256(filepath):
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def validate_raw_downloads():
    if not MANIFEST_PATH.exists():
        print(f"Manifest not found: {MANIFEST_PATH}")
        return

    df = pd.read_csv(MANIFEST_PATH)
    target_map = {row['System']: row for _, row in df.iterrows()}
    
    report = []
    
    if not RAW_DIR.exists():
        print(f"Raw directory not found: {RAW_DIR}")
        return

    for fits_file in RAW_DIR.glob("*.fits"):
        print(f"Validating {fits_file.name}...")
        
        try:
            with fits.open(fits_file) as hdul:
                header = hdul[0].header
                
                # Extract metadata, handling potential missing keys gracefully
                obj_name = header.get("OBJECT", "UNKNOWN")
                instrument = header.get("INSTRUME", "UNKNOWN")
                ra_deg = header.get("RA", None)
                dec_deg = header.get("DEC", None)
                date_obs = header.get("DATE-OBS", "UNKNOWN")
                naxis = header.get("NAXIS", 0)
                naxis1 = header.get("NAXIS1", 0)
                naxis2 = header.get("NAXIS2", 0)
                
                # Check if it's a 2D echellogram vs 1D spectrum
                # Keck HIRES raw 2D echellograms typically have NAXIS=2 and NAXIS2 > 1
                is_raw_2d = False
                is_reduced_1d = False
                if naxis == 2 and naxis2 > 1:
                    is_raw_2d = True
                elif naxis == 1 or (naxis == 2 and naxis2 == 1):
                    is_reduced_1d = True
                
                # Determine system match
                system_id = "UNKNOWN"
                required_lya = 0.0
                for sys_name, sys_row in target_map.items():
                    # Strip standard prefixes to match Keck OBJECT headers which might be "q1009+2956" or "1009+2956"
                    clean_sys = sys_name.replace('Q', '').replace('HS', '').replace('J', '')
                    if sys_name.lower() in obj_name.lower() or clean_sys in obj_name:
                        system_id = sys_name
                        required_lya = sys_row.get("LyA_Observed_A", 0.0)
                        break
                        
                science_target_match = (system_id != "UNKNOWN")

                validation_entry = {
                    "system_id": system_id,
                    "koaid": fits_file.name.replace(".fits", ""),
                    "file_path": str(fits_file),
                    "sha256": get_sha256(fits_file),
                    "object": obj_name,
                    "instrument": instrument,
                    "ra_deg": ra_deg,
                    "dec_deg": dec_deg,
                    "date_obs": date_obs,
                    "is_raw_2d_echellogram": is_raw_2d,
                    "is_reduced_1d": is_reduced_1d,
                    "science_target_match": science_target_match,
                    "required_lya_wavelength_angstrom": required_lya,
                    "coverage_status": "UNKNOWN_UNTIL_REDUCED" if is_raw_2d else "NEEDS_CHECK",
                    "pipeline_status": "RAW_ONLY_REDUCTION_REQUIRED" if is_raw_2d else "READY_FOR_PROVENANCE"
                }
                report.append(validation_entry)
        except Exception as e:
            print(f"Error reading {fits_file.name}: {e}")
            report.append({
                "system_id": "ERROR",
                "koaid": fits_file.name.replace(".fits", ""),
                "file_path": str(fits_file),
                "error": str(e),
                "pipeline_status": "CORRUPT_OR_UNREADABLE"
            })

    # Save report
    with open(REPORT_PATH, "w") as f:
        json.dump(report, f, indent=2)
    print(f"\nValidation complete. Report saved to {REPORT_PATH}")
    
    # Print summary
    total = len(report)
    raw_2d = sum(1 for r in report if r.get("is_raw_2d_echellogram"))
    reduced_1d = sum(1 for r in report if r.get("is_reduced_1d"))
    matched = sum(1 for r in report if r.get("science_target_match"))
    print(f"Total files: {total}")
    print(f"Target Matched: {matched}")
    print(f"Raw 2D Echellograms: {raw_2d}")
    print(f"Reduced 1D Spectra: {reduced_1d}")

if __name__ == "__main__":
    validate_raw_downloads()
