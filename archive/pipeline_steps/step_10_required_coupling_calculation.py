"""
Step 10: Required coupling calculation for TEP-BBN

Calculates the required TEP coupling to mimic D/H isotope shift.

This step does NOT calibrate parameters to achieve the target.
It solves for the required coupling given the component structure.
"""

import json
from pathlib import Path
from datetime import datetime
import sys
import numpy as np

# Add parent directory to path for imports
script_dir = Path(__file__).parent
project_root = script_dir.parent.parent
sys.path.insert(0, str(project_root))

def compute_required_alpha(features, delta_ln_a_required):
    """
    Compute required α for given features and required ΔlnA.
    
    For a shear law: ΔlnA = α * f
    Required α = ΔlnA_required / max(|f_i - f_j|)
    """
    features = np.asarray(features, dtype=float)
    delta_features = np.abs(features[:, None] - features[None, :])
    max_delta_feature = np.max(delta_features)
    
    if max_delta_feature == 0:
        return {
            'max_delta_feature': 0.0,
            'alpha_required': None,
            'status': 'fail_no_differential_feature'
        }
    
    alpha_required = delta_ln_a_required / max_delta_feature
    
    return {
        'max_delta_feature': float(max_delta_feature),
        'alpha_required': float(alpha_required),
        'status': 'computed'
    }

def calculate_required_coupling():
    """
    Calculate required TEP coupling for differential shear.
    
    This step:
    1. Loads DLA structure characterization
    2. Defines multiple shear law models
    3. Computes required coupling for each model
    4. Compares to TEP theory priors
    """
    print("Step 10: Required coupling calculation")
    print("=" * 60)
    print("CRITICAL: This step computes required TEP coupling.")
    print("No placeholder or synthetic data is allowed.")
    print("NOTE: This does NOT calibrate parameters to achieve target.")
    print("It solves for required coupling given component structure.")
    print("=" * 60)
    print()
    
    # Load DLA structure characterization
    structure_path = project_root / 'data/processed/dla_structure_characterization.json'
    if not structure_path.exists():
        print("ERROR: DLA structure characterization not found")
        print("Run step_09 to characterize DLA structure")
        return None
    
    with open(structure_path, 'r') as f:
        dla_structure = json.load(f)
    
    print(f"System: {dla_structure['system_id']}")
    print()
    
    # Required ΔlnA from Gate 0
    delta_ln_a_required = dla_structure['required_delta_ln_a']
    print(f"Required ΔlnA for deuterium mimicry: {delta_ln_a_required:.6e}")
    print(f"  (82 km/s / c = 82 / 299792)")
    print()
    
    # Extract DLA structure
    n_components = dla_structure['velocity_components']['n_components']
    component_log_n_hi = dla_structure['column_densities']['component_log_n_hi']
    size_range = dla_structure['physical_scales']['plausible_cloud_sizes_kpc']
    
    # Constants
    CM_PER_KPC = 3.085677581e21
    
    # Define shear law models
    shear_laws = {
        'S1_density_gradient': {
            'name': 'Density gradient',
            'equation': 'ΔlnA = κ * Δln(ρ/ρ₀)',
            'description': 'Shear proportional to density contrast',
            'parameters': {
                'kappa': {
                    'value': 1.0,
                    'description': 'Coupling constant',
                    'provisional_prior_range': [0.1, 10.0],
                    'note': 'Provisional range - not yet derived from TEP theory'
                },
                'rho_0': {
                    'value': 0.1,
                    'description': 'Reference density (cm^-3)',
                    'range': [0.01, 1.0]
                }
            }
        },
        'S2_column_gradient': {
            'name': 'Column density gradient',
            'equation': 'ΔlnA = λ * Δln(N_HI/N₀)',
            'description': 'Shear proportional to column density contrast',
            'parameters': {
                'lambda': {
                    'value': 1.0,
                    'description': 'Coupling constant',
                    'provisional_prior_range': [0.1, 10.0],
                    'note': 'Provisional range - not yet derived from TEP theory'
                },
                'N_0': {
                    'value': 1e20,
                    'description': 'Reference column density (cm^-2)',
                    'range': [1e19, 1e21]
                }
            }
        },
        'toy_power_law': {
            'name': 'Power law toy model',
            'equation': 'ΔlnA = α * (ρ/ρ₀)^β * (L/L₀)^γ',
            'description': 'Ad hoc power law model (toy only)',
            'parameters': {
                'alpha': {
                    'value': 1.0e-4,
                    'description': 'Overall shear amplitude',
                    'provisional_prior_range': [1.0e-5, 1.0e-3],
                    'note': 'Provisional range - not yet derived from TEP theory'
                },
                'beta': {
                    'value': 1.0,
                    'description': 'Density dependence exponent',
                    'range': [0.5, 2.0]
                },
                'gamma': {
                    'value': 0.5,
                    'description': 'Scale dependence exponent',
                    'range': [0.0, 1.0]
                },
                'rho_0': {
                    'value': 0.1,
                    'description': 'Reference density (cm^-3)',
                    'range': [0.01, 1.0]
                },
                'L_0': {
                    'value': 1.0,
                    'description': 'Reference scale (kpc)',
                    'range': [0.1, 10.0]
                }
            }
        }
    }
    
    print("Shear Law Models:")
    for law_name, law_info in shear_laws.items():
        print(f"  {law_name}: {law_info['name']}")
        print(f"    Equation: {law_info['equation']}")
    print()
    
    print("IMPORTANT NOTE:")
    print("  Under equal cloud-size assumptions, S1 density-gradient and")
    print("  S2 column-gradient are degenerate because n_i = N_i / L")
    print("  and L is common to all components. The constant cancels in")
    print("  the component-to-component difference, making S1 and S2")
    print("  mathematically equivalent under the current assumption.")
    print("  To make S1 genuinely different, component-dependent sizes (L_i)")
    print("  would be required.")
    print()
    
    # Calculate required coupling for each model and size
    print("Calculating required coupling grid...")
    print()
    
    results = {
        'calculation_date': datetime.now().isoformat(),
        'system_id': dla_structure['system_id'],
        'delta_ln_a_required': delta_ln_a_required,
        'analysis_mode': 'literature_feasibility',
        'evidence_level': 'toy_only',
        'claim_allowed': False,
        'shear_law_results': {}
    }
    
    # Process each shear law
    for law_name, law_info in shear_laws.items():
        print(f"Processing {law_name}: {law_info['name']}")
        print()
        
        law_results = {
            'name': law_info['name'],
            'equation': law_info['equation'],
            'size_grid': []
        }
        
        # Process each cloud size
        for size in size_range:
            print(f"  Cloud size: {size} kpc")
            
            # Calculate features for each component
            features = []
            
            if law_name == 'S1_density_gradient':
                # Density gradient model
                rho_0 = law_info['parameters']['rho_0']['value']
                for i in range(n_components):
                    # Use column-derived density
                    N_HI = 10**component_log_n_hi[i]
                    L_cm = size * CM_PER_KPC
                    density = N_HI / L_cm
                    feature = np.log(density / rho_0)
                    features.append(feature)
                    
            elif law_name == 'S2_column_gradient':
                # Column density gradient model
                N_0 = law_info['parameters']['N_0']['value']
                for i in range(n_components):
                    N_HI = 10**component_log_n_hi[i]
                    feature = np.log(N_HI / N_0)
                    features.append(feature)
                    
            elif law_name == 'toy_power_law':
                # Toy power law model
                beta = law_info['parameters']['beta']['value']
                gamma = law_info['parameters']['gamma']['value']
                rho_0 = law_info['parameters']['rho_0']['value']
                L_0 = law_info['parameters']['L_0']['value']
                
                for i in range(n_components):
                    # Use column-derived density
                    N_HI = 10**component_log_n_hi[i]
                    L_cm = size * CM_PER_KPC
                    density = N_HI / L_cm
                    feature = (density / rho_0)**beta * (size / L_0)**gamma
                    features.append(feature)
            
            # Compute required α
            result = compute_required_alpha(features, delta_ln_a_required)
            
            # Compare to provisional prior range
            if law_name == 'S1_density_gradient':
                provisional_range = law_info['parameters']['kappa']['provisional_prior_range']
                param_name = 'kappa'
            elif law_name == 'S2_column_gradient':
                provisional_range = law_info['parameters']['lambda']['provisional_prior_range']
                param_name = 'lambda'
            elif law_name == 'toy_power_law':
                provisional_range = law_info['parameters']['alpha']['provisional_prior_range']
                param_name = 'alpha'
            
            inside_prior = (provisional_range[0] <= result['alpha_required'] <= provisional_range[1]) if result['alpha_required'] is not None else False
            
            size_result = {
                'size_kpc': size,
                'features': [float(f) for f in features],
                'max_delta_feature': result['max_delta_feature'],
                f'{param_name}_required': result['alpha_required'],
                f'{param_name}_provisional_prior_range': provisional_range,
                'inside_provisional_prior': inside_prior,
                'status': result['status']
            }
            
            law_results['size_grid'].append(size_result)
            
            print(f"    Max Δfeature: {result['max_delta_feature']:.6e}")
            print(f"    Required {param_name}: {result['alpha_required']:.6e}")
            print(f"    Provisional prior range: {provisional_range}")
            print(f"    Inside provisional prior: {inside_prior}")
            print()
        
        results['shear_law_results'][law_name] = law_results
        print("-" * 60)
        print()
    
    # Overall assessment
    print("Overall Assessment:")
    print()
    print("This is a required coupling calculation, not a calibration.")
    print("The results show what TEP coupling is required to mimic D/H.")
    print("Whether this is feasible depends on TEP theory priors.")
    print()
    print("Status labels:")
    print("  - analysis_mode: literature_feasibility")
    print("  - evidence_level: toy_only")
    print("  - claim_allowed: False")
    print()
    
    # Save results
    output_path = project_root / 'data/processed/required_coupling_calculation.json'
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"Required coupling calculation saved to {output_path}")
    print()
    print("=" * 60)
    print("STATUS: Required coupling calculation complete")
    print("Analysis mode: literature_feasibility")
    print("Evidence level: toy_only")
    print("Claim allowed: False")
    print("=" * 60)
    
    return results

if __name__ == '__main__':
    calculate_required_coupling()
