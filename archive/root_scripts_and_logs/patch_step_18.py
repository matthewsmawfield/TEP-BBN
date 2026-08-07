with open("scripts/steps/step_18_coordinate_archive_sweep.py", "r") as f:
    code = f.read()

target = """def query_eso_tap(ra, dec, z_abs):
    hits = []
    service = vo.dal.TAPService("http://archive.eso.org/tap_obs")
    query = f\"\"\"
    SELECT top 100 target_name, dp_id, s_ra, s_dec, instrument_name, em_min, em_max, access_url
    FROM ivoa.ObsCore 
    WHERE CONTAINS(POINT('ICRS', s_ra, s_dec), CIRCLE('ICRS', {ra}, {dec}, {SEARCH_RADIUS_DEG})) = 1
    AND dataproduct_type = 'spectrum'
    \"\"\"
    try:
        res = service.search(query)
        for row in res:
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
                        "target_ra_deg": ra,
                        "target_dec_deg": dec,
                        "archive_ra_deg": s_ra,
                        "archive_dec_deg": s_dec,
                        "separation_arcsec": sep,
                        "access_url": str(row['access_url'])
                    })
    except Exception as e:
        print(f"  [!] ESO TAP error: {e}")
    
    return hits"""

replacement = """import requests
def query_eso_tap(ra, dec, z_abs):
    hits = []
    query = f\"\"\"
    SELECT top 100 target_name, dp_id, s_ra, s_dec, instrument_name, em_min, em_max, access_url
    FROM ivoa.ObsCore 
    WHERE CONTAINS(POINT('ICRS', s_ra, s_dec), CIRCLE('ICRS', {ra}, {dec}, {SEARCH_RADIUS_DEG})) = 1
    AND dataproduct_type = 'spectrum'
    \"\"\"
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
                                "target_ra_deg": ra,
                                "target_dec_deg": dec,
                                "archive_ra_deg": s_ra,
                                "archive_dec_deg": s_dec,
                                "separation_arcsec": sep,
                                "access_url": str(row['access_url'])
                            })
    except Exception as e:
        print(f"  [!] ESO TAP error: {e}")
    
    return hits"""

code = code.replace(target, replacement)
with open("scripts/steps/step_18_coordinate_archive_sweep.py", "w") as f:
    f.write(code)
