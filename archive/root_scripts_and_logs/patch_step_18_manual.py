with open("scripts/steps/step_18_coordinate_archive_sweep.py", "r") as f:
    code = f.read()

target = """def resolve_coordinates(name):
    try:
        res = Simbad.query_object(name)
        if res is not None and len(res) > 0:
            sc = SkyCoord(res['ra'][0], res['dec'][0], unit=(u.hourangle, u.deg))
            return sc.ra.deg, sc.dec.deg, "SIMBAD"
    except Exception as e:
        pass
    
    try:
        res = Ned.query_object(name)
        if res is not None and len(res) > 0:
            ra = res['RA'][0]
            dec = res['DEC'][0]
            return ra, dec, "NED"
    except Exception as e:
        pass
    
    return None, None, None"""

replacement = """def resolve_coordinates(name):
    manual_coords = {
        'Q1351+3221': (207.75, 32.35),
        'Q1444+2919': (221.0, 29.317),
        'SDSSJ1358+6522': (209.5, 65.367),
        'SDSS J1358+6522': (209.5, 65.367),
        'Q0311-1722': (47.75, -17.367)
    }
    
    if name in manual_coords:
        return manual_coords[name][0], manual_coords[name][1], "MANUAL"
        
    try:
        res = Simbad.query_object(name)
        if res is not None and len(res) > 0:
            sc = SkyCoord(res['ra'][0], res['dec'][0], unit=(u.hourangle, u.deg))
            return sc.ra.deg, sc.dec.deg, "SIMBAD"
    except Exception as e:
        pass
    
    try:
        res = Ned.query_object(name)
        if res is not None and len(res) > 0:
            ra = res['RA'][0]
            dec = res['DEC'][0]
            return ra, dec, "NED"
    except Exception as e:
        pass
    
    return None, None, None"""

code = code.replace(target, replacement)
with open("scripts/steps/step_18_coordinate_archive_sweep.py", "w") as f:
    f.write(code)
