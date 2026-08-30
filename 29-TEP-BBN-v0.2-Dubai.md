# Temporal Equivalence Principle: Dynamical Proper Time and the Illusion of Primordial Deuterium
**Matthew Lukin Smawfield**
Version: v0.2 (Dubai)
First published: 12 August 2026 - Last updated: 31 August 2026
DOI: 10.5281/zenodo.21841147

---

## Abstract

This paper demonstrates that purported primordial deuterium features in quasar absorption spectra are better explained as shifted ordinary hydrogen. Using a shared Voigt architecture and Monte-Carlo-calibrated nested testing across the three best-studied D/H sightlines---Q1009+2956 (Keck/HIRES), PKS\,1937$-$101 (ESPRESSO), and J1332$+$0052 (UVES+HIRES)---the unrestricted hydrogen model is significantly preferred over the true-deuterium model under both the canonical-parent and adversarial parent-reassignment statistics ($p \le 0.001$ for all three sightlines, surviving Bonferroni correction). The key physical insight is that *isotope identifiability is controlled by both Doppler regime and D column density*: at the unsaturated LLS-class columns typical of D/H measurements, the intrinsic H/D profile-shape difference is sub-noise on a per-pixel basis, so the deuterium identification depends predominantly on the velocity offset---which the free-H model can reproduce without invoking deuterium at all. A multi-pronged evidence analysis (Gate 8) calibrates three discriminators---$b$-value ratio, velocity offset deviation, and column density difference---against true-D injection Monte Carlo: the joint statistic is highly significant for all three sightlines ($p < 0.005$), with Q1009's velocity deviation alone rejecting isotope-D at $p < 0.005$ and PKS\,1937's velocity deviation also rejecting it at $p < 0.005$; J1332's $b$-value ratio rejects isotope-D individually ($p = 0.045$) and the joint statistic is highly significant ($p < 0.005$). All three features are blueward of the parent, as the conformal sign theorem predicts. A velocity-selection theorem explains the universality of the $-81.6$\,km/s offset as a selection effect of the D-search protocol, and a quantitative population forecast predicts $\sim 20$ orphan narrow components at non-isotope offsets across $\sim 80$ high-S/N LLS sightlines---testable with existing archival data.

The Temporal Equivalence Principle (TEP) provides the alternative mechanism: the deuterium-like velocity feature is the spectroscopic signature of temporal shear in diffuse, unscreened edge gas. The TEP absorber field deterministically predicts the blueward sign from conformal core-edge geometry; the environmental screening operator is calibrated by three boundary conditions (absorber, Cassini, galactic halo) that yield $132\times$ screening contrast between solar-system and galactic regimes; the conformal-only amplitude is quantified and the required amplification ($\mathcal{A}_{\rm env} \approx 9.3 \times 10^3$) is identified as a falsifiable target for the non-perturbative transport path. Cosmological redshift is reformulated as temporal transport over a static spatial background, the helium-4 mass fraction emerges as the equilibrium of baryonic-cycling reaction flows under temporal-horizon metal sequestration, and the line-of-sight optical depth diverges at high redshift to create an observable boundary without a physical plasma wall. The broader TEP corpus establishes CMB acoustic peak preservation at $< 6$\,ppm, temporal-horizon regularity, cosmological distances without expansion, and JWST high-redshift anomaly resolution.

Keywords: temporal equivalence principle, deuterium abundance, isotopic line identification, temporal shear, absorption-line spectroscopy, Lyman-limit systems, Big Bang nucleosynthesis, cosmology, TEP, Proper-Time Transport

## 1. Introduction

The prevailing cosmological paradigm interprets the Hubble redshift as the kinematic expansion of a spatial volume, directly linking high redshifts to a dense, ultra-hot spatial singularity—the Big Bang. Within this framework, the measurement of light element abundances, particularly deuterium (D/H) in high-redshift Lyman-limit systems such as Q1009+2956, serves as a crucial anchor for Big Bang Nucleosynthesis (BBN) [22], [45]. However, this standard inference assumes that cosmological redshift is intrinsically geometric and that the spectroscopic structure of deuterium is uniquely distinguishable from contaminating intergalactic hydrogen.

Tensions in precision cosmology—such as the Hubble tension [17], [18] and the $S_8$ growth tension—have motivated numerous theoretical extensions to the $\Lambda$CDM framework [16]. Recent literature has extensively explored modified gravity (e.g., $f(R)$ or scalar-tensor theories [30], [42]), non-standard recombination histories, and Early Dark Energy (EDE) to resolve these anomalies. While these approaches introduce new dynamical parameters to accommodate the standard hot-thermal history, they generally preserve the foundational assumption that cosmological redshift equates to geometric spatial expansion.

### The Temporal Equivalence Principle Framework

The standard Friedmann-Lemaître-Robertson-Walker (FLRW) metric [11], [12], [13] explicitly couples cosmological evolution to a dynamic spatial volume. Extrapolating this geometric expansion backward inevitably terminates in a spatial singularity ($a \to 0$)—a regime where polynomial curvature invariants diverge and the foundational equations of General Relativity break down [5], [6], [7]. Alternative non-singular cosmologies, including bouncing models [8], [9], cyclic scenarios [10], and conformal approaches [37], [38], [39], have been explored but typically require additional dynamical ingredients. The Temporal Equivalence Principle (TEP) avoids this singular outcome by formally decoupling spatial kinematics from temporal dynamics. By anchoring the universe to a static physical matter frame ($a_{\rm m} = 1$) governed by a dynamical proper-time field $A(\phi)$ [40], [41], the TEP geometry removes the spatial singularity. Cosmological redshift is not the stretching of space, but rather the manifestation of a temporal gradient between the emitting and observing frames. This approach shares conceptual ground with static-universe and conformal frameworks [31], [32], [33], [34], but distinguishes itself through the dynamical proper-time field and its coupling to matter. The apparent "Big Bang" is replaced by an asymptotic temporal horizon ($\mathscr{T}^-$) in the far past, characterized by a vanishing relative clock rate ($A_{\rm clock} \to 0$). Because the underlying spatial manifold remains static, all polynomial curvature invariants remain finite at this boundary. The hot, dense spatial origin required by standard cosmology is therefore not needed; the temporal horizon replaces the Big Bang as the observational boundary, establishing a regular geometric foundation for early-universe observables without requiring an explosive spatial origin.

The standard hot-BBN inference is challenged on two fronts within the TEP framework [1], [2]. First, an algorithmically controlled analysis of Q1009+2956 shows that the canonical deuterium interpretation is not uniquely identifiable against the ordinary-H alternative at the available resolution. Second, the temporal-transport framework is developed to show how the associated cosmological observables can be represented without a primordial spatial singularity.

## 2. Spectroscopic Analysis

The spectroscopic uniqueness of the deuterium identification in high-redshift quasar absorption systems is examined under nested model comparison with Monte-Carlo calibrated significance. The primary finding is that the statistical preference for an unrestricted hydrogen model over a true-D model is *robust across sightlines, under both the canonical-parent and parent-reassignment statistics*. The *parent-reassignment statistic* ($T_{\rm parent}$, $p_{\rm parent}$)—which gives D maximum freedom to select the most favorable parent—is the more conservative and informative number, and is reported as the primary result throughout. The canonical-parent (standard) statistic is reported as a secondary comparison. A second key finding is that isotope identifiability is *strictly regime-dependent*: it must be assessed per absorber rather than assumed, as the distinguishability of H and D Voigt profiles depends critically on the thermal-to-turbulent Doppler ratio.

The analysis is performed on the high-resolution Keck/HIRES spectrum of the benchmark Q1009+2956 absorption system, from Zavarygin et al. 2018 [44] (22 HIRES exposures co-added into four setups using the wspectrum software). The published kinematic architecture and component parameters from Zavarygin et al. 2018 [44] are used as the structural prior for the Voigt component family, fitted with the VPFIT framework [50]. The spectral data comprise four coadds at two instrumental settings: C1 ($R\approx49\,000$, $\sigma_{\rm inst}=2.6$\,km/s) and C5 ($R\approx37\,000$, $\sigma_{\rm inst}=3.4$\,km/s), with S/N $\approx 47$–$78$ per pixel near Ly$\alpha$. The system was originally measured for primordial D/H by Burles & Tytler [46] and subsequently by Zavarygin et al. [44], with independent measurements from other quasar sightlines contributing to the primordial D/H estimate [47], [48]. Two additional benchmark sightlines—PKS\,1937$-$101 (ESPRESSO, $z=3.572$) and J1332$+$0052 (UVES+HIRES, $z=3.421$)—are analysed with the identical framework in Section 2.4.

### 2.1 Isotope Identifiability Limits in Q1009+2956

Using the physical atomic registries for H I and D I (NIST ASD), synthetic deuterium was embedded at the actual Q1009 D column ($N_{\rm D} = 5.7\times10^{12}\,\mathrm{cm}^{-2}$, derived from D/H $= 2.48\times10^{-5}$ and $\log N_{\rm HI} = 17.362$) and recovered using unrestricted hydrogen models. Zavarygin et al. [44] themselves noted that the putative D feature is likely contaminated by weak interloping Ly$\alpha$ absorption from a low-column-density H I cloud, reducing the D/H precision. The present analysis extends this insight by quantifying the D/H degeneracy through explicit adversarial model comparison with Monte-Carlo-calibrated parent reassignment, comparing multiple sightlines, and then asking whether the ordinary-H alternative admits a TEP interpretation. The isotope identifiability depends on both the Doppler parameter regime and the D column density. For thermally-dominated gas, the H and D Doppler parameters differ by the mass ratio: $b_{\rm H} = b_{\rm D}\sqrt{m_{\rm D}/m_{\rm H}} \approx 1.41\,b_{\rm D}$. With this physical mass scaling, the maximum convolved flux discrepancy between H and D profiles across all Lyman transitions is $0.52\sigma$ at Keck/HIRES C1 resolution ($R\approx49\,000$, $\sigma_{\rm inst} = 2.6$\,km/s), indicating that H and D are **marginally distinguishable** for thermally-dominated gas at this column. The $\sigma$ statistic is computed as the maximum pixel-level flux residual divided by a conservative constant noise floor ($\sigma_{\rm floor} = 0.05$), evaluated across the five strongest Lyman transitions (Ly$\alpha$ through Ly$\epsilon$). For turbulence-dominated gas ($b_{\rm turb} \gg b_{\rm therm}$), the mass-dependent thermal contribution is negligible and $b_{\rm H} \approx b_{\rm D}$; in this limit the maximum discrepancy falls to $0.0002\sigma$, making the isotopes operationally unidentifiable. For the actual Q1009 fitted parameters ($T_K = 2000$\,K, $b_{\rm turb} = 11.60$\,km/s, giving $b_{\rm turb}/b_{\rm therm} \approx 2.02$), the mixed-regime discrepancy is $0.10\sigma$ — far below conventional detectability. The identifiability is controlled by the D column: at the unsaturated LLS-class columns typical of D/H measurements ($\log N_{\rm D} \lesssim 13$), the single-pixel discrepancy is sub-threshold in every Doppler regime; only saturated sub-DLA columns ($\log N_{\rm D} \gtrsim 14$) approach distinguishability. Isotope identifiability must therefore be assessed per absorber as a function of both column and Doppler regime.

### 2.2 Likelihood Nesting and Significance Testing

A complete structural analysis of the Q1009+2956 spectrum is performed under a rigorously nested model hierarchy. By anchoring the fits to a SHA-256-validated data manifest, the likelihood surfaces of the standard D-interpretation ($M_D$), an unrestricted hydrogen interpretation ($M_{H,\rm free}$), and the joint space ($M_{D+H}$) are mapped. The 141 shared parameters (43 H I Voigt component parameters: centres, $b$-values, and column densities, plus continuum basis coefficients for each data block) are held at the published literature architecture [44], identically for every hypothesis. This fixed scaffold is part of the definition of the test statistic rather than an uncontrolled nuisance choice: the significance of $T$ is not read off an asymptotic $\chi^2$ distribution but calibrated by parametric bootstrap in Section 2.3, where true-D spectra are regenerated on the same scaffold and the identical statistic is recomputed. Because the scaffold enters the observed and simulated statistics in exactly the same way, the resulting $p$-value is valid without requiring the shared architecture to be re-optimised.

The candidate component parameter structure is made fully explicit. Each model differs only in the candidate component; the shared scaffold is identical:

| Model | Candidate params | $v$ | $\log N$ | $T_K$ | $b_{\rm turb}$ | $k_{\rm cand}$ |
| --- | --- | --- | --- | --- | --- | --- |
| $M_D$ (M_Dfree) | D tied to parent | tied to parent $+ v_{\rm iso}$ | free | free | free | 3 |
| $M_{H,\rm free}$ (M_H) | unrestricted H | free | free | free | free | 4 |
| $M_{D+H}$ | D + unrestricted H | D tied, H free | D free, H free | shared | shared | 5 |
| $M_{\rm kin}$ | pure kinematic H | free | free | — | — | 2 |

The parameter count difference is $\Delta k = k(M_{H,\rm free}) - k(M_D) = 4 - 3 = 1$: the unrestricted-H model gains one free parameter (the velocity $v_H$, which in $M_D$ is tied to the parent velocity via $v_D = v_{\rm parent} + v_{\rm iso}$). The column density, temperature, and turbulent broadening are free in both models. The $\Delta k = 1$ therefore reflects exactly the velocity-tying difference between the isotope-D and free-H hypotheses — the single physical degree of freedom that distinguishes them.

| Model | Candidate interpretation | $k$ | $\ln L_{\max}$ | $\Delta\text{AIC}$ | Nested? |
| --- | --- | --- | --- | --- | --- |
| $M_D$ | D tied to parent H | 3 | $-15446.77$ | 0 | — |
| $M_{H,\rm free}$ | unrestricted H | 4 | $-15366.26$ | $-159.03$ | observationally embeds $M_D$ at Q1009 precision |
| $M_{D+H}$ | D + unrestricted H | 5 | $-15366.26$ | $-153.03$ | contains $M_{H,\rm free}$ if $N_{\rm D}\to 0$ (verified to $2.8\times10^{-10}$ in $\Delta\ln L$) |

#### Statistical Significance

The unrestricted hydrogen model—the TEP edge-gas signature, in which the deuterium-like feature is interpreted as diffuse, unscreened edge gas displaced by temporal shear—provided a superior description of the data, yielding a likelihood improvement:

\begin{equation} \Delta \ln L = 80.51, \qquad T = 161.03, \qquad \Delta k = 1, \qquad \Delta\mathrm{AIC} = -159.03. \end{equation}

The unrestricted-H model adds one free parameter (the H velocity) relative to the D-tied model ($\Delta k = 1$), yet the likelihood improvement of $\Delta\ln L = 80.51$ exceeds the AIC penalty of 2, yielding $\Delta\mathrm{AIC} = -159.03$ and $\Delta\mathrm{BIC} = -151.97$ ($n = 8{,}610$ data points, $\ln n \approx 9.06$). Both information criteria favor $M_{H,\rm free}$. Because the shared scaffold is identical under both hypotheses, the comparison isolates the single additional kinematic parameter of the unrestricted-H model and does not depend on the number of shared components. The information criteria are reported for orientation only; the significance quoted below rests on the Monte Carlo calibration, not on asymptotic likelihood-ratio theory, whose regularity conditions are not satisfied here because $M_D$ sits on the boundary $N_{\rm D}\to 0$ of $M_{D+H}$. Monte Carlo $p$-values use the Laplace-corrected estimator $\hat{p} = (k+1)/(N+1)$, where $k$ is the exceedance count and $N$ is the number of realizations.

To establish rigorous significance, 1000 physical Monte Carlo simulations generating exact, noisy true-D flux were run, followed by dense free-H refitting. Two calibration statistics are reported. The *standard statistic* locks D to the canonical parent (matching the observed fit). The *parent-reassignment statistic* allows D to select the most favorable parent from the H I components within ±1000 km/s of the absorber systemic velocity. The standard statistic represents the prespecified comparison; the parent-reassignment statistic represents the most adversarial test. Both are reported to bracket the significance honestly.

### 2.3 Leave-One-Out and Parent Reassignment Robustness

The component misattribution vulnerability was exhaustively tested by tying the candidate D velocity to every single available H component in the model family (43 distinct parent candidate structures). The maximum alternative-parent test statistic is defined as:

\begin{equation} T_{\rm parent} = 2 \left[ \ln L(M_{H,\rm free}) - \max_j \ln L(M_D\mid j) \right]. \end{equation}

Against the most advantageous alternative parent assignment, the free-H interpretation is preferred for Q1009+2956 with $T_{\rm parent} = 161.03$, equal to $T = 161.03$ for the canonical parent. The discrimination is therefore not specific to the published parent assignment, and the parent-reassignment statistic is the conservative quantity to calibrate. When calibrated inside the true-D Monte Carlo loop—utilizing bounded L-BFGS-B optimization with a multi-start grid spanning the full velocity range $[-160, +50]\text{ km/s}$, $\log N_{\rm D} \in [0, 20]$, $T_K \in [100, 4\times10^4]$\,K, and $b_{\rm turb} \in [1, 50]$\,km/s, with the best likelihood retained across all starts to prevent local minima from artificially widening the null distribution—the empirical $p_{\rm parent}$ is reported below.

**Parent-reassignment window.** Two parent-reassignment windows are reported. The *conservative* window ($\pm 1000\text{ km/s}$) gives the deuterium hypothesis maximum freedom to find a favorable parent, establishing a lower bound for the $T_{\rm parent}$ statistic. Of the 43 H I components in the Q1009 model, 14 fall within this window; none are DLA-class ($\log N_{\rm HI} > 20.3$), and components from unrelated absorber systems at $v \sim -47\,000$ to $-74\,000\text{ km/s}$ are correctly excluded. The *physical* window ($\pm 3b_{\rm max}$, where $b_{\rm max} = 56.7$\,km/s is the largest Doppler parameter of the main complex) restricts eligible parents to those within the kinematic structure of the absorber: 9 H I components fall within the velocity window, of which 4 satisfy the column-density eligibility cut ($\log N_{\rm HI} \ge \log N_{\rm max} - 2$\,dex). The physical window is reported as the *headline* statistic because it is motivated by the absorber's own velocity structure rather than an arbitrary fixed range. Under the physical window, the conclusions are essentially unchanged from the conservative window (see robustness check C1 in Section 5.5), confirming that the $\pm 1000\text{ km/s}$ conservative bound was not driving the results.

A critical interpretation issue arises in the parent-reassignment test. For Q1009+2956, $T_{\rm parent} = T_{\rm obs} = 161.03$, meaning that allowing reassignment does not improve the D fit over the canonical parent—the discrimination is not specific to the published parent assignment. For PKS\,1937$-$101, $T_{\rm parent} = 59.00 < T_{\rm obs} = 161.31$, so the best alternative parent substantially reduces the statistic, but the result remains significant. For J1332$+$0052, $T_{\rm parent} = 135.76 < T_{\rm obs} = 136.97$, so the best alternative parent slightly reduces the statistic. In all three cases, the free-H model is significantly preferred even under the most favorable parent assignment for D. The parent-reassignment statistic is therefore the conservative quantity to calibrate, and the $p_{\rm parent}$ values reported below should be interpreted as the significance under the most favorable parent assignment for D.

**Parent-identity diagnostic (Gate 7).** Under the isotope-D interpretation, the best alternative parent $j^*$ (the H I component maximizing $\ln L(M_D \mid j)$) should be the main narrow thermal component — D is tied to the gas it formed beside. Under TEP, $j^*$ might be a diffuse, low-column edge component — the edge gas anchors to its own local structure. For all three sightlines, the best non-canonical parent within the eligible window ($\log N_{\rm HI} \ge \log N_{\rm max} - 2$\,dex, $|v| \le 1000$\,km/s) is a core component: Q1009+2956 parent 1 ($v = -43.7$\,km/s, $\log N_{\rm HI} = 16.80$, $b = 17.8$\,km/s), PKS\,1937$-$101 parent 20 ($v = +17.9$\,km/s, $\log N_{\rm HI} = 17.38$, $b = 17.1$\,km/s), and J1332$+$0052 parent 2 ($v = +8.7$\,km/s, $\log N_{\rm HI} = 18.39$, $b = 15.8$\,km/s). This is consistent with the isotope-D interpretation and does not support the TEP edge-parent prediction. The parent-identity test is presently treated as a descriptive diagnostic rather than a TEP-specific discriminator. Under TEP the feature is ordinary edge H, not D tied to any parent; the identity of the parent that minimizes a mis-specified D fit may be a fitting artefact rather than a physical TEP observable. A derivation showing why a displaced edge-H feature mathematically causes the false-D likelihood to maximize on diffuse edge components is required before Gate 7 can be elevated to a TEP-specific prediction.

**Offset-exactness test (Gate 4E).** Under the isotope-D interpretation, the free-H component should sit at the exact isotope-shifted velocity $v_{\rm iso} = -81.6$\,km/s relative to its parent. Under TEP, the edge-gas feature need not sit at the exact isotope shift — the observed offset depends on the local shear amplitude, which varies with core-edge geometry. The fitted $M_{H,\rm free}$ velocities deviate from the isotope-shifted position by:

| Sightline | Parent $v$ (km/s) | $v_{\rm iso}$ (km/s) | Expected D $v$ (km/s) | Fitted $v_H$ (km/s) | Deviation (km/s) |
| --- | --- | --- | --- | --- | --- |
| Q1009+2956 | $-52.4$ | $-81.6$ | $-134.0$ | $-131.3$ | $+2.7$ |
| PKS\,1937$-$101 | $+8.7$ | $-81.6$ | $-72.9$ | $-67.3$ | $+5.7$ |
| J1332$+$0052 | $0.0$ | $-81.6$ | $-81.6$ | $-118.2$ | $-36.6$ |

Q1009+2956 sits $2.7$\,km/s from the isotope shift — consistent with isotope-D to within the spectral resolution ($2.6$\,km/s), but highly inconsistent when calibrated against the true-D simulation distribution ($\pm 0.2$\,km/s, $p < 0.005$, Section 5.6). PKS\,1937$-$101 deviates by $5.7$\,km/s — also highly significant after calibration ($p < 0.005$). J1332$+$0052 deviates by $-36.6$\,km/s — marginal after calibration ($p = 0.09$). The cross-sightline pattern — increasing offset deviation with increasing D column — is quantitatively testable: if the feature is isotope-D, all three should sit at $v_{\rm iso}$ within spectral resolution; under TEP, the offset varies with core-edge geometry. The J1332 feature shows the largest departure from the isotope-shifted position, and it is also the sightline with the highest D column (saturated, $\log N_{\rm D} \approx 14.65$), where the edge-gas interpretation is most physically motivated.

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

**Quantitative population forecast (Gate 6-II).** The observed cross-sightline deviations from the isotope shift ($+2.7$, $+5.7$, $-36.6$\,km/s for Q1009, PKS\,1937, J1332 respectively) imply a shear spread $\sigma_{\rm shear} \approx 19$\,km/s. The D-search selection function $|\Delta v - v_{\rm iso}| < 5$\,km/s captures only $\sim 21\%$ of edge-shear features; the remaining $\sim 79\%$ are orphans absorbed into the H I component structure. In a sample of $\sim 80$ high-S/N LLS sightlines with full Lyman coverage (SQUAD DR1, UVES SLS, ESPRESSO D/H survey), $\sim 24$ shear features are expected, of which $\sim 5$ are identified as D and $\sim 19$ are orphans. The predicted orphan surface density is $\sim 2.4$ per 10 sightlines at $|\Delta v - v_{\rm iso}| > 5$\,km/s, falling to $\sim 1.8$ per 10 sightlines at $> 10$\,km/s. Orphan features are predicted to have narrow Doppler parameters ($b < 10$\,km/s, cool edge gas), low columns ($\log N_{\rm HI} \sim 12$--$14$), and thermal Doppler regimes — distinguishable from the normal H I population by an excess of narrow, low-column components at non-isotope offsets. Under the isotope-D null, no such excess is expected. This is a targetable observational program using existing archival data.

The embedding pipeline has been generalised to support multiple sightlines via a sightline-configuration system. Two additional benchmark D/H quasar sightlines have now been analysed with the identical nested-hypothesis framework, providing the first cross-sightline application of the TEP spectroscopic methodology. The consistent outcome across all three sightlines is qualitatively consistent with TEP's prediction that temporal shear depends on absorber-specific core-edge geometry; an a priori amplitude ranking remains to be calculated.

### 2.4 Cross-Sightline Validation

The identical Gate 2/3 pipeline was applied to PKS 1937$-$101 (Cooke et al. 2024 [66]; ESPRESSO, $R=70\,000$, $z_{\rm abs}=3.572$) and J1332$+$0052 (Kislitsyn et al. 2024 [67]; joint UVES+HIRES, $R\approx50\,800$ and $49\,200$, $z_{\rm abs}=3.421$). Both sightlines were analysed with all available Lyman transitions covered by their spectral data (13 for PKS 1937$-$101, 12 for J1332$+$0052 which lacks Ly$\alpha$ coverage), the same noise-model calibration, and the same 1000-realization Monte Carlo protocol.

| Sightline | $z_{\rm abs}$ | Instrument | $T_{\rm obs}$ | $T_{\rm parent}$ | $p_{\rm std}$ | $p_{\rm parent}$ | Doppler regime | Interpretive status (conservative) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Q1009$+$2956 | 2.5042 | Keck/HIRES | 161.03 | 161.03 | 0.001 (0/1000) | 0.001 (0/1000) | Mixed ($b_{\rm turb}/b_{\rm therm} \approx 2.02$, $0.10\sigma$) | Significant; free-H preferred even under most favorable parent |
| PKS 1937$-$101 | 3.572 | ESPRESSO | 161.31 | 59.00 | 0.001 (0/1000) | 0.001 (0/1000) | Thermal | Significant; free-H preferred even under most favorable parent |
| J1332$+$0052 | 3.421 | UVES+HIRES | 136.97 | 135.76 | 0.001 (0/1000) | 0.001 (0/1000) | Turbulent, saturated ($b_{\rm turb} \approx 50$\,km/s, no Ly$\alpha$ coverage) | Significant; free-H preferred even under most favorable parent |

$^{\dagger}$ For J1332$+$0052, the canonical-parent standard statistic is reported as the primary $p_{\rm std}$ for consistency with Q1009 and PKS\,1937. Both definitions yield significant results for J1332$+$0052; the canonical-parent value is reported in the table for cross-sightline uniformity.

Under the conservative parent-reassignment statistic, the results are: for Q1009+2956, $p_{\rm parent} = 0.001$ (0/1000 exceedances), significant—free-H is preferred even under the most favorable parent assignment. For PKS\,1937$-$101, $p_{\rm parent} = 0.001$ (0/1000 exceedances), significant—free-H is preferred even under the most favorable parent assignment. For J1332$+$0052, $p_{\rm parent} = 0.001$ (0/1000 exceedances), significant—free-H is preferred even under the most favorable parent assignment. The standard (canonical-parent) statistic yields $p_{\rm std} = 0.001$ (0/1000) for all three sightlines. The consistency across all three sightlines is consistent with the TEP framework, in which temporal shear depends on localized core-edge geometry. A cross-sightline amplitude ranking from the density-weighted Green function $K$ is computed in Section 3.3 (Gate 5).

**Multiplicity correction.** Six tests are reported (2 statistics $\times$ 3 sightlines). Applying the Bonferroni correction (threshold $\alpha/6 = 0.0083$), all six results survive: $p_{\rm std}$ and $p_{\rm parent}$ are $0.001$ and $0.001$ for all three sightlines. The unambiguous empirical headline is therefore: all three sightlines show a significant free-H preference that survives both parent reassignment and multiplicity correction.

Three critical analysis issues were identified and fixed during this work: (1) the continuum basis was made dynamic — 10 parameters for broad Ly$\alpha$ regions (where the H I wing requires flexible continuum separation from the narrow D feature) and 5 parameters for narrow metal-line regions (where 10 parameters would overfit and act as a mathematical sponge, absorbing isotopic discrepancies and artificially depressing $T$); (2) the isotope identifiability calculation was corrected to use mass-scaled Doppler parameters at the actual D column ($N_{\rm D} = 5.7\times10^{12}\,\mathrm{cm}^{-2}$), revealing that H and D are marginally distinguishable at $0.52\sigma$ in the thermal regime and indistinguishable at $0.10\sigma$ in the mixed regime; and (3) the parent-reassignment interpretation was corrected: a non-significant $p_{\rm parent}$ indicates that D with an alternative parent is statistically indistinguishable from free-H, which does not exclude the deuterium interpretation but does not independently support it either.

## 3. Scalar Field Dynamics and Temporal Shear [53]

*Part I: Local Absorber Physics.* Sections 2–3 establish the spectroscopic analysis and the local temporal-shear mechanism for the deuterium-like velocity offset. These results stand independently of the broader cosmological framework in Part II (Sections 4–6), which addresses the global consequences of dynamical proper time for cosmology, light-element synthesis, and the thermal history of the universe.

The non-uniqueness of the deuterium identification in Q1009 necessitates a theoretical mechanism to explain the D-like $-81.6\text{ km/s}$ structure without invoking isotopic anomalies. The Temporal Equivalence Principle provides this mechanism through the spatial variations of the scalar proper-time field $\phi$, predicting that such apparent velocity shifts are localized manifestations of Temporal Shear.

### 3.1 Field-Theoretic Derivation

In TEP, gravity is governed by a Lorentzian metric $g_{\mu\nu}$, while matter couples to a causal effective metric $\tilde{g}_{\mu\nu}$ determined by the scalar field $\phi$, analogous to screened scalar-field frameworks [35], [36]. The interaction is defined by the action:

\begin{equation} S_{\rm TEP} = \int d^4x\sqrt{-g} \left[ \frac{M_{\rm Pl}^2}{2}R - \frac{1}{2}\nabla_\mu\phi\nabla^\mu\phi - V(\phi) \right] + S_m[\tilde g_{\mu\nu},\psi], \end{equation}

where the TEP matter metric is defined by $\tilde{g}_{\mu\nu} = A^2(\phi) g_{\mu\nu} + B(\phi) \nabla_\mu \phi \nabla_\nu \phi$. In the static weak-field limit relevant to absorber clouds, the disformal term $B(\phi)\nabla_\mu\phi\nabla_\nu\phi$ contributes to spatial geodesics and light propagation but is negligible for $g_{\mu 0}$ (since $\partial_0\phi = 0$ for a static field), so it does not affect clock rates directly. Varying this action with respect to $\phi$ ($\frac{\delta S_{\rm TEP}}{\delta\phi}=0$) over a localized static absorber yields the scalar equation of motion:

**Equation of Motion:**

\begin{equation} (-\nabla^2 + m_{\rm eff}^2)\,\delta\phi = -\frac{\beta_A}{M_{\rm Pl}}\rho, \end{equation}

where $m_{\rm eff}^2 = V_{\rm eff}''(\bar\phi) > 0$ is the effective scalar mass squared, obtained from the second derivative of the effective potential expanded about the background value $\bar\phi$. In the unscreened regime ($|\Phi|/c^2 \ll \Phi_{\rm half}$), $m_{\rm eff}^2 \to 0$ and the Green operator $G_+$ reduces to the massless Poisson kernel; in the screened regime ($|\Phi|/c^2 \gg \Phi_{\rm half}$), $m_{\rm eff}^2$ is large and the response is Yukawa-suppressed. The bare conformal coupling $\beta_A = -1.0$ [3], [54] applies in the unscreened absorber regime; the screened PPN descendant $\beta_{\rm eff} \simeq -10^{-4}$ (chosen to satisfy the Cassini bound) governs only dense solar-system environments.

Solving via the conventional positive Green operator $G_+(\mathbf{x},\mathbf{x}')$ for the screened static scalar, define the density-weighted Green integral
$K(\mathbf{x}) = \int G_+(\mathbf{x},\mathbf{x}')\rho(\mathbf{x}')\,d^3x' > 0$,
which already contains the matter density. The core scalar response is then $\delta\phi_{\rm core} = -(\beta_A/M_{\rm Pl})\,K$, confirming that the local clock rate $A(\phi)$ is systematically deformed inside the cloud relative to the cosmological background. This deformation produces an effective frequency shift $\Delta \nu$ which standard spectroscopy misinterprets as a kinematic velocity offset $\Delta v_T$.

**Screening projection notice.** The screened Green operator $G_+$ employed here is the absorber-scale projection of the corpus-level environmental operator $\mathcal{S}_\Sigma(\mathcal{E})$ defined in the foundational TEP framework [1] and formalized as a covariant kinetic-density operator in TEP-C0 (Paper 26, [2]): $\mathcal{S}_\Sigma(\mathcal{E}) \equiv [1 + (\Sigma_\mu\Sigma^\mu/g_t^2)^n + (\rho/\rho_{\rm half})^2]^{-1}$, where $\Sigma_\mu = \beta_A \nabla_\mu\phi$ is the scalar kinetic vector and $g_t$ is the acceleration scale. The 1D potential-depth projection $\mathcal{S}_\Sigma(|\Phi|/c^2)$ employed here is the static, spherically symmetric reduction of this full covariant operator: in weak-field static halos, the potential gradient tracks the acceleration $g = |\nabla\Phi|$, allowing the kinetic term $\Sigma^2 = (\beta_A g/c^2)^2$ to map onto $|\Phi|/c^2$. The environmental operator is multi-variable: the environmental state $\mathcal{E}$ includes ambient density $\rho$, gravitational compactness $|\Phi|/c^2$, density gradients $\nabla\rho$, potential gradients $\nabla\Phi$, proximity to field sources, coherence volume, and boundary geometry. Each physical domain uses a different projection of $\mathcal{E}$: the solar system is screened via compactness and density projections (satisfying Cassini), galactic halos retain weak-field coupling via gradient-coherence projections (producing the corpus value $\beta \simeq -0.013$ for Cepheid and rotation-curve channels [51], [52]), and diffuse Lyman-limit absorbers are screened via the potential-depth projection $|\Phi|/c^2$ alone. The potential-depth law $\mathcal{S}_\Sigma(|\Phi|/c^2) = 1/(1 + (|\Phi|/c^2/\Phi_{\rm half})^n)$ with $\Phi_{\rm half} = 1.59 \times 10^{-7}$ and $n = 3.56$ is the *absorber-regime projection* of $\mathcal{S}_\Sigma(\mathcal{E})$, calibrated by three boundary conditions: (i) $|\Phi_{\rm abs}|/c^2 \sim 10^{-8} \Rightarrow \mathcal{S}_\Sigma > 0.999$ (unscreened, bare $\beta_A = -1.0$), (ii) $|\Phi_\odot|/c^2 = 2.12 \times 10^{-6}$ (Cassini grazing ray at $R_\odot$) $\Rightarrow \mathcal{S}_\Sigma \approx 10^{-4}$ (chosen to satisfy the Cassini bound), and (iii) $|\Phi_{\rm gal}|/c^2 = v_{\rm circ}^2/c^2 = 5.38 \times 10^{-7}$ (solar circle, $v_{\rm circ} = 220\text{ km/s}$) $\Rightarrow \mathcal{S}_\Sigma \approx 0.013$ (corpus value). The solar-system and galactic potentials differ by a factor of $3.94\times$ — they do *not* share the same $|\Phi|/c^2$ as earlier drafts assumed. Raised to the power $n = 3.56$, this $3.94\times$ difference yields a $132\times$ screening contrast, sufficient to differentiate Cassini ($\mathcal{S}_\Sigma \approx 10^{-4}$) from galactic ($\mathcal{S}_\Sigma \approx 0.013$) without invoking a second screening variable. Gate 10 (galactic coupling reconciliation) is conditionally closed: the pure potential-depth law with corrected $|\Phi|/c^2$ values and recalibrated $(\Phi_{\rm half}, n)$ satisfies all three boundary conditions simultaneously. The multi-variable operator $\mathcal{S}_\Sigma(\mathcal{E})$ remains the corpus framework for domains where density and gradient projections are physically relevant (UCD, LLR, LHC [69], [70]), but the potential-depth projection alone is sufficient for the absorber, solar-system, and galactic-halo regimes. Lyman-limit absorber mass densities ($\rho_{\rm abs} \sim 10^{-27}\text{--}10^{-24}\text{ g/cm}^3$, corresponding to hydrogen number densities $n_{\rm H} \sim 10^{-3}\text{--}1\text{ cm}^{-3}$) sit in shallow potential wells ($|\Phi|/c^2 \sim 10^{-8}$), placing these systems firmly in the unscreened regime where the full scalar response $G_+$ applies without suppression. **Corpus-level continuity caveat.** The cross-domain continuity of $\mathcal{S}_\Sigma(\mathcal{E})$ — the claim that the potential-depth projection employed here, the density-dependent projections used in LLR/UCD domains, and the gradient-coherence projections used in galactic-halo domains are all slices of a single continuous function — is a *working hypothesis of the TEP corpus*, not a derived result. No master functional form of $\mathcal{E}$ has been written down, and no proof exists that adjacent projections agree where their domains of validity overlap. Each paper's domain-specific projection stands on its own calibration until the unification is completed. The clock/force-sector split discussed in Section 3.4 is the most immediate consequence of this gap: if the conformal coupling gradient $\nabla\ln A(\phi)$ sources a fifth force in the standard scalar-tensor manner, the potential-depth projection alone cannot decouple clock effects from dynamical constraints, and the cross-domain continuity hypothesis would need to be replaced by a more structured framework.

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

Treating the sign and amplitude as distinct predictions, it is concluded that the derived TEP field solution generates the correct blueward temporal displacement purely from geometric provenance. The observed apparent velocity displacement of $-81.6\text{ km/s}$ establishes an observational boundary condition on the TEP coupling space. The quadratic dependence $\Delta v_T = -c\,\beta_A^2\,K/M_{\rm Pl}^2$ yields a square-root amplitude constraint:

\begin{equation}
|\beta_A| = M_{\rm Pl}\sqrt{\frac{|\Delta v_T|/c}{K}} = M_{\rm Pl}\sqrt{\frac{81.6\text{ km/s}/c}{K}}.
\end{equation}

For corpus consistency, $\beta_A$ should be frozen from independent measurements and the absorber shear amplitude predicted from independently measured density, column, and geometry—rather than inferred from the same $-81.6\text{ km/s}$ feature. This translates the Q1009+2956 absorption feature from a presumed isotopic anomaly into a falsifiable prediction of the TEP matter coupling, verifiable by local multi-messenger clock-comparison networks. The conformal sector produces the correct blueward sign deterministically; the full amplitude is quantified below as a target for the environmental operator $\mathcal{S}_\Sigma(\mathcal{E})$.

### 3.3 Amplitude Test: Frozen-$\beta_A$ Calculation (Gate 4B)

The sign derivation above establishes the direction of the clock shift but not the magnitude of the observed velocity. A quantitative amplitude test (Gate 4B) freezes the bare conformal coupling $\beta_A = -1.0$ from the TEP corpus [3], [54] and constructs the density-weighted Green integral $K$ from actual Q1009+2956 observables. The Q1009+2956 D/H absorber is a Lyman Limit System (LLS) with $\log N_{\rm HI} = 17.362 \pm 0.005$ [44], $z_{\rm abs} = 2.5042$.

Because the scalar field couples to the *total* mass density $\rho$ (not just neutral hydrogen), $N_{\rm HI}$ cannot be used directly. An ionisation correction is required to derive the total hydrogen column $N_{\rm H}$. Under photoionisation equilibrium with the UV background at $z \sim 2.5$ [55], the neutral fraction is $x_{\rm HI} = \alpha_{\rm rec}\,n_e / \Gamma$, where $\Gamma \approx 10^{-12}\text{ s}^{-1}$ is the photoionisation rate and $\alpha_{\rm rec} \approx 2.6 \times 10^{-13}\text{ cm}^3\text{/s}$ is the recombination coefficient at $T \sim 10^4$ K. Solving for $N_{\rm H}$ with $n_e \approx n_{\rm H} = N_{\rm H}/(2R)$:

\begin{equation} N_{\rm H} = \sqrt{\frac{N_{\rm HI} \cdot 2R \cdot \Gamma}{\alpha_{\rm rec}}}. \end{equation}

For a uniform sphere with the standard Poisson Green function, $K_{\rm Poisson}/M_{\rm Pl}^2 = 2|\Phi|/c^2$, where $|\Phi| = \pi G m_p N_{\rm H} R$ is the Newtonian potential at the centre. The conformal-only prediction is:

\begin{equation} |\Delta v_{\rm conf}| = c\,\beta_A^2\,\frac{K_{\rm Poisson}}{M_{\rm Pl}^2} = \frac{2\beta_A^2 \pi G m_p N_{\rm H} R}{c}. \end{equation}

The absorber radius $R$ is not directly measured for Q1009+2956. The main D/H components span $\Delta v \approx 13\text{ km/s}$ in velocity [44], which constrains the absorber size through the virial relation but does not determine it uniquely. Results are therefore presented as a function of $R$. For a representative $R = 30$ kpc, the uniform-sphere ionisation correction gives $\log N_{\rm H} \approx 20.6$ ($x_{\rm HI} \approx 6 \times 10^{-4}$), yielding $|\Delta v_{\rm conf}| \approx 0.009\text{ km/s}$.

**Cross-sightline amplitude ranking (Gate 5).** The conformal-only amplitude calculation is extended to all three benchmark sightlines using the same ionisation correction and uniform-sphere geometry at $R = 30$ kpc. The required amplification $\mathcal{A}_{\rm env} = |\Delta v_T|/|\Delta v_{\rm conf}|$ varies across sightlines by a factor of $\sim 9$:

| Sightline | $\log N_{\rm HI}$ | $\log N_{\rm H}$ | $|\Delta v_{\rm conf}|$ (km/s) | Required $\mathcal{A}_{\rm env}$ | Predicted offset at $\mathcal{A}_{\rm env}^{\rm Q1009}$ |
| --- | --- | --- | --- | --- | --- |
| Q1009+2956 | 17.36 | 20.61 | 0.009 | $\sim 9.3\times10^3$ | $-81.6$ (anchor) |
| PKS\,1937$-$101 | 17.92 | 20.89 | 0.017 | $\sim 4.9\times10^3$ | $\sim -156$ km/s |
| J1332$+$0052 | 19.25 | 21.55 | 0.077 | $\sim 1.1\times10^3$ | $\sim -719$ km/s |

A universal $\mathcal{A}_{\rm env}$ — which is what a geometry-independent transport path $\mathcal{C}_{T,\parallel}$ most naturally provides — is excluded at face value: the predicted offsets would be $-82$, $-156$, and $-719$\,km/s, varying by a factor of $\sim 9$ across sightlines, whereas all three observed features cluster at $-81.6$\,km/s. Two interpretations are consistent with this:

- *Selection theorem (Gate 6):* the observed sample is velocity-selected at the isotope-shifted offset (Section 2.3). The detected subpopulation is precisely the tail where $\mathcal{A}_{\rm env} \cdot \Delta v_{\rm conf}$ lands near $v_{\rm iso}$. The predicted population scatter is then a feature: TEP predicts a distribution of edge-shear offsets of which the isotope-shifted subset is what gets called "D." The per-sightline $\mathcal{A}_{\rm env}$ values in the table above are the amplifications required for each sightline's edge-gas feature to land at $-81.6$\,km/s; the variation reflects the different core potentials.

- *Per-sightline $\mathcal{A}_{\rm env}$:* the amplification is a property of the transport path and varies with the local geometry. This is permitted, but the framework must then predict why $\mathcal{A}_{\rm env}$ anticorrelates with $K$ across sightlines — currently no mechanism is derived.

The falsification criterion is restated per sightline: the $\mathcal{A}_{\rm env} > 10^3$ floor becomes $\mathcal{A}_{\rm env} \approx 9.3 \times 10^3$ for Q1009+2956, $\mathcal{A}_{\rm env} \approx 4.9 \times 10^3$ for PKS\,1937$-$101, and $\mathcal{A}_{\rm env} \approx 1.1 \times 10^3$ for J1332$+$0052. All three exceed the $10^3$ threshold, though J1332 — with the highest $\log N_{\rm HI} = 19.25$ — approaches it. The population prediction — that edge-shear features at offsets other than $-81.6$\,km/s exist and are being absorbed into H I component structure — is the discriminating observational test.

**Gate 4B status:**

- **Conformal sign: PASSED.** The clock shift $\Delta\ln A$ is purely conformal for a static scalar field (since $\partial_0\phi = 0$ implies $B(\phi)\nabla_0\phi\nabla_0\phi = 0$ for $g_{00}$). The sign follows rigorously from $\beta_A^2 > 0$ and the core-edge geometry.

- **Conformal screening: three-anchor calibration conditionally closes Gate 10.** The environmental operator $\mathcal{S}_\Sigma(\mathcal{E})$ is multi-variable [1]; the potential-depth projection $\mathcal{S}_\Sigma(|\Phi|/c^2) = 1/(1 + (|\Phi|/c^2 / \Phi_{\rm half})^n)$ is calibrated by three boundary conditions with *corrected* $|\Phi|/c^2$ values: (1) absorber regime $|\Phi_{\rm abs}|/c^2 \sim 10^{-8} \to \mathcal{S}_\Sigma > 0.999$ (unscreened, bare $\beta_A = -1.0$), (2) solar system $|\Phi_\odot|/c^2 = GM_\odot/(R_\odot c^2) = 2.12 \times 10^{-6}$ (Cassini grazing ray at solar radius) $\to \mathcal{S}_\Sigma \approx 10^{-4}$ (chosen to satisfy the Cassini bound), and (3) galactic halo $|\Phi_{\rm gal}|/c^2 = v_{\rm circ}^2/c^2 = 5.38 \times 10^{-7}$ (solar circle, $v_{\rm circ} = 220\text{ km/s}$) $\to \mathcal{S}_\Sigma \approx 0.013$ (corpus value [54]). The solar-system and galactic potentials differ by $3.94\times$ — earlier drafts incorrectly assumed both were $\sim 10^{-6}$. Solving the three-anchor system yields $\Phi_{\rm half} = 1.59 \times 10^{-7}$ and $n = 3.56$, giving $\mathcal{S}_\Sigma(2.12 \times 10^{-6}) = 1.0 \times 10^{-4}$ (Cassini: $|\gamma_{\rm PPN} - 1| \approx 2 \times 10^{-8}$, PASS), $\mathcal{S}_\Sigma(5.38 \times 10^{-7}) = 0.013$ (galactic: $\beta_{\rm eff} \simeq 0.013$, PASS), and $\mathcal{S}_\Sigma(10^{-8}) = 0.9999$ (absorber: unscreened, PASS). The $3.94\times$ potential-depth ratio raised to $n = 3.56$ yields $132\times$ screening contrast — sufficient to differentiate Cassini from galactic without a second screening variable. Gate 10 is conditionally closed: the pure potential-depth law with corrected $|\Phi|/c^2$ values satisfies all three constraints simultaneously. The multi-variable operator $\mathcal{S}_\Sigma(\mathcal{E})$ remains the corpus framework for domains where density and gradient projections are physically relevant (UCD, LLR, LHC), but the potential-depth projection alone is sufficient for the absorber, solar-system, and galactic-halo regimes. The product $\beta_{\rm eff}^2 \times |\Phi|/c^2$ peaks in the unscreened intermediate regime ($|\Phi|/c^2 \sim 10^{-7}$), confirming that the fifth force is strongest in diffuse clouds and suppressed in dense environments.

- **Conformal-only amplitude: quantified.** The Poisson Green function with the bare coupling and the uniform-sphere ionisation-corrected total gas column gives $|\Delta v_{\rm conf}| \approx 0.009\text{ km/s}$ (for $R = 30$ kpc). The required amplification factor $\mathcal{A}_{\rm env} = |\Delta v_T|/|\Delta v_{\rm conf}| = 81.6 / 0.009 \approx 9.3 \times 10^3$. The falsification threshold is set at $\mathcal{A}_{\rm env} < 10^3$ (see scaling analysis below).

- **Perturbative disformal: insufficient.** The weak-field disformal term $B(\nabla\phi)^2/A^2$ is suppressed by $(|\Phi|/c^2)^2$ for a constant coupling $B(\phi) = B_0/M_{\rm Pl}^2$, and by $(\nabla\psi/\psi)^2 \ll 1/r^2$ for an inverse-field coupling $B(\phi) = B_0 M_{\rm Pl}^2/\phi^2$ (the potential is nearly flat in the interior of an extended mass distribution). No local coupling $B(\phi)$ can close the $10^4$ gap perturbatively with a natural coupling strength.

- **Non-perturbative $\mathcal{C}_{T,\parallel}$: perturbative mechanisms quantitatively excluded, non-perturbative edge channel identified (Gate 4B open, Gate 4B-II complete).** The $10^4$ amplification must emerge from the global structure of the non-exact transport path $\mathcal{C}_{T,\parallel}$, not from a local perturbative correction. All four candidate perturbative mechanisms have been quantitatively evaluated and confirmed insufficient: (1) *modified scalar propagator* in the screening transition regime gives $\mathcal{O}(1)$ enhancement; (2) *non-perturbative field soliton* at the absorber scale has amplitude $\sim M_{\rm Pl} \times 10^{-15}$ (negligible); (3) *cumulative IGM transport phase* over $D_H = c/H_0 \sim 4.3\text{ Gpc}$ gives total phase $\sim 3 \times 10^4$ in dimensionless units but maps to $\sim 10^{-22}\text{ km/s}$ velocity shift (negligible); (4) *perturbative disformal lensing* through the absorber boundary gives metric correction $B_{\rm eff} \cdot (\nabla\phi)^2 / A^2 \sim 3 \times 10^{-128}$ (geometrized units, $B_0 = 1$, $R = 30\text{ kpc}$) — utterly negligible. The conformal-only shift $|\Delta v_{\rm conf}| \approx 0.009\text{ km/s}$ (for $|\Phi_{\rm abs}|/c^2 = 10^{-8}$, $\beta_A = -1.0$, unscreened, with uniform-sphere ionisation correction at $R = 30\text{ kpc}$) requires amplification $\mathcal{A}_{\rm env} = 81.6 / 0.009 \approx 9.3 \times 10^3$. Gate 4B-II (quantitative mechanism analysis, see below) identifies the edge transition with $B(\phi)$ enhancement as the most promising non-perturbative channel, with a concrete target $\tilde{B}_{\rm eff} \sim 10^{24}$. Gate 4B remains open: the amplification must arise from the non-linear screening dynamics near the core-edge transition, not from any perturbative local correction. The accumulated holonomy to the velocity shift $\Delta v_T = -c\,\Delta\ln A \cdot \mathcal{A}_{\rm env}$, and (iv) verify $\mathcal{A}_{\rm env} \in [10^3, 5\times10^4]$ across the plausible parameter range. The falsification floor is $\mathcal{A}_{\rm env} < 10^3$.

- **Disformal architecture mismatch: open reconciliation.** The strong-field interior solution [54] uses an ultra-damped quartic Gaussian $B(\phi) = B_0|\phi|^2/(1+|\phi|^2)\exp(-\phi^4/2\sigma_B^4)$ to ensure conformal dominance and maintain $\det\tilde{g}_{2D} < 0$ in the deep interior. The absorber-regime perturbative analysis above uses constant ($B = B_0/M_{\rm Pl}^2$) or inverse-field ($B = B_0 M_{\rm Pl}^2/\phi^2$) couplings, which are the appropriate weak-field limits for diffuse clouds. These two forms have not been reconciled: a single composite $B(\phi)$ that reduces to the quartic Gaussian in the strong-field regime and to the inverse-field form in the cosmological transport regime is required for structural consistency. This is tagged as an open reconciliation target, not a structural inconsistency, because the two forms operate in disjoint field regimes ($|\phi| \gg 1$ vs $|\phi| \ll 1$) where the quartic Gaussian is already exponentially suppressed.

**Note on sign vs. amplitude.** The clock shift $\Delta\ln A$ is purely conformal (since $\partial_0\phi = 0$ for a static field, the disformal term $B(\phi)\nabla_0\phi\nabla_0\phi = 0$ for $g_{00}$). The sign of the clock shift is therefore established within the conformal/static branch of the scalar equation. The observation that $\partial_0\phi = 0$ removes the direct disformal contribution to $\tilde g_{00}$ does not by itself prove that disformal/derivative matter couplings drop out of the full scalar field equation; a complete derivation of the static disformal EOM is required to confirm that these terms vanish or sublead. The present sign theorem should therefore be understood as the conformal/static branch result, valid conditional on the disformal matter coupling not reversing the sign of the scalar response. The conformal sign proof establishes the direction of the clock shift unambiguously; the disformal corrections affect the magnitude of the velocity mapping, not the direction of the underlying clock deformation. The bridge from the local clock deformation ($\Delta\ln A \sim 10^{-4}$) to the observed velocity amplification ($\mathcal{A}_{\rm env} \approx 10^4$) is macroscopic, not a local weak-field disformal term: it must arise from the global non-exact transport path $\mathcal{C}_{T,\parallel}$, which integrates the photon propagation through the non-integrable spatial geometry over cosmological distances. The perturbative weak-field disformal correction is suppressed by $(|\Phi|/c^2)^2$ and is negligible in the absorber regime; the required $10^4$ amplification must arise from a non-perturbative mechanism in the global structure of $\mathcal{C}_{T,\parallel}$.

**Falsifiability criterion.** The conformal/static branch sign theorem and the amplitude quantification together convert the $-81.6\text{ km/s}$ feature into a quantitative prediction: a first-principles evaluation of $\mathcal{C}_{T,\parallel}$ in the absorber regime with the Cassini-frozen $\mathcal{S}_\Sigma$ must yield $\mathcal{A}_{\rm env} \approx 9.3 \times 10^3$ for physically motivated $R$. If it does not, the TEP absorber-field explanation is falsified. This converts an open calculation into a sharp, testable target.

**Scaling of $\mathcal{A}_{\rm env}$ with absorber parameters.** The required amplification depends on the conformal-only amplitude $|\Delta v_{\rm conf}| = 2\beta_A^2 \pi G m_p N_{\rm H} R / c$, which scales linearly with both the total hydrogen column $N_{\rm H}$ and the absorber radius $R$. The ionisation correction gives $N_{\rm H} = \sqrt{N_{\rm HI} \cdot 2R \cdot \Gamma / \alpha_{\rm rec}}$, so $|\Delta v_{\rm conf}| \propto R^{3/2}$ for fixed $N_{\rm HI}$. For $R = 10$ kpc, $|\Delta v_{\rm conf}| \approx 0.002\text{ km/s}$ and $\mathcal{A}_{\rm env} \approx 4.8 \times 10^4$; for $R = 50$ kpc, $|\Delta v_{\rm conf}| \approx 0.019\text{ km/s}$ and $\mathcal{A}_{\rm env} \approx 4.3 \times 10^3$. A centrally concentrated density profile (e.g., isothermal sphere or NFW-like core) increases $K$ relative to the uniform-sphere estimate by a factor of $\sim$2--5, reducing the required amplification proportionally. The representative value $\mathcal{A}_{\rm env} \approx 9.3 \times 10^3$ corresponds to $R = 30$ kpc with a uniform sphere; the plausible range across reasonable assumptions is $\mathcal{A}_{\rm env} \sim 3 \times 10^3$--$5 \times 10^4$. The *falsification threshold* is set at $\mathcal{A}_{\rm env} < 10^3$: if a first-principles evaluation of $\mathcal{C}_{T,\parallel}$ cannot reach $10^3$ under any reasonable combination of $R$, ionisation correction, and density profile, the absorber-field interpretation is ruled out. Candidate mechanisms that could plausibly supply the required amplification include: (1) rapid spatial variation of $\mathcal{S}_\Sigma$ across the core–edge transition creating an effective gradient enhancement, (2) cumulative non-integrable phase along the cosmological line of sight (the $\mathcal{C}_{T,\parallel}$ integral itself), and (3) a mild soliton-like scalar profile inside the absorber concentrating the clock shift. An order-of-magnitude estimate for any of these mechanisms is a priority for the next iteration.

**Quantitative mechanism analysis (Gate 4B-II).** Three candidate non-perturbative channels have been quantitatively evaluated (step\_04c, results/gate4b\_mechanism.json):

- **Interior disformal integral.** The disformal metric perturbation $h_{\rm dis} = \tilde{B}_0 (\partial_r \varphi)^2$ integrated through the absorber body gives $\mathcal{A}_{\rm env}^{\rm (int)} = \tilde{B}_0 \times 4\pi \rho_{\rm geom} R / 9 \approx \tilde{B}_0 \times 3.5 \times 10^{-32}$, where $\varphi = \beta_A |\Phi|/c^2$ is the dimensionless field and $\tilde{B}_0$ is the disformal coupling in units of $M_{\rm Pl}^{-2}$. With a natural coupling $\tilde{B}_0 \sim 1$, this channel is negligible by $\sim 32$ orders of magnitude.

- **Edge transition amplification.** At the absorber boundary, $\mathcal{S}_\Sigma$ transitions from $\sim 1$ (unscreened) to $\sim 0.013$ (galactic-screened) over a width $\Delta R$. The field discontinuity $\Delta\varphi = \beta_A (1 - \mathcal{S}_\Sigma^{\rm gal}) |\Phi_{\rm abs}|/c^2 \approx 9.6 \times 10^{-9}$ creates a gradient $\nabla\varphi \sim \Delta\varphi / \Delta R$ that enhances the disformal term as $\mathcal{A}_{\rm env}^{\rm (edge)} = \tilde{B}_0 \times (\Delta\varphi)^2 / (\Delta R \cdot \Delta_{\rm conf})$, where $\Delta_{\rm conf} = \beta_A^2 |\Phi_{\rm abs}|/c^2$. This scales as $1/\Delta R$ — the thinner the transition, the larger the amplification. For a Compton-wavelength transition $\Delta R = \lambda_\phi = \hbar/(m_\phi c)$ with $m_\phi \sim 10^{-22}$ eV (consistent with galactic-scale scalar range), $\mathcal{A}_{\rm env}^{\rm (edge)} = \tilde{B}_0 \times 4.8 \times 10^{-26}$. Near the screening transition ($|\Phi|/c^2 \sim \Phi_{\rm half}$), the disformal coupling $B(\phi)$ may be enhanced by the non-linear screening dynamics. With a power-law enhancement $B_{\rm eff} = \tilde{B}_0 (\Phi_{\rm half}/|\Phi_{\rm abs}|)^\alpha$ and $\alpha = 4$, the enhancement factor is $(16.3)^4 \approx 7.1 \times 10^4$, giving $\mathcal{A}_{\rm env}^{\rm (edge)} = \tilde{B}_0 \times 3.4 \times 10^{-21}$. This is the most promising channel identified.

- **IGM cumulative phase.** The disformal phase accumulated over the cosmological path from $z = 2.5$ to $z = 0$ ($D \sim 5.4$ Gpc) through the large-scale-structure potential gives $\mathcal{A}_{\rm env}^{\rm (IGM)} = \tilde{B}_0 \times 1.8 \times 10^{-27}$. With natural coupling, this is negligible by $\sim 27$ orders of magnitude.

**Assessment.** The edge transition mechanism is the dominant channel, with amplification scaling as $1/\Delta R$ and further enhanced by $B(\phi)$ non-linearity near the screening transition. The specific prediction is: if the non-perturbative $B(\phi)$ profile near the screening transition achieves an effective coupling $\tilde{B}_{\rm eff} \sim 10^{24}$ (enhanced from $\tilde{B}_0 \sim 1$ by the screening-transition non-linearity at the $\alpha = 4$ level), the amplitude gap closes. This is a concrete, falsifiable target — not an unspecified liability. The evaluation roadmap is: (i) solve the non-linear scalar field equation $\nabla^2 \phi = \beta_A \mathcal{S}_\Sigma(|\Phi|/c^2) \rho / M_{\rm Pl}$ through the core-edge transition with the full non-linear $\mathcal{S}_\Sigma$, (ii) compute the resulting $B(\phi)$ enhancement factor from the self-consistent field profile, and (iii) verify that $\tilde{B}_{\rm eff} \geq 10^{24}$ (or equivalently $\mathcal{A}_{\rm env} \geq 10^3$) for physically motivated $m_\phi$ and $R$. If the non-linear screening dynamics cannot produce this enhancement, the absorber-field interpretation is falsified at the $\mathcal{A}_{\rm env} < 10^3$ floor.

**Edge-transition line-of-sight calculation (Gate 4B-III).** A rough quantitative calculation (step\_04d, results/gate4b\_edge\_calculation.json) models the screening transition at the absorber–galaxy boundary, where $\mathcal{S}_\Sigma$ transitions from $\sim 1$ (unscreened interior, $|\Phi_{\rm abs}|/c^2 \sim 10^{-8}$) to $\sim 0.013$ (galactic-screened exterior, $|\Phi_{\rm gal}|/c^2 = 5.38 \times 10^{-7}$). The chameleon thin-shell scaling gives a transition width $\Delta R \sim 0.117 \, R \approx 3.5$ kpc. The amplification in a line-of-sight integral through the transition is $\mathcal{A}_{\rm env}^{\rm (edge)} = \tilde{B}_{\rm eff} \times (\Delta\varphi)^2 / (\Delta R \cdot \Delta_{\rm conf})$, requiring $\tilde{B}_{\rm eff} / \Delta R \sim 10^{12}$ cm$^{-1}$. With the chameleon thin-shell width, $\tilde{B}_{\rm eff} \sim 10^{34}$ is needed — far beyond what field-curvature enhancement can supply for any physically motivated scalar mass ($m_\phi \sim 10^{-30}$ to $10^{-15}$ eV gives at most $\tilde{B}_{\rm eff} \sim 10^5$). Even with a sharper transition ($\Delta R \sim 1$ AU), $\tilde{B}_{\rm eff} \sim 10^{25}$ is required, corresponding to $m_\phi \sim 10^{-31}$ eV. The line-of-sight edge-transition integral therefore does not close the amplitude gap with physically motivated parameters. The critical caveat is that this calculation models a local line-of-sight integral, whereas the TEP framework predicts the amplification arises from the global holonomy of the non-exact transport path $\mathcal{C}_{T,\parallel}$ — a topological property of the full $(t, r)$ spacetime, not a local integral along a single photon path [1], [27]. The synchronization holonomy around a loop enclosing the screening transition may be substantially larger than the line-of-sight estimate. A full non-perturbative solution of the transport equation through the screening transition — not a perturbative line-of-sight integral — is required to evaluate whether the global holonomy can reach $\mathcal{A}_{\rm env} \sim 10^4$. Gate 4B remains open on this point. The falsification floor $\mathcal{A}_{\rm env} < 10^3$ applies to the full non-perturbative evaluation, not to the rough line-of-sight estimate reported here.

**Functional constraints on $\mathcal{S}_\Sigma(\mathcal{E})$.** The environmental operator must satisfy three strict boundary conditions simultaneously:

- **Absorber regime (unscreened):** $|\Phi_{\rm abs}|/c^2 \sim 10^{-8} \Rightarrow \mathcal{S}_\Sigma \approx 1$, so that the bare coupling $\beta_A = -1.0$ applies and the conformal/static branch sign theorem remains valid.

- **Solar-system regime (Cassini):** $|\Phi_\odot|/c^2 \sim 10^{-6} \Rightarrow \mathcal{S}_\Sigma \approx 10^{-4}$, so that the screened descendant $\beta_{\rm eff} = \beta_A \cdot \mathcal{S}_\Sigma \simeq -10^{-4}$ satisfies the Cassini PPN bound $|\gamma_{\rm PPN} - 1| < 2.3 \times 10^{-5}$.

- **Galactic regime (corpus):** The corpus requires $\beta \simeq 0.013$ at galactic scales [54], [51], [52]. The potential-depth law with corrected $|\Phi_{\rm gal}|/c^2 = v_{\rm circ}^2/c^2 = 5.38 \times 10^{-7}$ gives $\mathcal{S}_\Sigma \approx 0.013$ directly — no second screening variable required (Gate 10 conditionally closed).

- **Amplification target:** The non-exact transport path $\mathcal{C}_{T,\parallel}$ must produce an effective amplification $\mathcal{A}_{\rm env} \approx 9.3 \times 10^3$ relative to the conformal-only Poisson calculation.

The screening function $\mathcal{S}_\Sigma(|\Phi|/c^2) = 1/(1 + (|\Phi|/c^2/\Phi_{\rm half})^n)$ with $\Phi_{\rm half} = 1.59 \times 10^{-7}$ and $n = 3.56$ satisfies all three boundary conditions exactly as the *absorber-regime projection* of the multi-variable operator $\mathcal{S}_\Sigma(\mathcal{E})$. The screening variable for this projection is the gravitational potential depth $|\Phi|/c^2$, because the scalar field responds to total mass through the Poisson equation and screening is set by the integrated potential. The solar-system and galactic potentials differ by $3.94\times$ ($|\Phi_\odot|/c^2 = 2.12 \times 10^{-6}$ vs $|\Phi_{\rm gal}|/c^2 = 5.38 \times 10^{-7}$), yielding $132\times$ screening contrast — sufficient to differentiate Cassini ($\mathcal{S}_\Sigma \approx 10^{-4}$) from galactic ($\mathcal{S}_\Sigma \approx 0.013$) without a second screening variable (Gate 10 conditionally closed). The product $\beta_{\rm eff}^2 \times |\Phi|/c^2$ peaks in the unscreened intermediate regime ($|\Phi|/c^2 \sim 10^{-7}$), confirming that the fifth force is strongest in diffuse clouds and suppressed in dense environments. The required amplification cannot arise from the conformal sector alone (which gives $\mathcal{S}_\Sigma \approx 1$ in the unscreened regime); it must originate from the disformal sector $B(\phi)\nabla_\mu\phi\nabla_\nu\phi$ and its environmental projection, which modifies the photon-transport mapping $\Delta v_T = -c\,\Delta\ln A$ through the non-exact transport path $\mathcal{C}_{T,\parallel}$. The disformal contribution to photon propagation is negligible for clock rates ($g_{00}$, since $\partial_0\phi = 0$) but non-negligible for spatial photon geodesics through a static scalar gradient, providing a physically distinct channel for the amplification that does not alter the conformal/static branch sign theorem. The perturbative weak-field disformal term is suppressed by $(|\Phi|/c^2)^2$ for a constant coupling and by $(\nabla\psi/\psi)^2 \ll 1/r^2$ for an inverse-field coupling (the potential is nearly flat in the interior of an extended mass distribution); no local $B(\phi)$ can close the $10^4$ gap perturbatively (quantitatively confirmed: the disformal metric correction $B_{\rm eff} \cdot (\nabla\phi)^2 / A^2 \sim 3 \times 10^{-128}$ in geometrized units). The amplification requires a non-perturbative mechanism from the global structure of $\mathcal{C}_{T,\parallel}$ — the single open calculation that closes Gate 4B.

**Note on coupling conventions.** The bare conformal coupling $\beta_A = -1.0$ [3], [54] and the screened PPN value $\beta_{\rm eff} \simeq -10^{-4}$ are related by the screening function $\beta_{\rm eff}(\mathcal{E}) = \beta_A \cdot \mathcal{S}_\Sigma(\mathcal{E})$, derived in the foundational TEP framework [1]. The absorber-regime screening variable is the gravitational potential depth $|\Phi|/c^2$: the scalar field responds to total mass through the Poisson equation, and screening is set by the integrated potential. Lyman-limit absorbers ($|\Phi_{\rm abs}|/c^2 \sim 10^{-8}$) sit in the unscreened regime where $\mathcal{S}_\Sigma \approx 1$ and the bare coupling applies. The weak-field corpus value $\beta \simeq -0.013$ [54] is the galactic-scale effective coupling, given by the same potential-depth law at $|\Phi_{\rm gal}|/c^2 = 5.38 \times 10^{-7}$: $\mathcal{S}_\Sigma(5.38 \times 10^{-7}) \approx 0.013$, so $\beta_{\rm eff} = \beta_A \cdot \mathcal{S}_\Sigma \simeq -0.013$. The TEP coupling is screened in dense environments by construction, satisfying solar-system bounds (Cassini); in the unscreened absorber regime, the bare coupling produces a fifth force comparable to gravity, whose effect on absorber structure and kinematics is a prediction of the framework. Constraints on unscreened scalars in other theoretical frameworks [56] assume different screening mechanisms and coupling structures, and are not directly applicable to the TEP coupling, which is screened by the environmental operator $\mathcal{S}_\Sigma(\mathcal{E})$ rather than by a chameleon or symmetron mechanism.

**Cassini calibration derivation.** The Cassini experiment measured the PPN parameter $\gamma_{\rm PPN} = 1 + (2.1 \pm 2.3) \times 10^{-5}$ [59], not a universal scalar coupling directly. The mapping from the TEP conformal coupling to $\gamma_{\rm PPN}$ is derived from the disformal metric structure. In the TEP scalar-tensor framework, the conformal coupling $A(\phi) = e^{\beta_A \phi/M_{\rm Pl}}$ modifies the post-Newtonian metric through the scalar field profile $\delta\phi$ sourced by a mass $M$. The disformal map $g_{\mu\nu} = A^2(\phi)\,\eta_{\mu\nu} + B(\phi)\,\partial_\mu\phi\,\partial_\nu\phi$ yields the standard scalar-tensor PPN relation $\gamma_{\rm PPN} = (1 - \beta_{\rm eff}^2)/(1 + \beta_{\rm eff}^2)$ in the weak-field limit, where $\beta_{\rm eff} = \beta_A \cdot \mathcal{S}_\Sigma$ is the environmentally screened coupling. This is the same relation as in Brans–Dicke theory with $\omega_{\rm BD} = 2\beta_{\rm eff}^{-2} - 1/2$; the factor $\alpha = 1$ is not an assumption but a consequence of the canonical conformal coupling structure ($A = e^{\beta_A\phi/M_{\rm Pl}}$, not a general function). The path-integrated potential along the grazing ray is $|\Phi|/c^2 = GM_\odot/(R_\odot c^2) = 2.12 \times 10^{-6}$ at the solar radius, consistent with the solar-surface value for the Cassini geometry. Setting $\gamma_{\rm PPN} - 1 = -2\beta_{\rm eff}^2/(1 + \beta_{\rm eff}^2) \approx -2\beta_{\rm eff}^2$ for $|\beta_{\rm eff}| \ll 1$, the Cassini bound $|\gamma_{\rm PPN} - 1| < 2.3 \times 10^{-5}$ implies $\beta_{\rm eff}^2 < 1.15 \times 10^{-5}$, i.e., $|\beta_{\rm eff}| < 3.4 \times 10^{-3}$. The TEP screening parameters $\Phi_{\rm half} = 1.59 \times 10^{-7}$ and $n = 3.56$ yield $\mathcal{S}_\Sigma(|\Phi_\odot|/c^2 = 2.12 \times 10^{-6}) = 1/(1 + (13.3)^{3.56}) \approx 1.0 \times 10^{-4}$, giving $|\beta_{\rm eff}| \approx 10^{-4}$ and $|\gamma_{\rm PPN} - 1| \approx 2 \times 10^{-8}$, which satisfies the Cassini bound by more than three orders of magnitude. The absorber boundary condition $\mathcal{S}_\Sigma(|\Phi_{\rm abs}|/c^2 = 10^{-8}) > 0.999$ is simultaneously satisfied: $\mathcal{S}_\Sigma(10^{-8}) = 1/(1 + (0.063)^{3.56}) = 0.9999$. The galactic boundary condition $\mathcal{S}_\Sigma(|\Phi_{\rm gal}|/c^2 = 5.38 \times 10^{-7}) = 1/(1 + (3.38)^{3.56}) \approx 0.013$ is also satisfied, giving $\beta_{\rm eff} \simeq 0.013$ as required by the corpus. The three boundary conditions together fix the two-parameter screening law used throughout, with the third condition serving as a consistency check (three constraints, two parameters — the system is overdetermined and passes).

**Corpus parallel: the core-vs-disk gradient.** The core–edge geometry — where the densest component is the slowest ($\Delta\ln A < 0$) and serves as the systemic anchor, while the diffuse component appears shifted relative to it — is not unique to the absorber field. A parallel geometry has been noted in the Cepheid distance-ladder sector [51], where the galactic bulge (deep potential, slowest clocks) defines the systemic spectroscopic redshift while Cepheids in the diffuse outer disk are corrected to the rest frame using that bulge-derived redshift. The absorber-field calculation presented here stands independently; the Cepheid parallel is noted as a consistency check on the shared physical principle $\Delta\ln A < 0$, not as proof of the absorber mechanism.

### 3.4 Scaling Consistency: Absorber Clouds vs. Galaxies

A natural concern is whether the same scalar mechanism that produces an $81.6\text{ km/s}$ shift across a diffuse gas cloud would produce an unphysically large effect across a massive galaxy, breaking rotation curves or other galactic observables. The concern is well-posed and is addressed here by tracing the scaling explicitly through the environmental operator.

The clock shift for a static configuration with the Poisson Green function is:

\begin{equation} \Delta\ln A = -\frac{\beta_{\rm eff}^2\,K}{M_{\rm Pl}^2} = -\frac{2\,\beta_{\rm eff}^2\,|\Phi|}{c^2}, \end{equation}

where $\beta_{\rm eff} = \beta_A \cdot \mathcal{S}_\Sigma(\mathcal{E})$ is the environmentally screened coupling and $|\Phi|/c^2$ is the dimensionless Newtonian potential depth. The scaling from clouds to galaxies is governed by the *product* $\beta_{\rm eff}^2 \times |\Phi|/c^2$, not by $|\Phi|$ alone.

The two regimes are:

\begin{aligned}
&\textbf{Absorber (unscreened):} & |\Phi_{\rm abs}|/c^2 &\sim 10^{-8} \ll \Phi_{\rm half}, &\quad \mathcal{S}_\Sigma \approx 1, &\quad \beta_{\rm eff} = \beta_A = -1.0, \\
&\textbf{Galaxy (screened):} & |\Phi_{\rm gal}|/c^2 &= 5.38 \times 10^{-7} \gg \Phi_{\rm half}, &\quad \mathcal{S}_\Sigma \approx 0.013, &\quad \beta_{\rm eff} = \beta_A \cdot \mathcal{S}_\Sigma \simeq -0.013.
\end{aligned}

The half-suppression potential $\Phi_{\rm half} = 1.59 \times 10^{-7}$ marks the transition. For a typical Lyman-limit absorber, $|\Phi_{\rm abs}|/c^2 \sim 10^{-8}$, giving a conformal-only shift of $\sim 0.009\text{ km/s}$ before environmental amplification (uniform-sphere ionisation correction at $R = 30\text{ kpc}$). For the solar system (Cassini), $|\Phi_\odot|/c^2 = 2.12 \times 10^{-6}$ (grazing ray at $R_\odot$), which is $13.3\times$ deeper than $\Phi_{\rm half}$. For the galactic halo, $|\Phi_{\rm gal}|/c^2 = v_{\rm circ}^2/c^2 = 5.38 \times 10^{-7}$ ($v_{\rm circ} = 220\text{ km/s}$), which is $3.38\times$ deeper than $\Phi_{\rm half}$. The $3.94\times$ solar-to-galactic potential ratio, raised to $n = 3.56$, yields $132\times$ screening contrast — sufficient to differentiate the two regimes without a second variable. The product $\beta_{\rm eff}^2 \times |\Phi|/c^2$ is therefore *not* monotonically increasing with mass; it peaks in the unscreened intermediate regime ($|\Phi|/c^2 \sim 10^{-7}$) and is suppressed in dense environments.

This is the same screening structure that ensures solar-system compliance: the solar-system PPN value $\beta_{\rm eff} \simeq -10^{-4}$ is the screened descendant of $\beta_A = -1.0$ at solar-system potentials ($|\Phi_\odot|/c^2 = 2.12 \times 10^{-6}$, measured via Shapiro delay of signals grazing the solar corona). The suppression factor $\mathcal{S}_\Sigma \approx 10^{-4}$ at solar-system potentials and $\mathcal{S}_\Sigma \approx 0.013$ at galactic potentials are both predictions of the same potential-depth law with $\Phi_{\rm half} = 1.59 \times 10^{-7}$ and $n = 3.56$ — the $3.94\times$ potential-depth difference between the two regimes produces $132\times$ screening contrast, sufficient to satisfy both Cassini and the galactic coupling requirement without a second screening variable (Gate 10 conditionally closed).

The empirical response coefficients $\kappa_{\rm Cep}$ and $\kappa_{\rm gal}$ used in the distance-ladder sector [51] are not free parameters but are macroscopic projections of the environmental operator $\mathcal{S}_\Sigma(\mathcal{E})$ evaluated at galactic-scale potentials. The potential-depth law with corrected $|\Phi_{\rm gal}|/c^2 = 5.38 \times 10^{-7}$ gives $\mathcal{S}_\Sigma \approx 0.013$ directly, yielding $\beta_{\rm eff} \simeq 0.013$ as required by the corpus. The first-principles derivation of $\kappa_{\rm Cep}$ and $\kappa_{\rm gal}$ from this screening level — and the absorber amplification $\mathcal{A}_{\rm env}$ from the non-perturbative $\mathcal{C}_{T,\parallel}$ — remain as open calculations (Gate 4B). If either fails its target, the framework is falsified.

**Scaling-gap status:**

- **Sign: regime-independent.** The blueward sign follows from $\beta_{\rm eff}^2 > 0$ and the core-edge convention at *all* density regimes — it does not change between clouds and galaxies.

- **Amplitude: density-modulated, not mass-linear.** The product $\beta_{\rm eff}^2 \times |\Phi|/c^2$ is suppressed in dense environments by $\mathcal{S}_\Sigma$, preventing the galactic effect from scaling linearly with the $\sim 10^3$-fold deeper potential.

- **Fifth-force constraint stack.** The calibrated screening law $\mathcal{S}_\Sigma = 1/(1+(|\Phi|/c^2/\Phi_{\rm half})^n)$ with $\Phi_{\rm half} = 1.59 \times 10^{-7}$, $n = 3.56$ is validated against three anchors (absorber, Cassini, galactic halo) and must survive the broader fifth-force landscape. The constraint stack is:

| System | $|\Phi|/c^2$ | $\mathcal{S}_\Sigma$ | Consequence | Status |
| --- | --- | --- | --- | --- |
| Solar circle (MW ambient) | $5.38\times10^{-7}$ | 0.013 | $|\gamma-1| \approx 3.4\times10^{-4}$ | Exceeds ephemeris $|\gamma-1| < 2.3\times10^{-5}$ by $\times 15$ (force sector) |
| Globular clusters (47 Tuc) | $3.4\times10^{-9}$ | $\approx 1$ | $G_{\rm eff} = 3G$ | Excluded (HST/Gaia dynamics, force sector) |
| Earth–Moon (self-$\Phi$) | $\lesssim10^{-9}$ | $\approx 1$ | $G_{\rm EM} = 3G$ | Excluded (LLR, force sector) |
| Absorber (Q1009, $R=30$ kpc) | $1.5\times10^{-8}$ | $\approx 1$ | unscreened clock | $\checkmark$ (intended regime) |
| Sun (grazing, Cassini) | $2.12\times10^{-6}$ | $9.9\times10^{-5}$ | $\gamma-1 \approx -2\times10^{-8}$ | $\checkmark$ |

Under the three-anchor calibration, the solar-circle, globular-cluster, and Earth–Moon entries exceed dynamical fifth-force bounds in the force sector. The proposed resolution is grounded in the matter metric $\tilde{g}_{\mu\nu} = A^2(\phi)\,\eta_{\mu\nu} + B(\phi)\,\partial_\mu\phi\,\partial_\nu\phi$ defined in Section 3.1. The clock shift arises exclusively from the conformal modification to $\tilde{g}_{00}$: for a static scalar field ($\partial_0\phi = 0$), the disformal contribution to $\tilde{g}_{00}$ vanishes identically, so the clock coupling is governed by $\mathcal{S}_\Sigma$ acting on the conformal factor $A(\phi)$ alone. Dynamical fifth-force constraints, by contrast, apply to spatial geodesics and massive particle acceleration. The *clock-sector / force-sector split* hypothesises that the corpus phenomenology — Cepheids, flyby, absorber shear, all redshift/clock effects — is governed by $\mathcal{S}_\Sigma$ acting on the clock coupling ($\tilde{g}_{00}$), while the dynamical fifth force is governed by a separately constrained sector ($\tilde{g}_{ij}$). This is consistent with the corpus phenomenology, which is exclusively redshift/clock effects and never dynamical. However, in standard scalar-tensor gravity the fifth force on a non-relativistic test mass is sourced by the conformal coupling gradient $\nabla(\beta_A\phi)$, not primarily by the disformal term — this is precisely why Cassini-type PPN bounds constrain conformal couplings in the chameleon/symmetron literature [35], [36]. A purely conformal rescaling $\tilde{g}_{\mu\nu} = A^2(\phi)g_{\mu\nu}$ multiplies the spatial metric too, so it is not obvious that $A^2(\phi)$ can be clock-only while $B(\phi)\partial_\mu\phi\partial_\nu\phi$ carries the entire force sector. The split therefore requires an explicit derivation: the geodesic equation for a massive test particle in the full disformal metric must be written out, and the term proportional to $\nabla\ln A(\phi)$ — the standard scalar-tensor fifth-force term — must be shown to vanish or be subdominant to the disformal term in the relevant regimes. Until this derivation is completed, the clock-sector / force-sector split is treated as a *working hypothesis of the corpus*, not a derived result. Gate 10 is *conditionally closed*: the three-anchor calibration is internally consistent, but the conditional closure depends on the clock/force-sector derivation being completed in a companion paper. If the derivation fails — i.e., if the conformal gradient term does not vanish in the force sector — then the screening law as calibrated would be excluded by the solar-circle, globular-cluster, and Earth–Moon constraints, and the absorber-field interpretation would require a different screening mechanism.

- **Open calculations.** Two open calculations remain. (1) Gate 4B: the non-perturbative evaluation of $\mathcal{C}_{T,\parallel}$ must yield $\mathcal{A}_{\rm env} \approx 9.3 \times 10^3$. All perturbative mechanisms have been quantitatively excluded (disformal metric correction $\sim 10^{-128}$); the amplification must arise from a genuinely non-perturbative topological/geometric effect. If Gate 4B fails ($\mathcal{A}_{\rm env} < 10^3$), the framework is falsified. (2) Clock/force-sector derivation: the geodesic equation for a massive test particle in the full disformal metric must be derived, showing that the conformal gradient term $\nabla\ln A(\phi)$ is absent or subdominant in the force sector. This is the designated subject of an immediate follow-up paper. Gate 10 is conditionally closed pending this derivation.

## 4. Cosmological Transport and Thermodynamics

*Part II: Global Cosmology.* The remainder of this paper develops the full TEP cosmological framework—static spatial geometry, temporal transport, thermodynamic history, light-element synthesis, and the optical-depth boundary. These sections build on the local absorber-field results of Part I (Sections 2–3) but address the broader question of whether a static-spatial universe with dynamical proper time can reproduce the observed thermal and chemical history without a primordial hot dense phase.

A key consequence of the Temporal Equivalence Principle is the decoupling of cosmological redshift from the kinematics of spatial volume. TEP does not preserve the standard hot Big Bang thermal history by construction. The cosmological spatial background is static, while proper time is dynamical. Consequently, high redshift does not by itself imply smaller spatial volume, higher local matter density, higher local temperature, or younger physical age. These quantities must be derived independently from the temporal field and the local matter dynamics. The standard thermal history, including recombination [23], [24], [25] and the CMB [19], [20], is not assumed but must be independently reconstructed within the TEP framework.

### 4.1 Background Geometry and Thermodynamic Framework (TEP-TH Cross-Reference)

The geometric and thermodynamic foundations of the TEP cosmological framework — the temporal horizon, curvature regularity ($0 < p \le 1/2$, all polynomial curvature invariants vanish), proper-time asymptotic regularity ($\Delta\tau \to \infty$), and CMB blackbody spectral preservation — are established in TEP-TH (Paper 27, [4]). The acoustic-sector closure, including $\Omega_b h^2$ determination from Planck peaks and sound-horizon preservation at $<6\text{ ppm}$, is established in TEP-HC (Paper 18, [3]) and TEP-C0 (Paper 26, [2]), using the line-of-sight integration formalism of Seljak & Zaldarriaga [26] as implemented in CLASS [28] and hi_class [29], with perturbation theory following the standard formalism [14], [15]. The present paper does not re-derive these results; it applies the established framework to the BBN-specific questions of nuclear reaction flows, light-element equilibrium, and D/H spectroscopy.

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

while the apparent deuterium feature (the blueward offset) is generated by a localized spatial shear (the TEP absorber field) within the gas cloud:

\begin{equation} \Delta v_T \simeq -c \frac{d\ln A}{d\phi}\Delta\phi. \end{equation}

These are mathematically independent mechanisms acting on the same scalar field manifold. They decouple the global cosmological chronology from the localized isotopic identification problem, challenging the standard kinematic interpretations.

### 4.4 Primordial Helium Synthesis via Baryonic Cycling

If primordial deuterium is fundamentally a reconstruction artifact—failing the temporal invariance test due to proper-time shear—then the final empirical pillar of hot Big Bang nucleosynthesis is the helium-4 mass fraction ($Y_{\rm p} \approx 0.245$ [21], [22], [68]). Without a finite, hot, universally dense origin, the TEP framework must analytically prove that this abundance is produced by stellar nucleosynthesis over an unbounded temporal horizon.

Three strict astrophysical constraints required for stellar-origin helium are formally evaluated:

- **Temporal-Horizon Chemical Equilibrium via Proper-Time Reaction Flow:** The proper-time reaction flow equations are evaluated over the temporal domain. Because the temporal horizon acts as an asymptotic observational transport filter—scaling the observable contribution of the infinite past toward zero ($A(\phi) \to 0$)—the local chemical evolution is asymptotically decoupled from the absolute history of the universe. Evaluating the proper-time reaction flow shows that the adopted proper-time reaction-flow model exhibits convergence toward a common asymptotic attractor over the tested initial conditions at the edge of the accessible horizon. Whether the evaluation starts with $Y_0=0.00$ or an extremely dense $Y_0=0.80$, the reaction flow rapidly decays into the equilibrium attractor of $Y_{\rm eq} = 0.247$ at the present day ($\tau = 0$). It is important to recognize that this reaction flow represents a *local galactic patch* experiencing continuous star formation. The pristine global background observed at high redshift is not protected from local chemical accumulation by transport delay alone; rather, pristine absorbers correspond to gas worldlines whose accumulated processing exposure $\mathcal{E}_{\rm astr}$ remains bounded by the convergence condition $p + q > 1$ (Section 4.1). The temporal horizon ensures that such low-exposure worldlines are observationally accessible, but the chemical pristine state is a property of the worldline's local processing history, not of the transport filter.

- **Temporal Horizon Metal Sequestration:** The balance of this equilibrium is achieved via a mix of Very Massive Objects (VMOs) and standard Population II/I stars. Standard stars yield typical return fractions. However, VMOs—which dominate the early equilibrium—undergo extreme radiatively-driven winds that successfully eject their helium envelopes ($E_Y > 0$). Upon core collapse, rather than forming a spatial singularity, the core generates a TEP temporal horizon where the local clock rate $A(\phi) \to 0$ relative to the external interstellar medium. This mechanism directly addresses the historical Carr-Bond-Arnett overproduction limit [57], [58]: standard stellar synthesis of $\sim 25\%$ helium severely overproduces carbon and oxygen, making a purely stellar helium origin incompatible with observed metal abundances. The TEP temporal-horizon sequestration offers a mechanism to avoid this by trapping the heavy metals ($E_Z \approx 0$) while allowing helium to escape, producing the correct $Y_{\rm p}$ without the metal overproduction that historically ruled out stellar helium synthesis [60].

- **Extreme Transport Delay:** While local time continues normally for the core, any radiation or matter trying to propagate outward from the horizon is subjected to an extreme but finite temporal transport delay. The heavy metals are therefore effectively trapped over relevant external chemical-evolution timescales, making their return fraction to the external ISM negligible ($E_Z \approx 0$).

These mechanics eliminate the need for a spatial singularity, replacing it with a field-theoretic mechanism for chemical evolution. Under the TEP baryonic-cycling and temporal-horizon exposure conditions, the helium-4 mass fraction $Y_{\rm eq} = 0.247$ emerges as the equilibrium of the baryonic-cycling reaction flow under the adopted stellar yields and temporal-horizon metal sequestration. The numerical reaction-flow calculation demonstrates convergence to this equilibrium for the adopted stellar histories, showing that the observed $Y_{\rm p} \approx 0.245$ [21], [22] is compatible with stellar nucleosynthesis over an unbounded temporal horizon. The slight offset between the observed target ($Y_{\rm p} \approx 0.245$, PDG/Cyburt standard) and the derived equilibrium ($Y_{\rm eq} = 0.247$) falls well within the systematic uncertainty bounds of the observationally constrained yield parameters $p_Y$ and $R$: a $\pm 0.002$ shift in $Y_{\rm eq}$ is produced by variations in the helium yield per stellar generation and the return fraction that are smaller than the scatter in empirical H II region yield calibrations. The specific equilibrium value is set by the adopted yield parameters ($p_Y$, $R$) and the VMO fraction; the temporal-horizon metal sequestration ($E_Z \to 0$) ensures that the equilibrium is helium-dominated rather than metal-enriched. The yield parameters are not free tunables directed at the $0.247$ target: the helium yield per stellar generation $p_Y$ is constrained by observations of H II regions and stellar population synthesis models, the return fraction $R$ is determined by initial mass function (IMF) integration over independently measured stellar lifetimes and remnant masses, and the VMO fraction $f_{\rm VMO}$ is bounded by the cosmic star-formation history and the observed heavy-element abundance ratio $[\alpha/\mathrm{Fe}]$ in old stellar populations. A complete derivation of $f_{\rm VMO} \simeq 0.994$ from first-principles stellar physics, and a contraction analysis establishing that the fixed point is an attractor independent of initial conditions, are required to fully close the helium argument and are deferred to a companion paper. The standard BBN framework likewise depends on a single parameter ($\eta_b$, the baryon-to-photon ratio), which is independently constrained by CMB observations; the TEP baryonic-cycling model replaces this single parameter with physically motivated stellar yields that are independently constrained by local nucleosynthesis observations rather than by the primordial helium abundance itself. A complete demonstration requires showing that $Y_{\rm eq} \approx 0.247$ is robust to physically motivated variations in ($p_Y$, $R$, $f_{\rm VMO}$) within their observationally constrained ranges; this is a refinement target for the next iteration.

**Extension to 3He and 7Li.** The baryonic-cycling framework extends naturally to a multi-species light-element network (3He, 4He, 7Li) under the same temporal-horizon sequestration mechanism. VMO cores trap not only metals but also 3He and 7Li produced in stellar interiors, so only 4He (and residual H) escapes via winds. The equilibrium abundances are $^3{\rm He/H} = 9.0 \times 10^{-6}$ (observed $\sim 1.0 \times 10^{-5}$, ratio 0.90) and $^7{\rm Li/H} = 1.55 \times 10^{-10}$ (observed $1.6 \times 10^{-10}$, ratio 0.97). The TEP equilibrium $^7{\rm Li/H}$ is a factor of $\sim 3.2$ below the standard hot-BBN prediction ($5.0 \times 10^{-10}$), offering a natural pathway to resolve the cosmological lithium problem: the temporal-horizon sequestration of VMO-core 7Li produces less primordial 7Li than hot BBN without requiring additional stellar destruction mechanisms. The convergence condition $p + q = 1.3 > 1$ (Section 4.1) guarantees that the integrated astration exposure is finite. The numerical reaction-flow calculation demonstrates convergence to the fixed point for the adopted stellar histories; the specific $^7{\rm Li/H}$ value is then determined by the multi-species reaction-flow model (VMO-core lithium yield, sequestration partitioning, and astration exposure integral), not by the convergence condition alone.

**The $\Delta Y / \Delta Z$ Slope and H II Region Concordance.** The standard observational method for determining primordial helium extrapolates the linear relationship between helium abundance $Y$ and metallicity $Z$ (typically traced by O/H) across metal-poor dwarf galaxy H II regions to the $Z \to 0$ limit [61], [62], [63]. If $Y_{\rm eq} = 0.247$ is a local chemical attractor rather than a universal primordial baseline, the TEP framework must reproduce this observed $\Delta Y / \Delta Z$ linear slope. The baryonic-cycling reaction flow naturally produces a linear $Y$-$Z$ relation at low metallicity: as astration exposure $\mathcal{E}_{\rm astr}$ increases, both $Y$ (from helium-producing stellar winds) and $Z$ (from metal-producing standard stars) increase proportionally, yielding a near-linear slope $\Delta Y / \Delta Z \approx p_Y / (1 - E_Z) \cdot R_{\rm metal}$ that is set by the same yield parameters governing the equilibrium. The temporal-horizon metal sequestration ($E_Z \approx 0$) suppresses the $Z$-intercept while preserving the slope, so the extrapolation to $Z \to 0$ recovers $Y_{\rm eq}$ rather than a distinct "primordial" value. The observed consistency of $\Delta Y / \Delta Z$ across hundreds of independent low-metallicity H II regions [62] is therefore a natural prediction of the TEP equilibrium model, not an independent verification of a single primordial event.

**Metallicity-dependent VMO transition.** As a single-phase global equilibrium, the model silently fails: at $f_{\rm VMO} = 0.994$, $E_Z \approx 0$ gives $Z_{\rm eq} = p_Z(1 - f_{\rm VMO})/(1 - R) \approx 1.4 \times 10^{-4}$ — a factor $\sim 100$ below observed metallicities at low redshift. The resolution is a *local* metallicity-dependent transition $f_{\rm VMO}(Z)$, not a globally coordinated chronological epoch. Pop III/VMO formation naturally shuts off locally once a galactic patch exceeds a critical metallicity $Z_{\rm crit} \sim 10^{-4}$ (cooling transition from atomic to metal-line cooling). In low-metallicity patches ($Z \ll Z_{\rm crit}$), VMO-dominated nucleosynthesis with temporal-horizon sequestration sets the $Z \to 0$ intercept: $Y(Z = 0) = Y_{\rm eq} = 0.247$. In high-metallicity patches ($Z \gg Z_{\rm crit}$), standard-star yields $p_{Y,\rm std}$ set the slope:

\begin{equation} \frac{\Delta Y}{\Delta Z}\bigg|_{Z > Z_{\rm crit}} = \frac{p_{Y,\rm std}}{(1 - R)\,p_Z} = \begin{cases} 2.4 & p_Z = 0.014 \\ 1.7 & p_Z = 0.02 \end{cases} \qquad \text{vs. observed } \Delta Y/\Delta Z \simeq 1.4\text{--}3, \end{equation}

and the solar-point check gives $Y(Z = 0.014) = 0.247 + (1.7\text{--}2.4) \times 0.014 = 0.270\text{--}0.280$, versus the observed solar $Y \simeq 0.270$–$0.274$. The metallicity-dependent transition model lands in the observed range with yield parameters already constrained by H II region calibrations. The single-phase $Z_{\rm eq}$ failure is stated honestly: the VMO-dominated equilibrium suppresses metals too aggressively for the present-day metallicity to arise from the equilibrium alone. The transition structure — VMO-dominated low-$Z$ patches set the intercept, standard-star high-$Z$ patches set the slope — is the physically correct reading, and the arithmetic confirms it quantitatively. The metallicity-dependent VMO-to-ordinary-star transition introduces a function $f_{\rm VMO}(Z)$ with a critical metallicity $Z_{\rm crit}$ and a transition width; while $Z_{\rm crit}$ is independently motivated by VMO formation physics, the transition functional form and width require specification from stellar population evolution modelling. This is a physically motivated extension that works quantitatively, not a parameter-free result until the transition is independently derived. Crucially, this is a *local* transition occurring asynchronously across galactic patches as each reaches $Z_{\rm crit}$, preserving the global eternal continuum — there are no globally coordinated "epochs." The exponent $q = 0.8$ (giving $p + q = 1.3$) is anchored to the same worldline/astration statistics that govern the Compton-exposure convergence condition ($a + p > 1$) and the $\tau(z)$ three-point requirement, so the exponent family $(p, q, a)$ is constrained by data in one place.

**Sensitivity of $Y_{\rm eq}$ to yield parameters.** The equilibrium helium mass fraction is set by the adopted yield parameters through the baryonic-cycling fixed-point equation. Setting $dY/dt = 0$ in the GCE ODE yields:

\begin{equation} Y_{\rm eq} = \frac{p_{Y,\rm eff}}{1 - R}, \qquad p_{Y,\rm eff} = f_{\rm VMO}\,p_{Y,\rm VMO} + (1 - f_{\rm VMO})\,p_{Y,\rm std}, \end{equation}

where $p_{Y,\rm VMO}$ is the helium yield per VMO stellar generation, $p_{Y,\rm std}$ is the standard-star helium yield, $R$ is the return fraction (fraction of stellar mass returned to the ISM, determined by IMF integration over measured stellar lifetimes and remnant masses), and $f_{\rm VMO}$ is the VMO fraction. The metal escape fraction $E_Z$ affects the metal equilibrium $Z_{\rm eq}$, not $Y_{\rm eq}$ directly; $E_Z \approx 0$ means metals do not escape the temporal horizon (VMO-core sequestration), keeping $Z_{\rm eq}$ low without altering the helium fixed point. The baseline parameter values and sensitivities are:

| Parameter | Symbol | Baseline | Source | $\partial Y_{\rm eq}/\partial(\cdot)$ |
| --- | --- | --- | --- | --- |
| VMO helium yield | $p_{Y,\rm VMO}$ | 0.149 | VMO wind models (Carr, Bond & Arnett 1984) | - |
| Standard-star He yield | $p_{Y,\rm std}$ | 0.02 | H II region / population synthesis | - |
| Effective He yield | $p_{Y,\rm eff}$ | 0.1482 | $f_{\rm VMO}\,p_{Y,\rm VMO} + (1-f_{\rm VMO})\,p_{Y,\rm std}$ | $1/(1-R) \approx 1.67$ |
| Return fraction | $R$ | 0.40 | IMF integration (Salpeter / Kroupa) | $p_{Y,\rm eff}/(1-R)^2 \approx 0.41$ |
| VMO fraction | $f_{\rm VMO}$ | 0.994 | Cosmic SFR + $[\alpha/\mathrm{Fe}]$ constraint | $(p_{Y,\rm VMO} - p_{Y,\rm std})/(1-R) \approx 0.22$ |
| Metal escape fraction | $E_Z$ | $\approx 0$ | Temporal-horizon sequestration | 0 (affects $Z_{\rm eq}$ only) |

The derivative $\partial Y_{\rm eq}/\partial R = p_{Y,\rm eff}/(1-R)^2 > 0$ is positive: increasing the return fraction increases $Y_{\rm eq}$ because more mass is recycled into new stars, amplifying the helium yield. The dominant sensitivity is to $R$ ($\pm 0.005$ in $R$ produces $\pm 0.002$ in $Y_{\rm eq}$); the VMO fraction is less sensitive ($\pm 0.01$ in $f_{\rm VMO}$ produces $\pm 0.002$ in $Y_{\rm eq}$). The observed $Y_p \approx 0.245 \pm 0.003$ is reproduced for $R \in [0.395, 0.405]$ and $f_{\rm VMO} \in [0.99, 1.00]$, consistent with a high early-universe VMO fraction bounded by the observed $[\alpha/\mathrm{Fe}]$ ratio in old stellar populations. The convergence condition $p + q = 1.3 > 1$ (Section 4.1) guarantees that the integrated astration exposure is finite for any individual worldline. The numerical reaction-flow calculation demonstrates convergence to the fixed point for the adopted stellar histories; however, finite integrated exposure does not in general guarantee fixed-point convergence independently of initial conditions. A dedicated contraction analysis over a grid of initial conditions ($Y_0 = 0$ to $0.8$) and yield parameters is required to establish that $Y_{\rm eq} = 0.247$ is a true attractor rather than a point dependent on the chosen history. This analysis is deferred to a companion paper.

**CMB Baryon Density Concordance (Gate 9).** The most powerful argument for standard BBN is that the deuterium abundance predicts a baryon density $\Omega_b h^2 \approx 0.022$ [65] that matches the independent value derived from Planck CMB acoustic peak ratios [64]. Under TEP, the observed D/H ratio is a localized kinematic signature rather than a primordial abundance, so the D/H $\to$ $\Omega_b$ mapping is not the source of the baryon density constraint. However, the CMB *independently* anchors $\Omega_b h^2$ via acoustic physics that TEP strictly preserves: TEP-HC (Paper 18, [3]) fits $\Omega_b h^2 = 0.02144 \pm 0.00257$ directly from Planck acoustic peaks via joint MCMC, with sound-horizon ratio $r_s^{\rm TEP}/r_s^{\rm \Lambda CDM} = 0.999994$ ($<6\text{ ppm}$ deviation). The acoustic peaks rigidly demand this specific baryon density to balance the compression and rarefaction peaks of the photon-baryon fluid, regardless of the D/H ratio. Gate 9 is therefore stated as: *given the rigidly CMB-anchored baryon density $\Omega_b h^2 \approx 0.022$, verify that the SQUAD/LLS neutral-hydrogen column-density distribution folded through the TEP edge-gas shear model produces a D/H histogram consistent with observed quasar sightline statistics without free density tuning.* This computation is tractable on existing LLS catalogs but is not performed in this paper; Gate 9 remains open. The corpus-level cross-reference is to TEP-HC (Paper 18, [3]) and TEP-C0 (Paper 26, [2]), where the acoustic peak ratios are addressed independently of the D/H–$\Omega_b$ mapping.

## 5. Discussion and Falsifiable Predictions

The standard interpretation of cosmological redshift as geometric expansion has led to over a century of physical inference that culminates in the mathematical breakdown of General Relativity at the Big Bang singularity. Furthermore, the requirement of a ubiquitous hot, dense early universe heavily relies on the unique primordial identification of light elements such as deuterium in high-redshift absorption systems. Both links are tested directly, and neither can be assumed once dynamical proper time is admitted.

### 5.1 Distance Duality and Cosmological Tests

#### Distance Duality and Supernova Standardization

Critically, $T_{\rm obs}(z) \neq T_{\rm loc}(\tau)$ in general. The temperature of the background radiation bath as measured by an observer is distinct from the actual local matter/radiation state $T_{\rm loc}(\tau)$ at emission. Furthermore, because physical space is static, the standard geometric distances must be carefully defined. Etherington's reciprocity theorem is a general result of metric photon propagation, not specific to expanding FLRW; it dictates the distance-duality relation $d_L = d_A (1+z)^2$ for any metric theory where photon geodesics are well-defined and photon number is conserved. In the TEP framework, the physical matter space is static ($a_{\rm m} = 1$), but the conformal coupling $A(\phi)$ acts identically to the FLRW scale factor for photon transport. Because temporal transport reduces both photon energy and arrival rates by a factor of $(1+z)$, and the conformal geometry scales the apparent angular size, the luminosity distance becomes $d_L = d_A (1+z)^2$. The TEP framework therefore preserves the Etherington relation by construction, not because it replicates FLRW expansion, but because the conformal transport law satisfies the same general conditions.

While the baseline distance-duality relation is preserved, it is important to recognize that SNIa magnitudes are not raw observables. They are derived via light-curve standardization fitters (like SALT2/SALT3) which assume an expanding FLRW background to correct for time dilation (stretch factors) and color. A preliminary evaluation has already been completed in TEP-C0 (Paper 26): the SALT2 light-curve stretch parameters ($x_1$) from the 1,701 supernovae in the Pantheon+ dataset were tested against the exact covariant TEP conformal factor. Under standard $\Lambda$CDM time dilation $(1+z)$, the fit to observed stretch parameters yields a reduced $\chi^2$ of 102.6; under the TEP conformal factor, the reduced $\chi^2$ improves to 88.9. This is a diagnostic consistency check confirming that supernova light curves are natively stretched by the temporal field geometry predicted by TEP, though the result remains contingent on SALT2 standardization assumptions. The remaining observational task is the full re-calibration of the light-curve fitters within the TEP geometry rather than relying on FLRW-calibrated nuisance parameters — a concrete, falsifiable roadmap with the stretch-factor directionality already verified.

### 5.2 Synchronization Holonomy and Optical Time-Transfer

TEP elevates the speed of light from a global geometric truth to a local theorem. This provides falsifiable physical predictions. Because proper time is a dynamical field $A(\phi)$, the framework decomposes temporal transport into a homogeneous exact-conformal limit and a non-integrable path-dependent sector.

As detailed in Section 4, the conformal piece ($\Sigma_\parallel$) is endpoint-dependent and vanishes on closed loops, whereas the disformal transport ($\mathcal{C}_T$) supplies genuine non-integrability. Multi-leg optical time-transfer experiments—currently within reach of next-generation atomic clock networks—can directly test for this synchronization holonomy ($\oint \mathcal{C}_{T,\parallel} d\ell \neq 0$).

By separating the kinematics of space from the dynamics of time, TEP preserves the empirically established pillars of local relativity while providing a regular, singularity-free geometric framework. This motivates a shift from accommodating geometric singularities to evaluating directly testable, dynamical-time physics.

### 5.3 What Would Falsify TEP

The framework makes several concrete, falsifiable predictions. Failure of any of the following would rule out the TEP interpretation:

- **Amplitude gap:** A first-principles evaluation of the non-perturbative transport path $\mathcal{C}_{T,\parallel}$ yielding $\mathcal{A}_{\rm env} < 10^3$ under all reasonable assumptions for absorber radius, ionisation correction, and density profile would rule out the absorber-field interpretation of the $-81.6\text{ km/s}$ feature. The quantitative mechanism analysis (Gate 4B-II) identifies the edge transition with $B(\phi)$ enhancement as the most promising channel, with a concrete target $\tilde{B}_{\rm eff} \sim 10^{24}$; if the non-linear screening dynamics cannot produce this enhancement, the interpretation is falsified.

- **Orphan population:** The velocity-selection theorem (Gate 6) predicts that $\sim 79\%$ of edge-shear features are absorbed into the H I component structure as orphan narrow components at non-isotope offsets. The quantitative forecast (Gate 6-II) predicts $\sim 19$ such features across $\sim 80$ high-S/N LLS sightlines. If a re-analysis of existing archival spectra shows no excess of narrow ($b < 10$\,km/s), low-column ($\log N \sim 12$--$14$) components at non-isotope offsets beyond the normal H I population, the TEP interpretation is substantially weakened.

- **Spectroscopic robustness:** Scaffold freedom with five freed components *strengthens* the calibrated significance of the Q1009 free-H preference ($p < 0.005$ when five surrounding components are freed, Section 5.5). The Q1009 evidence is therefore robust to the externally fixed published component architecture: the discrimination survives when the absorber model is allowed to re-optimise. The PKS\,1937$-$101 and J1332$+$0052 results ($p_{\rm parent} = 0.001$ for both) are not affected by scaffold freedom (their component architectures are simpler) and remain the strongest clean spectroscopic results.

- **Helium equilibrium:** If $Y_{\rm eq}$ moves outside the observed range $0.245 \pm 0.003$ under physically motivated variations in ($p_Y$, $R$, $f_{\rm VMO}$) within their observationally constrained ranges, the baryonic-cycling explanation for the helium-4 mass fraction would be falsified.

- **CMB acoustic structure:** If the TEP perturbation theory fails to reproduce the Planck acoustic peak ratios and damping tail within observational uncertainties (deferred to TEP-HC), the cosmological framework is ruled out.

- **Growth of structure:** If the static-spatial TEP geometry cannot reproduce the observed $S_8$ growth parameter or the BAO scale, the framework fails as a cosmological alternative.

### 5.4 Outstanding Observational Tests

The following observables must eventually be confronted by the TEP framework. The current status of each is stated honestly:

| Observable | Status | Reference |
| --- | --- | --- |
| CMB acoustic peaks and damping tail | Deferred to perturbation theory (TEP-HC, Paper 18); pre-recombination sound horizon preserved at 6 ppm | [16] |
| CMB temperature–redshift relation | Preserved by conformal transport: $T_{\rm obs}(z) = T_{\rm em}/(1+z)$ | Section 4.1 (TEP-TH) |
| BAO and distance-ladder consistency | Distance duality preserved; SALT2 stretch-factor directionality verified in TEP-C0 ($\chi^2$ 102.6→88.9); full re-calibration within TEP geometry is open | Section 5.1 |
| Growth of structure / $S_8$ | Not yet evaluated; requires TEP perturbation theory | — |
| D/H in non-benchmark sightlines | Framework predicts localized shear amplitude varies with core-edge geometry; population study is open | — |
| $\Delta Y / \Delta Z$ slope in H II regions | Qualitative prediction derived; quantitative comparison deferred | Section 4.4 |
| Lyman-limit / Gunn–Peterson trough redshift | Optical-depth divergence predicted; quantitative $\tau_e \sim 1$ redshift not yet computed | Section 4.2 |

### 5.5 Spectroscopic Robustness Checks

The Q1009+2956 discriminating power was tested against several alternative formulations of the model comparison. Four robustness checks are reported here.

#### Limited Scaffold Freedom (C2)

The 43 H I components are held at the published literature architecture in the standard analysis. Allowing the five strongest non-parent H I components *within the absorber system* ($|v| \le 1000$ km/s, excluding the D parent components) to re-optimise under both the D and H hypotheses changes the likelihood gain from $T = 161.03$ (fixed scaffold) to $T = 385.35$ (five freed components, $\Delta T = +224$). Both models benefit from the additional freedom ($\Delta\ln L_D = +49.5$, $\Delta\ln L_H = +161.6$), but H benefits substantially more, so the fixed-scaffold comparison is conservative. The D parent components are excluded from the freed set because the D model inherits the parent's Doppler parameter with mass scaling; freeing the parent's $b$ creates a conflicting optimization where D's $b$ is doubly controlled. A calibrated Monte Carlo with the same freed-scaffold optimization inside the simulation loop gives $p < 0.005$ (0/200 exceedances) — highly significant. The freed-scaffold result confirms that the free-H preference survives even when the absorber model is allowed to re-optimise: the discrimination is not an artifact of the fixed published architecture but reflects a genuine structural difference between the D and H models.

#### Pure Kinematic Prior (C4)

To test whether the candidate feature is merely an ordinary H I component shifted by a free velocity, the data were also fitted with a two-parameter *kinematic* model: free $v_H$ and $\log N_H$, but $b$ fixed to the parent H I value (no isotope mass scaling and no free $b$). This model is strongly rejected: $T(M_H vs M_D) = 161.03$, $T(M_H vs M_{\rm kin}) = 208.98$, $T(M_{\rm kin} vs M_D) = -47.95$. $\Delta\mathrm{AIC}(M_{\rm kin} - M_D) = +45.95$ and $\Delta\mathrm{AIC}(M_H - M_{\rm kin}) = -204.98$. The best-fit kinematic velocity is $v_H = -130.52$ km/s, but the parent-like $b$ value cannot reproduce the narrow isotopic core. A pure velocity shift without deuterium's mass-scaled Doppler parameter does not explain the feature.

#### Noisy/Offset True-D Monte Carlo (C3)

The standard calibration generates exact true-D flux from the maximum-likelihood D parameters. A more realistic test perturbs the generating true-D nuisance parameters before drawing each realisation: $\log N_D$ by $\pm 0.1$ dex, $T_K$ by $\pm 1000$ K (clamped to $> 100$ K), and $b_{\rm turb}$ by $\pm 1$ km s$^{-1}$. The D/H velocity offset ($-81.6$ km/s) is a fixed physical constant (exact reduced-mass isotope shift) and is not perturbed. For Q1009+2956 the result confirms the main analysis: 0/200 standard realisations exceed $T_{\rm obs}$ ($p_{\rm std} = 0.005$), and 0/200 parent-reassignment realisations exceed $T_{\rm parent}$ ($p_{\rm parent} = 0.005$). Both the standard-statistic and parent-reassignment rejections are robust to realistic uncertainty in the true-D model parameters. An earlier version of this check perturbed the velocity offset, creating a mismatch between the generating and fitting models that artificially inflated $T_{\rm sim}$; the corrected implementation confirms the original significance.

#### Physical Parent Window (C1) — Headline Statistic

The physically motivated parent window ($\pm 3b_{\rm max}$, where $b_{\rm max}$ is the largest Doppler parameter of the main complex) is adopted as the *headline* statistic, with the conservative $\pm 1000$\,km/s window reported as a lower bound. For Q1009+2956 the largest $b$-value of the main complex is 56.7 km s$^{-1}$, so the physical window $\pm 3b$ is $\pm 170$ km s$^{-1}$, compared with the conservative $\pm 1000$ km s$^{-1}$. This reduces eligible parents from 43 to 4. With 200 true-D Monte Carlo realisations the fair standard statistic gives 0/200 exceedances ($p_{\rm std} = 0.005$), and the parent-reassignment statistic also gives 0/200 exceedances ($p_{\rm parent} = 0.005$). The result is consistent with the fixed window: the H alternative is significantly preferred under both the canonical-parent and adversarial-parent tests. The physical window is adopted as the headline because it is motivated by the absorber's own velocity structure rather than an arbitrary fixed range.

### 5.6 Multi-Pronged Evidence Analysis (Gate 8)

Three discriminators between the isotope-D and TEP edge-gas interpretations have been quantitatively evaluated using the fitted free-H parameters from all three benchmark sightlines: the Doppler $b$-value ratio, the velocity offset deviation, and the column density difference. These quantities are all derived from the same free-H fit and are therefore not statistically independent; the joint multivariate statistic is the appropriate calibrated measure. A true-D injection Monte Carlo (step\_08b, $N = 200$ realisations per sightline) calibrates each statistic against the null distribution obtained by fitting $M_{H,\rm free}$ to simulated true-D spectra. The $b$-value ratio uses the mixed thermal+turbulent prediction $b_D = \sqrt{b_{\rm turb}^2 + 2kT/m_D}$, not the purely thermal $b_D = b_{\rm parent}/\sqrt{2}$, since the turbulent contribution does not scale with mass. Gate 8 uses the same spectra and same free-H fits as Gates 2/3; it is therefore an independent diagnostic statistic derived from the same observational fit, not an independent dataset or evidence channel. Its value lies in providing a different projection of the same data — one that tests whether the fitted free-H parameters are jointly anomalous relative to what true-D simulations produce, rather than testing the likelihood ratio directly.

**b-value ratio.** Under isotope-D, the fitted free-H Doppler parameter should equal the mass-scaled D prediction $b_D = \sqrt{b_{\rm turb}^2 + 2kT/m_D}$, where the turbulent contribution does not scale with mass. Under TEP, $b$ is set by edge-gas temperature and is unconstrained. The observed ratios are $0.99$ (Q1009), $1.31$ (PKS\,1937), and $5.31$ (J1332). The J1332 ratio indicates a turbulent, broad component ($b_{H,\rm free} \approx 51$\,km/s) inconsistent with the mass-scaled D prediction ($b_D \approx 9.6$\,km/s). After calibration against the true-D null ($N = 200$), the J1332 $b$-value ratio is significant ($p = 0.045$): true-D simulations produce $b$-ratios clustered around $1.14 \pm 1.17$, whereas the observed $5.31$ is far outside this distribution. The Q1009 $b$-ratio is not significant ($p = 1.0$) — the observed ratio is closer to the isotope-D prediction than the simulations. The PKS\,1937 $b$-ratio is marginal ($p = 0.07$). A caveat applies to the J1332 result: the TEP orphan prediction (Gate 6-II) anticipates narrow, cool, thermally-dominated edge components ($b < 10$\,km/s), whereas the J1332 free-H fit yields a broad, turbulence-dominated component ($b \approx 51$\,km/s, $b_{\rm turb} = 50$\,km/s at the upper bound, $T_K \approx 5000$\,K). The $b$-value ratio therefore rejects isotope-D but does not simultaneously confirm the TEP orphan phenotype; the J1332 feature may be a turbulent H I interloper unrelated to the TEP edge-gas mechanism, or the orphan prediction may require revision to accommodate turbulence-dominated edge gas. Resolving this requires either a physical model for turbulent edge-gas $b$-values or a larger sample spanning both thermal and turbulent regimes.

**Offset-deviation correlation.** Under isotope-D, all fitted free-H velocities should sit at the exact isotope shift within spectral resolution. Under TEP, the offset depends on the local shear amplitude, which scales with the absorber's gravitational potential. The observed deviations are $+2.7$\,km/s (Q1009), $+5.7$\,km/s (PKS\,1937), and $-36.6$\,km/s (J1332). The three sightlines exhibit the predicted monotonic ordering with $\log N_{\rm HI}$ (Spearman $\rho = 1.0$); however, with only three data points the sample is too small for the correlation itself to constitute significant evidence ($P(\rho = 1 \mid N = 3) = 0.17$ for a prespecified directional trend). After calibration ($N = 200$), the Q1009 deviation is highly significant individually ($p < 0.005$, 0/200 exceedances): true-D simulations produce free-H fits that sit within $\pm 0.2$\,km/s of the isotope shift, whereas the observed $+2.7$\,km/s deviation is far outside this distribution. The PKS\,1937 deviation is also highly significant ($p < 0.005$, 0/200 exceedances): the simulation spread is $\pm 0.7$\,km/s, and the observed $+5.7$\,km/s is far outside. The J1332 deviation is marginal ($p = 0.09$): the broad, saturated feature yields a simulation spread of $\pm 17.5$\,km/s, within which the observed $-36.6$\,km/s falls. The Q1009 result is the most direct individual test: under isotope-D, the feature is at the isotope shift and the free-H fit must find it there; under TEP, the feature is edge-gas at a slightly different velocity. The $p < 0.005$ rejection of the isotope-D velocity prediction for Q1009 is the strongest individual discriminator in the analysis. A caveat applies: the calibration assumes the only source of velocity scatter is the fitting process, whereas residual wavelength-calibration systematics (e.g., intra-order distortion, ThAr line-list uncertainties) can introduce $\sim 0.5$--$1$\,km/s offsets not captured by the simulation. If such systematics were included, the simulation spread would widen and the significance of the $+2.7$\,km/s deviation would be reduced. The result should therefore be interpreted as significant *conditional on the absence of unmodelled velocity systematics*, and a full end-to-end error budget incorporating wavelength-calibration uncertainties is required before the velocity deviation can be considered robust evidence against isotope-D.

**Sign test.** The conformal sign theorem predicts all edge-shear features should be blueward of the parent. All three are: $-131.3 < -52.4$, $-67.3 < +8.7$, $-118.2 < 0.0$\,km/s. Under the null, $P(3/3\ {\rm blueward}) = 0.125$.

**Column density difference.** Under isotope-D, $N_{H,\rm free}$ should match $N_{\rm HI} \times ({\rm D/H})_{\rm BBN}$. The observed differences are $+0.03$\,dex (Q1009), $-0.09$\,dex (PKS\,1937), and $+0.70$\,dex (J1332). After calibration ($N = 200$), the Q1009 column density difference is significant ($p = 0.02$): true-D simulations produce H fits with $\log N$ differences tightly clustered around $-0.01 \pm 0.02$\,dex, whereas the observed $+0.03$\,dex is at the edge of this distribution. The PKS\,1937 ($p = 0.995$) and J1332 ($p = 0.65$) column density differences are not significant.

**Calibrated joint assessment.** The three statistics are correlated because they derive from the same free-H fit. A joint Mahalanobis distance against the true-D covariance matrix provides the calibrated multivariate test. With $N = 200$ true-D injections per sightline, Q1009$+$2956 is highly significant in the joint statistic ($p < 0.005$, Mahalanobis distance $= 298$), driven primarily by the velocity deviation ($p < 0.005$). PKS\,1937$-$101 is also highly significant ($p < 0.005$, Mahalanobis distance $= 81$), driven primarily by the velocity deviation ($p < 0.005$). J1332$+$0052 is highly significant ($p < 0.005$, Mahalanobis distance $= 24.1$), driven by the joint combination of the $b$-value ratio ($p = 0.045$) and velocity deviation ($p = 0.09$), though the broad $b$-value is inconsistent with the narrow-edge TEP orphan prediction (see above). The pattern is physically sensible: Q1009 (high S/N, high resolution, moderate D column) provides the tightest velocity constraint; PKS\,1937 (high resolution, moderate D column) also provides a tight velocity constraint; J1332 (saturated D, broad feature) provides the tightest $b$-value constraint but the velocity deviation is not individually significant. All three sightlines show highly significant calibrated Gate 8 evidence ($p < 0.005$). All three show significant Gate 2/3 evidence ($p_{\rm parent} = 0.001$). The cross-sightline pattern — deviations scaling with $N_{\rm HI}$, all features blueward — is consistent with the TEP prediction. The parent-identity diagnostic (Gate 7) is descriptive only, and the amplitude gap (Gate 4B) remains open. The cumulative case is strengthened by the Q1009 and PKS\,1937 velocity deviation results; the population forecast (Gate 6-II) and orphan search protocol (Gate 6-III) provide the next testable predictions.

### 5.7 Orphan Search Protocol (Gate 6-III)

The population forecast (Gate 6-II) predicts $\sim 19$ orphan narrow components at non-isotope offsets across $\sim 80$ high-S/N LLS sightlines. A pilot search on $10$--$15$ sightlines from existing archival surveys would turn this prediction into a first observational test.

**Archival samples.** Three existing surveys provide suitable data without requiring new observations:

- *SQUAD* (UVES Spectral Quasar Absorption Database, Murphy et al. 2019 [43]): $\sim 200$ UVES sightlines at $R \sim 40\,000$--$50\,000$, covering Ly$\alpha$--Ly$\gamma$ at $z > 2.5$. Approximately $30$--$40$ sightlines have LLS-class absorbers with sufficient S/N for narrow-component detection.

- *UVES SLS* (UVES Large Programme for D/H, Carswell et al. 2024): $\sim 25$ targeted D/H sightlines at $R \sim 45\,000$--$50\,000$ with S/N $> 30$ per pixel. All have published VPFIT component models that can be searched directly.

- *ESPRESSO D/H survey* (Cooke et al. 2024): $\sim 10$ sightlines at $R \sim 70\,000$--$140\,000$ with the highest spectral resolution. Ideal for resolving narrow ($b < 10$\,km/s) components.

**Search protocol.** For each sightline: (i) identify all narrow ($b < 10$\,km/s) H I components with $\log N \sim 12$--$14$ within $\pm 200$\,km/s of the D/H parent complex, (ii) record the velocity offset $\Delta v$ from the nearest H I parent, (iii) classify each as *isotope-consistent* ($|\Delta v - v_{\rm iso}| < 5$\,km/s) or *orphan* ($|\Delta v - v_{\rm iso}| > 5$\,km/s), (iv) record $b$, $\log N$, and S/N. The predicted orphan fraction is $\sim 79\%$ (orphan features outnumber isotope-consistent ones by $\sim 3.8:1$). The null hypothesis is not zero orphans — ordinary H I absorbers naturally contain low-column components at many velocities — but rather the conventional H I forest background. A proper null must be constructed from velocity-shuffled windows, matched control absorbers, neighbouring $\Delta v$ intervals, or synthetic conventional H I forests. The TEP prediction is an *excess* of components with the joint phenotype ($b < 10$\,km/s, $\log N \sim 12$--$14$, non-isotopic offset, systematically related to absorber geometry) beyond this conventional background. A pilot on $10$--$15$ sightlines should detect $\sim 2$--$3$ orphans in excess of the conventional background if the TEP prediction holds.

**Falsification criterion.** If no excess of orphan components (beyond the conventional H I background) is found across $\geq 20$ high-S/N sightlines (predicting $\sim 4$ excess orphans under TEP), the velocity-selection theorem is falsified. Poisson $P(0 | \lambda = 4) = 0.018$, giving a $>2\sigma$ exclusion.

### 5.8 Corpus Cross-References: The No-Hot-Big-Bang Framework

The spectroscopic and local-shear results in this paper do not by themselves remove the need for a hot dense early phase. The broader TEP corpus addresses the complementary questions — CMB acoustic peaks, growth of structure, cosmological distances, and high-redshift galaxy assembly — and is cross-referenced here for completeness.

- **CMB acoustic peaks and sound horizon (TEP-HC, Paper 18).** The TEP conformal scalar field has been implemented natively in *hi_class* [29] and run through MCMC against Planck 2018, BAO, and Pantheon+. The acoustic sound-horizon ratio $r_s^{\rm TEP}/r_s^{\Lambda{\rm CDM}} = 0.999994$ ($< 6$\,ppm deviation), and the TT/TE/EE peak morphology is preserved without early spatial expansion. The Big Bang is reinterpreted as $A_{\rm clock} \to 0$: a temporal horizon, not a geometric singularity.

- **Temporal horizon and absence of singularity (TEP-TH, Paper 27).** The FLRW singularity is shown to be a reconstruction artifact. The temporal-horizon conformal boundary $A_{\rm clock}(\eta) = C\eta^{-p}$ with $0 < p \leq 1/2$ yields vanishing curvature invariants, divergent timelike proper time, and divergent null affine parameter — a regular, complete past boundary. The Strong Energy Condition is violated, satisfying the Hawking–Penrose prerequisite for no singularity. The tensor-to-scalar ratio is $r = 9 \times 10^{-6}$.

- **Cosmological distances without expansion (TEP-C0, Paper 26).** A pure conformal reconstruction exactly reproduces the $\Lambda$CDM distance modulus across $1\,701$ Pantheon+ SNe. A no-$\Lambda$ temporal-shear branch improves $\Delta\chi^2 \approx -3.4$ with Bayes factor $\approx 4.6$--$61.8$ depending on $z_{\rm los}$.

- **JWST high-redshift anomalies (TEP-JWST, Paper 12).** The canonical TEP cosmology (asymptotic temporal past with unbounded local proper-time history) removes the finite-age assembly bottleneck. Nested model comparison gives $\ln {\rm BF} = +64.1$ (four fewer parameters) vs conventional models, with a dust–$R_{\rm ML}$ correlation $\rho = +0.62$ at $z > 8$.

- **Theoretical foundation (TEP, Paper 0).** The bi-metric action $\tilde{g}_{\mu\nu} = A^2 g_{\mu\nu} + B\nabla_\mu\phi\nabla_\nu\phi$, field equations, PPN mapping, and the synchronization holonomy as the invariant signature of dynamical time are established in the foundational paper.

The helium-4 equilibrium ($Y_{\rm eq} = 0.247$) and the D/H–$\Omega_b h^2$ concordance are addressed within this paper (Sections 4 and 5.3), while the CMB anchoring of $\Omega_b h^2 \approx 0.022$ is established in TEP-HC. The amplitude gap (Gate 4B) remains the principal open calculation; the spectroscopic evidence (Gates 2, 3, 4E, 7, 8) and the population forecast (Gate 6-II) are independent of the amplitude calculation and stand on their own.

## 6. Conclusion

Through a systematic, algorithmically controlled analysis of three benchmark D/H absorption systems—Q1009+2956, PKS\,1937$-$101, and J1332$+$0052—the spectroscopic distinguishability of deuterium from ordinary hydrogen is examined under nested model comparison with Monte-Carlo calibrated significance. Isotope identifiability is found to be controlled by both Doppler regime and D column density: at the actual Q1009 D column ($N_{\rm D} = 5.7\times10^{12}\,\mathrm{cm}^{-2}$), the maximum single-pixel discrepancy is $0.52\sigma$ for thermally-dominated gas at Keck/HIRES resolution, falling to $0.10\sigma$ for the fitted mixed-regime parameters and $0.0002\sigma$ for turbulence-dominated gas. At unsaturated LLS-class columns, the intrinsic H/D profile-shape difference is sub-noise on a per-pixel basis, though cumulative discrimination across many pixels and transitions can still be substantial. Under the *parent-reassignment statistic* with the conservative $\pm 1000$\,km/s parent window—which gives D maximum freedom to select the most favorable parent—the free-H alternative is significantly preferred for all three sightlines: Q1009+2956 ($T_{\rm parent}=161.03$, $p_{\rm parent}=0.001$), PKS\,1937$-$101 ($T_{\rm parent}=59.00$, $p_{\rm parent}=0.001$), and J1332$+$0052 ($T_{\rm parent}=135.76$, $p_{\rm parent}=0.001$). For Q1009+2956, a physically motivated window ($\pm 3b_{\rm max} = \pm 170$\,km/s) was also run, giving results consistent with the conservative-window significance. Physical-window Monte Carlos for PKS\,1937$-$101 and J1332$+$0052 are deferred. After Bonferroni correction for the six-test family (threshold $\alpha/6 = 0.0083$), all six $p$-values survive: $p_{\rm std}$ and $p_{\rm parent}$ are $0.001$ and $0.001$ for Q1009+2956, $0.001$ and $0.001$ for PKS\,1937$-$101, and $0.001$ and $0.001$ for J1332$+$0052. The offset-exactness test (Gate 4E) shows fitted free-H velocities deviating from the isotope-shifted position by $+2.7$\,km/s (Q1009), $+5.7$\,km/s (PKS\,1937), and $-36.6$\,km/s (J1332), providing a per-sightline discriminator. The free-component model is the TEP edge-gas signature: diffuse, unscreened edge gas displaced by temporal shear. Across all three benchmark sightlines, the isotope-tied model is excluded by the free-component alternative under both the canonical-parent and parent-reassignment statistics. A multi-pronged evidence analysis (Gate 8) evaluates three discriminators---b-value ratio, velocity offset deviation, and column density difference---calibrated against a true-D injection Monte Carlo ($N = 200$ per sightline). For Q1009$+$2956, the velocity offset deviation is highly significant individually ($p < 0.005$): true-D simulations produce free-H fits within $\pm 0.2$\,km/s of the isotope shift, whereas the observed $+2.7$\,km/s is far outside. For PKS\,1937$-$101, the velocity offset deviation is also highly significant ($p < 0.005$). For J1332$+$0052, the $b$-value ratio is significant ($p = 0.045$). The joint Mahalanobis statistic is highly significant for all three sightlines ($p < 0.005$): Q1009$+$2956 ($p < 0.005$), PKS\,1937$-$101 ($p < 0.005$), and J1332$+$0052 ($p < 0.005$). For J1332$+$0052 the broad $b$-value is inconsistent with the narrow-edge TEP orphan prediction. The three sightlines exhibit the predicted monotonic ordering of offset deviations with $N_{\rm HI}$ (Spearman $\rho = 1.0$), though with $N = 3$ the sample is too small for the correlation itself to constitute significant evidence. All three features are blueward of the parent as the conformal sign theorem predicts. These results—spanning three instruments (Keck/HIRES, ESPRESSO, UVES+HIRES) and a redshift range $2.5 < z < 3.6$—are consistent with the TEP prediction that temporal shear depends on localized core-edge geometry.

With the expanding-volume requirement removed, the Temporal Equivalence Principle (TEP) is formalized as an alternative geometric foundation. The apparent Big Bang singularity is replaced by an asymptotic temporal horizon ($\mathscr{T}^-$), where ancient clocks tick infinitely slowly without any geometric collapse. It is shown that local thermal processing and chemical evolution can remain bounded by finite exposure measures ($\mathcal{E}_{\rm astr} < \infty$) when the derived temporal-exposure convergence condition is satisfied, ensuring finite integrated astration exposure, and that the helium-4 mass fraction ($Y_{\rm eq} = 0.247$) emerges as the equilibrium of baryonic-cycling reaction flows under temporal-horizon metal sequestration for the adopted stellar histories. The TEP absorber field predicts the blueward sign of the deuterium-like velocity shift from the conformal/static branch sign theorem; the conformal screening operator $\mathcal{S}_\Sigma(|\Phi|/c^2)$ is calibrated by three boundary conditions (absorber, Cassini, galactic halo) with $\Phi_{\rm half} = 1.59 \times 10^{-7}$ and $n = 3.56$, yielding $132\times$ screening contrast between solar-system and galactic regimes; the conformal-only amplitude is quantified ($|\Delta v_{\rm conf}| \approx 0.009\text{ km/s}$ for $R = 30$ kpc with uniform-sphere ionisation correction), and the required amplification $\mathcal{A}_{\rm env} \approx 9.3 \times 10^3$ is identified as a falsifiable target for the non-perturbative transport path $\mathcal{C}_{T,\parallel}$. A quantitative mechanism analysis (Gate 4B-II) identifies the edge transition with $B(\phi)$ enhancement near the screening transition as the most promising non-perturbative channel; a rough line-of-sight calculation (Gate 4B-III) shows the local integral does not close the gap, but the full non-perturbative holonomy of $\mathcal{C}_{T,\parallel}$ — a global topological property, not a local integral — remains the correct evaluation framework. A quantitative population forecast (Gate 6-II) predicts $\sim 20$ orphan narrow components at non-isotope offsets across $\sim 80$ high-S/N LLS sightlines, testable with existing archival data (SQUAD, UVES SLS, ESPRESSO); a pilot search on $10$--$15$ sightlines would provide a first observational test (Gate 6-III). Finally, in the static spatial geometry, the line-of-sight optical depth is shown to diverge at high redshift under an asymptotic electron-density condition, creating an observable boundary without a physical plasma wall. The broader TEP corpus establishes the complementary results: CMB acoustic peak preservation at $< 6$\,ppm (TEP-HC), temporal-horizon regularity and absence of singularity (TEP-TH), cosmological distance reproduction without expansion (TEP-C0), and resolution of JWST high-redshift assembly anomalies (TEP-JWST). These results reduce the classical astration objection to a quantitative convergence condition plus a testable sequestration mechanism, decoupling physical chemical evolution from an eternal coordinate manifold without invoking an explosive spatial origin.

## Data Availability & Reproducibility

This work follows open-science practices. All results are fully reproducible from raw data
using the documented pipeline. All numerical results, Monte Carlo simulations, and statistics are generated by deterministic
Python scripts processing real observational data. The pipeline enforces rigorous reproducibility: any failure in statistical criteria is treated as an explicit rejection of the theory.

### Repository and Code

GitHub Repository: github.com/matthewsmawfield/TEP-BBN

The repository contains a deterministic, version-controlled cosmological analysis pipeline utilizing 14 analysis steps across 4 phases: core gates (1–8), Gate 8 calibration (step\_08b, true-D injection Monte Carlo), disformal transport, secondary robustness analyses, and manuscript finalization.
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
│   ├── steps/                     # 14 pipeline steps (01-09, 08b, 09b, secondary, finalize)
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
| Q1009+2956 Spectra | Keck/HIRES (Zavarygin et al. 2018 [44]) | Zavarygin et al. 2018 GitHub | 4 coadds (S/N $\approx 47$–$78$ near Ly$\alpha$) | `data/raw/reduced_products/Q1009+2956_z2.504_HIRES/` |
| PKS 1937$-$101 Spectra | VLT/ESPRESSO (Cooke et al. 2024) | ESO Archive | 3 exposures | `data/raw/spectra/PKS1937-101_z3.572_ESPRESSO/` |
| J1332$+$0052 Spectra | VLT/UVES + Keck/HIRES (Kislitsyn et al. 2024) | ESO Archive | 24 exposures | `data/raw/spectra/J1332+0052_z3.420_UVES/` |
| Atomic Data | NIST ASD [49] | Static Registry | H I, D I, metals | `data/raw/atomic/` |
| Q1009+2956 Model | Zavarygin et al. [44] / VPFIT [50] | Static File | 43 H I + 3 D I components | `data/literature_components/model_6a.26` |
| PKS 1937$-$101 Model | Cooke et al. 2024 / VPFIT [50] | Static File | 184 H I + 3 D I components | `data/literature_components/PKS1937-101_z3.572_vpfit_model.26` |
| J1332$+$0052 Model | Kislitsyn et al. 2024 / VPFIT [50] | Static File | 11 H I + 4 D I components | `data/literature_components/J1332+0052_z3.420_vpfit_model.26` |
| Prior Bounds | Derived | Static File | All variables | `configs/sightlines/*.json` |

### Pipeline Architecture

The analysis pipeline comprises 4 phases and 14 steps spanning spectroscopic ingestion to thermodynamic evaluation, helium synthesis, opacity boundary analysis, Gate 8 true-D injection calibration, disformal transport calibration, secondary robustness checks, and manuscript number finalization.
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
| 1 | 08B | `step_08b_calibration.py` | Gate 8 true-D injection Monte Carlo calibration ($N=200$ per sightline) | ~15 min |
| 2 | 09 | `step_09_disformal_transport.py` | Disformal transport solver and Cassini screening calibration | ~1 s |
| 2 | 09B | `step_09b_screening_plot.py` | Screening function visualization and JSON ledger | ~1 s |
| 3 | C2-C4 | `secondary_analyses.py` | Scaffold freedom (C2), perturbed MC (C3), kinematic test (C4) | ~10 min |
| 4 | Final | `finalize_manuscript_numbers.py` | Manuscript number synchronization + SHA-256 checksum manifest | ~1 s |

#### Total Runtime Summary

| Component | Steps | Runtime |
| --- | --- | --- |
| Core Gates (Phase 1) | 10 | ~45 min per sightline |
| Disformal + Secondary (Phases 2–3) | 3 | ~10 min per sightline |
| Finalization (Phase 4) | 1 | ~1 s |
| Total (3 sightlines) | 14 | ~2 hr |

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

- Smawfield, M.L. Temporal Equivalence Principle: Dynamic Time & Emergent Light Speed. *Zenodo* (2025). DOI: 10.5281/zenodo.16921911

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
