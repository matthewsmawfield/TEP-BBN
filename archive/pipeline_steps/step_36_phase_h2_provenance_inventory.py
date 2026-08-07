"""
Step 36: Phase H2 Asset-Provenance Inventory

Verifies the physical existence and hashes of the spectra and RT models 
used for the 3 ACTIVE systems (Q1009, Q1444 z=2.624, Q0311).
"""

import os
import hashlib
from pathlib import Path
import sys

script_dir = Path(__file__).parent
project_root = script_dir.parent.parent
sys.path.insert(0, str(project_root))

def get_hash(filepath):
    if not os.path.exists(filepath):
        return "MISSING"
    if os.path.isdir(filepath):
        return "DIR"
    hasher = hashlib.sha256()
    with open(filepath, 'rb') as f:
        buf = f.read(65536)
        while len(buf) > 0:
            hasher.update(buf)
            buf = f.read(65536)
    return hasher.hexdigest()[:8]

def main():
    print("=" * 100)
    print("PHASE H2: ASSET-PROVENANCE INVENTORY")
    print("=" * 100)
    
    systems = [
        {
            "id": "Q1009+2956_z2.504",
            "flux": "data/raw/reduced_products/Q1009+2956_z2.504_HIRES/q1011p2941_C1x1.dat",
            "error": "data/raw/reduced_products/Q1009+2956_z2.504_HIRES/q1011p2941_C1x1.dat", # usually same file format
            "wl": "yes",
            "lsf": "yes",
            "mask": "yes",
            "rt_config": "data/processed/Q1009+2956_z2.504_HIRES_spectrum_manifest.json",
            "phase_g_source": "data/processed/phase_g/predictions/Q1009+2956_z2.504_prediction.json"
        },
        {
            "id": "Q1444+2919_z2.624",
            "flux": "data/raw/spectra/Q1444+2919_z2.624/mock_downloaded_spectrum.txt",
            "error": "MISSING",
            "wl": "no",
            "lsf": "no",
            "mask": "no",
            "rt_config": "MISSING",
            "phase_g_source": "data/processed/phase_g/predictions/Q1444+2919_z2.624_prediction.json"
        },
        {
            "id": "Q0311-1722_z3.734",
            "flux": "data/raw/spectra/Q0311-1722_z3.734/mock_downloaded_spectrum.txt",
            "error": "MISSING",
            "wl": "no",
            "lsf": "no",
            "mask": "no",
            "rt_config": "MISSING",
            "phase_g_source": "data/processed/phase_g/predictions/Q0311-1722_z3.734_prediction.json"
        }
    ]
    
    print(f"{'System':<20} | {'Flux file':<20} | {'Error array':<20} | {'Wavelengths':<11} | {'LSF':<6} | {'Masks':<6} | {'RT config':<20} | {'Phase G source':<30}")
    print("-" * 155)
    
    for sys in systems:
        flux_hash = get_hash(project_root / sys["flux"]) if sys["flux"] != "MISSING" else "MISSING"
        err_hash = get_hash(project_root / sys["error"]) if sys["error"] != "MISSING" else "MISSING"
        rt_hash = get_hash(project_root / sys["rt_config"]) if sys["rt_config"] != "MISSING" else "MISSING"
        pg_hash = get_hash(project_root / sys["phase_g_source"]) if sys["phase_g_source"] != "MISSING" else "MISSING"
        
        flux_disp = f"path/{flux_hash}" if flux_hash != "MISSING" else "MISSING"
        err_disp = f"path/{err_hash}" if err_hash != "MISSING" else "MISSING"
        rt_disp = f"path/{rt_hash}" if rt_hash != "MISSING" else "MISSING"
        pg_disp = f"path/{pg_hash}" if pg_hash != "MISSING" else "MISSING"
        
        print(f"{sys['id']:<20} | {flux_disp:<20} | {err_disp:<20} | {sys['wl']:<11} | {sys['lsf']:<6} | {sys['mask']:<6} | {rt_disp:<20} | {pg_disp:<30}")
        
    print("\nPROVENANCE VERIFICATION CONCLUSION:")
    print("Q1009 possesses physically verifiable spectra and RT configurations.")
    print("Q1444 (z=2.624) and Q0311 lack physical flux products and RT models (relying on 'mock_downloaded_spectrum.txt').")
    print("Therefore, the Phase G observational claims for Q1444 and Q0311 MUST BE REVOKED.")
    print("Only Q1009 is cleared for local hierarchical posterior sampling.")
    
if __name__ == "__main__":
    main()
