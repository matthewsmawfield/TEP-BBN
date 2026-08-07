import sys
from astroquery.koa import Koa
from astropy.coordinates import SkyCoord
import astropy.units as u

def test_koa():
    print("Testing KOA...")
    ra = 134.72467
    dec = 29.69489
    coord = SkyCoord(ra=ra, dec=dec, unit=(u.deg, u.deg))
    try:
        # We want HIRES reduced data if available
        # But let's just query everything first
        table = Koa.query_region(coord, radius=5*u.arcsec)
        print("KOA Results:", len(table))
        if len(table) > 0:
            print(table.colnames)
            # check for level 1 or 2 products
            # or just print a few rows
            for row in table[:3]:
                print(row['progid'], row['koaid'], row['level'])
    except Exception as e:
        print("KOA Error:", e)

if __name__ == "__main__":
    test_koa()
