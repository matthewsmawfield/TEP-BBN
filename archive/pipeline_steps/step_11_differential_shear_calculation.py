"""
Step 11: Differential shear calculation for TEP-BBN

Calculates the differential temporal shear across the DLA structure.
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

def calculate_differential_shear():
    """
    Calculate the differential temporal shear across the DLA structure.
    
    This step:
    1. Applies TEP shear law to DLA structure
    2. Computes shear for each component
    3. Subtracts common-mode (global) shift
    4. Calculates differential shear between components
    5. Assesses physical plausibility
    """
    print("Step 11: Differential shear calculation")
    print("=" * 60)
    print("CRITICAL: This step calculates differential temporal shear.")
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
    
    # Load TEP shear law specification
    shear_law_path = project_root / 'data/processed/tep_shear_law_specification.json'
    if not shear_law_path.exists():
        print("ERROR: TEP shear law specification not found")
        print("Run step_10 to specify TEP shear law")
        return None
    
    with open(shear_law_path, 'r') as f:
        shear_law = json.load(f)
    
    print(f"System: {dla_structure['system_id']}")
    print()
    
    # Required ΔlnA
    delta_ln_a_required = dla_structure['required_delta_ln_a']
    print(f"Required ΔlnA for deuterium mimicry: {delta_ln_a_required:.6e}")
    print(f"  (82 km/s / c = 82 / 299792)")
    print()
    
    # Calculate differential shear using toy model
    print("Calculating differential temporal shear using toy model...")
    print()
    
    # Extract toy model parameters
    alpha = shear_law['toy_model']['parameters']['alpha']['value']
    beta = shear_law['toy_model']['parameters']['beta']['value']
    gamma = shear_law['toy_model']['parameters']['gamma']['value']
    rho_0 = shear_law['toy_model']['parameters']['rho_0']['value']
    L_0 = shear_law['toy_model']['parameters']['L_0']['value']
    
    # Extract DLA structure
    n_components = dla_structure['velocity_components']['n_components']
    component_strengths = dla_structure['velocity_components']['relative_strengths']
    density_range = dla_structure['physical_scales']['density_range_cm3']
    size_range = dla_structure['physical_scales']['plausible_cloud_sizes_kpc']
    
    print("Component-wise shear calculation:")
    print("Testing multiple plausible cloud sizes:")
    print()
    
    # Test each plausible cloud size
    results_by_size = {}
    for size in size_range:
        print(f"Testing cloud size: {size} kpc")
        print()
        
        # Calculate shear for each component
        component_shears = []
        for i in range(n_components):
            # Assume density scales with component strength
            density = density_range[0] + (density_range[1] - density_range[0]) * component_strengths[i]
            
            # Use the same size for all components (testing size dependence)
            scale = size
            
            # Calculate shear
            shear = alpha * (density / rho_0)**beta * (scale / L_0)**gamma
            component_shears.append(shear)
            
            print(f"  Component {i}: density={density:.2f} cm^-3, scale={size:.2f} kpc, shear={shear:.6e}")
        
        print()
        
        # Calculate common-mode (global) shift
        common_mode = np.mean(component_shears)
        print(f"Common-mode shift: {common_mode:.6e}")
        print()
        
        # Calculate differential shear (subtract common-mode)
        print("Differential shear (after common-mode subtraction):")
        differential_shears = []
        for i in range(n_components):
            diff_shear = component_shears[i] - common_mode
            differential_shears.append(diff_shear)
            print(f"  Component {i}: ΔlnA = {diff_shear:.6e}")
        
        print()
        
        # Calculate maximum differential shear between components
        max_differential_shear = 0
        for i in range(n_components - 1):
            diff = abs(differential_shears[i+1] - differential_shears[i])
            max_differential_shear = max(max_differential_shear, diff)
        
        print(f"Maximum differential shear: {max_differential_shear:.6e}")
        print()
        
        # Compare to required ΔlnA
        print(f"Required ΔlnA: {delta_ln_a_required:.6e}")
        print(f"Ratio (max differential / required): {max_differential_shear / delta_ln_a_required:.6f}")
        print()
        
        # Store results for this size
        results_by_size[str(size)] = {
            'component_shears': [float(s) for s in component_shears],
            'common_mode': float(common_mode),
            'differential_shears': [float(s) for s in differential_shears],
            'max_differential_shear': float(max_differential_shear),
            'ratio_to_required': float(max_differential_shear / delta_ln_a_required)
        }
        
        # Assess feasibility for this size
        magnitude_feasible = abs(max_differential_shear - delta_ln_a_required) / delta_ln_a_required < 1.0
        print(f"Feasibility for size {size} kpc: {'✓ Feasible' if magnitude_feasible else '✗ Not feasible'}")
        print()
        print("-" * 60)
        print()
    
    # Find best size
    best_size = None
    best_ratio = 0
    for size, results in results_by_size.items():
        if results['ratio_to_required'] > best_ratio and results['ratio_to_required'] < 10.0:
            best_ratio = results['ratio_to_required']
            best_size = float(size)
    
    print("Summary:")
    print(f"Best cloud size: {best_size} kpc")
    print(f"Best ratio to required: {best_ratio:.6f}")
    print()
    
    # Overall assessment
    print("Overall Assessment:")
    print()
    print("Toy Model Results:")
    print(f"  Required ΔlnA: {delta_ln_a_required:.6e}")
    print(f"  Best achieved ΔlnA: {results_by_size[str(best_size)]['max_differential_shear']:.6e}")
    print(f"  Ratio: {results_by_size[str(best_size)]['ratio_to_required']:.6f}")
    print()
    
    if results_by_size[str(best_size)]['ratio_to_required'] >= 1.0:
        print("  ✓ Toy model can produce required differential shear")
        print("  ✓ With appropriate cloud size assumption")
    else:
        print("  ✗ Toy model underproduces required differential shear")
        print("  ✗ Even with best cloud size assumption")
    print()
    
    print("IMPORTANT: This is a TOY MODEL result.")
    print("  - Assumes ad hoc power-law shear law")
    print("  - Assumes arbitrary cloud sizes")
    print("  - Assumes arbitrary density scaling")
    print("  - NOT a TEP-derived prediction")
    print()
    print("  Do NOT interpret as TEP rejection.")
    print("  This is a failed toy implementation, not a physical result.")
    print()
    
    # Create results
    differential_shear_results = {
        'calculation_date': datetime.now().isoformat(),
        'system_id': dla_structure['system_id'],
        'status': 'toy_model_calculation_complete',
        
        'required_delta_ln_a': delta_ln_a_required,
        'results_by_size': results_by_size,
        'best_size': best_size,
        'best_ratio': best_ratio,
        
        'overall_feasible': bool(results_by_size[str(best_size)]['ratio_to_required'] >= 1.0),
        
        'sign_determined': False,
        'sign_value': None,
        
        'notes': 'This is a toy model calculation. Do NOT interpret as TEP rejection. Requires TEP-derived shear law and actual absorber geometry.'
    }
    
    # Save results
    output_path = project_root / 'data/processed/differential_shear_calculation.json'
    with open(output_path, 'w') as f:
        json.dump(differential_shear_results, f, indent=2)
    
    print(f"Differential shear calculation saved to {output_path}")
    print()
    print("=" * 60)
    print("STATUS: Toy model calculation complete")
    print(f"Overall feasibility: {'Feasible' if differential_shear_results['overall_feasible'] else 'Not feasible'}")
    print("NOTE: This is a toy model, not a TEP rejection")
    print("=" * 60)
    
    return differential_shear_results

if __name__ == '__main__':
    calculate_differential_shear()
