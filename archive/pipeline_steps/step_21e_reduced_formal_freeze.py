import sys
import json
import hashlib
from pathlib import Path

script_dir = Path(__file__).parent
project_root = script_dir.parent.parent
sys.path.append(str(project_root))

def get_file_sha256(filepath):
    h = hashlib.sha256()
    with open(filepath, 'rb') as f:
        h.update(f.read())
    return h.hexdigest()

def main():
    audit_results_path = project_root / 'data/processed/q1009_reduced_convergence_audit_results.json'
    with open(audit_results_path) as f:
        results = json.load(f)
        
    print("Reduced Convergence Audit Summary:")
    nlives = [100, 300, 600]
    for nl in nlives:
        subset = [r for r in results if r['nlive'] == nl]
        deltas = [r['delta_logz'] for r in subset]
        mean_dz = sum(deltas) / len(deltas)
        min_dz = min(deltas)
        max_dz = max(deltas)
        edges = sum(1 for r in subset if r['at_lower'] or r['at_upper'])
        print(f"nlive={nl:3d}: delta_logZ = {mean_dz:.1f} (range {min_dz:.1f} to {max_dz:.1f}), edges hit = {edges}/{len(subset)}")
        
    # Verify that nlive=600 stably produces delta_logZ > 5.0
    nlive600_results = [r for r in results if r['nlive'] == 600]
    if all(r['delta_logz'] > 5.0 for r in nlive600_results):
        print("\nSTATUS: SAMPLER_QUALIFIED")
        
        # Write formal freeze configuration
        joint_lib_path = project_root / 'scripts/lib/joint_spectrum_likelihood.py'
        manifest_path = project_root / 'data/processed/Q1009+2956_z2.504_HIRES_spectrum_manifest.json'
        
        freeze_config = {
            "status": "QUALIFIED",
            "joint_likelihood_sha256": get_file_sha256(joint_lib_path),
            "manifest_sha256": get_file_sha256(manifest_path),
            "formal_campaign_ready": True
        }
        
        freeze_path = project_root / 'data/processed/q1009_formal_freeze_config.json'
        with open(freeze_path, 'w') as f:
            json.dump(freeze_config, f, indent=2)
            
        print(f"Formal freeze written to {freeze_path}")
    else:
        print("\nSTATUS: SAMPLER_FAILED_CONVERGENCE")
        sys.exit(1)

if __name__ == '__main__':
    main()
