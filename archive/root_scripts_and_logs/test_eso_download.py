import json
import requests
from astropy.io import fits

with open('data/processed/public_dh_target_candidates.json', 'r') as f:
    cands = json.load(f)

for c in cands:
    if c['status'] == 'PUBLIC_SPECTRUM_FOUND':
        url = c.get('access_url')
        print(f"Downloading {url} ...")
        r = requests.get(url)
        with open('temp.fits', 'wb') as f_out:
            f_out.write(r.content)
            
        with fits.open('temp.fits') as hdul:
            hdul.info()
            for hdu in hdul:
                if isinstance(hdu, fits.BinTableHDU):
                    print("Columns:", hdu.columns.names)
                    print("Wavelength unit:", hdu.header.get('TUNIT1'))
                    break
