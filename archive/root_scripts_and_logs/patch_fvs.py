import json
from pathlib import Path

data_dir = Path("data/processed")

fvs = [
    ("measured_feature_vector_Q0913+072.json", 2.618, False, True),
    ("measured_feature_vector_PKS1937-1009_z3.256.json", 3.256, True, False)
]

for filename, ref_z, is_proxy, sci_use in fvs:
    filepath = data_dir / filename
    if filepath.exists():
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        data['reference_redshift'] = ref_z
        data['is_proxy'] = is_proxy
        data['scientific_use'] = sci_use
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"Patched {filename}")

