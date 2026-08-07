import json
import sys
import warnings
from pathlib import Path
import pyvo as vo
from astropy.coordinates import SkyCoord
import astropy.units as u
from astroquery.simbad import Simbad
from astroquery.ipac.ned import Ned
import numpy as np

warnings.filterwarnings('ignore')

script_dir = Path(__file__).parent
project_root = script_dir.parent.parent

c_kms = 299792.458
SEARCH_RADIUS_ARCSEC = 30.0
SEARCH_RADIUS_DEG = SEARCH_RADIUS_ARCSEC / 3600.0
MATCH_RADIUS_ARCSEC = 10.0

def resolve_coordinates(system_id, aliases, registry_coordinates):
    # 1. Full-precision verified registry coordinates
    reg_coord = registry_coordinates.get(system_id)
    if reg_coord and reg_coord.get('verified'):
        return reg_coord['ra_deg'], reg_coord['dec_deg'], "REGISTRY_VERIFIED"
        
    for alias in aliases:
        # 2. SIMBAD result
        try:
            res = Simbad.query_object(alias)
            if res is not None and len(res) > 0:
                sc = SkyCoord(res['ra'][0], res['dec'][0], unit=(u.hourangle, u.deg))
                return sc.ra.deg, sc.dec.deg, "SIMBAD"
        except Exception:
            pass
        
        # 3. NED result
        try:
            res = Ned.query_object(alias)
            if res is not None and len(res) > 0:
                ra = res['RA'][0]
                dec = res['DEC'][0]
                return ra, dec, "NED"
        except Exception:
            pass
            
    # 4. Approximate coordinate decoded from canonical J-name
    if reg_coord:
        return reg_coord['ra_deg'], reg_coord['dec_deg'], "CANONICAL_J_NAME_APPROXIMATE"
        
    # 5. Unresolved
    return None, None, "UNRESOLVED"

def check_wavelength_coverage(em_min_m, em_max_m, z_abs):
    lya_obs_angstrom = 1215.67 * (1 + z_abs)
    lam_min_angstrom = lya_obs_angstrom * (1 - 300.0 / c_kms)
    lam_max_angstrom = lya_obs_angstrom * (1 + 100.0 / c_kms)

    lam_min_m = lam_min_angstrom * 1e-10
    lam_max_m = lam_max_angstrom * 1e-10
    
    if em_min_m <= lam_min_m and em_max_m >= lam_max_m:
        return True
    return False

import requests
def query_eso_tap(ra, dec, z_abs):
    hits = []
    query = f"""
    SELECT top 100 target_name, dp_id, s_ra, s_dec, instrument_name, em_min, em_max, access_url
    FROM ivoa.ObsCore 
    WHERE CONTAINS(POINT('ICRS', s_ra, s_dec), CIRCLE('ICRS', {ra}, {dec}, {SEARCH_RADIUS_DEG})) = 1
    AND dataproduct_type = 'spectrum'
    """
    try:
        resp = requests.post("http://archive.eso.org/tap_obs/sync", data={
            "REQUEST": "doQuery",
            "LANG": "ADQL",
            "FORMAT": "json",
            "QUERY": query
        }, timeout=10)
        
        if resp.status_code == 200:
            data = resp.json()
            if 'data' in data:
                cols = [c['name'] for c in data['metadata']]
                for row_data in data['data']:
                    row = dict(zip(cols, row_data))
                    s_ra = float(row['s_ra'])
                    s_dec = float(row['s_dec'])
                    sep = SkyCoord(ra, dec, unit='deg').separation(SkyCoord(s_ra, s_dec, unit='deg')).arcsec
                    if sep <= SEARCH_RADIUS_ARCSEC:
                        has_cov = check_wavelength_coverage(float(row['em_min']), float(row['em_max']), z_abs)
                        if has_cov:
                            hits.append({
                                "archive": "ESO",
                                "archive_target_name": str(row['target_name']),
                                "instrument": str(row['instrument_name']).strip().upper(),
                                "input_ra_deg": ra,
                                "target_dec_deg": dec,
                                "archive_ra_deg": s_ra,
                                "archive_dec_deg": s_dec,
                                "separation_arcsec": sep,
                                "coordinate_match": sep <= MATCH_RADIUS_ARCSEC,
                                "access_url": str(row['access_url'])
                            })
    except Exception as e:
        print(f"  [!] ESO TAP error: {e}")
    
    return hits

def query_koa_tap(ra, dec, z_abs):
    hits = []
    try:
        service = vo.dal.TAPService("https://koa.ipac.caltech.edu/TAP")
        query = f"""
        SELECT top 100 target_name, s_ra, s_dec, instrument_name, em_min, em_max, access_url
        FROM ivoa.ObsCore
        WHERE CONTAINS(POINT('ICRS', s_ra, s_dec), CIRCLE('ICRS', {ra}, {dec}, {SEARCH_RADIUS_DEG})) = 1
        """
        res = service.search(query)
        for row in res:
            s_ra = float(row['s_ra'])
            s_dec = float(row['s_dec'])
            sep = SkyCoord(ra, dec, unit='deg').separation(SkyCoord(s_ra, s_dec, unit='deg')).arcsec
            if sep <= SEARCH_RADIUS_ARCSEC:
                has_cov = check_wavelength_coverage(float(row['em_min']), float(row['em_max']), z_abs)
                if has_cov:
                    hits.append({
                        "archive": "KOA",
                        "archive_target_name": str(row.get('target_name', '')),
                        "instrument": str(row.get('instrument_name', '')).strip().upper(),
                        "input_ra_deg": ra,
                        "target_dec_deg": dec,
                        "archive_ra_deg": s_ra,
                        "archive_dec_deg": s_dec,
                        "separation_arcsec": sep,
                        "coordinate_match": sep <= MATCH_RADIUS_ARCSEC,
                        "access_url": str(row.get('access_url', ''))
                    })
    except Exception as e:
        # Silently fail if KOA schema doesn't exist or requires auth
        pass
    
    return hits

def main():
    print("Step 18: Coordinate Archive Sweep")
    print("=" * 60)
    
    audit_path = project_root / "data/processed/catalog_integrity_audit.json"
    if not audit_path.exists():
        print("catalog_integrity_audit.json not found. Run step 17 first.")
        sys.exit(1)
        
    with open(audit_path, 'r') as f:
        audit = json.load(f)
        
    registry_path = project_root / "data/processed/dh_literature_registry.json"
    with open(registry_path, 'r') as f:
        registry = json.load(f)
    registry_lookup = {s['system_id']: s for s in registry.get('systems', registry)}
    
    coord_registry_path = project_root / "data/processed/target_coordinate_registry.json"
    target_coord_registry = {}
    if coord_registry_path.exists():
        with open(coord_registry_path, 'r') as f:
            target_coord_registry = json.load(f)
    
    sweep_results = []
    
    for item in audit:
        sys_id = item['system_id']
        status = item['status']
        z_abs = item['registry_redshift']
        qso_name = item['qso_name']
        
        if status not in ["DATA_UNAVAILABLE", "AUTH_REQUIRED", "PUBLIC_SPECTRUM_NOT_FOUND", "INSUFFICIENT_SECONDARY_STRUCTURE"]:
            continue
            
        print(f"\nProcessing {sys_id} ({status})...")
        sys_obj = registry_lookup.get(sys_id, {})
        aliases = [qso_name] + sys_obj.get('aliases', [])
        
        ra, dec, resolver = resolve_coordinates(sys_id, aliases, target_coord_registry)
        if ra is not None:
            print(f"  [✓] Resolved via {resolver}: RA={ra:.5f}, Dec={dec:.5f}")
                
        if ra is None:
            print("  [x] Could not resolve coordinates via SIMBAD or NED.")
            sweep_results.append({
                "system_id": sys_id,
                "status": "COORD_NOT_RESOLVED",
                "hits": []
            })
            continue
            
        hits = []
        eso_hits = query_eso_tap(ra, dec, z_abs)
        if eso_hits:
            hits.extend(eso_hits)
            
        koa_hits = query_koa_tap(ra, dec, z_abs)
        if koa_hits:
            hits.extend(koa_hits)
            
        # Rank hits by separation
        hits.sort(key=lambda x: x['separation_arcsec'])
        
        final_status = "NO_HIGH_RES_SPECTRUM_FOUND"
        best_hit = None
        
        for hit in hits:
            instr = hit['instrument']
            if 'UVES' in instr or 'HIRES' in instr:
                if hit['archive'] == 'ESO':
                    final_status = "ESO_PUBLIC_SPECTRUM_FOUND"
                elif hit['archive'] == 'KOA':
                    final_status = "KOA_PUBLIC_HIT_FOUND"
                
                # Check for ready download
                if hit['access_url'] and "auth" not in hit['access_url'].lower():
                    final_status = "READY_FOR_DOWNLOAD"
                best_hit = hit
                break
                
        if final_status == "NO_HIGH_RES_SPECTRUM_FOUND" and len(hits) > 0:
            # Check for XSHOOTER
            for hit in hits:
                if 'XSHOOTER' in hit['instrument']:
                    final_status = "LOWER_RESOLUTION_CANDIDATE"
                    best_hit = hit
                    break
                    
        # If no valid hits but KOA error or AUTH_REQUIRED
        if len(hits) == 0:
            final_status = "AUTH_REQUIRED"
            
        print(f"  [→] Status: {final_status}")
        if best_hit:
            print(f"      Closest match: {best_hit['instrument']} from {best_hit['archive']} ({best_hit['separation_arcsec']:.2f} arcsec)")
            
        sweep_results.append({
            "system_id": sys_id,
            "qso_name": qso_name,
            "registry_redshift": z_abs,
            "coordinate_source": resolver,
            "ra_deg": ra,
            "dec_deg": dec,
            "status": final_status,
            "hits": hits
        })

    out_path = project_root / "data/processed/coordinate_archive_sweep_results.json"
    with open(out_path, 'w') as f:
        json.dump(sweep_results, f, indent=2)
    print(f"\nSaved {len(sweep_results)} results to {out_path.name}")

if __name__ == '__main__':
    main()
