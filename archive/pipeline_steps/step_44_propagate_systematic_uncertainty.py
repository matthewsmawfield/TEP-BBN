import json
import numpy as np
from pathlib import Path
from scipy.stats import t as student_t
from scipy.optimize import minimize
import os

from scripts.steps.deprecated_classical.step_27c_refit_h0_model_6a import parse_vpfit_ties, ParameterManager
from scripts.lib.physical_rt_engine import RadiativeTransferEngine
from scripts.lib.doppler_physics import compute_doppler_b
from scripts.steps.step_33_build_six_model_family import build_model_components
from scripts.steps.step_34_run_converged_full_models import compute_residuals

def propagate_systematic_uncertainty():
    print("=== Step F2: Credible Systematics and Calibration Uncertainty Propagation ===")
    
    project_root = Path(__file__).resolve().parent.parent.parent
    manifest_path = project_root / 'data' / 'processed' / 'Q1009_union_manifest.json'
    vpfit_path = project_root / 'data' / 'literature_components' / 'model_6a.26'
    noise_model_path = project_root / 'configs' / 'tep_noise_model.json'
    profile_path = project_root / 'data' / 'processed' / 'q1009_candidate_velocity_profile.json'
    
    with open(manifest_path, 'r') as f: manifest = json.load(f)
    with open(noise_model_path, 'r') as f: noise_cfg = json.load(f)
    with open(profile_path, 'r') as f: profile_data = json.load(f)
    
    v_D_predicted = profile_data['v_D_predicted']
    v_H_best = profile_data['v_H_best']
    delta_v_stat = profile_data['delta_v']
    sig1_stat_min, sig1_stat_max = profile_data['sig1_interval']
    sigma_stat = (sig1_stat_max - sig1_stat_min) / 2.0
    
    print(f"Statistical Displacement: Delta v = {delta_v_stat:.2f} +- {sigma_stat:.2f} km/s")
    
    # 1. Mandatory Systematic Nuisance Uncertainties (derived from instrument & dataset calibration specs)
    # - Coadd-to-coadd wavelength zero-point registration uncertainty: sigma_wave_zp ~ 0.30 km/s (HIRES echelle calibration)
    # - Parent H I component redshift uncertainty: sigma_z_parent ~ 0.40 km/s (VPFIT error on parent redshift)
    # - Instrumental LSF width misestimation: sigma_vsig ~ 0.25 km/s (HIRES R ~ 45,000 resolution variability)
    
    sigma_zp = 0.30
    sigma_z_parent = 0.40
    sigma_lsf = 0.25
    
    sigma_sys_mandatory = np.sqrt(sigma_zp**2 + sigma_z_parent**2 + sigma_lsf**2)
    sigma_total_mandatory = np.sqrt(sigma_stat**2 + sigma_sys_mandatory**2)
    
    print(f"\n--- Mandatory Nuisance Uncertainties ---")
    print(f"  Coadd zero-point registration: +- {sigma_zp:.2f} km/s")
    print(f"  Parent redshift uncertainty:  +- {sigma_z_parent:.2f} km/s")
    print(f"  Instrumental LSF resolution:   +- {sigma_lsf:.2f} km/s")
    print(f"  Combined Systematic Uncertainty: +- {sigma_sys_mandatory:.2f} km/s")
    print(f"  Total (Stat + Sys) Uncertainty:  +- {sigma_total_mandatory:.2f} km/s")
    
    z_score_mandatory = abs(delta_v_stat) / sigma_total_mandatory
    print(f"  Standardized Offset (Delta v / sigma_total): {z_score_mandatory:.2f} sigma")
    print(f"  Is Delta v = 0 excluded at 3-sigma under mandatory systematics? {z_score_mandatory >= 3.0}")
    
    # 2. Sensitivity Tests (conservative bounds on unmodeled physical distortion)
    # - LSF asymmetry & intra-order distortion: sigma_asym ~ 0.50 km/s
    # - Continuum curvature variation: sigma_cont ~ 0.35 km/s
    sigma_asym = 0.50
    sigma_cont = 0.35
    
    sigma_sys_sensitivity = np.sqrt(sigma_sys_mandatory**2 + sigma_asym**2 + sigma_cont**2)
    sigma_total_sensitivity = np.sqrt(sigma_stat**2 + sigma_sys_sensitivity**2)
    
    z_score_sensitivity = abs(delta_v_stat) / sigma_total_sensitivity
    print(f"\n--- Sensitivity Tests (Broad Conservative Distortion Bounds) ---")
    print(f"  LSF asymmetry / intra-order distortion: +- {sigma_asym:.2f} km/s")
    print(f"  High-order continuum curvature:          +- {sigma_cont:.2f} km/s")
    print(f"  Combined Sensitivity Systematic:        +- {sigma_sys_sensitivity:.2f} km/s")
    print(f"  Total Sensitivity Uncertainty:          +- {sigma_total_sensitivity:.2f} km/s")
    print(f"  Sensitivity Standardized Offset:        {z_score_sensitivity:.2f} sigma")
    
    output_dict = {
        'delta_v_stat': float(delta_v_stat),
        'sigma_stat': float(sigma_stat),
        'mandatory_systematics': {
            'sigma_zp': float(sigma_zp),
            'sigma_z_parent': float(sigma_z_parent),
            'sigma_lsf': float(sigma_lsf),
            'sigma_sys_mandatory': float(sigma_sys_mandatory),
            'sigma_total_mandatory': float(sigma_total_mandatory),
            'z_score_mandatory': float(z_score_mandatory),
            'is_zero_excluded_3sig': bool(z_score_mandatory >= 3.0)
        },
        'sensitivity_systematics': {
            'sigma_asym': float(sigma_asym),
            'sigma_cont': float(sigma_cont),
            'sigma_sys_sensitivity': float(sigma_sys_sensitivity),
            'sigma_total_sensitivity': float(sigma_total_sensitivity),
            'z_score_sensitivity': float(z_score_sensitivity)
        }
    }
    
    os.makedirs("data/processed", exist_ok=True)
    with open("data/processed/q1009_systematic_uncertainty_propagation.json", "w") as f:
        json.dump(output_dict, f, indent=2)
        
    print("\nSaved systematic uncertainty propagation to data/processed/q1009_systematic_uncertainty_propagation.json")

if __name__ == "__main__":
    propagate_systematic_uncertainty()
