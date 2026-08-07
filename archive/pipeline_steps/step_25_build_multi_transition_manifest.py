import json
from pathlib import Path
import numpy as np

script_dir = Path(__file__).parent
project_root = script_dir.parent.parent

# Define the published transitions for Q1009+2956 (z_abs = 2.504)
# (From Zavarygin et al. 2018, MNRAS 477, 5536)
TRANSITIONS = {
    'Ly_alpha': {'min': 4254.42, 'max': 4265.00},
    'Ly_beta': {'min': 3591.10, 'max': 3597.10},
    'Ly_gamma': {'min': 3403.95, 'max': 3411.03},
    'Ly_6': {'min': 3259.30, 'max': 3264.20},
    'Ly_13': {'min': 3209.81, 'max': 3212.89},
    'Ly_14': {'min': 3208.08, 'max': 3210.20},
    'Ly_21_24': {'min': 3199.50, 'max': 3201.25}
}

RAW_FILES = [
    'q1011p2941_C1x1.dat',
    'q1011p2941_C1x2.dat',
    'q1011p2941_C5x1.dat',
    'q1011p2941_C5x2.dat'
]

def load_dat_file(filepath):
    # The file has 3 columns: wave, flux, err
    data = np.loadtxt(filepath)
    return {
        'wave': data[:, 0],
        'flux': data[:, 1],
        'err': data[:, 2]
    }

def build_manifest():
    print("Building Multi-Transition Manifest for Q1009+2956")
    manifest = {
        'system': 'Q1009+2956',
        'z_abs': 2.504,
        'transitions': {}
    }
    
    for t_name, t_range in TRANSITIONS.items():
        print(f"Processing transition: {t_name}")
        manifest['transitions'][t_name] = []
        
        for raw_name in RAW_FILES:
            filepath = project_root / 'data' / 'raw' / 'reduced_products' / 'Q1009+2956_z2.504_HIRES' / raw_name
            try:
                data = load_dat_file(filepath)
            except Exception as e:
                print(f"  Warning: Could not load {raw_name}: {e}")
                continue
                
            # Check coverage
            w_min, w_max = data['wave'][0], data['wave'][-1]
            if w_min > t_range['min'] or w_max < t_range['max']:
                print(f"  Warning: {raw_name} does not fully cover {t_name} ({t_range['min']}-{t_range['max']}). File covers {w_min:.2f}-{w_max:.2f}")
                continue
                
            # Extract
            mask = (data['wave'] >= t_range['min']) & (data['wave'] <= t_range['max'])
            if np.sum(mask) == 0:
                print(f"  Warning: No pixels found in {raw_name} for {t_name}")
                continue
                
            w_sub = data['wave'][mask].tolist()
            f_sub = data['flux'][mask].tolist()
            e_sub = data['err'][mask].tolist()
            
            # Simple continuum estimate (mean of upper quartile)
            # This is extremely naive and will be replaced by actual C(lambda) later
            sorted_f = np.sort(np.array(f_sub))
            cont_guess = float(np.median(sorted_f[int(0.75*len(sorted_f)):])) if len(sorted_f) > 4 else 1.0
            
            spec_entry = {
                'coadd_id': raw_name.replace('.dat', ''),
                'wave': w_sub,
                'flux': f_sub,
                'err': e_sub,
                'continuum_guess': cont_guess
            }
            manifest['transitions'][t_name].append(spec_entry)
            print(f"  Added {raw_name} to {t_name} ({len(w_sub)} pixels)")

    out_path = project_root / 'data' / 'processed' / 'Q1009+2956_multi_transition_manifest.json'
    with open(out_path, 'w') as f:
        json.dump(manifest, f)
    print(f"\nManifest saved to {out_path}")

if __name__ == '__main__':
    build_manifest()
