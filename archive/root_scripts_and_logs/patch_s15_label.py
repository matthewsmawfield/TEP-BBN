with open("scripts/steps/step_15_catalog_scale.py", "r") as f:
    code = f.read()

target = """            is_tep_win, classification, reason = classify_result(logZs, logZerrs, posteriors)"""

replacement = """            is_tep_win, classification, reason = classify_result(logZs, logZerrs, posteriors)
            
            if not merged_windows:
                classification = "INSUFFICIENT_SECONDARY_STRUCTURE"
                is_tep_win = False
                reason = "Only 1 component available; cannot test secondary TEP structure."
"""

code = code.replace(target, replacement)

with open("scripts/steps/step_15_catalog_scale.py", "w") as f:
    f.write(code)
print("Patched step_15 label logic.")
