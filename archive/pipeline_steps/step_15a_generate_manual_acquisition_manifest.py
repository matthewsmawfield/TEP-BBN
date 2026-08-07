import json
import pandas as pd
from pathlib import Path

script_dir = Path(__file__).parent
project_root = script_dir.parent.parent

with open(project_root / 'data/processed/missing_spectra_manifest.json', 'r') as f:
    missing_manifest = json.load(f)
    
pack_data = []


with open(project_root / 'data/processed/coordinate_archive_sweep_results.json', 'r') as f:
    sweep_results = json.load(f)
sweep_lookup = {s['system_id']: s for s in sweep_results}

with open(project_root / 'data/processed/dh_literature_registry.json', 'r') as f:
    registry = json.load(f)
reg_lookup = {s['system_id']: s for s in registry.get('systems', registry)}

coord_registry_path = project_root / 'data/processed/target_coordinate_registry.json'
coord_registry = {}
if coord_registry_path.exists():
    with open(coord_registry_path, 'r') as f:
        coord_registry = json.load(f)

for sys_data in missing_manifest:
    sys_id = sys_data['system_id']
    name = sys_data['qso_name']
    z_abs = sys_data['absorber_redshift']
    instrument = sys_data['instrument']
    
    sweep_info = sweep_lookup.get(sys_id, {})
    reg_info = reg_lookup.get(sys_id, {})
    coord_info = coord_registry.get(sys_id, {})
    
    ra_deg = coord_info.get('ra_deg', sweep_info.get('ra_deg', ''))
    dec_deg = coord_info.get('dec_deg', sweep_info.get('dec_deg', ''))
    coord_status = sweep_info.get('status', 'NOT_PROCESSED')
    
    if coord_status == 'COORD_NOT_RESOLVED':
        archive_status = 'NEEDS_MANUAL_COORDINATES'
    elif coord_status in ['AUTH_REQUIRED', 'NO_HIGH_RES_SPECTRUM_FOUND', 'LOWER_RESOLUTION_CANDIDATE']:
        archive_status = 'AUTH_REQUIRED'
    else:
        archive_status = coord_status
        
    priority = 'HIGH' if reg_info.get('notes', '').lower().find('component') != -1 or 'HIRES' in instrument or 'UVES' in instrument else 'NORMAL'

    
    c_kms = 299792.458
    lya_obs = 1215.67 * (1 + z_abs)
    lam_min = lya_obs * (1 - 300.0 / c_kms)
    lam_max = lya_obs * (1 + 100.0 / c_kms)
    req_window = [lam_min, lam_max]
    
    pack_data.append({
        'System': name,
        'Instrument': instrument,
        'Absorber_z': z_abs,
        'LyA_Observed_A': round(lya_obs, 2),
        'Required_Window_A': f"[{round(req_window[0], 2)}, {round(req_window[1], 2)}]",
        'Status': sys_data['status'],
        'RA_deg': round(ra_deg, 5) if isinstance(ra_deg, float) else ra_deg,
        'Dec_deg': round(dec_deg, 5) if isinstance(dec_deg, float) else dec_deg,
        'coordinate_status': coord_status,
        'archive_sweep_status': archive_status,
        'priority': priority
    })

df = pd.DataFrame(pack_data)

md_path = project_root / 'data/processed/manual_spectrum_request_pack.md'
csv_path = project_root / 'data/processed/manual_spectrum_request_pack.csv'

df.to_csv(csv_path, index=False)

with open(md_path, 'w') as f:
    f.write("# Manual Spectrum Request Pack\n\n")
    f.write("The following systems are required for the TEP population analysis but are behind authentication gateways or not found in automated phase 3 archives.\n\n")
    f.write(df.to_markdown(index=False))
    
print(f"Generated manual request pack with {len(df)} systems.")
