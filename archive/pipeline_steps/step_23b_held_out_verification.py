import os
import sys
import numpy as np
import json
from pathlib import Path

script_dir = Path(__file__).parent
project_root = script_dir.parent.parent
sys.path.append(str(project_root))

from scripts.steps.step_14c_joint_power_triage_screen import load_joint_spectra, generate_synthetic_joint_flux
from scripts.lib.q1009_primary_test_engine import fit_deterministic_model
from scripts.steps.step_23a_deterministic_smoke_calibration import compute_masks
import scripts.steps.step_13c_nested_synthetic_adversarial_validation as step13c

def main():
    manifest_path = project_root / 'data/processed/Q1009+2956_z2.504_HIRES_spectrum_manifest.json'
    base_spectra = load_joint_spectra(str(manifest_path))
    
    feature_vector_path = project_root / 'data/processed/measured_feature_vector_Q1009+2956_z2.504.json'
    with open(feature_vector_path) as f:
        step13c.set_system_feature_vector(json.load(f))
        
    compute_masks(base_spectra)
    
    tep_params = {'v_shift': 0.0, 'B_abs': 1.5e-5, 'f_D': 0.0, 'alpha': 0.0007}
    
    synth_spec, _ = generate_synthetic_joint_flux(
        spectra=base_spectra,
        generating_model='H2',
        physical_parameters=tep_params,
        data_seed=9999
    )
    
    train_pixels = 0
    held_pixels = 0
    for s, bs in zip(synth_spec, base_spectra):
        s['train_mask'] = bs['train_mask']
        s['held_out_mask'] = bs['held_out_mask']
        train_pixels += np.sum(bs['train_mask'])
        held_pixels += np.sum(bs['held_out_mask'])
        
    r_h0 = fit_deterministic_model(synth_spec, 'H0')
    r_h1 = fit_deterministic_model(synth_spec, 'H1')
    r_h2 = fit_deterministic_model(synth_spec, 'H2')
    
    S_held_calculated = 2 * (r_h2['logL_held'] - max(r_h0['logL_held'], r_h1['logL_held']))
    
    output = {
        'training_pixel_count': int(train_pixels),
        'held_out_pixel_count': int(held_pixels),
        'H0_held_out_logL': r_h0['logL_held'],
        'H1_held_out_logL': r_h1['logL_held'],
        'H2_held_out_logL': r_h2['logL_held'],
        'calculated_S_held': S_held_calculated,
        'H0_params_used': {
            'physical': r_h0['physical_parameters'],
            'continuum_c_opts': [c.tolist() for c in r_h0['c_opts']]
        },
        'H1_params_used': {
            'physical': r_h1['physical_parameters'],
            'continuum_c_opts': [c.tolist() for c in r_h1['c_opts']]
        },
        'H2_params_used': {
            'physical': r_h2['physical_parameters'],
            'continuum_c_opts': [c.tolist() for c in r_h2['c_opts']]
        }
    }
    
    print(json.dumps(output, indent=2))

if __name__ == '__main__':
    main()
