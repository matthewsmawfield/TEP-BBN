with open("scripts/steps/step_17_catalog_integrity_audit.py", "r") as f:
    code = f.read()

target = """            z_feat = fv.get('reference_redshift', None)"""

replacement = """            # Check if provenance exists
            prov_path = project_root / f"data/processed/{sys_id}_spectrum_provenance.json"
            if not prov_path.exists():
                prov_path = project_root / f"data/processed/{qso_name}_spectrum_provenance.json"
            
            z_prov = None
            if prov_path.exists():
                import json as _json
                with open(prov_path, 'r') as fp:
                    prov = _json.load(fp)
                    z_prov = prov.get('absorber_redshift', None)
            else:
                if status == "SCIENTIFIC_ELIGIBLE": status = "ENGINEERING_ONLY"
                reasons.append("Missing spectrum_provenance.json.")

            z_feat = fv.get('reference_redshift', None)"""

code = code.replace(target, replacement)

target2 = """            if z_feat is not None:
                delta_v = c_kms * (z_feat - z_reg) / (1 + z_reg)
                if abs(delta_v) > 5.0:
                    status = "REDSHIFT_MISMATCH"
                    reasons.append(f"delta_v = {delta_v:.1f} km/s (> 5 km/s threshold). Registry: {z_reg}, FV: {z_feat}")
            else:
                # If reference redshift isn't specified, assume it matches
                pass"""

replacement2 = """            if z_feat is not None:
                delta_v_reg = c_kms * (z_feat - z_reg) / (1 + z_reg)
                if abs(delta_v_reg) > 5.0:
                    status = "REDSHIFT_MISMATCH"
                    reasons.append(f"delta_v (FV vs Reg) = {delta_v_reg:.1f} km/s (> 5 km/s threshold). Registry: {z_reg}, FV: {z_feat}")
                
                if z_prov is not None:
                    delta_v_prov = c_kms * (z_feat - z_prov) / (1 + z_prov)
                    if abs(delta_v_prov) > 5.0:
                        status = "REDSHIFT_MISMATCH"
                        reasons.append(f"delta_v (FV vs Prov) = {delta_v_prov:.1f} km/s (> 5 km/s threshold). Prov: {z_prov}, FV: {z_feat}")
            else:
                # If reference redshift isn't specified, assume it matches
                pass"""
                
code = code.replace(target2, replacement2)

with open("scripts/steps/step_17_catalog_integrity_audit.py", "w") as f:
    f.write(code)
print("Patched step_17.")
