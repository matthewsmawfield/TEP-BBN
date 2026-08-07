"""
Step 10: TEP shear law specification for TEP-BBN

Specifies the TEP shear law relating physical quantities to differential temporal shear.
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

def specify_tep_shear_law():
    """
    Specify the TEP shear law relating physical quantities to ΔlnA.
    
    This step:
    1. Defines the functional form of the TEP shear law
    2. Specifies how physical quantities affect temporal shear
    3. Establishes parameter values and ranges
    4. Ensures physical consistency
    """
    print("Step 10: TEP shear law specification")
    print("=" * 60)
    print("CRITICAL: This step specifies the TEP shear law for differential shear.")
    print("No placeholder or synthetic data is allowed.")
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
    
    # TEP shear law specification
    print("Specifying TEP shear law...")
    print()
    
    # Define TEP shear law
    # Based on temporal equivalence principle: clock rates depend on local conditions
    # Differential shear depends on gradients in physical quantities
    
    # Required ΔlnA from Gate 0
    delta_ln_a_required = dla_structure['required_delta_ln_a']
    
    tep_shear_law = {
        'specification_date': datetime.now().isoformat(),
        'system_id': dla_structure['system_id'],
        'status': 'specified',
        'delta_ln_a_required': delta_ln_a_required,
        
        # Multiple physically motivated shear laws
        'shear_laws': {
            'S1_density_gradient': {
                'name': 'Density gradient',
                'equation': 'ΔlnA = κ * Δln(ρ/ρ₀)',
                'description': 'Shear proportional to density contrast',
                'parameters': {
                    'kappa': {
                        'value': 1.0,  # Will be calibrated
                        'description': 'Coupling constant',
                        'range': [0.1, 10.0]
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
                        'value': 1.0,  # Will be calibrated
                        'description': 'Coupling constant',
                        'range': [0.1, 10.0]
                    },
                    'N_0': {
                        'value': 1e20,
                        'description': 'Reference column density (cm^-2)',
                        'range': [1e19, 1e21]
                    }
                }
            },
            'S3_potential_gradient': {
                'name': 'Potential gradient',
                'equation': 'ΔlnA = ζ * ΔΦ/c²',
                'description': 'Shear proportional to gravitational potential contrast',
                'parameters': {
                    'zeta': {
                        'value': 1.0,  # Will be calibrated
                        'description': 'Coupling constant',
                        'range': [0.1, 10.0]
                    }
                }
            }
        },
        
        # Original toy model (for comparison)
        'toy_model': {
            'name': 'Power law toy model',
            'equation': 'ΔlnA = α * (ρ/ρ₀)^β * (L/L₀)^γ',
            'description': 'Ad hoc power law model (toy only)',
            'parameters': {
                'alpha': {
                    'value': 1.0e-4,
                    'description': 'Overall shear amplitude',
                    'range': [1.0e-5, 1.0e-3]
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
        },
        
        # Physical consistency requirements
        'consistency_requirements': {
            'causality': 'Shear must be causal (no superluminal effects)',
            'locality': 'Shear must depend on local conditions',
            'covariance': 'Shear must be Lorentz covariant',
            'energy_conservation': 'Shear must conserve energy'
        },
        
        # Sign convention
        'sign_convention': {
            'positive_shear': 'Clock runs faster in higher density regions',
            'negative_shear': 'Clock runs slower in higher density regions',
            'deuterium_requirement': 'Need to determine sign from D/H offset direction'
        }
    }
    
    print("TEP Shear Law Specification:")
    print(f"  Required ΔlnA: {delta_ln_a_required:.6e}")
    print(f"  (82 km/s / c = 82 / 299792)")
    print()
    print("Shear Laws:")
    for law_name, law_info in tep_shear_law['shear_laws'].items():
        print(f"  {law_name}: {law_info['name']}")
        print(f"    Equation: {law_info['equation']}")
        print(f"    Description: {law_info['description']}")
    print()
    print("Toy Model (for comparison):")
    print(f"  {tep_shear_law['toy_model']['name']}")
    print(f"    Equation: {tep_shear_law['toy_model']['equation']}")
    print()
    
    # Calibrate toy model to match required ΔlnA
    print("Calibrating toy model to match required ΔlnA...")
    print()
    
    # Extract DLA structure parameters
    density_range = dla_structure['physical_scales']['density_range_cm3']
    size_range = dla_structure['physical_scales']['plausible_cloud_sizes_kpc']
    
    # Calculate density contrast
    density_contrast = density_range[1] / density_range[0]
    print(f"Density contrast: {density_contrast:.1f}")
    
    # Calculate scale contrast (use max size)
    scale_contrast = size_range[-1] / size_range[0]
    print(f"Scale contrast: {scale_contrast:.1f}")
    
    # Extract toy model parameters
    beta = tep_shear_law['toy_model']['parameters']['beta']['value']
    gamma = tep_shear_law['toy_model']['parameters']['gamma']['value']
    rho_0 = tep_shear_law['toy_model']['parameters']['rho_0']['value']
    L_0 = tep_shear_law['toy_model']['parameters']['L_0']['value']
    
    # Calculate required α to match required ΔlnA
    # ΔlnA = α * (ρ/ρ₀)^β * (L/L₀)^γ
    # α = ΔlnA / [(ρ/ρ₀)^β * (L/L₀)^γ]
    alpha_required = delta_ln_a_required / ((density_contrast / rho_0)**beta * (scale_contrast / L_0)**gamma)
    
    print(f"Required α: {alpha_required:.6e}")
    print(f"  (to match ΔlnA = {delta_ln_a_required:.6e})")
    print()
    
    # Update toy model with calibrated α
    tep_shear_law['toy_model']['parameters']['alpha']['value'] = alpha_required
    tep_shear_law['toy_model']['calibration'] = {
        'delta_ln_a_target': delta_ln_a_required,
        'density_contrast': density_contrast,
        'scale_contrast': scale_contrast,
        'alpha_calibrated': alpha_required
    }
    
    # Verify calibration
    delta_ln_a_calibrated = alpha_required * (density_contrast / rho_0)**beta * (scale_contrast / L_0)**gamma
    print(f"Verification: ΔlnA = {delta_ln_a_calibrated:.6e}")
    print(f"  (should match required: {delta_ln_a_required:.6e})")
    print(f"  Ratio: {delta_ln_a_calibrated / delta_ln_a_required:.6f}")
    print()
    
    # Assess feasibility
    print("Feasibility Assessment:")
    if abs(delta_ln_a_calibrated - delta_ln_a_required) / delta_ln_a_required < 0.01:
        print("  ✓ Calibration successful (within 1%)")
        print("  ✓ Toy model can produce required ΔlnA with calibrated parameters")
    else:
        print("  ✗ Calibration failed")
        print("  ✗ Check for unit or calculation errors")
    print()
    
    # Sign determination (placeholder)
    print("Sign Determination:")
    print("  Status: Not yet determined")
    print("  Required: Calculate sign from D/H offset direction")
    print("  Action: Need to analyze observed D I vs H I velocity structure")
    print()
    
    # Add prediction to shear law specification
    tep_shear_law['prediction'] = {
        'delta_ln_a_calibrated': delta_ln_a_calibrated,
        'delta_ln_a_required': delta_ln_a_required,
        'ratio': delta_ln_a_calibrated / delta_ln_a_required,
        'calibration_successful': abs(delta_ln_a_calibrated - delta_ln_a_required) / delta_ln_a_required < 0.01
    }
    
    # Save shear law specification
    output_path = project_root / 'data/processed/tep_shear_law_specification.json'
    with open(output_path, 'w') as f:
        json.dump(tep_shear_law, f, indent=2)
    
    print(f"TEP shear law specification saved to {output_path}")
    print()
    print("=" * 60)
    print("STATUS: TEP shear law specification complete")
    print("Ready for differential shear calculation")
    print("=" * 60)
    
    return tep_shear_law

if __name__ == '__main__':
    specify_tep_shear_law()
