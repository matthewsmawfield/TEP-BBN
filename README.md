# Temporal Equivalence Principle: Dynamical Proper Time and the Illusion of Primordial Deuterium

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21841147.svg)](https://doi.org/10.5281/zenodo.21841147)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
![TEP-BBN: Dynamical Proper Time and the Illusion of Primordial Deuterium](site/public/image.webp)

**Author:** Matthew Lukin Smawfield  
**Version:** v0.6 (Dubai)  
**First published:** 12 August 2026 · **Last updated:** 17 October 2026  
**Status:** Preprint  
**DOI:** [10.5281/zenodo.21841147](https://doi.org/10.5281/zenodo.21841147)  
**Website:** [https://mlsmawfield.com/tep/bbn/](https://mlsmawfield.com/tep/bbn/)  
**Paper Series:** TEP Series · Group F (VI. Cosmological Transport, Horizon Boundary & Standard Sirens) · Paper 29 (`F29`)

## Abstract

<!-- Generated from site/components/00_abstract.html; update the manuscript source, then run tools/sync_current_corpus_readmes.py. -->

The spectroscopic identification of primordial deuterium—a foundational empirical pillar of Big Bang cosmology—is not mathematically unique. Within standard Voigt-profile fitting architectures, the absorption features conventionally attributed to deuterium across the three best-studied quasar sightlines are statistically better described by unrestricted ordinary hydrogen. Using Monte-Carlo-calibrated model comparison across Q1009+2956 (Keck/HIRES), PKS 1937$-$101 (ESPRESSO), and J1332$+$0052 (UVES+HIRES), the unrestricted hydrogen model is significantly preferred over the true-deuterium model under both the canonical-parent and adversarial parent-reassignment statistics (largest calibrated $p=0.001$ among the primary Gate 2/3 statistics, surviving $\alpha/6$). The key physical insight is that isotope identifiability is controlled by both Doppler regime and D column density: at the unsaturated LLS-class columns typical of D/H measurements, the intrinsic H/D profile-shape difference is sub-noise on a per-pixel basis, so the deuterium identification depends predominantly on the velocity offset—which the free-H model can reproduce without invoking deuterium at all. A multi-pronged evidence analysis (Gate 8) calibrates three discriminators—$b$-value ratio, velocity offset deviation, and column density difference—against true-D injection Monte Carlo ($N = 1000$ per sightline): the calibrated joint results are Q1009: $p=0.001$; PKS1937: $p=0.001$; J1332: $p=0.023$. The two unsaturated systems give velocity-diagnostic probabilities Q1009: $p=0.001$; PKS1937: $p=0.001$. All three features are blueward of the parent, consistent with the conformal sign theorem (though the D-selected sample is not an independent sign test). A velocity-selection theorem explains the universality of the $-81.6$ km/s offset as a selection effect of the D-search protocol, and motivates an independently selected population test for non-isotope displaced H I components. An archival feasibility search establishes the principal saturation and Ly$\alpha$-forest selection limits and identifies one candidate component in Q1009$+$2956, motivating a larger targeted survey. A pilot search of the three benchmark sightlines identifies one candidate feature already present in the literature scaffold near the predicted orphan phenotype in Q1009$+$2956: a narrow ($b = 10.3$ km/s, $\log N = 11.5$) H I component at $\Delta v = -155.5$ km/s from the parent ($73.9$ km/s from the isotope shift), identified as a candidate non-isotope component in the HIRES spectrum.

Conformal core–edge geometry predicts a blueward sign. An absorber-regime amplitude ansatz $S_A^{\rm abs}$ is introduced for diffuse absorbers; Cassini independently constrains the source-charge response $S_\Sigma^{(\odot)}$. Both are projections of the common microscopic scalar solution (Paper 0 §7): the derived kinetic operator $\mathcal{S}_\Sigma(\mathcal{E})=[k\sqrt{\xi}+2\xi]^{-1}$, $\xi=|X|/\Lambda_X⁴$; the quoted environment table uses the acceleration proxy $\xi_{\rm tab}=(g/g_t)²$ inherited from the foundational benchmark, rather than identifying that proxy with the solved-field kinetic invariant. Under this tabulation convention the operator returns $\mathcal{S}_\Sigma\simeq1.6\times10^{-15}$ at 1 AU and $\mathcal{S}_\Sigma\sim1.5$–$21$ at the Lyman-limit absorber ambient; evaluated instead on the solved drift-dominated field at the absorber epochs the same operator returns $\mathcal{S}_\Sigma\sim0.13$–$0.18$ (step_21 drift-branch), so the environmental discrimination is supplied by one operator rather than assumed, under either field reconstruction. The conformal-only amplitude is $\sim10^{-2}\,\mathrm{km\,s^{-1}}$; the temporal-disformal channel activated by the cosmological scalar time derivative was investigated as a candidate amplitude mechanism. It can reach the observed scale per sightline in the Einstein-frame parametrisation explored here. The power-law $B(\phi)$ forms tested so far do not achieve predictive closure across the three sightlines: $n = 2$ exceeds the Cassini bound only under a conservatively adopted solar source-charge profile (under the derived operator the disformal spatial term carries an $\mathcal{S}_\Sigma²\sim10^{-48}$ suppression and the bound is non-binding), while $n = 5$ loses Lorentzian signature above $z \approx 3.4$. The full covariant calculation (Gate 10) with $\omega=-u^\mu k_\mu$ confirms that the near-criticality and cross-redshift signature loss persist under the complete matter-frame treatment when the drift is imported from the $\Lambda$CDM expansion history; the binding constraint is then the $A²/\dot{\bar\phi}^{\,2}$ variation across redshift, which prevents any single increasing power-law $B(\phi)$ from achieving simultaneous near-criticality at all three sightlines. That constraint is shown to be a property of the imported rate rather than of the disformal channel: the joint sign-and-closure criterion reduces to $d\ln H_T²/d\ln(1+z) < 0$ — a descent-type ambient drift — and the unsourced free-roll on the reconstructed corpus potential, $\dot{\bar\phi}^{\,2} = \bar\Pi_\infty² + \bar\rho\,e^{-\bar\varphi}$, satisfies it. Under the pure-descent limit the descent-tracking coupling $B(\varphi) = B_0\,\varphi⁴/(\varphi_c⁴+\varphi⁴)\,e^{-\varphi}$ has inverse-fit roots agreeing to a factor $1.00004$ and satisfies the Cassini and GW170817 bounds; forward evaluation at that common $B_0$ does not reproduce the three amplitudes, and the branch is independently excluded by ambient-lapse self-consistency: the boundary factor $u = B\dot{\bar\phi}^{\,2}/A²$ is constant along the descent at $\approx 1 - 10^{-5}$, so the matter-metric redshift map $1+z = \tilde N(0)/\tilde N(\bar\varphi)$ would require a negative ambient field to reproduce the observed absorber population. The unscreened temporal-disformal amplitude channel is thereby bounded sub-critical at these epochs; a contribution of the observed scale can arise only where $B(\phi)$ is environmentally screened. The $-81.6$ km/s clustering is explained by the velocity-selection theorem (Gate 6-I) as a selection effect of the D-search protocol, not as a universal TEP-produced shift. Within the adopted VMO-dominated reaction-flow model, the helium-4 abundance is reproduced as an equilibrium, while a conditional opacity theorem provides an observable high-redshift boundary without a physical plasma wall. Cosmological redshift is reformulated as temporal transport over a static spatial background. The broader TEP framework—CMB acoustic peak preservation, temporal-horizon regularity, cosmological distances without expansion, and JWST high-redshift phenomenology—is developed in companion papers.

Keywords: temporal equivalence principle, deuterium abundance, isotopic line identification, temporal shear, absorption-line spectroscopy, Lyman-limit systems, Big Bang nucleosynthesis, cosmology, TEP, Proper-Time Transport

Current manuscript source: [00_abstract.html](site/components/00_abstract.html).

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

## Key Results

The current results and their comparison assumptions are reported in [6. Conclusion](site/components/06_conclusion.html). The abstract above is synchronized from the current manuscript.

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
└── F29-TEP-BBN-v0.6-Dubai.md # Generated Markdown manuscript
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

CC-BY-4.0 (Manuscript, Code & Data) - see [LICENSE](LICENSE) file.

## Contact

For questions, issues, or collaborative inquiries regarding the TEP framework, please submit an issue to the repository or contact the author directly via the listed ORCiD profile.
