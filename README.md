# Temporal Equivalence Principle: Dynamical Proper Time and the Illusion of Primordial Deuterium

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21841148.svg)](https://doi.org/10.5281/zenodo.21841148)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

![TEP-BBN: Dynamical Proper Time and the Illusion of Primordial Deuterium](site/public/image.webp)

**Author:** Matthew Lukin Smawfield  
**Version:** v0.2 (Dubai)  
**First published:** 12 August 2026  
**Last updated:** 27 August 2026  
**Status:** Preprint (Open for Collaboration)  
**DOI:** [10.5281/zenodo.21841148](https://doi.org/10.5281/zenodo.21841148)  
**Website:** [https://mlsmawfield.com/tep/bbn](https://mlsmawfield.com/tep/bbn)  
**Paper Series:** TEP Series: Paper 29 (Dynamical Proper Time and the Illusion of Primordial Deuterium)

## Abstract

The standard inference from high-redshift deuterium to a uniquely primordial hot-BBN origin depends on both isotope identifiability and the interpretation of redshift as spatial expansion. Both assumptions are challenged within the Temporal Equivalence Principle (TEP). Using physical H I and D I atomic data, it is shown that the optimally embedded ordinary-H spectrum differs from true D by only $0.0208\sigma$ at Q1009 resolution. A nested-hypothesis analysis of Q1009+2956, with the shared Voigt architecture held fixed across hypotheses so that the resulting statistic can be calibrated exactly, finds an unrestricted-H optimum improved by $\Delta\ln L=28.29$ ($T=56.57$); against the most favourable alternative parent the margin falls to $T_{\rm parent}=5.03$, and calibration against 1000 true-D Monte Carlo realizations of the identical statistic yields $p_{\rm parent} = 0.018$, with the discrimination concentrated in the Ly$\alpha$ transition ($T_{-\mathrm{Ly}\alpha} = 1.95$). The TEP absorber field and its blueward displacement sign are then derived from core–edge geometry: the dense absorber core is the most redshifted component, and the diffuse edge appears blueshifted relative to it when the core defines the systemic redshift. The conformal sector deterministically produces the correct blueward sign; the full amplitude is quantified as a falsifiable prediction of the environmental operator $\mathcal{S}_\Sigma(\mathcal{E})$. This apparent velocity shift is a localized manifestation of Temporal Shear, and cosmological redshift is formulated as temporal transport over a static spatial background. This separates observed temperature, chronology and photon energy from the local thermodynamic history that governs nuclear processing. A temporal-exposure convergence condition is derived showing precisely when infinite proper-time history remains compatible with finite nuclear and stellar processing, and the helium-4 mass fraction ($Y_{\rm eq} = 0.247$) is shown to emerge as the equilibrium of baryonic-cycling reaction flows under temporal-horizon metal sequestration. Finally, in the static spatial geometry, the line-of-sight optical depth is shown to diverge at high redshift, creating an observable boundary without a physical plasma wall. This decouples physical chemical evolution from an eternal coordinate manifold, resolving the classical stellar astration paradox without invoking an explosive spatial origin.

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
The core analysis is orchestrated by `run_pipeline.py`, which executes 7 sequential "gates":
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

The output metrics, structural fits, and physical derivations are dumped as JSON ledgers into the `results/` directory, terminating with a cryptographic `checksums_sha256.json` file.

### Manuscript Generation
To rebuild the Markdown and high-quality PDF manuscript from the HTML components and mathematical derivations:

```bash
python scripts/generate_site_pdf.py
```
*(Requires a running Chrome/Chromium installation for Headless PDF rendering).*

## Key Results (v0.2)

1. **Statistical Non-Identifiability**: Subjected to rigorously nested hypothesis testing, an unrestricted hydrogen model fits the Q1009 data with statistical dominance ($p_{\rm add-one} = 0.001$ standard, $p_{\rm parent} = 0.018$ conservative), with discrimination concentrated in the Ly$\alpha$ transition.
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
│   ├── steps/               # Individual pipeline gates (01-07)
│   └── run_pipeline.py      # Full pipeline runner
├── tests/                # Verification tests
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
