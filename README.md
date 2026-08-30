# Temporal Equivalence Principle: Dynamical Proper Time and the Illusion of Primordial Deuterium

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21841147.svg)](https://doi.org/10.5281/zenodo.21841147)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

![TEP-BBN: Dynamical Proper Time and the Illusion of Primordial Deuterium](site/public/image.webp)

**Author:** Matthew Lukin Smawfield  
**Version:** v0.2 (Dubai)  
**First published:** 12 August 2026  
**Last updated:** 31 August 2026  
**Status:** Preprint (Open for Collaboration)  
**DOI:** [10.5281/zenodo.21841147](https://doi.org/10.5281/zenodo.21841147)  
**Website:** [https://mlsmawfield.com/tep/bbn](https://mlsmawfield.com/tep/bbn)  
**Paper Series:** TEP Series: Paper 29 (Dynamical Proper Time and the Illusion of Primordial Deuterium)

## Abstract

This paper proves that purported primordial deuterium features in quasar absorption spectra are better explained as shifted ordinary hydrogen. Using a shared Voigt architecture and Monte-Carlo-calibrated nested testing across the three best-studied D/H sightlines---Q1009+2956 (Keck/HIRES), PKS\,1937$-$101 (ESPRESSO), and J1332$+$0052 (UVES+HIRES)---the unrestricted hydrogen model is significantly preferred over the true-deuterium model under both the canonical-parent and adversarial parent-reassignment statistics ($p \le 0.001$ for all three sightlines, surviving Bonferroni correction). The key physical insight is that *isotope identifiability is controlled by both Doppler regime and D column density*: at the unsaturated LLS-class columns typical of D/H measurements, the intrinsic H/D profile-shape difference is sub-noise on a per-pixel basis, so the deuterium identification rests entirely on the velocity offset---which the free-H model can reproduce without invoking deuterium at all. A multi-pronged evidence analysis (Gate 8) calibrates three discriminators---$b$-value ratio, velocity offset deviation, and column density difference---against true-D injection Monte Carlo: the joint statistic is highly significant for all three sightlines ($p < 0.005$), with Q1009's velocity deviation alone rejecting isotope-D at $p < 0.005$ and PKS\,1937's velocity deviation also rejecting it at $p < 0.005$; J1332's $b$-value ratio rejects isotope-D individually ($p = 0.045$) and the joint statistic is highly significant ($p < 0.005$). All three features are blueward of the parent, as the conformal sign theorem predicts. A velocity-selection theorem explains the universality of the $-81.6$\,km/s offset as a selection effect of the D-search protocol, and a quantitative population forecast predicts $\sim 20$ orphan narrow components at non-isotope offsets across $\sim 80$ high-S/N LLS sightlines---testable with existing archival data.

The Temporal Equivalence Principle (TEP) provides the alternative mechanism: the deuterium-like velocity feature is the spectroscopic signature of temporal shear in diffuse, unscreened edge gas. The TEP absorber field deterministically predicts the blueward sign from conformal core-edge geometry; the environmental screening operator is calibrated by three boundary conditions (absorber, Cassini, galactic halo) that yield $132\times$ screening contrast between solar-system and galactic regimes; the conformal-only amplitude is quantified and the required amplification ($\mathcal{A}_{\rm env} \approx 9.3 \times 10^3$) is identified as a falsifiable target for the non-perturbative transport path. Cosmological redshift is reformulated as temporal transport over a static spatial background, the helium-4 mass fraction emerges as the equilibrium of baryonic-cycling reaction flows under temporal-horizon metal sequestration, and the line-of-sight optical depth diverges at high redshift to create an observable boundary without a physical plasma wall. The broader TEP corpus establishes CMB acoustic peak preservation at $< 6$\,ppm, temporal-horizon regularity, cosmological distances without expansion, and JWST high-redshift anomaly resolution.

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
2. **Gate 2**: Generating and fitting standard parent-tied $D$ and displaced free-$H$ components across three benchmark sightlines (Q1009+2956, PKS\,1937$-$101, J1332$+$0052).
3. **Gate 3**: Executing a 1000-realization Monte Carlo significance test with parent-reassignment calibration.
4. **Gate 4**: Symbolic proof of the TEP absorber field blueward velocity sign.
5. **Gate 4B**: Quantitative amplitude test with frozen $\beta_A = -1.0$ and ionisation-corrected Q1009+2956 observables.
6. **Gate 5**: Symbolic proof of Planck spectrum preservation under temporal transport.
7. **Gate 6**: Primordial helium synthesis via baryonic cycling, temporal-horizon metal sequestration, and velocity-selection theorem with orphan population forecast.
8. **Gate 7**: Analytical proof of divergent optical depth in the static spatial geometry (Opacity Boundary).
9. **Gate 8**: Multi-pronged evidence analysis calibrating three discriminators ($b$-value ratio, velocity offset deviation, column density difference) against true-D injection Monte Carlo.

The output metrics, structural fits, and physical derivations are dumped as JSON ledgers into the `results/` directory, terminating with a cryptographic `checksums_sha256.json` file.

### Manuscript Generation
To rebuild the Markdown and high-quality PDF manuscript from the HTML components and mathematical derivations:

```bash
python scripts/generate_site_pdf.py
```
*(Requires a running Chrome/Chromium installation for Headless PDF rendering).*

## Key Results (v0.2)

1. **Statistical Non-Identifiability**: Subjected to rigorously nested hypothesis testing across three benchmark sightlines (Q1009+2956, PKS\,1937$-$101, J1332$+$0052), an unrestricted hydrogen model is significantly preferred over true-D under both the canonical-parent and adversarial parent-reassignment statistics ($p \le 0.001$ for all three sightlines, surviving Bonferroni correction). A multi-pronged evidence analysis (Gate 8) calibrates three discriminators---$b$-value ratio, velocity offset deviation, and column density difference---against true-D injection Monte Carlo, yielding a highly significant joint statistic for all three sightlines ($p < 0.005$).
2. **Velocity-Selection Theorem and Population Forecast**: The universality of the $-81.6$\,km/s offset is explained as a selection effect of the D-search protocol. A quantitative population forecast predicts $\sim 20$ orphan narrow components at non-isotope offsets across $\sim 80$ high-S/N LLS sightlines---testable with existing archival data.
3. **TEP Absorber Field Sign and Amplitude**: The blueward displacement sign is deterministically derived from conformal core-edge geometry (Gate 4). The environmental screening operator is calibrated by three boundary conditions (absorber, Cassini, galactic halo) yielding $132\times$ screening contrast; the required amplification ($\mathcal{A}_{\rm env} \approx 9.3 \times 10^3$) is identified as a falsifiable target for the non-perturbative transport path (Gate 4B).
4. **Planck Spectral Preservation**: A symbolic proof demonstrates that any emitted Planck spectrum is strictly preserved in form under temporal transport, without requiring a singular early phase or FLRW geometric expansion.
5. **Helium-4 Equilibrium**: The helium-4 mass fraction ($Y_{\rm eq} = 0.247$) emerges as the equilibrium of baryonic-cycling reaction flows under temporal-horizon metal sequestration.
6. **Opacity Boundary**: In the static spatial geometry, the line-of-sight optical depth diverges at high redshift (proven via constant $n_e$ and divergent path length $\ell(z) \to \infty$), creating an observable boundary without a physical plasma wall.

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
