# TEP-BBN Pipeline

## Clean Run

To reproduce all results from a clean state:

```bash
cd "$(dirname "$0")/.."
rm -rf results/*.json results/*.csv results/figures/*
python -m scripts.steps.step_01_embedding
python -m scripts.steps.step_02_q1009
python -m scripts.steps.step_03_significance
python -m scripts.steps.step_04_prior
python -m scripts.steps.step_05_thermodynamics
```

Or run individually:

```bash
python scripts/steps/step_03_significance.py
```

## Dependencies

- Python 3.11+
- NumPy, SciPy
- CLASS Python bindings (`external/class/python/classy.pyx` built)
- AlterBBN (`external/AlterBBN/` built)

## Outputs

All step results are written to `results/` as JSON and CSV.
Key results include embedding separations (step_01), Voigt fits for Q1009+2956 (step_02), Monte Carlo significance tests (step_03), and thermodynamic exposure constraints (step_05).

## Audit

Run the automated integrity audit:

```bash
python scripts/utils/full_audit.py
python scripts/utils/check2_audit.py
```
