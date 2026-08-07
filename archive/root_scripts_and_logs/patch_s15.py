import re
import os

with open("scripts/steps/step_15_catalog_scale.py", "r") as f:
    code = f.read()

# Replace the registry load with loading scientific_eligible_systems if not --include-engineering
replacement = """
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--include-engineering', action='store_true')
    args = parser.parse_args()
    
    registry_path = project_root / "data/processed/scientific_eligible_systems.json"
    if args.include_engineering:
        registry_path = project_root / "data/processed/public_dh_target_candidates.json"
        
    if not registry_path.exists():
        print(f"ERROR: Registry {registry_path} not found.")
        sys.exit(1)
"""

code = re.sub(r'    registry_path = project_root / "data/processed/dh_literature_registry.json".*?sys\.exit\(1\)', replacement, code, flags=re.DOTALL)

# Remove the fallback `if not merged_windows:` we added earlier
fallback_removal_target = """        if not merged_windows:
            merged_windows = [[-100.0, 100.0]]  # Fallback to avoid crash on single-component systems
            
        lz, lzerr, pdiag = fit_model_nested(flux, 'M4_secondary_local', noise, centroid_bounds=centroid_bounds, sec_windows=merged_windows)"""

fallback_replacement = """        if not merged_windows:
            logZs['M4_secondary_local'] = -1e9
            logZerrs['M4_secondary_local'] = 0.0
            posteriors['M4_secondary_local'] = {}
        else:
            lz, lzerr, pdiag = fit_model_nested(flux, 'M4_secondary_local', noise, centroid_bounds=centroid_bounds, sec_windows=merged_windows)
            logZs['M4_secondary_local'] = lz
            logZerrs['M4_secondary_local'] = lzerr
            posteriors['M4_secondary_local'] = pdiag"""

code = code.replace(fallback_removal_target, fallback_replacement)

with open("scripts/steps/step_15_catalog_scale.py", "w") as f:
    f.write(code)

print("Patched step_15")
