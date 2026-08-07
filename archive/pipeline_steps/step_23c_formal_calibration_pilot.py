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

def run_calibration_pilot():
    print("--- Formal Calibration Pilot ---")
    manifest_path = project_root / 'data/processed/Q1009+2956_z2.504_HIRES_spectrum_manifest.json'
    base_spectra = load_joint_spectra(str(manifest_path))
    
    feature_vector_path = project_root / 'data/processed/measured_feature_vector_Q1009+2956_z2.504.json'
    with open(feature_vector_path) as f:
        step13c.set_system_feature_vector(json.load(f))
        
    compute_masks(base_spectra)
    
    null_params = {'v_shift': 0.0, 'B_abs': 1.5e-5, 'f_D': 1.0, 'alpha': 0.0, 'int_v': 0.0, 'int_n': 0.0, 'int_b': 5.0}
    tep_params = {'v_shift': 0.0, 'B_abs': 1.5e-5, 'f_D': 0.0, 'alpha': 0.0007}
    
    results = []
    
    print("Running 100 Null Simulations...")
    for i in range(100):
        seed = 40001 + i
        synth_spec, manifest = generate_synthetic_joint_flux(
            spectra=base_spectra,
            generating_model='H0',
            physical_parameters=null_params,
            data_seed=seed
        )
        
        for s, bs in zip(synth_spec, base_spectra):
            s['train_mask'] = bs['train_mask']
            s['held_out_mask'] = bs['held_out_mask']
            
        r_h0 = fit_deterministic_model(synth_spec, 'H0')
        r_h1 = fit_deterministic_model(synth_spec, 'H1')
        r_h2 = fit_deterministic_model(synth_spec, 'H2')
        
        T_full = 2 * (r_h2['logL_train'] - r_h0['logL_train'])
        T_sec = 2 * (r_h2['logL_train'] - r_h1['logL_train'])
        S_held = 2 * (r_h2['logL_held'] - max(r_h0['logL_held'], r_h1['logL_held']))
        
        res_dict = {
            "condition": "null",
            "data_seed": seed,
            "generating_model": "H0",
            "actual_parameters": null_params,
            "flux_sha256": manifest["flux_sha256"],
            "H0": {"logL_train": r_h0['logL_train'], "logL_held": r_h0['logL_held'], "converged": r_h0['converged']},
            "H1": {"logL_train": r_h1['logL_train'], "logL_held": r_h1['logL_held'], "converged": r_h1['converged']},
            "H2": {"logL_train": r_h2['logL_train'], "logL_held": r_h2['logL_held'], "converged": r_h2['converged']},
            "T_full": T_full,
            "T_secondary": T_sec,
            "S_held": S_held,
            "active_boundaries": list(set(list(r_h0['active_bounds'].keys()) + list(r_h1['active_bounds'].keys()) + list(r_h2['active_bounds'].keys()))),
            "completed": True
        }
        results.append(res_dict)
        if (i+1) % 10 == 0:
            print(f"  Completed {i+1}/100 Nulls")
            
    print("Running 50 TEP Simulations...")
    for i in range(50):
        seed = 50001 + i
        synth_spec, manifest = generate_synthetic_joint_flux(
            spectra=base_spectra,
            generating_model='H2',
            physical_parameters=tep_params,
            data_seed=seed
        )
        
        for s, bs in zip(synth_spec, base_spectra):
            s['train_mask'] = bs['train_mask']
            s['held_out_mask'] = bs['held_out_mask']
            
        r_h0 = fit_deterministic_model(synth_spec, 'H0')
        r_h1 = fit_deterministic_model(synth_spec, 'H1')
        r_h2 = fit_deterministic_model(synth_spec, 'H2')
        
        T_full = 2 * (r_h2['logL_train'] - r_h0['logL_train'])
        T_sec = 2 * (r_h2['logL_train'] - r_h1['logL_train'])
        S_held = 2 * (r_h2['logL_held'] - max(r_h0['logL_held'], r_h1['logL_held']))
        
        res_dict = {
            "condition": "TEP_0.0007",
            "data_seed": seed,
            "generating_model": "H2",
            "actual_parameters": tep_params,
            "flux_sha256": manifest["flux_sha256"],
            "H0": {"logL_train": r_h0['logL_train'], "logL_held": r_h0['logL_held'], "converged": r_h0['converged']},
            "H1": {"logL_train": r_h1['logL_train'], "logL_held": r_h1['logL_held'], "converged": r_h1['converged']},
            "H2": {"logL_train": r_h2['logL_train'], "logL_held": r_h2['logL_held'], "converged": r_h2['converged']},
            "T_full": T_full,
            "T_secondary": T_sec,
            "S_held": S_held,
            "active_boundaries": list(set(list(r_h0['active_bounds'].keys()) + list(r_h1['active_bounds'].keys()) + list(r_h2['active_bounds'].keys()))),
            "completed": True
        }
        results.append(res_dict)
        if (i+1) % 10 == 0:
            print(f"  Completed {i+1}/50 TEPs")

    # Evaluate gates
    nulls = [r for r in results if r['condition'] == 'null']
    teps = [r for r in results if r['condition'] == 'TEP_0.0007']
    
    # 1. Numerical reliability
    all_completed = all(r['completed'] for r in results)
    all_converged = all(r['H0']['converged'] and r['H1']['converged'] and r['H2']['converged'] for r in results)
    print(f"\nNumerical Reliability: All completed: {all_completed}, All converged: {all_converged}")
    
    # 2. Null behaviour
    gross_false_positives = [r for r in nulls if r['T_full'] >= 25 and r['T_secondary'] >= 2 and r['S_held'] >= 10]
    print(f"Gross Null False Positives (Alarm threshold): {len(gross_false_positives)}/100")
    
    # 3. Central recovery
    central_recoveries = [r for r in teps if r['T_full'] >= 25 and r['T_secondary'] >= 2 and r['S_held'] >= 10]
    print(f"Central TEP Recoveries: {len(central_recoveries)}/50")
    
    # 4. Distribution separation
    null_t_full = [r['T_full'] for r in nulls]
    tep_t_full = [r['T_full'] for r in teps]
    null_t_full_99 = np.percentile(null_t_full, 99)
    tep_t_full_10 = np.percentile(tep_t_full, 10)
    
    null_s_held = [r['S_held'] for r in nulls]
    tep_s_held = [r['S_held'] for r in teps]
    null_s_held_99 = np.percentile(null_s_held, 99)
    tep_s_held_10 = np.percentile(tep_s_held, 10)
    
    print("\nDistribution Separation:")
    print(f"  T_full: Null 99th ({null_t_full_99:.2f}) < TEP 10th ({tep_t_full_10:.2f})")
    print(f"  S_held: Null 99th ({null_s_held_99:.2f}) < TEP 10th ({tep_s_held_10:.2f})")
    
    out_path = project_root / 'data/processed/q1009_calibration_pilot.json'
    with open(out_path, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\nPilot results saved to {out_path}")

if __name__ == '__main__':
    run_calibration_pilot()
