from astroquery.simbad import Simbad
from astroquery.ned import Ned
import astropy.units as u

names = ["Q1009+2956", "Q1243+3047", "HS0105+1619", "SDSS J1358+6522"]
for name in names:
    try:
        res = Simbad.query_object(name)
        if res:
            ra, dec = res['RA'][0], res['DEC'][0]
            print(f"Simbad {name}: RA {ra}, DEC {dec}")
        else:
            res = Ned.query_object(name)
            if res:
                ra, dec = res['RA'][0], res['DEC'][0]
                print(f"NED {name}: RA {ra}, DEC {dec}")
            else:
                print(f"Not found: {name}")
    except Exception as e:
        print(f"Error {name}: {e}")
