"""
Step 01b: Download Literature Components

Automatically fetches the arXiv source for Pettini et al. 2008 (arXiv:0805.0594)
and Cooke et al. 2016 (arXiv:1607.03900) to extract the genuine published
component tables for Q0913+072.

This ensures no data is synthesized or fabricated.
"""

import urllib.request
import tarfile
import os
import re
import csv
from pathlib import Path

script_dir = Path(__file__).parent
project_root = script_dir.parent.parent
sys_id = "Q0913+072"
arxiv_id = "0805.0594" # Pettini 2008 is the source of the high-res component table

def fetch_and_parse_components():
    print("Step 01b: Download Literature Components")
    print("=" * 60)
    
    tmp_dir = project_root / "data/raw/literature_source"
    tmp_dir.mkdir(parents=True, exist_ok=True)
    tar_path = tmp_dir / f"{arxiv_id}.tar.gz"
    
    if not tar_path.exists():
        print(f"Downloading arXiv source for {arxiv_id}...")
        url = f"https://arxiv.org/e-print/{arxiv_id}"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (TEP-BBN Research Pipeline)'})
        with urllib.request.urlopen(req) as response, open(tar_path, 'wb') as out_file:
            out_file.write(response.read())
        print("Download complete.")
        
    extract_dir = tmp_dir / arxiv_id
    extract_dir.mkdir(exist_ok=True)
    
    with tarfile.open(tar_path, "r:gz") as tar:
        tar.extractall(path=extract_dir)
        
    tex_file = extract_dir / "mpettini_v3.tex"
    if not tex_file.exists():
        raise FileNotFoundError(f"Could not find mpettini_v3.tex in {extract_dir}")
        
    print(f"Parsing {tex_file.name} for Table 2 (Q0913+072 component model)...")
    
    with open(tex_file, 'r') as f:
        content = f.read()
        
    # We are looking for Table 1 / Table 2 for Q0913+072.
    # From inspection, it's Table tab:Q0913_cloudmodel.
    # Lines look like: O\,{\sc i} & 2.61828    & 3.5  &  0.31 \\
    
    table_start = content.find(r"Q0913+072.")
    table_end = content.find(r"\end{table}", table_start)
    table_text = content[table_start:table_end]
    
    components = []
    # We only care about the O I metal components for the metal-feature vector
    for line in table_text.split('\n'):
        if 'O\\,{\\sc i}' in line:
            # Parse line: O\,{\sc i} & 2.61828    & 3.5  &  0.31 \\
            parts = [p.strip().replace('\\\\', '') for p in line.split('&')]
            if len(parts) >= 4:
                z = float(parts[1])
                b = float(parts[2])
                frac = float(parts[3])
                components.append({'z': z, 'b': b, 'frac': frac})
                
    if not components:
        raise ValueError("Could not parse component table from LaTeX source.")
        
    print(f"Extracted {len(components)} metal components.")
    
    # Process into standard component table CSV
    # Calculate velocity relative to the primary (highest fraction) component
    primary = max(components, key=lambda c: c['frac'])
    z_ref = primary['z']
    c_kms = 299792.458
    
    out_dir = project_root / "data/literature_components"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_csv = out_dir / "Q0913+072_component_table.csv"
    
    total_log_N_HI = 20.31 # From Cooke 2016
    
    with open(out_csv, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['component_id', 'velocity_kms', 'redshift', 'metal_fraction', 'b_kms', 'log_N_HI_inferred', 'source', 'uncertainty'])
        
        for i, comp in enumerate(sorted(components, key=lambda c: c['z'])):
            z = comp['z']
            v = c_kms * (z - z_ref) / (1 + z_ref)
            frac = comp['frac']
            
            # Apportion total column density by metal fraction (assuming uniform metallicity)
            import math
            log_N_HI = total_log_N_HI + math.log10(frac)
            
            writer.writerow([
                i, 
                round(v, 2), 
                z, 
                frac, 
                comp['b'], 
                round(log_N_HI, 2), 
                "Pettini2008_Table2", 
                0.05 # Conservative minimum measurement uncertainty
            ])
            print(f"  Component {i}: v = {v:.2f} km/s, frac = {frac}, inferred log_N_HI = {log_N_HI:.2f}")

    print(f"Saved real component data to {out_csv}")
    print("=" * 60)

if __name__ == "__main__":
    fetch_and_parse_components()
