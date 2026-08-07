with open("scripts/steps/step_15_catalog_scale.py", "r") as f:
    code = f.read()

target = """    systems = registry['systems']"""
replacement = """    systems = registry.get('systems', registry) if isinstance(registry, dict) else registry"""

code = code.replace(target, replacement)

with open("scripts/steps/step_15_catalog_scale.py", "w") as f:
    f.write(code)
