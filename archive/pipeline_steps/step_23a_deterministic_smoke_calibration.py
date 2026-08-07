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
import scripts.steps.step_13c_nested_synthetic_adversarial_validation as step13c

def compute_masks(spectra):
    """
    Computes train_mask and held_out_mask for each spectrum.
    Held out: The secondary predicted windows based on alpha_blind_interval.
    Train: Everything else.
    """
    c_kms = 299792.458
    alpha_blind_interval = [0.0005, 0.0009]
    g_primary = step13c.components[step13c.primary_idx]['g_i']
    
    sec_windows_raw = []
    w_sec = 3.0
    for i, hc in enumerate(step13c.hi_comps):
        if i == step13c.primary_idx: continue
        g_i = step13c.components[i]['g_i']
        s1 = c_kms * alpha_blind_interval[0] * (g_i - g_primary)
        s2 = c_kms * alpha_blind_interval[1] * (g_i - g_primary)
        v_base = hc['v'] - 82.0
        v_min = v_base + min(s1, s2)
        v_max = v_base + max(s1, s2)
        sec_windows_raw.append([v_min - w_sec, v_max + w_sec])
        
    sec_windows_raw.sort(key=lambda x: x[0])
    merged_windows = []
    for w in sec_windows_raw:
        if not merged_windows:
            merged_windows.append(w)
        else:
            last = merged_windows[-1]
            if w[0] <= last[1]:
                merged_windows[-1] = [last[0], max(last[1], w[1])]
            else:
                merged_windows.append(w)
                
    for spec in spectra:
        v = spec['v']
        held_mask = np.zeros_like(v, dtype=bool)
        for mw in merged_windows:
            held_mask |= (v >= mw[0]) & (v <= mw[1])
            
        spec['held_out_mask'] = held_mask
        spec['train_mask'] = ~held_mask

def run_smoke_calibration():
    print("--- Deterministic Smoke Calibration ---")
    manifest_path = project_root / 'data/processed/Q1009+2956_z2.504_HIRES_spectrum_manifest.json'
    base_spectra = load_joint_spectra(str(manifest_path))
    
    feature_vector_path = project_root / 'data/processed/measured_feature_vector_Q1009+2956_z2.504.json'
    with open(feature_vector_path) as f:
        step13c.set_system_feature_vector(json.load(f))
        
    # Calculate fixed masks
    compute_masks(base_spectra)
    
    null_params = {'v_shift': 0.0, 'B_abs': 1.5e-5, 'f_D': 1.0, 'alpha': 0.0, 'int_v': 0.0, 'int_n': 0.0, 'int_b': 5.0}
    tep_params = {'v_shift': 0.0, 'B_abs': 1.5e-5, 'f_D': 0.0, 'alpha': 0.0007}
    
    null_results = []
    tep_results = []
    
    print("\nRunning 10 Null Simulations (H0 -> H0, H1, H2)")
    for i in range(10):
        print(f" Null Trial {i+1}/10...")
        synth_spec, _ = generate_synthetic_joint_flux(
            spectra=base_spectra,
            generating_model='H0',
            physical_parameters=null_params,
            data_seed=1000 + i
        )
        
        # Apply the frozen masks to the noisy synthetic spectra
        for s, bs in zip(synth_spec, base_spectra):
            s['train_mask'] = bs['train_mask']
            s['held_out_mask'] = bs['held_out_mask']
            
        r_h0 = fit_deterministic_model(synth_spec, 'H0')
        r_h1 = fit_deterministic_model(synth_spec, 'H1')
        r_h2 = fit_deterministic_model(synth_spec, 'H2')
        
        T_full = 2 * (r_h2['logL_train'] - r_h0['logL_train'])
        T_sec = 2 * (r_h2['logL_train'] - r_h1['logL_train'])
        S_held = 2 * (r_h2['logL_held'] - max(r_h0['logL_held'], r_h1['logL_held']))
        
        provisionally_positive = (T_full > 0) and (T_sec > 0) and (S_held > 0)
        null_results.append(provisionally_positive)
        print(f"  -> T_full={T_full:.2f}, T_sec={T_sec:.2f}, S_held={S_held:.2f} | Positive: {provisionally_positive}")
        
    print("\nRunning 10 TEP Simulations (alpha=0.0007 -> H0, H1, H2)")
    for i in range(10):
        print(f" TEP Trial {i+1}/10...")
        synth_spec, _ = generate_synthetic_joint_flux(
            spectra=base_spectra,
            generating_model='H2',
            physical_parameters=tep_params,
            data_seed=2000 + i
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
        
        provisionally_positive = (T_full > 0) and (T_sec > 0) and (S_held > 0)
        tep_results.append(provisionally_positive)
        print(f"  -> T_full={T_full:.2f}, T_sec={T_sec:.2f}, S_held={S_held:.2f} | Positive: {provisionally_positive}")
        
    null_pos = sum(null_results)
    tep_pos = sum(tep_results)
    
    print("\n--- Smoke Test Summary ---")
    print(f"Null Provisional Positives: {null_pos}/10 (Required: 0/10)")
    print(f"TEP Provisional Recoveries: {tep_pos}/10 (Required: >=8/10)")
    
    if null_pos == 0 and tep_pos >= 8:
        print("\nSTATUS: PROVISIONAL_QUALIFIED. The deterministic engine behaves sensibly.")
    else:
        print("\nSTATUS: SMOKE_FAILED. The deterministic engine failed basic operational sanity checks.")

if __name__ == '__main__':
    run_smoke_calibration()
