from astroquery.simbad import Simbad
res = Simbad.query_object("Q1009+2956")
if res:
    print(res.colnames)
