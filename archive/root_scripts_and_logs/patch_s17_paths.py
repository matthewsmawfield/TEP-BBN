with open("scripts/steps/step_17_catalog_integrity_audit.py", "r") as f:
    code = f.read()

target = """        fv_path = project_root / f"data/processed/measured_feature_vector_{sys_id}.json"
        spec_path = project_root / f"data/processed/{sys_id}_1D_spectrum.txt"
        
        if not fv_path.exists():
            if spec_path.exists():"""

replacement = """        qso_name = sys_obj.get("qso_name", sys_id)
        fv_path = project_root / f"data/processed/measured_feature_vector_{sys_id}.json"
        if not fv_path.exists():
            fv_path = project_root / f"data/processed/measured_feature_vector_{qso_name}.json"
            
        spec_path = project_root / f"data/processed/{sys_id}_1D_spectrum.txt"
        if not spec_path.exists():
            spec_path = project_root / f"data/processed/{qso_name}_1D_spectrum.txt"
            
        if not fv_path.exists():
            if spec_path.exists():"""

code = code.replace(target, replacement)

with open("scripts/steps/step_17_catalog_integrity_audit.py", "w") as f:
    f.write(code)
