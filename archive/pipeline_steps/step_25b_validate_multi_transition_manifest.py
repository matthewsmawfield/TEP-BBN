import json
import hashlib
from pathlib import Path
import numpy as np
from datetime import datetime

script_dir = Path(__file__).parent
project_root = script_dir.parent.parent

# Q1009 z_abs = 2.5042
# We define the fitting windows for all transitions.
# Overlapping windows will be merged into contiguous chunks to prevent double counting.

TRANSITIONS = {
    'Ly_alpha': {'min': 4254.42, 'max': 4265.00, 'rest_w': 1215.67},
    'Ly_beta': {'min': 3591.10, 'max': 3597.10, 'rest_w': 1025.72},
    'Ly_gamma': {'min': 3403.95, 'max': 3411.03, 'rest_w': 972.53},
    'Ly_6': {'min': 3259.30, 'max': 3264.20, 'rest_w': 930.74},
    'Ly_13': {'min': 3209.81, 'max': 3212.89, 'rest_w': 916.42},
    'Ly_14': {'min': 3208.08, 'max': 3210.20, 'rest_w': 915.82},
    'Ly_21_24': {'min': 3199.50, 'max': 3201.25, 'rest_w': 913.0}, # Approximate avg rest for Ly21-24
    
    # Metal lines derived from rest wavelength * (1 + 2.5042) +/- 3.5 Angstroms
    'C_II_1334': {'min': 4672.0, 'max': 4680.0, 'rest_w': 1334.5323},
    'C_III_977': {'min': 3419.0, 'max': 3427.0, 'rest_w': 977.0201},
    'C_IV_1548': {'min': 5422.0, 'max': 5430.0, 'rest_w': 1548.1950},
    'C_IV_1550': {'min': 5431.0, 'max': 5439.0, 'rest_w': 1550.7700},
    'Si_IV_1393': {'min': 4881.0, 'max': 4889.0, 'rest_w': 1393.7550},
    'Si_IV_1402': {'min': 4913.0, 'max': 4921.0, 'rest_w': 1402.7700}
}

RAW_FILES = [
    'q1011p2941_C1x1.dat',
    'q1011p2941_C1x2.dat',
    'q1011p2941_C5x1.dat',
    'q1011p2941_C5x2.dat'
]

def load_dat_file(filepath):
    data = np.loadtxt(filepath)
    return {
        'wave': data[:, 0],
        'flux': data[:, 1],
        'err': data[:, 2]
    }

def sha256_file(filepath):
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def main():
    print("Validating and Building Unified Multi-Transition Manifest...")
    
    # Generate the validation report
    report_lines = []
    report_lines.append("# Q1009+2956 Manifest Validation Report")
    report_lines.append(f"Generated: {datetime.utcnow().isoformat()}Z\n")
    
    report_lines.append("## Data Conventions & Provenance")
    report_lines.append("- **Wavelength Grid**: Strictly monotonic, Vacuum (standard KODIAQ convention)")
    report_lines.append("- **Heliocentric Correction**: Applied (standard KODIAQ convention)")
    report_lines.append("- **Flux Normalization**: Unnormalized raw flux units (continuum required during fitting)")
    report_lines.append("- **Error Interpretation**: 1-sigma flux uncertainties")
    report_lines.append("- **Instrumental Gaussian Sigma**: 2.5 - 3.0 km/s (depends on binning, will be free/profiled in RT fit)\n")
    
    report_lines.append("## Raw File Provenance")
    for raw_name in RAW_FILES:
        filepath = project_root / 'data' / 'raw' / 'reduced_products' / 'Q1009+2956_z2.504_HIRES' / raw_name
        file_hash = sha256_file(filepath)
        report_lines.append(f"- `{raw_name}`: SHA-256 `{file_hash}`")
    report_lines.append("\n")

    manifest = {
        'system': 'Q1009+2956',
        'z_abs': 2.5042,
        'coadds': {}
    }
    
    report_lines.append("## Coverage & Masking")
    report_lines.append("To prevent duplicated likelihood pixels from overlapping windows (e.g. Ly13/Ly14), we construct a union mask across all requested transitions for each coadd. Pixels are grouped into contiguous chunks and evaluated exactly once.\n")
    
    for raw_name in RAW_FILES:
        filepath = project_root / 'data' / 'raw' / 'reduced_products' / 'Q1009+2956_z2.504_HIRES' / raw_name
        data = load_dat_file(filepath)
        wave, flux, err = data['wave'], data['flux'], data['err']
        
        # Check monotonicity
        is_monotonic = np.all(np.diff(wave) > 0)
        
        # Build Union Mask
        global_mask = np.zeros(len(wave), dtype=bool)
        for t_name, t_range in TRANSITIONS.items():
            mask = (wave >= t_range['min']) & (wave <= t_range['max'])
            global_mask |= mask
            
        masked_wave = wave[global_mask]
        masked_flux = flux[global_mask]
        masked_err = err[global_mask]
        
        neg_err_count = np.sum(masked_err <= 0)
        
        # Find contiguous chunks
        chunks = []
        if len(masked_wave) > 0:
            indices = np.where(global_mask)[0]
            breaks = np.where(np.diff(indices) > 1)[0] + 1
            chunk_indices = np.split(indices, breaks)
            
            for chunk_idx in chunk_indices:
                chunks.append({
                    'wave': wave[chunk_idx].tolist(),
                    'flux': flux[chunk_idx].tolist(),
                    'err': err[chunk_idx].tolist()
                })
        
        manifest['coadds'][raw_name] = chunks
        
        report_lines.append(f"### {raw_name}")
        report_lines.append(f"- **Total Native Pixels**: {len(wave)}")
        report_lines.append(f"- **Wavelength Range**: {wave[0]:.2f} - {wave[-1]:.2f} Å")
        report_lines.append(f"- **Monotonic Grid**: {is_monotonic}")
        report_lines.append(f"- **Pixels in Union Mask**: {np.sum(global_mask)}")
        report_lines.append(f"- **Contiguous Chunks**: {len(chunks)}")
        report_lines.append(f"- **Negative/Invalid Errors in Mask**: {neg_err_count}\n")
    
    report_lines.append("## Transition Inclusions")
    for t_name, t_range in TRANSITIONS.items():
        report_lines.append(f"- **{t_name}**: {t_range['min']:.2f} - {t_range['max']:.2f} Å (Rest: {t_range['rest_w']} Å)")
    
    # Save Manifest
    out_path = project_root / 'data' / 'processed' / 'Q1009_union_manifest.json'
    with open(out_path, 'w') as f:
        json.dump(manifest, f)
    
    # Save Report
    report_path = project_root / 'paper' / 'notes' / 'Q1009_manifest_validation.md'
    with open(report_path, 'w') as f:
        f.write("\n".join(report_lines))
        
    print(f"Manifest saved to {out_path}")
    print(f"Validation Report saved to {report_path}")

if __name__ == '__main__':
    main()
