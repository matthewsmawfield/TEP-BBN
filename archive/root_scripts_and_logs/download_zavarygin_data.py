import os
import requests
from pathlib import Path
import gzip

project_root = Path(__file__).parent
raw_dir = project_root / "data/raw/reduced_products/Q1009+2956_z2.504_HIRES"
raw_dir.mkdir(parents=True, exist_ok=True)

files_to_download = [
    "q1011p2941_C1x1.dat.gz",
    "q1011p2941_C1x2.dat.gz",
    "q1011p2941_C5x1.dat.gz",
    "q1011p2941_C5x2.dat.gz"
]

base_url = "https://raw.githubusercontent.com/ezavarygin/q1009p2956/master/data"

for filename in files_to_download:
    url = f"{base_url}/{filename}"
    out_path_gz = raw_dir / filename
    
    print(f"Downloading {filename}...")
    res = requests.get(url)
    if res.status_code == 200:
        with open(out_path_gz, "wb") as f:
            f.write(res.content)
            
        print(f"  Saved {filename}.")
        
        # Extract gz
        out_path = out_path_gz.with_suffix('')
        with gzip.open(out_path_gz, 'rb') as f_in:
            with open(out_path, 'wb') as f_out:
                f_out.write(f_in.read())
        print(f"  Extracted to {out_path.name}")
    else:
        print(f"  [!] Failed to download {filename} - Status {res.status_code}")
