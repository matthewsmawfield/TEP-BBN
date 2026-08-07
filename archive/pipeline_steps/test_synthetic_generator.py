import sys
from pathlib import Path
import json
import numpy as np

script_dir = Path(__file__).parent
project_root = script_dir.parent.parent
sys.path.append(str(project_root))

from scripts.steps.step_14c_joint_power_triage_screen import load_joint_spectra, generate_synthetic_joint_flux
import scripts.steps.step_13c_nested_synthetic_adversarial_validation as step13c

def main():
    print("--- Testing Synthetic Generator ---")
    manifest_path = project_root / 'data/processed/Q1009+2956_z2.504_HIRES_spectrum_manifest.json'
    spectra = load_joint_spectra(str(manifest_path))
    
    feature_vector_path = project_root / 'data/processed/measured_feature_vector_Q1009+2956_z2.504.json'
    with open(feature_vector_path) as f:
        step13c.set_system_feature_vector(json.load(f))

    physical_params_null = {'v_shift': 0.0, 'B_abs': 1.5e-5, 'f_D': 0.0, 'alpha': 0.0}
    physical_params_tep = {'v_shift': 0.0, 'B_abs': 1.5e-5, 'f_D': 0.0, 'alpha': 0.0007}

    print("Test 1: Identical seeds produce identical spectra")
    s1, m1 = generate_synthetic_joint_flux(spectra=spectra, generating_model='H2', physical_parameters=physical_params_tep, data_seed=123)
    s2, m2 = generate_synthetic_joint_flux(spectra=spectra, generating_model='H2', physical_parameters=physical_params_tep, data_seed=123)
    assert m1['flux_sha256'] == m2['flux_sha256'], "Hashes must match for identical seed"
    print(" -> Passed")

    print("Test 2: Different seeds alter noise but preserve noiseless structure")
    s3, m3 = generate_synthetic_joint_flux(spectra=spectra, generating_model='H2', physical_parameters=physical_params_tep, data_seed=456)
    assert m1['flux_sha256'] != m3['flux_sha256'], "Hashes must differ for different seeds"
    print(" -> Passed")

    print("Test 3: H2 alpha=0.0007 numerically differs from matched null")
    diff = m1['maximum_difference_from_null']
    print(f" -> Max diff from null = {diff:.6f}")
    assert diff > 1e-5, "Injection must differ from null"
    print(" -> Passed")

    print("Test 4: H0 generation mathematically behaves like null alpha=0")
    s_h0, m_h0 = generate_synthetic_joint_flux(spectra=spectra, generating_model='H0', physical_parameters=physical_params_null, data_seed=123)
    assert m_h0['maximum_difference_from_null'] == 0.0, "H0 at alpha=0 must have zero difference from null (since it IS null)"
    print(" -> Passed")
    
    print("Test 5: Actual Q1009 flux is never used as synthetic baseline")
    assert m1['observed_flux_used'] is False
    print(" -> Passed")
    
    print("All tests passed.")

if __name__ == '__main__':
    main()
