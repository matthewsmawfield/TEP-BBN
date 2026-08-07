import json

def patch_file(filepath):
    with open(filepath, 'r') as f:
        data = json.load(f)
    
    systems = data['systems'] if isinstance(data, dict) else data
    
    for sys in systems:
        if sys['system_id'] == 'J1419+0829_z3.040':
            sys['system_id'] = 'J1419+0829_z3.049840'
            sys['absorber_redshift'] = 3.049840
            
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)

patch_file('data/processed/dh_literature_registry.json')
patch_file('data/processed/public_dh_target_candidates.json')
print("Patched registries.")
