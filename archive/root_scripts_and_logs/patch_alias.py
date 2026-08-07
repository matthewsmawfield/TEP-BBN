import json

def patch(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    
    lst = data if isinstance(data, list) else data['systems']
    
    for item in lst:
        if item['system_id'] == 'PKS1937-1009_z3.256':
            if "PKS1937-101" not in item['aliases']:
                item['aliases'].append("PKS1937-101")
                
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)

patch('data/processed/extended_dh_target_seed_list.json')
patch('data/processed/dh_literature_registry.json')
print("Patched aliases.")
