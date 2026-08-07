import re
from pathlib import Path
import sys

script_dir = Path(__file__).parent
project_root = script_dir.parent.parent
sys.path.insert(0, str(project_root))

def parse_vpfit_to_table(filepath):
    lines_data = []
    
    with open(filepath, 'r') as f:
        for line_num, line in enumerate(f, 1):
            if line.startswith(' H I') or line.startswith(' D I'):
                parts = line.split()
                if len(parts) < 7:
                    continue
                    
                species = parts[0] + ' ' + parts[1]
                z_raw = parts[2]
                b_raw = parts[4]
                logN_raw = parts[6]
                
                z_match = re.match(r'([0-9\.]+)([a-zA-Z]*)', z_raw)
                b_match = re.match(r'([0-9\.]+)([a-zA-Z]*)', b_raw)
                logN_match = re.match(r'([0-9\.\-]+)([a-zA-Z]*)', logN_raw)
                
                z = float(z_match.group(1)) if z_match else float(z_raw)
                z_tie = z_match.group(2) if z_match else ""
                
                b = float(b_match.group(1)) if b_match else float(b_raw)
                b_tie = b_match.group(2) if b_match else ""
                
                logN = float(logN_match.group(1)) if logN_match else float(logN_raw)
                logN_tie = logN_match.group(2) if logN_match else ""
                
                # Relative velocity to z=2.5042
                v_rel = 299792.458 * (z - 2.5042) / (1.0 + 2.5042)
                
                lines_data.append({
                    'line_num': line_num,
                    'species': species,
                    'z': z,
                    'v_rel': v_rel,
                    'b': b,
                    'logN': logN,
                    'z_tie': z_tie,
                    'b_tie': b_tie,
                    'logN_tie': logN_tie,
                    'raw': line.strip()
                })
                
    # Output to markdown
    out_md = project_root / 'data' / 'processed' / 'Q1009_vpfit_components.md'
    with open(out_md, 'w') as f:
        f.write("| Line | Species | z | v_rel (km/s) | b (km/s) | b_tie | logN | logN_tie | z_tie |\n")
        f.write("|------|---------|---|-------------:|---------:|-------|------|----------|-------|\n")
        for d in lines_data:
            f.write(f"| {d['line_num']} | {d['species']} | {d['z']:.6f} | {d['v_rel']:.1f} | {d['b']:.2f} | {d['b_tie']} | {d['logN']:.3f} | {d['logN_tie']} | {d['z_tie']} |\n")
            
    print(f"Extracted {len(lines_data)} components to {out_md}")

if __name__ == '__main__':
    vpfit = project_root / 'data' / 'literature_components' / 'model_1a.26'
    parse_vpfit_to_table(vpfit)
