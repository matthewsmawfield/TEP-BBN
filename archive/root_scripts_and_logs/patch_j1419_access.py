import json

with open("data/processed/public_dh_target_candidates.json", "r") as f:
    data = json.load(f)

for sys in data:
    if sys["system_id"] == "J1419+0829_z3.049840":
        sys["status"] = "PUBLIC_SPECTRUM_FOUND"
        sys["access_url"] = "http://archive.eso.org/datalink/links?ID=ivo://eso.org/ID?ADP.2020-06-19T07:49:49.431"

with open("data/processed/public_dh_target_candidates.json", "w") as f:
    json.dump(data, f, indent=2)
