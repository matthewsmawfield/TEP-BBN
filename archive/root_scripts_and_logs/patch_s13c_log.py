with open("scripts/steps/step_13c_nested_synthetic_adversarial_validation.py", "r") as f:
    code = f.read()

target = """    if not is_tep_win:
        if delta_tep <= 0.0:
            reason = "Standard D / non-TEP models dominate or tie; TEP replacement criteria not satisfied."
"""

replacement = """    if not is_tep_win:
        if delta_tep <= 2.0 or delta_tep <= combined_err_tep:
            reason = "Standard D / non-TEP models dominate or tie; TEP replacement criteria not satisfied."
"""

code = code.replace(target, replacement)

with open("scripts/steps/step_13c_nested_synthetic_adversarial_validation.py", "w") as f:
    f.write(code)
print("Patched s13c log output.")
