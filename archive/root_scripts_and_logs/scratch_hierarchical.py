import json
import numpy as np

with open('data/processed/dh_literature_registry.json', 'r') as f:
    systems = {s['system_id']: s for s in json.load(f)['systems']}

secure_ids = [
    "Q0913+072_z2.618", "Q1243+3047_z2.529", 
    "J1419+0829_z3.049840", "PKS1937-1009_z3.256", 
    "SDSSJ1358+6522_z3.067", "SDSSJ1558-0031_z2.702",
    "Q1351+3221_z2.597", "HS0105+1619_z2.536",
    "Q1444+2919_z2.428"
]

print(f"{'System':<25} | {'D/H (x1e5)':<12} | {'Err (x1e5)':<12} | {'Weight':<10}")
for sid in secure_ids + ["Q1009+2956_z2.504"]:
    v = systems[sid].get("dh_ratio") or systems[sid].get("reported_dh")
    e = systems[sid].get("dh_error") or (systems[sid].get("reported_dh")*0.015)
    w = 1.0 / e**2
    print(f"{sid:<25} | {v*1e5:<12.3f} | {e*1e5:<12.3f} | {w/1e10:<10.3f}")

