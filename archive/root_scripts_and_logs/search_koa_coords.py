import pyvo as vo
import pandas as pd
from astropy.coordinates import SkyCoord
from astropy import units as u

targets = [
    {"name": "Q1009+2956", "ra": 134.72467, "dec": 29.69489},
    {"name": "HS0105+1619", "ra": 255.40147, "dec": 16.59721}
]

print("Searching KOA TAP by coordinates...")
service = vo.dal.TAPService("https://koa.ipac.caltech.edu/TAP")

for t in targets:
    print(f"Target: {t['name']}")
    query = f"""
    SELECT TOP 100 koaid, progid, pi, targname, filetype
    FROM koa_hires 
    WHERE CONTAINS(POINT('ICRS', ra, dec), CIRCLE('ICRS', {t['ra']}, {t['dec']}, 0.1)) = 1
    """
    try:
        results = service.search(query)
        print(f"  Found {len(results)} HIRES records in KOA")
        if len(results) > 0:
            df = results.to_table().to_pandas()
            print(df.head(10))
    except Exception as e:
        print(f"  KOA Error: {e}")
    break # Just testing Q1009 first

print("\nSearching ESO TAP by coordinates...")
eso_service = vo.dal.TAPService("https://archive.eso.org/tap_obs")

for t in targets:
    print(f"Target: {t['name']}")
    query = f"""
    SELECT dp_id, target_name, instrument_name, obstech, access_url
    FROM ivoa.ObsCore
    WHERE CONTAINS(POINT('ICRS', s_ra, s_dec), CIRCLE('ICRS', {t['ra']}, {t['dec']}, 0.1)) = 1
    AND instrument_name LIKE '%UVES%'
    """
    try:
        results = eso_service.search(query)
        print(f"  Found {len(results)} UVES records in ESO")
        if len(results) > 0:
            df = results.to_table().to_pandas()
            print(df.head(3))
    except Exception as e:
        print(f"  ESO Error: {e}")
