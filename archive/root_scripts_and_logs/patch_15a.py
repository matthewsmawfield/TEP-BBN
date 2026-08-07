with open("scripts/steps/step_15a_generate_manual_acquisition_manifest.py", "r") as f:
    code = f.read()
    
target = """for sys_data in missing_manifest:
    name = sys_data['qso_name']
    z_abs = sys_data['absorber_redshift']
    instrument = sys_data['instrument']"""

replacement = """
with open(project_root / 'data/processed/coordinate_archive_sweep_results.json', 'r') as f:
    sweep_results = json.load(f)
sweep_lookup = {s['system_id']: s for s in sweep_results}

with open(project_root / 'data/processed/dh_literature_registry.json', 'r') as f:
    registry = json.load(f)
reg_lookup = {s['system_id']: s for s in registry}

for sys_data in missing_manifest:
    sys_id = sys_data['system_id']
    name = sys_data['qso_name']
    z_abs = sys_data['absorber_redshift']
    instrument = sys_data['instrument']
    
    sweep_info = sweep_lookup.get(sys_id, {})
    reg_info = reg_lookup.get(sys_id, {})
    
    ra_deg = sweep_info.get('ra_deg', '')
    dec_deg = sweep_info.get('dec_deg', '')
    coord_status = sweep_info.get('status', 'NOT_PROCESSED')
    
    if coord_status == 'COORD_NOT_RESOLVED':
        archive_status = 'NEEDS_MANUAL_COORDINATES'
    elif coord_status in ['AUTH_REQUIRED', 'NO_HIGH_RES_SPECTRUM_FOUND', 'LOWER_RESOLUTION_CANDIDATE']:
        archive_status = 'AUTH_REQUIRED'
    else:
        archive_status = coord_status
        
    priority = 'HIGH' if reg_info.get('notes', '').lower().find('component') != -1 or 'HIRES' in instrument or 'UVES' in instrument else 'NORMAL'
"""

target2 = """    pack_data.append({
        'System': name,
        'Instrument': instrument,
        'Absorber_z': z_abs,
        'LyA_Observed_A': round(lya_obs, 2),
        'Required_Window_A': f"[{round(req_window[0], 2)}, {round(req_window[1], 2)}]",
        'Status': sys_data['status']
    })"""

replacement2 = """    pack_data.append({
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
    })"""

code = code.replace(target, replacement).replace(target2, replacement2)
with open("scripts/steps/step_15a_generate_manual_acquisition_manifest.py", "w") as f:
    f.write(code)
