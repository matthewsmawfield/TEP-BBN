import json
from pathlib import Path
import math

def generate_report():
    project_root = Path('/Users/matthewsmawfield/www/Temporal Equivalence Principle/TEP-BBN')
    json_path = project_root / 'data/processed/q1009_reduced_convergence_audit_results.json'
    
    with open(json_path) as f:
        results = json.load(f)
        
    report = []
    report.append("# Bounded Convergence Adjudication Report\n")
    report.append("This report evaluates the `dynesty` nested sampler convergence under the strictly frozen validation criteria.\n")
    
    # Group by data_seed and nlive
    groups = {}
    for r in results:
        key = (r['data_seed'], r['nlive'])
        if key not in groups:
            groups[key] = []
        groups[key].append(r)
        
    report.append("## Raw Audit Results\n")
    report.append("| Data seed | nlive | Sampler seed | Classification | $\Delta\\log Z$ | $\\alpha$ mean | $\\alpha$ std | Lower edge | Upper edge | max logL | null logL | ESS | ncall |")
    report.append("| --------- | ----: | -----------: | -------------- | ----: | -----: | ----: | ---------- | ---------- | -----------: | --: | --: | --: |")
    
    for (dseed, nlive), subset in sorted(groups.items()):
        for r in sorted(subset, key=lambda x: x['sampler_seed']):
            report.append(f"| {r['data_seed']} | {r['nlive']} | {r['sampler_seed']} | {r['classification']} | {r['delta_logz']:.2f} | {r['alpha_mean']:.6f} | {r['alpha_std']:.6f} | {r['at_lower']} | {r['at_upper']} | {r['full_max_logl']:.2f} | {r['null_max_logl']:.2f} | {r['full_eff_samples']:.0f} | {r['ncall']} |")
            
    report.append("\n## Frozen Criteria Evaluation\n")
    
    for (dseed, nlive), subset in sorted(groups.items()):
        report.append(f"### Data Seed {dseed}, `nlive`={nlive}")
        
        # 1. Classification Stability
        classifications = [r['classification'] for r in subset]
        stable_classification = len(set(classifications)) == 1
        report.append(f"- **Classification Stability**: {'PASS' if stable_classification else 'FAIL'} ({classifications})")
        
        # 2. Evidence Stability
        logzs = [r['full_logz'] for r in subset]
        logz_errs = [r['full_logzerr'] for r in subset]
        evidence_stable = True
        max_diff = 0
        for i in range(len(logzs)):
            for j in range(i+1, len(logzs)):
                diff = abs(logzs[i] - logzs[j])
                tol = max(2.0, 2 * math.sqrt(logz_errs[i]**2 + logz_errs[j]**2))
                if diff > max_diff:
                    max_diff = diff
                if diff > tol:
                    evidence_stable = False
        report.append(f"- **Evidence Stability (M2)**: {'PASS' if evidence_stable else 'FAIL'} (Max diff: {max_diff:.2f})")
        
        # 3. Delta logZ Stability
        deltas = [r['delta_logz'] for r in subset]
        delta_spread = max(deltas) - min(deltas)
        # Check against the theoretical tolerance
        null_errs = [r['null_logzerr'] for r in subset]
        delta_stable = True
        max_delta_diff = 0
        for i in range(len(deltas)):
            for j in range(i+1, len(deltas)):
                diff = abs(deltas[i] - deltas[j])
                # Combined error of both M2 and M3
                err_i = math.sqrt(logz_errs[i]**2 + null_errs[i]**2)
                err_j = math.sqrt(logz_errs[j]**2 + null_errs[j]**2)
                tol = max(2.0, 2 * math.sqrt(err_i**2 + err_j**2))
                if diff > max_delta_diff:
                    max_delta_diff = diff
                if diff > tol:
                    delta_stable = False
        
        report.append(f"- **Delta logZ Stability**: {'PASS' if delta_stable else 'FAIL'} (Max diff: {max_delta_diff:.2f})")
        
        # 4. Posterior Edges
        edges = [(r['at_lower'] or r['at_upper']) for r in subset]
        edge_stable = len(set(edges)) == 1
        report.append(f"- **Edge Flag Stability**: {'PASS' if edge_stable else 'FAIL'} ({edges})")
        
        report.append("")
        
    out_path = project_root / 'data/processed/adjudication_report.md'
    with open(out_path, 'w') as f:
        f.write('\n'.join(report))
    print(f"Report written to {out_path}")

if __name__ == '__main__':
    generate_report()
