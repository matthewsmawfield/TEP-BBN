# Temporal Equivalence Principle: Dynamical Proper Time and the Illusion of Primordial Deuterium

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21841147.svg)](https://doi.org/10.5281/zenodo.21841147)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

![TEP-BBN: Dynamical Proper Time and the Illusion of Primordial Deuterium](site/public/image.webp)

**Author:** Matthew Lukin Smawfield  
**Version:** v0.3 (Dubai)  
**First published:** 12 August 2026  
**Last updated:** 10 September 2026  
**Status:** Preprint (Open for Collaboration)  
**DOI:** [10.5281/zenodo.21841147](https://doi.org/10.5281/zenodo.21841147)  
**Website:** [https://mlsmawfield.com/tep/bbn](https://mlsmawfield.com/tep/bbn)  
**Paper Series:** TEP Series: Paper 29 (Dynamical Proper Time and the Illusion of Primordial Deuterium)

## Abstract

The spectroscopic identification of primordial deuterium---a foundational empirical pillar of Big Bang cosmology---is not mathematically unique. Within standard Voigt-profile fitting architectures, the absorption features conventionally attributed to deuterium across the three best-studied quasar sightlines are statistically better described by unrestricted ordinary hydrogen. Using Monte-Carlo-calibrated model comparison across Q1009+2956 (Keck/HIRES), PKS\,1937$-$101 (ESPRESSO), and J1332$+$0052 (UVES+HIRES), the unrestricted hydrogen model is significantly preferred over the true-deuterium model under both the canonical-parent and adversarial parent-reassignment statistics ($p \le 0.001$ for all three sightlines on the primary Gate 2/3 family, surviving $\alpha/6$). The key physical insight is that *isotope identifiability is controlled by both Doppler regime and D column density*: at the unsaturated LLS-class columns typical of D/H measurements, the intrinsic H/D profile-shape difference is sub-noise on a per-pixel basis, so the deuterium identification depends predominantly on the velocity offset---which the free-H model can reproduce without invoking deuterium at all. A multi-pronged evidence analysis (Gate 8) calibrates three discriminators---$b$-value ratio, velocity offset deviation, and column density difference---against true-D injection Monte Carlo ($N = 1000$ per sightline): the joint statistic is highly significant for Q1009+2956 and PKS\,1937$-$101 ($p \le 0.001$), with velocity deviations alone rejecting isotope-D at $p \le 0.001$ for both sightlines; J1332$+$0052 is less discriminating. All three features are blueward of the parent, consistent with the conformal sign theorem (though the D-selected sample is not an independent sign test). A velocity-selection theorem explains the universality of the $-81.6$\,km/s offset as a selection effect of the D-search protocol, and motivates an independently selected population test for non-isotope displaced H I components. An archival feasibility search establishes the principal saturation and Ly$\alpha$-forest selection limits and identifies one candidate component in Q1009$+$2956, motivating a larger targeted survey. A pilot search of the three benchmark sightlines identifies one candidate feature already present in the literature scaffold near the predicted orphan phenotype in Q1009$+$2956: a narrow ($b = 10.3$\,km/s, $\log N = 11.5$) H I component at $\Delta v = -155.5$\,km/s from the parent ($73.9$\,km/s from the isotope shift), identified as a candidate non-isotope component in the HIRES spectrum.

A TEP mapping is offered as a candidate, not a derived result of this paper. Conformal core–edge geometry predicts a blueward sign. An absorber-regime amplitude ansatz $S_A^{\rm abs}$ is introduced for diffuse absorbers; Cassini independently constrains the source-charge response $S_\Sigma^{(\odot)}$, while the relation between these projections remains to be derived from the common microscopic scalar solution. The conformal-only amplitude is $\sim10^{-2}\,\mathrm{km\,s^{-1}}$; the temporal-disformal channel activated by the cosmological scalar time derivative is investigated as the candidate amplitude mechanism. It can reach the observed scale in the Einstein-frame parametrisation explored here. Both power-law realisations tested are excluded---$n = 2$ by the Cassini bound, $n = 5$ by loss of Lorentzian signature above $z \approx 3.4$---so no viable microscopic $B(\phi)$ has yet been exhibited, and the covariant matter-frame frequency mapping remains to be closed. The $-81.6$\,km/s clustering is explained by the velocity-selection theorem (Gate 6-I) as a selection effect of the D-search protocol, not as a universal TEP-produced shift. Within the adopted VMO-dominated reaction-flow model, the helium-4 abundance is reproduced as an equilibrium, while a conditional opacity theorem provides an observable high-redshift boundary without a physical plasma wall. Cosmological redshift is reformulated as temporal transport over a static spatial background. The broader TEP framework---CMB acoustic peak preservation, temporal-horizon regularity, cosmological distances without expansion, and JWST high-redshift anomaly resolution---is developed in companion papers.

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

## Key Results (v0.3)

1. **Statistical Non-Identifiability**: Subjected to rigorously controlled model comparison across three benchmark sightlines (Q1009+2956, PKS\,1937$-$101, J1332$+$0052), an unrestricted hydrogen model is significantly preferred over true-D under both the canonical-parent and adversarial parent-reassignment statistics ($p \le 0.001$ for all three sightlines on the primary Gate 2/3 family, surviving $\alpha/6$). A multi-pronged evidence analysis (Gate 8) calibrates three discriminators---$b$-value ratio, velocity offset deviation, and column density difference---against true-D injection Monte Carlo ($N = 1000$ per sightline), yielding a highly significant joint statistic for Q1009+2956 and PKS\,1937$-$101 ($p \le 0.001$); J1332$+$0052 is less discriminating.
2. **Velocity-Selection Theorem and Population Forecast**: The universality of the $-81.6$\,km/s offset is explained as a selection effect of the D-search protocol. An archival feasibility search establishes the principal saturation and Ly$\alpha$-forest selection limits; a pilot search of the three benchmark sightlines identifies one candidate orphan feature in Q1009$+$2956.
3. **TEP Absorber Field Sign and Amplitude**: The blueward displacement sign is predicted by conformal core–edge geometry (Gate 4). An absorber-regime amplitude ansatz $S_A^{\rm abs}$ is introduced for diffuse absorbers; Cassini independently constrains the source-charge response $S_\Sigma^{(\odot)}$, while the relation between these projections remains to be derived from the common microscopic scalar solution. The conformal-only amplitude is $\sim10^{-2}\,\mathrm{km\,s^{-1}}$; the temporal-disformal channel activated by the cosmological scalar time derivative is investigated as the candidate amplitude mechanism. A universal microscopic $B(\phi)$ and the covariant matter-frame frequency mapping remain to be closed.
4. **Planck Spectral Preservation**: A symbolic proof demonstrates that any emitted Planck spectrum is strictly preserved in form under temporal transport, without requiring a singular early phase or FLRW geometric expansion.
5. **Helium-4 Equilibrium**: Within the adopted VMO-dominated reaction-flow model, the helium-4 mass fraction ($Y_{\rm eq} = 0.247$) is reproduced as an equilibrium under temporal-horizon metal sequestration.
6. **Opacity Boundary**: A conditional opacity theorem provides an observable high-redshift boundary without a physical plasma wall.

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
└── 29-TEP-BBN-v0.3-Dubai.md # Generated Markdown manuscript
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
