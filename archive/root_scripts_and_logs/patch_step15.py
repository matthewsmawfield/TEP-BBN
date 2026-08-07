import json

# Read existing registry
with open('data/processed/dh_literature_registry.json', 'r') as f:
    reg = json.load(f)

# Read extended
with open('data/processed/extended_dh_target_seed_list.json', 'r') as f:
    ext = json.load(f)

# Combine
existing_sys = {s['system_id'] for s in reg['systems']}
for s in ext:
    if s['system_id'] not in existing_sys:
        reg['systems'].append(s)

with open('data/processed/dh_literature_registry.json', 'w') as f:
    json.dump(reg, f, indent=2)

print("Merged extended seed list into dh_literature_registry.json.")
