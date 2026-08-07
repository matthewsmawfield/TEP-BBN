import sys

with open('scripts/steps/step_13c_nested_synthetic_adversarial_validation.py', 'r') as f:
    lines = f.readlines()

new_lines = []
skip = False
for line in lines:
    if line.startswith("with open(project_root / 'data/processed/measured_feature_vector_Q0913+072.json', 'r') as f:"):
        new_lines.append("""
def set_system_feature_vector(fv_data):
    global components, hi_comps, primary_idx
    components = fv_data['components']
    hi_comps = []
    for comp in components:
        v = comp['velocity_kms']
        n_hi = 1.0 * comp['metal_alignment_strength'] 
        hi_comps.append({'v': v, 'n': n_hi, 'b': 12.0, 'g_i': comp['g_i']})
        
    primary_idx = 0
    for i, comp in enumerate(components):
        if comp.get('column_feature', 0.0) == 1.0:
            primary_idx = i
            break

# Initialize with Q0913+072 to avoid breaking scripts that run step_13c directly
import json
with open(project_root / 'data/processed/measured_feature_vector_Q0913+072.json', 'r') as f:
    set_system_feature_vector(json.load(f))
""")
        skip = True
        
    if skip and ("primary_idx = i" in line):
        skip = False
        continue
        
    if skip and not ("c_kms" in line or "alpha_prior" in line or "v_grid" in line or "x_norm" in line):
        continue
        
    if skip and ("c_kms" in line or "alpha_prior" in line or "v_grid" in line or "x_norm" in line):
        new_lines.append(line)
        continue

    if not skip:
        # Also patch g_primary = components[1]['g_i']
        if "g_primary = components[1]['g_i']" in line:
            new_lines.append(line.replace("g_primary = components[1]['g_i']", 
                                          "primary_comp = next((c for c in components if c.get('column_feature', 0.0) == 1.0), components[0])\n        g_primary = primary_comp['g_i']"))
        else:
            new_lines.append(line)

with open('scripts/steps/step_13c_nested_synthetic_adversarial_validation.py', 'w') as f:
    f.writelines(new_lines)
