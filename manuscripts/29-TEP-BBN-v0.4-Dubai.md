# Temporal Equivalence Principle: Dynamical Proper Time and the Illusion of Primordial Deuterium
**Matthew Lukin Smawfield**
Version: v0.4 (Dubai)
First published: 12 August 2026 - Last updated: 10 September 2026
DOI: 10.5281/zenodo.21841147

---

## Abstract

The spectroscopic identification of primordial deuterium---a foundational empirical pillar of Big Bang cosmology---is not mathematically unique. Within standard Voigt-profile fitting architectures, the absorption features conventionally attributed to deuterium across the three best-studied quasar sightlines are statistically better described by unrestricted ordinary hydrogen. Using Monte-Carlo-calibrated model comparison across Q1009+2956 (Keck/HIRES), PKS\,1937$-$101 (ESPRESSO), and J1332$+$0052 (UVES+HIRES), the unrestricted hydrogen model is significantly preferred over the true-deuterium model under both the canonical-parent and adversarial parent-reassignment statistics ($p \le 0.001$ for all three sightlines on the primary Gate 2/3 family, surviving $\alpha/6$). The key physical insight is that *isotope identifiability is controlled by both Doppler regime and D column density*: at the unsaturated LLS-class columns typical of D/H measurements, the intrinsic H/D profile-shape difference is sub-noise on a per-pixel basis, so the deuterium identification depends predominantly on the velocity offset---which the free-H model can reproduce without invoking deuterium at all. A multi-pronged evidence analysis (Gate 8) calibrates three discriminators---$b$-value ratio, velocity offset deviation, and column density difference---against true-D injection Monte Carlo ($N = 1000$ per sightline): the joint statistic is highly significant for Q1009+2956 and PKS\,1937$-$101 ($p ≤ 0.001$), with velocity deviations alone rejecting isotope-D at $p ≤ 0.001$ for both sightlines; J1332$+$0052 is less discriminating. All three features are blueward of the parent, consistent with the conformal sign theorem (though the D-selected sample is not an independent sign test). A velocity-selection theorem explains the universality of the $-81.6$\,km/s offset as a selection effect of the D-search protocol, and motivates an independently selected population test for non-isotope displaced H I components. An archival feasibility search establishes the principal saturation and Ly$\alpha$-forest selection limits and identifies one candidate component in Q1009$+$2956, motivating a larger targeted survey. A pilot search of the three benchmark sightlines identifies one candidate feature already present in the literature scaffold near the predicted orphan phenotype in Q1009$+$2956: a narrow ($b = 10.3$\,km/s, $\log N = 11.5$) H I component at $\Delta v = -155.5$\,km/s from the parent ($73.9$\,km/s from the isotope shift), identified as a candidate non-isotope component in the HIRES spectrum.

Conformal core–edge geometry predicts a blueward sign. An absorber-regime amplitude ansatz $S_A^{\rm abs}$ is introduced for diffuse absorbers; Cassini independently constrains the source-charge response $S_\Sigma^{(\odot)}$, while the relation between these projections remains to be derived from the common microscopic scalar solution. The conformal-only amplitude is $\sim10^{-2}\,\mathrm{km\,s^{-1}}$; the temporal-disformal channel activated by the cosmological scalar time derivative is investigated as the candidate amplitude mechanism. It can reach the observed scale in the Einstein-frame parametrisation explored here. Both power-law realisations tested fail: $n = 2$ is excluded by the Cassini bound, while $n = 5$ loses Lorentzian signature above $z \approx 3.4$. Thus no viable microscopic $B(\phi)$ has yet been exhibited, and the covariant matter-frame frequency mapping remains to be closed. The $-81.6$\,km/s clustering is explained by the velocity-selection theorem (Gate 6-I) as a selection effect of the D-search protocol, not as a universal TEP-produced shift. Within the adopted VMO-dominated reaction-flow model, the helium-4 abundance is reproduced as an equilibrium, while a conditional opacity theorem provides an observable high-redshift boundary without a physical plasma wall. Cosmological redshift is reformulated as temporal transport over a static spatial background. The broader TEP framework-CMB acoustic peak preservation, temporal-horizon regularity, cosmological distances without expansion, and JWST high-redshift phenomenology-is developed in companion papers.

Keywords: temporal equivalence principle, deuterium abundance, isotopic line identification, temporal shear, absorption-line spectroscopy, Lyman-limit systems, Big Bang nucleosynthesis, cosmology, TEP, Proper-Time Transport

## 1. Introduction

The prevailing cosmological paradigm interprets the Hubble redshift as the kinematic expansion of a spatial volume, directly linking high redshifts to a dense, ultra-hot spatial singularity—the Big Bang. Within this framework, the measurement of light element abundances, particularly deuterium (D/H) in high-redshift Lyman-limit systems such as Q1009+2956, serves as a crucial anchor for Big Bang Nucleosynthesis (BBN) <sup>[22], [45]</sup>. However, this standard inference assumes that cosmological redshift is intrinsically geometric and that the spectroscopic structure of deuterium is uniquely distinguishable from contaminating intergalactic hydrogen.

Tensions in precision cosmology—such as the Hubble tension <sup>[17], [18]</sup> and the $S_8$ growth tension—have motivated numerous theoretical extensions to the $\Lambda$CDM framework <sup>[16]</sup>. Recent literature has extensively explored modified gravity (e.g., $f(R)$ or scalar-tensor theories <sup>[30], [42]</sup>), non-standard recombination histories, and Early Dark Energy (EDE) to resolve these anomalies. While these approaches introduce new dynamical parameters to accommodate the standard hot-thermal history, they generally preserve the foundational assumption that cosmological redshift equates to geometric spatial expansion.

### The Temporal Equivalence Principle Framework

The standard Friedmann-Lemaître-Robertson-Walker (FLRW) metric <sup>[11], [12], [13]</sup> explicitly couples cosmological evolution to a dynamic spatial volume. Extrapolating this geometric expansion backward inevitably terminates in a spatial singularity ($a \to 0$)—a regime where polynomial curvature invariants diverge and the foundational equations of General Relativity break down <sup>[5], [6], [7]</sup>. Alternative non-singular cosmologies, including bouncing models <sup>[8], [9]</sup>, cyclic scenarios <sup>[10]</sup>, and conformal approaches <sup>[37], [38], [39]</sup>, have been explored but typically require additional dynamical ingredients. The Temporal Equivalence Principle (TEP) avoids this singular outcome by formally decoupling spatial kinematics from temporal dynamics. By anchoring the universe to a static physical matter frame ($a_{\rm m} = 1$) governed by a dynamical proper-time field $A(\phi)$ <sup>[40], [41]</sup>, the TEP geometry removes the spatial singularity. Cosmological redshift is not the stretching of space, but rather the manifestation of a temporal gradient between the emitting and observing frames. This approach shares conceptual ground with static-universe and conformal frameworks <sup>[31], [32], [33], [34]</sup>, but distinguishes itself through the dynamical proper-time field and its coupling to matter. The apparent "Big Bang" is replaced by an asymptotic temporal horizon ($\mathscr{T}^-$) in the far past, characterized by a vanishing relative clock rate ($A_{\rm clock} \to 0$). Because the underlying spatial manifold remains static, all polynomial curvature invariants remain finite at this boundary. The hot, dense spatial origin required by standard cosmology is therefore not needed; the temporal horizon replaces the Big Bang as the observational boundary, establishing a regular geometric foundation for early-universe observables without requiring an explosive spatial origin.

The standard hot-BBN inference is challenged on two fronts within the TEP framework <sup>[1], [2]</sup>. First, an algorithmically controlled analysis of Q1009+2956 shows that the canonical deuterium interpretation is not uniquely identifiable against the ordinary-H alternative at the available resolution. Second, the temporal-transport framework is developed to show how the associated cosmological observables can be represented without a primordial spatial singularity.

## 2. Spectroscopic Analysis

The spectroscopic uniqueness of the deuterium identification in high-redshift quasar absorption systems is examined under Monte-Carlo-calibrated model comparison. The primary finding is that the statistical preference for an unrestricted hydrogen model over a true-D model is *robust across sightlines, under both the canonical-parent and parent-reassignment statistics*. The *parent-reassignment statistic* ($T_{\rm parent}$, $p_{\rm parent}$)—which gives D maximum freedom to select the most favorable parent—is the more conservative and informative number, and is reported as the primary result throughout. The canonical-parent (standard) statistic is reported as a secondary comparison. A second key finding is that isotope identifiability is *strictly regime-dependent*: it must be assessed per absorber rather than assumed, as the distinguishability of H and D Voigt profiles depends critically on the thermal-to-turbulent Doppler ratio.

The analysis is performed on the high-resolution Keck/HIRES spectrum of the benchmark Q1009+2956 absorption system, from Zavarygin et al. 2018 <sup>[44]</sup> (22 HIRES exposures co-added into four setups using the wspectrum software). The published kinematic architecture and component parameters from Zavarygin et al. 2018 <sup>[44]</sup> are used as the structural prior for the Voigt component family, fitted with the VPFIT framework <sup>[50]</sup>. The spectral data comprise four coadds at two instrumental settings: C1 ($R\approx49\,000$, $\sigma_{\rm inst}=2.6$\,km/s) and C5 ($R\approx37\,000$, $\sigma_{\rm inst}=3.4$\,km/s), with S/N $\approx 47$–$78$ per pixel near Ly$\alpha$. The system was originally measured for primordial D/H by Burles & Tytler <sup>[46]</sup> and subsequently by Zavarygin et al. <sup>[44]</sup>, with independent measurements from other quasar sightlines contributing to the primordial D/H estimate <sup>[47], [48]</sup>. Two additional benchmark sightlines—PKS\,1937$-$101 (ESPRESSO, $z=3.572$) and J1332$+$0052 (UVES+HIRES, $z=3.421$)—are analysed with the identical framework in Section 2.4.

### 2.1 Isotope Identifiability Limits in Q1009+2956

Using the physical atomic registries for H I and D I (NIST ASD), synthetic deuterium was embedded at the actual Q1009 D column ($N_{\rm D} = 5.7\times10^{12}\,\mathrm{cm}^{-2}$, derived from D/H $= 2.48\times10^{-5}$ and $\log N_{\rm HI} = 17.362$) and recovered using unrestricted hydrogen models. Zavarygin et al. <sup>[44]</sup> themselves noted that the putative D feature is likely contaminated by weak interloping Ly$\alpha$ absorption from a low-column-density H I cloud, reducing the D/H precision. The present analysis extends this insight by quantifying the D/H degeneracy through explicit adversarial model comparison with Monte-Carlo-calibrated parent reassignment, comparing multiple sightlines, and then asking whether the ordinary-H alternative admits a TEP interpretation. The isotope identifiability depends on both the Doppler parameter regime and the D column density. For thermally-dominated gas, the H and D Doppler parameters differ by the mass ratio: $b_{\rm H} = b_{\rm D}\sqrt{m_{\rm D}/m_{\rm H}} \approx 1.41\,b_{\rm D}$. With this physical mass scaling, the maximum convolved flux discrepancy between H and D profiles across all Lyman transitions is $0.52\sigma$ at Keck/HIRES C1 resolution ($R\approx49\,000$, $\sigma_{\rm inst} = 2.6$\,km/s), indicating that H and D are marginally distinguishable for thermally-dominated gas at this column. The $\sigma$ statistic is computed as the maximum pixel-level flux residual divided by a conservative constant noise floor ($\sigma_{\rm floor} = 0.05$), evaluated across the five strongest Lyman transitions (Ly$\alpha$ through Ly$\epsilon$). For turbulence-dominated gas ($b_{\rm turb} \gg b_{\rm therm}$), the mass-dependent thermal contribution is negligible and $b_{\rm H} \approx b_{\rm D}$; in this limit the maximum discrepancy falls to $0.0002\sigma$, making the isotopes operationally unidentifiable. For the actual Q1009 fitted parameters ($T_K = 2000$\,K, $b_{\rm turb} = 11.60$\,km/s, giving $b_{\rm turb}/b_{\rm therm} \approx 2.02$), the mixed-regime discrepancy is $0.10\sigma$ — far below conventional detectability. The identifiability is controlled by the D column: at the unsaturated LLS-class columns typical of D/H measurements ($\log N_{\rm D} \lesssim 13$), the single-pixel discrepancy is sub-threshold in every Doppler regime; only saturated sub-DLA columns ($\log N_{\rm D} \gtrsim 14$) approach distinguishability. Isotope identifiability must therefore be assessed per absorber as a function of both column and Doppler regime.

### 2.2 Likelihood Model Comparison and Significance Testing

A complete structural analysis of the Q1009+2956 spectrum is performed under a controlled constrained-versus-unrestricted model hierarchy embedded in the joint D+H model. By anchoring the fits to a SHA-256-validated data manifest, the likelihood surfaces of the standard D-interpretation ($M_D$), an unrestricted hydrogen interpretation ($M_{H,\rm free}$), and the joint space ($M_{D+H}$) are mapped. The 142 shared parameters (43 H I Voigt component parameters: centres, $b$-values, and column densities, plus continuum basis coefficients for each data block) are held at the published literature architecture <sup>[44]</sup>, identically for every hypothesis. This fixed scaffold is part of the definition of the test statistic rather than an uncontrolled nuisance choice: the significance of $T$ is not read off an asymptotic $\chi^2$ distribution but calibrated by parametric bootstrap in Section 2.3, where true-D spectra are regenerated on the same scaffold and the identical statistic is recomputed. Because the scaffold enters the observed and simulated statistics identically, the resulting $p$-value is calibrated conditional on the adopted published architecture. Q1009 scaffold freedom is tested explicitly in §5.5.

The candidate component parameter structure is made fully explicit. Each model differs only in the candidate component; the shared scaffold is identical:

| Model | Candidate params | $v$ | $\log N$ | $T_K$ | $b_{\rm turb}$ | $k_{\rm cand}$ |
| --- | --- | --- | --- | --- | --- | --- |
| $M_D$ (M_Dfree) | D tied to parent | tied to parent $+ v_{\rm iso}$ | free | free | free | 3 |
| $M_{H,\rm free}$ (M_H) | unrestricted H | free | free | free | free | 4 |
| $M_{D+H}$ | D + unrestricted H | D tied, H free | D free, H free | shared | shared | 5 |
| $M_{\rm kin}$ | parent-width-constrained H control | free | free | — | — | 2 |

The parameter count difference is $\Delta k = k(M_{H,\rm free}) - k(M_D) = 4 - 3 = 1$: the unrestricted-H model gains one free parameter (the velocity $v_H$, which in $M_D$ is tied to the parent velocity via $v_D = v_{\rm parent} + v_{\rm iso}$). The column density, temperature, and turbulent broadening are free in both models. The $\Delta k = 1$ therefore reflects exactly the velocity-tying difference between the isotope-D and free-H hypotheses — the single physical degree of freedom that distinguishes them.

| Model | Candidate interpretation | $k$ | $\ln L_{\max}$ | $\Delta\text{AIC}$ | Nested? |
| --- | --- | --- | --- | --- | --- |
| $M_D$ | D tied to parent H | 3 | $-15446.77$ | 0 | — |
| $M_{H,\rm free}$ | unrestricted H | 4 | $-15366.26$ | $-159.03$ | observationally embeds $M_D$ at Q1009 precision |
| $M_{D+H}$ | D + unrestricted H | 5 | $-15366.26$ | $-153.03$ | contains $M_{H,\rm free}$ if $N_{\rm D}\to 0$ (verified to $2.8\times10^{-10}$ in $\Delta\ln L$) |

#### Statistical Significance

The unrestricted hydrogen model—which supplies the displaced-H phenomenology to which the candidate TEP edge-gas interpretation is later applied—provided a superior description of the data, yielding a likelihood improvement:

\begin{equation} \Delta \ln L = 80.51, \qquad T = 161.03, \qquad \Delta k = 1, \qquad \Delta\mathrm{AIC} = -159.03. \end{equation}

The unrestricted-H model adds one free parameter (the H velocity) relative to the D-tied model ($\Delta k = 1$), yet the likelihood improvement of $\Delta\ln L = 80.51$ exceeds the AIC penalty of 2, yielding $\Delta\mathrm{AIC} = -159.03$ and $\Delta\mathrm{BIC} = -151.97$ ($n = 8{,}610$ data points, $\ln n \approx 9.06$). Both information criteria favor $M_{H,\rm free}$. Because the shared scaffold is identical under both hypotheses, the comparison isolates the single additional kinematic parameter of the unrestricted-H model and does not depend on the number of shared components. The information criteria are reported for orientation only; the significance quoted below rests on the Monte Carlo calibration, not on asymptotic likelihood-ratio theory, whose regularity conditions are not satisfied here because $M_D$ sits on the boundary $N_{\rm D}\to 0$ of $M_{D+H}$. Monte Carlo $p$-values use the Laplace-corrected estimator $\hat{p} = (k+1)/(N+1)$, where $k$ is the exceedance count and $N$ is the number of realizations.

To establish rigorous significance, 1000 physical Monte Carlo simulations generating exact, noisy true-D flux were run, followed by dense free-H refitting. Two calibration statistics are reported. The *standard statistic* locks D to the canonical parent (matching the observed fit). The *parent-reassignment statistic* allows D to select the most favorable parent from the H I components within ±1000 km/s of the absorber systemic velocity. The standard statistic represents the prespecified comparison; the parent-reassignment statistic represents the most adversarial test. Both are reported to bracket the significance honestly.

### 2.3 Leave-One-Out and Parent Reassignment Robustness

The component misattribution vulnerability was exhaustively tested by tying the candidate D velocity to every eligible H component within the conservative $\pm 1000\,{\rm km\,s^{-1}}$ parent window (14 parent candidates). The maximum alternative-parent test statistic is defined as:

\begin{equation} T_{\rm parent} = 2 \left[ \ln L(M_{H,\rm free}) - \max_j \ln L(M_D\mid j) \right]. \end{equation}

Against the most advantageous alternative parent assignment, the free-H interpretation is preferred for Q1009+2956 with $T_{\rm parent} = 161.03$, equal to $T = 161.03$ for the canonical parent. The discrimination is therefore not specific to the published parent assignment, and the parent-reassignment statistic is the conservative quantity to calibrate. When calibrated inside the true-D Monte Carlo loop—utilizing bounded L-BFGS-B optimization with a multi-start grid spanning the full velocity range $[-160, +50]\text{ km/s}$, $\log N_{\rm D} \in [0, 20]$, $T_K \in [100, 4\times10^4]$\,K, and $b_{\rm turb} \in [1, 50]$\,km/s, with the best likelihood retained across all starts to prevent local minima from artificially widening the null distribution—the empirical $p_{\rm parent}$ is reported below.

**Parent-reassignment window.** Two parent-reassignment windows are reported. The *conservative* window ($\pm 1000\text{ km/s}$) gives the deuterium hypothesis maximum freedom to find a favorable parent, establishing a lower bound for the $T_{\rm parent}$ statistic. Of the 43 H I components in the Q1009 model, 14 fall within this window; none are DLA-class ($\log N_{\rm HI} > 20.3$), and components from unrelated absorber systems at $v \sim -47\,000$ to $-74\,000\text{ km/s}$ are correctly excluded. The *physical* window ($\pm 3b_{\rm max}$, where $b_{\rm max} = 56.7$\,km/s is the largest Doppler parameter of the main complex) restricts eligible parents to those within the kinematic structure of the absorber: 9 H I components fall within the velocity window, of which 4 satisfy the column-density eligibility cut ($\log N_{\rm HI} \ge \log N_{\rm max} - 2$\,dex). The conservative $\pm 1000\text{ km/s}$ window is the cross-sightline headline statistic; the $\pm 3b_{\rm max}$ physical window has also been calibrated for all three sightlines (Section 5.5), with results consistent with the conservative window. Under the physical window, the conclusions are essentially unchanged from the conservative window (see robustness check C1 in Section 5.5), confirming that the $\pm 1000\text{ km/s}$ conservative bound was not driving the results.

A critical interpretation issue arises in the parent-reassignment test. For Q1009+2956, $T_{\rm parent} = T_{\rm obs} = 161.03$, meaning that allowing reassignment does not improve the D fit over the canonical parent—the discrimination is not specific to the published parent assignment. For PKS\,1937$-$101, $T_{\rm parent} = 59.00 < T_{\rm obs} = 161.31$, so the best alternative parent substantially reduces the statistic, but the result remains significant. For J1332$+$0052, $T_{\rm parent} = 135.76 < T_{\rm obs} = 136.97$, so the best alternative parent slightly reduces the statistic. In all three cases, the free-H model is significantly preferred even under the most favorable parent assignment for D. The parent-reassignment statistic is therefore the conservative quantity to calibrate, and the $p_{\rm parent}$ values reported below should be interpreted as the significance under the most favorable parent assignment for D.

**Parent-identity diagnostic (Gate 7).** Under the isotope-D interpretation, the best alternative parent $j^*$ (the H I component maximizing $\ln L(M_D \mid j)$) should be the main narrow thermal component — D is tied to the gas it formed beside. Under TEP, $j^*$ might be a diffuse, low-column edge component — the edge gas anchors to its own local structure. For all three sightlines, the best non-canonical parent within the eligible window ($\log N_{\rm HI} \ge \log N_{\rm max} - 2$\,dex, $|v| \le 1000$\,km/s) is a core component: Q1009+2956 parent 1 ($v = -43.7$\,km/s, $\log N_{\rm HI} = 16.80$, $b = 17.8$\,km/s), PKS\,1937$-$101 parent 20 ($v = +17.9$\,km/s, $\log N_{\rm HI} = 17.38$, $b = 17.1$\,km/s), and J1332$+$0052 parent 2 ($v = +8.7$\,km/s, $\log N_{\rm HI} = 18.39$, $b = 15.8$\,km/s). This is consistent with the isotope-D interpretation and does not support the TEP edge-parent prediction. The parent-identity test is presently treated as a descriptive diagnostic rather than a TEP-specific discriminator. Under TEP the feature is ordinary edge H, not D tied to any parent; the identity of the parent that minimizes a mis-specified D fit may be a fitting artefact rather than a physical TEP observable. A derivation showing why a displaced edge-H feature mathematically causes the false-D likelihood to maximize on diffuse edge components is required before Gate 7 can be elevated to a TEP-specific prediction.

**Offset-exactness test (Gate 4E).** Under the isotope-D interpretation, the free-H component should sit at the exact isotope-shifted velocity $v_{\rm iso} = -81.6$\,km/s relative to its parent. Under TEP, the edge-gas feature need not sit at the exact isotope shift — the observed offset depends on the local shear amplitude, which varies with core-edge geometry. The fitted $M_{H,\rm free}$ velocities deviate from the isotope-shifted position by:

| Sightline | Parent $v$ (km/s) | $v_{\rm iso}$ (km/s) | Expected D $v$ (km/s) | Fitted $v_H$ (km/s) | Deviation (km/s) |
| --- | --- | --- | --- | --- | --- |
| Q1009+2956 | $-52.4$ | $-81.6$ | $-134.0$ | $-131.3$ | $+2.7$ |
| PKS\,1937$-$101 | $+8.7$ | $-81.6$ | $-72.9$ | $-67.3$ | $+5.7$ |
| J1332$+$0052 | $0.0$ | $-81.6$ | $-81.6$ | $-118.2$ | $-36.6$ |

The signed residuals in this table are measured relative to the isotope position, not relative to the parent. Thus the $+2.7$ and $+5.7$\,km/s residuals mean that Q1009+2956 and PKS\,1937$-$101 are slightly less blueward than exact D; they do not represent redward core-edge shifts. All three fitted components remain blueward of their respective parents.

Q1009+2956 sits $2.7$\,km/s from the isotope shift — lying approximately one instrumental Gaussian width ($\sigma_{\rm inst}\simeq2.6\,{\rm km\,s^{-1}}$) from the isotope position, but highly inconsistent when calibrated against the true-D simulation distribution ($\pm 0.2$\,km/s, $p ≤ 0.001$, Section 5.6). PKS\,1937$-$101 deviates by $5.7$\,km/s — also highly significant after calibration ($p ≤ 0.001$). J1332$+$0052 deviates by $-36.6$\,km/s — not individually significant after calibration ($p = 0.094$). The cross-sightline pattern — increasing offset deviation with increasing D column — is quantitatively testable: if the feature is isotope-D, all three should sit at $v_{\rm iso}$ within spectral resolution; under TEP, the offset varies with core-edge geometry. The J1332 feature shows the largest departure from the isotope-shifted position, and it is also the sightline with the highest D column (saturated, $\log N_{\rm D} \approx 14.65$), where the edge-gas interpretation is most physically motivated.

Finally, performing a transition-level leave-one-out (LOO) test reveals where the empirical discrimination resides. The full LOO vector for Q1009+2956 (10 entries: 4 coadd deletions + 6 transition deletions):

| Excluded | Type | $T_{\rm LOO}$ | $\Delta T$ vs $T_{\rm full}$ |
| --- | --- | --- | --- |
| C1x1 coadd | coadd | 125.05 | $-35.98$ |
| C1x2 coadd | coadd | 141.03 | $-20.00$ |
| C5x1 coadd | coadd | 77.31 | $-83.71$ |
| C5x2 coadd | coadd | 139.87 | $-21.16$ |
| Ly$\alpha$ | transition | 34.15 | $-126.88$ |
| Ly$\beta$ | transition | 148.64 | $-12.39$ |
| Ly$\gamma$ | transition | 156.16 | $-4.86$ |
| Ly6 | transition | 160.70 | $-0.33$ |
| Ly13 | transition | 161.05 | $+0.02$ |
| Ly14 | transition | 161.03 | $+0.00$ |

The full LOO vector reveals that the discrimination is strongly concentrated in Ly$\alpha$: removing Ly$\alpha$ *decreases* $T$ from 161.03 to 34.15, indicating that Ly$\alpha$ provides the bulk of the isotope discrimination. This is physically expected: the isotope velocity shift ($-81.6$\,km/s) is the same across all Lyman transitions, but Ly$\alpha$ has the highest oscillator strength and signal-to-noise ratio, yielding the deepest absorption profile and the largest number of informative pixels over which the mass-scaled Doppler difference between H and D accumulates. Ly$\beta$ is the second most important transition ($T_{-\mathrm{Ly}\beta} = 148.64$, $\Delta T = -12.39$), followed by Ly$\gamma$ ($\Delta T = -4.86$). The high-order transitions (Ly6, Ly13, Ly14) contribute negligibly ($|\Delta T| < 0.5$). The coadd deletions show that the C5x1 setting contributes the most discrimination ($\Delta T = -83.71$), followed by C1x1 ($\Delta T = -35.98$). All coadd deletions decrease $T$, confirming that the discrimination is distributed across all four coadd settings rather than being driven by a single dataset. The result demonstrates that a benchmark high-redshift D/H system is not spectroscopically self-authenticating once the displaced-H model class is admitted.

**Velocity-selection theorem (Gate 6).** The strongest objection to the TEP interpretation is that the observed velocity offset matches the exact reduced-mass isotope shift ($-81.6$\,km/s) in all three sightlines. The chance probability of three independent features landing within $\pm 5$\,km/s of the isotope shift is $\sim 10^{-6}$ (assuming a $\pm 500$\,km/s prior range of narrow-component velocities). However, this coincidence is a property of the *selection function*, not of the gas: the D-identification protocol is a filter $|\Delta v - v_{\rm iso}| < \epsilon$ — VPFIT initializes D components at the isotope-shifted velocity, and analysts search for D at that specific offset. Any shear feature at $-40$\,km/s or $-120$\,km/s relative to the core is fitted as an ordinary H I component and never flagged as D. The universality of $-81.6$\,km/s therefore cannot be treated as independent evidence for isotope identity within a sample selected through the isotope-shift criterion; it is true by construction of the sample. The falsifiable prediction is that edge-shear features at other offsets exist and are being absorbed into H I component structure: there should be a population of anomalously narrow "orphan" components in high-S/N LLS spectra whose velocity distribution is broader than the isotope shift and whose columns track the edge-gas prediction.

**Illustrative Population Forecast (Gate 6-II).** An illustrative selection model, calibrated to the three benchmark fitted offsets, gives $\sigma_{\rm shear} \approx 19$\,km/s and an orphan fraction of $\sim 79\%$. Because the benchmark sample is D-selected and the J1332 fitted velocity is width-prior-sensitive, these numbers are exploratory rather than a frozen TEP population prediction. The observed cross-sightline deviations ($+2.7$, $+5.7$, $-36.6$\,km/s for Q1009, PKS\,1937, J1332 respectively) give: the D-search selection function $|\Delta v - v_{\rm iso}| < 5$\,km/s captures only $\sim 21\%$ of edge-shear features; the remaining $\sim 79\%$ are orphans absorbed into the H I component structure. This is not the expected detected fraction: the archival feasibility analysis in §5.7 shows that saturation and forest contamination reduce an 80-sightline parent sample to roughly 10 usable systems, corresponding to approximately two detectable excess candidates. Because the shear width is inferred from only three D-selected systems, this fraction is provisional; the robust TEP prediction is an excess of non-isotope displaced components with the joint edge-gas phenotype relative to a matched conventional H I background. In a sample of $\sim 80$ high-S/N LLS sightlines with full Lyman coverage (SQUAD DR1, UVES SLS, ESPRESSO D/H survey), $\sim 24$ shear features are expected, of which $\sim 5$ are identified as D and $\sim 19$ are orphans. The predicted orphan surface density is $\sim 2.4$ per 10 sightlines at $|\Delta v - v_{\rm iso}| > 5$\,km/s, falling to $\sim 1.8$ per 10 sightlines at $> 10$\,km/s. Orphan features are predicted to have narrow Doppler parameters ($b < 10$\,km/s, cool edge gas), low columns ($\log N_{\rm HI} \sim 12$--$14$), and thermal Doppler regimes — distinguishable from the normal H I population by an excess of narrow, low-column components at non-isotope offsets. Under the isotope-D null, no such excess is expected. This is a targetable observational program using existing archival data.

The embedding pipeline has been generalised to support multiple sightlines via a sightline-configuration system. Two additional benchmark D/H quasar sightlines have now been analysed with the identical model-comparison framework, providing the first cross-sightline application of the TEP spectroscopic methodology. The same spectroscopic framework is applied to the two additional benchmark sightlines in §2.4; their cross-sightline amplitude comparison is presented in §3.3.

### 2.4 Cross-Sightline Validation

The identical Gate 2/3 pipeline was applied to PKS 1937$-$101 (Cooke et al. 2024 <sup>[66]</sup>; ESPRESSO, $R=70\,000$, $z_{\rm abs}=3.572$) and J1332$+$0052 (Kislitsyn et al. 2024 <sup>[67]</sup>; joint UVES+HIRES, $R\approx50\,800$ and $49\,200$, $z_{\rm abs}=3.421$). Both sightlines were analysed with all available Lyman transitions covered by their spectral data (13 for PKS 1937$-$101, 12 for J1332$+$0052 which lacks Ly$\alpha$ coverage), the same noise-model calibration, and the same 1000-realization Monte Carlo protocol.

| Sightline | $z_{\rm abs}$ | Instrument | $T_{\rm obs}$ | $T_{\rm parent}$ | $p_{\rm std}$ | $p_{\rm parent}$ | Doppler regime | Interpretive status (conservative) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Q1009$+$2956 | 2.5042 | Keck/HIRES | 161.03 | 161.03 | 0.001 (0/1000) | 0.001 (0/1000) | Mixed ($b_{\rm turb}/b_{\rm therm} \approx 2.02$, $0.10\sigma$) | Significant; free-H preferred even under most favorable parent |
| PKS 1937$-$101 | 3.572 | ESPRESSO | 161.31 | 59.00 | 0.001 (0/1000) | 0.001 (0/1000) | Thermal | Significant; free-H preferred even under most favorable parent |
| J1332$+$0052 | 3.421 | UVES+HIRES | 136.97 | 135.76 | 0.001 (0/1000) | 0.001 (0/1000) | Turbulent, saturated ($b_{\rm turb} \approx 50$\,km/s at bound, no Ly$\alpha$ coverage; boundary check in §5.6) | Significant; free-H preferred even under most favorable parent |

$^{\dagger}$ For J1332$+$0052, the canonical-parent standard statistic is reported as the primary $p_{\rm std}$ for consistency with Q1009 and PKS\,1937. Both definitions yield significant results for J1332$+$0052; the canonical-parent value is reported in the table for cross-sightline uniformity.

Under the conservative parent-reassignment statistic, the results are: for Q1009+2956, $p_{\rm parent} = 0.001$ (0/1000 exceedances), significant—free-H is preferred even under the most favorable parent assignment. For PKS\,1937$-$101, $p_{\rm parent} = 0.001$ (0/1000 exceedances), significant—free-H is preferred even under the most favorable parent assignment. For J1332$+$0052, $p_{\rm parent} = 0.001$ (0/1000 exceedances), significant—free-H is preferred even under the most favorable parent assignment. The standard (canonical-parent) statistic yields $p_{\rm std} = 0.001$ (0/1000) for all three sightlines. The common free-H preference across all three sightlines provides the displaced-H phenomenology to which the TEP interpretation is subsequently applied. A cross-sightline amplitude ranking from the density-weighted Green function $K$ is computed in Section 3.3 (Gate 5).

**Multiplicity correction.** The primary confirmatory family comprises the six Gate 2/3 statistics and is Bonferroni-corrected at $\alpha/6=0.0083$; all six survive. Gate 8 consists of three secondary correlated multivariate diagnostics derived from the same fitted spectra and is reported separately, not added to the primary family as independent confirmation. Correcting the three Gate-8 joint statistics among themselves gives $\alpha/3=0.0167$, under which the calibrated joint results for Q1009+2956 ($p ≤ 0.001$) and PKS\,1937$-$101 ($p ≤ 0.001$) remain significant; J1332$+$0052 ($p = 0.023$) is significant at the uncorrected $\alpha = 0.05$ level but does not survive the corrected threshold. Parent maximization is already inside $T_{\rm parent}$ and its Monte Carlo calibration; it is not a further Bonferroni factor.

Three critical analysis issues were identified and fixed during this work: (1) the continuum basis was made dynamic — 10 parameters for broad Ly$\alpha$ regions (where the H I wing requires flexible continuum separation from the narrow D feature) and 5 parameters for narrow metal-line regions (where 10 parameters would overfit and act as a mathematical sponge, absorbing isotopic discrepancies and artificially depressing $T$); (2) the isotope identifiability calculation was corrected to use mass-scaled Doppler parameters at the actual D column ($N_{\rm D} = 5.7\times10^{12}\,\mathrm{cm}^{-2}$), revealing that H and D are marginally distinguishable at $0.52\sigma$ in the thermal regime and indistinguishable at $0.10\sigma$ in the mixed regime; and (3) the parent-reassignment interpretation was corrected: a non-significant $p_{\rm parent}$ indicates that D with an alternative parent is statistically indistinguishable from free-H, which does not exclude the deuterium interpretation but does not independently support it either.

## 3. Scalar Field Dynamics and Temporal Shear <sup>[53]</sup>

*Part I: Local Absorber Physics.* Sections 2–3 establish the spectroscopic analysis and the local temporal-shear mechanism for the deuterium-like velocity offset. These results stand independently of the broader cosmological framework in Part II (Sections 4–6), which addresses the global consequences of dynamical proper time for cosmology, light-element synthesis, and the thermal history of the universe.

The free-H preference motivates a separate physical question: whether TEP can provide a non-kinematic contribution to the displaced-H phenomenology. TEP does not predict the isotope constant; it predicts geometry-dependent temporal shifts, while the D-search protocol preferentially selects features lying near the $-81.6\,{\rm km\,s^{-1}}$ isotope window.

### 3.1 Field-Theoretic Derivation

In TEP, gravity is governed by a Lorentzian metric $g_{\mu\nu}$, while matter couples to a causal effective metric $\tilde{g}_{\mu\nu}$ determined by the scalar field $\phi$, analogous to screened scalar-field frameworks <sup>[35], [36]</sup>. The interaction is defined by the action:

\begin{equation} S_{\rm TEP} = \int d^4x\sqrt{-g} \left[ \frac{M_{\rm Pl}^2}{2}R - \frac{1}{2}\nabla_\mu\phi\nabla^\mu\phi - V(\phi) \right] + S_m[\tilde g_{\mu\nu},\psi], \end{equation}

where the TEP matter metric is defined by $\tilde{g}_{\mu\nu} = A^2(\phi) g_{\mu\nu} + B(\phi) \nabla_\mu \phi \nabla_\nu \phi$. In the static weak-field limit relevant to absorber clouds, the disformal term $B(\phi)\nabla_\mu\phi\nabla_\nu\phi$ contributes to spatial geodesics and light propagation but is negligible for $g_{\mu 0}$ (taking the local perturbation $\partial_0\delta\phi \simeq 0$; the non-zero cosmological background derivative $\partial_0\bar\phi$ is treated separately in Gate 4B-IV), so it does not affect clock rates directly. Varying this action with respect to $\phi$ ($\frac{\delta S_{\rm TEP}}{\delta\phi}=0$) over a localized static absorber yields the scalar equation of motion:

**Equation of Motion:**

\begin{equation} (-\nabla^2 + m_{\rm eff}^2)\,\delta\phi = -\frac{\beta_A}{M_{\rm Pl}}\rho, \end{equation}

where $m_{\rm eff}^2 = V_{\rm eff}''(\bar\phi) > 0$ is the effective scalar mass squared, obtained from the second derivative of the effective potential expanded about the background value $\bar\phi$. In the unscreened regime ($|\Phi|/c^2 \ll \Phi_{\rm half}$), $m_{\rm eff}^2 \to 0$ and the Green operator $G_+$ reduces to the massless Poisson kernel; in the screened regime ($|\Phi|/c^2 \gg \Phi_{\rm half}$), $m_{\rm eff}^2$ is large and the response is Yukawa-suppressed. The bare conformal coupling $\beta_A = -1.0$ <sup>[3], [54]</sup> applies in the unscreened absorber regime; the Solar-System source-charge response is $\alpha_{\rm eff}=S_\Sigma^{(\odot)}\beta_A$, with Cassini requiring $|\alpha_{\rm eff}|\lesssim3.4\times10^{-3}$; the illustrative Gate-4B consistency profile below uses $S_\Sigma^{(\odot)}=5.3\times10^{-4}$.

Solving via the conventional positive Green operator $G_+(\mathbf{x},\mathbf{x}')$ for the screened static scalar, define the density-weighted Green integral
$K(\mathbf{x}) = \int G_+(\mathbf{x},\mathbf{x}')\rho(\mathbf{x}')\,d^3x' > 0$,
which already contains the matter density. The core scalar response is then $\delta\phi_{\rm core} = -(\beta_A/M_{\rm Pl})\,K$, confirming that the local clock rate $A(\phi)$ is systematically deformed inside the cloud relative to the cosmological background. This deformation supplies the conformal clock contribution to the candidate spectral shift quantified below.

**Screening convention.** This paper uses the absorber-regime amplitude projection $S_A^{\rm abs}(|\Phi|/c^2)$, for which diffuse Lyman-limit systems are effectively unscreened. This is distinct from the source-charge projection $S_\Sigma$ constrained by Solar-System tests. The relation between these projections must ultimately follow from the common microscopic scalar solution and is not derived here. The numerical absorber law used below is therefore a benchmark amplitude prescription, not a universal screening operator.

### 3.2 Sign Provenance and the Core–Edge Geometry

To ensure a genuinely deterministic sign prediction, the geometric and observational conventions are frozen prior to evaluating the candidate feature:

- **Line-of-Sight (LOS) Orientation:** Positive outward from the observer.

- **Reference Component:** The dense center of the neutral hydrogen absorber — the most redshifted component, serving as the system redshift anchor.

- **Candidate Component:** The diffuse outer regions of the absorber, where the density contrast relative to the cosmological background is small.

- **Fundamental Coupling:** The conformal coupling $\beta_A$ ($A=e^{\beta_A\phi/M_{\rm Pl}}$) enters the clock shift quadratically ($\propto \beta_A^2$). The sign of the blueward displacement is therefore robust to the sign of $\beta_A$: any non-zero linear conformal coupling produces the same blueward sign. This makes the sign prediction robust within the conformal coupling class, though not unique to TEP — any scalar-tensor theory with a linear conformal coupling produces the same sign. The TEP-specific discriminator is the amplitude (Gate 4B), not the sign.

- **Stress-Energy Trace:** With metric signature $(-,+,+,+)$, the non-relativistic matter trace is $T^{(m)} = -\rho < 0$.

- **Definition of Difference:** $\Delta \ln A_{\rm abs} \equiv \ln \frac{A(\phi_{\rm edge})}{A(\phi_{\rm core})}$. This separates the local absorber shear ($\Delta \ln A_{\rm abs}$) from the global cosmological endpoint map ($A_{\rm clock}$).

- **Velocity Sign Convention:** $\Delta v_T \simeq -c \Delta \ln A_{\rm abs}$ (with $\Delta v_T < 0$ defined as blueward relative to the core).

The sign of the temporal shift must emerge directly from the field equation rather than being assumed. Using the screened scalar EOM with the positive Green operator, the deterministic chain is:

\begin{aligned}
K &= \int G_+(\mathbf{x},\mathbf{x}')\,\rho(\mathbf{x}')\,d^3x' > 0, \\[4pt]
\delta\phi_{\rm core} &= -\frac{\beta_A}{M_{\rm Pl}}\,K, \\[4pt]
\Delta\ln A_{\rm core} &= \frac{\beta_A}{M_{\rm Pl}}\,\delta\phi_{\rm core} = -\frac{\beta_A^2\,K}{M_{\rm Pl}^2} < 0.
\end{aligned}

For any non-zero conformal coupling ($\beta_A \neq 0$) and positive density-weighted Green integral ($K > 0$), the core clock rate is suppressed. Crucially, the dependence is quadratic in $\beta_A$: the sign of $\Delta\ln A_{\rm core}$ does not depend on the sign of $\beta_A$, but follows from $\beta_A^2 > 0$.

\begin{equation} \Delta\ln A_{\rm core} = -\frac{\beta_A^2\,K}{M_{\rm Pl}^2} < 0. \end{equation}

The dense core is therefore the most redshifted component of the absorption
system. The diffuse outer regions, where the density contrast relative to
the background is small, experience a negligible clock shift
($\Delta\ln A_{\rm edge} \approx 0$). This assumes a radially
monotonic density profile ($\partial\rho/\partial r < 0$ from core to
edge), consistent with the gravitationally stratified structure of
Lyman-limit absorbers, so that the scalar response $\Delta\phi$ decays
smoothly outward and the edge clock shift vanishes to leading order.
When the core is adopted as the
system redshift anchor — the standard practice for absorption-line
analysis, where the deepest component defines the systemic redshift —
the diffuse edge appears blueshifted relative to the core:

\begin{equation} \Delta\ln A_{\rm abs} = \ln\frac{A(\phi_{\rm edge})}{A(\phi_{\rm core})} \approx -\Delta\ln A_{\rm core} > 0, \qquad \Delta v_T = -c\,\Delta\ln A_{\rm abs} < 0 \;\text{(blueward)}. \end{equation}

The TEP field equations deterministically require $\Delta v_T < 0$ for
the diffuse edge relative to the dense core, predicting the
characteristic blueward shift observed in the putative deuterium
windows. The sign emerges from $\beta_A^2 > 0$ combined with the
edge-minus-core convention: the dense core is the most redshifted
reference, and the less shifted diffuse edge appears blueshifted
relative to it. The sign does not depend on the sign of $\beta_A$
directly, but follows from the quadratic coupling and the
observational convention that the core defines the systemic redshift.

Treating the sign and amplitude as distinct predictions, the conformal absorber solution fixes the blueward sign of the core-edge clock deformation. The sign is a consistency prediction rather than a unique TEP discriminator; the quantitative test is whether the full matter metric can reproduce the observed amplitude and its variation between sightlines.

### 3.3 Amplitude Test: Frozen-$\beta_A$ Calculation (Gate 4B)

The sign derivation above establishes the direction of the clock shift but not the magnitude of the observed velocity. A quantitative amplitude test (Gate 4B) freezes the bare conformal coupling $\beta_A = -1.0$ from the TEP corpus <sup>[3], [54]</sup> and constructs the density-weighted Green integral $K$ from actual Q1009+2956 observables. The Q1009+2956 D/H absorber is a Lyman Limit System (LLS) with $\log N_{\rm HI} = 17.362 \pm 0.005$ <sup>[44]</sup>, $z_{\rm abs} = 2.5042$.

Because the scalar field couples to the *total* mass density $\rho$ (not just neutral hydrogen), $N_{\rm HI}$ cannot be used directly. An ionisation correction is required to derive the total hydrogen column $N_{\rm H}$. Under photoionisation equilibrium with the UV background at $z \sim 2.5$ <sup>[55]</sup>, the neutral fraction is $x_{\rm HI} = \alpha_{\rm rec}\,n_e / \Gamma$, where $\Gamma \approx 10^{-12}\text{ s}^{-1}$ is the photoionisation rate and $\alpha_{\rm rec} \approx 2.6 \times 10^{-13}\text{ cm}^3\text{/s}$ is the recombination coefficient at $T \sim 10^4$ K. Solving for $N_{\rm H}$ with $n_e \approx n_{\rm H} = N_{\rm H}/(2R)$:

\begin{equation} N_{\rm H} = \sqrt{\frac{N_{\rm HI} \cdot 2R \cdot \Gamma}{\alpha_{\rm rec}}}. \end{equation}

For a uniform sphere with the standard Poisson Green function, $K_{\rm Poisson}/M_{\rm Pl}^2 = 2|\Phi|/c^2$, where $|\Phi| = \pi G m_p N_{\rm H} R$ is the Newtonian potential at the centre. The conformal-only prediction is:

\begin{equation} |\Delta v_{\rm conf}| = c\,\beta_A^2\,\frac{K_{\rm Poisson}}{M_{\rm Pl}^2} = \frac{2\beta_A^2 \pi G m_p N_{\rm H} R}{c}. \end{equation}

The absorber radius $R$ is not directly measured for Q1009+2956. The main D/H components span $\Delta v \approx 13\text{ km/s}$ in velocity <sup>[44]</sup>, which constrains the absorber size through the virial relation but does not determine it uniquely. Results are therefore presented as a function of $R$. For a representative $R = 30$ kpc, the uniform-sphere ionisation correction gives $\log N_{\rm H} \approx 20.6$ ($x_{\rm HI} \approx 6 \times 10^{-4}$), yielding $|\Delta v_{\rm conf}| \approx 0.009\text{ km/s}$. This conformal-only scale is far below the wavelength-calibration/systematic floor of the present spectra and is not separately detectable in these data. It should therefore be interpreted as the calculated signed baseline of the TEP absorber field, not as an observed spectral shift.

**Cross-sightline amplitude ranking (Gate 5).** The conformal-only amplitude calculation is extended to all three benchmark sightlines using the same ionisation correction and uniform-sphere geometry at $R = 30$ kpc. The ratio $\mathcal{A}_{\rm env}\equiv|\Delta v_H|/|\Delta v_{\rm conf}|$ is a conditional diagnostic. If the full fitted free-H displacement is attributed to TEP rather than ordinary gas kinematics, it measures the additional non-conformal contribution required relative to the conformal baseline. It is not itself an observed amplification factor or an independent measurement of the TEP field. The ratio varies across sightlines by a factor of $\sim 9$:

| Sightline | $\log N_{\rm HI}$ | $\log N_{\rm H}$ | $|\Delta v_{\rm conf}|$ (km/s) | $\mathcal{A}_{\rm env}$ (disformal/conformal) | Fitted $\Delta v_H$ |
| --- | --- | --- | --- | --- | --- |
| Q1009+2956 | 17.36 | 20.61 | 0.009 | $\sim 9.0\times10^3$ | $-78.9$ km/s |
| PKS\,1937$-$101 | 17.92 | 20.89 | 0.017 | $\sim 4.5\times10^3$ | $-76.0$ km/s |
| J1332$+$0052 | 19.25 | 21.55 | 0.077 | $\sim 1.5\times10^3$ | $-118.0$ km/s |

The $\mathcal{A}_{\rm env}$ values in this table use the Poisson Green function with the ionisation-corrected neutral-hydrogen column as the source density (the &ldquo;gas-column basis&rdquo;). The halo-mass calculation (Gate 4B-0-III below) uses the total host halo mass as the source density and gives $|\Delta v_{\rm conf}| \approx 0.005$\,km/s for all three sightlines (same $10^{10}\,M_\odot$ host), corresponding to $\mathcal{A}_{\rm env} \approx 1.6$--$2.5 \times 10^4$. The halo-mass basis provides a more complete total-gravitating-mass benchmark within this stress test, while remaining a conventional proxy rather than a TEP-native source solution. Both bases are retained because the gas-column calculation provides the per-sightline ranking while the halo-mass calculation provides the total-mass benchmark amplitude.

A universal $\mathcal{A}_{\rm env}$ — which is what a geometry-independent transport path $\mathcal{C}_{T,\parallel}$ most naturally provides — is excluded at face value: applying Q1009's $\mathcal{A}_{\rm env} \approx 9.0\times10^3$ to all three sightlines would predict offsets of $-79$, $-151$, and $-694$\,km/s, whereas the fitted free-H displacements are $-78.9$, $-76.0$, and $-118.2$\,km/s. Under the limiting pure-TEP attribution, TEP must account for the unrestricted-H displacement rather than the isotope constant; the per-sightline $\mathcal{A}_{\rm env}$ values quantify the corresponding maximal non-conformal requirement. Two interpretations are consistent with this:

- *Selection theorem (Gate 6):* the observed sample is velocity-selected at the isotope-shifted offset (Section 2.3). The detected subpopulation is precisely the tail where the geometry-dependent TEP offset happens to lie near $v_{\rm iso}$. The predicted population scatter is then a feature: TEP predicts a distribution of edge-shear offsets of which the isotope-shifted subset is what gets called "D." The per-sightline $\mathcal{A}_{\rm env}$ values reflect the different core potentials and halo environments.

- *Per-sightline $\mathcal{A}_{\rm env}$:* the ratio is a property of the temporal-disformal transport and varies with the local geometry. This is permitted, but the framework must then predict why $\mathcal{A}_{\rm env}$ anticorrelates with $K$ across sightlines — currently no mechanism is derived.

The decisive empirical test is the orphan population (Gate 6): the velocity-selection theorem predicts that edge-shear features at offsets other than $-81.6$\,km/s exist and are being absorbed into H I component structure. The theoretical test is the three-sightline predictive closure (Gate 4B-IV): a single frozen microscopic $B(\phi)$, combined with independently specified absorber environments, must predict the temporal contribution without using the observed velocities, with the fitted free-H displacements serving as maximal pure-TEP amplitude targets.

**One-line-of-sight transport calculation (Gate 4B-0-III).** A benchmark one-line-of-sight, two-parcel calculation (step\_04g, results/gate4b\_0\_honest\_transport.json) confirms the static-sector predictions of the framework. The scalar field is solved from the Jakarta action with the frozen conformal coupling $\beta_A = -1$ and the named benchmark $V(\phi) = \frac12 m_\phi^2\phi^2$, $B(\phi) = B_0\phi^2$, with $m_\phi$ and $B_0$ taken from external constraints rather than from the observed velocity. The source density is a conventional $10^{10}\,M_\odot$ dynamical host halo mass, employed here as an external benchmark proxy for the total gravitating mass; the TEP-consistent source content (which does not invoke particle dark matter) will be treated in a companion paper. For this benchmark proxy at $R = 30$ kpc, the conformal piece gives $|\Delta v_{\rm conf}| \approx 0.005$\,km/s with the correct blueward sign. Paper 29 screening suppresses massive halos ($M > 10^{11}\,M_\odot$) and leaves intermediate halos ($10^{10}$--$10^{11}\,M_\odot$) weakly screened — exactly the LLS host halo mass range — confirming that the fifth force is strongest where TEP requires it. The screening separation is the central TEP prediction. Using the frozen Paper-0 PPN mapping $\gamma_{\rm PPN} - 1 = -2\alpha_{\rm eff}^2/(1 + \alpha_{\rm eff}^2)$ with $\alpha_{\rm eff} = \mathcal{S}_\Sigma^{(\odot)}\,\alpha_0$, the bare unscreened coupling ($\alpha_{\rm eff} = \alpha_0 = -1$) gives $\gamma_{\rm PPN} - 1 = -1$ in the Solar System, violating the Cassini bound $|\gamma - 1| < 2.3 \times 10^{-5}$ by over four orders of magnitude; with Paper 29 screening at the solar grazing potential $|\Phi_\odot|/c^2 \approx 1.3 \times 10^{-6}$, the source-charge screening factor $\mathcal{S}_\Sigma^{(\odot)} \approx 5.3 \times 10^{-4}$ suppresses the effective coupling to $\alpha_{\rm eff} \approx 5.3 \times 10^{-4}$, giving $\gamma_{\rm PPN} - 1 \approx -5.5 \times 10^{-7}$, so $|\gamma_{\rm PPN} - 1| < 2.3 \times 10^{-5}$ (Cassini PASS). Under the absorber-regime amplitude ansatz, LLS-scale potentials place the absorber in the effectively unscreened limit $S_A^{\rm abs}\approx 1$ at LLS host potentials $|\Phi_{\rm abs}|/c^2 \sim 10^{-8}$, so the bare coupling operates in the absorber regime. Note that the Cassini PPN bound constrains the source-charge projection $\mathcal{S}_\Sigma^{(\odot)}$ (which enters $\gamma_{\rm PPN}$), while the absorber clock shift is governed by the amplitude projection $S_A^{\rm abs}$ (which enters $\Delta\ln A$); the same potential-depth environmental variable characterizes both projections, but their response functions are distinct and are not assumed numerically identical (Jakarta §2.2). This environmental separation — screened in the Solar System, unscreened in diffuse LLS clouds — is not a fine-tuning but a prediction of the TEP screening mechanism. The Cassini grazing ray at $b = 1.6\,R_\odot$ lies inside the solar transition radius $r_{\rm trans} = 13.3\,R_\odot$, but the disformal frequency shift is zero for a static field ($\tilde g_{00} = A^2 g_{00}$ when $\partial_0\phi = 0$), and $D|\nabla\phi|^2 \ll 10^{-15}$ (GW170817 PASS). The static conformal piece provides a signed lower bound; the disformal contribution $\mathcal{A}_{\rm env} \sim 10^4$ would have to arise from the non-static disformal transport path $\mathcal{C}_{T,\parallel}$, the identified Gate 4B channel. The same law applied to all three benchmark sightlines (Q1009+2956, PKS\,1937$-$101, J1332$+$0052) with no retuning gives the same conformal lower bound, confirming that the static sector is consistent across the sample.

**Disformal clock mechanism: cosmological $\partial_0\bar\phi$ channel (Gate 4B-IV).** The static-field calculation above correctly identifies that the disformal $g_{00}$ contribution vanishes when $\partial_0\phi = 0$. However, the v0.11 cosmological architecture $1+z = A_0/A_{\rm em} = \exp(|\beta_A|\,\phi/M_{\rm Pl})$ requires a non-zero cosmological time derivative of the scalar field. Defining the TEP temporal-rate function $H_T(z) \equiv -d\ln A/dt$, the scalar background satisfies $\dot{\bar\phi} = M_{\rm Pl}\,H_T(z)$, so for $A = e^{-\phi/M_{\rm Pl}}$ (step\_04h, results/gate4b\_disformal\_clock.json). The cosmological time derivative activates a disformal $g_{00}$ term that is the candidate amplitude mechanism to the TEP velocity shift. TEP predicts a geometry-dependent $\Delta v_T$, not a universal $-81.6$\,km/s shift; the $-81.6$\,km/s clustering is explained by the velocity-selection theorem (Gate 6-I) as a selection effect of the D-search protocol. The maximal amplitude targets under a pure-TEP attribution are the fitted free-H displacements: $-78.9$, $-76.0$, $-118.0$\,km/s for Q1009+2956, PKS\,1937$-$101, and J1332$+$0052 respectively.

\begin{equation} \partial_0\bar\phi = M_{\rm Pl}\,H_T(z) \neq 0. \end{equation}

For the reconstructed TEP background used in this calculation, $H_T(z)$ is identified with the effective observational Hubble-rate function corresponding to the fitted distance-redshift relation. At the absorber redshift $z = 2.5042$, the cosmological field is $\bar\phi/M_{\rm Pl} = \ln(1+z)/|\beta_A| = 1.254$, and the cosmological time derivative is $\partial_0\bar\phi = M_{\rm Pl}\,H_T(z) = 1.34 \times 10^{-5}\text{ eV}^2$. The total scalar field at the absorber is $\phi = \bar\phi(t) + \delta\phi(r)$, where the local perturbation $\delta\phi/M_{\rm Pl} \sim 10^{-8}$ is the Poisson-sourced contribution from the host halo. The cosmological time derivative activates the disformal $g_{00}$ term:

\begin{equation} \tilde g_{00} = A^2\,g_{00} + B(\phi)\,(\partial_0\bar\phi)^2, \end{equation}

producing a differential clock shift between core and edge. The exact matter-metric lapse is $N^2(\phi) = A^2 - B(\phi)\,(\partial_0\bar\phi)^2$, and the exact core-edge clock difference is:

\begin{equation} \Delta_{\rm ec}^{\rm clock} = \ln\frac{N_{\rm edge}}{N_{\rm core}} = \frac12 \ln\frac{A^2 - B_{\rm edge}\,(\partial_0\bar\phi)^2}{A^2 - B_{\rm core}\,(\partial_0\bar\phi)^2}. \end{equation}

With $B(\phi) = B_0(\phi/M_{\rm Pl})^n$ and the cross-term expansion $B(\phi_{\rm core}) - B(\phi_{\rm edge}) \approx n\,B_0\,(\bar\phi/M_{\rm Pl})^{n-1}\,\Delta(\delta\phi/M_{\rm Pl})$, the first-order expansion gives the linearized velocity shift:

\begin{equation} \frac{|\Delta v|}{c} \simeq \frac{n}{2}\,B_0\,\left(\frac{\bar\phi}{M_{\rm Pl}}\right)^{n-1}\,\Delta\!\left(\frac{\delta\phi}{M_{\rm Pl}}\right)\,\frac{(M_{\rm Pl}\,H_T)^2}{A^2}, \end{equation}

valid only when $B(\phi)\,(\partial_0\bar\phi)^2/A^2 \ll 1$. The exact matter-metric lapse is $N^2(\phi) = A^2 - B(\phi)\,(\partial_0\bar\phi)^2$, and the exact core-edge clock difference is $\Delta_{\rm ec}^{\rm clock} = \frac12 \ln\frac{N_{\rm edge}^2}{N_{\rm core}^2}$. The exact solution, obtained by solving $-c\,\Delta_{\rm ec}^{\rm clock} = \Delta v$ for $B_0$ subject to the Lorentzian condition $N^2 > 0$, gives $B_0 = B_0^{\rm lin}/(1 + \beta\,B_0^{\rm lin})$ where $\beta = (\bar\phi/M_{\rm Pl})^n\,(M_{\rm Pl}\,H_T)^2/A^2$ and $B_0^{\rm lin}$ is the linearized value.

**Pure-TEP amplitude stress test.** The exact-lapse equation has a divergence: as $B_0 \to 1/\beta$, the invariant $\mathcal{I} = 1 - B(\bar\phi)\,(\partial_0\bar\phi)^2/A^2 \to 0$ and the predicted shift $\Delta v \to \infty$. The original analysis targeted the full $81.6$\,km/s isotope shift, but TEP does not predict a universal $-81.6$\,km/s shift; the velocity-selection theorem (Gate 6-I) explains the clustering as a selection effect. Under the limiting pure-TEP attribution, the fitted free-H displacement defines the maximal amplitude target: $78.9$\,km/s for Q1009+2956. The exact-lapse solution under the first-order core-edge field expansion for this target gives $B_0 \sim 10^8$\,eV$^{-4}$ with $\mathcal{I} \sim 10^{-4}$, sitting near the Lorentzian boundary. The near-critical regime is a property of the exact-lapse equation: any target above the linear-regime maximum ($\sim 0.01$\,km/s) drives $B_0$ toward $1/\beta$. Because $B_0$ is inferred here by solving backward from the observed displacement, the near-critical value of $\mathcal{I}$ is a diagnostic property of this ansatz rather than an independent prediction or evidence for TEP. Predictive significance requires $B(\phi)$ to be frozen independently of these velocities.

**Constraint analysis.** The same $B_0$ enters both the temporal disformal term (clock shift, the candidate amplitude contribution) and the spatial disformal term (Shapiro delay, constrained by Cassini). The spatial term at the Sun is $\gamma_{\rm dis} = B(\phi_\odot)\,(\partial_r\phi_\odot)^2/(2U_\odot)$, where $U_\odot = |\Phi_\odot|/c^2 = 2.12 \times 10^{-6}$. For this reduced Solar-System consistency calculation, the nonlinear environmental response is represented phenomenologically by an effective source-charge projection $S_\Sigma^{(\odot)}$. In the microscopic Jakarta formulation, $S_\Sigma$ is not an independent factor inserted into the fundamental scalar source equation; it is an observable projection of the environment-dependent scalar solution. The reduced solution gives $\phi_\odot/M_{\rm Pl} = 2.26 \times 10^{-10}$, with $\partial_r\phi_\odot = 156\text{ eV}^2$. For the quadratic continuation $n = 2$, the exact-lapse $B_0 = 2.88 \times 10^{8}\text{ eV}^{-4}$ gives $\gamma_{\rm dis} \approx 8.4 \times 10^{-2}$, exceeding the Cassini bound $|\gamma - 1| < 2.3 \times 10^{-5}$ by a factor $\sim 10^3$. The quadratic $B \propto \phi^2$ realization at the normalization required to reproduce the Q1009 amplitude remains incompatible with Cassini even with the exact lapse. A steeper field dependence can satisfy the local Cassini, GW170817 and clock constraints. For $n = 5$, the Q1009-normalised solution gives $\gamma_{\rm dis}\approx4.9\times10^{-31}$, $\delta c/c\approx8.6\times10^{-20}$, and a negligible local clock shift. However, as shown by the cross-sightline transfer test below, the same $n = 5$ power law loses Lorentzian signature at the two higher-redshift absorbers. Thus $n = 2$ is excluded by local constraints and $n = 5$ by cross-redshift transfer; neither tested power law provides a viable universal microscopic closure. The v0.11 theory states that the microscopic form of $B(\phi)$ is not uniquely frozen; the field-space envelope $B(\phi) = B_0\,\varphi^2/(1+\varphi^2)\exp(-\varphi^4/2\sigma_B^4)$ with $\varphi \equiv \phi/M_{\rm Pl}$ is a named benchmark, not a unique prediction. The Cassini and three-sightline constraints derived here bound the still-open $B(\phi)$ closure: the quadratic realization at the required normalization is excluded, and the combined constraints sharply restrict the still-open microscopic $B(\phi)$ closure.

For this Gate-IV consistency calculation an illustrative Solar-System source-charge profile is adopted with $\mathcal{S}_\Sigma^{(\odot)} = 5.3 \times 10^{-4}$, safely below the Cassini ceiling $3.4 \times 10^{-3}$. This value is not inferred from the absorber $S_A^{\rm abs}$ ansatz.

**Three-sightline test: diagnostic, transfer, and predictive closure.** The test is performed in three stages. *Diagnostic mode*: infer $B_0$ per sightline from the fitted free-H displacement. Each sightline admits an individually fitted Lorentzian solution ($\mathcal{I} > 0$), establishing algebraic feasibility of the temporal-disformal channel under this ansatz. The inferred $B_0$ values are $1.46 \times 10^8$, $1.52 \times 10^7$, and $2.00 \times 10^7$\,eV$^{-4}$ for Q1009+2956, PKS\,1937$-$101, and J1332$+$0052 respectively. *Transfer mode*: freeze a single $B_0$ from Q1009+2956 and transfer it unchanged to the other two sightlines. The invariant $\mathcal{I} = 1 - \beta(z)\,B_0$ depends only on the cosmological background ($\beta(z) = (\bar\phi/M_{\rm Pl})^n\,(M_{\rm Pl}\,H_T)^2/A^2$), not on the halo environment. With $B_0$ from Q1009+2956 ($z = 2.5042$), the invariant becomes $\mathcal{I} < 0$ at PKS\,1937$-$101 ($z = 3.572$) and J1332$+$0052 ($z = 3.421$), crossing the Lorentzian boundary. This signature change is a constraint on the microscopic form of $B(\phi)$: the simple power-law $B(\phi) \propto \phi^5$ calibrated at $z = 2.5$ does not transfer to $z > 3.4$. This is a failure of that particular transfer ansatz, not a falsification of the temporal-disformal channel. *Predictive closure* (not yet performed): with a single independently frozen microscopic $B(\phi)$ and independently specified absorber environments for each sightline, predict $\Delta v_T$ without using any of the three observed velocities. The decisive test is whether such a calculation predicts the temporal contribution without using the observed velocities, with the fitted free-H displacements providing the limiting pure-TEP amplitude targets.

**Limit of the reduced Gate-4B closure.** The failed power-law transfer constrains the specific reduced construction tested here; it does not yet determine the outcome of the full TEP matter-frame transport problem. The present calculation represents the cosmological scalar evolution through an effective background-rate function and reduces the absorber observable to a core-edge lapse difference. In the static-space TEP formulation, predictive closure requires instead a TEP-native background solution $\bar\phi(t)$, an inhomogeneous absorber solution $\delta\phi(x)$, and covariant propagation of the photon through the complete matter metric, with the measured frequency evaluated as $\omega=-u^\mu k_\mu$. Whether the near-criticality and cross-redshift signature loss persist under that calculation is therefore an open, directly testable theoretical question.

**Environmental discrimination.** Solar-System and absorber observables probe distinct projections of the same environment-dependent scalar configuration. Cassini constrains the source-charge projection $S_\Sigma^{(\odot)}$, whereas conformal clock amplitudes depend on $S_A$. Their numerical relationship is not assumed here and must emerge from the common nonlinear scalar solution. The reduced Gate-4B calculation shows that a temporal-disformal contribution can be large in the absorber parametrisation while remaining constrained locally, but the successful microscopic $B(\phi)$ and full covariant transport remain open.

**Gate 4B status.** The conformal field fixes the sign but gives only $0.005$--$0.01\,{\rm km\,s^{-1}}$. Static perturbative disformal terms are also insufficient. The cosmological temporal-disformal term $B(\phi)\dot{\bar\phi}^{\,2}$ can reach much larger amplitudes in the Einstein-frame parametrisation explored here, although the solutions are near-critical. Individually fitted sightlines demonstrate algebraic feasibility, while the simple $B(\phi)\propto\phi^5$ form fails the cross-redshift transfer test. Predictive closure therefore requires one microscopic $B(\phi)$, fixed independently of the observed velocities, and evaluation of the covariant matter-frame frequency $\omega=-u^\mu k_\mu$.

**Functional constraints on $S_A^{\rm abs}$ and $S_\Sigma^{(\odot)}$.** The amplitude and source-charge projections must satisfy their respective boundary conditions:

- **Absorber regime (unscreened):** $|\Phi_{\rm abs}|/c^2 \sim 10^{-8} \Rightarrow S_A^{\rm abs} \approx 1$, so that the bare coupling $\alpha_{A,\rm eff} = S_A^{\rm abs}\alpha_0 = -1.0$ applies and the conformal/static branch sign theorem remains valid.

- **Solar-system regime (Cassini):** $|\Phi_\odot|/c^2 \sim 10^{-6} \Rightarrow S_\Sigma^{(\odot)} \lesssim 3.4 \times 10^{-3}$, so that the screened source-charge response $\alpha_{\rm eff}^{\rm PPN} = S_\Sigma^{(\odot)}\,\alpha_0$ satisfies the Cassini PPN bound $|\gamma_{\rm PPN} - 1| < 2.3 \times 10^{-5}$.

- **Disformal contribution target:** Under a pure-TEP attribution, the temporal-disformal channel would need to supply a geometry-dependent contribution $\mathcal{A}_{\rm env} \approx 9.0 \times 10^3$ for Q1009+2956 on the gas-column basis ($\sim 10^4$ on the halo-mass basis; per-sightline: $4.5 \times 10^3$, $1.5 \times 10^3$ on the gas-column basis) relative to the conformal-only Poisson calculation, with the fitted free-H displacements as the maximal amplitude targets under a pure-TEP attribution.

The absorber amplitude ansatz $S_A^{\rm abs}(|\Phi|/c^2) = 1/(1 + (|\Phi|/c^2/\Phi_{\rm half})^n)$ with $\Phi_{\rm half} = 1.59 \times 10^{-7}$ and $n = 3.56$ is the *absorber-regime amplitude transfer* employed in this paper. The screening variable for this ansatz is the gravitational potential depth $|\Phi|/c^2$, because the scalar field responds to total mass through the Poisson equation and screening is set by the integrated potential. Cassini independently constrains the source-charge response $S_\Sigma^{(\odot)}$. The relation between $S_A^{\rm abs}$ and $S_\Sigma^{(\odot)}$ is not established by this ansatz. The product $\alpha_{\rm eff}^2 \times |\Phi|/c^2$ peaks in the unscreened intermediate regime ($|\Phi|/c^2 \sim 10^{-7}$), confirming that the fifth force is strongest in diffuse clouds and suppressed in dense environments. The required disformal contribution cannot arise from the conformal sector alone (which gives $S_A^{\rm abs} \approx 1$ in the unscreened regime); it must originate from the disformal sector $B(\phi)\nabla_\mu\phi\nabla_\nu\phi$ and its environmental projection. The conformal/static contribution maps through $\Delta v_{\rm conf}\simeq-c\,\Delta\ln A$. The temporal-disformal contribution instead modifies the matter-frame lapse $N^2=A^2-B(\phi)\dot{\bar\phi}^{\,2}$; its observable spectral shift must be derived from the covariant frequency $\omega=-u^\mu k_\mu$. No identification of the disformal contribution with $-c\Delta\ln A$ is assumed. For the quasistatic local perturbation, $\partial_0\delta\phi \simeq 0$, so the static disformal term does not modify $g_{00}$. The cosmological background has $\partial_0\bar\phi \neq 0$, activating the distinct temporal-disformal clock channel tested in Gate 4B-IV. The perturbative weak-field disformal term is suppressed by $(|\Phi|/c^2)^2$ for a constant coupling and by $(\nabla\psi/\psi)^2 \ll 1/r^2$ for an inverse-field coupling (the potential is nearly flat in the interior of an extended mass distribution); no local perturbative $B(\phi)$ can provide the required disformal contribution (quantitatively confirmed: the disformal metric correction $B_0 \cdot (|\Phi|/c^2)^2/r^2 \sim 10^{-62}$ in geometrized units for $B_0 = 1$). The static spatial perturbative disformal channels are excluded (Gate 4B-II). The temporal disformal clock channel $B(\phi)(\partial_0\bar\phi)^2$ activated by the cosmological scalar time derivative is the candidate amplitude mechanism (Gate 4B-IV). The full covariant core-edge observable $\omega = -u^\mu k_\mu$ remains to be closed.

**Note on coupling conventions.** Following Paper 0, the frozen microscopic coupling is $\alpha_0 = \beta_A = -1.0$ <sup>[3], [54]</sup>. The environmentally screened effective scalar charge for source-charge/fifth-force observables is $\alpha_{\rm eff} = S_\Sigma(\mathcal{E})\,\alpha_0$ <sup>[1]</sup>; the environmentally screened effective amplitude for clock/Cepheid observables is $\alpha_{A,\rm eff} = S_A(\mathcal{E})\,\alpha_0$. These are distinct projections. The absorber-regime screening variable is the gravitational potential depth $|\Phi|/c^2$: the scalar field responds to total mass through the Poisson equation, and screening is set by the integrated potential. Lyman-limit absorbers ($|\Phi_{\rm abs}|/c^2 \sim 10^{-8}$) sit in the unscreened regime where $S_A^{\rm abs} \approx 1$ and the bare coupling applies. No numerical galactic $S_A$ anchor is assumed in the present calculation; the relation between weak-field conventions across the TEP corpus remains part of the common microscopic closure. The potential-depth law is a phenomenological amplitude-transfer ansatz for the absorber calculation. Cassini independently constrains the source-charge response $S_\Sigma^{(\odot)} \lesssim 3.4 \times 10^{-3}$. The relation between $S_A$ and $S_\Sigma$ must be derived from the common microscopic scalar solution and is not established by this two-parameter fit. The TEP coupling is screened in dense environments by construction, satisfying solar-system bounds (Cassini); in the unscreened absorber regime, the bare coupling produces a fifth force comparable to gravity, whose effect on absorber structure and kinematics is a prediction of the framework. Constraints on unscreened scalars in other theoretical frameworks <sup>[56]</sup> assume different screening mechanisms and coupling structures, and are not directly applicable to the TEP coupling, which is screened by the environmental operator rather than by a chameleon or symmetron mechanism.

**Cassini constraint derivation.** The Cassini experiment measured the PPN parameter $\gamma_{\rm PPN} = 1 + (2.1 \pm 2.3) \times 10^{-5}$ <sup>[59]</sup>. Following Paper 0's frozen convention, $\gamma_{\rm PPN} - 1 = -2\alpha_{\rm eff}^2/(1 + \alpha_{\rm eff}^2)$, where $\alpha_{\rm eff} = S_\Sigma\,\alpha_0$ is the environmentally screened effective scalar charge and $\alpha_0 = \beta_A = -1$ is the frozen microscopic coupling. The path-integrated potential along the grazing ray is $|\Phi|/c^2 = GM_\odot/(R_\odot c^2) = 2.12 \times 10^{-6}$ at the solar radius. For $|\alpha_{\rm eff}| \ll 1$, the Cassini bound $|\gamma_{\rm PPN} - 1| < 2.3 \times 10^{-5}$ requires $S_\Sigma^{(\odot)} \lesssim 3.4 \times 10^{-3}$ in the Solar-System environment. This is an independent constraint on the source-charge response $S_\Sigma^{(\odot)}$; it is not used to calibrate the absorber amplitude ansatz $S_A^{\rm abs}$. The relation between $S_A^{\rm abs}$ and $S_\Sigma^{(\odot)}$ must be derived from the common microscopic scalar solution.

**Corpus parallel: the core-vs-disk gradient.** The core–edge geometry — where the densest component is the slowest ($\Delta\ln A < 0$) and serves as the systemic anchor, while the diffuse component appears shifted relative to it — is not unique to the absorber field. A parallel geometry has been noted in the Cepheid distance-ladder sector <sup>[51]</sup>, where the galactic bulge (deep potential, slowest clocks) defines the systemic spectroscopic redshift while Cepheids in the diffuse outer disk are corrected to the rest frame using that bulge-derived redshift. The absorber-field calculation presented here stands independently; the Cepheid parallel is noted as a consistency check on the shared physical principle $\Delta\ln A < 0$, not as proof of the absorber mechanism.

### 3.4 Scaling Consistency: Absorber Clouds vs. Galaxies

A natural concern is whether a scalar mechanism capable of accounting for a $\sim 80\text{ km/s}$ shift across a diffuse gas cloud would produce an unphysically large effect across a massive galaxy. The clock shift for a static configuration with the Poisson Green function is:

\begin{equation} \alpha_{A,\rm eff}\equiv S_A^{\rm abs}\,\alpha_0, \qquad \Delta\ln A = -\frac{\alpha_{A,\rm eff}^2\,K}{M_{\rm Pl}^2} = -\frac{2\,\alpha_{A,\rm eff}^2\,|\Phi|}{c^2}, \end{equation}

The conformal amplitude does not scale with potential depth alone because the effective amplitude projection is environmentally screened. Diffuse absorbers remain effectively unscreened ($S_A^{\rm abs} \approx 1$ at $|\Phi_{\rm abs}|/c^2 \sim 10^{-8}$). Solar-System fifth-force constraints probe the distinct source-charge projection $S_\Sigma$ ($S_\Sigma^{(\odot)} \lesssim 3.4 \times 10^{-3}$). No numerical galactic $S_A$ anchor is assumed here. A common microscopic scalar solution must ultimately derive both projections; this cross-domain closure is not required for the spectroscopic result tested here.

## 4. Cosmological Transport and Thermodynamics

*Part II: Global Cosmology.* The remainder of this paper develops the full TEP cosmological framework—static spatial geometry, temporal transport, thermodynamic history, light-element synthesis, and the optical-depth boundary. These sections build on the local absorber-field results of Part I (Sections 2–3) but address the broader question of whether a static-spatial universe with dynamical proper time can reproduce the observed thermal and chemical history without a primordial hot dense phase.

A key consequence of the Temporal Equivalence Principle is the decoupling of cosmological redshift from the kinematics of spatial volume. TEP does not preserve the standard hot Big Bang thermal history by construction. The cosmological spatial background is static, while proper time is dynamical. Consequently, high redshift does not by itself imply smaller spatial volume, higher local matter density, higher local temperature, or younger physical age. These quantities must be derived independently from the temporal field and the local matter dynamics. The standard thermal history, including recombination <sup>[23], [24], [25]</sup> and the CMB <sup>[19], [20]</sup>, is not assumed but must be independently reconstructed within the TEP framework.

### 4.1 Background Geometry and Thermodynamic Framework (TEP-TH Cross-Reference)

The geometric and thermodynamic foundations of the TEP cosmological framework — the temporal horizon, curvature regularity ($0 < p \le 1/2$, all polynomial curvature invariants vanish), proper-time asymptotic regularity ($\Delta\tau \to \infty$), and CMB blackbody spectral preservation — are established in TEP-TH (Paper 27, <sup>[4]</sup>). The acoustic-sector closure, including $\Omega_b h^2$ determination from Planck peaks and sound-horizon preservation at $<6\text{ ppm}$, is established in TEP-HC (Paper 18, <sup>[3]</sup>) and TEP-C0 (Paper 26, <sup>[2]</sup>), using the line-of-sight integration formalism of Seljak & Zaldarriaga <sup>[26]</sup> as implemented in CLASS <sup>[28]</sup> and hi_class <sup>[29]</sup>, with perturbation theory following the standard formalism <sup>[14], [15]</sup>. The present paper does not re-derive these results; it applies the established framework to the BBN-specific questions of nuclear reaction flows, light-element equilibrium, and D/H spectroscopy.

The essential structural results inherited from TEP-TH are: (i) the effective scale factor $a_{\rm eff} = A_{\rm clock}$ with $A_{\rm clock}(z) = (1+z)^{-1}$; (ii) the redshift decomposition $\ln(1+z_T) = \int_\gamma (\Sigma_\parallel + \mathcal{C}_{T,\parallel})\,d\ell$; and (iii) the temporal horizon limit $A_{\rm clock} \to 0$, $z \to \infty$, $\tau \to \infty$, $\mathcal{K} \to 0$. The BBN-specific convergence conditions — the astration exposure convergence $p + q > 1$ and the Compton-exposure convergence $a + p > 1$ — are introduced in the present paper as requirements on the worldline exposure integrals that govern chemical evolution in an eternal universe; they are not derived in TEP-TH but are consistent with its curvature-regular branch ($p = 0.5$, $q = 0.8$, giving $p + q = 1.3$).

### 4.2 Nuclear Reaction Flows and the Opacity Boundary

Nuclear production in the TEP framework occurs along local matter histories parameterised by proper time $\tau$ and spatial position $x$:

\begin{equation} \frac{dY_i(x)}{d\tau} = \sum_r N_{ir} \lambda_r[T_{\rm loc}(\tau, x), n_{\rm loc}(\tau, x)] \prod_j Y_j^{\nu_{jr}}, \end{equation}

where $Y_i$ is the abundance of species $i$, $N_{ir}$ is the stoichiometric coefficient, $\lambda_r$ is the temperature- and density-dependent reaction rate, and the sum runs over all nuclear reactions $r$. The observed abundance distribution constrains the population of physical histories, not a single cosmic thermal trajectory. The temporal horizon ensures that low-exposure worldlines (those with bounded $\mathcal{E}_{\rm astr}$) remain observationally accessible at high redshift, while the convergence condition $p + q = 1.3 > 1$ guarantees that the integrated astration exposure converges for any individual worldline.

**Opacity boundary and the $\tau(z)$ three-point requirement.**

In the TEP static frame, the comoving path length $\ell(z)$ to the temporal horizon diverges ($\eta \to \infty$ as $A_{\rm clock} \to 0$), and static space removes FLRW $a^{-3}$ dilution of the electron density. The opacity theorem is *conditional*: it requires an asymptotic electron-density bound $n_e(\ell) \gtrsim \ell^{-s}$ with $s \le 1$, ensuring $\int^\infty n_e\,d\ell = \infty$. Under this condition, the Thomson optical depth diverges at high redshift, providing an observable last-scattering boundary without a physical plasma wall. The $\tau(z)$ three-point requirement — reproducing reionization $\tau(z < 7) \approx 0.054$, a last-scattering surface at $\tau \sim 1$, and the trough onset — requires the line-of-sight-weighted $n_e(\ell)$ to rise by $\sim 14\times$ by $z \sim 7$ and $\sim 500\times$ by the LSS relative to today's mean. This is a quantitative, checkable requirement: the LLS/Lyman-forest column-density distribution per redshift provides $n_e(\ell)$ along random sightlines, and inverting the observed absorber statistics into $n_e(\ell)$ and forward-integrating $\tau(\ell)$ confronts the three-point constraint directly. This reconstruction from absorber statistics is the independent derivation that TEP requires and no FLRW paper needs to perform. The Compton-exposure convergence condition ($a + p > 1$) ensures that the divergent optical depth does not Comptonize the CMB spectrum; the full FIRAS verification is established in TEP-TH (Paper 27, Section 6).

### 4.3 Separation of Spatial and Temporal Shear

The two distinct phenomenological manifestations of the scalar field $\phi$ must be distinguished. The cosmological redshift is a global temporal transport mechanism between distant clocks:

\begin{equation} 1+z = \frac{A_{\rm obs}}{A_{\rm em}}, \end{equation}

while the apparent deuterium feature is interpreted in the TEP hypothesis as arising from localized absorber shear. For the local absorber, the conformal/static contribution is $\Delta v_{\rm conf}\simeq-c\,\Delta\ln A$. When the temporal-disformal channel is active, however, the matter-frame lapse becomes $N^2=A^2-B(\phi)\dot{\bar\phi}^{\,2}$, and the complete observable must be obtained from the covariant measured frequency $\omega=-u^\mu k_\mu$. The full absorber displacement is therefore not identified with the conformal expression alone.

These are mathematically independent mechanisms acting on the same scalar field manifold. They decouple the global cosmological chronology from the localized isotopic identification problem, challenging the standard kinematic interpretations.

### 4.4 Primordial Helium Synthesis via Baryonic Cycling

If primordial deuterium is fundamentally a reconstruction artifact—failing the temporal invariance test due to proper-time shear—then the final empirical pillar of hot Big Bang nucleosynthesis is the helium-4 mass fraction ($Y_{\rm p} \approx 0.245$ <sup>[21], [22], [68]</sup>). Without a finite, hot, universally dense origin, the TEP framework must quantitatively demonstrate that this abundance is produced by stellar nucleosynthesis over an unbounded temporal horizon.

Three strict astrophysical constraints required for stellar-origin helium are formally evaluated:

- **Temporal-Horizon Chemical Equilibrium via Proper-Time Reaction Flow:** The proper-time reaction flow equations are evaluated over the temporal domain. Because the temporal horizon acts as an asymptotic observational transport filter—scaling the observable contribution of the infinite past toward zero ($A(\phi) \to 0$)—the local chemical evolution is asymptotically decoupled from the absolute history of the universe. Evaluating the proper-time reaction flow shows that the adopted proper-time reaction-flow model exhibits convergence toward a common asymptotic attractor over the tested initial conditions at the edge of the accessible horizon. Whether the evaluation starts with $Y_0=0.00$ or an extremely dense $Y_0=0.80$, the reaction flow rapidly decays into the equilibrium attractor of $Y_{\rm eq} = 0.247$ at the present day ($\tau = 0$). It is important to recognize that this reaction flow represents a *local galactic patch* experiencing continuous star formation. The pristine global background observed at high redshift is not protected from local chemical accumulation by transport delay alone; rather, pristine absorbers correspond to gas worldlines whose accumulated processing exposure $\mathcal{E}_{\rm astr}$ remains bounded by the convergence condition $p + q > 1$ (Section 4.1). The temporal horizon ensures that such low-exposure worldlines are observationally accessible, but the chemical pristine state is a property of the worldline's local processing history, not of the transport filter.

- **Temporal Horizon Metal Sequestration:** The balance of this equilibrium is achieved via a mix of Very Massive Objects (VMOs) and standard Population II/I stars. Standard stars yield typical return fractions. However, VMOs—which dominate the low-metallicity branch—undergo extreme radiatively-driven winds that successfully eject their helium envelopes ($E_Y > 0$). Upon core collapse, rather than forming a spatial singularity, the core generates a TEP temporal horizon where the local clock rate $A(\phi) \to 0$ relative to the external interstellar medium. This mechanism directly addresses the historical Carr-Bond-Arnett overproduction limit <sup>[57], [58]</sup>: standard stellar synthesis of $\sim 25\%$ helium severely overproduces carbon and oxygen, making a purely stellar helium origin incompatible with observed metal abundances. The TEP temporal-horizon sequestration offers a mechanism to avoid this by trapping the heavy metals ($E_Z \approx 0$) while allowing helium to escape, producing the correct $Y_{\rm p}$ without the metal overproduction that historically ruled out stellar helium synthesis <sup>[60]</sup>.

- **Extreme Transport Delay:** While local time continues normally for the core, any radiation or matter trying to propagate outward from the horizon is subjected to an extreme but finite temporal transport delay. The heavy metals are therefore effectively trapped over relevant external chemical-evolution timescales, making their return fraction to the external ISM negligible ($E_Z \approx 0$). In the present branch, $E_Z \simeq 0$ is the defining metal-sequestration assumption; deriving the corresponding escape fraction from a full temporal-horizon remnant transport solution remains an independent closure requirement.

These mechanics eliminate the need for a spatial singularity, replacing it with a field-theoretic mechanism for chemical evolution. Under the TEP baryonic-cycling and temporal-horizon exposure conditions, the helium-4 mass fraction $Y_{\rm eq} = 0.247$ emerges as the equilibrium of the baryonic-cycling reaction flow under the adopted stellar yields and temporal-horizon metal sequestration. The numerical reaction-flow calculation demonstrates convergence to this equilibrium for the adopted stellar histories, showing that the observed $Y_{\rm p} \approx 0.245$ <sup>[21], [22]</sup> is compatible with stellar nucleosynthesis over an unbounded temporal horizon. The slight offset between the observed target ($Y_{\rm p} \approx 0.245$, PDG/Cyburt standard) and the derived equilibrium ($Y_{\rm eq} = 0.247$) falls well within the systematic uncertainty bounds of the observationally constrained yield parameters $p_Y$ and $R$: a $\pm 0.002$ shift in $Y_{\rm eq}$ is produced by variations in the helium yield per stellar generation and the return fraction that are smaller than the scatter in empirical H II region yield calibrations. The specific equilibrium value is set by the adopted yield parameters ($p_Y$, $R$) and the VMO fraction; the temporal-horizon metal sequestration ($E_Z \to 0$) ensures that the equilibrium is helium-dominated rather than metal-enriched. The yield parameters are not free tunables directed at the $0.247$ target: the helium yield per stellar generation $p_Y$ is constrained by observations of H II regions and stellar population synthesis models, the return fraction $R$ is determined by initial mass function (IMF) integration over independently measured stellar lifetimes and remnant masses, and the VMO fraction $f_{\rm VMO}$ is bounded by the cosmic star-formation history and the observed heavy-element abundance ratio $[\alpha/\mathrm{Fe}]$ in old stellar populations. A complete derivation of $f_{\rm VMO} \simeq 0.994$ from first-principles stellar physics remains an open refinement target. The contraction analysis establishing that $Y_{\rm eq} = 0.247$ is a true attractor independent of initial conditions is reported below in this section, and the sensitivity analysis confirms robustness to physically motivated variations in ($p_Y$, $R$, $f_{\rm VMO}$) within their observationally constrained ranges: $\pm 0.005$ in $R$ produces $\pm 0.002$ in $Y_{\rm eq}$, and $\pm 0.01$ in $f_{\rm VMO}$ produces $\pm 0.002$ in $Y_{\rm eq}$.

**Extension to 3He and 7Li.** The baryonic-cycling framework extends naturally to a multi-species light-element network (3He, 4He, 7Li) under the same temporal-horizon sequestration mechanism. VMO cores trap not only metals but also 3He and 7Li produced in stellar interiors, so only 4He (and residual H) escapes via winds. The equilibrium abundances are $^3{\rm He/H} = 9.0 \times 10^{-6}$ (observed $\sim 1.0 \times 10^{-5}$, ratio 0.90) and $^7{\rm Li/H} = 1.55 \times 10^{-10}$ (observed $1.6 \times 10^{-10}$, ratio 0.97). The TEP equilibrium $^7{\rm Li/H}$ is a factor of $\sim 3.2$ below the standard hot-BBN prediction ($5.0 \times 10^{-10}$), offering a natural pathway to resolve the cosmological lithium problem: the temporal-horizon sequestration of VMO-core 7Li produces less primordial 7Li than hot BBN without requiring additional stellar destruction mechanisms. The convergence condition $p + q = 1.3 > 1$ (Section 4.1) guarantees that the integrated astration exposure is finite. The numerical reaction-flow calculation demonstrates convergence to the fixed point for the adopted stellar histories; the specific $^7{\rm Li/H}$ value is then determined by the multi-species reaction-flow model (VMO-core lithium yield, sequestration partitioning, and astration exposure integral), not by the convergence condition alone.

**The $\Delta Y / \Delta Z$ Slope and H II Region Concordance.** The standard observational method for determining primordial helium extrapolates the linear relationship between helium abundance $Y$ and metallicity $Z$ (typically traced by O/H) across metal-poor dwarf galaxy H II regions to the $Z \to 0$ limit <sup>[61], [62], [63]</sup>. If $Y_{\rm eq} = 0.247$ is a local chemical attractor rather than a universal primordial baseline, the TEP framework must reproduce this observed $\Delta Y / \Delta Z$ linear slope. The baryonic-cycling reaction flow naturally produces a linear $Y$-$Z$ relation at low metallicity: as astration exposure $\mathcal{E}_{\rm astr}$ increases, both $Y$ (from helium-producing stellar winds) and $Z$ (from metal-producing standard stars) increase proportionally, yielding a near-linear slope $\Delta Y / \Delta Z \approx p_Y / (1 - E_Z) \cdot R_{\rm metal}$ that is set by the same yield parameters governing the equilibrium. The temporal-horizon metal sequestration ($E_Z \approx 0$) suppresses the $Z$-intercept while preserving the slope, so the extrapolation to $Z \to 0$ recovers $Y_{\rm eq}$ rather than a distinct "primordial" value. The observed consistency of $\Delta Y / \Delta Z$ across hundreds of independent low-metallicity H II regions <sup>[62]</sup> is therefore a natural prediction of the TEP equilibrium model, not an independent verification of a single primordial event.

**Metallicity-dependent VMO transition.** As a single-phase global equilibrium, the model silently fails: at $f_{\rm VMO} = 0.994$, $E_Z \approx 0$ gives $Z_{\rm eq} = p_Z(1 - f_{\rm VMO})/(1 - R) \approx 1.4 \times 10^{-4}$ — a factor $\sim 100$ below observed metallicities at low redshift. The resolution is a *local* metallicity-dependent transition $f_{\rm VMO}(Z)$, not a globally coordinated chronological epoch. Pop III/VMO formation naturally shuts off locally once a galactic patch exceeds a critical metallicity $Z_{\rm crit} \sim 10^{-4}$ (cooling transition from atomic to metal-line cooling). In low-metallicity patches ($Z \ll Z_{\rm crit}$), VMO-dominated nucleosynthesis with temporal-horizon sequestration sets the $Z \to 0$ intercept: $Y(Z = 0) = Y_{\rm eq} = 0.247$. In high-metallicity patches ($Z \gg Z_{\rm crit}$), standard-star yields $p_{Y,\rm std}$ set the slope:

\begin{equation} \frac{\Delta Y}{\Delta Z}\bigg|_{Z > Z_{\rm crit}} = \frac{p_{Y,\rm std}}{(1 - R)\,p_Z} = \begin{cases} 2.4 & p_Z = 0.014 \\ 1.7 & p_Z = 0.02 \end{cases} \qquad \text{vs. observed } \Delta Y/\Delta Z \simeq 1.4\text{--}3, \end{equation}

and the solar-point check gives $Y(Z = 0.014) = 0.247 + (1.7\text{--}2.4) \times 0.014 = 0.270\text{--}0.280$, versus the observed solar $Y \simeq 0.270$–$0.274$. The metallicity-dependent transition model lands in the observed range with yield parameters already constrained by H II region calibrations. The single-phase $Z_{\rm eq}$ failure is stated honestly: the VMO-dominated equilibrium suppresses metals too aggressively for the present-day metallicity to arise from the equilibrium alone. The transition structure — VMO-dominated low-$Z$ patches set the intercept, standard-star high-$Z$ patches set the slope — is the physically correct reading, and the arithmetic confirms it quantitatively. The metallicity-dependent VMO-to-ordinary-star transition introduces a function $f_{\rm VMO}(Z)$ with a critical metallicity $Z_{\rm crit}$ and a transition width; while $Z_{\rm crit}$ is independently motivated by VMO formation physics, the transition functional form and width are constrained by VMO formation physics and stellar population evolution modelling. The transition is physically motivated by the metal-line cooling threshold at $Z_{\rm crit} \sim 10^{-4}$ and works quantitatively with yield parameters already constrained by H II region calibrations. Crucially, this is a *local* transition occurring asynchronously across galactic patches as each reaches $Z_{\rm crit}$, preserving the global eternal continuum — there are no globally coordinated "epochs." The exponent $q = 0.8$ (giving $p + q = 1.3$) is anchored to the same worldline/astration statistics that govern the Compton-exposure convergence condition ($a + p > 1$) and the $\tau(z)$ three-point requirement, so the exponent family $(p, q, a)$ is constrained by data in one place.

**Sensitivity of $Y_{\rm eq}$ to yield parameters.** The equilibrium helium mass fraction is set by the adopted yield parameters through the baryonic-cycling fixed-point equation. Setting $dY/dt = 0$ in the GCE ODE yields:

\begin{equation} Y_{\rm eq} = \frac{p_{Y,\rm eff}}{1 - R}, \qquad p_{Y,\rm eff} = f_{\rm VMO}\,p_{Y,\rm VMO} + (1 - f_{\rm VMO})\,p_{Y,\rm std}, \end{equation}

where $p_{Y,\rm VMO}$ is the helium yield per VMO stellar generation, $p_{Y,\rm std}$ is the standard-star helium yield, $R$ is the return fraction (fraction of stellar mass returned to the ISM, determined by IMF integration over measured stellar lifetimes and remnant masses), and $f_{\rm VMO}$ is the VMO fraction. The metal escape fraction $E_Z$ affects the metal equilibrium $Z_{\rm eq}$, not $Y_{\rm eq}$ directly; $E_Z \approx 0$ means metals do not escape the temporal horizon (VMO-core sequestration), keeping $Z_{\rm eq}$ low without altering the helium fixed point. The baseline parameter values and sensitivities are:

| Parameter | Symbol | Baseline | Source | $\partial Y_{\rm eq}/\partial(\cdot)$ |
| --- | --- | --- | --- | --- |
| VMO helium yield | $p_{Y,\rm VMO}$ | 0.149 | VMO wind models (Carr, Bond & Arnett 1984) | - |
| Standard-star He yield | $p_{Y,\rm std}$ | 0.02 | H II region / population synthesis | - |
| Effective He yield | $p_{Y,\rm eff}$ | 0.1482 | $f_{\rm VMO}\,p_{Y,\rm VMO} + (1-f_{\rm VMO})\,p_{Y,\rm std}$ | $1/(1-R) \approx 1.67$ |
| Return fraction | $R$ | 0.40 | IMF integration (Salpeter / Kroupa) | $p_{Y,\rm eff}/(1-R)^2 \approx 0.41$ |
| VMO fraction | $f_{\rm VMO}$ | 0.994 | Required low-metallicity VMO-dominated branch; population closure open | $(p_{Y,\rm VMO} - p_{Y,\rm std})/(1-R) \approx 0.22$ |
| Metal escape fraction | $E_Z$ | $\approx 0$ | Temporal-horizon sequestration | 0 (affects $Z_{\rm eq}$ only) |

The derivative $\partial Y_{\rm eq}/\partial R = p_{Y,\rm eff}/(1-R)^2 > 0$ is positive: increasing the return fraction increases $Y_{\rm eq}$ because more mass is recycled into new stars, amplifying the helium yield. The dominant sensitivity is to $R$ ($\pm 0.005$ in $R$ produces $\pm 0.002$ in $Y_{\rm eq}$); the VMO fraction is less sensitive ($\pm 0.01$ in $f_{\rm VMO}$ produces $\pm 0.002$ in $Y_{\rm eq}$). The observed $Y_p \approx 0.245 \pm 0.003$ is reproduced for $R \in [0.395, 0.405]$ and $f_{\rm VMO} \in [0.975, 0.995]$, consistent with a high VMO fraction in low-metallicity stellar populations bounded by the observed $[\alpha/\mathrm{Fe}]$ ratio in old stellar populations. A dedicated $f_{\rm VMO}$ sensitivity scan (step\_06, $f_{\rm VMO} \in [0.90, 1.00]$ at $\Delta f = 0.005$ resolution, results/gate6\_helium\_results.json) confirms that the compatible range spans $\Delta f_{\rm VMO} \approx 0.02$, not a single fine-tuned point: $Y_{\rm eq}$ varies from $0.227$ ($f_{\rm VMO} = 0.90$) to $0.248$ ($f_{\rm VMO} = 1.00$), with the observed $Y_p$ sitting in the upper portion of this range. The model therefore requires $f_{\rm VMO} \gtrsim 0.97$: the primordial helium abundance is reproduced only when the low-metallicity stellar population is VMO-dominated, with standard stars contributing at most a few per cent by fraction. This is an aggressive but not fine-tuned requirement: the compatible range spans $0.02$ in $f_{\rm VMO}$, and the physical motivation (metal-line cooling shuts off below $Z_{\rm crit} \sim 10^{-4}$, channeling star formation into VMOs at low metallicity) naturally produces $f_{\rm VMO} \to 1$ as $Z \to 0$. The convergence condition $p + q = 1.3 > 1$ (Section 4.1) guarantees that the integrated astration exposure is finite for any individual worldline. The numerical reaction-flow calculation demonstrates convergence to the fixed point for the adopted stellar histories. To verify that $Y_{\rm eq} = 0.247$ is a true attractor rather than a point dependent on the chosen history, a dedicated contraction analysis was performed over a grid of initial conditions spanning $Y_0 = 0$ to $Y_0 = 0.8$ (step\_08, results/gate8\_light\_elements.json). All four tested initial conditions converge to $Y_{\rm eq} = 0.247$ within $\Delta Y < 4 \times 10^{-6}$: $Y_0 = 0.00 \to Y_{\rm final} = 0.24704$, $Y_0 = 0.25 \to Y_{\rm final} = 0.24704$, $Y_0 = 0.50 \to Y_{\rm final} = 0.24704$, $Y_0 = 0.80 \to Y_{\rm final} = 0.24705$. The fixed point is therefore an attractor: the equilibrium helium-4 mass fraction is independent of the tested initial compositions under the adopted reaction-flow model, confirming that $Y_{\rm eq} = 0.247$ is a robust prediction of the temporal-horizon reaction-flow framework rather than an artifact of a particular initial condition.

**CMB Baryon Density Concordance (Gate 9).** The most powerful argument for standard BBN is that the deuterium abundance predicts a baryon density $\Omega_b h^2 \approx 0.022$ <sup>[65]</sup> that matches the independent value derived from Planck CMB acoustic peak ratios <sup>[64]</sup>. Under TEP, the observed D/H ratio is a localized kinematic signature rather than a primordial abundance, so the D/H $\to$ $\Omega_b$ mapping is not the source of the baryon density constraint. However, the CMB *independently* anchors $\Omega_b h^2$ via acoustic physics that TEP strictly preserves: TEP-HC (Paper 18, <sup>[3]</sup>) fits $\Omega_b h^2 = 0.02144 \pm 0.00257$ directly from Planck acoustic peaks via joint MCMC, with sound-horizon ratio $r_s^{\rm TEP}/r_s^{\rm \Lambda CDM} = 0.999994$ ($<6\text{ ppm}$ deviation). The acoustic peaks rigidly demand this specific baryon density to balance the compression and rarefaction peaks of the photon-baryon fluid, regardless of the D/H ratio. Gate 9 is therefore stated as: *given the rigidly CMB-anchored baryon density $\Omega_b h^2 \approx 0.022$, verify that the SQUAD/LLS neutral-hydrogen column-density distribution folded through the TEP edge-gas shear model produces a D/H histogram consistent with observed quasar sightline statistics without free density tuning.* This computation is tractable on existing LLS catalogs but is not performed in this paper. The corpus-level cross-reference is to TEP-HC (Paper 18, <sup>[3]</sup>) and TEP-C0 (Paper 26, <sup>[2]</sup>), where the acoustic peak ratios are addressed independently of the D/H–$\Omega_b$ mapping.

## 5. Discussion and Falsifiable Predictions

The standard interpretation of cosmological redshift as geometric expansion has led to over a century of physical inference that culminates in the mathematical breakdown of General Relativity at the Big Bang singularity. Furthermore, the requirement of a ubiquitous hot, dense early universe heavily relies on the unique primordial identification of light elements such as deuterium in high-redshift absorption systems. Both links are tested directly, and neither can be assumed once dynamical proper time is admitted.

### 5.1 Distance Duality and Cosmological Tests

#### Distance Duality and Supernova Standardization

Critically, $T_{\rm obs}(z) \neq T_{\rm loc}(\tau)$ in general. The temperature of the background radiation bath as measured by an observer is distinct from the actual local matter/radiation state $T_{\rm loc}(\tau)$ at emission. Furthermore, because physical space is static, the standard geometric distances must be carefully defined. Etherington's reciprocity theorem is a general result of metric photon propagation, not specific to expanding FLRW; it dictates the distance-duality relation $d_L = d_A (1+z)^2$ for any metric theory where photon geodesics are well-defined and photon number is conserved. In the TEP framework, the physical matter space is static ($a_{\rm m} = 1$), but the conformal coupling $A(\phi)$ acts identically to the FLRW scale factor for photon transport. Because temporal transport reduces both photon energy and arrival rates by a factor of $(1+z)$, and the conformal geometry scales the apparent angular size, the luminosity distance becomes $d_L = d_A (1+z)^2$. The TEP framework therefore preserves the Etherington relation by construction, not because it replicates FLRW expansion, but because the conformal transport law satisfies the same general conditions.

While the baseline distance-duality relation is preserved, it is important to recognize that SNIa magnitudes are not raw observables. They are derived via light-curve standardization fitters (like SALT2/SALT3) which assume an expanding FLRW background to correct for time dilation (stretch factors) and color. A preliminary evaluation has already been completed in TEP-C0 (Paper 26): the SALT2 light-curve stretch parameters ($x_1$) from the 1,701 supernovae in the Pantheon+ dataset were tested against the exact covariant TEP conformal factor. Under standard $\Lambda$CDM time dilation $(1+z)$, the fit to observed stretch parameters yields a reduced $\chi^2$ of 102.6; under the TEP conformal factor, the reduced $\chi^2$ improves to 88.9. This is a diagnostic consistency check showing consistency with temporal-field stretching of supernova light curves as predicted by TEP, though the result remains contingent on SALT2 standardization assumptions. The remaining observational task is the full re-calibration of the light-curve fitters within the TEP geometry rather than relying on FLRW-calibrated nuisance parameters — a concrete, falsifiable roadmap with the stretch-factor directionality already verified.

### 5.2 Line-of-Sight Transport and Optical Time-Transfer

TEP elevates the speed of light from a global geometric truth to a local theorem. This provides falsifiable physical predictions. Because proper time is a dynamical field $A(\phi)$, the framework decomposes temporal transport into a homogeneous exact-conformal limit and a non-integrable path-dependent sector.

As detailed in Section 4, the conformal piece ($\Sigma_\parallel$) is endpoint-dependent and vanishes on closed loops, whereas the disformal transport ($\mathcal{C}_T$) supplies genuine non-integrability. Multi-leg optical time-transfer experiments—currently within reach of next-generation atomic clock networks—can directly test for this line-of-sight transport integral ($\oint \mathcal{C}_{T,\parallel} d\ell \neq 0$).

By separating the kinematics of space from the dynamics of time, TEP preserves the empirically established pillars of local relativity while providing a regular, singularity-free geometric framework. This motivates a shift from accommodating geometric singularities to evaluating directly testable, dynamical-time physics.

### 5.3 What Would Falsify TEP

The framework makes several concrete falsifiable predictions and discriminating tests. Failure has the consequence stated for each test below.

- **Disformal clock three-sightline test:** TEP predicts a geometry-dependent $\Delta v_T$ via the temporal-disformal channel, with the fitted free-H displacements ($-78.9$, $-76.0$, $-118.0$\,km/s) as the maximal amplitude targets under a pure-TEP attribution. The $-81.6$\,km/s clustering is explained by the velocity-selection theorem (Gate 6-I) as a selection effect. Diagnostic mode establishes algebraic feasibility; transfer mode shows the simple power-law $B(\phi) \propto \phi^5$ does not transfer across redshifts. Predictive closure — a single frozen microscopic $B(\phi)$ with independently specified absorber environments — remains the decisive test. If no physically motivated $B(\phi)$ can produce an independently predicted temporal contribution compatible with the observed displaced-H phenomenology while satisfying Cassini, GW170817 and matter-metric consistency constraints, the temporal-disformal interpretation would be falsified.

- **Orphan population (decisive empirical test):** The velocity-selection theorem (Gate 6) predicts an excess of narrow H I components at non-isotope offsets beyond the conventional background. The illustrative forecast (Gate 6-II) gives $\sim 19$ orphan features per $\sim 80$ parent sightlines before observability cuts; the archival feasibility analysis reduces this to approximately two detectable excess candidates per 80 parent sightlines, corresponding to roughly ten usable systems. If a re-analysis of existing archival spectra shows no excess of narrow ($b < 10$\,km/s), low-column ($\log N \sim 12$--$14$) components at non-isotope offsets beyond the normal H I population, the TEP interpretation is substantially weakened.

- **Spectroscopic robustness:** Scaffold freedom with five freed components *strengthens* the calibrated significance of the Q1009 free-H preference ($p < 0.005$ when five surrounding components are freed, Section 5.5). The Q1009 evidence is therefore robust to the externally fixed published component architecture: the discrimination survives when the absorber model is allowed to re-optimise. Equivalent scaffold-freedom calibrations have not yet been completed for PKS\,1937$-$101 (184 H I components) and J1332$+$0052; their quoted significance ($p_{\rm parent} = 0.001$ for both) therefore remains conditional on the adopted published component architectures.

- **Helium equilibrium:** If $Y_{\rm eq}$ moves outside the observed range $0.245 \pm 0.003$ under physically motivated variations in ($p_Y$, $R$, $f_{\rm VMO}$) within their observationally constrained ranges, the baryonic-cycling explanation for the helium-4 mass fraction would be falsified.

- **CMB acoustic structure:** If the TEP perturbation theory fails to reproduce the Planck acoustic peak ratios and damping tail within observational uncertainties (deferred to TEP-HC), the cosmological framework is ruled out.

- **Growth of structure:** If the static-spatial TEP geometry cannot reproduce the observed $S_8$ growth parameter or the BAO scale, the framework fails as a cosmological alternative.

### 5.4 Outstanding Observational Tests

The following observables must eventually be confronted by the TEP framework. The current status of each is stated honestly:

| Observable | Status | Reference |
| --- | --- | --- |
| CMB acoustic peaks and damping tail | Deferred to perturbation theory (TEP-HC, Paper 18); pre-recombination sound horizon preserved at 6 ppm | <sup>[16]</sup> |
| CMB temperature–redshift relation | Preserved by conformal transport: $T_{\rm obs}(z) = T_{\rm em}/(1+z)$ | Section 4.1 (TEP-TH) |
| BAO and distance-ladder consistency | Distance duality preserved; SALT2 stretch-factor directionality verified in TEP-C0 ($\chi^2$ 102.6→88.9); full re-calibration within TEP geometry is open | Section 5.1 |
| Growth of structure / $S_8$ | Linear pure-conformal growth evaluated in TEP-HC; full nonlinear/matter-only structure formation remains open | — |
| D/H in non-benchmark sightlines | Framework predicts localized shear amplitude varies with core-edge geometry; population study is open | — |
| $\Delta Y / \Delta Z$ slope in H II regions | Qualitative prediction derived; quantitative comparison deferred | Section 4.4 |
| Lyman-limit / Gunn–Peterson trough redshift | Optical-depth divergence predicted; quantitative $\tau_e \sim 1$ redshift not yet computed | Section 4.2 |

### 5.5 Spectroscopic Robustness Checks

The Q1009+2956 discriminating power was tested against several alternative formulations of the model comparison. Four robustness checks are reported here.

#### Limited Scaffold Freedom (C2)

The 43 H I components are held at the published literature architecture in the standard analysis. Allowing the five strongest non-parent H I components *within the absorber system* ($|v| \le 1000$ km/s, excluding the D parent components) to re-optimise under both the D and H hypotheses changes the likelihood gain from $T = 161.03$ (fixed scaffold) to $T = 385.35$ (five freed components, $\Delta T = +224$). Both models benefit from the additional freedom ($\Delta\ln L_D = +49.5$, $\Delta\ln L_H = +161.6$), but H benefits substantially more, so the fixed-scaffold comparison is conservative. The D parent components are excluded from the freed set because the D model inherits the parent's Doppler parameter with mass scaling; freeing the parent's $b$ creates a conflicting optimization where D's $b$ is doubly controlled. A calibrated Monte Carlo with the same freed-scaffold optimization inside the simulation loop gives $p < 0.005$ (0/200 exceedances) — highly significant. The freed-scaffold result confirms that the free-H preference survives even when the absorber model is allowed to re-optimise: the discrimination is not an artifact of the fixed published architecture but reflects a genuine structural difference between the D and H models.

#### Parent-Width-Constrained H Control (C4)

To test whether the candidate feature is merely an ordinary H I component shifted by a free velocity, the data were also fitted with a two-parameter *kinematic* model: free $v_H$ and $\log N_H$, but $b$ fixed to the parent H I value (no isotope mass scaling and no free $b$). This restricted control is not the general ordinary-H alternative, which is represented by $M_{H,\rm free}$. This model is strongly rejected: $T(M_H vs M_D) = 161.03$, $T(M_H vs M_{\rm kin}) = 208.98$, $T(M_{\rm kin} vs M_D) = -47.95$. $\Delta\mathrm{AIC}(M_{\rm kin} - M_D) = +45.95$ and $\Delta\mathrm{AIC}(M_H - M_{\rm kin}) = -204.98$. The best-fit kinematic velocity is $v_H = -130.52$ km/s, but the parent-like $b$ value cannot reproduce the narrow isotopic core. A pure velocity shift without deuterium's mass-scaled Doppler parameter does not explain the feature.

#### Noisy/Offset True-D Monte Carlo (C3)

The standard calibration generates exact true-D flux from the maximum-likelihood D parameters. A more realistic test perturbs the generating true-D nuisance parameters before drawing each realisation: $\log N_D$ by $\pm 0.1$ dex, $T_K$ by $\pm 1000$ K (clamped to $> 100$ K), and $b_{\rm turb}$ by $\pm 1$ km s$^{-1}$. The D/H velocity offset ($-81.6$ km/s) is a fixed physical constant (exact reduced-mass isotope shift) and is not perturbed. For Q1009+2956 the result confirms the main analysis: 0/1000 standard realisations exceed $T_{\rm obs}$ ($p_{\rm std} = 0.001$), and 0/1000 parent-reassignment realisations exceed $T_{\rm parent}$ ($p_{\rm parent} = 0.001$). Both the standard-statistic and parent-reassignment rejections are robust to realistic uncertainty in the true-D model parameters. An earlier version of this check perturbed the velocity offset, creating a mismatch between the generating and fitting models that artificially inflated $T_{\rm sim}$; the corrected implementation confirms the original significance.

#### Physical Parent Window (C1) — Additional Robustness Test

The conservative $\pm 1000$\,km/s parent window is the cross-sightline headline statistic; the $\pm 3b_{\rm max}$ physical window has also been calibrated for all three sightlines ($N=1000$ each). For Q1009+2956 the largest $b$-value of the main complex is 56.7 km s$^{-1}$, so the physical window $\pm 3b$ is $\pm 170$ km s$^{-1}$, compared with the conservative $\pm 1000$ km s$^{-1}$. This reduces the eligible-parent set from 14 in the conservative $\pm 1000\,{\rm km\,s^{-1}}$ window to 4 in the physical window. With $N=1000$ true-D Monte Carlo realisations the fair standard statistic gives 0/1000 exceedances ($p_{\rm std} = 0.001$), and the parent-reassignment statistic also gives 0/1000 exceedances ($p_{\rm parent} = 0.001$). For PKS\,1937$-$101 the physical window is $\pm 173$\,km/s ($b_{\rm max} = 57.7$\,km/s), giving 0/1000 exceedances under both statistics ($p_{\rm std} = p_{\rm parent} = 0.001$). For J1332$+$0052 the physical window is $\pm 59$\,km/s ($b_{\rm max} = 19.5$\,km/s), giving 0/1000 exceedances under both statistics ($p_{\rm std} = p_{\rm parent} = 0.001$). The results are consistent with the fixed window across all three sightlines: the H alternative is significantly preferred under both the canonical-parent and adversarial-parent tests. The physical window is motivated by the absorber's own velocity structure rather than an arbitrary fixed range.

### 5.6 Multi-Pronged Evidence Analysis (Gate 8)

Three discriminators between the isotope-D and TEP edge-gas interpretations have been quantitatively evaluated using the fitted free-H parameters from all three benchmark sightlines: the Doppler $b$-value ratio, the velocity offset deviation, and the column density difference. These quantities are all derived from the same free-H fit and are therefore not statistically independent; the joint multivariate statistic is the appropriate calibrated measure. A true-D injection Monte Carlo (step\_08b, $N = 1000$ realisations per sightline) calibrates each statistic against the null distribution obtained by fitting $M_{H,\rm free}$ to simulated true-D spectra. The $b$-value ratio uses the mixed thermal+turbulent prediction $b_D = \sqrt{b_{\rm turb}^2 + 2kT/m_D}$, not the purely thermal $b_D = b_{\rm parent}/\sqrt{2}$, since the turbulent contribution does not scale with mass. Gate 8 uses the same spectra and same free-H fits as Gates 2/3; it is therefore an independent diagnostic statistic derived from the same observational fit, not an independent dataset or evidence channel. Its value lies in providing a different projection of the same data — one that tests whether the fitted free-H parameters are jointly anomalous relative to what true-D simulations produce, rather than testing the likelihood ratio directly.

**b-value ratio.** Under isotope-D, the fitted free-H Doppler parameter should equal the mass-scaled D prediction $b_D = \sqrt{b_{\rm turb}^2 + 2kT/m_D}$, where the turbulent contribution does not scale with mass. Under TEP, $b$ is set by edge-gas temperature and is unconstrained. The observed ratios are $0.99$ (Q1009), $1.31$ (PKS\,1937), and $5.31$ (J1332). The J1332 ratio indicates a turbulent, broad component ($b_{H,\rm free} \approx 51$\,km/s) inconsistent with the mass-scaled D prediction ($b_D \approx 9.6$\,km/s). After calibration against the true-D null ($N = 1000$), the J1332 $b$-value ratio is marginal ($p = 0.059$): true-D simulations produce $b$-ratios clustered around $1.14 \pm 1.17$, whereas the observed $5.31$ is far outside this distribution. The Q1009 $b$-ratio is not significant ($p = 0.998$) — the observed ratio is closer to the isotope-D prediction than the simulations. The PKS\,1937 $b$-ratio is marginal ($p = 0.05$). A caveat applies to the J1332 result: the TEP orphan prediction (Gate 6-II) anticipates narrow, cool, thermally-dominated edge components ($b < 10$\,km/s), whereas the J1332 free-H fit yields a broad, turbulence-dominated component ($b \approx 51$\,km/s, $b_{\rm turb} = 50$\,km/s at the upper bound, $T_K \approx 5000$\,K). A boundary check with $b_{\rm turb,max}=100$ and $150\,{\rm km\,s^{-1}}$ shows that the fitted turbulent width does not stabilise, rising to $\sim 112\,{\rm km\,s^{-1}}$, while $v_H$ shifts from $-118.0$ to $-115.3\,{\rm km\,s^{-1}}$ and $T_{\rm obs}$ increases from $137.0$ to $140.6$. The likelihood preference therefore does not weaken, but no expanded-bound Monte-Carlo significance is assigned here. J1332-specific fitted width and velocity diagnostics are consequently treated as bound-sensitive. The $b$-value ratio is marginally inconsistent with isotope-D but does not simultaneously confirm the TEP orphan phenotype; the J1332 feature may be a turbulent H I interloper unrelated to the TEP edge-gas mechanism, or the orphan prediction may require revision to accommodate turbulence-dominated edge gas. Resolving this requires either a physical model for turbulent edge-gas $b$-values or a larger sample spanning both thermal and turbulent regimes.

**Offset-deviation correlation.** Under isotope-D, all fitted free-H velocities should sit at the exact isotope shift within spectral resolution. Under TEP, the offset depends on the local shear amplitude, which scales with the absorber's gravitational potential. The observed deviations are $+2.7$\,km/s (Q1009), $+5.7$\,km/s (PKS\,1937), and $-36.6$\,km/s (J1332). Using the primary bounded fits, the three sightlines show a monotonic ordering with $\log N_{\rm HI}$; however, the J1332 velocity is sensitive to the turbulent-width prior, so this $N=3$ ordering is descriptive rather than a robust correlation test ($P(\rho = 1 \mid N = 3) = 0.17$ for a prespecified directional trend). After calibration ($N = 1000$), the Q1009 deviation is highly significant individually ($p ≤ 0.001$, 0/1000 exceedances): true-D simulations produce free-H fits that sit within $\pm 0.2$\,km/s of the isotope shift, whereas the observed $+2.7$\,km/s deviation is far outside this distribution. The PKS\,1937 deviation is also highly significant ($p ≤ 0.001$, 0/1000 exceedances): the simulation spread is $\pm 0.5$\,km/s, and the observed $+5.7$\,km/s is far outside. The J1332 deviation is not individually significant ($p = 0.094$): the broad, saturated feature yields a simulation spread of $\pm 17.5$\,km/s, within which the observed $-36.6$\,km/s falls. The Q1009 result is the most direct individual test: under isotope-D, the feature is at the isotope shift and the free-H fit must find it there; under TEP, the feature is edge-gas at a slightly different velocity. The $p ≤ 0.001$ rejection of the isotope-D velocity prediction for Q1009 is the strongest individual discriminator in the analysis. For scale: among the six H I components of Q1009 within the $\pm 3b_{\rm max} = \pm 170$\,km/s physical window, the mean nearest-neighbour velocity spacing is $56$\,km/s (median $45$\,km/s); the fitted free-H displacement of $-78.9$\,km/s is therefore $\sim 1.4$ times the mean spacing, comparable to — but somewhat larger than — ordinary H I component structure. The displacement is not anomalously large relative to the absorber's own kinematic texture. A caveat applies: the calibration assumes the only source of velocity scatter is the fitting process, whereas residual wavelength-calibration systematics (e.g., intra-order distortion, ThAr line-list uncertainties) can introduce $\sim 0.5$--$1$\,km/s offsets not captured by the simulation. Folding a Gaussian systematic with $\sigma_{\rm sys} = 1$\,km/s into the simulation spread (step\_08c, results/gate8\_wavelength\_systematics.json) reduces the Q1009 deviation from $16.9\sigma$ ($p ≤ 0.001$) to $2.7\sigma$ ($p \approx 0.008$), while PKS\,1937 remains at $5.0\sigma$ ($p \approx 4.7 \times 10^{-7}$), robustly significant. At $\sigma_{\rm sys} = 0.5$\,km/s both sightlines remain highly significant ($5.2\sigma$ and $7.9\sigma$ respectively). The Q1009 result should therefore be interpreted as significant *conditional on wavelength-calibration systematics remaining below $\sim 1$\,km/s*, and a full end-to-end error budget incorporating wavelength-calibration uncertainties is required before the velocity deviation can be considered robust evidence against isotope-D.

**Sign test.** The conformal sign theorem predicts all edge-shear features should be blueward of the parent. All three are: $-131.3 < -52.4$, $-67.3 < +8.7$, $-118.2 < 0.0$\,km/s. However, the D-selected benchmark sample does not constitute an independent sign test, because its selection protocol already targets blueward isotope-shifted absorption. The sign becomes genuinely predictive in an independently selected population of non-isotope displaced components (Gate 6-III).

**Column density difference.** Under isotope-D, $N_{H,\rm free}$ should match $N_{\rm HI} \times ({\rm D/H})_{\rm BBN}$. The observed differences are $+0.03$\,dex (Q1009), $-0.09$\,dex (PKS\,1937), and $+0.70$\,dex (J1332). After calibration ($N = 1000$), the Q1009 column density difference is significant ($p = 0.017$): true-D simulations produce H fits with $\log N$ differences tightly clustered around $-0.01 \pm 0.02$\,dex, whereas the observed $+0.03$\,dex is at the edge of this distribution. The PKS\,1937 ($p = 1.0$) and J1332 ($p = 0.688$) column density differences are not significant.

**Calibrated joint assessment.** The three statistics are correlated because they derive from the same free-H fit. A joint Mahalanobis distance against the true-D covariance matrix provides the calibrated multivariate test. With $N = 1000$ true-D injections per sightline, Q1009$+$2956 is highly significant in the joint statistic ($p ≤ 0.001$, 0/1000 exceedances, Mahalanobis distance $= 288$), driven primarily by the velocity deviation ($p ≤ 0.001$). PKS\,1937$-$101 is also highly significant ($p ≤ 0.001$, 0/1000 exceedances, Mahalanobis distance $= 130$), driven primarily by the velocity deviation ($p ≤ 0.001$). J1332$+$0052 is significant ($p = 0.023$, 23/1000 exceedances, Mahalanobis distance $= 14.7$), driven by the joint combination of the $b$-value ratio ($p = 0.059$) and velocity deviation ($p = 0.094$), though the broad $b$-value is inconsistent with the narrow-edge TEP orphan prediction (see above). The pattern is physically sensible: Q1009 (high S/N, high resolution, moderate D column) provides the tightest velocity constraint; PKS\,1937 (high resolution, moderate D column) also provides a tight velocity constraint; J1332 (saturated D, broad feature) provides the tightest $b$-value constraint but the velocity deviation is not individually significant. Q1009$+$2956 and PKS\,1937$-$101 show highly significant calibrated Gate 8 evidence ($p ≤ 0.001$); J1332$+$0052 is significant at the uncorrected level ($p = 0.023$) but does not survive the $\alpha/3 = 0.0167$ correction among the three Gate-8 statistics. All three show significant Gate 2/3 evidence ($p_{\rm parent} = 0.001$). The cross-sightline pattern — deviations scaling with $N_{\rm HI}$, all features blueward — is consistent with the TEP prediction. The parent-identity diagnostic (Gate 7) is descriptive only, and the amplitude gap (Gate 4B) is the principal remaining calculation. The cumulative case is strengthened by the Q1009 and PKS\,1937 velocity deviation results; the population forecast (Gate 6-II) and orphan search protocol (Gate 6-III) provide the next testable predictions.

**Wavelength-calibration systematics.** The velocity-deviation statistic measures a relative offset between the fitted free-H component and the isotope-shifted position within the same spectrum. The relevant wavelength systematic is therefore the intra-spectrum relative velocity distortion (intra-order or long-range), not the absolute wavelength offset or inter-night drift, which cancel in the relative measurement. Instrument-specific residual distortion amplitudes are taken from supercalibration studies: $\sigma_{\rm sys} = 0.25$\,km/s for Keck/HIRES with ThAr calibration, based on iodine-cell measurements of intra-order distortions $\sim 250$\,m/s <sup>[71]</sup>; $\sigma_{\rm sys} = 0.05$\,km/s for VLT/ESPRESSO with ThAr+Fabry-Perot calibration, based on laser-frequency-comb discrepancies $\lesssim 24$\,m/s <sup>[73]</sup>; and $\sigma_{\rm sys} = 0.20$\,km/s for VLT/UVES+Keck/HIRES, based on solar-twin supercalibration long-range distortions $\sim 200$\,m/s per $1000$\,\AA <sup>[72]</sup>. Folding these into the calibrated spread via $\sigma_{\rm total} = \sqrt{\sigma_{\rm fit}^2 + \sigma_{\rm sys}^2}$ (step\_08c, $N = 100\,000$ Monte Carlo draws per case) gives Gaussian-equivalent significances of $9.1\sigma$ (Q1009$+$2956), $11.0\sigma$ (PKS\,1937$-$101), and $2.1\sigma$ (J1332$+$0052), corresponding under a normal-tail approximation to $p\sim10^{-19}$, $10^{-27}$, and $0.032$, respectively. The Monte-Carlo sampling itself does not directly resolve tail probabilities below its finite simulation floor. The Q1009 and PKS\,1937 velocity-deviation rejections of isotope-D therefore survive at high significance even under the literature-calibrated systematic floor; the J1332 result remains not individually significant after the $\alpha/3$ correction, consistent with the unsystematic calibration. A sensitivity scan over $\sigma_{\rm sys} \in [0, 1]$\,km/s is reported in the supplementary results (results/gate8\_wavelength\_systematics.json); the $9.1\sigma$ Q1009 result degrades to $2.7\sigma$ only at $\sigma_{\rm sys} = 1.0$\,km/s, a value exceeding all measured intra-spectrum distortions for the relevant instruments.

### 5.7 Orphan Search: Protocol and Pilot Results (Gate 6-III)

The population forecast (Gate 6-II) predicts $\sim 19$ orphan narrow components at non-isotope offsets across $\sim 80$ high-S/N LLS sightlines. A pilot search on the three benchmark sightlines has been carried out using both the published VPFIT component decompositions and direct spectral inspection of the Ly$\alpha$ region (step\_06\_orphan\_search, results/gate6\_orphan\_search.json).

**Pilot search results.** The VPFIT models and HIRES/ESPRESSO spectra were searched for narrow ($b < 15$\,km/s), low-column ($\log N < 15$) H I components at non-isotope offsets ($|\Delta v - v_{\rm iso}| > 10$\,km/s) within $\pm 300$\,km/s of the parent. One orphan candidate is identified: a narrow H I component in Q1009$+$2956 at $\Delta v = -155.5$\,km/s from the parent ($|\Delta v - v_{\rm iso}| = 73.9$\,km/s), with $b = 10.3$\,km/s and $\log N = 11.5$, detected at $5\sigma$ on a single coadd in the HIRES spectrum. No global significance is assigned because the search over velocity, width and column density has not been Monte-Carlo calibrated. A second absorption feature at $\Delta v = -170$\,km/s in PKS\,1937$-$101 is detected at $5\sigma$ on a single coadd in the ESPRESSO spectrum, but the VPFIT decomposition fits it as a broad component ($b = 31.5$\,km/s); a narrow orphan may be hidden within the broad fit. J1332$+$0052 is not searchable: the Ly$\alpha$ is completely saturated ($\log N_{\rm HI} = 19.25$) and Ly$\beta$ falls outside the UVES wavelength coverage.

The Q1009 orphan candidate is already present in the published VPFIT decomposition (one of the 43 H I components in the Zavarygin et al. 2018 model). The pilot count is not an independent test of the revised forecast, because the usable-fraction correction is estimated from this same archival exercise. It is therefore reported as a feasibility result rather than confirmatory evidence. Three factors suppress the yield: (i) the parent H I is saturated from $\Delta v \approx -50$ to $+100$\,km/s at all three sightlines, hiding any orphans in that window; (ii) the VPFIT models only contain components above the statistical significance threshold, so sub-threshold orphans are invisible; (iii) $\sigma_{\rm shear}$ is estimated from only 3 data points (the D-identified features) and is biased small, understating the predicted velocity spread. The full population test requires the $\sim 80$-sightline archival search described below.

**Archival search.** An archival search has been carried out using publicly available data from two surveys (step\_06\_orphan\_search, results/gate6\_archival\_search.json):

- *SQUAD DR1* (UVES Spectral Quasar Absorption Database, Murphy et al. 2018 <sup>[43]</sup>): 467 UVES quasar spectra at $R \sim 40\,000$--$50\,000$, accessed via the ESO Phase 3 archive. Three benchmark sightline spectra were downloaded and inspected: Q1009$+$2956 (UVES, 3\,000\,s), Q0913$+$072 (UVES, 77\,525\,s), and J212912$-$153841 (UVES, 101\,016\,s). The SQUAD UVES spectrum of Q1009$+$2956 shows a feature at $\Delta v \approx -155$\,km/s consistent with the HIRES orphan candidate, though at lower S/N ($\sim 33$ vs $\sim 87$ for HIRES); this is a consistency check on the same sightline, not an independent detection. Q0913$+$072 is a DLA ($\log N_{\rm HI} = 20.15$) with all Lyman series lines through Ly$\varepsilon$ saturated. J212912$-$153841 has an LLS at $z = 2.968$ ($\log N_{\rm HI} = 17.32$), but the Ly$\alpha$ forest at $z \sim 3$ produces near-zero flux throughout the $\pm 300$\,km/s search window.

- *KODIAQ DR2* (Keck Observatory Database of Ionized Absorption toward Quasars, O'Meara et al. 2017): 593 continuum-normalised, coadded HIRES spectra of 300 quasars, downloaded from the Keck KOA. The KODIAQ Z survey (Lehner et al. 2016) provides a catalog of 26 pLLSs/LLSs at $2.3 < z < 3.3$ with $\log N_{\rm HI} = 16.16$--$18.65$, of which 9 are LLS-class ($17.0 \leq \log N_{\rm HI} \leq 19.0$). Spectra for 7 of these 9 LLS-class sightlines were extracted and searched.

**Archival search results.** All 7 KODIAQ LLS-class sightlines have broad LLS core absorption that saturates the isotope-shift region, preventing orphan detection at the predicted velocity. The saturation arises from two compounding effects: (i) the LLS itself produces Ly$\alpha$ absorption covering $\sim 100$\,km/s, and (ii) the Ly$\alpha$ forest at $z > 2.4$ contributes additional absorption that drives the flux to near-zero at most velocities. The only sightline where the isotope-shift region is recovered is Q1009$+$2956, where the LLS has a relatively narrow core (saturating only from $\Delta v \approx -50$ to $+100$\,km/s) and the forest at $z = 2.504$ is sufficiently sparse. This identifies a critical selection criterion for the population test: only sightlines with (a) narrow LLS cores ($< 50$\,km/s saturated width), (b) S/N $> 30$ per pixel, and (c) $z < 2.6$ are suitable for orphan detection. The usable fraction of the KODIAQ Z LLS sample is $\sim 12\%$ (1 of 8 searched sightlines), substantially lower than the $\sim 30\%$ detectable-geometry fraction assumed in the Gate 6-II forecast.

**Search protocol.** For each sightline: (i) identify all narrow ($b < 10$\,km/s) H I components with $\log N \sim 12$--$14$ within $\pm 200$\,km/s of the D/H parent complex, (ii) record the velocity offset $\Delta v$ from the nearest H I parent, (iii) classify each as *isotope-consistent* ($|\Delta v - v_{\rm iso}| < 5$\,km/s) or *orphan* ($|\Delta v - v_{\rm iso}| > 5$\,km/s), (iv) record $b$, $\log N$, and S/N. An illustrative selection model calibrated to the three benchmark offsets gives an orphan fraction of $\sim 79\%$ (orphan features outnumber isotope-consistent ones by $\sim 3.8:1$); because the shear width is inferred from only three D-selected systems, this fraction is provisional. The null hypothesis is not zero orphans — ordinary H I absorbers naturally contain low-column components at many velocities — but rather the conventional H I forest background. A proper null must be constructed from velocity-shuffled windows, matched control absorbers, neighbouring $\Delta v$ intervals, or synthetic conventional H I forests. The robust TEP prediction is an *excess* of components with the joint phenotype ($b < 10$\,km/s, $\log N \sim 12$--$14$, non-isotopic offset, systematically related to absorber geometry) beyond this conventional background.

**Pilot feasibility forecast.** The archival search demonstrates that the effective survey size is reduced by the saturation selection effect. If the usable fraction is $\sim 12\%$ rather than the assumed $\sim 30\%$, the effective survey size for a 80-sightline parent sample is $\sim 10$ sightlines, predicting $\sim 2$ excess orphans under TEP. A pilot on $10$--$15$ *usable* sightlines (requiring a parent sample of $\sim 80$--$120$ LLS sightlines to account for the saturation selection) should detect $\sim 2$--$3$ orphans in excess of the conventional background. A pilot on $\geq 20$ usable sightlines would provide initial evidence; the Poisson threshold $P(0 | \lambda = 4) = 0.018$ is a planning benchmark rather than a hard theory-falsification threshold, given the exploratory nature of the $N=3$ shear calibration. The KODIAQ Z survey (26 pLLSs/LLSs) and the HD-LLS survey (Prochaska et al. 2015; 46 additional LLSs) together provide $\sim 72$ LLS sightlines, yielding $\sim 9$ usable sightlines after the saturation selection — sufficient for a pilot but not for a definitive falsification. A definitive test requires either a larger parent sample or a search strategy that recovers orphans in saturated regions via higher-order Lyman lines or metal-line proxies.

### 5.8 Corpus Cross-References: The No-Hot-Big-Bang Framework

The spectroscopic and local-shear results in this paper do not by themselves remove the need for a hot dense early phase. The broader TEP corpus addresses the complementary questions — CMB acoustic peaks, growth of structure, cosmological distances, and high-redshift galaxy assembly — and is cross-referenced here for completeness.

- **CMB acoustic peaks and sound horizon (TEP-HC, Paper 18).** The TEP conformal scalar field has been implemented natively in *hi_class* <sup>[29]</sup> and run through MCMC against Planck 2018, BAO, and Pantheon+. The acoustic sound-horizon ratio $r_s^{\rm TEP}/r_s^{\Lambda{\rm CDM}} = 0.999994$ ($< 6$\,ppm deviation), and the TT/TE/EE peak morphology is preserved without early spatial expansion. The Big Bang is reinterpreted as $A_{\rm clock} \to 0$: a temporal horizon, not a geometric singularity.

- **Temporal horizon and absence of singularity (TEP-TH, Paper 27).** The FLRW singularity is shown to be a reconstruction artifact. The temporal-horizon conformal boundary $A_{\rm clock}(\eta) = C\eta^{-p}$ with $0 < p \leq 1/2$ yields vanishing curvature invariants, divergent timelike proper time, and divergent null affine parameter — a regular, complete past boundary. The Strong Energy Condition is violated, satisfying the Hawking–Penrose prerequisite for no singularity. The tensor-to-scalar ratio is $r = 9 \times 10^{-6}$.

- **Cosmological distances without expansion (TEP-C0, Paper 26).** Pantheon+ supports the temporal-shear distance reconstruction in SN-only fits, while the joint Planck+Pantheon analysis strongly constrains the additional homogeneous shear amplitude toward zero. The conformal reconstruction remains compatible with the observed distance and acoustic background.

- **JWST high-redshift anomalies (TEP-JWST, Paper 12).** The TEP predictor carries substantial information beyond a standard mass-plus-redshift baseline and removes the finite-age assembly constraint in the static-temporal interpretation. Complete-model Bayesian comparisons are mixed, however, with flexible bursty-star-formation and AGN-feedback models remaining competitive or preferred in some joint tests. The JWST results are therefore supportive of the temporal interpretation but are not uniquely discriminating.

- **Theoretical foundation (TEP, Paper 0).** The bi-metric action $\tilde{g}_{\mu\nu} = A^2 g_{\mu\nu} + B\nabla_\mu\phi\nabla_\nu\phi$, field equations, PPN mapping, and the line-of-sight transport integral as the invariant signature of dynamical time are established in the foundational paper.

The helium-4 equilibrium is calculated within this paper. The D/H–$\Omega_b h^2$ relation is reformulated as Gate 9, while its catalogue-level population test remains to be performed; the independent CMB anchoring of $\Omega_b h^2\approx0.022$ is inherited from TEP-HC. The amplitude gap (Gate 4B) is the principal remaining calculation; the primary Gates 2/3 spectroscopic result is independent of the unresolved Gate-4B amplitude closure. Gates 4E, 7 and 8 provide secondary diagnostics, while Gate 6 defines the exploratory population test.

## 6. Conclusion

Across three benchmark D/H absorption systems, unrestricted H I is significantly preferred over isotope-tied D I within the tested Voigt architecture, including under adversarial parent reassignment and the primary multiplicity correction. Q1009+2956 and PKS\,1937$-$101 also show significant departures from exact isotope locking in the calibrated Gate-8 analysis, while J1332$+$0052 is less discriminating. The result therefore demonstrates that the deuterium interpretation is not spectroscopically unique within the tested model class; the isotope-tied model is strongly disfavoured relative to unrestricted H within the tested architecture.

The fixed $-81.6\,{\rm km\,s^{-1}}$ clustering is not an independent discriminator in a sample selected through the deuterium search window. The corresponding falsifiable population test is an excess of suitable displaced H I components outside that window. The archival pilot establishes the practical selection limits of this test and identifies one candidate feature in Q1009+2956, but a substantially larger usable sample is required.

TEP provides a candidate physical interpretation of this displaced-H phenomenology. The conformal absorber field gives the blueward sign but only a $0.005$--$0.01\,{\rm km\,s^{-1}}$ shift. A temporal-disformal channel can reach the observed scale in the explored parametrisation, but its microscopic $B(\phi)$ and full covariant frequency mapping remain open. Independently, the baryonic-cycling calculation shows that a helium-4 equilibrium near the observed abundance is possible under the adopted VMO-dominated, metal-sequestering branch. The spectroscopic, population and light-element predictions therefore provide separate empirical routes for testing the proposed non-hot-BBN interpretation.

## Data Availability & Reproducibility

This work follows open-science practices. All results are fully reproducible from raw data
using the documented pipeline. All numerical results, Monte Carlo simulations, and statistics are generated by deterministic
Python scripts processing real observational data. The pipeline enforces rigorous reproducibility: prespecified statistical outcomes are reported without post-hoc alteration and interpreted according to the scope of each test.

### Repository and Code

GitHub Repository: github.com/matthewsmawfield/TEP-BBN

The repository contains a deterministic, version-controlled cosmological analysis pipeline utilizing 15 analysis steps across 4 phases: core gates (1–8), Gate 8 calibration (step\_08b, true-D injection Monte Carlo), Gate 8 wavelength-systematics sensitivity (step\_08c), disformal transport, secondary robustness analyses, and manuscript finalization.
All steps are orchestrated by `scripts/run_pipeline.py` with comprehensive per-step logging, SHA-256 checksum manifest generation, and a pipeline summary ledger.

All raw spectroscopic data (Keck/HIRES, VLT/UVES + Keck/HIRES, and VLT/ESPRESSO), structural likelihood matrices, and the temporal-field equation solvers are released in the Zenodo repository (DOI: 10.5281/zenodo.21841147) under CC-BY 4.0. The full codebase and execution environments are identical to the published version.

#### Repository Structure

TEP-BBN/
├── data/
│   ├── raw/                       # Spectroscopic exposures (Keck/HIRES, UVES+HIRES, ESPRESSO)
│   │   ├── atomic/                # Physical H I, D I line registries (NIST ASD)
│   │   └── reduced_products/      # Pre-reduced and co-added normalized spectra
│   ├── literature_components/     # Published VPFIT model files and component tables
│   └── processed/                 # Pipeline-ready union manifests
├── scripts/
│   ├── steps/                     # 15 pipeline steps (01-09, 08b, 08c, 09b, secondary, finalize)
│   ├── lib/                       # Physical RT engine, Voigt fitters, model parsers
│   ├── utils/                     # Logging, isotopic shift, shear model utilities
│   └── run_pipeline.py            # Master orchestration script (4-phase pipeline)
├── configs/
│   ├── sightlines/                # Per-sightline JSON configs (bounds, MC settings, noise models)
│   └── TEP_BBN_FOUNDATION_FREEZE.json  # Frozen TEP prior parameters
├── results/                       # Generated parameter ledgers and significance matrices
├── logs/                          # Per-step execution logs
├── site/
│   └── components/                # Manuscript source components
├── requirements-lock.txt          # Locked Python dependencies
└── README.md                      # Documentation

### Data Provenance

| Data Source | Provider | Access Method | Records | Location |
| --- | --- | --- | --- | --- |
| Q1009+2956 Spectra | Keck/HIRES (Zavarygin et al. 2018 <sup>[44]</sup>) | Zavarygin et al. 2018 GitHub | 4 coadds (S/N $\approx 47$–$78$ near Ly$\alpha$) | `data/raw/reduced_products/Q1009+2956_z2.504_HIRES/` |
| PKS 1937$-$101 Spectra | VLT/ESPRESSO (Cooke et al. 2024) | ESO Archive | 3 exposures | `data/raw/spectra/PKS1937-101_z3.572_ESPRESSO/` |
| J1332$+$0052 Spectra | VLT/UVES + Keck/HIRES (Kislitsyn et al. 2024) | ESO Archive | 24 exposures | `data/raw/spectra/J1332+0052_z3.420_UVES/` |
| SQUAD DR1 Spectra | UVES/SQUAD (Murphy et al. 2018 <sup>[43]</sup>) | ESO Phase 3 Archive | 3 sightlines (Q1009, Q0913, J212912) | `data/raw/spectra/SQUAD/` |
| KODIAQ DR2 Spectra | Keck/HIRES (O'Meara et al. 2017) | Keck KOA | 7 LLS-class sightlines | `data/raw/spectra/KODIAQ/` |
| KODIAQ Z LLS Catalog | Lehner et al. 2016 | Literature | 26 pLLSs/LLSs at $2.3 < z < 3.3$ | `data/kodiaq_z_lls_catalog.json` |
| Atomic Data | NIST ASD <sup>[49]</sup> | Static Registry | H I, D I, metals | `data/raw/atomic/` |
| Q1009+2956 Model | Zavarygin et al. <sup>[44]</sup> / VPFIT <sup>[50]</sup> | Static File | 43 H I + 3 D I components | `data/literature_components/model_6a.26` |
| PKS 1937$-$101 Model | Cooke et al. 2024 / VPFIT <sup>[50]</sup> | Static File | 184 H I + 3 D I components | `data/literature_components/PKS1937-101_z3.572_vpfit_model.26` |
| J1332$+$0052 Model | Kislitsyn et al. 2024 / VPFIT <sup>[50]</sup> | Static File | 11 H I + 4 D I components | `data/literature_components/J1332+0052_z3.420_vpfit_model.26` |
| Prior Bounds | Derived | Static File | All variables | `configs/sightlines/*.json` |

### Pipeline Architecture

The analysis pipeline comprises 4 phases and 15 steps spanning spectroscopic ingestion to thermodynamic evaluation, helium synthesis, opacity boundary analysis, Gate 8 true-D injection calibration, wavelength-systematics sensitivity, disformal transport calibration, secondary robustness checks, and manuscript number finalization.
Each step is a standalone Python script in `scripts/steps/` that produces serialized JSON outputs and
detailed logs with SHA-256 checksum verification.

#### Complete Step Inventory and Runtime

Runtimes are approximate and measured on Apple M4 Pro (14-core, 24 GB). The dominant cost is the Monte Carlo significance test (step 03), which scales with the number of realizations multiplied by the parent reassignment refit performed inside each realization.

| Phase | Step | Script | Description | Est. Runtime |
| --- | --- | --- | --- | --- |
| 1 | 01 | `step_01_embedding.py` | Physical atomic-data embedding (H vs D isotope identifiability) | ~1 s |
| 1 | 02 | `step_02_q1009.py` | Nested-hypothesis fit (multi-start; nesting invariants verified) | ~4 min |
| 1 | 03 | `step_03_significance.py` | 1000-realization Monte Carlo significance calibration (parent reassignment inside each realization) | ~25 min |
| 1 | 04 | `step_04_prior.py` | TEP absorber field sign closure ($\Delta v_T < 0$) | ~1 s |
| 1 | 04B | `step_04b_amplitude.py` | TEP absorber amplitude test (conformal/static branch sign theorem) | ~1 s |
| 1 | 05 | `step_05_thermodynamics.py` | Matter-frame temporal thermodynamics (Planck spectrum preservation) | ~1 s |
| 1 | 06 | `step_06_helium.py` | Primordial helium synthesis via baryonic cycling | ~1 s |
| 1 | 07 | `step_07_global_opacity.py` | Analytical proof of divergent optical depth in the static spatial geometry | ~1 s |
| 1 | 08 | `step_08_light_elements.py` | Light-element network (3He, 4He, 7Li) and convergence constraints | ~1 s |
| 1 | 08B | `step_08b_calibration.py` | Gate 8 true-D injection Monte Carlo calibration ($N=1000$ per sightline) | ~45 min |
| 1 | 08C | `step_08c_wavelength_systematics.py` | Gate 8 wavelength-systematics sensitivity (literature-calibrated $\sigma_{\rm sys}$ per sightline, $N=100\,000$ MC) | ~1 s |
| 2 | 09 | `step_09_disformal_transport.py` | Disformal transport solver and absorber-ansatz / Cassini bound bookkeeping | ~1 s |
| 2 | 4B-IV | `step_04h_disformal_clock.py` | Disformal clock mechanism: cosmological $\partial_0\bar\phi$ channel, $B(\phi)$ field-dependence scan, Cassini/GW170817 constraints, three-sightline test | ~1 s |
| 2 | 09B | `step_09b_screening_plot.py` | Screening function visualization and JSON ledger | ~1 s |
| 2 | 6-III | `step_06_orphan_search.py` | Orphan feature search in VPFIT models, direct spectral inspection, and archival SQUAD/KODIAQ search | ~10 s |
| 3 | C2-C4 | `secondary_analyses.py` | Scaffold freedom (C2), perturbed MC (C3), kinematic test (C4) | ~10 min |
| 4 | Final | `finalize_manuscript_numbers.py` | Manuscript number synchronization + SHA-256 checksum manifest | ~1 s |

#### Total Runtime Summary

| Component | Steps | Runtime |
| --- | --- | --- |
| Core Gates (Phase 1) | 10 | ~45 min per sightline |
| Disformal + Secondary (Phases 2–3) | 4 | ~10 min per sightline |
| Finalization (Phase 4) | 1 | ~1 s |
| Total (3 sightlines) | 15 | ~2 hr |

### Reproduction Instructions

#### Quick Start (Full Reproduction)

# 1. Clone repository
git clone https://github.com/matthewsmawfield/TEP-BBN.git
cd TEP-BBN

# 2. Install dependencies
pip install -r requirements-lock.txt

# 3. Run full pipeline (default: Q1009+2956 sightline, 1000 MC sims)
python scripts/run_pipeline.py

# 3b. Quick mode (50 MC sims, for faster testing)
python scripts/run_pipeline.py --quick

# 3c. Run a specific sightline
python scripts/run_pipeline.py --sightline PKS1937-101

# 3d. Run all sightlines with ingested data
python scripts/run_pipeline.py --all-sightlines

# 3e. Skip secondary robustness analyses
python scripts/run_pipeline.py --skip-secondary

# 3f. Custom MC simulation count
python scripts/run_pipeline.py --n-sims 500

# 4. Results will be stored in results/ and logs/
#    Pipeline summary: results/pipeline_summary.json
#    SHA-256 manifest: results/checksums_sha256.json

#### Multi-Sightline Configuration

The pipeline supports multiple D/H absorber sightlines through per-sightline JSON configuration files in `configs/sightlines/`.
Each config specifies the data manifest path, VPFIT model file, noise model, absorber redshift, candidate parameter bounds, multi-start initial points, and Monte Carlo settings.
Three sightlines are currently supported with ingested data: Q1009+2956 (Keck/HIRES, $z=2.5042$), PKS 1937$-$101 (ESPRESSO, $z=3.572$), and J1332$+$0052 (UVES+HIRES, $z=3.421$).
Sightlines without ingested data (PKS 1937$-$1009, HS 0105+1619) are automatically skipped with a diagnostic message.

#### System Requirements

| Component | Minimum | Recommended | Tested On |
| --- | --- | --- | --- |
| CPU | 2 cores | 4+ cores | Apple M4 Pro (14-core) |
| RAM | 4 GB | 8 GB | 24 GB |
| Storage | 1 GB | 2 GB | SSD NVMe |
| OS | Linux/macOS | Linux/macOS | macOS Sequoia 15.1 |

#### Version Changelog (v0.3 → v0.4)

The following changes were applied between v0.3 (Dubai) and v0.4 (Dubai):

| Change | Description |
| --- | --- |
| Literature-calibrated wavelength systematics | The generic $\sigma_{\rm sys} \in \{0.5, 1.0\}$\,km/s scan (step\_08c) is replaced by instrument-specific residual distortion amplitudes from supercalibration studies: $\sigma_{\rm sys} = 0.25$\,km/s for Keck/HIRES (Griest et al. 2010, iodine-cell intra-order distortions $\sim 250$\,m/s), $0.05$\,km/s for VLT/ESPRESSO (Schmidt et al. 2021, laser-frequency-comb discrepancies $\lesssim 24$\,m/s), and $0.20$\,km/s for VLT/UVES+HIRES (Whitmore & Murphy 2014, solar-twin long-range distortions $\sim 200$\,m/s per $1000$\,\AA). The Gate 8 observable is reframed as a *relative* velocity offset between the fitted free-H component and the isotope-shifted position within the same spectrum, so absolute wavelength offsets and inter-night drifts cancel; only intra-spectrum distortions contribute. |
| Gate 8 velocity-deviation significances under systematic floor | Folding the literature $\sigma_{\rm sys}$ into the calibrated spread via $\sigma_{\rm total} = \sqrt{\sigma_{\rm fit}^2 + \sigma_{\rm sys}^2}$ ($N = 100\,000$ Monte Carlo draws per case) gives effective significances of $9.1\sigma$ (Q1009$+$2956, $p \sim 10^{-19}$), $11.0\sigma$ (PKS\,1937$-$101, $p \sim 10^{-27}$), and $2.1\sigma$ (J1332$+$0052, $p = 0.032$). The Q1009 and PKS\,1937 rejections of isotope-D survive at high significance; the J1332 result remains not individually significant after the $\alpha/3$ correction. A sensitivity scan over $\sigma_{\rm sys} \in [0, 1]$\,km/s is reported in results/gate8\_wavelength\_systematics.json; the $9.1\sigma$ Q1009 result degrades to $2.7\sigma$ only at $\sigma_{\rm sys} = 1.0$\,km/s, exceeding all measured intra-spectrum distortions for the relevant instruments. |
| Helium $f_{\rm VMO}$ sensitivity scan | A dedicated scan over $f_{\rm VMO} \in [0.90, 1.00]$ at $\Delta f = 0.005$ resolution (step\_06, results/gate6\_helium\_results.json) confirms that $Y_{\rm eq}$ varies from $0.227$ ($f_{\rm VMO} = 0.90$) to $0.248$ ($f_{\rm VMO} = 1.00$), with the observed $Y_p = 0.245 \pm 0.003$ compatible with $f_{\rm VMO} \in [0.975, 0.995]$ — a range spanning $\Delta f_{\rm VMO} \approx 0.02$, not a single fine-tuned point. The $f_{\rm VMO}$ requirement is softened from $\geq 0.99$ to $\gtrsim 0.97$. |
| Envelope $B(\phi)$ probe | A saturating non-power-law envelope $B(\phi) = B_0\,\phi^2/(1+(\phi/\phi_c)^2)$ is scanned over $\phi_c/M_{\rm Pl} \in [10^{-2}, 10]$ (step\_04h) as a candidate field dependence that behaves as $\phi^2$ at small $\phi$ (Cassini) while saturating at large $\phi$ (cosmological). No viable solution satisfies both the Cassini bound and cross-redshift transfer ($\mathcal{I} > 0$ at all three sightlines) in the scanned range; the saturating form alone is insufficient. A "Limit of the reduced Gate-4B closure" paragraph is added clarifying that the failed power-law transfer constrains the specific reduced construction tested here, not the full TEP matter-frame transport problem, whose covariant $\omega = -u^\mu k_\mu$ evaluation remains open. |
| Supercalibration references | Three supercalibration references added [71] Griest et al. (2010), [72] Whitmore & Murphy (2014), [73] Schmidt et al. (2021). |
| Pipeline step count | step\_08c\_wavelength\_systematics promoted into the disformal phase of `run_pipeline.py`; total step count $14 \to 15$. |

#### Version Changelog (v0.2 → v0.3)

The following changes were applied between v0.2 (Thika) and v0.3 (Dubai):

| Change | Description |
| --- | --- |
| Gate 8 calibration upgraded | True-D injection Monte Carlo increased from $N=200$ to $N=1000$ per sightline. Joint Mahalanobis statistics recomputed; Q1009 and PKS\,1937 remain $p ≤ 0.001$, J1332 $p = 0.023$. |
| J1332 interpretive status downgraded | J1332$+$0052 Gate 8 joint $p = 0.023$ does not survive the $\alpha/3 = 0.0167$ correction among the three Gate-8 statistics. The broad $b$-value ($b_{H,\rm free} \approx 51$\,km/s) is acknowledged as inconsistent with the narrow-edge TEP orphan prediction. Stated as significant at the uncorrected level only. |
| $S_A^{\rm abs}$ / $S_\Sigma^{(\odot)}$ separation | The absorber-regime amplitude ansatz $S_A^{\rm abs}(|\Phi|/c^2)$ and the Solar-System source-charge screening $S_\Sigma^{(\odot)}$ are explicitly distinguished as separate projections of the common environmental scalar configuration. The relation between them remains to be derived from the microscopic scalar solution; the paper no longer re-implies a single operator. |
| Spurious $132\times$ factor removed | An earlier version of the conformal amplitude calculation contained a $132\times$ arithmetic factor with no physical derivation. Removed; the conformal-only amplitude $|\Delta v_{\rm conf}| \approx 0.009$\,km/s at $R = 30$\,kpc now follows directly from the Poisson Green function with uniform-sphere ionisation correction. |

#### Version Changelog (v0.1 → v0.2)

Several analysis fixes were applied between v0.1 and v0.2, each with a quantitative impact on the primary statistic:

| Fix | Description | Impact on $T$ (Q1009) |
| --- | --- | --- |
| Dynamic continuum basis | 10-parameter monomial for Ly$\alpha$ regions (broad H I wing), 5-parameter for metal-line regions. v0.1 used a rigid 3-parameter basis that could not separate the H I wing from the D feature. | $T$: 56.54 → 24.04 |
| VPFIT tie parser fix | Corrected parsing of `x`/`X` tie flags in VPFIT `.26` files. The parser was misclassifying tied H I components, corrupting their column densities by 0.56–0.84 dex and inflating the D model's likelihood. After fix, the H I columns are correctly read and the D model's likelihood decreases appropriately. | $T$: 56.54 → 144.38 → 161.03 |
| Mass-scaled Doppler identifiability | Corrected to use mass-scaled $b$-values at the actual D column ($N_{\rm D} = 5.7\times10^{12}$). v0.1 used $b_H = b_D$ (turbulence-only limit) and an inflated column ($10^{14}$), giving $5.25\sigma$. v0.2: $0.52\sigma$ (thermal), $0.10\sigma$ (mixed), $0.0002\sigma$ (turbulent). | Identifiability: $5.25\sigma$ → $0.10\sigma$ |
| Parent-reassignment interpretation | Corrected: non-significant $p_{\rm parent}$ means D with alternative parent is indistinguishable from free-H (D remains viable), not that TEP is supported. v0.1 inverted this interpretation. | Interpretation corrected; $T_{\rm parent}$ unchanged |
| Per-sightline noise models | v0.1 used a single Q1009-calibrated noise model for all sightlines. v0.2 calibrates per-sightline Student-$t$ models from each absorber's D-model residuals. | PKS $T$: 8982 → 85.41 → 161.31; J1332 $T$: 1886 → 141.56 → 89.14 → 136.97 |
| MC realizations increased | v0.1 used 200 realizations ($p$-precision $\sim 0.015$). v0.2 uses 1000 realizations ($p$-precision $\sim 0.003$). | $N_{\rm MC}$: 200 → 1000 |

The net effect of these fixes is to *strengthen* the TEP thesis: the corrected identifiability ($0.10\sigma$ at actual D column) is far below the v0.1 claim ($5.25\sigma$), meaning H and D are substantially less distinguishable than previously reported. The primary statistic $T$ started at 56.54 (v0.1), decreased to 24.04 after the continuum basis fix, then increased to 144.38 after the tie parser fix, and finally to 161.03 after the Gate 2 re-run with the corrected noise model and continuum basis. The Monte Carlo calibration yields $p_{\rm std} = 0.001$ and $p_{\rm parent} = 0.001$ (both significant) — a more honest and defensible result than the v0.1 headline.

## References

- Smawfield, M.L. Temporal Equivalence Principle: Dynamic Time & Emergent Light Speed. *Zenodo* (2025), v0.11 (Jakarta). DOI: 10.5281/zenodo.16921911

- Smawfield, M.L. Temporal Equivalence Principle: A Covariant Alternative to Cosmic Expansion. *Zenodo* (2026). DOI: 10.5281/zenodo.20370143

- Smawfield, M.L. Temporal Equivalence Principle: Native hi_class Conformal Implementation, Linear Perturbation Closure, and CMB Acoustic Peak Preservation. *Zenodo* (2026). DOI: 10.5281/zenodo.20572722

- Smawfield, M.L. Temporal Equivalence Principle: Temporal Horizon Cosmology and the Absence of a Physical Big Bang Singularity. *Zenodo* (2026). DOI: 10.5281/zenodo.20723059

- Hawking, S.W. The occurrence of singularities in cosmology. *Proc. R. Soc. A* **294**, 511-521 (1966).

- Hawking, S.W. & Penrose, R. The singularities of gravitational collapse and cosmology. *Proc. R. Soc. A* **314**, 529-548 (1970).

- Borde, A., Guth, A.H. & Vilenkin, A. Inflationary spacetimes are incomplete in past directions. *Phys. Rev. Lett.* **90**, 151301 (2003).

- Brandenberger, R. & Peter, P. Bouncing cosmologies: progress and problems. *Found. Phys.* **47**, 797-850 (2017).

- Novello, M. & Bergliaffa, S.E.P. Bouncing cosmologies. *Phys. Rep.* **463**, 127-213 (2008).

- Ijjas, A. & Steinhardt, P.J. Entropy, black holes and the new cyclic universe. *Phys. Lett. B* **824**, 136823 (2022).

- Peebles, P.J.E. *Principles of Physical Cosmology*. Princeton University Press (1993).

- Weinberg, S. *Cosmology*. Oxford University Press (2008).

- Dodelson, S. *Modern Cosmology*. Academic Press (2003).

- Mukhanov, V.F., Feldman, H.A. & Brandenberger, R.H. Theory of cosmological perturbations. *Phys. Rep.* **215**, 203-333 (1992).

- Liddle, A.R. & Lyth, D.H. *Cosmological Inflation and Large-Scale Structure*. Cambridge University Press (2000).

- Planck Collaboration, et al. Planck 2018 results. VI. Cosmological parameters. *A&A* **641**, A6 (2020).

- Riess, A.G., et al. Milky Way Cepheid Standards for Measuring Cosmic Distances and Application to Gaia DR2: Implications for the Hubble Constant. *ApJ* **861**, 126 (2018).

- Brout, D., et al. The Pantheon+ Analysis: Cosmological Constraints. *ApJ* **938**, 110 (2022).

- Fixsen, D.J., et al. The Cosmic Microwave Background Spectrum from the Full COBE FIRAS Data Set. *ApJ* **473**, 576 (1996).

- Chluba, J. & Sunyaev, R.A. The evolution of CMB spectral distortions in the early Universe. *MNRAS* **419**, 1294-1314 (2012).

- PARTICLE DATA GROUP. Review of Particle Physics. *PTEP* **2022**, 083C01 (2022).

- Cyburt, R.H., Fields, B.D., Olive, K.A. & Yeh, T.H. Big bang nucleosynthesis: Present status. *Rev. Mod. Phys.* **88**, 015004 (2016).

- Seager, S., Sasselov, D.D. & Scott, D. A new calculation of the recombination epoch. *ApJ* **523**, L1-L5 (1999).

- Peebles, P.J.E. Recombination of the Primeval Plasma. *ApJ* **153**, 1 (1968).

- Zeldovich, Y.B. & Sunyaev, R.A. The interaction of matter and radiation in a hot-model universe. *Astrophys. Space Sci.* **4**, 301-316 (1969).

- Seljak, U. & Zaldarriaga, M. A Line of Sight Integration Approach to Cosmic Microwave Background Anisotropies. *ApJ* **469**, 437 (1996).

- Lewis, A., Challinor, A., & Lasenby, A. Efficient Computation of CMB Anisotropies in Closed FRW Models. *ApJ* **538**, 473 (2000).

- Lesgourgues, J. & Tram, T. The Cosmic Linear Anisotropy Solving System (CLASS). Part IV: efficient implementation of non-cold relics. *JCAP* **09**, 032 (2011).

- Zumalacárregui, M., Bellini, E., Sawicki, I., Lesgourgues, J. & Ferreira, P.G. hi_class: Horndeski in the Cosmic Linear Anisotropy Solving System. *JCAP* **08**, 019 (2017).

- De Felice, A. & Tsujikawa, S. f(R) Theories. *Living Rev. Rel.* **13**, 3 (2010).

- Wetterich, C. Cosmology and the fate of dilatation symmetry. *Nucl. Phys. B* **302**, 668-696 (1988).

- Wetterich, C. A universe without expansion. *Phys. Dark Universe* **2**, 184 (2013).

- Narlikar, J.V. & Arp, H.C. Flat spacetime cosmology: A unified framework for extragalactic redshifts. *Astrophys. J.* **405**, 51-56 (1993).

- Mannheim, P.D. Conformal gravity and the nature of dark matter. *Prog. Part. Nucl. Phys.* **94**, 217-272 (2017).

- Khoury, J. & Weltman, A. Chameleon cosmology. *Phys. Rev. D* **69**, 044026 (2004).

- Hinterbichler, K. & Khoury, J. Symmetron cosmology. *Phys. Rev. Lett.* **104**, 231301 (2010).

- Penrose, R. Before the Big Bang: an outrageous new perspective and its implications for particle physics. *Proc. EPAC* (2006).

- Tod, K.P. Isotropic cosmological singularities. *Gen. Relativ. Gravit.* **35**, 779-805 (2003).

- Tod, K.P. The equations of conformal cyclic cosmology. *Gen. Relativ. Gravit.* **47**, 31 (2015).

- Ratra, B. & Peebles, P.J.E. Cosmological Consequences of a Rolling Homogeneous Scalar Field. *Phys. Rev. D* **37**, 3406 (1988).

- Caldwell, R.R., Dave, R., & Steinhardt, P.J. Cosmological Imprint of an Energy Component with General Equation of State. *Phys. Rev. Lett.* **80**, 1582 (1998).

- Clifton, T., Ferreira, P.G., Padilla, A. & Skordis, C. Modified gravity and cosmology. *Phys. Rep.* **513**, 1-189 (2012).

- Murphy, M.T., Kacprzak, G.G., Savorgnan, G.A.D. & Carswell, R.F. The UVES Spectral Quasar Absorption Database (SQUAD) data release 1: the first 10 million seconds. *MNRAS* **482**, 3458-3482 (2019). arXiv:1810.06136

- Zavarygin, E., Webb, J.K., Dumont, V. & Riemer-Sørensen, S. The primordial deuterium abundance at z<sub>abs</sub> = 2.504 from a high signal-to-noise spectrum of Q1009+2956. *MNRAS* **477**, 5536-5553 (2018). arXiv:1706.09512

- Cooke, R.J., Pettini, M., Jorgenson, R.A., Murphy, M.T. & Steidel, C.C. Precision measures of the primordial abundance of deuterium. *ApJ* **781**, 31 (2014).

- Burles, S. & Tytler, D. The Deuterium Abundance toward QSO 1009+2956. *ApJ* **507**, 732 (1998).

- O'Meara, J.M., Burles, S., Prochaska, J.X., Prochter, G.E., Bernstein, R.A. & Burgess, K.M. The Deuterium-to-Hydrogen Abundance Ratio toward the QSO SDSS J155810.16-003120.0. *ApJ* **649**, L61 (2006).

- Kirkman, D., Tytler, D., Burles, S., Lubin, D. & O'Meara, J.M. On the primordial deuterium abundance. *ApJ* **529**, 655 (2000).

- Kramida, A., Ralchenko, Yu., Reader, J. & NIST ASD Team. NIST Atomic Spectra Database (ver. 5.11). National Institute of Standards and Technology, Gaithersburg, MD (2023).

- Carswell, R.F. & Webb, J.K. VPFIT: Voigt profile fitting program. Astrophysics Source Code Library, ascl:1408.015 (2014).

- Smawfield, M.L. The Cepheid Bias: Resolving the Hubble Tension. *Zenodo* (2026). DOI: 10.5281/zenodo.18209702

- Smawfield, M.L. Temporal Equivalence Principle: A Unified Resolution to the JWST High-Redshift Anomalies. *Zenodo* (2026). DOI: 10.5281/zenodo.19000827

- Smawfield, M.L. Temporal Equivalence Principle: Temporal Shear in the Earth Flyby Anomaly. *Zenodo* (2026). DOI: 10.5281/zenodo.19454863

- Smawfield, M.L. Temporal Equivalence Principle: Black Holes and the Temporal Horizon. *Zenodo* (2026). DOI: 10.5281/zenodo.21677826

- Haardt, F. & Madau, P. Radiative transfer in a clumpy universe. IV. New synthesis models of the UV/X-ray cosmic background. *ApJ* **746**, 125 (2012).

- Benisty, D., Brax, P. & Davis, A.C. Constraining modified gravity with cosmological data. *Phys. Rev. D* **107**, 064049 (2023).

- Carr, B.J., Bond, J.R. & Arnett, W.D. Cosmological consequences of Population III stars. *ApJ* **277**, 445-469 (1984).

- Bond, J.R., Arnett, W.D. & Carr, B.J. The evolution and fate of Very Massive Objects. *ApJ* **280**, 825-847 (1984).

- Bertotti, B., Iess, L. & Tortora, P. A test of general relativity using radio links with the Cassini spacecraft. *Nature* **425**, 374-376 (2003).

- Ober, W.W., El Eid, M.F. & Fricke, K.J. Evolution of massive Pop III stars with helium-overshooting. *A&A* **119**, 61-68 (1983).

- Aver, E., Olive, K.A. & Skillman, E.D. The effects of He I λ10830 on helium abundance determinations. *JCAP* **07**, 011 (2011).

- Izotov, Y.I., Thuan, T.X. & Guseva, N.G. A new determination of the primordial He-4 abundance: A self-consistent reanalysis of the H II region data. *MNRAS* **445**, 778-801 (2014).

- Peimbert, M., Peimbert, A. & Luridiana, V. The primordial helium abundance and the number of neutrino species. *Rev. Mex. Astron. Astrofis.* **52**, 319-326 (2016).

- Planck Collaboration, et al. Planck 2018 results. VI. Cosmological parameters. *A&A* **641**, A6 (2020). (See also: Cooke, R.J., Pettini, M. & Steidel, C.C. The primordial deuterium abundance and the baryon density. *ApJ* **817**, 79 (2016) for the D/H → Ω<sub>b</sub>h² concordance.)

- Cooke, R.J., Pettini, M. & Steidel, C.C. The primordial deuterium abundance and the baryon density. *ApJ* **817**, 79 (2016).

- Cooke, R.J., et al. ESPRESSO observations of the D/H ratio in PKS 1937−101. *MNRAS*, stae452 (2024). arXiv:2402.05586

- Kislitsyn, R., Balashev, S.A., Murphy, M.T., et al. A new precise determination of the primordial abundance of deuterium: measurement in the metal-poor sub-DLA system at z = 3.42 towards quasar J 1332+0052. *MNRAS* **528**, 4068-4084 (2024). arXiv:2401.12797

- Fields, B.D., Olive, K.A., Yeh, T.H. & Cyburt, R.H. The Hubble tension and the primordial helium abundance. *Universe* **9**, 165 (2023).

- Smawfield, M.L. Temporal Topology Saturation Scale: Cross-Scale Consistency of $\rho_T$. *Zenodo* (2026). DOI: 10.5281/zenodo.18064365

- Smawfield, M.L. Temporal Equivalence Principle: Lunar Laser Ranging and the Nordtvedt Effect. *Zenodo* (2026). DOI: 10.5281/zenodo.19446029

- Griest, K., Whitmore, J.B., Wolfe, A.M., Prochaska, J.X., Dawley, M.M. & Vladilo, G. Wavelength Accuracy of the Keck HIRES Spectrograph and Measuring Changes in the Fine Structure Constant. *ApJ* **708**, 158-170 (2010). DOI: 10.1088/0004-637X/708/1/158

- Whitmore, J.B. & Murphy, M.T. Impact of instrumental systematic errors on fine-structure constant measurements with quasar spectra. *MNRAS* **444**, 2 (2014). DOI: 10.1093/mnras/stu2420. arXiv:1409.4467

- Schmidt, T.M., Murphy, M.T., Lo Curto, G., et al. Fundamental physics with ESPRESSO: Towards an accurate wavelength calibration for a precision test of the fine-structure constant. *A&A* **646**, A104 (2021). DOI: 10.1051/0004-6361/202039345
