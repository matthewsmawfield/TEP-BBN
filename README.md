# Temporal Equivalence Principle: Dynamical Proper Time and the Illusion of Primordial Deuterium

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21841148.svg)](https://doi.org/10.5281/zenodo.21841148)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

![TEP-BBN: Dynamical Proper Time and the Illusion of Primordial Deuterium](site/public/image.webp)

**Author:** Matthew Lukin Smawfield  
**Version:** v0.2 (Dubai)  
**First published:** 12 August 2026  
**Last updated:** 28 August 2026  
**Status:** Preprint (Open for Collaboration)  
**DOI:** [10.5281/zenodo.21841148](https://doi.org/10.5281/zenodo.21841148)  
**Website:** [https://mlsmawfield.com/tep/bbn](https://mlsmawfield.com/tep/bbn)  
**Paper Series:** TEP Series: Paper 29 (Dynamical Proper Time and the Illusion of Primordial Deuterium)

## Abstract

The standard inference from high-redshift deuterium to a uniquely primordial hot-BBN origin depends on both isotope identifiability and the interpretation of redshift as spatial expansion. Both assumptions are examined within the Temporal Equivalence Principle (TEP). Using physical H I and D I atomic data with mass-scaled Doppler parameters, the isotope identifiability is found to be regime-dependent: for thermally-dominated gas the H and D Voigt profiles differ by $0.52\sigma$ at Keck/HIRES resolution (actual D column), while for turbulence-dominated gas ($b_{\rm turb} \gg b_{\rm therm}$) the discrepancy falls to $0.0002\sigma$. The Q1009 D/H absorber components are mixed regime ($b_{\rm turb}/b_{\rm therm} \approx 1.87$ from the Gate 2 fit: $T_K = 2000$\,K, $b_{\rm turb} = 10.7$\,km/s), giving a discrepancy of $0.10\sigma$ — far below conventional detectability. A nested-hypothesis analysis of three benchmark D/H quasar sightlines---Q1009+2956 (Keck/HIRES, $z=2.5042$), PKS\,1937$-$101 (ESPRESSO, $z=3.572$), and J1332$+$0052 (UVES+HIRES, $z=3.421$)---with the shared Voigt architecture held fixed across hypotheses so that the resulting statistic can be calibrated exactly, finds that the unrestricted-H optimum is preferred over true-D for all three sightlines ($\Delta\ln L=12.02$, $T=24.04$ for Q1009+2956; $T=85.41$ for PKS\,1937$-$101; $T=141.56$ for J1332$+$0052). Calibration against 1000 true-D Monte Carlo realizations of the identical statistic yields the significance levels reported below. The parent-reassignment test---which allows D to select the most favorable parent from all H I components within $\pm 1000$ km/s with $\log N_{\rm HI}$ within 2 dex of the strongest component---gives $T_{\rm parent}$: Q1009 $24.04$, PKS\,1937 $30.63$, J1332 $52.51$. Monte Carlo calibration on 1000 true-D realizations yields $p_{\rm std} = 0.001$ and $p_{\rm parent} = 0.001$ for Q1009+2956; $p_{\rm std} = 0.002$ and $p_{\rm parent} = 0.002$ for PKS\,1937$-$101; $p_{\rm std} = 0.002$ and $p_{\rm parent} = 0.004$ for J1332$+$0052. All three sightlines show strong evidence for TEP under both the standard and parent-reassignment statistics.

Keywords: temporal equivalence principle, deuterium abundance, isotopic line identification, temporal shear, absorption-line spectroscopy, Lyman-limit systems, Big Bang nucleosynthesis, cosmology, TEP, Proper-Time Transport

## Purpose

TEP-BBN is a research-grade data pipeline testing whether primordial deuterium abundance measurements are invariant under the isochrony axiom of the Temporal Equivalence Principle framework. It provides:

- **Monte Carlo hypothesis testing** of the hallmark Q1009+2956 absorption system.
- **Voigt-profile fitting** for isotopic line shifts and temporal-shear models.
- **Symbolic proof** of Planck spectrum preservation under temporal transport.
- **Analytic derivation** of the TEP non-FLRW closure, helium equilibrium, and opacity boundary.

## Installation

```bash
# Clone repository
git clone https://github.com/matthewsmawfield/TEP-BBN
cd TEP-BBN

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies strictly
pip install -r requirements-lock.txt
```

## Pipeline Execution

### Full Pipeline
The core analysis is orchestrated by `run_pipeline.py`, which executes 8 sequential "gates":
```bash
python scripts/run_pipeline.py
```

This master script performs:
1. **Gate 1**: Embedding the Q1009 transition manifold.
2. **Gate 2**: Generating and fitting standard parent-tied $D$ and displaced free-$H$ components.
3. **Gate 3**: Executing a 1000-realization Monte Carlo significance test.
4. **Gate 4**: Symbolic proof of the TEP absorber field blueward velocity sign.
5. **Gate 4B**: Quantitative amplitude test with frozen $\beta_A = -1.0$ and ionisation-corrected Q1009+2956 observables.
6. **Gate 5**: Symbolic proof of Planck spectrum preservation under temporal transport.
7. **Gate 6**: Primordial helium synthesis via baryonic cycling and temporal-horizon metal sequestration.
8. **Gate 7**: Analytical proof of divergent optical depth in the static spatial geometry (Opacity Boundary).
9. **Gate 8**: Light-element network and convergence constraints.

The output metrics, structural fits, and physical derivations are dumped as JSON ledgers into the `results/` directory, terminating with a cryptographic `checksums_sha256.json` file.

### Manuscript Generation
To rebuild the Markdown and high-quality PDF manuscript from the HTML components and mathematical derivations:

```bash
python scripts/generate_site_pdf.py
```
*(Requires a running Chrome/Chromium installation for Headless PDF rendering).*

## Key Results (v0.2)

1. **Statistical Non-Identifiability**: Subjected to rigorously nested hypothesis testing across three benchmark sightlines (Q1009+2956, PKS 1937$-$101, J1332$+$0052), an unrestricted hydrogen model fits the data with statistical dominance under both the canonical-parent statistic ($p_{\rm std} = 0.001$ for Q1009, $p_{\rm std} = 0.002$ for PKS 1937$-$101, $p_{\rm std} = 0.002$ for J1332$+$0052) and the conservative parent-reassignment statistic ($p_{\rm parent} = 0.001$ for Q1009, $p_{\rm parent} = 0.002$ for PKS 1937$-$101, $p_{\rm parent} = 0.004$ for J1332$+$0052). All three sightlines show strong evidence for TEP under both statistics, with discrimination concentrated in the Ly$\alpha$ transition.
2. **TEP Absorber Field Sign**: The blueward displacement sign is deterministically derived from conformal core-edge geometry (Gate 4, sign proof). The conformal amplitude is quantified with the frozen bare coupling $\beta_A = -1.0$ and ionisation-corrected Q1009+2956 observables (Gate 4B); the full amplitude is a falsifiable prediction of the environmental operator $\mathcal{S}_\Sigma(\mathcal{E})$.
3. **Planck Spectral Preservation**: A symbolic proof demonstrates that any emitted Planck spectrum is strictly preserved in form under temporal transport, without requiring a singular early phase or FLRW geometric expansion.
4. **Helium-4 Equilibrium**: The helium-4 mass fraction ($Y_{\rm eq} = 0.247$) emerges as the equilibrium of baryonic-cycling reaction flows under temporal-horizon metal sequestration.
5. **Opacity Boundary**: In the static spatial geometry, the line-of-sight optical depth diverges at high redshift (proven via constant $n_e$ and divergent path length $\ell(z) \to \infty$), creating an observable boundary without a physical plasma wall.

## Project Structure

```
TEP-BBN/
├── configs/              # Run configurations and YAML priors
├── logs/                 # Execution logs
├── scripts/              # Analysis pipeline
│   ├── lib/                 # Core logic, likelihoods, and radiative transfer
│   ├── steps/               # Individual pipeline gates (01-08)
│   └── run_pipeline.py      # Full pipeline runner
├── results/              # Pipeline outputs
│   ├── checksums_sha256.json
│   └── *.json               # Gate ledgers and results
├── site/                 # Static-site manuscript builder
│   ├── components/          # HTML sections
│   └── build.js             # Site compiler
└── 29-TEP-BBN-v0.2-Dubai.md # Generated Markdown manuscript
```

## Citation

If using this pipeline, please cite:

```bibtex
@software{tep_bbn,
  title = {Temporal Equivalence Principle: Dynamical Proper Time and the Illusion of Primordial Deuterium},
  year = {2026},
  url = {https://github.com/matthewsmawfield/TEP-BBN}
}
```

## License

MIT License (Codebase) | CC-BY 4.0 (Manuscript & Data) - see [LICENSE](LICENSE) file.

## Contact

For questions, issues, or collaborative inquiries regarding the TEP framework, please submit an issue to the repository or contact the author directly via the listed ORCiD profile.
