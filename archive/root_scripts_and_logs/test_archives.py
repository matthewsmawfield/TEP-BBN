import pyvo as vo
import requests
from astropy.coordinates import SkyCoord
import astropy.units as u

targets = [
    ("Q1009+2956", 134.72467, 29.69489, "HIRES"),
    ("Q1243+3047", 353.175, 30.52139, "HIRES"),
    ("Q1351+3221", 207.75, 32.35, "HIRES"),
    ("Q1444+2919", 221.0, 29.317, "HIRES"),
    ("HS0105+1619", 255.40147, 16.59721, "UVES"),
    ("J1358+6522", 209.5, 65.367, "UVES"),
    ("J1558-0031", 353.13526, -0.52223, "UVES"),
    ("Q0311-1722", 47.75, -17.367, "HIRES")
]

def search_eso(ra, dec):
    try:
        service = vo.dal.TAPService("http://archive.eso.org/tap_obs")
        query = f"""
        SELECT top 5 target_name, dp_id, s_ra, s_dec, instrument_name
        FROM ivoa.ObsCore 
        WHERE CONTAINS(POINT('ICRS', s_ra, s_dec), CIRCLE('ICRS', {ra}, {dec}, 0.05)) = 1
        AND instrument_name = 'UVES'
        """
        res = service.search(query)
        if len(res) > 0:
            return True, len(res), res['dp_id'][0]
    except Exception as e:
        pass
    return False, 0, None

def search_koa(ra, dec):
    try:
        service = vo.dal.TAPService("https://koa.ipac.caltech.edu/TAP")
        query = f"""
        SELECT top 5 target_name, koaid, instrument
        FROM koa_v1
        WHERE CONTAINS(POINT('ICRS', ra, dec), CIRCLE('ICRS', {ra}, {dec}, 0.05)) = 1
        AND instrument = 'HIRES'
        """
        res = service.search(query)
        if len(res) > 0:
            return True, len(res), res['koaid'][0]
    except Exception as e:
        pass
    return False, 0, None

for name, ra, dec, inst in targets:
    if "UVES" in inst:
        found, count, sample_id = search_eso(ra, dec)
        print(f"ESO {name}: {found} ({count} records) - Sample: {sample_id}")
    else:
        found, count, sample_id = search_koa(ra, dec)
        print(f"KOA {name}: {found} ({count} records) - Sample: {sample_id}")

