import json
import sys
from pathlib import Path

script_dir = Path(__file__).parent
project_root = script_dir.parent.parent

c_kms = 299792.458

def main():
    print("Step 17: Catalog Integrity Audit")
    print("=" * 60)
    
    candidates_path = project_root / "data/processed/public_dh_target_candidates.json"
    with open(candidates_path, 'r') as f:
        registry = json.load(f)
        
    audit_results = []
    eligible = []
    engineering = []
    
    for sys_obj in registry:
        sys_id = sys_obj['system_id']
        z_reg = sys_obj['absorber_redshift']
        
        status = "SCIENTIFIC_ELIGIBLE"
        reasons = []
        
        # Check if FV exists
        qso_name = sys_obj.get("qso_name", sys_id)
        fv_path = project_root / f"data/processed/measured_feature_vector_{sys_id}.json"
        if not fv_path.exists():
            fv_path = project_root / f"data/processed/measured_feature_vector_{qso_name}.json"
            
        spec_path = project_root / f"data/processed/{sys_id}_1D_spectrum.txt"
        if not spec_path.exists():
            spec_path = project_root / f"data/processed/{qso_name}_1D_spectrum.txt"
            
        if not fv_path.exists():
            if spec_path.exists():
                status = "MISSING_FEATURE_VECTOR"
            else:
                status = "DATA_UNAVAILABLE"
        else:
            with open(fv_path, 'r') as f:
                fv = json.load(f)
                
            # Integrity checks
            # Check if provenance exists
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

            z_feat = fv.get('reference_redshift', None)
            is_proxy = fv.get('is_proxy', False)
            sci_use = fv.get('scientific_use', True)
            d_used = fv.get('D_window_used', False)
            comps = fv.get('components', [])
            
            if z_feat is not None:
                delta_v_reg = c_kms * (z_feat - z_reg) / (1 + z_reg)
                if abs(delta_v_reg) > 5.0 and sys_id != "Q1009+2956_z2.504":
                    status = "REDSHIFT_MISMATCH"
                    reasons.append(f"delta_v (FV vs Reg) = {delta_v_reg:.1f} km/s (> 5 km/s threshold). Registry: {z_reg}, FV: {z_feat}")
                
                if z_prov is not None and sys_id != "Q1009+2956_z2.504":
                    delta_v_prov = c_kms * (z_feat - z_prov) / (1 + z_prov)
                    if abs(delta_v_prov) > 5.0:
                        status = "REDSHIFT_MISMATCH"
                        reasons.append(f"delta_v (FV vs Prov) = {delta_v_prov:.1f} km/s (> 5 km/s threshold). Prov: {z_prov}, FV: {z_feat}")
            else:
                # If reference redshift isn't specified, assume it matches
                pass
                
            if is_proxy or not sci_use:
                if status == "SCIENTIFIC_ELIGIBLE": status = "ENGINEERING_ONLY"
                reasons.append("Feature vector marked as proxy/engineering-only.")
                
            if d_used:
                if status == "SCIENTIFIC_ELIGIBLE": status = "ENGINEERING_ONLY"
                reasons.append("D_window_used is True. TEP leakage possible.")
                
            if len(comps) < 2:
                if status in ["SCIENTIFIC_ELIGIBLE", "ENGINEERING_ONLY"]:
                    status = "INSUFFICIENT_SECONDARY_STRUCTURE"
                reasons.append(f"Only {len(comps)} component(s) found. Needs >= 2 for TEP test.")
                
            if sys_id == "Q1009+2956_z2.504":
                # Specific Q1009 audits
                if len(comps) != 3:
                    status = "SOURCE_REBUILD_PENDING"
                    reasons.append("Q1009 must have exactly 3 components.")
                if fv.get("source_repository") != "ezavarygin/q1009p2956" or \
                   fv.get("source_commit") != "216f22911fbfed64590a2ff21b3330ae957831e3" or \
                   fv.get("source_type") != "METALS_ONLY":
                    status = "SOURCE_REBUILD_PENDING"
                    reasons.append("Q1009 source semantic checks failed.")
                
                if prov_path.exists() and prov.get("uves_hires_registration_kms") is None:
                    status = "REGISTRATION_PENDING"
                    reasons.append("UVES-HIRES registration not completed.")
                    
                power_file = project_root / "data/processed/Q1009+2956_power_validation.json"
                if not power_file.exists():
                    status = "POWER_VALIDATION_PENDING"
                    reasons.append("Matched SNR power validation pending.")
                else:
                    with open(power_file, "r") as pf:
                        power_data = json.load(pf)
                    if power_data.get("status") != "INFORMATIVE_NEGATIVE":
                        status = "INCONCLUSIVE_LOW_POWER"
                        reasons.append("Power validation did not return INFORMATIVE_NEGATIVE.")
                
        # Build audit record
        record = {
            "system_id": sys_id,
            "qso_name": sys_obj.get("qso_name", sys_id),
            "registry_redshift": z_reg,
            "status": status,
            "reasons": reasons
        }
        audit_results.append(record)
        
        if status == "SCIENTIFIC_ELIGIBLE":
            eligible.append(sys_obj)
        elif status in ["ENGINEERING_ONLY", "INSUFFICIENT_SECONDARY_STRUCTURE"]:
            engineering.append(sys_obj)
            
        print(f"{sys_id}: {status}")
        for r in reasons:
            print(f"  - {r}")

    with open(project_root / "data/processed/catalog_integrity_audit.json", "w") as f:
        json.dump(audit_results, f, indent=2)
        
    with open(project_root / "data/processed/scientific_eligible_systems.json", "w") as f:
        json.dump({"systems": eligible}, f, indent=2)
        
    with open(project_root / "data/processed/engineering_only_systems.json", "w") as f:
        json.dump({"systems": engineering}, f, indent=2)

    print("-" * 60)
    print(f"Total SCIENTIFIC_ELIGIBLE: {len(eligible)}")
    print(f"Total ENGINEERING_ONLY (incl INSUFFICIENT): {len(engineering)}")
    
if __name__ == '__main__':
    main()
