import json
import sys
from pathlib import Path
import numpy as np
import pyvo as vo
import re

script_dir = Path(__file__).parent
project_root = script_dir.parent.parent
sys.path.insert(0, str(project_root))

from scripts.steps.step_15_catalog_scale import load_system_spectrum, check_lyman_window_coverage

def query_eso_tap_for_uves(aliases, z_abs):
    try:
        eso_tap = vo.dal.TAPService('http://archive.eso.org/tap_obs')
        
        # Build alias matching
        conditions = []
        for alias in aliases:
            # strip spaces or common prefixes for looser matching
            clean = re.sub(r'[^a-zA-Z0-9\+\-]', '%', alias)
            conditions.append(f"target_name LIKE '%{clean}%'")
            
        alias_cond = " OR ".join(conditions)
        
        query = f"""
        SELECT target_name, s_ra, s_dec, dataproduct_type, instrument_name, em_min, em_max, access_url
        FROM ivoa.ObsCore
        WHERE instrument_name LIKE '%UVES%' 
          AND dataproduct_type='spectrum'
          AND ({alias_cond})
        """
        
        res = eso_tap.search(query).to_table()
        
        if len(res) == 0:
            return {"status": "PUBLIC_SPECTRUM_NOT_FOUND"}
            
        # Check Lyman coverage
        lya_rest = 1215.67
        lya_obs = lya_rest * (1 + z_abs)
        
        # We need [-300, 100] km/s coverage
        # velocity = c * (lambda - lambda_obs) / lambda_obs
        c_kms = 299792.458
        l_min = lya_obs * (1 - 300.0 / c_kms) * 1e-10 # Angstroms to meters
        l_max = lya_obs * (1 + 100.0 / c_kms) * 1e-10
        
        for row in res:
            em_min = row['em_min']
            em_max = row['em_max']
            if em_min <= l_min and em_max >= l_max:
                return {
                    "status": "PUBLIC_SPECTRUM_FOUND",
                    "access_url": row['access_url'].decode('utf-8') if isinstance(row['access_url'], bytes) else str(row['access_url']),
                    "archive_target_name": row['target_name'].decode('utf-8') if isinstance(row['target_name'], bytes) else str(row['target_name']),
                    "em_min": float(em_min),
                    "em_max": float(em_max),
                    "instrument_name": row['instrument_name'].decode('utf-8') if isinstance(row['instrument_name'], bytes) else str(row['instrument_name'])
                }
                
        return {"status": "NO_LYMAN_COVERAGE"}
        
    except Exception as e:
        print(f"ESO TAP Error: {e}")
        return {"status": "PUBLIC_SPECTRUM_NOT_FOUND"}


def main():
    print("Step 16: Public D/H Target Discovery")
    print("=" * 60)
    
    seed_lists = [
        project_root / "data/processed/dh_literature_registry.json",
        project_root / "data/processed/missing_spectra_manifest.json",
        project_root / "data/processed/extended_dh_target_seed_list.json"
    ]
    
    systems_to_evaluate = {}
    
    for seed_path in seed_lists:
        if seed_path.exists():
            print(f"Loading seed list: {seed_path.name}")
            with open(seed_path, 'r') as f:
                data = json.load(f)
                if isinstance(data, dict) and 'systems' in data:
                    sys_list = data['systems']
                elif isinstance(data, list):
                    sys_list = data
                else:
                    sys_list = []
                    
                for s in sys_list:
                    # Resolve IDs consistently
                    qso = s.get('qso_name', 'Unknown')
                    z_abs = s.get('absorber_redshift', s.get('redshift', 0.0))
                    key = f"{qso}_z{z_abs}"
                    
                    if key not in systems_to_evaluate:
                        systems_to_evaluate[key] = s
                    else:
                        # Merge aliases if necessary
                        existing_aliases = set(systems_to_evaluate[key].get('aliases', []))
                        new_aliases = set(s.get('aliases', []))
                        existing_aliases.update(new_aliases)
                        systems_to_evaluate[key]['aliases'] = list(existing_aliases)

    if not systems_to_evaluate:
        print("No seed systems found to evaluate.")
        return
        
    print(f"Total unique systems seeded: {len(systems_to_evaluate)}\n")
    
    candidates = []
    
    for key, sys_data in systems_to_evaluate.items():
        qso_name = sys_data.get('qso_name')
        z_abs = float(sys_data.get('absorber_redshift', sys_data.get('redshift', 0.0)))
        system_id = sys_data.get('system_id', f"{qso_name}_z{z_abs}")
        instrument = sys_data.get('instrument', 'Unknown')
        
        aliases = [qso_name] + sys_data.get('aliases', [])
        
        candidate = {
            "system_id": system_id,
            "qso_name": qso_name,
            "aliases": aliases,
            "absorber_redshift": z_abs,
            "instrument": instrument,
            "paper": sys_data.get('paper', ''),
            "status": "UNKNOWN"
        }
        
        print(f"Evaluating {system_id}...")
        
        # 1. Check local spectrum
        spec_path, fetch_status = load_system_spectrum(system_id, qso_name, z_abs, instrument)
        
        if fetch_status["status"] == "READY":
            try:
                data = np.loadtxt(spec_path)
                v_grid = data[:, 0]
                if check_lyman_window_coverage(v_grid):
                    fv_paths = [
                        project_root / f"data/processed/measured_feature_vector_{system_id}.json",
                        project_root / f"data/processed/measured_feature_vector_{qso_name}.json"
                    ]
                    if any(p.exists() for p in fv_paths):
                        candidate["status"] = "READY_FOR_STEP15"
                    else:
                        candidate["status"] = "NEEDS_FEATURE_VECTOR"
                else:
                    candidate["status"] = "NO_LYMAN_COVERAGE"
            except Exception:
                candidate["status"] = "LOAD_FAILED"
        else:
            # If not local, search public archives based on instrument
            if "UVES" in instrument.upper():
                print(f"  [*] Querying ESO Phase 3 TAP for aliases: {aliases}")
                tap_res = query_eso_tap_for_uves(aliases, z_abs)
                candidate["status"] = tap_res["status"]
                if candidate["status"] == "PUBLIC_SPECTRUM_FOUND":
                    candidate["access_url"] = tap_res.get("access_url")
                    candidate["archive_target_name"] = tap_res.get("archive_target_name")
                    candidate["em_min"] = tap_res.get("em_min")
                    candidate["em_max"] = tap_res.get("em_max")
                    candidate["archive_instrument"] = tap_res.get("instrument_name")
            elif "HIRES" in instrument.upper():
                print("  [*] Flagging KOA/HIRES for manual authentication")
                candidate["status"] = "AUTH_REQUIRED"
            else:
                candidate["status"] = "PUBLIC_SPECTRUM_NOT_FOUND"
                
        print(f"  -> {candidate['status']}")
        candidates.append(candidate)
        
    out_path = project_root / "data/processed/public_dh_target_candidates.json"
    with open(out_path, 'w') as f:
        json.dump(candidates, f, indent=2)
        
    print(f"\nSaved target candidates to {out_path.name}")
    
    summary = {}
    for c in candidates:
        summary[c['status']] = summary.get(c['status'], 0) + 1
        
    print("\nSummary:")
    for status, count in summary.items():
        print(f"  {status}: {count}")

if __name__ == '__main__':
    main()
