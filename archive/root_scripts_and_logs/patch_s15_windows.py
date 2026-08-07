import re

with open("scripts/steps/step_15_catalog_scale.py", "r") as f:
    code = f.read()

replacement = """
        if not merged_windows:
            merged_windows = [[-100.0, 100.0]]  # Fallback to avoid crash on single-component systems
            
        lz, lzerr, pdiag = fit_model_nested(flux, 'M4_secondary_local', noise, centroid_bounds=centroid_bounds, sec_windows=merged_windows)
"""
code = code.replace("        lz, lzerr, pdiag = fit_model_nested(flux, 'M4_secondary_local', noise, centroid_bounds=centroid_bounds, sec_windows=merged_windows)", replacement)

with open("scripts/steps/step_15_catalog_scale.py", "w") as f:
    f.write(code)
    print("Patched M4_secondary_local window logic.")
