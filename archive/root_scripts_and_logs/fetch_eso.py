import os
import numpy as np
from astropy.io import fits
from astroquery.eso import Eso
eso = Eso()
table = eso.query_surveys(target='Q0913+072', radius=10)
datasets = table['ARCFILE'].data[:10]

for ds in datasets:
    print(f"Downloading {ds}...")
    try:
        eso.retrieve_data([ds])
        fpath = f"/Users/matthewsmawfield/.astropy/cache/astroquery/Eso/{ds}.fits"
        with fits.open(fpath) as hdul:
            wave = hdul[1].data['WAVE'][0]
            print(f"  {ds} wave range: {np.min(wave):.1f} - {np.max(wave):.1f}")
            if np.min(wave) < 4400 and np.max(wave) > 4400:
                print(f"  *** FOUND LYMAN ALPHA COVERAGE in {ds} ***")
    except Exception as e:
        print(e)
