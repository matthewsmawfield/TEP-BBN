import json
from scripts.steps.step_13c_nested_synthetic_adversarial_validation import components, c_kms

primary_idx = 1
g_primary = components[primary_idx]['g_i']
alpha_blind_interval = [0.0005, 0.0009]

sec_windows_raw = []
w_sec = max(1.0, 3 * 1.5, 3.0)
for i, hc in enumerate(components):
    if i == primary_idx: continue
    g_i = components[i]['g_i']
    s1 = c_kms * alpha_blind_interval[0] * (g_i - g_primary)
    s2 = c_kms * alpha_blind_interval[1] * (g_i - g_primary)
    v_base = -82.0
    v_min = v_base + min(s1, s2)
    v_max = v_base + max(s1, s2)
    sec_windows_raw.append([v_min - w_sec, v_max + w_sec])

sec_windows_raw.sort(key=lambda x: x[0])
merged_windows = []
for w in sec_windows_raw:
    if not merged_windows:
        merged_windows.append(w)
    else:
        last = merged_windows[-1]
        if w[0] <= last[1]:
            merged_windows[-1] = [last[0], max(last[1], w[1])]
        else:
            merged_windows.append(w)

print("Merged Windows:", merged_windows)
print("Total range:", [merged_windows[0][0], merged_windows[-1][1]])
