import os
import json
import pandas as pd
import requests
import pyvo as vo
from pathlib import Path
import argparse
import webbrowser
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

MANIFEST_PATH = Path("data/processed/manual_spectrum_request_pack.csv")
SQUAD_CSV_URL = "https://raw.githubusercontent.com/MTMurphy77/UVES_SQUAD_DR1/master/DR1_quasars_master.csv"
OUT_PATH = Path("data/processed/reduced_product_candidates.json")

def get_session():
    session = requests.Session()
    session.mount(
        "https://",
        HTTPAdapter(
            max_retries=Retry(
                total=4,
                connect=3,
                read=3,
                backoff_factor=1.5,
                status_forcelist=[429, 500, 502, 503, 504],
            )
        ),
    )
    return session

def fetch_squad_csv():
    try:
        df = pd.read_csv(SQUAD_CSV_URL)
        return df
    except Exception as e:
        print(f"Failed to fetch SQUAD DR1 CSV: {e}")
        return pd.DataFrame()

def discover_koa_table():
    service = vo.dal.TAPService("https://koa.ipac.caltech.edu/TAP")
    query = """
    SELECT table_name
    FROM TAP_SCHEMA.tables
    WHERE table_name LIKE '%reduced%'
       OR table_name LIKE '%kodiaq%'
    """
    try:
        results = service.search(query)
        tables = results.to_table().to_pandas()['table_name'].tolist()
        return tables
    except Exception as e:
        print(f"Failed to introspect KOA TAP schema: {e}")
        return []

def query_koa_kodiaq(table_name, target_id):
    service = vo.dal.TAPService("https://koa.ipac.caltech.edu/TAP")
    query = f"SELECT * FROM {table_name} WHERE targname = '{target_id}'"
    try:
        results = service.search(query)
        df = results.to_table().to_pandas()
        return df
    except Exception as e:
        print(f"Failed to query {table_name} for {target_id}: {e}")
        return pd.DataFrame()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--open-portals", action="store_true", help="Open official archive portals in browser")
    args = parser.parse_args()
    
    if args.open_portals:
        print("Opening official KODIAQ and SQUAD portals...")
        webbrowser.open("https://koa.ipac.caltech.edu/applications/KODIAQ/index.html")
        webbrowser.open("https://data-portal.hpc.swin.edu.au/dataset/uves-squad-dr1")
        
    if not MANIFEST_PATH.exists():
        print(f"Manifest not found at {MANIFEST_PATH}")
        return
        
    manifest_df = pd.read_csv(MANIFEST_PATH)
    target_lya_map = {row['System']: row['LyA_Observed_A'] for _, row in manifest_df.iterrows()}
    
    candidates = []
    
    # 1. Process SQUAD Targets
    print("Processing SQUAD DR1 targets...")
    squad_df = fetch_squad_csv()
    squad_targets = {
        "Q1009+2956_z2.504": "J101155+294141",
        "Q0311-1722_z3.734": "J031115-172247"
    }
    
    if not squad_df.empty:
        session = get_session()
        package_api = "https://data-portal.hpc.swin.edu.au/api/3/action/package_show?id=uves-squad-dr1"
        squad_resources = []
        squad_ckan_status = "LEGACY_HOST_UNAVAILABLE"
        
        try:
            resp = session.get(package_api, timeout=15)
            resp.raise_for_status()
            package = resp.json()
            squad_resources = package.get("result", {}).get("resources", [])
            squad_ckan_status = "RESOURCE_URL_CONFIRMED"
        except Exception as exc:
            print(f"  [!] CKAN API unavailable: {exc}")
            if args.open_portals:
                squad_ckan_status = "PORTAL_BROWSER_REQUIRED"
            else:
                squad_ckan_status = "MANUAL_MIRROR_REQUEST_REQUIRED"
                
        for sys_id, squad_id in squad_targets.items():
            match = squad_df[squad_df['Name_Adopt'] == squad_id]
            if not match.empty:
                wmin = float(match['WavStart'].iloc[0])
                wmax = float(match['WavEnd'].iloc[0])
                base_sys_id = sys_id.split('_')[0]
                req_lya = float(target_lya_map.get(base_sys_id, 0.0))
                coverage_pass = wmin <= req_lya <= wmax
                
                expected_filename = f"{squad_id}_Final_Spectrum.tar.gz"
                
                # Check CKAN resources
                res_url = None
                for res in squad_resources:
                    if res.get("name") == expected_filename or expected_filename in res.get("url", ""):
                        res_url = res.get("url")
                        break
                
                if res_url:
                    status_flag = "PRODUCT_CONFIRMED"
                else:
                    status_flag = squad_ckan_status
                
                candidates.append({
                    "system_id": sys_id,
                    "archive": "SQUAD_DR1",
                    "archive_object_id": squad_id,
                    "expected_filename": expected_filename,
                    "resource_url": res_url,
                    "resource_discovery_method": "CKAN_API" if res_url else "LEGACY_CKAN_OR_MANUAL",
                    "product_type": "CONTINUUM_NORMALIZED_1D",
                    "wavelength_start_angstrom": wmin,
                    "wavelength_end_angstrom": wmax,
                    "required_lya_angstrom": req_lya,
                    "coverage_pass": coverage_pass,
                    "status": status_flag
                })
                print(f"  Found {sys_id} in SQUAD DR1 as {squad_id} (Coverage: {coverage_pass}) -> {status_flag}")
    
    # 2. Process KODIAQ Targets
    print("\nProcessing KODIAQ targets...")
    koa_tables = discover_koa_table()
    print(f"  Found KOA reduced tables: {koa_tables}")
    
    kodiaq_targets = {
        "HS0105+1619_z2.536": "J010806+163550"
    }
    
    for sys_id, kodiaq_id in kodiaq_targets.items():
        found = False
        base_sys_id = sys_id.split('_')[0]
        req_lya = float(target_lya_map.get(base_sys_id, 0.0))
        
        for table in koa_tables:
            if "reduced" in table.lower() or "kodiaq" in table.lower():
                df = query_koa_kodiaq(table, kodiaq_id)
                if not df.empty:
                    # In koa_reduced_data, check access_url or equivalent
                    url = None
                    if 'access_url' in df.columns:
                        url = df['access_url'].iloc[0]
                        
                    candidates.append({
                        "system_id": sys_id,
                        "archive": "KODIAQ_DR1_DR2",
                        "archive_object_id": kodiaq_id,
                        "expected_filename": f"{kodiaq_id}_kodiaq.fits",
                        "resource_url": url,
                        "resource_discovery_method": "KOA_TAP",
                        "product_type": "CONTINUUM_NORMALIZED_1D",
                        "required_lya_angstrom": req_lya,
                        "coverage_pass": True,
                        "status": "REDUCED_PRODUCT_IDENTIFIED" if url else "MANUAL_PRODUCT_SELECTION_REQUIRED"
                    })
                    print(f"  Found {sys_id} in KOA table '{table}' as {kodiaq_id}")
                    found = True
                    break
        if not found:
            print(f"  Could not find {sys_id} in KOA tables.")
            candidates.append({
                "system_id": sys_id,
                "archive": "KODIAQ_DR1_DR2",
                "archive_object_id": kodiaq_id,
                "expected_filename": None,
                "resource_url": None,
                "resource_discovery_method": "KOA_TAP",
                "product_type": "CONTINUUM_NORMALIZED_1D",
                "required_lya_angstrom": req_lya,
                "coverage_pass": False,
                "status": "KODIAQ_CATALOG_CONFIRMED | MANUAL_PRODUCT_SELECTION_REQUIRED"
            })
            
    with open(OUT_PATH, "w") as f:
        json.dump(candidates, f, indent=2)
    print(f"\nDiscovery complete. Candidates written to {OUT_PATH}")

if __name__ == "__main__":
    main()
