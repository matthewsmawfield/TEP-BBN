with open("scripts/steps/step_15a_generate_manual_acquisition_manifest.py", "r") as f:
    code = f.read()

target = """    lya_obs = 1215.67 * (1 + z_abs)
    req_window = [lya_obs - 5.0, lya_obs + 5.0]"""

replacement = """    c_kms = 299792.458
    lya_obs = 1215.67 * (1 + z_abs)
    lam_min = lya_obs * (1 - 300.0 / c_kms)
    lam_max = lya_obs * (1 + 100.0 / c_kms)
    req_window = [lam_min, lam_max]"""

code = code.replace(target, replacement)

with open("scripts/steps/step_15a_generate_manual_acquisition_manifest.py", "w") as f:
    f.write(code)
print("Patched step_15a")
