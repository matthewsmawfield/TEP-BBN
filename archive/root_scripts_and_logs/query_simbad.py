from astroquery.simbad import Simbad
import json

targets = [
    "HS 0105+1619",
    "PKS 1937-1009",
    "SDSS J1358+6522",
    "SDSS J155810.16-003120.0"
]

for t in targets:
    try:
        res = Simbad.query_object(t)
        if res is not None:
            ra = res['RA'][0]
            dec = res['DEC'][0]
            print(f"{t}: RA={ra}, DEC={dec}")
        else:
            print(f"{t}: Not found")
    except Exception as e:
        print(f"Error querying {t}: {e}")
