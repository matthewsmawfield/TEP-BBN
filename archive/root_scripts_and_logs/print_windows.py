import json
import numpy as np

with open('data/processed/measured_feature_vector_Q0913+072.json', 'r') as f:
    features = json.load(f)

components = features['components']
hi_comps = [{'v': c['velocity_kms'], 'n': c['metal_alignment_strength'], 'b': 12.0, 'g_i': c['g_i']} for c in components]

c_kms = 299792.458
alpha_blind = [0.0005, 0.0009]

primary_idx = 0
min_diff = 1e9
for i, hc in enumerate(hi_comps):
    v_d = hc['v'] - 82.0
    if abs(v_d - (-81.6)) < min_diff:
        min_diff = abs(v_d - (-81.6))
        primary_idx = i

g_primary = components[primary_idx]['g_i']
w_sec = 4.0 # approximate max(1.0, 3*sigma_v, 3.0)

windows = []
for i, hc in enumerate(hi_comps):
    if i == primary_idx: continue
    g_i = components[i]['g_i']
    s1 = c_kms * alpha_blind[0] * (g_i - g_primary)
    s2 = c_kms * alpha_blind[1] * (g_i - g_primary)
    v_base = hc['v'] - 82.0
    v_min = v_base + min(s1, s2)
    v_max = v_base + max(s1, s2)
    windows.append([v_min - w_sec, v_max + w_sec])

windows.sort(key=lambda x: x[0])
merged = []
for w in windows:
    if not merged: merged.append(w)
    elif w[0] <= merged[-1][1]: merged[-1][1] = max(merged[-1][1], w[1])
    else: merged.append(w)

print("Windows:", merged)
