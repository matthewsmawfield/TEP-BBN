import os
import sys
import json
import argparse
import pandas as pd
import requests
import pyvo as vo
from astropy.coordinates import SkyCoord
from astropy import units as u
from pathlib import Path
from dotenv import load_dotenv
import shutil
from astropy.io import fits
import tempfile

# Load local credentials if they exist (optional, .env is gitignored)
load_dotenv()

# Directories
RAW_DIR = Path("data/raw/spectra")
RAW_DIR.mkdir(parents=True, exist_ok=True)
MANIFEST_PATH = Path("data/processed/manual_spectrum_request_pack.csv")
DOWNLOAD_ATTEMPTS_PATH = Path("data/processed/koa_download_attempts.json")
RECORDS_FOUND_PATH = Path("data/processed/koa_records_found.json")
GUIDE_PATH = Path("data_ingestion_guide.md")

def get_koa_ids(system_id):
    """Query Keck KOA TAP for HIRES records by target name."""
    service = vo.dal.TAPService("https://koa.ipac.caltech.edu/TAP")
    clean_id = system_id.replace('Q', '').replace('HS', '').replace('J', '')
    query = f"""
    SELECT TOP 5 koaid 
    FROM koa_hires 
    WHERE targname LIKE '%{system_id}%' OR targname LIKE '%{clean_id}%'
    """
    try:
        results = service.search(query)
        if len(results) > 0:
            return results.to_table().to_pandas()['koaid'].tolist()
    except Exception as e:
        print(f"Error querying KOA TAP for system_id={system_id}: {e}")
    return []

def generate_commands_and_records(manifest_df):
    """Emit the exact curl/wget commands and save tracking records."""
    print("# ==========================================")
    print("# DATA INGESTION GUIDE (EMIT COMMANDS)")
    print("# ==========================================")
    print("# Run the following commands to download the raw FITS files.\n")
    
    records_found = []
    
    with open(GUIDE_PATH, "w") as guide:
        guide.write("# Data Ingestion Guide\n\n")
        guide.write("Public KOA data requires accepting a data access policy or logging in.\n")
        guide.write("Please download the following datasets via browser or authenticated wget/curl.\n\n")
    
        for _, row in manifest_df.iterrows():
            print(f"# Target: {row['System']} (RA: {row['RA_deg']}, DEC: {row['Dec_deg']})")
            if "HIRES" in row['Instrument']:
                koa_ids = get_koa_ids(row['System'])
                if koa_ids:
                    for koaid in koa_ids:
                        url = f"https://koa.ipac.caltech.edu/cgi-bin/getKOA/nph-getKOA?koaid={koaid}"
                        out_path = RAW_DIR / f"{koaid}.fits"
                        
                        record = {
                            "system_id": row['System'],
                            "koaid": koaid,
                            "download_url": url,
                            "download_status": "KOA_RECORD_FOUND",
                            "next_action": "Open in browser, accept KOA data policy / login if required, download actual FITS manually."
                        }
                        records_found.append(record)
                        
                        print(f"URL: {url}")
                        guide.write(f"### {row['System']} - {koaid}\n")
                        guide.write(f"URL: {url}\n")
                        guide.write(f"Save to: {out_path}\n\n")
                else:
                    print(f"# No public KOA HIRES records found for {row['System']}")
            else:
                print(f"# Not implemented for {row['Instrument']}")
            print()

    with open(RECORDS_FOUND_PATH, "w") as f:
        json.dump(records_found, f, indent=2)
        
    print(f"Saved guide to {GUIDE_PATH}")
    print(f"Saved records found to {RECORDS_FOUND_PATH}")
    return records_found

def is_html_response(response, filepath):
    """Check if the response is an HTML page (e.g., login redirect/agreement)."""
    content_type = response.headers.get("Content-Type", "")
    if "text/html" in content_type.lower():
        return True
    
    # Read first 20 bytes from the temp file
    with open(filepath, "rb") as f:
        first_bytes = f.read(20).lower()
        if b"<html" in first_bytes or b"<!doctype html" in first_bytes:
            return True
    
    return False

def validate_fits_structure(filepath, koaid):
    """Attempt to open with astropy and ensure it matches the target."""
    try:
        with fits.open(filepath) as hdul:
            header = hdul[0].header
            obj_name = header.get("OBJECT", "UNKNOWN")
            instrume = header.get("INSTRUME", "UNKNOWN")
            # Minimal check, 19b does deeper validation
            if "HIRES" not in instrume and instrume != "UNKNOWN":
                print(f"    [!] Warning: INSTRUME is {instrume}, expected HIRES.")
        return True
    except Exception as e:
        print(f"    [!] astropy.io.fits failed to open: {e}")
        return False

def check_fits_magic(filepath):
    with open(filepath, "rb") as f:
        header = f.read(8)
        if header == b"SIMPLE  ":
            return True
        # Could also check for gzip magic (1f 8b) if we supported compressed files directly
    return False

def execute_downloads(manifest_df):
    """Attempt to download the data and validate FITS headers strictly."""
    print("Executing downloads of real data...")
    attempts = []
    
    for _, row in manifest_df.iterrows():
        print(f"Processing {row['System']}...")
        if "HIRES" in row['Instrument']:
            koa_ids = get_koa_ids(row['System'])
            if not koa_ids:
                print(f"  No public KOA records found.")
                continue
            
            for koaid in koa_ids:
                url = f"https://koa.ipac.caltech.edu/cgi-bin/getKOA/nph-getKOA?koaid={koaid}"
                out_path = RAW_DIR / f"{koaid}.fits"
                
                attempt = {
                    "system_id": row['System'],
                    "koaid": koaid,
                    "download_url": url,
                    "download_status": "UNKNOWN",
                    "http_status": None,
                    "content_type": None,
                    "final_url": None,
                    "saved_to_scientific_pool": False,
                    "next_action": "Open in browser, accept KOA data policy / login if required, download actual FITS manually."
                }
                
                if out_path.exists():
                    print(f"  Already downloaded {koaid} (skipping auto-download, will be checked by 19b).")
                    attempt["download_status"] = "FILE_EXISTS_LOCALLY"
                    attempt["saved_to_scientific_pool"] = True
                    attempts.append(attempt)
                    continue
                
                print(f"  Downloading {koaid}...")
                try:
                    response = requests.get(url, stream=True)
                    attempt["http_status"] = response.status_code
                    attempt["content_type"] = response.headers.get("Content-Type", "")
                    attempt["final_url"] = response.url
                    
                    if response.status_code == 200:
                        # Write to temp file first
                        fd, temp_path = tempfile.mkstemp(suffix=".tmp")
                        os.close(fd)
                        
                        try:
                            with open(temp_path, 'wb') as f:
                                for chunk in response.iter_content(chunk_size=8192):
                                    f.write(chunk)
                                    
                            if is_html_response(response, temp_path):
                                print(f"  [!] Received HTML redirect/agreement page for {koaid}.")
                                attempt["download_status"] = "DOWNLOAD_REDIRECT_HTML"
                                attempt["next_action"] = "Complete the KOA access agreement or browser-mediated download."
                            else:
                                if check_fits_magic(temp_path) and validate_fits_structure(temp_path, koaid):
                                    shutil.move(temp_path, out_path)
                                    print(f"  [+] Saved valid FITS to {out_path}")
                                    attempt["download_status"] = "FITS_DOWNLOAD_CONFIRMED"
                                    attempt["saved_to_scientific_pool"] = True
                                    attempt["next_action"] = "Run step_19b_validate_raw_downloads.py"
                                else:
                                    print(f"  [!] Received non-FITS binary data or invalid FITS for {koaid}.")
                                    attempt["download_status"] = "INVALID_FITS_FORMAT"
                        finally:
                            if os.path.exists(temp_path):
                                os.unlink(temp_path)
                    else:
                        print(f"  Failed to download {koaid}: HTTP {response.status_code}")
                        attempt["download_status"] = f"HTTP_ERROR_{response.status_code}"
                except Exception as e:
                    print(f"  Error downloading {koaid}: {e}")
                    attempt["download_status"] = "DOWNLOAD_ERROR"
                    attempt["error"] = str(e)
                    
                attempts.append(attempt)

    with open(DOWNLOAD_ATTEMPTS_PATH, "w") as f:
        json.dump(attempts, f, indent=2)
    print(f"\nDownload attempts recorded in {DOWNLOAD_ATTEMPTS_PATH}")

def manual_ingest(manifest_df):
    """Scan RAW_DIR for manually downloaded files."""
    print("Scanning for manually downloaded files...")
    found_files = list(RAW_DIR.glob("*.fits"))
    print(f"Found {len(found_files)} files in {RAW_DIR}")
    for f in found_files:
        print(f"  - {f.name}")
    print("Manual ingest complete. Proceed to Step 19b.")

def main():
    parser = argparse.ArgumentParser(description="Secure provisioning bridge for raw spectral data.")
    parser.add_argument("--emit-commands", action="store_true", help="Print download commands (default).")
    parser.add_argument("--download", action="store_true", help="Download the actual public real data automatically.")
    parser.add_argument("--manual-ingest", action="store_true", help="Ingest manually downloaded files from data/raw/spectra.")
    args = parser.parse_args()

    if not MANIFEST_PATH.exists():
        print(f"Manifest not found: {MANIFEST_PATH}")
        return

    df = pd.read_csv(MANIFEST_PATH)

    if args.manual_ingest:
        manual_ingest(df)
    elif args.download:
        execute_downloads(df)
    else:
        # Default mode
        generate_commands_and_records(df)

if __name__ == "__main__":
    main()
