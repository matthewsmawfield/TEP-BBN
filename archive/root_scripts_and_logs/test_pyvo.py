import pyvo as vo
from astropy.coordinates import SkyCoord
import astropy.units as u

def test_eso():
    service = vo.dal.TAPService("http://archive.eso.org/tap_obs")
    query = """
    SELECT top 10 target_name, dp_id, s_ra, s_dec, instrument_name, em_min, em_max 
    FROM ivoa.ObsCore 
    WHERE CONTAINS(POINT('ICRS', s_ra, s_dec), CIRCLE('ICRS', 152.98, 29.69, 0.01)) = 1
    AND dataproduct_type = 'spectrum'
    """
    try:
        res = service.search(query)
        print("ESO:", len(res))
    except Exception as e:
        print("ESO Error:", e)

def test_koa():
    # KOA doesn't have an obvious public TAP that works exactly like ESO, but we can check if it exists:
    service = vo.dal.TAPService("https://koa.ipac.caltech.edu/TAP")
    query = """
    SELECT top 10 * 
    FROM koa_v1
    WHERE CONTAINS(POINT('ICRS', ra, dec), CIRCLE('ICRS', 152.98, 29.69, 0.01)) = 1
    """
    try:
        res = service.search(query)
        print("KOA:", len(res))
    except Exception as e:
        print("KOA Error:", e)

test_eso()
test_koa()
