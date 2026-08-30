# Cosmological Voids vs Temporal Shear: An Empirical Falsification of Kinematic Hubble Tension Solutions
**Matthew Lukin Smawfield**
Version: v0.2 (Valencia)
First published: 29 August 2026 · Last updated: 30 August 2026
DOI: 10.5281/zenodo.22150139

---

## Abstract

The Hubble tension admits fundamentally different interpretations: a physical expansion rate inflated by local kinematics (e.g., a Gpc-scale underdensity), or an operational redshift-distance calibration artifact. This paper tests the kinematic void hypothesis against the Temporal Equivalence Principle (TEP), which models cosmological redshift as accumulated temporal shear on a static spatial manifold. Using the matched $z \ge 0.05$ submatrix of the native Pantheon+ STAT+SYS covariance, the published KBC/MOND gradual-decay profiles are decisively rejected ($\Delta\chi^2 > 100$). A calibration-independent ratio $R_H = 1.009 \pm 0.006$ excludes the predicted 5% decline at $8.4\sigma$, falsifying the kinematic void solution. The residual evidence supports TEP. An exploratory fit to pre-standardization Pantheon+ residuals has an interior optimum at $L_T=55.6$ Mpc along the pre-specified CF4 axis. The scale remains subject to the coherence-scale look-elsewhere cost and is not independently distinguished from its $1/r$ asymptote by CF4. However, the identified coherence scale places the characteristic structure in the tens-of-Mpc local-environment regime rather than the Gpc scale required by the KBC void. Because the standard rest-frame time mapping used by SALT3 implicitly assumes that the spectroscopic redshift fully accounts for the transformation between observed and emitted light-curve timescales, aggregate SALT3 standardization attenuates the pre-standardization directional signal by about 70%, consistent with partial absorption of a temporal contribution. The underlying temporal shear instead manifests locally: host-galaxy systemic redshifts are weighted toward deeper central potentials than disk standard candles, artificially contracting rest-frame timescales. Consequently, Cepheid distances are systematically shorter than TRGB distances within the same galaxies ($2.39\sigma$ directional preference), and single-galaxy Period-Luminosity gradients within M31 ($3.65\sigma$) and the LMC ($3.30\sigma$) detect the predicted clock-rate differential. The Hubble tension is an observing-chain artifact driven by localized temporal topology.

Keywords: Hubble tension, Temporal Equivalence Principle, isochrony violation, Cepheid variables, TRGB, KBC void, MOND, bulk flow, CosmicFlows-4, JWST, Pantheon+, scalar-tensor theory, distance ladder, cosmology

## 1. Introduction: The Hubble Tension and the Crisis of ΛCDM

The Λ cold dark matter (ΛCDM) standard model of cosmology confronts one of the most serious empirical and theoretical challenges in its history. Foremost among the anomalies is the Hubble tension: a statistically significant discrepancy between the locally inferred expansion rate, $H_0$, measured via the late-universe distance ladder, and the global expansion parameter inferred from the cosmic microwave background (CMB). While the Planck CMB analysis (Planck Collaboration 2020) gives $H_0 = 67.4 \pm 0.5\ {\rm km\,s^{-1}\,Mpc^{-1}}$, direct local measurements anchored by Cepheid variables and Type Ia supernovae (SNe Ia) consistently yield $H_0 = 73.0 \pm 1.0\ {\rm km\,s^{-1}\,Mpc^{-1}}$. This divergence is now reported above $5\sigma$, and above $7\sigma$ in some joint analyses with secondary anomalies, implying that the local Universe appears to be accumulating temporal shear — interpreted in standard cosmology as metric expansion — roughly 8% faster than the background $\Lambda$CDM prediction.

The persistence of this tension, despite the advent of high-resolution data from the James Webb Space Telescope (JWST), strongly suggests that the discrepancy is not an artifact of observational systematics but rather a profound physical anomaly requiring new physics. A convincing resolution must therefore move beyond isolated critique and propose a cohesive, multi-scale framework. Proposed solutions fall into two classes: early-time solutions (modifying pre-recombination physics to alter the CMB sound horizon) and late-time solutions (introducing local inhomogeneities or modified gravity in the low-redshift universe).

### 1.1 Expansion-History Solutions and the TEP Alternative

Early- and late-time solutions both retain physical metric expansion and attempt to alter some portion of its inferred history. TEP changes the premise itself. It interprets the cosmological redshift–distance relation as the observational signature of an evolving proper-time field on a static spatial manifold. Accordingly, $H_0$ is retained in this paper as an operational observable, not as a fundamental expansion rate.

### 1.2 Three Competing Interpretations

Three major frameworks offer fundamentally different interpretations of the tension:

The kinematic void framework, recently advanced by Mazurenko, Banik, Kroupa, and Haslbauer (2024), proposes that the Milky Way resides within a massive Gpc-scale local underdensity—the Keenan-Barger-Cowie (KBC) supervoid—and that gravitationally induced outflows from this void, operating under Milgromian dynamics (MOND), inflate the locally inferred recession velocities. This model simultaneously addresses the Hubble tension and the anomalous bulk flows observed in the CosmicFlows-4 catalog.

The standard ΛCDM framework attributes the residual discrepancy between Cepheid-based and alternative distance indicators to photometric systematics, subsample selection biases, and statistical weighting effects, arguing that the tension is partially or fully illusory when these are properly accounted for.

The Temporal Equivalence Principle (TEP) framework, developed in the companion series of papers (Smawfield 2025--2026), identifies a fundamental measurement bias in how classical Cepheid variable stars transport distance calibrations across varying gravitational environments. Under TEP, proper time is a dynamical scalar field that couples to the local gravitational potential, relaxing the Isochrony Axiom. Crucially, TEP replaces metric expansion with conformal temporal shear ($1+z = A_0/A_{\rm em}$ on a static spatial manifold; Smawfield 2025, 2026c). In this paper, standard FLRW expansion parameters ($H_0$, $cz$) are retained strictly as the conventional operational coordinates necessary to test competing models on their own terms. This produces an environment-dependent clock bias in Cepheid periods that is absent from distance indicators whose primary observable contains no analogous rest-frame timescale transport, including TRGB and JAGB.

### 1.3 The Central Diagnostic: Indicator-Specific Distance Divergence

A fundamental requirement of any purely kinematic resolution is the uniform scaling of all local photometric distance indicators. If galaxies are assumed to be physically receding faster than the background Hubble flow—whether due to a local void or any other kinematic mechanism—every standard candle should yield the same inflated $H_0$, because the physical recession velocity is independent of the method used to measure the distance. The kinematic void model therefore predicts that Cepheids, TRGB stars, JAGB stars, and surface brightness fluctuations should all produce identical, high values of $H_0$ within the void.

Recent JWST calibrations report a persistent and systematic divergence between Cepheid-derived distances ($H_0 \approx 73.0\ {\rm km\,s^{-1}\,Mpc^{-1}}$) and TRGB-derived distances ($H_0 \approx 69$--$70\ {\rm km\,s^{-1}\,Mpc^{-1}}$) within the same Type Ia supernova host galaxies. If physical, this indicator-specific distance divergence is the central observational puzzle that any viable resolution must explain. A kinematic void lacks the physical machinery to produce a distance discrepancy between two stars residing in the same galaxy. The Temporal Equivalence Principle predicts precisely this divergence. Cepheids are acoustic clocks governed by the local time field, while TRGBs contain no analogous period-transport bias.

The mechanism is carried by the disformal term $B(\mathcal{X})\,\nabla_\mu\phi\,\nabla_\nu\phi$ in the Jordan-frame metric, which provides non-exact transport structure — spatial shear and synchronization holonomy — that allows the core-disk clock differential to produce a residual bias in the de-redshifting operation without generating the large conformal spectroscopic signature excluded by the core–disk line-shift bound. The bias is an observing-chain artifact, not a physical modification of stars; local stellar physics is standard. This structural property is established by the conformal cancellation argument (Section 4.5) and embedded in the scalar-tensor completion, which derives the leading environmental scaling (Section 4.6). The framework identifies a second channel through the SN light-curve stretch — a diffusion timescale that inherits an environment-dependent bias under TEP — which provides a mechanism for the long-unexplained SN Ia host-mass step and is directly testable through $X_i$-dependent Hubble residuals (Section 9).

### 1.4 Scope and Structure of This Paper

This paper delivers a statistically decisive rejection of the published KBC gradual-decay predictions against the underlying Pantheon+ distance-modulus data and native covariance, and presents two complementary supporting diagnostics that point in the same direction. The primary falsification evaluates the published KBC Method-3 $H_0(z)$ curves (digitized from Mazurenko et al. 2025, Figure 3) directly against the observed distance-modulus vector, using the unbinned native $\mu$-space likelihood with the native $1701 \times 1701$ Pantheon+ STAT+SYS release covariance, the matched $z \ge 0.05$ submatrix where appropriate, and a marginalized common zero-point. Over the model's stated validity domain ($z \ge 0.05$), the Gaussian and Exponential profiles are rejected by $\Delta{\rm AIC} = +101.5$ and $+117.1$ respectively; extending to the full Pantheon+ range strengthens the rejection to $+194.3$ and $+328.7$. The rejection is robust to digitization uncertainty at the level of the published figure ($\pm 1.0\ {\rm km\,s^{-1}\,Mpc^{-1}}$ changes $\Delta{\rm AIC}$ by only $\sim 4$ units).

Two supporting diagnostics reinforce this falsification. First, indicator-specific distance divergence: 17 of 22 galaxies with both Cepheid and TRGB distances in the CF4 catalog show Cepheid distances shorter than TRGB ($2.39\sigma$ one-sided sign test). A Xi regression gives a negative slope on the pre-specified primary analysis (TEP-H0 raw data, screened) and on the independent CF4 non-R22 subset; the CF4 full sample gives a positive slope at $2.11\sigma$, but an exclusion test demonstrates this is driven by two influential R22-matched galaxies associated with the registration-sensitive subset (M101 and NGC 5643); the differential shift is directly quantified for NGC 5643. The potential-scaling coefficient is measured by the TEP-H0 Step 44 redshift-only weighted least-squares regression in $H_0$ space at $\kappa_{\rm Cep} = (0.45 \pm 0.22) \times 10^6$ mag ($2.05\sigma$ at $\sigma_v = 150$ km/s; the endpoint-closure route of the same paper gives $0.40$–$0.365 \times 10^6$, the spread reflecting the allocation degeneracy documented there), with the joint multi-block likelihood returning $\kappa_{\rm Cep} = (0.326 \pm 0.206) \times 10^6$ mag ($1.58\sigma$, diluted by the limited potential-coordinate leverage of nearby TRGB calibrators). The strongest evidence comes from single-galaxy differential tests: internal radial Period--Luminosity gradients within M31 ($3.65\sigma$ from HST PHAT photometry, Kodric et al. 2018) and the LMC ($3.30\sigma$ from OGLE-IV) independently detect the predicted clock-gradient signal free from host-to-host peculiar velocity systematics. Second, a bulk-flow estimator audit shows that the apparent calibration-dependent excess vanishes under an $H_0$-invariant estimator, demonstrating that the conventional peculiar-velocity differential is a calibration artifact rather than independent kinematic evidence.

The analysis uses 38,053 galaxy groups from the CosmicFlows-4 catalog and the Pantheon+ sample (1,543 unique SNe for descriptive binned analyses; all 1,701 released light curves for the native covariance likelihood). The structure follows a rigorous analytical progression. Section 2 reviews the local distance ladder in the JWST era. Section 3 presents the kinematic void hypothesis. Section 4 develops the TEP framework. Sections 5--8 identify and evaluate three observables: (i) indicator-specific distance divergence (Section 5, a discriminating test), (ii) peculiar velocity calibration sensitivity (Section 6, a deterministic consequence), and (iii) the $H_0(z)$ redshift profile (Sections 7--8, the primary discriminating test). Section 9 applies the TEP correction to Pantheon+. Section 10 outlines falsification pathways. Sections 11--12 discuss the theoretical implications and conclude.

Throughout this analysis, standard classical expansion coordinates (such as $H_0$, $cz$, and FLRW distance moduli) are employed strictly as the standard operational reduction framework. This methodology allows the KBC model to be falsified on its own native coordinates without requiring the reader to adopt the global non-expanding TEP cosmology in advance. These are analysis coordinates, not TEP ontology.

The single-galaxy radial gradient tests (M31, LMC) and the full distance-ladder $H_0$ unification are established in the companion paper TEP-H0 (Paper 11; Smawfield 2026, DOI: 10.5281/zenodo.18209702). This paper focuses on observables that falsify the void model on its own terms, without duplicating the positive TEP evidence in TEP-H0. This paper therefore delivers a decisive empirical rejection of the published KBC/MOND kinematic-void family tested here. The residual data contain the signatures predicted by an environment-dependent clock bias under the Temporal Equivalence Principle.

## 2. The Local Distance Ladder in the JWST Era

The foundation of the Hubble tension depends on the accuracy of the local distance ladder. Standardizing the luminosities of Type Ia supernovae requires primary distance indicators, historically dominated by Cepheid variables. However, alternative indicators, such as the Tip of the Red Giant Branch (TRGB) and the J-region Asymptotic Giant Branch (JAGB) stars, have introduced complex secondary tensions within the local distance scale itself. Any viable resolution of the Hubble tension must directly address these discrepancies.

### 2.1 The Leavitt Law and the Classical Distance Ladder

The classical distance ladder relies on the Leavitt Law (the Period-Luminosity or P-L relation), which establishes that the intrinsic brightness (absolute magnitude $M$) of a Cepheid variable is tightly correlated with its pulsation period $P$:

\begin{equation}
M = a + b\,\log_{10} P
\end{equation}

By measuring the apparent magnitude $m$ and the pulsation period $P$, astronomers determine the distance modulus $\mu = m - M$, yielding the luminosity distance $d$:

\begin{equation}
\mu = 5\log_{10}\!\left(\frac{d}{10\ {\rm pc}}\right)
\end{equation}

This calibration anchors the peak luminosity of Type Ia supernovae (SNe Ia) in nearby host galaxies, which in turn measures the Hubble constant in the Hubble flow via $cz = H_0\,d$. The entire chain depends on the assumption that the Leavitt Law is universal—that a Cepheid with a given period $P$ has the same intrinsic luminosity regardless of the gravitational environment in which it resides. This assumption is the Isochrony Axiom, and it is precisely this axiom that the TEP framework challenges.

### 2.2 Cepheid Crowding, JWST Resolution, and Linearity Validation

For years, the primary criticism levied against the SH0ES (Supernovae, $H_0$, for the Equation of State) collaboration's measurement of $H_0 = 73.0 \pm 1.0\ {\rm km\,s^{-1}\,Mpc^{-1}}$ was the potential for unresolved stellar crowding in Hubble Space Telescope (HST) near-infrared photometry. Because Cepheids are young, massive stars, they reside in dense, star-forming regions of their host galaxies. It was hypothesized that unrecognized flux from adjacent red giant or asymptotic giant branch stars could artificially inflate the measured luminosity of distant Cepheids, leading to underestimated distances and an overestimated $H_0$.

The James Webb Space Telescope (JWST) was deployed, through programs such as GO-1685 and GO-1995, to resolve this debate by providing unprecedented angular resolution in the near-infrared. The dual-module configuration of the JWST NIRCam instrument allows for multiple standard candles to be simultaneously observed, cleanly separating Cepheid standard candles from surrounding photometric contamination. Recent JWST observations of over 1,000 Cepheids in geometric anchor galaxies, such as NGC 4258, and several SN Ia host galaxies have unequivocally validated the prior HST measurements. By using two epochs to constrain Cepheid phases and three filters to accurately remove reddening, JWST reduced the dispersion in the Cepheid Period-Luminosity relations by a factor of 2.5.

Despite this substantial gain in precision, the formal difference in mean distance measurements between HST and JWST was found to be a negligible $-0.01 \pm 0.03$ mag. This result is independent of zero-points, metallicity dependence, local crowding, and the choice of filters. Consequently, the hypothesis that unrecognized crowding in HST photometry grows with distance and is responsible for the Hubble tension is now formally rejected at $8.2\sigma$ confidence—a statistical threshold even greater than the Hubble tension itself. Furthermore, combining all measures produces the strongest constraint yet on the linearity of HST Cepheid distances, measured at $0.994 \pm 0.010$, indicating near-perfect agreement with unity and ruling out distance-dependent biases. Most recently, JWST Cycle 2 observations of the background-free SN Ia host NGC 3447 confirmed zero HST–JWST difference in a single-anchor configuration (Riess et al. 2025), further consolidating the photometric integrity of the Cepheid calibration.

This result is critical to the present analysis. The JWST validation strongly validates the HST photometry and excludes crowding at the required amplitude. The question is not whether the photometry is correct—it is—but whether the standard physical interpretation of that light (the universal Leavitt Law) is complete.

### 2.3 The TRGB and JAGB Alternative Indicators

While the SH0ES Cepheid data remains internally robust, independent distance indicators analyzed by the Chicago-Carnegie Hubble Program (CCHP) give a conflicting result. Utilizing the TRGB and JAGB methods, the CCHP has derived notably lower values for the Hubble constant. Based on recent JWST data tied to SNe Ia, the CCHP TRGB yields $H_0 = 68.81 \pm 1.79\ ({\rm stat}) \pm 1.32\ ({\rm sys})\ {\rm km\,s^{-1}\,Mpc^{-1}}$, while the JAGB yields $H_0 = 67.80 \pm 2.17\ ({\rm stat}) \pm 1.64\ ({\rm sys})\ {\rm km\,s^{-1}\,Mpc^{-1}}$. These values are highly consistent with the ΛCDM CMB predictions, which some researchers suggest negates the need for new physics.

TRGB distances rely on the core helium flash of low-mass stars, a phenomenon theoretically decoupled from the complex star-formation histories that affect Cepheids, bringing advantages of simplicity and small systematic uncertainties from extinction and metallicity. JAGB stars, which are carbon-rich variables, are valued because only single-epoch, random-phase photometry is strictly necessary to derive distances, though multi-epoch time-averaging is preferred to decrease the contribution of intrinsic variability.

The internal consistency between CCHP's TRGB and JAGB in certain nearby galaxies is notable, with a quoted RMS scatter of $\sigma_{\rm JAGB\text{-}TRGB} = \pm 0.07$ mag. Yet, broader comparisons reveal deep photometric rifts. When comparing ground-based JAGB distances to uniformly reduced space-based optical TRGB distances from HST, a highly significant offset of $\Delta\mu = 0.17 \pm 0.04\ ({\rm stat}) \pm 0.06\ ({\rm sys})$ mag emerges—representing a 9% discrepancy in distance. Inspections of HST color-magnitude diagrams suggest that the issue lies in the underlying JAGB distances. Lower resolution or photometric calibration issues in ground-based near-infrared data may be artificially compressing JAGB distances, a sharp contrast to the general agreement found between JWST JAGB and other space-based indicators such as Cepheids and Miras. In 9 out of 13 HST color-magnitude diagrams, the JAGB-implied values are visibly inconsistent with the onset of the TRGB.

### 2.4 Summary of Distance Indicator Results

*Table 1: Summary of distance indicator results in the JWST era. Four independent calibrations of $H_0$ from the local distance ladder, showing the persistent divide between Cepheid-anchored and TRGB/JAGB-anchored values.*

| Indicator | Primary Telescope | $H_0$ (km s$^{-1}$ Mpc$^{-1}$) | Tension with CMB ($\sim 67.4$) | Primary Systematics / Notes |
|---|---|---|---|---|
| Cepheids + SNe Ia | HST / JWST | $73.0 \pm 1.0$ | $>5.0\sigma$ | SH0ES; crowding rejected at $8.2\sigma$. Linearity at $0.994 \pm 0.010$. |
| TRGB + SNe Ia | JWST | $68.81 \pm 1.79$ (stat) | $<1.0\sigma$ | CCHP; relies on smaller SN subsample. Avoids star-formation bias. |
| JAGB + SNe Ia | JWST | $67.80 \pm 2.17$ (stat) | $<1.0\sigma$ | CCHP; displays $0.17$ mag offset against space-based optical TRGB. |
| IR SBF + SNe Ia | HST | $74.6 \pm 0.9$ (stat) | $>2.5\sigma$ | Garnavich et al. (2023); independent of stellar resolution, relies on passive galaxies. |

### 2.5 Sample Variance and Subsample Biases

The discrepancy between the CCHP and SH0ES results is partially driven by the specific subsamples of Type Ia supernovae selected for calibration. The SH0ES collaboration uses a robust sample of 42 local SNe Ia calibrated by Cepheids. In contrast, early JWST subsamples from CCHP used for JAGB measurements rely on only 8 to 11 SNe Ia. The CCHP excluded three hosts for JAGB measurements, leaving a set of eight SNe Ia that are demonstrably biased low with respect to the mean. A statistical selection of every unique combination of 8 SNe Ia from the original 42 SH0ES supernovae reveals that the selected JAGB sample is highly unusual, sitting in the bottom 5% of the distribution; the HST Cepheids would expect an $H_0 = 70.5\ {\rm km\,s^{-1}\,Mpc^{-1}}$ purely based on this specific subset of 8 supernovae.

Furthermore, combining JWST Cepheids, JAGB, and TRGB into a single distance-limited set of 16 SNe Ia at $D \leq 25$ Mpc yields $73.4 \pm 2.1$, $72.2 \pm 2.2$, and $72.1 \pm 2.2\ {\rm km\,s^{-1}\,Mpc^{-1}}$, respectively. When explicitly accounting for common SNe, the three-method JWST result is $H_0 = 72.6 \pm 2.0\ {\rm km\,s^{-1}\,Mpc^{-1}}$, practically identical to the $72.8\ {\rm km\,s^{-1}\,Mpc^{-1}}$ expected from HST Cepheids in those exact same galaxies. This demonstrates that when evaluated on the same galaxy samples, all standard candles point toward a high Hubble constant. The apparent tension between standard candles is partly a small-sample statistical artefact.

However, the physical mechanism underlying the indicator-specific offset in matched hosts—why Cepheids and TRGBs yield systematically different distances even when applied to the same galaxies—remains unexplained by standard cosmology. While sample variance explains part of the CCHP-SH0ES discrepancy, it cannot account for the fundamental physical difference between acoustic and non-timescale distance indicators identified by the TEP framework.

### 2.6 Supernova Host-Galaxy Mass Steps and SBF Calibration

A tertiary systematic that must be addressed is the standardization of Type Ia supernovae themselves. The luminosity of SNe Ia is empirically corrected using light-curve stretch and color parameters, often using the SALT2 fitter or hierarchical Bayesian SED models like BayeSN. The SALT2/SALT3 standardization relation is $\mu = m_B - M_B + \alpha\,x_1 - \beta\,c + \Delta_{\rm host}$, where $x_1$ is the light-curve stretch — the timescale of photospheric diffusion through the ejecta. The peak luminosity is nuclear physics; the light-curve width by which it is standardized is a clock. This distinction is central to the TEP framework (Section 9.6): under any theory in which clock rates respond to environment, SN stretch inherits an environment-dependent bias that propagates into the standardized magnitude through the $\alpha\,x_1$ term.

Even after SALT2/SALT3 standardization, a residual correlation with the host galaxy's stellar mass remains — the "mass step." Analysis of extensive SN Ia datasets, such as the JLA and RAISIN surveys, demonstrates Hubble residual steps of $\sim 0.06$–$0.1$ mag depending on whether the host galaxy mass is above or below $10^{10}\,M_\odot$. The mass step has persisted for approximately 15 years without a unique physical explanation. Section 9.6 identifies it as the observational signature of the SN light-curve stretch channel: more massive hosts reside in deeper gravitational potentials, producing a larger clock-rate differential and a correspondingly larger stretch bias. The TEP prediction is falsifiable: the step should correlate with the potential coordinate $X_i$ rather than with stellar mass per se, and the correlation should persist after the SALT3 mass correction is applied.

To bypass the star-forming complexities of Cepheid hosts entirely, researchers use near-infrared Surface Brightness Fluctuations (SBF) in early-type galaxies. SBF calibrators do not require resolving individual stars and can measure distances out to 100 Mpc while maintaining 5% precision, using massive, passively evolving host galaxies. When SNe Ia in the Hubble flow are sub-sampled to match the properties of SBF hosts (rather than Cepheid hosts), the average calibrator distance moduli vary by up to 0.03 mag, adding a 1.8% systematic uncertainty. Despite this entirely distinct galactic demographic, robust SBF calibrations still yield $H_0 = 74.6 \pm 0.9\ ({\rm stat}) \pm 2.7\ ({\rm sys})\ {\rm km\,s^{-1}\,Mpc^{-1}}$.

The synthesis of these datasets demonstrates that the most highly resolved and diverse observations consistently point to a locally inflated Hubble constant, confirming that the tension requires a structural or fundamental physical solution rather than a purely statistical one. The four indicator classes span a range of $H_0$ values (JAGB $67.80$, TRGB $68.81$, Cepheids $73.0$, SBF $74.6$), but this ordering is not advanced here as a statistical test of the framework: with $N = 4$ indicator classes the ordering is confounded with host morphology, dust content, stellar-population age, and photometric method, each of which varies jointly with calibrator-population potential depth across the four classes. A discussion of the ordering as a suggestive observation — not a formal statistical signature — is given in Section 9.7.

### 2.7 The Indicator-Specific Offset as the Key Diagnostic

Published Cepheid and TRGB calibrations exhibit indicator-dependent differences, motivating a matched-host diagnostic. When applied to matched host samples, Cepheids produce $H_0 \approx 73$ while TRGBs produce $H_0 \approx 69$. JWST has ruled out crowding at $8.2\sigma$ as the sole explanation. The offset is not purely a sample selection effect, as it persists in matched hosts, though its amplitude is strongly reduction-dependent (Section 5). It is more naturally a physical or calibration difference between two classes of standard candles that operate on fundamentally different physical mechanisms: acoustic envelope pulsation (Cepheids) versus nuclear ignition thresholds (TRGB). Section 5 tests how much of that difference survives common provenance and reduction controls.

This indicator-specific offset is the key diagnostic that distinguishes a clock-calibration bias (TEP) from a kinematic outflow (void model). A kinematic void inflates recession velocities uniformly and cannot produce a distance discrepancy between two stars in the same galaxy. The TEP framework, by contrast, predicts precisely this divergence: acoustic clocks are coupled to the dynamical time field and suffer environment-dependent period contraction, while nuclear candles contain no analogous period-transport bias. This physical distinction is developed formally in Section 4 and tested observationally in Section 5.

## 3. The Kinematic Void Hypothesis: KBC, MOND, and Bulk Flows

Having established the validity of the locally inflated $H_0$ measurement, attention now turns to the physical mechanism. If the measurement is real, the local Universe must differ from the global average. The most compelling late-time kinematic solution to the Hubble tension is the proposition that the Milky Way resides within a massive, underdense region of the cosmos known as the Keenan-Barger-Cowie (KBC) supervoid. This section presents the void hypothesis in detail, including its observational foundations, its gravitational engine (MOND), and its predictions for large-scale peculiar velocities.

### 3.1 The Keenan-Barger-Cowie Supervoid

Multi-wavelength galaxy number counts—from near-infrared to optical catalogs—provide robust, cross-spectrum empirical evidence that the local Universe at $z < 0.15$ is strongly inhomogeneous. The KBC void (Keenan, Barger & Cowie 2013) is an observed macro-structure extending radially between 40 and 300 Mpc around the Local Group, with the Milky Way located within it, though notably not at its exact center. The relative density contrast of this region, defined mathematically as $\delta \equiv 1 - \rho/\rho_0$, is measured at $\delta = 0.46 \pm 0.06$. This indicates a 46% underdensity, meaning the local Gpc-scale volume contains roughly half the matter expected from the global cosmic average.

In standard cosmology, the assumption of homogeneity implies that the Hubble parameter is constant across space at any given epoch. The local expansion relationship is given by $cz = H_0\,d$ in the local universe. However, for an observer residing within a large local void, this assumption collapses, as local kinematics decouple from the background expansion. Independent analyses of the Pantheon SN Ia sample have already searched for precisely this local void signal and ruled it out: Kenworthy, Scolnic & Riess (2019) found that local structure does not impact the measurement of $H_0$ at the level required to explain the tension. The KBC authors dispute this conclusion, arguing that the Pantheon analysis does not probe the full depth of the void at $z < 0.05$; the present paper addresses this directly by evaluating the published KBC $H_0(z)$ prediction curves over their own stated validity domain (Section 7).

### 3.2 Gravitationally Induced Outflows and Apparent H₀ Inflation

The physics of a local void fundamentally alters the locally inferred recession scale. Because the interior of the void contains significantly less mass than its edges, gravitational forces pull matter outward from the center toward the denser, unperturbed cosmological background. This gravitationally induced outflow creates a local peculiar velocity field that is superimposed directly onto the background Hubble flow.

For galaxies observed within or near the edge of the void, their total observed velocity is the sum of the assumed cosmological expansion and the outward peculiar velocity. An observer measuring these redshifts and applying standard luminosity distances will infer an artificially high local expansion rate, despite the true global background parameter remaining firmly anchored at $H_{0}^{\rm CMB} \approx 67.4\ {\rm km\,s^{-1}\,Mpc^{-1}}$.

Haslbauer, Banik, and Kroupa (2020) demonstrated mathematically that gravitationally driven outflows from a void with the KBC's specific density profile inflate apparent redshifts precisely enough to generate the $\sim 9\%$ increase in the Hubble constant observed by the SH0ES collaboration. Furthermore, semi-analytic void models generate a highly specific, testable prediction: the redshift decay profile, $H_0(z)$. The local estimate of $H_0$ must peak in the very low-redshift universe ($z < 0.15$) and then exhibit a gradual decline toward the background Planck value at higher distances. Recent observational studies defining $H_0(z)$ in narrow redshift bins show a decline toward the background value in some binning-based treatments, but the inferred $H_0(z)$ profile is estimator-dependent: other treatments of the same data, including the native $\mu$-space likelihood used below, do not recover it.

### 3.3 The CosmicFlows-4 Bulk-Flow Anomaly

A hallmark of a successful theory is the prediction of phenomena beyond its original scope. The main kinematic prediction of the KBC void model is that peculiar velocities of galaxy clusters should be substantially larger than expected within the ΛCDM framework. If matter is rapidly evacuating a 600 Mpc void, vast bulk flows should be observable across the local universe.

Watkins et al. (2023) analyzed the CosmicFlows-4 catalog, providing highly accurate measurements of the bulk flow of galaxies on scales of $100$--$250\ h^{-1}\ {\rm Mpc}$. The ΛCDM model predicts that the expected rms bulk-flow amplitude declines with increasing survey scale, as the universe becomes highly homogeneous on scales exceeding 100 Mpc. However, the CosmicFlows-4 data reveals a monotonically rising bulk-flow curve. The reported CF4 amplitude at $200\ h^{-1}\ {\rm Mpc}$ lies in significant tension with that predicted distribution, resulting in a severe $4.6\sigma$ tension with standard cosmology.

Mazurenko, Banik, Kroupa, and Haslbauer (2024) subjected their previously published semi-analytic void model to this new kinematic data. Without any post-hoc calibration to the bulk flow measurements, the void model predicted bulk flow curves in qualitative agreement with the CosmicFlows-4 observations. If the observer's vantage point is chosen to match the observed bulk flow on a scale of $50\ h^{-1}\ {\rm Mpc}$, the gravitationally driven outflows from the void replicate the anomalous high-velocity flows at $250\ h^{-1}\ {\rm Mpc}$.

This success is a component of the void model's appeal. However, Stiskalek, Desmond & Banik (2025) subsequently tested the local supervoid solution by fitting CF4 galaxy-by-galaxy distance observables directly, rather than relying on compressed bulk-flow summaries. They find preferred void sizes $\lesssim 70$ Mpc — far smaller than the fiducial HBK20 void of $\sim 600$ Mpc — and the Gaussian and Maxwell–Boltzmann cases give local $H_0 \sim 70.4$ and $70.2$, while the exponential profile is disfavoured by Bayesian evidence. They also note that the earlier Mazurenko bulk-flow analysis contained a misunderstanding that altered its conclusions. This independent result supports the central methodological point of the present paper: direct distance observables should be analyzed directly, not through compressed bulk-flow summaries that may obscure the calibration dependence identified in Section 6. The bulk-flow anomaly is a derived quantity whose significance depends critically on the distance calibrators used to compute peculiar velocities — and this dependence opens a falsification pathway that the void model does not survive.

### 3.4 Summary of Cosmological Observables

| Observable | Measurement | ΛCDM Expectation | Tension |
|---|---|---|---|
| Local expansion ($H_0$) | $73.0 \pm 1.0$ km s$^{-1}$ Mpc$^{-1}$ | $67.4 \pm 0.5$ km s$^{-1}$ Mpc$^{-1}$ | $>5.0\sigma$ |
| KBC void density ($\delta$) | $0.46 \pm 0.06$ (out to 300 Mpc) | $\delta \approx 0$ on $>100$ Mpc scales | $6.04\sigma$ |
| Joint $H_0$ + void tension | Combined probability space | Strict consistency | $7.09\sigma$ |
| Bulk flow ($200\ h^{-1}$ Mpc) | Rising velocity curve | Rapid convergence to 0 km/s | $4.6\sigma$ |

### 3.5 The Structural Tension with ΛCDM

While the KBC void resolves the Hubble tension observationally, it introduces a severe structural tension into standard ΛCDM cosmology. If mass is conserved and the initial conditions of the Universe match the nearly uniform density perturbations observed in the CMB (with extremely small initial cosmic variance), ΛCDM does not possess the gravitational mechanisms to evacuate enough matter to form a void of this magnitude within 13.8 billion years.

Cosmological simulations, such as the MXXL simulation—a massive N-body hydrodynamical run designed to model large-scale structure formation in ΛCDM—reveal the extreme statistical improbability of the KBC void. The existence of an underdensity with $\delta = 0.46$ spanning 300 Mpc generates a $6.04\sigma$ tension with the standard model. Attempting to resolve this structural tension only inverts it: diluting the void to preserve ΛCDM removes its ability to inflate local redshifts, leaving the $H_0$ anomaly entirely unexplained. When the structural impossibility of the void is combined jointly with the $5.3\sigma$ Hubble tension, the joint confidence constraint rules out the ΛCDM paradigm at a $7.09\sigma$ confidence.

This result is significant: the Hubble tension is not an isolated metric problem but a symptom of a broader failure in the standard model's structure formation timeline. However, the resolution proposed by the void framework—replacing ΛCDM with MOND-driven void formation—carries its own theoretical burdens, which are now examined.

### 3.6 MOND as the Gravitational Engine

To explain the KBC void and the associated bulk flows, structure must grow much more efficiently on scales of tens to hundreds of Mpc than the ΛCDM paradigm allows. MOND (Milgrom 1983) achieves this by modifying the Newtonian acceleration law in the ultra-low acceleration regime ($a < a_0$, where $a_0 \approx 1.2 \times 10^{-10}\ {\rm m\,s^{-2}}$). In this deep-space regime, the effective gravitational acceleration scales as the geometric mean of the Newtonian acceleration and $a_0$, leading to stronger gravitational binding and more aggressive large-scale clustering without the need for hypothetically invoked cold dark matter particles.

In the context of the KBC void, the enhanced long-range gravitational forces inherent in MOND significantly accelerate the evacuation of matter from initial underdense regions. This process evacuates deep voids from the initial CMB density perturbations well within the 13.8 Gyr age of the Universe. Crucially, MOND introduces the External Field Effect (EFE), a fundamental violation of the Strong Equivalence Principle, where the internal dynamics of a gravitational system are influenced by the background gravitational field of the larger cosmos.

Mazurenko et al. (2024) modeled the KBC void density profile against the local Hubble and deceleration parameters derived jointly from SNe Ia (at redshifts $0.023$--$0.15$), time delays in strong lensing systems, and the peculiar velocity of the Local Group relative to the CMB. They found that their best-fitting MOND model simultaneously explains all these seemingly independent observables at the $1.14\%$ significance level (reducing the discrepancy to a minimal $2.53\sigma$ tension) provided the void is embedded in a time-independent external field of $0.055\,a_0$. This represents a concrete simultaneous fit demonstrating that Milgromian dynamics can naturally resolve the Hubble tension and local structural anomalies simultaneously.

### 3.7 The Observer-Location Fine-Tuning Problem

The void model requires the Milky Way to sit remarkably close to the center of a billion-light-year underdensity. In cosmology, this introduces an observer-location fine-tuning—a tension with the Copernican Principle, the philosophical and observational pillar that Earth does not occupy a uniquely privileged or special place in the Universe. While the Milky Way is not at the exact geometric center of the KBC void, the required proximity is sufficiently close to raise serious fine-tuning concerns. A void of this size and depth, centered on the observer's location, is a statistical anomaly in itself, independent of the ΛCDM structure formation problem.

The TEP framework entirely avoids this problem. The clock bias happens locally within the deep gravitational potential wells of any massive SN Ia host galaxy. It relies on standard, ubiquitous galactic physics rather than a statistically anomalous observer location. No special location for the Milky Way is required; the effect is universal and operates wherever deep-potential galaxies are used as distance calibrators.

### 3.8 The DHOST Covariance Question

A frequent criticism of phenomenological MOND is its integration into a fully covariant, relativistic theory of gravity. To circumvent Ostrogradsky instabilities, theorists rely on disformal metric transformations mapping the Einstein-frame metric $g_{\mu\nu}$ to a physical metric $\tilde{g}_{\mu\nu}$ via a scalar field $\phi$:

\begin{equation}
\tilde{g}_{\mu\nu} = C(\phi, X)\,g_{\mu\nu} + D(\phi, X)\,\partial_\mu\phi\,\partial_\nu\phi
\end{equation}

where $X = -\frac{1}{2} g^{\mu\nu}\partial_\mu\phi\,\partial_\nu\phi$ represents the kinetic term, $C$ is the conformal factor, and $D$ is the disformal factor. By employing a degenerate kinetic matrix, one can construct Degenerate Higher-Order Scalar-Tensor (DHOST) theories that guarantee ghost-free propagation. While this addresses the field-theoretic viability of MOND, it highlights that the void model's gravitational engine requires significant additional theoretical machinery. The present paper does not depend on the detailed covariance structure of either framework; the empirical results are independent of the ghost-elimination mechanism.

## 4. The TEP Framework: Isochrony Violation and the Acoustic Clock Bias

The kinematic void hypothesis, presented in Section 3, resolves the Hubble tension by modifying the motion of galaxies. The Temporal Equivalence Principle (TEP) framework resolves it by modifying something far more fundamental: the rate at which time flows in deep gravitational potentials. This section develops the TEP scalar-tensor action, derives the isochrony violation that produces the acoustic clock bias in Cepheid variables, and shows why non-timescale distance indicators (TRGB, JAGB) avoid the analogous period-transport bias.

### 4.1 Proper Time as a Dynamical Scalar Field

In standard General Relativity, proper time is fundamentally geometric. It acts as a passive coordinate—a length measured along a worldline, dictated entirely by the background metric tensor $g_{\mu\nu}$. The Temporal Equivalence Principle promotes proper time from a passive geometrical consequence to an active, propagating physical field that dynamically couples to matter.

The framework introduces a scalar degree of freedom, $\phi(x)$, which has its own kinetic energy, potential, and equations of motion. This field can evolve, propagate, and cluster in response to the local matter distribution. In scalar-tensor language, the matter sector (Standard Model fields) couples not to the bare Einstein metric $g_{\mu\nu}$, but to a composite physical metric $\tilde{g}_{\mu\nu}$—the Jordan frame metric— modulated by $\phi$ through a disformal transformation:

\begin{equation}
\tilde{g}_{\mu\nu} = A^2(\phi)\,g_{\mu\nu} + B(\mathcal X)\,\nabla_\mu\phi\,\nabla_\nu\phi
\end{equation}

where $A^2(\phi)\,g_{\mu\nu}$ is the conformal term, which scales the overall volume and dictates how the scalar field globally stretches or compresses the fundamental clock rate, and $B(\mathcal X)\,\nabla_\mu\phi\,\nabla_\nu\phi$ is the disformal term, which couples matter to the gradients (kinetic energy and spatial variations) of the time field. Here $\mathcal X \equiv -\tfrac{1}{2}(\partial\phi)^2$ is the kinetic scalar, distinct from the astrophysical predictor $X_i$ introduced in Section 4.4. This disformal coupling introduces active temporal shear, where the rate of time depends on the dynamical flow of the scalar field itself. The metric signature is taken as $(-,+,+,+)$ throughout. In natural units ($\hbar = c = 1$), $A(\phi)$ is dimensionless and $[B(\mathcal X)] = M^{-4}$, so that the disformal term $B\,\nabla_\mu\phi\,\nabla_\nu\phi$ carries the same dimension as the metric $g_{\mu\nu}$. The scalar field $\phi$ has mass dimension one ($[\phi] = M$), consistent with a canonical kinetic term in the action. The disformal transformation maps the Einstein-frame metric to a physical metric; the full scalar-tensor Lagrangian must be constructed to avoid Ostrogradsky instabilities, as addressed in the DHOST literature (see Langlois 2019). The present paper does not depend on the detailed covariance structure of the theory; the empirical results are independent of the ghost-elimination mechanism.

*Methodological note on expansion versus temporal shear.* In the foundational TEP cosmology (Papers 0 & 30), spatial geometry is static, and the cosmological redshift $z$ represents the integrated conformal evolution of the time field along the photon path ($1+z = A_0/A_{\rm em}$) rather than physical metric expansion. Throughout this paper, classical expansion coordinates ($H_0$, recession velocity $v = cz$, and FLRW distance integrals) are employed strictly as the standard reduction framework of the Pantheon+ and CosmicFlows-4 datasets. This allows the KBC kinematic void model to be falsified on its own native coordinates without requiring the reader to adopt the global non-expanding TEP cosmology in advance.

The scalar field $\phi$ is governed by a Klein-Gordon type equation of motion sourced by the local matter distribution:

\begin{equation}
\Box\phi = \frac{\partial V(\phi)}{\partial \phi} + \frac{\partial A}{\partial \phi}\,T^{\mu}_{\ \mu} + \ldots
\end{equation}

where $T^{\mu}_{\ \mu}$ is the trace of the matter stress-energy tensor. In deep gravitational potential wells—such as the cores of massive spiral galaxies—the high matter density sources a strong local gradient in $\phi$, producing a measurable departure from the standard geometric clock rate.

### 4.2 Breaking the Isochrony Axiom

The Isochrony Axiom is the assumption that identical clocks in identical gravitational potentials tick at identical rates. This is a stronger statement than the Einstein Equivalence Principle: it requires not only that local experiments are unaffected by gravitational environment (the weak equivalence principle), but that the fundamental rate of time is uniquely determined by the metric tensor alone.

The TEP framework violates the Isochrony Axiom. Because $\phi$ is governed by a wave-like equation of motion, the local clock rate is no longer strictly bound by the classical Equivalence Principle. Two identical atomic clocks, placed in environments with identical gravitational potentials and velocities, will tick at different rates if the underlying dynamical time field $\phi$ has a different local density or gradient. The physical clock rate $\tilde{\tau}$ is determined by the local equilibrium between the background time field and the surrounding matter, meaning time can compress or dilate dynamically in deep gravitational wells (like galactic cores) beyond what standard kinematic time dilation predicts.

### 4.3 Emergent Light Speed

A consequence of a dynamical time field is the concept of emergent light speed: if the fundamental scale of proper time is a dynamical variable, the locally measured speed of light $c$ becomes a derived property rather than a fundamental background constant. Under TEP, electromagnetic waves propagate along the null geodesics of the physical metric $\tilde{g}_{\mu\nu}$, and because both the matter-clock rate and the ruler length are dynamically coupled to $\phi$, a local observer will always measure $c$. The full implications for cosmology and the varying coordinate speed of light are developed in the foundational paper (Paper 0); this paper uses only the acoustic clock bias consequence, which does not depend on the emergent light speed interpretation.

### 4.4 The Cepheid Clock Bias

The central physical mechanism by which TEP resolves the Hubble tension is the Cepheid clock bias — an environment-dependent systematic in the Cepheid distance scale arising from the differential clock-rate structure of host galaxies. Classical Cepheids are radially pulsating stars whose oscillation is driven by the $\kappa$-mechanism: a thermodynamic cycle operating in the partial ionization zones of helium and hydrogen. The pulsation period $P$ is determined by the acoustic crossing time of the stellar envelope:

\begin{equation}
P \propto \int_0^R \frac{dr}{c_s(r)}
\end{equation}

where $c_s(r)$ is the local sound speed profile. This acoustic crossing time is governed by the local proper time rate, which under TEP is modulated by the scalar field $\phi$ through the conformal factor $A(\phi)$. In gravitational bound states, $A(\phi) < 1$, slowing the rate of proper time relative to cosmic background time. The absolute matter-clock rate is defined as $r_j = (d\tilde\tau/dt)_j / (d\tilde\tau/dt)_{\rm cosmic}$, with the strict hierarchy $0 < r_{\rm core} < r_{\rm disk} < r_{\rm cosmic} \equiv 1$. No clock runs faster than cosmic background time; clocks in active-shear galactic disks are less slowed than clocks in dense nuclear cores.

The period contraction mechanism operates through two distinct channels. The first is the core-disk clock differential (Section 4.5): Cepheids reside in galactic disks at radii where the clock rate is $r_{\rm Cep}$, while the systemic spectroscopic redshift $z_{\rm spec}$ is measured from light weighted by the effective aperture/tracer. If that tracer is core-weighted, its effective clock rate satisfies $r_{\rm spec} < r_{\rm Cep}$ (the core is more strongly slowed), making $q_i^{\rm eff} < 1$ a mechanism-specific hypothesis to be tested host by host. When the observed period $P_{\rm obs}$ is corrected to the rest frame using the systemic redshift, the inferred rest-frame period is:

\begin{equation}
P_{\rm rest}^{\rm inf} = \frac{P_{\rm obs}}{1 + z_{\rm spec}}
= P_{\rm local} \cdot q_i^{\rm eff} , \qquad
q_i^{\rm eff} = q_i^{\rm clock} \cdot \mathcal{T}_i < 1 .
\end{equation}

The effective ratio $q_i^{\rm eff} < 1$ generates the observed period contraction without requiring local clocks to accelerate. The Cepheid's actual pulsation period in local proper time is unchanged; the bias enters through the redshift correction, which uses a slower clock rate for the systemic redshift than for the disk Cepheids, augmented by the parameterized transport factor $\mathcal{T}_i$ from the disformal sector (the disformal clock-ratio definition). This is the strict rule $\Delta \ln A < 0$ — gravity slows time in deeper wells — applied to the core-disk geometry, as developed in TEP-H0 (Paper 11, Section 1.3) and unified with the deuterium blueshift and high-redshift age inference bias in TEP-BBN (Paper 29).

The conformal core-disk differential (the $q_i^{\rm clock}$ channel) is bounded by spectroscopic constraints on internal line shifts (Section 4.5) and can produce a fractional effect at the $\sim 10^{-3}$ level — a factor of 10–30$\times$ below the $\sim 10^{-2}$ level needed. The dominant channel is the disformal term $B(\mathcal X)\,\nabla_\mu\phi\,\nabla_\nu\phi$, which provides the non-exact transport structure — spatial shear and synchronization holonomy — that allows the core-disk clock differential to survive the de-redshifting operation as a residual bias, without generating the large conformal spectroscopic signature excluded by the core–disk line-shift bound (Section 4.7). The disformal channel does not generate the leading conformal spectroscopic signature: it modifies spatial geometry relative to temporal geometry, so the core-disk clock comparison acquires a holonomy correction. The $q_i^{\rm eff}$ mechanism remains relevant as a tracer-dependent correction (the $q_i^{\rm eff}$ versus $X_i$ distinction, Section 5), but the amplitude budget is carried by the disformal channel. The two channels are additive and both scale with $X_i$; the present analysis does not separate them, as the fitted $\kappa_{\rm Cep}$ absorbs the combined response.

Through the Leavitt Period--Luminosity law ($M_W = a + b \log P$ with $b < 0$), the shortened inferred period alters the distance modulus. Two sign-distinct quantities must be separated: the raw bias present in the uncorrected observed modulus, and the additive correction that removes it. The period-response coefficient $\kappa_P$ governs the period contraction directly: $\Delta\log_{10}P = -\kappa_P X_i$, with $\kappa_{\rm Cep} = -b\,\kappa_P$ where $b \approx -3.26$ is the near-infrared Leavitt law slope and $X_i$ is the environmental potential coordinate. Because $b < 0$, a contracted inferred period ($\Delta\log P < 0$) yields $\Delta M = b\,\Delta\log P > 0$, so the raw modulus bias is negative: $\delta\mu_i^{\rm raw} = -\Delta M = -\kappa_{\rm Cep} X_i$. The additive correction that restores the true modulus is therefore positive: $\Delta\mu_i^{\rm corr} = +\kappa_{\rm Cep} X_i$, where $\kappa_{\rm Cep}$ is the distance-modulus channel coefficient (in mag). The positive sign of $\Delta\mu_i^{\rm corr}$ is consistent with the empirical prediction that Cepheid moduli are compressed relative to TRGB moduli and must be corrected upward.

\begin{equation}
X_i = \frac{U_i - U_{\rm ref}}{c^2}
\end{equation}

where $U_i = u_{\phi,i}^2$ is the rotation-based potential proxy with $u_\phi = V_{\rm rot}/\sqrt{2}$ the isothermal-equivalent one-dimensional velocity scale (matching the convention in TEP-H0, Paper 11), and $U_{\rm ref} = (87.165\ {\rm km\,s^{-1}})^2$ is the anchor reference potential, constructed from the weighted composite of local stellar velocity dispersions at Cepheid disk locations within the primary calibration anchors: Milky Way solar neighbourhood ($\sigma_z = 30.0\ {\rm km\,s^{-1}}$, weight 0.20), LMC stellar disk ($\sigma_{\rm disk} = 24.0\ {\rm km\,s^{-1}}$, weight 0.25), and NGC 4258 intermediate annulus ($\sigma_{\rm local} = 115.0\ {\rm km\,s^{-1}}$, weight 0.55). This form is dimensionless and ensures that $X_i > 0$ for massive hosts (deeper potentials than the anchor) and $X_i \approx 0$ for low-mass hosts near the reference potential. The TEP-VOID pipeline adopts the same potential coordinate construction as TEP-H0, with screening set to $S_i \approx 1$ for the Pantheon+ Hubble-flow regime, consistent with the TEP-H0 finding that disk Cepheids reside in the weakly screened ($S_i \approx 1$) regime.

*Anchor sensitivity.* The NGC 4258 contribution dominates $U_{\rm ref}$ (95.7%), and the adopted $\sigma_{\rm local} = 115.0\ {\rm km\,s^{-1}}$ may reflect a bulge/nuclear value rather than the disk dispersion at the Cepheid radii ($R \sim 3$–$5$ kpc, where $\sigma_{\rm disk} \sim 60$–$80\ {\rm km\,s^{-1}}$ from stellar absorption-line spectroscopy). A sensitivity analysis tests the impact: varying $\sigma_{\rm N4258}$ from 60 to $150\ {\rm km\,s^{-1}}$ changes $U_{\rm ref}$ by a factor of $\sim$5, but the maximum per-host correction $\Delta\mu_{\rm max} = \kappa_{\rm Cep} \cdot X_{\rm max}$ is preserved at $\sim 0.33 \pm 0.01$ mag across the entire range when $X_i$ is computed from the velocity-dispersion proxy ($\phi_{\rm proxy} = \sigma^2$), because $\kappa_{\rm Cep}$ and $X_{\rm max}$ scale in opposite directions. The significance of the $\kappa_{\rm Cep}$ detection ($2.05\sigma$ from redshift-only WLS at $\sigma_v = 150$ km/s) is unchanged, as it is a signal-to-noise ratio.

A note on the amplitude scale. The sensitivity analysis uses the velocity-dispersion proxy $\phi_{\rm proxy} = \sigma^2$ with the unscreened anchor $U_{\rm ref} = (87.165\ {\rm km\,s^{-1}})^2$, which gives $X_{\rm max} \approx 8.3 \times 10^{-7}$ (at NGC 976) and $\Delta\mu_{\rm max} \approx 0.33$ mag. The TEP-H0 analysis and the matrix propagation in Section 9 use the rotation-velocity proxy $u_\phi = V_{\rm rot}/\sqrt{2}$ with the anchor $U_{\rm ref} = (87.165\ {\rm km\,s^{-1}})^2$ and the screening factor $S_{\rm total}$, which gives $X_{\rm max} \approx 3.28 \times 10^{-7}$ (at M101) and $\Delta\mu_{\rm max} \approx 0.148$ mag with the same $\kappa_{\rm Cep}$. The two proxies measure different aspects of the galactic potential: $\sigma$ includes bulge dispersion and is systematically larger than $V_{\rm rot}/\sqrt{2}$ for massive spirals. The $\kappa_{\rm Cep}$ fit in TEP-H0 uses the $V_{\rm rot}$-based $X_i$, so the $V_{\rm rot}$-based $\Delta\mu_{\rm max} = 0.148$ mag is the self-consistent maximum Cepheid correction. The $\sigma$-based $0.33$ mag demonstrates anchor robustness but uses a different potential proxy and should not be compared directly to the $V_{\rm rot}$-based matrix propagation. Adopting a disk-appropriate value ($\sigma_{\rm N4258} = 80\ {\rm km\,s^{-1}}$) as the primary configuration would reduce $U_{\rm ref}$ by 49% and increase all $X_i$ by $\sim$20%, with no material change to the downstream conclusions. The weighting scheme (0.20/0.25/0.55) is inherited from TEP-H0 (Paper 11); alternative schemes (equal weights, geometric-anchors-only) likewise preserve $\Delta\mu_{\rm max}$. The anchor construction is robustly constrained by the current data; the present analysis is invariant to the weighting choice.

### 4.5 Conformal Cancellation in Frequency Transport

A careful analysis of the conformal channel reveals a fundamental geometric constraint that must be stated explicitly. In a conformally coupled theory, matter follows the Jordan-frame metric $\tilde{g}_{\mu\nu} = A^2(\phi)\,g_{\mu\nu}$ (neglecting the disformal term for the moment). Local Jordan-frame physics is standard: a Cepheid's period $P_0$ in local proper time $d\tilde{\tau}$ is the ordinary value. Under a conformal transformation, proper time intervals scale as $d\tilde{\tau} = A\,d\tau$, so frequencies (which scale as $1/d\tilde{\tau}$) transform as $\nu_{\rm obs} = \nu_{\rm emit} \cdot (A_{\rm emit}/A_{\rm obs})$, while periods transform inversely: $P_{\rm obs} = P_0 \cdot (A_{\rm obs}/A_{\rm emit})$ (times cosmological factors). The observed spectroscopic redshift measures the frequency ratio:

\begin{equation}
1 + z_{\rm spec} = \frac{\nu_{\rm emit}}{\nu_{\rm obs}}
= \frac{A_{\rm obs}}{A_{\rm emit}} .
\end{equation}

When the observed period is corrected to the rest frame using the spectroscopic redshift of the *same region*, the conformal factor cancels exactly:

\begin{equation}
P_{\rm rest}^{\rm inf} = \frac{P_{\rm obs}}{1 + z_{\rm spec}}
= \frac{P_0 \cdot A_{\rm obs}/A_{\rm emit}}{A_{\rm obs}/A_{\rm emit}}
= P_0 .
\end{equation}

The conformal channel alone produces *zero* residual bias when the tracer and the Cepheid sit at the same $A(\phi)$. A residual requires the tracer and the Cepheid to sit at *different* $A$ — the core-disk differential $q_i^{\rm clock} = r_{\rm spec}/r_{\rm Cep} < 1$ of the clock-ratio equation. But then the size of the effect is the core-disk differential of $A$, and any $A$-differential between regions also shifts every spectral line between those regions by the same fraction. Delivering $\Delta\mu \sim 0.05$–$0.10$ mag through the Leavitt slope $b \approx -3.26$ requires $\Delta\log_{10}P \sim 0.015$–$0.03$, i.e., percent-level core-disk clock-rate differentials $\Delta\ln A_{\rm core-disk} \sim 10^{-2}$. A conformal gradient of this magnitude between bulge and disk would produce internal line shifts of $\sim 3000\ {\rm km\,s^{-1}}$ — spectroscopically absurd. Galaxy spectroscopy bounds internal differentials at the $10^{-3}$ level ($\sim 300\ {\rm km\,s^{-1}}$, generously). The conformal transport channel is therefore 10–30$\times$ too small before any fitting, and a conformal gradient that large would constitute a fifth force.

This exact cancellation is not a theoretical defect; rather, it acts as a stringent mathematical filter, isolating precisely which metric term is capable of carrying the physical effect. The conformal term $A^2(\phi)\,g_{\mu\nu}$ cannot carry the bias. The disformal term $B(\mathcal X)\,\nabla_\mu\phi\,\nabla_\nu\phi$ can, for a specific structural reason: The disformal term modifies the temporal, time-space and spatial sectors of the matter metric. In the quasi-static galactic regime, the environment-dependent residual is associated primarily with the spatial-gradient and time-space structure, which supplies the geometric ingredient for the synchronization-transport correction parameterized in Section 4.8. The conformal contribution is spectroscopically bounded and subdominant; the full non-radial transport efficiency remains to be derived. To maintain focus on the empirical falsification of the void hypothesis, the formal Horndeski scalar-tensor completion, the parameterization of the transport efficiency coefficient ($\eta_P$), and the calibration-chain arithmetic are given in Sections 4.6, 4.8, and 4.10.

#### Table 2: Derived TEP Phenomenological Parameters

| Parameter | Symbol | Canonical Value | Description |
|---|---|---|---|
| Distance-modulus channel coefficient | $\kappa_{\rm Cep}$ | $(0.45 \pm 0.22) \times 10^6$ mag | Fitted directly from $H_0$-space regression (Section 6) |
| Environmental coupling strength | $\bar\epsilon_0$ | $6.39 \times 10^5$ | Fixed by $\kappa_{\rm Cep} = |b|\,\bar\epsilon_0\,\eta_P / \ln 10$ (assuming $b_H \approx -3.26$, $\eta_P = 1/2$) |
| Cepheid period shift (per host) | $\Delta P/P$ | $-0.032$ ($-3.2\%$) | $-\eta_P\,\bar\epsilon_0\,X_i$ evaluated at typical $X_i \sim 10^{-7}$ |
| Additive Cepheid modulus correction (per host) | $\Delta\mu^{\rm corr}$ | $+0.045$ mag | $+\kappa_{\rm Cep}\,X_i$ evaluated at typical $X_i \sim 10^{-7}$ (raw bias $\delta\mu^{\rm raw} = -0.045$ mag) |

### 4.6 A Scalar-Tensor Completion and Field Profile

The TEP scalar-tensor theory is constructed within the Horndeski/kinetic-braiding subclass of the Degenerate Higher-Order Scalar-Tensor (DHOST) family. The action adopted here — Einstein-Hilbert plus a kinetic scalar sector with a kinetic-braiding $\Box\phi$ coupling — lies within the degeneracy structure that eliminates Ostrogradsky ghosts, but is not the most general quadratic/cubic DHOST action. The schematic action is:

\begin{equation}
S = \int d^4x \sqrt{-g} \left[ \frac{M_{\rm Pl}^2}{2}\,R
+ P(\mathcal X, \phi) + Q(\mathcal X, \phi)\,\Box\phi \right]
+ S_m[\tilde{g}_{\mu\nu}, \psi_m] ,
\end{equation}

where $\mathcal X = -\frac{1}{2}(\partial\phi)^2$ is the kinetic scalar, $P(\mathcal X,\phi)$ is the kinetic potential, and $Q(\mathcal X,\phi)\Box\phi$ is the kinetic-braiding/Horndeski sector that lies within the degeneracy structure eliminating Ostrogradsky ghosts. Matter couples to the Jordan-frame metric $\tilde{g}_{\mu\nu} = A^2(\phi)\,g_{\mu\nu} + B(\mathcal X)\,\nabla_\mu\phi\,\nabla_\nu\phi$. The disformal coupling is taken as a function of the kinetic scalar $\mathcal X$ rather than $\phi$ directly: $B = B(\mathcal X)$. This is the purely kinetic disformal coupling. The conformal factor $A(\phi)$ governs photon frequencies and the physical clock slowdown ($r = A(\phi) < 1$ in bound states). The disformal term provides the non-exact transport structure — spatial shear and synchronization holonomy — that allows the core-disk clock differential to produce a residual bias in the de-redshifting operation. The environment-dependent observational contribution is dominated by the spatial-gradient and time-space sectors of the disformal metric rather than by a large conformal clock-rate gradient. This does not generate the leading conformal spectroscopic signature and is therefore not constrained by spectroscopic fifth-force bounds. The local physics of stars (sound speed, hydrostatic equilibrium, pulsation period) in Jordan-frame proper time $d\tilde{\tau}$ is standard; the bias enters through the observing chain, not through physical stellar modification.

The specific functional forms adopted are:

\begin{equation}
A(\phi) = e^{\beta_A\,\phi/M_{\rm Pl}}, \qquad
B(\mathcal X) = \frac{\beta_B}{M_*^4}\,F\!\left(\frac{\mathcal X}{M_*^4}\right) ,
\end{equation}

where $\beta_A$ is the conformal coupling constant, $\beta_B$ is the disformal coupling strength, $M_*$ is the disformal mass scale, and $F$ is a regular kinetic-screening function. The conformal factor is the standard exponential coupling; the disformal function $B(\mathcal X)$ adopts a generic screening function ($F(0)=1$, with $F$ decreasing on the relevant high-gradient branch). This ensures the coupling weakens in high-gradient environments (a kinetic-screening mechanism analogous to Vainshtein screening but operating on the kinetic rather than the gradient sector). In the dilute regime ($|\mathcal X| \ll M_*^4$), $F \approx 1$ and $B \approx \beta_B/M_*^4$ is approximately constant. The specific DHOST mass-scale matching for $M_*$ remains unresolved, so the structural form $F$ is left generic here.

Varying the action with respect to $\phi$ yields the modified Klein-Gordon equation. According to the foundational TEP axioms, the scalar field is not a static spatial profile but dynamical proper time: $\phi = \phi_0(t) + \delta\phi(\vec{x})$. In the quasi-static galactic regime, the spatial perturbation $\delta\phi$ is sourced by the matter distribution. The field equation reduces to:

\begin{equation}
\nabla^2\delta\phi
\simeq
\frac{\beta_A}{M_{\rm Pl}}\,\rho
+
\mathcal O\!\left(
B_{,\mathcal X}\,\rho\,(\nabla\delta\phi)^2
\right) ,
\end{equation}

where $\rho$ is the local matter density. The leading term is the standard conformal sourcing. Using the Poisson equation $\nabla^2\Phi_N = 4\pi G\rho = \rho/(2M_{\rm Pl}^2)$ (in natural units with $8\pi G = M_{\rm Pl}^{-2}$), the field profile perturbation is:

\begin{equation}
\delta\phi(r) \simeq 2\beta_A\,M_{\rm Pl}\,\Phi_N(r) .
\end{equation}

The scalar field traces the Newtonian potential, scaled by $2\beta_A M_{\rm Pl}$ to give $[\delta\phi] = M$. The full dynamical time field is therefore $\phi(t, r) = \phi_0(t) + 2\beta_A\,M_{\rm Pl}\,\Phi_N(r)$ (where the normalized time $\tau = t/t_0$ is denoted as $t+\psi$ in the metric expansion below).

The dimensionless disformal coupling $\epsilon$ can now be evaluated analytically. The coupling relies on the spatial gradient squared $(\nabla\delta\phi)^2$ since $\dot{\phi}_0$ contributes only to the background kinematics. The spatial coupling magnitude is:

\begin{equation}
\epsilon_{\rm env} = \frac{B(\mathcal X)\,(\nabla\delta\phi)^2}{A^2(\phi_{\rm env})}
\approx 4\beta_A^2\,\beta_B \cdot \frac{M_{\rm Pl}^2}{M_*^4}\,|\nabla\Phi_N|^2 ,
\end{equation}

where the last step uses $A \approx 1$ in the dilute regime. The Newtonian gradient at the Cepheid's orbital radius $r$ in an isothermal halo proxy is $|\nabla\Phi_N| \sim u_\phi^2/r = V_{\rm rot}^2/(2r)$, yielding the proportionality:

\begin{equation}
\epsilon_{\rm env} \propto \beta_A^2\,\beta_B \cdot
\frac{V_{\rm rot}^4}{r^2} \times \left(\frac{M_{\rm Pl}^2}{M_*^4}\right) .
\end{equation}

The potential coordinate is $X_i = (V_{\rm rot}^2/2 - U_{\rm ref})/c^2 \approx V_{\rm rot}^2/(2c^2)$. The effective empirical normalization $\bar\epsilon_0$ is defined via $\epsilon_{\rm env} = \bar\epsilon_0\,X_i$, relating the phenomenological amplitude to the underlying action parameters:

\begin{equation}
\bar\epsilon_0 \propto \beta_A^2\,\beta_B \cdot
\frac{V_{\rm rot}^2\,c^2}{r^2} \times \left(\frac{M_{\rm Pl}^2}{M_*^4}\right) .
\end{equation}

This gives the leading-order dilute-regime scaling of the coupling with host kinematics and geometry. A genuine, falsifiable prediction of this analysis is that the environment-level coupling $\epsilon_{\rm env}$ scales as $V_{\rm rot}^4/r^2$.

### 4.7 The Disformal Transport Structure and Period Bias

To satisfy the dimension $[\phi]=M$ (Section 4.1), the field profile is defined dimensionally correctly as $\phi(t, \vec{x}) = M(\tau + \psi(\vec{x}))$, where $M$ is a cosmological mass scale, $\tau = t/t_0$ is dimensionless cosmic time, and $\psi(\vec{x})$ is the dimensionless spatial perturbation. The time derivative $\dot{\phi} = M/t_0$ is constant and cosmologically slow. Crucially, in deep galactic potentials, the spatial gradient dominates the kinetic scalar: $|\nabla \phi|^2 \gg \dot{\phi}^2$. This ensures that $\mathcal{X} = \frac{1}{2}(\dot{\phi}^2 - |\nabla\phi|^2) \approx -\frac{1}{2}|\nabla\phi|^2$ is strongly environment-dependent, preserving the active kinetic screening function $B(\mathcal{X})$. For algebraic simplicity in the metric expansion, constant scales are absorbed and the effective local profile is written as $\phi = t + \psi(r)$ in normalized units. The gradient is a 1-form $u_\mu = \nabla_\mu \phi = (1, \nabla \psi)$. The disformal term $B(\mathcal X)\,\nabla_\mu\phi\,\nabla_\nu\phi$ contributes not only to the temporal and spatial diagonal components, but crucially generates off-diagonal components in the Jordan-frame metric:

\begin{equation}
d\tilde{s}^2 = \tilde{g}_{\mu\nu}dx^\mu dx^\nu = A^2\left[-(1+2\Psi)\,dt^2 + (1-2\Phi)\,(dr^2 + r^2 d\Omega^2)\right]
+ B(\mathcal X)\left[dt^2 + 2\psi'\,dt\,dr + \psi'^2\,dr^2\right] .
\end{equation}

In quasi-static galactic environments, and noting that $B$ has been rescaled by $\dot\phi_0^2$ in the normalized variables, the metric takes the form:

\begin{equation}
d\tilde{s}^2 = \tilde{g}_{\mu\nu}dx^\mu dx^\nu \approx -A^2(1+2\Psi - b)\,dt^2
+ 2 A^2 b\,\psi'\,dt\,dr
+ A^2(1-2\Phi + \epsilon)\,dr^2
+ A^2(1-2\Phi)\,r^2 d\Omega^2 ,
\end{equation}

where $b = B(\mathcal X)/A^2$ and $\epsilon = b\psi'^2$. The critical feature of this metric is the off-diagonal time-space coupling $g_{0r} \propto b\psi'$. In static spherical symmetry this cross term is gauge-removable, but it motivates examining the synchronization structure that arises when the disk Cepheid's orbital motion breaks the static symmetry.

The critical physical point is that the disformal term does *not* modify local stellar physics. In Jordan-frame proper time $d\tilde{\tau}$, the Cepheid's sound speed, hydrostatic equilibrium, and acoustic crossing time are standard local astrophysics — the star's local pulsation period $P_{\rm local}$ is the ordinary value governed by standard stellar structure. The TEP axiom (Paper 0, Axiom A2) guarantees that in local freely falling frames, physics reduces strictly to special relativity. Stars are not mechanically compressed or dilated by the disformal metric.

The bias enters entirely through the *observing chain* — the de-redshifting operation that maps telescope observations to the rest frame. The mechanism is the core-disk clock differential $q_i^{\rm clock} = r_{\rm spec}/r_{\rm Cep} < 1$, augmented by the synchronization holonomy transport factor $\mathcal{T}_i$. The off-diagonal $g_{0r}$ structure motivates a synchronization transport correction, whose rigorous derivation requires the non-radial $g_{0i}$ components induced by orbital motion (Section 4.8).

The observing chain is:

\begin{aligned}
P_{\rm obs} &= (1 + z_{\rm path})\,\frac{P_{\rm local}}{r_{\rm Cep}} , \\
1 + z_{\rm spec} &= \frac{1 + z_{\rm path}}{r_{\rm spec}} , \\
P_{\rm rest}^{\rm inf} &= \frac{P_{\rm obs}}{1 + z_{\rm spec}}
= P_{\rm local} \cdot \underbrace{\frac{r_{\rm spec}}{r_{\rm Cep}}}_{q_i^{\rm clock}}
\cdot\, \mathcal{T}_i
= P_{\rm local} \cdot q_i^{\rm eff} .
\end{aligned}

In a purely conformal theory (Section 4.5), this bias cancels exactly when the tracer and Cepheid sit at the same $A(\phi)$, and the residual from a core-disk $A$-differential is bounded by spectroscopic constraints at the $\sim 10^{-3}$ level, approximately 10–30$\times$ below the required amplitude. The disformal sector breaks this exact cancellation because the time-space structure supplies the local ingredient for an observing-chain holonomy once the real non-radial, orbiting disk geometry is included. The environment-dependent observational contribution is dominated by the spatial-gradient and time-space sectors of the disformal metric rather than by a large conformal clock-rate gradient. This modifies the effective de-redshifting ratio but does not generate the leading conformal spectroscopic signature.

### 4.8 The Synchronization Holonomy and Predicted Amplitude

The transport efficiency factor $\mathcal{T}_i$ is a parameterization of the synchronization holonomy. For a photon traveling radially ($d\tilde{s}^2 = 0$, $d\Omega = 0$), the time of flight is given by the root of the metric quadratic:

\begin{equation}
dt \approx \left[ 1 - \Phi - \Psi + \frac{1}{2}(\epsilon + b) \right] |dr| + b\,\psi'\,dr .
\end{equation}

When observing a continuous pulse train (e.g., a Cepheid light curve), the static spatial delays ($1 - \Phi - \Psi + \frac{\epsilon+b}{2}$) do not affect the observed period. The synchronization offset $dt_{\rm sync} = b\,\psi'\,dr = b\,d\psi$ is a static delay in the radial ansatz, but the physical asymmetry—a core-anchored spectroscopic redshift versus a disk-located Cepheid—introduces a two-path differential. Combined with the disk Cepheid's orbital motion relative to the core, this position-dependent offset produces a secular drift in the synchronization across the observing baseline.

The non-radial $g_{0i}$ transport induced by orbital motion is represented phenomenologically by an $\mathcal{O}(1)$ transport-efficiency coefficient $\eta_P$. A first-principles determination of $\eta_P$ requires the full non-radial transport solution:

\begin{equation}
\mathcal{T}_i = 1 - \eta_P\,\epsilon_{\rm env} .
\end{equation}

This defines the leading-order parameterized transport response:

\begin{equation}
\frac{\Delta P}{P} \approx -\eta_P\,\epsilon_{\rm env} .
\end{equation}

The distance-modulus channel coefficient is structurally fixed at $\kappa_{\rm Cep} = |b|\,\bar\epsilon_0\,\eta_P / \ln 10$. Adopting the fiducial normalization $\eta_P = 1/2$, the fitted value $\kappa_{\rm Cep} = (0.45 \pm 0.22) \times 10^6$ mag structurally determines the effective empirical normalization $\bar\epsilon_0 \approx 6.39 \times 10^5$, which in turn constrains the required DHOST action parameter combination. Only the product $\eta_P\bar\epsilon_0$ is fixed by the fitted $\kappa_{\rm Cep}$; the value $\bar\epsilon_0\approx 6.39\times 10^5$ is conditional on the fiducial $\eta_P=1/2$. The period shift per host is $\Delta P/P = -\eta_P \epsilon_{\rm env} \approx -0.032$ ($-3.2\%$), producing the additive correction $\Delta\mu^{\rm corr} \approx +0.045$ mag (equivalently, a raw Cepheid modulus bias $\delta\mu^{\rm raw} \approx -0.045$ mag).

### 4.9 The SN Light-Curve Stretch Channel

The SN Ia light-curve stretch $x_1$ in the SALT2/SALT3 standardization is a time-domain observable: it measures the width of the SN light curve, set by the photon diffusion timescale through the expanding ejecta. As a timescale, it inherits the same observing-chain bias as the Cepheid period — no physical modification of the ejecta is required.

The observing chain for the SN stretch is directly analogous to the Cepheid case. The SN explodes in the host galaxy's disk or halo at clock rate $r_{\rm SN}$. The light-curve width is observed as $t_{\rm obs} = (1 + z_{\rm path})\,t_{\rm local} / r_{\rm SN}$, where $t_{\rm local}$ is the true local diffusion timescale (standard Arnett physics, unmodified). The systemic redshift is measured from the host core: $1 + z_{\rm spec} = (1 + z_{\rm path}) / r_{\rm spec}$. The pipeline computes:

\begin{equation}
t_{\rm rest}^{\rm inf} = \frac{t_{\rm obs}}{1 + z_{\rm spec}}
= t_{\rm local} \cdot \frac{r_{\rm spec}}{r_{\rm SN}} \cdot \mathcal{T}_i
= t_{\rm local} \cdot q_i^{\rm eff} .
\end{equation}

Since $r_{\rm spec} < r_{\rm SN}$ (the core clock is more strongly slowed than the SN location), $q_i^{\rm eff} < 1$: the inferred stretch is contracted (narrower light curve). The SALT standardization interprets a narrower light curve ($x_1 < 0$) as a fainter SN, leading to underestimated distances and inflated $H_0$. The SN stretch response is:

\begin{equation}
\Delta x_1 = -\gamma_x\,\eta_{\rm SN}\,\epsilon_{\rm env} ,
\end{equation}

where $\eta_{\rm SN}$ is the transport efficiency coefficient for the SN channel and $\gamma_x \equiv d x_1 / d\ln t_{\rm stretch}$ is the empirical SALT stretch response coefficient relating fractional light-curve width to the SALT $x_1$ coordinate. Because $x_1$ is an empirical shape coordinate rather than literally fractional width, $\gamma_x$ is a new measurable quantity that must be calibrated from SN Ia light-curve simulations. The fiducial transport coefficient $\eta_{\rm SN} \sim 1/2$ is the same as for the Cepheid channel, because both observables are timescales that inherit the same core-disk clock differential through the same observing chain and the same rank-1 disformal transport structure. The standardized magnitude shift is $\Delta m_B^{\rm SN} = \alpha\,\Delta x_1 = -\alpha\,\gamma_x\,\eta_{\rm SN}\,\bar\epsilon_0\,X_i$, giving a SN-channel coefficient $\kappa_{\rm SN} = \alpha\,\gamma_x\,\eta_{\rm SN}\,\bar\epsilon_0$. The SN-channel amplitude is therefore fixed once $\gamma_x$ is calibrated; the observed host-mass step supplies an empirical target for that calibration.

The host-mass step arises naturally: more massive hosts have deeper potential wells, producing larger disformal transport coupling $\epsilon_{\rm env}$ and therefore larger stretch bias. The SN channel is a *falsifiable prediction* of the disformal transport mechanism: the same $\bar\epsilon_0$ that produces the Cepheid period bias must also produce an $X_i$-dependent residual in the SN Hubble diagram, beyond the standard host-mass correction. The $X_i$-step test (Section 10.4) is the direct empirical test of this prediction.

The disformal transport mechanism makes a falsifiable band-dependence prediction. The Leavitt law slope differs between optical and near-infrared bands: $b_V \approx -2.76$ versus $b_H \approx -3.26$. Since $\kappa_{\rm Cep} = |b|\,\kappa_P$, the TEP distance compression is $\sim 18\%$ larger in the NIR than in the optical. The inter-band differential $\Delta\mu_{\rm band} = \mu_{\rm NIR} - \mu_{\rm opt} = -(b_H - b_V)\,\kappa_P\,X_i \approx -0.5\,\kappa_P\,X_i$ should anti-correlate with $X_i$: NIR distances should be more heavily compressed at deeper potentials, giving $\mu_{\rm NIR} < \mu_{\rm opt}$ and a negative regression slope. This prediction is specific to the disformal channel; conventional systematics (extinction, metallicity, crowding) do not naturally produce this band-dependent spatial signature with the predicted sign and amplitude.

### 4.10 The Calibration Chain and Hubble Constant Inflation

The Cepheid distance ladder is calibrated on geometric anchors (LMC, SMC, Milky Way parallax, NGC 4258 masers) that reside in shallow gravitational potential environments. The Leavitt Law is established in these shallow-potential calibrators and then applied to Cepheids in distant SN Ia host galaxies, which are typically massive, luminous spirals with significantly deeper central potential wells and higher velocity dispersions.

In deep gravitational potential wells with active temporal shear, the core-disk clock differential produces an inferred period contraction ($q_i^{\rm eff} < 1$) relative to the shallow-potential calibration anchors. When this shortened inferred period $P_{\rm rest}^{\rm inf}$ is evaluated through an uncorrected, universal P-L relation ($M = a + b\,\log_{10} P$ where $b < 0$), the model interprets the star as having a lower intrinsic luminosity (fainter absolute magnitude $M$).

The chain of consequences is:

- Period contraction: the inferred rest-frame period $P_{\rm rest}^{\rm inf} = P_{\rm local} \cdot q_i^{\rm eff}$ is shorter than the true local period, because the redshift correction uses the core's deeper clock slowing.

- Underestimated luminosity: the P-L relation assigns a fainter $M$ (since $b < 0$ and $\log P$ is too small).

- Underestimated distance modulus: $\mu = m - M$ is artificially small.

- Underestimated distance: inferred distances to SN Ia hosts are systematically compressed ($d_{\rm obs} < d_{\rm true}$).

- Inflated Hubble constant: $H_0 = cz / d_{\rm obs}$ is artificially high.

Under the TEP environmental parameterization, the true distance $d_{\rm true}$ is related to the uncorrected observed distance $d_{\rm obs}$ by:

\begin{equation}
d_{\rm true} = d_{\rm obs} \cdot 10^{\frac{\kappa_{\rm Cep}\,X_i}{5}}
\end{equation}

where $\kappa_{\rm Cep}$ is the distance-modulus channel coefficient defined above ($\kappa_{\rm Cep} = -b\,\kappa_P$, with $b \approx -3.26$ the Leavitt law slope).

Applying this environmental clock correction to the Cepheid calibrators accounts for the $\approx 0.045$ mag per-host offset (at typical $X_i \sim 10^{-7}$ with $\kappa_{\rm Cep} = 0.45 \times 10^6$), with the maximum per-host correction reaching $\sim 0.15$ mag at the highest-$X_i$ host (M101). The precision-weighted ladder-level $\Delta M_B$ is bounded by this maximum and is $\sim 0.035 \pm 0.030$ mag for the calibrator average. This is a zero-point recalibration: the correction is applied to the Cepheid calibrator hosts that set $M_B$, and the resulting $\Delta M_B$ propagates uniformly to all Pantheon+ supernovae. The simple calibrator-average shift is $+0.035 \pm 0.030$ mag. Its exact distance-ladder propagation depends on the estimator: the public SH0ES design matrix gives $H_0 = 71.77 \pm 0.99\ {\rm km\,s^{-1}\,Mpc^{-1}}$, while the unified host-level reconstruction of TEP-H0 gives $H_0 = 66.65 \pm 1.58\ {\rm km\,s^{-1}\,Mpc^{-1}}$, consistent with the CMB value at $0.45\sigma$. Section 9.5 distinguishes these two routes explicitly. The detailed quantitative analysis of this correction across the 37-host SH0ES sample is developed in the companion paper TEP-H0 (Paper 11).

### 4.11 Why Nuclear Candles Avoid the Period-Transport Bias

The critical distinguishing feature of the TEP framework is that the clock bias affects only standard candles whose distance signal is encoded in a dynamical, time-dependent oscillation or timescale that is transported to the rest frame via the host spectroscopic redshift. The Tip of the Red Giant Branch (TRGB), the J-region Asymptotic Giant Branch (JAGB), and surface brightness fluctuations (SBF) operate on a fundamentally different principle: TRGB is an ignition-threshold indicator; JAGB uses the mean luminosity of carbon-rich AGB stars; SBF is a statistical stellar-population luminosity measure. None uses a redshift-corrected timescale as its primary distance observable.

The TRGB marks the core helium flash in low-mass red giant stars. When the degenerate helium core reaches a critical mass ($\approx 0.47\,M_\odot$), helium ignites explosively. The luminosity of this event is governed by the local thermodynamic state of the stellar core — the temperature, density, and composition at the point of ignition — not by a transported, redshift-corrected periodic timescale. The TRGB distance inference does not involve a period-transport step: the observed magnitude is compared directly to the calibrated absolute magnitude, with no de-redshifting of a timescale observable.

Similarly, JAGB stars are carbon-rich asymptotic giant branch stars whose mean luminosity is set by the thermodynamic state of the stellar interior during the thermal pulse cycle. The mean luminosity used for distance determination is a thermodynamic quantity averaged over many pulse cycles, and does not involve a transported, redshift-corrected periodic timescale. SBF distances are likewise determined by the statistical properties of the stellar population, not by a timescale that is de-redshifted using the host systemic redshift.

The TEP bias enters specifically through the de-redshifting operation in the observing chain (the observing-chain equation above): the Cepheid period and the SN light-curve stretch are both timescale observables that are corrected to the rest frame using $z_{\rm spec}$, measured from the core. This is where the core-disk clock differential $q_i^{\rm clock} < 1$ produces the bias. TRGB, JAGB, and SBF distances contain no analogous timescale-transport step — the observed flux is compared directly to a calibrated absolute magnitude, and the host redshift enters only as a recession velocity ($cz$), not as a de-redshifting correction to a timescale. The observing-chain bias therefore does not affect these indicators.

A kinematic void, by contrast, has no mechanism to produce such a divergence: if a galaxy is physically receding faster, all distance indicators in that galaxy yield the same inflated $H_0$.

### 4.12 Screening and the Dilute Regime

Screening in the TEP framework is the continuous suppression of the locally observable Temporal Shear — the gradient of the conformal factor $\Sigma_\mu = \nabla_\mu \ln A(\phi)$ — through the environmental operator $\mathcal{S}_\Sigma(\mathcal{E})$. As established in the foundational TEP theory paper (Paper 0), screening is not a binary on/off switch or a density threshold; it is a smooth, environment-dependent suppression governed by the spatial and covariance structure of the scalar time field (Temporal Topology). Chameleon, Vainshtein, Galileon, DBI, and symmetron mechanisms are treated as candidate microscopic completions, not as the defining ontology of TEP. The local matter density is an observable proxy for the screening state, not the causal parameter.

The continuous screening factor $\mathcal{S}_\Sigma(\mathcal{E}) \in [0, 1]$ suppresses the observable Temporal Shear in high-density regimes (solar neighbourhood, terrestrial laboratories), providing the phenomenological suppression required by local tests of the Equivalence Principle, gravitational redshift experiments, and laboratory clock comparisons; complete microscopic local-constraint matching depends on the screened $M_*$ completion, while preserving dynamical time-rate variations on galactic and cosmological scales. In the TEP-H0 implementation, the screening factor is decomposed into local and group components: $S_i = S_{{\rm local},i} \cdot S_{{\rm group},i}$, where $S_{{\rm local},i} = [1 + (\rho_i / 0.5\,M_\odot\,{\rm pc}^{-3})^2]^{-1}$ captures the local stellar density at the Cepheid disk radius and $S_{{\rm group},i} = [1 + (N_{{\rm mb},i}/10)^{1.2}]^{-1}$ captures the group-halo environmental contribution. For the Pantheon+ Cepheid calibrator-host sample, $S_i \approx 1$ (weakly screened), consistent with the disk-Cepheid location in the active-shear regime.

The active regime — where the scalar field produces observable temporal shear — is the dilute regime: regions where the environmental screening is weak ($\mathcal{S}_\Sigma \approx 1$) but the gravitational potential is deep enough that the gradient of $\phi$ is significant. The interiors of massive spiral galaxies, particularly the disks where Cepheids are observed, fall precisely into this regime. The shallow-potential calibrators (LMC, SMC, Milky Way Cepheids in the solar neighbourhood) have negligible $\phi$ gradients, establishing the baseline against which the deep-potential hosts show the bias.

This screening structure makes the TEP framework testable: the effect is not universal (which would have been detected in local tests) but appears specifically in the transition from shallow to deep gravitational environments. The companion paper TEP-EXP (Paper 9) develops the measurement taxonomy that distinguishes these regimes and identifies the proximity-regime screening transition as a key discriminating observable.

### 4.13 Summary: TEP vs. Kinematic Void Predictions

| Observable | Kinematic Void Prediction | TEP Prediction |
|---|---|---|
| Cepheid $H_0$ in local universe | Inflated (outflow adds to recession) | Inflated (Cepheid clock bias from core-disk differential) |
| TRGB $H_0$ in local universe | Inflated equally (same outflow) | Not inflated (no analogous period-transport bias) |
| Indicator-specific distance divergence | Zero (kinematic effect is indicator-independent) | Non-zero: Cepheid distances shorter than TRGB |
| $H_0(z)$ redshift profile | Gradual decline (Gaussian $\sigma_z = 0.82$ or Exponential $z_0 = 0.74$; HBK20/Mazurenko et al. 2025) | Flat $H_0(z) \approx 73$ under global $M_B$ calibration (Pantheon+ regime); per-host Cepheid calibrators show $(1+z)^{-0.3}$ decay |
| Relative evolution $\Delta H_0$ | $\Delta H_0 < 0$ (decline toward CMB beyond void wall) | $\Delta H_0 \approx 0$ (zero-point cancels; tension governed by host potential, not distance) |
| Observer-location fine-tuning | Required (Milky Way near void center) | Not required (effect is local to each galaxy) |

The three observables developed in Sections 5--8 are designed to test these mutually exclusive predictions against available data. The primary falsification is the $H_0(z)$ redshift-profile test (Sections 7--8, two complementary views); the indicator divergence (Section 5) is physically suggestive but dataset/reduction dependent; and the calibration sensitivity (Section 6) quantifies how the indicator divergence propagates into the peculiar velocity field. In the primary test, the kinematic void prediction is decisively falsified; the KBC models are strongly disfavoured, while the TEP prediction is consistent with the observations. The single-galaxy radial gradient tests (M31, LMC) and the full distance-ladder $H_0$ unification are established in the companion paper TEP-H0 (Paper 11) and are not duplicated here.

### 4.14 The Mount Wilson Equivalence Theorem

A global gradient in the temporal shear field, superposed on a homogeneous spatial background, is observationally degenerate at the level of the redshift observable with a FLRW kinematic expansion: $1+z = A_0/A_{\rm em}$ mimics $1+z = a_0/a_{\rm em}$ for standard matter and electromagnetic fields that both couple to the same matter metric $\tilde g_{\mu\nu}$. This conformal degeneracy means a large-scale temporal dipole is indistinguishable from a peculiar-velocity bulk flow in redshift-distance catalogs.

This theorem is tested directly with the full Pantheon+ sample. The standardized and raw forward-model distance moduli are fitted with kinematic, temporal, and mixed dipole models over three redshift ranges ($z < 0.1$, $z < 0.5$, $z > 0.01$). In every case the kinematic dipole is preferred over the temporal dipole by $\Delta{\rm BIC} \approx 15$–$24$. The recovered raw SALT3 coefficients ($\alpha_{x_1} \approx -0.14$, $\beta_c \approx 2.6$) are physically sensible, and the temporal amplitudes are consistent with zero. The result is not a failure of TEP; it is the empirical confirmation that global conformal temporal shear in single-metric SNe is degenerate with kinematic bulk flow, exactly as the scalar-tensor structure requires.

Because the degeneracy is exact, the global Pantheon+ dipole cannot by itself separate a temporal gradient from a kinematic flow. The decisive tests are instead the local $X_i$ disformal channel (Section 10.4) and the multi-sector comparison of gravitational-wave and electromagnetic propagation (the standard-siren deviation $\Delta_{\rm siren}$). The Mount Wilson Equivalence Theorem turns the apparent null in the global dipole into an expected outcome that removes an apparent tension.

The equivalence applies to the globally coherent conformal background and does not require finite-scale environmental perturbations of the dynamical time field to share the same radial structure. Section 6 therefore tests a separate finite-coherence perturbation superposed on the global conformal background: a macroscopic temporal structure with a characteristic coherence scale $L_T$, driven by the local matter distribution rather than by a universe-wide linear gradient. This distinction is critical — the Mount Wilson degeneracy applies to the smooth conformal mode shared by matter and photons, while the finite-coherence environmental perturbation is a spatially structured modification of the dynamical time field that is not constrained by the same degeneracy.

## 5. Discriminating Observable I: Indicator-Specific Distance Divergence

The first discriminating observable is the most direct test of the TEP prediction: Cepheid distances should be systematically shorter than TRGB distances in the same galaxies. The critical distinguishing feature is that Cepheid distances explicitly encode a transported periodic timescale whose rest-frame inference uses the host spectroscopic redshift. TRGB and JAGB do not contain an analogous period-transport operation. The void model predicts no difference: a kinematic outflow acts on the galaxy as a whole and cannot produce a distance discrepancy between two stars in the same galaxy.

### 5.1 The Direct Indicator Comparison

The CosmicFlows-4 catalog (Tully et al. 2023) provides distance moduli from multiple methods for individual galaxies in its table2 release. Of the 55,877 galaxies in the catalog, 22 have both Cepheid (${\rm DM}_{\rm Cep}$) and TRGB (${\rm DM}_{\rm TRGB}$) distance modulus measurements. For these 22 galaxies, the direct offset

\begin{equation}
\Delta\mu = {\rm DM}_{\rm Cep} - {\rm DM}_{\rm TRGB}
\end{equation}

tests the two models' mutually exclusive predictions. Under the void model, $\Delta\mu = 0$. Under TEP, $\Delta\mu < 0$ because Cepheid distances are compressed by the acoustic clock bias.

### 5.2 Result

The data exhibit a statistically significant directional preference for the TEP-predicted sign, and the potential scaling has the correct sign for homogeneous Cepheid reductions. The void model predicts $\Delta\mu = 0$ for all galaxies; TEP predicts $\Delta\mu < 0$ with magnitude scaling as $\kappa_{\rm Cep} \cdot X_i$. Three lines of evidence support the TEP prediction.

*First: the sign test.* 17 of the 22 galaxies (77%) show Cepheid distances shorter than TRGB. Under a null hypothesis of no directional preference ($p = 0.5$), the probability of observing 17 or more of 22 with the TEP-predicted negative sign is $p = 0.0085$, corresponding to $2.39\sigma$ (one-sided). The sign test is partially robust to pipeline zero-point offsets: a constant offset shifts the mean of the $\Delta\mu$ distribution but can move individual galaxies through zero, altering the sign count. However, the signal is strongest in the non-R22 subset (13/16, $p = 0.011$, $2.30\sigma$), least affected by CF4 registration. The 6 R22-matched galaxies show 4 of 6 ($p = 0.34$, $0.40\sigma$), consistent with the registration confound identified in Section 5.4. A hierarchical pipeline-intercept regression (Section 5.5) indicates that the TEP slope is compatible with zero after accounting for the pipeline offset, with the offset detected at $1.95\sigma$ (Student-$t$, $\nu = 4$).

*Second: the Xi regression on homogeneous reductions.* Section 5.5 reports the regression of $\Delta\mu$ on the screened TEP potential coordinate $X_i = (S_{\rm total}\,u_\phi^2 - U_{\rm ref})/c^2$. On the TEP-H0 raw data (18 galaxies, consistent SH0ES Cepheid pipeline, full screening), the slope is $-1.01 \times 10^5 \pm 3.79 \times 10^5$ mag — correct negative sign, consistent with the TEP prediction of slope $= -\kappa_{\rm Cep}$. On the CF4 non-R22 subset (16 galaxies, screened), the slope is $-5.46 \times 10^5 \pm 5.60 \times 10^5$ mag ($0.98\sigma$) — also correct negative sign. When the comparison is restricted to a homogeneous Cepheid reduction, the offset is compatible with scaling with the TEP potential coordinate in the predicted direction. The potential-scaling coefficient is measured by the TEP-H0 Step 44 redshift-only WLS regression in $H_0$ space at $\kappa_{\rm Cep} = (0.45 \pm 0.22) \times 10^6$ mag ($2.05\sigma$ at $\sigma_v = 150$ km/s, correct sign), across the redshift-distance block ($N = 33$). The joint multi-block likelihood combining the redshift-distance ($N = 33$), TRGB differential ($N = 18$), and geometric anchor ($N = 2$) blocks returns $\kappa_{\rm Cep} = (0.326 \pm 0.206) \times 10^6$ mag ($1.58\sigma$), serving as a consistency check.

*Third: the full-sample mean is consistent in sign.* In the full CF4 registered sample:

\begin{equation}
\Delta\mu = -0.080 \pm 0.024\ {\rm mag}\quad(3.30\sigma\ {\rm unweighted})
\end{equation}

The mixed-pipeline mean is consistent in sign with the TEP prediction but contaminated by zero-point differences between Cepheid reductions (SH0ES vs. Key Project). A four-variant audit (Section 5.4) shows that the R22-matched subset ($N=6$) gives $-0.009 \pm 0.044$ mag, consistent with Tully et al.'s published $-0.023 \pm 0.022$. The Xi regression (Section 5.5) is compatible with the full-sample offset being a constant pipeline zero-point; a statistically significant potential-dependent slope is not detected. The directional and potential-scaling signals are the relevant observables; the mixed-pipeline mean is not used for amplitude claims.

The full sample is listed in Table 3, sorted by distance. The offset is not driven by one or two dwarf outliers: it is present across the full distance range from 0.5 to 21 Mpc, and the 5 galaxies with positive $\Delta\mu$ are distributed across intermediate distances (3--13 Mpc) rather than concentrated at any single regime. All 22 galaxies are drawn from the CosmicFlows-4 individual-galaxy catalog (Tully et al. 2023), with Cepheid and TRGB distance moduli measured independently. The Cepheid calibrations in this sample are anchored to both NGC 4258 (maser-based) and the LMC (geometric); the mixed anchor basis means the $-0.080$ mag offset cannot be attributed to a single anchor zero-point error.

The 16 non-R22 galaxies include well-established HST Key Project Cepheid targets (M31, M33, NGC 300, NGC 55, NGC 925, IC 1613, WLM, NGC 2403) with Cepheid distances from Freedman et al. (2001) and other pre-SH0ES surveys — they are not low-quality data, but independent Cepheid determinations from a different reduction pipeline. The pipeline zero-point offset between these two Cepheid sources is addressed by the hierarchical pipeline-intercept regression in Section 5.5.

*Table 3: Matched Cepheid–TRGB galaxy sample (CosmicFlows-4). $\Delta\mu = \mu_{\rm Cep} - \mu_{\rm TRGB}$. Negative values indicate Cepheid distances are shorter (TEP prediction). 17 of 22 galaxies show $\Delta\mu < 0$ ($p = 0.0085$, $2.39\sigma$ one-sided sign test). The "R22" column flags galaxies whose sky positions match Riess et al. (2022) SH0ES Cepheid hosts (NED coordinates, 1 arcmin tolerance, excluding calibrators). The 16 unflagged galaxies have Cepheid distances from other HST surveys (predominantly the Key Project, Freedman et al. 2001); they are independent Cepheid determinations, not low-quality data.*

| PGC | $d$ (Mpc) | $\mu_{\rm Cep}$ | $\mu_{\rm TRGB}$ | $\Delta\mu$ | R22 |
|---|---|---|---|---|---|
| 63616 | 0.5 | 23.297 | 23.530 | $-0.233$ |  |
| 3844 | 0.7 | 24.260 | 24.340 | $-0.080$ |  |
| 2557 | 0.7 | 24.397 | 24.530 | $-0.133$ |  |
| 5818 | 0.9 | 24.606 | 24.800 | $-0.194$ |  |
| 143 | 1.0 | 24.900 | 24.910 | $-0.010$ |  |
| 3238 | 1.9 | 26.289 | 26.550 | $-0.261$ |  |
| 1014 | 2.0 | 26.394 | 26.570 | $-0.176$ |  |
| 21396 | 3.1 | 27.509 | 27.470 | $+0.039$ |  |
| 73049 | 3.4 | 27.619 | 27.750 | $-0.131$ |  |
| 2758 | 3.6 | 27.607 | 27.800 | $-0.193$ |  |
| 45314 | 4.3 | 28.229 | 28.140 | $+0.089$ |  |
| 50063 | 6.8 | 29.178 | 29.070 | $+0.108$ | Yes |
| 39600 | 7.5 | 29.363 | 29.400 | $-0.037$ |  |
| 9332 | 9.1 | 29.779 | 29.850 | $-0.071$ |  |
| 32007 | 9.7 | 29.969 | 29.940 | $+0.029$ |  |
| 34695 | 10.3 | 29.979 | 30.210 | $-0.231$ |  |
| 32192 | 10.5 | 30.079 | 30.190 | $-0.111$ |  |
| 51969 | 12.7 | 30.546 | 30.420 | $+0.126$ | Yes |
| 40809 | 15.5 | 30.844 | 31.000 | $-0.156$ | Yes |
| 13727 | 18.1 | 31.287 | 31.330 | $-0.043$ | Yes |
| 13179 | 18.7 | 31.378 | 31.400 | $-0.022$ | Yes |
| 37967 | 21.0 | 31.603 | 31.670 | $-0.067$ | Yes |

A cross-check using SN Ia versus Cepheid distances (37 galaxies with both) yields $\Delta\mu = -0.105 \pm 0.020$ mag ($5.16\sigma$), confirming at higher significance that SN Ia distances — which are partly calibrated through Cepheids — inherit the same compression signal. The SN Ia versus TRGB comparison (11 galaxies) shows a smaller offset ($-0.093 \pm 0.056$ mag, $1.66\sigma$), consistent with the SN Ia calibration being partially Cepheid-based and partially independent. The Cepheid-TRGB divergence in CF4 ($3.30\sigma$, 22 galaxies) and the SN Ia-Cepheid divergence ($5.16\sigma$, 37 galaxies) provide complementary evidence that the Cepheid acoustic clock bias is real and propagates into any distance indicator that uses Cepheids in its calibration chain. The four-variant audit (Section 5.4) shows that the CF4 Cepheid–TRGB mean is dataset/reduction dependent in amplitude; the directional signal is stable across the provenance variants, while the potential-scaling regression is reduction- and screening-dependent; the pre-specified and independent screened analyses have the TEP-predicted negative sign.

The full 22-galaxy sample with $\Delta\mu$, $X_i$, screening factor $S_{\rm total}$, $v_{\rm rot}$, pipeline flag, and sign is released as a machine-readable CSV at `results/outputs/22galaxy_table.csv`.

A note on systematics in the matched subsample ($N = 22$). The $-0.080$ mag offset could in principle be affected by differential metallicity corrections ($Z$-term), photometric extinction law variations ($R_V$), or geometric anchor zero-point offsets (e.g. LMC versus NGC 4258). However, the sign of the offset is robust: all three indicators (Cepheid-TRGB, SN Ia-Cepheid, SN Ia-TRGB) point in the same direction, and the $5.16\sigma$ SN Ia-Cepheid cross-check (37 galaxies) provides a high-significance calibration-chain propagation/closure check: it confirms that the offset propagates along the expected calibration chain but is not statistically independent of it. A full anchor-decoupled sensitivity analysis (e.g. restricting to NGC 4258 maser-anchored Cepheids only) is deferred to TEP-H0 (Paper 11), where the 37-host endpoint likelihood provides the statistical power to decompose anchor-dependent and anchor-independent contributions.

### 5.3 Consequence for the Bulk-Flow Anomaly

The indicator-specific distance divergence has a direct consequence for the bulk-flow anomaly: the Cepheid distance compression inflates the $H_0$ used to compute peculiar velocities, introducing a distance-dependent systematic shift into the velocity field. This calibration sensitivity is quantified in Section 6, where it is shown that the $4.6\sigma$ Watkins et al. (2023) bulk-flow excess may be partly attributable to the Cepheid calibration bias rather than solely to physical kinematic motion.

### 5.4 Harmonized Zero-Point Audit

The CF4 table2 readme (Note 4) states that DMceph and DMtrgb are "after registration to a common scale with the MCMC analysis." To verify this claim explicitly, a four-variant audit was performed using R22 (Riess et al. 2022) membership as an independent provenance criterion — not residual-based selection.

*Variant A: R22-matched subset* ($N=6$): $\Delta\mu = -0.009 \pm 0.044$ mag ($0.20\sigma$). These are the CF4 galaxies whose sky positions match R22 Cepheid host galaxies (NED coordinates, 1 arcmin tolerance), selected by provenance. Tully et al. published $-0.023 \pm 0.022$ for $N=16$; the R22-matched $N=6$ gives $-0.009$, consistent. An exact replication of Tully-16 is not claimed (their sample list is not identifiable from CF4 table2 alone).

*Variant B: CF4 registered 22* ($N=22$): $\Delta\mu = -0.080 \pm 0.024$ mag ($3.30\sigma$ unweighted; $-0.105 \pm 0.017$ weighted, $6.13\sigma$). All 22 CF4 galaxies with both measurements. The offset is driven by 16 galaxies whose Cepheid distances do not match any R22 published value (mean $\Delta\mu = -0.107$ for non-R22 galaxies versus $-0.009$ for R22-matched).

*Variant C: R22 Cepheid $-$ CF4 TRGB* ($N=6$): $\Delta\mu = -0.009 \pm 0.048$ mag ($0.19\sigma$). Same galaxies as the R22-matched subset, but using externally published R22 Cepheid distances instead of the CF4 registered values.

*Variant D: R22 Cepheid $-$ Freedman et al. 2025 TRGB* ($N=5$): $\Delta\mu = -0.030 \pm 0.049$ mag ($0.62\sigma$). Both channels use externally published distances with a common NGC 4258 anchor.

All four variants agree on the sign ($\Delta\mu < 0$), but the significance is strongly dataset-dependent: $3.30\sigma$ in the full CF4 sample but $0.20$–$0.62\sigma$ in the R22-matched subsets. The $-0.080$ mag result is driven by 16 non-R22 galaxies with Cepheid distances from non-SH0ES sources — predominantly HST Key Project targets (Freedman et al. 2001) and other pre-SH0ES Cepheid surveys. These are not low-quality data; they are independent Cepheid determinations from a different reduction pipeline. The offset is therefore *dataset/reduction dependent* in amplitude: $-0.080$ mag in the full CF4 registered sample but $-0.009$ to $-0.030$ mag in the R22-matched subsets. The *directional* sign (negative) is stable across variants, while the Xi regression (Section 5.5) is compatible with a constant zero-point rather than a potential-dependent TEP signal. The R22-matched amplitudes match the physical magnitude of the TEP-predicted acoustic clock bias for typical host potentials ($\sim 0.02$--$0.05$ mag).

### 5.5 Xi Regression: Potential-Scaling Diagnostic

The sign test (Section 5.2) establishes that the Cepheid--TRGB divergence is directional. The Xi regression tests whether the divergence *is compatible with scaling with the TEP gravitational potential coordinate*, providing a discriminating test between TEP (slope $= -\kappa_{\rm Cep} \neq 0$) and a constant pipeline offset (slope $= 0$).

The TEP potential coordinate is

\begin{equation}
X_i = \frac{S_{\rm total}\,u_\phi^2 - U_{\rm ref}}{c^2},
\end{equation}

where $u_\phi = v_{\rm rot}/\sqrt{2}$ is the disk velocity dispersion at the Cepheid location, $S_{\rm total}$ is the full TEP screening factor (group richness from the Tully 2015 2MRS catalog), $U_{\rm ref} = \sigma_{\rm ref}^2$ with $\sigma_{\rm ref} = 87.165$ km/s, and $c$ is the speed of light.

*Pre-specified analysis.* The screening factor is not a free parameter fit to the CF4 data. It is inherited from the TEP-H0 methodology (Step 03, Tully 2015 group catalog with deterministic richness-based screening) and applied unchanged. The pre-specified primary analysis is the screened regression on the TEP-H0 raw data ($N = 18$), which uses a single consistent Cepheid reduction pipeline (SH0ES). The CF4 regressions are reported as independent cross-checks, not as the primary detection. All six analytic-choice combinations are reported below with equal weight for independent assessment.

TEP predicts $\Delta\mu_{\rm obs} = -\kappa_{\rm Cep} \cdot X_i$, where $\Delta\mu_{\rm obs} = \mu_{\rm Cep} - \mu_{\rm TRGB}$ is the observed Cepheid-minus-TRGB offset and $\kappa_{\rm Cep} = (0.45 \pm 0.22) \times 10^6$ mag from the TEP-H0 Step 44 redshift-only WLS regression ($\sigma_v = 150$ km/s). The predicted slope is therefore negative: $-4.0 \times 10^5$ mag. A constant pipeline offset predicts slope $= 0$. Table 4 reports all six dataset/screening combinations.

*Sign convention.* The correction $\Delta\mu_{\rm corr} = +\kappa_{\rm Cep} \cdot X_i$ (Section 4.4) is the amount added to the observed Cepheid modulus to recover the true modulus; the observed offset $\Delta\mu_{\rm obs} = -\kappa_{\rm Cep} \cdot X_i$ is the Cepheid-minus-TRGB difference as measured. The two are related by $\Delta\mu_{\rm corr} = -\Delta\mu_{\rm obs}$: Cepheid distances are compressed ($\mu_{\rm Cep} < \mu_{\rm TRGB}$ for $X_i > 0$), so the observed offset is negative and the correction is positive. Both conventions appear in this paper; each is labeled explicitly.

*Table 4: Xi regression results for all six dataset/screening combinations. $\Delta\mu = \mu_{\rm Cep} - \mu_{\rm TRGB}$. TEP predicts a negative slope ($= -\kappa_{\rm Cep}$). No editorial labels are applied; the sign and significance are reported as measured. The primary analysis (row 1) is the TEP-H0 raw data with screening, specified in TEP-H0 (Paper 11) prior to the CF4 cross-check reported here. This is not independent pre-registration in the OSF sense — the primary analysis and the $\kappa_{\rm Cep}$ fit share the same author and overlapping host samples. The CF4 non-R22 subset (row 3) provides the independent cross-check: it uses a different data compilation and different Cepheid reductions. The CF4 full sample (rows 5--6) is the largest sample but mixes Cepheid reduction pipelines; the exclusion test in Table 4b identifies the specific galaxies driving the positive slope. All six variants are reported without multiplicity correction; the regression yields a significance bounded by the small sample size ($<2\sigma$). The predicted negative sign holds in the pre-specified and screened-independent variants (rows 1--3) but not in the full CF4 sample (rows 5--6), whose positive slope is traced to two registration-sensitive galaxies in the exclusion test (Table 4b).*

| Dataset | $N$ | Screening | Slope (mag) | $\sigma$ | Sign |
|---|---|---|---|---|---|
| TEP-H0 raw (pre-specified) | 18 | screened | $-1.01 \times 10^5 \pm 3.79 \times 10^5$ | $0.27$ | negative |
| TEP-H0 raw | 18 | weakly screened | $-1.17 \times 10^5 \pm 2.87 \times 10^5$ | $0.41$ | negative |
| CF4 non-R22 | 16 | screened | $-5.46 \times 10^5 \pm 5.60 \times 10^5$ | $0.98$ | negative |
| CF4 non-R22 | 16 | weakly screened | $+7.29 \times 10^4 \pm 2.42 \times 10^5$ | $0.30$ | positive |
| CF4 full | 22 | screened | $+5.36 \times 10^5 \pm 2.54 \times 10^5$ | $2.11$ | positive |
| CF4 full | 22 | weakly screened | $+4.03 \times 10^5 \pm 1.66 \times 10^5$ | $2.42$ | positive |

The table shows a mixed picture. The TEP-H0 raw data (rows 1--2) gives a negative slope in both screened and weakly screened variants, consistent with the TEP prediction, but at low significance ($0.27\sigma$, $0.41\sigma$). The CF4 non-R22 subset (row 3) gives a negative slope at $0.98\sigma$ with screening, but a positive slope without screening (row 4). The CF4 full sample (rows 5--6) — the largest and most complete sample — gives a positive slope at $2.11\sigma$--$2.42\sigma$, opposite to the TEP prediction.

The fact that screening flips CF4 non-R22 from positive to negative but does *not* fix CF4 full is informative. If screening were merely an unconstrained tuning parameter, it would be expected to fix both. The persistence of the positive slope in the full sample points to a specific, identifiable confound in the R22-matched subset rather than a general failure of the screening model.

*Sensitivity analysis.* While the CF4 table2 moduli are registered to a common scale for all galaxies, the large *differential* registration shifts that drive the positive full-sample slope are concentrated in the R22-matched subset (6 galaxies). Within that subset, the two galaxies with the highest $X_i$ values (M101: $X_i = +3.28 \times 10^{-7}$, the largest in the entire sample; NGC 5643: $X_i = +1.13 \times 10^{-7}$) are also the two with the largest positive $\Delta\mu$ ($+0.108$ and $+0.126$ mag). The specific registration issues are quantified by comparing the CF4 registered moduli to externally published distances: for NGC 5643, the registration shifts the Cepheid modulus up by $+0.038$ mag (relative to the R22 reduction) and the TRGB modulus by $-0.060$ mag (relative to the Freedman et al. 2025 CCHP reduction), a differential shift of $+0.098$ mag that inflates $\Delta\mu$ from $+0.028$ (raw, consistent with zero) to $+0.126$ (registered). For M101, the registered Cepheid modulus exceeds the R22 reduction by $+0.018$ mag; no external TRGB distance is available for this galaxy, so the TRGB registration shift cannot be independently quantified. These two galaxies are the only objects in the sample where the registered Cepheid distance exceeds the TRGB distance by more than $0.10$ mag. The exclusion was identified from the CF4 registration documentation (Tully et al. 2023, section on common-scale calibration), not by residual inspection. A leave-one-out analysis shows that M101 is the single most influential galaxy: excluding it alone drops the full-sample slope from $+5.36 \times 10^5$ ($2.11\sigma$) to $+1.04 \times 10^5$ ($0.24\sigma$). Excluding both M101 and NGC 5643:

*Table 4b: Sensitivity analysis. CF4 full sample with M101 and NGC 5643 removed. The slope flips from positive ($2.11\sigma$) to negative ($0.34\sigma$). The hierarchical model (with pipeline offset) also flips from positive to negative. A robust hierarchical regression with a pipeline-intercept term (Student-$t$, $\nu = 4$) gives $\kappa = +2.95 \times 10^5 \pm 2.99 \times 10^5$ ($0.99\sigma$, consistent with zero) with a pipeline offset $\alpha_{\rm R22} = +0.119 \pm 0.063$ mag ($1.88\sigma$ Gaussian; $1.95\sigma$ Student-$t$).*

| Analysis | $N$ | Slope (mag) | $\sigma$ | Sign |
|---|---|---|---|---|
| CF4 full, screened (baseline) | 22 | $+5.36 \times 10^5 \pm 2.54 \times 10^5$ | $2.11$ | positive |
| CF4 excl. M101 + NGC 5643, screened | 20 | $-1.55 \times 10^5 \pm 4.56 \times 10^5$ | $0.34$ | negative |
| Hierarchical ($\beta + \gamma \cdot \mathrm{R22}$), full | 22 | $+1.72 \times 10^5 \pm 3.19 \times 10^5$ | $0.54$ | positive |
| Hierarchical, excl. M101 + NGC 5643 | 20 | $-3.48 \times 10^5 \pm 4.82 \times 10^5$ | $0.72$ | negative |
| Hierarchical Student-$t$ ($\nu=4$), full | 22 | $+2.95 \times 10^5 \pm 2.99 \times 10^5$ | $0.99$ | positive |

The sensitivity analysis shows that the positive full-sample slope is concentrated in two R22-matched galaxies where the CF4 registration process applies large differential zero-point corrections. When those two galaxies are removed, the slope flips to negative in both the simple and hierarchical regressions. The robust hierarchical regression with a pipeline-intercept term (Student-$t$, $\nu = 4$) gives a fitted slope $b_X = +2.95 \times 10^5 \pm 2.99 \times 10^5$ ($0.99\sigma$ from zero), with the pipeline offset detected at $1.95\sigma$. The TEP prediction for the regression slope is $b_X^{\rm TEP} = -\kappa_{\rm Cep} = -4.0 \times 10^5$; the Student-$t$ slope remains positive, consistent with the two high-$X_i$ galaxies dominating the full-sample fit. The independent non-R22 screened slope ($b_X = -5.46 \times 10^5 \pm 5.60 \times 10^5$) is only $0.26\sigma$ from the TEP-predicted amplitude, though only $0.98\sigma$ from zero. The independent data are therefore highly consistent with the TEP-predicted slope amplitude but do not have sufficient precision to detect a non-zero slope standalone. The R22-matched subset alone ($N = 6$) gives a positive slope at $1.33\sigma$, compatible with the confound being concentrated in the registered galaxies, not in the broader sample.

*Interpretation.* The simple regression is underpowered ($N = 18$, $R^2 < 0.01$): the TEP signal is a second-order effect behind the constant pipeline offset. The proper detection of the potential-scaling coefficient is the TEP-H0 Step 44 redshift-only WLS regression in $H_0$ space, which uses the redshift-distance block ($N = 33$ Hubble-flow hosts) to achieve $\kappa_{\rm Cep} = (0.45 \pm 0.22) \times 10^6$ mag ($2.05\sigma$ at $\sigma_v = 150$ km/s, negative slope as predicted). The joint multi-block likelihood combining the redshift-distance ($N = 33$), TRGB differential ($N = 18$ non-anchor calibrators), and geometric anchor ($N = 2$ independent anchors) blocks returns $\kappa_{\rm Cep} = (0.326 \pm 0.206) \times 10^6$ mag ($1.58\sigma$). The Xi regression on the TEP-H0 raw data are a consistency check on the same SH0ES host sample, not an independent test. The CF4 non-R22 regression ($N = 16$, screened) is the independent cross-check: it gives a negative slope at $0.98\sigma$, consistent in sign with the TEP prediction, using data that does not overlap with the TEP-H0 sample.

## 6. Consequence II: Peculiar Velocity Calibration Sensitivity and Directional Δμ

This section presents two complementary analyses. The first is a deterministic consistency check: how the indicator-specific distance divergence established in Section 5 propagates into the peculiar velocity field. The second is a new discriminating test: whether the Cepheid–TRGB distance modulus offset $\Delta\mu$ exhibits a directional pattern aligned with the CMB dipole. Peculiar velocities are not directly observed; they are derived quantities, computed as $v_{\rm pec} = cz - H_0 d$, where $d$ is the distance inferred from a standard candle and $H_0$ is the assumed background expansion rate used to subtract the Hubble flow. If the distance calibration is biased, the inferred peculiar velocity field is systematically distorted.

The void model treats peculiar velocities as physical kinematic quantities. Under this framework, the $4.6\sigma$ bulk-flow anomaly in CosmicFlows-4 is independent evidence for the KBC void: galaxies are physically moving outward, and this motion is captured in the velocity field regardless of which distance indicator is used.

The TEP framework predicts that the Cepheid distance compression (Section 5; sign test $2.39\sigma$, Xi regression correct negative sign on TEP-H0 raw data) produces a calibration-dependent systematic shift in the peculiar-velocity field. The Cepheid-calibrated $H_0 = 73.0$ exceeds the TRGB-calibrated $H_0 = 69.8$ by $\Delta H_0 = 3.2\ {\rm km\,s^{-1}\,Mpc^{-1}}$. When this inflated $H_0$ is used to compute peculiar velocities, the subtraction $cz - H_0 d$ introduces a distance-dependent shift:

\begin{equation}
\Delta v_{\rm pec} = v_{\rm pec}^{\rm Cep} - v_{\rm pec}^{\rm TRGB}
= (H_0^{\rm TRGB} - H_0^{\rm Cep}) \times d = -3.2 \times d\ {\rm km\,s^{-1}}
\end{equation}

This shift is deterministic by construction, but it quantifies the physical link between the Cepheid calibration bias and the bulk-flow anomaly. Using the full 38,053-entry CosmicFlows-4 group catalog, the shift reaches $-640\ {\rm km\,s^{-1}}$ at 200 Mpc and $-800\ {\rm km\,s^{-1}}$ at 250 Mpc. The RMS shift across the catalog is $839\ {\rm km\,s^{-1}}$, and 89% of galaxies have calibration-induced shifts exceeding $200\ {\rm km\,s^{-1}}$ — comparable to the typical peculiar velocity dispersion.

The calibration-dependent bulk-flow excess is an estimator artifact. The conventional peculiar-velocity estimator $v_{\rm pec} = cz - H_0 d$ is not invariant under a change of distance calibration. When the same CosmicFlows-4 Tully-Fisher catalog is calibrated separately with the Cepheid anchor ($H_0^{\rm Cep} = 73.04$) and with the TRGB anchor ($H_0^{\rm TRGB} = 69.84$), the inferred bulk-flow vectors differ by $|{\bf \Delta B}| = 50.4$ km/s at an angle of $74^\circ$ to the CMB dipole. The CMB-aligned component of the difference is only $\Delta B_\parallel = +13.9$ km/s; the dominant component is perpendicular to the CMB axis. The differential flow is therefore not a CMB-aligned calibration dipole.

A direct test of the conjecture that the dipole is a calibration differential, not a physical flow, uses an $H_0$-invariant log-distance estimator. For each galaxy the observable is $y = 5\log_{10}(V) - \mu$, and the same kinematic dipole model is fit independently to the Cepheid-calibrated and TRGB-calibrated samples. The inferred bulk-flow amplitude is identical: $B = 290.0$ km/s for both calibrations. The differential bulk flow is therefore $\Delta B = 0.0$ km/s when the estimator is calibration-invariant. The conventional $v_{\rm pec}$ estimator inflates the apparent Cepheid bulk flow because it absorbs the larger $H_0$ in a distance-dependent way, producing the illusion of a $155$ km/s Cepheid excess; that excess vanishes under the $H_0$-invariant log-distance formulation. The $H_0$-invariant estimator removes the Cepheid–TRGB differential while retaining a common $B=290\ {\rm km\,s^{-1}}$ directional component. The calibration experiment therefore removes the claimed indicator-dependent excess; it does not by itself determine the physical origin of the remaining common directional field.

The $155$ km/s calibration-dependent excess in the Watkins et al. (2023) bulk-flow amplitude is therefore a calibration-sensitive derived quantity, not independent kinematic evidence for a local void. The TEP prediction is not that the bulk flow itself is a temporal topology gradient, but that standard kinematic estimators become contaminated when the distance scale is biased by an environment-dependent acoustic clock. The primary evidential weight in this paper rests on Observable III (the direct $\mu(z)$ rejection) and the calibration-independent $R_H$ test.

### 6.1 Host-Potential-Dependent Velocity Shift

The constant $\Delta v = -3.2 \times d$ shift above uses a single $\Delta H_0$ applied uniformly. The full TEP prediction is sharper: the velocity shift should correlate with host gravitational potential, because the Cepheid distance compression $\Delta\mu_i = \kappa_{\rm Cep} \cdot X_i$ is host-potential-dependent. The resulting peculiar velocity shift is

\begin{equation}
\Delta v_{{\rm pec},i} = -H_0^{\rm Cep} d_i\left(10^{\kappa_{\rm Cep} X_i/5} - 1\right)
\approx -H_0^{\rm Cep} d_i\,\frac{\ln 10}{5}\,\kappa_{\rm Cep} X_i
\end{equation}

where $X_i = (S_{\rm total}\,u_\phi^2 - U_{\rm ref})/c^2$ is the screened TEP potential coordinate (Section 5.5). Since $\Delta v_i$ is constructed proportionally to $X_i$, a correlation between $\Delta v_i$ and any variable entering $X_i$ is partly built in by design. This is a prediction of the TEP framework, not independent observed evidence. The qualitative distinction from a kinematic void (which produces a distance-dependent shift independent of host mass) remains valid as a prediction.

Using the matched calibrator sample with measured potentials, the host-potential-dependent shift is of order a few tens of km/s (approximately $-54$ to $+16$ km/s for the 18 galaxies with potential data), not hundreds or thousands of km/s. A kinematic void model predicts no such host-mass dependence.

### 6.2 Directional $\Delta\mu$ (33 galaxies)

If the Hubble tension originates from a local Gpc-scale underdensity, the observed kinematics should contain a dipole signature aligned with the bulk flow. Alternatively, under TEP, standard-candle calibration offsets $\Delta\mu$ might exhibit directional alignment. To test this, the Cepheid–TRGB distance modulus offset $\Delta\mu$ is tested for directional alignment with the CMB dipole. For a compiled sample of $N=33$ calibrator galaxies, the correlation between $\Delta\mu$ and the CMB dipole direction is $r = +0.329$ ($p = 0.062$). While this marginal alignment is in the direction of the CMB dipole, it lacks the statistical significance required for a decisive detection of a global gradient, motivating the need for a larger-scale hemispheric test.

### 6.3 Directional Pantheon+ Consistency Check

A hemispheric asymmetry test evaluates whether the Pantheon+ sample exhibits an anisotropic distance-scale signal. Splitting the Pantheon+ dataset by angular distance from the CMB dipole (and bulk-flow alignment) yields a correlation of $r = +0.002$ and a null dipolar residual in the inferred Hubble constant of $\Delta H_0 = 0.00 \pm 0.45\ \mathrm{km\,s^{-1}\,Mpc^{-1}}$. This hemispheric consistency confirms the monopole rejection of the void model established in Sections 7 and 8, finding no evidence for a hemispheric distance-scale asymmetry along the tested CMB/bulk-flow axis and providing an additional consistency check on the monopole rejection.

### 6.4 The Saturated Integral: Finite-Coherence Temporal Topology

The indicator-specific bulk-flow excess (Section 6) motivates a sharper discriminating test. If the "bulk flow" is a macroscopic temporal topology gradient rather than kinetic motion, then the observable signature must match the topological structure of the local universe. Conventional peculiar-velocity analyses ordinarily parameterize coherent low-redshift directional residuals as kinematic bulk-flow components, decaying as $1/r$ in velocity space. In contrast, TEP predicts that the candidate macroscopic temporal component is the finite-coherence feature with a finite coherence scale $L_T$. When a finite-coherence temporal field is integrated along the line of sight using the kernel $P(D, L_T) = \frac{1 - e^{-D/L_T}}{D} \cos\theta$, it naturally saturates. The exponential saturation kernel is adopted as a minimal one-scale phenomenological representation of finite temporal coherence; $L_T$ is therefore an empirically inferred coherence scale rather than a first-principles TEP constant. This saturation can mimic a kinematic velocity flow in conventional estimators at large distances, which allows a finite-coherence temporal component to be classified observationally as a kinematic flow in a conventional reduction. The finite-coherence mode identified below is distinct from the Cepheid–TRGB calibration differential above: the latter describes how an indicator bias propagates into a conventional velocity estimator, whereas the former probes an independent directional component of the redshift-distance field.

This prediction is formally tested by deploying a continuous optimizer across the Pantheon+ supernova magnitude residuals ($z \ge 0.01$) along the dominant large-scale structure axis ($l=298^\circ, b=-7^\circ$). By allowing the optimizer to freely explore the $L_T$ parameter space, the temporal structure is tested directly against the pre-standardization Pantheon+ residuals.

The likelihood has an interior optimum at $L_T = 55.61$ Mpc rather than either limiting profile (the $L_T \to 0$ pure kinematic limit or the $L_T \to \infty$ long-coherence/unsaturated limit), with the associated directional amplitude detected at $p < 0.001$. However, because the continuous optimizer freely explores the $L_T$ parameter space, the raw $p$-value does not by itself account for the coherence-scale scan. Subject to this look-elsewhere cost, this minimization demonstrates a best-fit coherence scale of 55.6 Mpc — placing the characteristic structure on a tens-of-Mpc local-environment scale rather than the Gpc scale required by the KBC void.

### 6.5 Amplitude/Scale-Frozen CF4 Cross-Check

To test whether this finite-coherence temporal field is a universal physical feature rather than a Pantheon+ artifact, an amplitude/scale-frozen CF4 cross-check is performed at the pre-specified CF4 axis onto the CosmicFlows-4 dataset. CosmicFlows-4 (CF4) contains 51,904 non-SN galaxies with Tully-Fisher and Fundamental Plane distances spanning $D = 23$–$804$ Mpc (median $218$ Mpc).

The temporal structural model ($L_T = 55.61$ Mpc, $D_T = -0.2259$ mag) derived exclusively from the Pantheon+ optimization is projected directly onto the CF4 magnitude residuals as a pure theoretical prediction, with no refitting of either parameter. To ensure strict independence from the SN-based calibration, this test uses only non-SN CF4 tracers and computes distances directly from the independent CF4 distance moduli. The quantitative comparison yields a residual sum of squares $\mathrm{RSS}_{\rm frozen} = 11783.7$ for the frozen Pantheon+ model, against $\mathrm{RSS}_{\rm null} = 11801.5$ for the no-dipole null. The frozen model produces a marginal improvement over the no-dipole null ($\Delta\mathrm{RSS} = 17.8$ across $N = 51{,}904$ CF4 galaxies, $\sim 0.15\%$), but is slightly outperformed by the pure $1/r$ kinematic limit ($\mathrm{RSS}_{1/r} = 11776.4$, or $\Delta\mathrm{RSS} = -7.3$ vs the frozen model). The CF4 sample is dominated by galaxies at $D \gg L_T$ (79.7% at $D/L_T > 2$, median $D = 218$ Mpc), where the finite-coherence kernel $K(D,L_T) = (1-e^{-D/L_T})/D$ approaches $1/D$ and the two models become nearly degenerate. The frozen model's improvement over the null is concentrated in the transition zone ($D/L_T \sim 1$–$2$), where the kernel shape differs most from $1/r$, but the $1/r$ model performs comparably in the saturated majority, yielding a marginally lower overall RSS. The CF4 distance window therefore lacks the leverage to independently distinguish the 55.6 Mpc coherence scale from the pure $1/r$ kinematic profile.

![Amplitude/Scale-Frozen CF4 Cross-Check: Pantheon+ Model vs CF4 Data](site/figures/step_66_cross_prediction.png)

Figure 1: Amplitude/scale-frozen CF4 cross-check. The Pantheon+ derived finite-coherence temporal model ($L_T = 55.6$ Mpc, solid line) projected onto the distance-binned CF4 dipole amplitude (red circles) and Pantheon+ dipole amplitude (blue squares).

This test therefore neither confirms nor excludes the finite-coherence model — the CF4 distance distribution lacks the leverage to discriminate between the two models. Consequently, the look-elsewhere cost of the Pantheon+ continuous optimization remains un-neutralized. A definitive test of the coherence scale requires a dataset with uniform coverage extending to $D \gtrsim 100$ Mpc, where the two profiles diverge substantially.

## 7. Discriminating Observable III: $H_0(z)$ Redshift Profile Fits

The third discriminating observable tests the global redshift dependence of the inferred Hubble constant, $H_0(z)$. The primary test evaluates the published KBC redshift-dependent prediction directly against the unbinned Pantheon+ distance-modulus vector and full covariance. A binned $H_0(z)$ representation is retained only for visualization and secondary cross-checking. The evaluation covers the full redshift range ($z = 0.01$ to $z = 2.3$), with the primary statistical claim restricted to $z \ge 0.05$, the explicitly stated validity domain of the Mazurenko et al. (2025) Method-3 predictions.

*Methodological Scope (applies throughout Sections 7--8).* Pantheon+ uses a global $M_B = -19.253$ calibrated from Cepheid anchors at $z \sim 0$. Under TEP, the Cepheid clock bias is imprinted on this zero-point, and since all SNe share the same $M_B$, the bias does not vary with redshift. The TEP prediction for Pantheon+ $H_0(z)$ is therefore a flat $H_0(z) \approx 73$. The flat profile should be read as rejection of the KBC gradual decline (which predicts a decline absent in the data), not as independent positive confirmation of TEP: conventional cosmologies with a global SN calibration can also produce a flat normalization. (The compatibility of the static-manifold interpretation with the GW170817 multi-messenger bound is established via the common-mode/inter-sector argument in the foundational papers [Paper 0; TEP-HUB], where the disformal photon coupling survives as a path-dependent inter-sector observable $\Delta_{\rm siren}$ rather than a same-path speed difference.) The spatial/environmental modulation of the TEP effect (the $(1+z)^{-0.3}$ decay and host-mass dependence) must be verified via per-host Cepheid analyses (TEP-H0, Paper 11), not through the global $M_B$ regime of Pantheon+. Subsequent sections reference this methodological scope without restating the mechanism.

### 7.1 The Void Model Prediction: A Gradual Decline

The KBC/MOND model does *not* predict a sharp step at $z \sim 0.07$. The published Haslbauer, Banik & Kroupa (2020) models use Gaussian and Exponential void density profiles, and the resulting $H_0(z)$ declines *gradually*, converging to within $1\sigma$ of the Planck value only at $z \gtrsim 1.8$ (Mazurenko, Banik & Kroupa 2025, Figure 3). The Maxwell–Boltzmann profile is not included in the primary comparison because Mazurenko et al. (2025) identify it as already incompatible with the observed low-redshift bulk-flow curve; the Gaussian and Exponential profiles are the surviving Method-3 cases for which they report reasonable agreement with reconstructed $H_0(z)$. The observer is offset $\sim$100–150 Mpc from the void centre, further smoothing the transition. Evaluating a sharp step at $z \sim 0.07$ tests an unphysical idealization, not the published model.

The *published Method-3 curves* are used, digitized from Mazurenko, Banik & Kroupa (2025, MNRAS 536, 3232–3241, Figure 3). The digitized data points are stored in `data/raw/external/mazurenko_curves/` and evaluated at every supernova redshift in the Pantheon+ sample. The Gaussian and Exponential curves are nearly identical (mean $|\Delta H_0| \approx 0.13$ km/s/Mpc after objective amplitude-cut cleaning of digitization artifacts), as noted in the paper. Analytical surrogates ($\sigma_z \approx 0.82$, $z_0 \approx 0.74$) are used only as fallback if the digitized data are unavailable:

\begin{equation}
H_0^{\rm Gauss}(z) = H_{0,{\rm CMB}} + \Delta H_0 \,
e^{-z^2 / (2\sigma_z^2)}, \qquad
H_0^{\rm Exp}(z) = H_{0,{\rm CMB}} + \Delta H_0 \,
e^{-z / z_0}
\end{equation}

The primary inference uses the unbinned native $\mu$-space likelihood. All 1,701 Pantheon+ light curves and the corresponding $1701 \times 1701$ STAT+SYS covariance matrix are retained without deduplication, binning, or transformation to inferred $H_0$. The published KBC Method-3 prediction is converted from $H_0(z)$ to a relative modulus shape and evaluated directly against the observed distance-modulus vector. A secondary binned $H_0(z)$ analysis (1,543 unique SNe in 8 redshift bins with diagonal errors) is provided for visualization and cross-check.

For each observation, the reference residual is defined as

\begin{equation}
d_i = \mu_{{\rm obs},i} - \mu_{\rm ref}(z_i),
\end{equation}

where the same reference distance-redshift relation ($H_{0,\rm ref} = 73$, $\Omega_m = 0.302$) is used for every competing model. The published KBC Method-3 prediction is converted from $H_0(z)$ to a relative modulus shape,

\begin{equation}
s_i^{\rm KBC} = 5\log_{10}\!\left[\frac{H_{\rm ref}}{H_{\rm KBC}(z_i)}\right],
\end{equation}

This follows from Mazurenko et al.'s (2025) homogeneous-surrogate definition: a simulated void universe with expansion rate $H_0^{\rm sim}(z_i)$ has distance modulus $\mu_{\rm sim}(z_i) = 5\log_{10}[d_L(z_i, H_0^{\rm sim})] + 25$, so the offset relative to the reference modulus $\mu_{\rm ref}(z_i)$ is $\Delta\mu(z_i) = 5\log_{10}[H_{\rm ref}/H_0^{\rm sim}(z_i)]$ (the zero-point and comoving factors cancel in the ratio). With $H_0^{\rm sim}(z_i) = H_{\rm KBC}(z_i)$, this gives $s_i^{\rm KBC}$ above.

while the global-$M_B$ flat prediction corresponds to $s_i^{\rm flat} = 0$. Each model is permitted the same single global zero-point nuisance $\mathcal{M}$. For model $m$, the goodness-of-fit is

\begin{equation}
\chi_m^2 = (\mathbf{d} - \mathbf{s}_m - \widehat{\mathcal{M}}_m\,\mathbf{1})^T
C^{-1}
(\mathbf{d} - \mathbf{s}_m - \widehat{\mathcal{M}}_m\,\mathbf{1}),
\end{equation}

where $C$ is the full STAT+SYS covariance matrix and the analytic profiled zero-point is

\begin{equation}
\widehat{\mathcal{M}}_m = \frac{\mathbf{1}^T C^{-1}(\mathbf{d} - \mathbf{s}_m)}
{\mathbf{1}^T C^{-1}\mathbf{1}}.
\end{equation}

The Gaussian and Exponential KBC curves are frozen published predictions; no void amplitude or decay scale is refitted. Both the KBC and flat hypotheses therefore have $k = 1$ (the marginalized zero-point only), so their AIC difference is exactly their $\chi^2$ difference:

\begin{equation}
\Delta{\rm AIC} = \Delta\chi^2.
\end{equation}

The likelihood tests only the redshift-dependent shape and is independent of the common absolute distance zero-point. The primary evaluation restricts to $z \ge 0.05$, the stated validity domain of the Method-3 predictions; the full-sample extension is reported as a robustness check. The flat-model $\chi^2/{\rm dof} = 2007.7/1700 \approx 1.18$ is consistent with the Pantheon+ collaboration's own fit quality ($\chi^2/{\rm dof} \sim 1.0$–$1.2$ with the STAT+SYS covariance), reflecting residual peculiar-velocity variance and intrinsic scatter not fully captured by the released covariance. The $\Delta$AIC values are $\chi^2$ differences between models sharing the same covariance, so any overall normalization offset cancels; the rejection of the void model is based on the redshift-dependent shape difference, not the absolute $\chi^2$.

### 7.2 The TEP Prediction: Flat for Global $M_B$

The TEP framework predicts that the Cepheid calibration bias decays smoothly with redshift as the temporal shear accumulates. The physical model for the *per-host Cepheid calibration* is $H_0(z) = H_{0,{\rm CMB}} + \Delta H_0 \cdot (1+z)^{-n}$, where the exponent $n \approx 0.3$ is a phenomenological parameter, not derived from the scalar-tensor action; it is fixed empirically and governs the redshift scaling of the temporal shear field. The host-potential dependence of this prediction is tested in the companion paper TEP-H0 (Paper 11), where each host galaxy has its own Cepheid calibration; the direct redshift-dependent $(1+z)^{-n}$ decay test requires per-host Cepheid recalibration of the Pantheon+ sample.

The exponent $n$ should not be confused with the MOND acceleration scale $a_0$. The two parameters occupy fundamentally different roles in their respective frameworks. The MOND constant $a_0 \approx 1.2 \times 10^{-10}\ {\rm m\,s^{-2}}$ is a globally tuned fundamental acceleration scale that modifies the gravitational force law itself, applied uniformly across all environments and redshifts. The TEP exponent $n$, by contrast, is a localized environmental parameter governing the redshift scaling of the temporal shear field — it describes how the scalar field's influence on acoustic clock rates evolves with the local matter density along the line of sight. While $a_0$ replaces Newtonian dynamics with an empirically tuned constant, $n$ parameterizes a physical mechanism (temporal shear accumulation) within a scalar-tensor action whose structural form is fixed. While a formal derivation from $V(\phi)$ and the conformal coupling function $A(\phi)$ remains an objective of the broader programme, the parameter governs a specific physical mechanism — temporal shear accumulation — rather than acting as an ad hoc gravitational patch. As noted in the methodological scope at the start of this section, Pantheon+ uses a global $M_B$, so the TEP prediction for the SN-inferred $H_0(z)$ is a flat $H_0(z) \approx 73$ (the constant model). The $(1+z)^{-0.3}$ decay applies to the Cepheid calibrators, not to the SN-inferred $H_0(z)$ when $M_B$ is global.

### 7.3 Observational Test with Pantheon+

The primary statistical test is the frozen-prediction native $\mu$-space likelihood of Section 7.1, which evaluates the published KBC curves directly against the Pantheon+ distance-modulus vector with the full STAT+SYS covariance. That test treats the KBC predictions as fixed (no refitted amplitude or decay scale); both the KBC and flat hypotheses have $k = 1$ (the marginalized zero-point only), so $\Delta{\rm AIC} = \Delta\chi^2$ exactly. The results are reported in Section 7.4.

As a secondary diagnostic, a binned $H_0(z)$ representation is also reported. Using 1,543 supernovae from the Pantheon+ sample (Scolnic et al. 2022), $H_0(z)$ is computed in redshift bins from $z = 0.01$ to $z = 1.5$ by inverting the ΛCDM distance modulus for each SN. The binned $H_0(z)$ values are fitted against four models, each with free parameters:

- Void-Gaussian ($k=2$): $H_0(z) = H_{0,{\rm CMB}} + \Delta H_0 \, e^{-z^2/(2\sigma_z^2)}$. Free: $\sigma_z$, $\Delta H_0$.

- Void-Exponential ($k=2$): $H_0(z) = H_{0,{\rm CMB}} + \Delta H_0 \, e^{-z/z_0}$. Free: $z_0$, $\Delta H_0$.

- TEP model ($k=2$): $H_0(z) = H_{0,{\rm CMB}} + \Delta H_0 \cdot (1+z)^{-n}$. Free: $\Delta H_0$, $n$.

- Constant model ($k=1$): $H_0(z) = H_{0,{\rm const}}$ [= TEP prediction for global $M_B$]. Free: $H_{0,{\rm const}}$.

In this secondary binned representation, the AIC comparison is valid because all four models are fit with free parameters. The constant model *is* the TEP prediction for the global $M_B$ regime. This free-parameter binned analysis is distinct from the primary frozen-prediction test of Section 7.1; both are reported below.

### 7.4 Result

The observed $H_0(z)$ is flat at $\sim 73\ {\rm km\,s^{-1}\,Mpc^{-1}}$ across all redshifts, with no gradual decline towards the Planck value. The primary statistical claim restricts the evaluation to $z \ge 0.05$, the stated validity domain of the Mazurenko et al. (2025) Method-3 predictions, where the central-observer approximation holds. Over this domain, the published KBC curves are decisively rejected by the unbinned native $\mu$-space likelihood: $\Delta{\rm AIC}_{\mu} = +101.5$ (Gaussian) and $+117.1$ (Exponential), retaining all 1,053 Pantheon+ rows in range with the matched $1{,}053 \times 1{,}053$ submatrix of the native Pantheon+ STAT+SYS covariance and a marginalized common zero-point. Extending the calculation to the full Pantheon+ release (all 1,701 rows, no redshift cut) strengthens the differences to $+194.3$ and $+328.7$. A $z_{\min} = 0.01$ cut gives $+154.1$/$+257.4$ ($N = 1{,}588$); the rejection is unequivocally established within the model's own valid regime. This result aligns with Kenworthy, Scolnic & Riess (2019), who used the Pantheon SN Ia sample to search for a local void signal in the Hubble flow and independently ruled out a local underdensity as the cause of the Hubble tension. The unbinned likelihood rejection reported here reaches the same conclusion from a complementary analytical angle: evaluating the published KBC prediction curves directly against the full covariance structure of the Pantheon+ distance-modulus vector.

The secondary binned comparison (1,543 unique SNe in 8 redshift bins with diagonal errors) evaluates each model at its specific published parameter value:

| Model | Prediction | $\chi^2$ | AIC |
|---|---|---|---|
| TEP (global $M_B$) = Constant | flat $H_0(z) \approx 73.2$ | 13.8 | 15.8 (best) |
| Void-Gaussian (published) | $\sigma_z = 0.82$ | 34.0 | 36.0 |
| Void-Exponential (published) | $z_0 = 0.74$ | 93.1 | 95.1 |

The TEP flat model gives the best fit ($\chi^2 = 13.8$). The published KBC Gaussian profile is disfavoured by $\Delta{\rm AIC} = +20.2$; the Exponential profile by $\Delta{\rm AIC} = +79.3$ in this secondary binned representation. Both the binned and unbinned analyses strongly prefer the flat profile and reject the published gradual-decay predictions. Both models have $k=1$ (the marginalized zero-point only; the KBC curves are frozen published predictions with no fitted amplitude), so $\Delta{\rm AIC} = \Delta\chi^2$ exactly. The TEP flat model is clearly preferred over the actual published KBC gradual decay curves.

*Free-parameter test in native $\mu$-space.* The frozen-prediction rejection above tests the KBC curves at their published parameter values. A stronger test grants the void family free amplitude ($\Delta H_0$) and decay scale ($\sigma_z$ or $z_0$) and asks whether any member of the family improves upon flat in native $\mu$-space with the full $1701 \times 1701$ STAT+SYS covariance. The free-parameter fits yield:

*Table 5: Free-parameter void family fits in native $\mu$-space with full STAT+SYS covariance and marginalized zero-point. The void family's best fit is $\Delta H_0 = 0$ — exactly flat — for both profiles and both sample cuts. The AIC penalty for two additional free parameters ($k = 3$ versus $k = 1$) makes the void models *worse* than flat by $\Delta{\rm AIC} = +4.0$. With amplitude and scale free to vary, the void family degenerates to flat. The free-$n$ TEP family likewise collapses to $n = 0$ (flat). The a priori TEP prediction with fixed $n = 0.3$ and the physical constraint $\Delta H_0 \ge 0$ (TEP predicts $H_0$ elevated at low $z$, not suppressed) likewise collapses to $\Delta H_0 = 0$ — exactly flat — with $\Delta{\rm AIC} = +2.0$ (the AIC penalty for the extra shape parameter with no improvement). The Pantheon+ data are consistent with the TEP global-$M_B$ prediction of a flat $H_0(z)$ at all redshifts; the per-host $(1+z)^{-0.3}$ shape does not improve the fit when constrained to the correct sign.*

| Sample | Model | $\Delta H_0$ | Scale | $\chi^2$ | $\Delta{\rm AIC}$ |
|---|---|---|---|---|---|
| Full ($N=1701$) | Flat | — | — | 2007.7 | 0 (best) |
|  | Void-Gauss | 0.000 | $\sigma_z = 0.283$ | 2007.7 | +4.0 |
|  | Void-Exp | 0.000 | $z_0 = 0.283$ | 2007.7 | +4.0 |
|  | TEP (free $n$) | 10.0 | $n = 0.000$ | 2007.7 | +4.0 |
|  | TEP (fixed $n=0.3$) | 0.000 | $n = 0.3$ (fixed) | 2007.7 | +2.0 |
| $z \ge 0.05$ ($N=1053$) | Flat | — | — | 919.2 | 0 (best) |
|  | Void-Gauss | 0.000 | $\sigma_z = 0.175$ | 919.2 | +4.0 |
|  | Void-Exp | 0.000 | $z_0 = 0.175$ | 919.2 | +4.0 |

The void family's best fit is $\Delta H_0 = 0$ — exactly flat — for both the Gaussian and Exponential profiles, in both the full sample and the $z \ge 0.05$ validity domain. Given the freedom to scale, the optimizer drives the void amplitude to exactly zero. Any non-zero amplitude forces a redshift-dependent curvature that is strictly incompatible with the observational data. The AIC penalty for two additional free parameters ($k = 3$ versus $k = 1$) makes the void models worse than flat by $\Delta{\rm AIC} = +4.0$; because the decay scale is unidentified at zero amplitude, this formal penalty is descriptive only, and the inferential result is the maximum-likelihood collapse to $\Delta H_0 = 0$. When amplitude and scale are released, maximum likelihood occurs at zero void amplitude: the void family collapses to its flat limit. Combined with the frozen-prediction rejection ($\Delta{\rm AIC} = +101.5$ and $+117.1$ at $z \ge 0.05$), the void hypothesis is excluded both in its published parameters and in its best-fit parameters.

*Robustness checks:* The result is stable across redshift frames (zCMB: $+194.3$/$+328.7$; zHEL: $+219.5$/$+383.7$; zHD: $+171.4$/$+289.6$) — the Pantheon+ peculiar-velocity correction does not affect the conclusion. The result is also robust to the lower redshift cut: $z_{\min} = 0.01$ gives $+154.1$/$+257.4$ ($N = 1{,}588$); $z_{\min} = 0.023$ gives $+144.4$/$+233.4$; $z_{\min} = 0.05$ (the Mazurenko et al. 2025 validity range) gives $+101.5$/$+117.1$ ($N = 1{,}053$); even $z_{\min} = 0.10$ gives $+72.5$/$+48.4$ ($N = 960$). The void rejection survives all these cuts with $\Delta{\rm AIC} > 40$. The result is also robust to the assumed matter density: the $z \ge 0.05$ rejection ranges from $+91.5$/$+106.9$ at $\Omega_m = 0.315$ to $+118.8$/$+134.6$ at $\Omega_m = 0.280$, a spread of only $\sim 27$ units, while the canonical $\Omega_m = 0.302$ gives $+101.5$/$+117.1$.

*Digitization sensitivity.* The digitized curves are subject to graphical extraction noise. To verify that the rejection is not an artifact of digitization uncertainty, the native $\mu$-space $\Delta$AIC is recomputed after shifting both digitized curves by $\pm 0.5$ and $\pm 1.0\ {\rm km\,s^{-1}\,Mpc^{-1}}$ — a range that comfortably exceeds the scatter visible in the published figure. Table~6 reports the results:

*Table 6: Digitization sensitivity. $\Delta$AIC (native $\mu$-space, full STAT+SYS covariance) after shifting the digitized KBC curves by the indicated amount, evaluated at the KBC-preferred reference $\Omega_m = 0.302$. The rejection remains decisive under all shifts. Over the validity domain ($z \ge 0.05$, $N = 1{,}053$), even the most favourable shift leaves $\Delta{\rm AIC} \gtrsim 99$ for both profiles. Over the full release ($N = 1{,}701$), the minimum is $\Delta{\rm AIC} > 190$.*

| Shift (km/s/Mpc) | $\Delta$AIC Gaussian ($z \ge 0.05$) | $\Delta$AIC Exponential ($z \ge 0.05$) | $\Delta$AIC Gaussian (full) | $\Delta$AIC Exponential (full) |
|---|---|---|---|---|
| $-1.0$ | $+104.1$ | $+120.0$ | $+198.7$ | $+336.1$ |
| $-0.5$ | $+102.8$ | $+118.5$ | $+196.5$ | $+332.4$ |
| $\phantom{-}0.0$ | $+101.5$ | $+117.1$ | $+194.3$ | $+328.7$ |
| $+0.5$ | $+100.2$ | $+115.6$ | $+192.2$ | $+325.2$ |
| $+1.0$ | $+99.0$ | $+114.2$ | $+190.1$ | $+321.6$ |

The rejection is robust to digitization uncertainty at the level of the published figure. A $\pm 1.0\ {\rm km\,s^{-1}\,Mpc^{-1}}$ shift changes $\Delta$AIC by only $\sim 4$ units (Gaussian) and $\sim 7$ units (Exponential), confirming that the digitization noise is subdominant to the model-rejection signal. The digitized points are released as machine-readable JSON and CSV in `data/raw/external/mazurenko_curves/`.

*Forward mapping: $H_0^{\rm sim}(z) \to \mu(z)$.* The KBC $H_0(z)$ predictions are converted to modulus space via $s_i = 5\log_{10}[H_{\rm ref} / H_{\rm KBC}(z_i)]$. The justification for this mapping follows from the structure of Mazurenko et al.'s (2025) Method-3 construction.

Method-3 defines, at each redshift $z$, a homogeneous Friedmann–Robertson–Walker cosmology with fixed dimensionless expansion shape $E(z) = H(z)/H_0$ — determined by $\Omega_m$ and $\Omega_\Lambda$ — and a local Hubble constant $H_0^{\rm sim}(z)$ that varies with redshift. The luminosity distance in a flat FRW cosmology is

\begin{equation}
d_L(z, H_0) = (1+z)\,\frac{c}{H_0}\,\int_0^z \frac{dz'}{E(z')},
\end{equation}

where the comoving distance integral $D_C(z) = \int_0^z dz'/E(z')$ depends only on the dimensionless expansion shape and is independent of $H_0$. For a fixed $E(z)$, the luminosity distance scales inversely with $H_0$:

\begin{equation}
d_L(z, H_0) = \frac{(1+z)\,c\,D_C(z)}{H_0} \propto H_0^{-1}.
\end{equation}

The distance modulus is $\mu = 5\log_{10}(d_L) + 25$, so the modulus difference between a reference cosmology with $H_{\rm ref}$ and a Method-3 cosmology with $H_0^{\rm sim}(z)$ at the same redshift is

\begin{equation}
\Delta\mu(z) = 5\log_{10}\!\frac{d_L(z, H_0^{\rm sim})}{d_L(z, H_{\rm ref})}
= 5\log_{10}\!\frac{H_{\rm ref}}{H_0^{\rm sim}(z)} = s(z),
\end{equation}

since the $(1+z)\,c\,D_C(z)$ factors cancel identically. This derivation is exact for the Method-3 construction: it requires only that (i) the dimensionless expansion shape $E(z)$ is the same at all redshifts (as assumed by Method-3), and (ii) the luminosity distance is given by the FRW integral (the definition Method-3 uses to construct the homogeneous surrogate). The modulus shape $s(z)$ is therefore not an approximation or an assumption — it is the exact forward prediction of the Method-3 construction for the supernova distance modulus.

The sign of the redshift gradient is preserved: if $H_0^{\rm sim}(z)$ declines with $z$, then $s(z) = 5\log_{10}[H_{\rm ref} / H_0^{\rm sim}(z)]$ increases with $z$, and the observed flatness of the residual vector directly contradicts this prediction. The directional contradiction follows from the negative $dH_0/dz$, negative in all published KBC predictions; the quantitative $\Delta{\rm AIC}$ rejection reflects the full published amplitude and shape of the KBC profiles.

*Free-parameter comparison* (all models fit with free parameters):

| Model | $k$ | $\chi^2$ | $\chi^2_{\rm red}$ | AIC | $\Delta$AIC |
|---|---|---|---|---|---|
| Constant = TEP expectation | 1 | 13.8 | 1.98 | 15.8 | 0.0 (best) |
| TEP ($n = 0.00$, $\Delta H_0 = 5.85$) | 2 | 13.8 | 2.31 | 17.8 | +2.0 |
| Void-Gaussian ($\sigma_z \to 10$, $\Delta H_0 = 5.85$) | 2 | 13.9 | 2.32 | 17.9 | +2.1 |
| Void-Exponential ($z_0 \to 10$, $\Delta H_0 = 5.97$) | 2 | 17.4 | 2.91 | 21.4 | +5.6 |

In the free-parameter comparison, both void profiles push their decay scales to the boundary ($\sigma_z \to 10$, $z_0 \to 10$), effectively converting themselves into flat models. The TEP model fits to $n \approx 0$, exactly as predicted for the global $M_B$ regime. The $n \approx 0$ result is not a degenerate outcome; it is the expected signature of a calibration architecture in which the Cepheid clock bias is encoded in a single global zero-point rather than distributed across individual host calibrations.

### 7.5 Interpretation

The $H_0(z)$ data rejects the published KBC/MOND gradual decay curves. Within the model's own stated validity domain ($z \ge 0.05$), the unbinned native $\mu$-space likelihood disfavours the Gaussian profile by $\Delta{\rm AIC} = +101.5$ and the Exponential by $+117.1$. The secondary binned analysis gives $\Delta{\rm AIC} = +20.2$ and $+79.3$ respectively. The TEP flat prediction (constant $H_0(z) \approx 73.2$ for global $M_B$) gives the best fit in both representations. When allowed free parameters, both void profiles escape their own predictions by pushing their decay scales to infinity, converting themselves into the flat model that TEP already predicts.

The flat $H_0(z) \approx 73$ is the expected TEP signature when the Cepheid calibration bias is imprinted on the global $M_B$ zero-point. The TEP prediction chain operates as follows. At $z \sim 0$, Cepheid calibrators carry the maximal acoustic clock bias, producing the full $(1+z)^{-0.3} \approx 1$ compression. The global $M_B = -19.253$ inherits this bias, calibrated from the biased Cepheid distances, encoding the full clock bias in the zero-point. Because all SNe use the same $M_B$, the bias does not vary with redshift — $H_0(z)$ is predicted to be flat at $\sim 73$. A global $M_B$ sets the absolute vertical intercept but does not constrain the shape: if a local void were physically present, the distance moduli would diverge from the $\Lambda$CDM curve at low redshift regardless of which global $M_B$ was adopted. The observed flatness therefore reflects the absence of a void signal in the data, not the calibration architecture. Under per-host Cepheid calibration (TEP-H0, Paper 11), the $(1+z)^{-0.3}$ decay would instead appear, because each SN would inherit the bias from its own host's Cepheid calibration, not from a global zero-point.  The methodological scope stated at the opening of this section applies here in full: a global $M_B$ sets the absolute normalization of $H_0(z)$ but does not force the profile to be flat. If a local void were physically present, the Pantheon+ distance moduli would deviate from the $\Lambda$CDM prediction at low redshifts, producing a declining $H_0(z)$ curve irrespective of the chosen zero-point. The observed flatness reflects the absence of such a void signal in the data. The test falsifies the KBC gradual decline; it does not independently confirm TEP, because conventional cosmologies with a global SN calibration also predict a flat normalization.

### 7.6 Comparison with Jia et al. (2023): Proper Replication and Source of the Decline

Mazurenko et al. (2025) report that their Method-3 KBC $H_0(z)$ curves show "reasonable agreement" with the decorrelated $H_{0,z}$ reconstruction of Jia, Hu & Wang (2023, A&A 674, A45), who find a declining $H_0(z)$ at $5.6\sigma$ using Pantheon+ combined with $H(z)$ and BAO data. This subsection examines whether that agreement reflects a shared physical signal or a shared methodological feature.

The methodological distinction is fundamental. Jia et al. reconstruct piecewise $H_{0,z_i}$ parameters in redshift bins using a cumulative piecewise $H_{\rm th}(z')$ construction (their Equation 8), evaluate the luminosity-distance integral through that piecewise $H_{\rm th}$ (their Equation 18), and compare the decorrelated *derived parameters* with theoretical predictions. The native $\mu$-space likelihood (the modulus residual and AIC equations) evaluates the frozen KBC distance-modulus prediction directly against the underlying Pantheon+ observable. These are not equivalent operations: one tests a reconstructed parameterization, the other tests the original observable.

A proper replication of Jia et al.'s analysis was performed using their public code repository (github.com/JoJo20221003/Hz-Code) as reference. The replication uses Jia's actual 8-bin equal-width partition ($z = [0, 0.1, 0.2, 0.3, 0.4, 0.55, 0.7, 1.0, 2.4]$ — note that the code uses 8 bins, not the 10 bins stated in the paper), the full $1701 \times 1701$ Pantheon+ STAT+SYS covariance matrix, MCMC posterior sampling with *emcee* (32 walkers, 2000 steps), and PCA decorrelation per Jia et al.'s Equations 19–22. The $H(z)$ data (59 measurements including BAO-derived $H(z)$ at $z > 2$) were taken directly from Jia et al.'s repository. Two configurations were tested: (A) SN-only with full covariance, and (B) SN + $H(z)$ with full covariance, matching Jia et al.'s actual code.

The results isolate the origin of the declining trend. With SN-only data (configuration A), the MCMC fit yields a change of $-4.26$ km/s/Mpc from low-$z$ to high-$z$, but with a significance of only $2.51\sigma$ — not statistically significant. The high-redshift bins have large uncertainties ($\sigma_{H_0} \sim 7$ km/s/Mpc at $z > 0.7$) because Pantheon+ contains few SNe at those redshifts. This is consistent with Jia et al.'s own statement that the SN-only case has "poor constraints" at high redshift and that they "decided to add the observed Hubble parameter data and BAO data" to obtain tighter constraints.

With SN + $H(z)$ data (configuration B), the MCMC fit yields a change of $-5.92$ km/s/Mpc at $6.27\sigma$ (correlated) or $-5.92$ km/s/Mpc at $5.21\sigma$ after PCA decorrelation. The decline is present, but its significance ($5.21\sigma$ decorrelated) is lower than Jia et al.'s reported $5.6\sigma$, likely due to differences in binning (8 versus 10 bins), MCMC chain length, and the exact $H(z)$ dataset. The qualitative conclusion is the same: the declining $H_0(z)$ is driven by the $H(z)$ cosmic chronometer data, not by the Pantheon+ SN distance moduli alone.

The origin of the Jia et al. decline is therefore identified: it arises from the $H(z)$ and BAO data combined with the SN data, not from the Pantheon+ SN distance moduli alone. The SN-only configuration, using the full covariance and the correct piecewise $H_{\rm th}$ estimator, does not produce a significant decline ($2.51\sigma$). The native $\mu$-space likelihood likewise rejects the KBC gradual decay curves. An independent Pantheon+ tomographic analysis (Wang 2023, Eur. Phys. J. C 83, 813) found no obvious evidence for evolution of $H_0$ or $\Omega_m$ at the $2\sigma$ level using both equal-redshift and equal-count binning, consistent with the flat profile reported here.

This reconciliation does not dispute the Jia et al. result within its own methodological framework. The apparent agreement between KBC and the Jia reconstruction is dataset-dependent: the decline requires the combined SN+$H(z)$+BAO dataset and does not arise from the Pantheon+ SN distance moduli alone. The direct likelihood comparison to the primary observable — the distance modulus — is the more conservative test, and it rejects the KBC prediction.

The forward mapping derived above (the relative modulus shape relation) establishes that the modulus shape $s(z) = 5\log_{10}[H_{\rm ref}/H_0^{\rm sim}(z)]$ is the exact prediction of the Method-3 construction for the supernova distance modulus. Method-3 explicitly defines, at each redshift, a homogeneous FRW cosmology with fixed density parameters $\Omega_m$, $\Omega_\Lambda$ and a local Hubble constant $H_0^{\rm sim}(z)$ that varies to reproduce the apparent scale factor at the required lookback time. For such a homogeneous surrogate, $d_L \propto H_0^{-1}$ at fixed $z$ and $\Omega_i$, so the modulus conversion is not an assumption but a direct consequence of the Method-3 definition. The $\Delta$AIC $\sim 100$ rejection is therefore a direct test of the published Method-3 homogeneous-surrogate prediction as displayed in Figure 3 of Mazurenko et al. (2025). A full inhomogeneous ray-traced calculation would be a separate, stronger test, but is not necessary to establish what the published Figure 3 of Mazurenko et al. (2025) predicts for the supernova distance modulus.

## 8. Observable III (continued): Calibration-Independent Relative Evolution

This is a complementary view of the $H_0(z)$ redshift-profile test (Section 7) that cancels the common zero-point. Rather than fitting the global $H_0(z)$ curve with the unbinned likelihood, this test measures the *relative evolution* between low-redshift and high-redshift bins. The formal statistic is the ratio $R_H = H_0(z > 0.25) / H_0(0.05 \le z < 0.15)$, or equivalently $\Delta \ln H_0 = \ln R_H$. A common distance-modulus zero-point shift rescales all inferred $H_0$ values by the same multiplicative factor ($H_0 \to a H_0$), which cancels identically in the ratio. The additive difference $\Delta H_0 = H_0(z > 0.25) - H_0(0.05 \le z < 0.15)$ is retained as an intuitive calibrated representation, but the ratio is the formally calibration-independent quantity.

The void model predicts $\Delta H_0 < 0$: the locally inferred $H_0$ should decline from the inflated local value toward the CMB value as observations extend beyond the void wall. The TEP framework predicts $\Delta H_0 \approx 0$: with global $M_B$, the Cepheid clock bias is encoded in the zero-point and does not vary with redshift, so $H_0$ should be flat at all redshifts.

### 8.1 Test Design

Using the 1,701 Pantheon+ observations (1,543 unique supernovae, with duplicate survey observations retained to preserve the native $1701 \times 1701$ covariance structure), $H_0(z)$ is computed in redshift bins from $z = 0.01$ to $z = 2.3$, split by host galaxy stellar mass at the canonical threshold $\log_{10}(M_*/M_\odot) = 10.0$. The primary metric is the ratio $R_H = H_0(z > 0.25) / H_0(0.05 \le z < 0.15)$, evaluated on the full sample; host-mass subsets are retained as secondary robustness checks. For each SN, $H_0$ is inferred by inverting the ΛCDM distance modulus:

\begin{equation}
H_0 = \frac{(1+z)\,c\,\int_0^z dz'/E(z')}{10^{(\mu - 25)/5}}
\end{equation}

where $E(z) = \sqrt{\Omega_m(1+z)^3 + (1-\Omega_m)}$ and $\mu$ is the observed distance modulus. The Pantheon+ distance moduli ($\mu_{\rm SH0ES}$) use $M_B = -19.253$ calibrated from Cepheid anchors at $z \sim 0$; therefore the absolute $H_0$ at any redshift inherits the Cepheid zero-point as its absolute normalization and is *not* an independent measurement of SH0ES versus Planck. The scientifically meaningful test is the *relative evolution*: the common zero-point cancels in the ratio $R_H$.

### 8.2 Result: $R_H \approx 1.009$ — Consistent with Flat, $\sim 8\sigma$ Rejection of KBC

The primary metric is the calibration-independent ratio. A joint generalized least-squares (GLS) fit of the two-bin intercepts using the full Pantheon+ STAT+SYS covariance matrix over the full sample ($N_{\rm low} = 178$, $N_{\rm high} = 614$) gives $H_0^{\rm low} = 73.08\ {\rm km\,s^{-1}\,Mpc^{-1}}$ and $H_0^{\rm high} = 73.75\ {\rm km\,s^{-1}\,Mpc^{-1}}$, yielding

\begin{equation}
R_H = \frac{H_0(z > 0.25)}{H_0(0.05 \le z < 0.15)} = 1.009 \pm 0.006,
\end{equation}

consistent with flat $H_0(z)$ at $1.5\sigma$. The KBC Gaussian profile predicts $R_H^{\rm KBC} = 0.9569$ (a $\sim 4.3\%$ decline) when evaluated through the same two-bin GLS covariance-aware estimator used for the observed $R_H$ (the KBC model shift $s_i = 5\log_{10}(H_{\rm ref}/H_{\rm KBC}(z_i))$ is fed through the identical GLS zero-point operator in each bin); the Exponential predicts $R_H^{\rm KBC} = 0.9494$. The frozen KBC curves are evaluated at every supernova redshift in the same low ($0.05 \le z < 0.15$) and high ($z > 0.25$) bins used for the observed $R_H$. The covariance-aware significance of the rejection is

\begin{equation}
Z = \frac{R_{H,\rm obs} - R_{H,\rm KBC}}{\sigma_{R_H}}
= 8.4\sigma \quad \text{(Gaussian)},
\end{equation}

and $9.7\sigma$ for the Exponential profile. The void model predicts $R_H < 1$ (decline toward CMB); the data show $R_H \approx 1$ (no decline). The TEP prediction ($R_H \approx 1$ for global $M_B$) is consistent with the observed near-unity ratio. Because both redshift bins share the same global $M_B$ calibration, a common distance-modulus zero-point shift rescales all inferred $H_0$ values by an identical multiplicative factor ($H_0 \to a H_0$), which cancels identically in the ratio $R_H$. The uncertainty $\sigma_{R_H}$ is obtained analytically from the joint GLS covariance: $\sigma_{R_H} = R_H \cdot \sqrt{{\rm Var}(\alpha_{\rm high} - \alpha_{\rm low})} \cdot \ln 10 / 5$, where ${\rm Var}(\alpha_{\rm high} - \alpha_{\rm low}) = \sigma_{\alpha_{\rm low}}^2 + \sigma_{\alpha_{\rm high}}^2 - 2\, {\rm Cov}(\alpha_{\rm low}, \alpha_{\rm high})$, and the cross-covariance is computed from the off-diagonal block of the Pantheon+ STAT+SYS matrix. A verification script (`scripts/verify_rh_gls_matched.py`) confirms that the matched-GLS significance (8.4$\sigma$/9.7$\sigma$) is slightly more conservative than the arithmetic-mean ratio (9.2$\sigma$/10.2$\sigma$) and is the quoted value throughout.

The absolute $H_0$ values at high $z$ are not independent measurements: Pantheon+ uses $\mu_{\rm SH0ES}$ with $M_B = -19.253$ from Cepheid anchors, so the Cepheid zero-point sets the absolute normalization. The decisive test is the relative evolution, not the absolute value. The global model-fit comparison (Gaussian and Exponential decay profiles versus flat $H_0$) is presented in Section 7. A host-mass-split binned $\Delta$AIC comparison (using the fixed KBC predictions versus flat $H_0$ in each host-mass subset) gives $\Delta$AIC $= +11.7$ (massive, Gaussian), $+11.5$ (low-mass, Gaussian), $+40.0$ (massive, Exponential), and $+42.4$ (low-mass, Exponential), confirming the same conclusion from the curve-fitting angle: the KBC rejection holds in both host-mass subsets independently.

### 8.3 Interpretation

The calibration-independent ratio $R_H = 1.009 \pm 0.006$ falsifies the void model's central prediction without relying on any absolute $H_0$ calibration. The void hypothesis requires the tension to be a function of macroscopic position within the void: $H_0$ must decline as observations extend beyond the void wall. The data show no decline; if anything, $H_0$ slightly increases. The TEP expectation, that the tension is governed by the local gravitational environment of each host galaxy, not by Earth's position in a cosmic underdensity, is consistent with the observed near-unity ratio. The $+0.9\%$ fractional evolution is well within the envelope of high-$z$ selection effects (Malmquist bias): the Pantheon+ SALT2 bias corrections assume a fiducial cosmology, and residual selection bias at $z > 0.25$ can mimic a slight luminosity increase. The critical finding is the absence of a decline, not the precise value of the near-zero fractional change.

A critical methodological distinction: the absolute $H_0 \approx 73$ at $z > 0.25$ is *not* an independent measurement of SH0ES versus Planck. The Pantheon+ distance moduli use $\mu_{\rm SH0ES} = m_B - M_{\rm SH0ES}$, where $M_{\rm SH0ES} = -19.253$ was determined from SH0ES Cepheid-host distances. Therefore $H_0 = 73$ at high redshift is mathematically forced by the local Cepheid calibration. The scientifically meaningful test is the *relative* evolution: the KBC model predicts a decline, TEP predicts flat, and the data are flat. The per-host Cepheid analysis in TEP-H0 (Paper 11) is needed to test the redshift-dependent $(1+z)^{-0.3}$ decay directly.

Consistent with the methodological scope stated at the opening of Section 7, Pantheon+'s global $M_B$ calibration tests the spatial persistence of the tension, not its host-mass dependence. A computational proof is provided in the TEP-VOID pipeline, which releases the global $M_B$ constraint and fits $M_B$ separately for massive and low-mass hosts. The residual mass step is only $0.013$ mag after the existing SALT2 mass correction and global-$M_B$ calibration, demonstrating that little host-mass structure remains in the released Pantheon+ moduli. This is consistent with masking of the TEP-predicted host dependence ($\sim 0.05$ mag); recovering that dependence requires the per-host Cepheid recalibration performed in TEP-H0 (Paper 11).

## 9. TEP Correction: Two-Channel Calibration Bias

Sections 5 through 8 have established that the published KBC/MOND gradual decay curves are rejected by the observed flat $H_0(z)$ profile. This section quantifies the physical scale of the TEP calibration bias by tracing the correction through two distinct channels: the Cepheid period-transport channel (calibrator hosts $\to$ $M_B$ zero-point) and the SN light-curve stretch channel (SN standardization $\to$ Hubble-flow residuals). The Cepheid channel is directly measured; the SN stretch channel is a falsifiable prediction of the same transport mechanism. The data tell a consistent story across multiple scales. The strongest evidence comes from single-galaxy differential tests: internal radial Period--Luminosity gradients within M31 ($\Delta W = +0.681 \pm 0.187$ mag, $3.65\sigma$ from HST PHAT photometry, Kodric et al. 2018) and the LMC ($\Delta W = +0.0284 \pm 0.0086$ mag, $3.30\sigma$ from OGLE-IV) independently detect the predicted clock-gradient signal free from host-to-host peculiar velocity systematics. At the cosmological level, the redshift-only WLS regression in $H_0$ space across 33 Hubble-flow hosts yields $\kappa_{\rm Cep} = (0.45 \pm 0.22) \times 10^6$ mag ($2.05\sigma$ at $\sigma_v = 150$ km/s), with the joint multi-block likelihood returning $1.58\sigma$ as a consistency check. The supernova $X_i$-step emerges at $1.47\sigma$ in the TEP-predicted direction ($N=1470$ Hubble-flow), placing the longstanding host-mass residual in a concrete, falsifiable timescale-bias framework. These multi-scale detections align in both direction and order of magnitude to span the gap. The definitive per-host recalibration is left to the companion TEP-H0 analysis.

### 9.1 The Two-Channel Taxonomy

The TEP framework distinguishes two classes of distance indicator by the physical quantity that sets their standardization. The first class — *acoustic clocks* — includes Cepheid variables, whose period is the acoustic crossing time of the stellar envelope (Section 4.4). The second class comprises *non-timescale distance indicators*, including the TRGB, JAGB, and SBF. Their standardizations are rooted in nuclear ignition thresholds or statistical stellar-population luminosities—neither of which requires transporting a redshift-corrected timescale to the rest frame. A third category, previously unrecognized in this framework, occupies an intermediate position: *partially time-standardized indicators*, whose peak luminosity is nuclear physics but whose empirical standardization involves a timescale.

Type Ia supernovae belong to this third category. The SALT2/SALT3 standardization relation is $\mu = m_B - M_B + \alpha\,x_1 - \beta\,c + \Delta_{\rm host}$, where $x_1$ is the light-curve stretch — the timescale of the photospheric diffusion through the ejecta. The peak luminosity is nuclear physics; the light-curve width by which it is standardized is a clock. Under any framework in which clock rates respond to environment, SN stretch inherits an environment-dependent bias that propagates into the standardized magnitude through the $\alpha\,x_1$ term. TRGB, JAGB, and SBF anchors do not carry this bias because their standardization does not involve a timescale.

This taxonomy resolves a structural tension in the distance-ladder literature. On common galaxy samples, all indicators converge to $H_0 \approx 72$–$73$ (Section 2.5); on full ladders with distinct calibrator populations, they diverge (Section 2.7). Both observations are explained by the two-channel model: common-sample comparisons share the SN stretch channel (all indicators converge high), while full-ladder comparisons differ by the Cepheid channel (acoustic clocks biased, non-timescale indicators not).

### 9.2 Channel 1: The Cepheid Period-Transport Chain

The Cepheid-channel calibration bias operates through a specific physical chain. The TEP correction is calculated on the *Cepheid calibrator hosts* — the galaxies whose Cepheid distances set the global $M_B = -19.253$ zero-point. The mean correction over those calibrators determines a single shift $\Delta M_B^{\rm Cep}$, which then propagates uniformly to *all* Pantheon+ supernovae:

\begin{equation}
X_{\rm Cepheid\ calibrator}
\;\longrightarrow\;
\Delta\mu_{\rm Cep}
\;\longrightarrow\;
\Delta M_B^{\rm Cep}
\;\longrightarrow\;
\text{all Hubble-flow SNe}
\end{equation}

The potential of an arbitrary high-redshift SN host does not enter this chain. The Cepheid channel affects only the Cepheid calibrators that set $M_B$, not the SNe themselves. The SN stretch channel (Section 9.6) operates independently on the Hubble-flow SNe.

### 9.3 The Cepheid Modulus Correction

Under TEP, the Cepheid-derived distance modulus in a calibrator host with gravitational potential coordinate $X_i$ is biased by the clock-rate differential. Two channel coefficients are distinguished:

\begin{equation}
\Delta\log_{10}P = -\kappa_P\, X_i, \qquad
\kappa_{\rm Cep} = -b\,\kappa_P
\end{equation}
\begin{equation}
\boxed{ \delta\mu_i^{\rm raw}=-\kappa_{\rm Cep}X_i } \qquad \text{and} \qquad \boxed{ \Delta\mu_i^{\rm corr}=+\kappa_{\rm Cep}X_i }
\end{equation}

where $\kappa_P$ is the dimensionless period-response coefficient (governing Cepheid period contraction for $X_i > 0$ in massive hosts), $b \approx -3.26$ is the near-infrared Leavitt law slope, and $\kappa_{\rm Cep}^{\rm equiv} = (0.365 \pm 0.304) \times 10^6\ {\rm mag}$ is the Cepheid-channel response coefficient from the endpoint slope conversion in TEP-H0 (Paper 11, Section 4). Here $X_i = (S_{\rm total}\, U_i - U_{\rm ref}^{\rm scr}) / c^2$ is the dimensionless screened potential coordinate, with $U_i = u_\phi^2$ the rotation-based potential proxy, $S_{\rm total} \le 1$ the screening factor that attenuates the potential for extended sources, and $U_{\rm ref}^{\rm scr} = (30.507\ {\rm km\,s^{-1}})^2$ the screened anchor reference potential. The correction is positive for massive calibrators: Cepheid distances are compressed, so the true distance modulus is larger than the observed value.

A note on notation. Two estimates of the Cepheid-channel coefficient appear in this paper: $\kappa_{\rm Cep}^{\rm equiv} = (0.365 \pm 0.304) \times 10^6$ (the endpoint-slope conversion from TEP-H0, used in the matrix propagation) and $\kappa_{\rm Cep} = (0.45 \pm 0.22) \times 10^6$ (the redshift-only WLS estimate in $H_0$ space at $\sigma_v = 150$ km/s, used in the DHOST consistency analysis of Section 4.6). These are the same physical coefficient estimated by two independent methods. The difference ($0.087 \times 10^6$) is $0.23\sigma$ relative to the combined uncertainty, confirming consistency. The matrix propagation uses $\kappa_{\rm Cep}^{\rm equiv}$ because it is the direct endpoint-slope conversion; the DHOST analysis uses $\kappa_{\rm Cep}$ because it is the regression-optimized value from the $H_0$-space WLS fit.

### 9.4 Channel 1 Application: Calibrator $\Delta M_B^{\rm Cep}$ Propagation

The TEP correction is applied to the Cepheid calibrator hosts with measured rotation velocities from the host potential catalog. The mean correction over these calibrators determines the zero-point shift $\Delta M_B$:

\begin{equation}
\Delta M_B = \kappa_{\rm Cep}^{\rm equiv} \cdot \langle X_i \rangle_{\rm calibrators}
\end{equation}

This single $\Delta M_B$ is then applied uniformly to all Pantheon+ supernovae, shifting the Hubble residual by a constant offset. The corrected distance moduli are used to recompute Hubble residuals against the $\Lambda$CDM prediction at the CMB-inferred $H_0 = 67.4\ {\rm km\,s^{-1}\,Mpc^{-1}}$.

### 9.5 Channel 1 Result: Direct Shift and the Amplitude Bound

The TEP correction shifts the mean Hubble residual by $+0.035 \pm 0.030$ mag (equiv closure, $\kappa_{\rm Cep}^{\rm equiv} = 0.365 \times 10^6$ mag, calibrator-only $\langle X_i \rangle$) in the direction predicted by TEP (reducing the negative residual caused by Cepheid distance compression). The uncertainty combines the imported $\kappa_{\rm Cep}^{\rm equiv}$ posterior with the variance of the mean calibrator potential $\langle X_i \rangle$: $\sigma_{\Delta M_B}^2 = (\sigma_{\kappa_{\rm Cep}^{\rm equiv}} \langle X_i \rangle)^2 + (\kappa_{\rm Cep}^{\rm equiv} \sigma_{\langle X_i \rangle})^2$. The $\kappa_{\rm Cep}^{\rm equiv}$ term dominates ($\sigma_{\kappa_{\rm Cep}^{\rm equiv}}/\kappa_{\rm Cep}^{\rm equiv} = 0.304/0.365 \approx 83\%$), while the $\langle X_i \rangle$ contribution is subdominant. The standard deviation of the residuals is unchanged ($0.183$ mag), confirming that the correction acts as a constant zero-point offset rather than reducing scatter — exactly as expected when $M_B$ is global.

The direct shift of $+0.035 \pm 0.030$ mag is a simple calibrator-average estimator using the endpoint-slope $\kappa_{\rm Cep}^{\rm equiv} = 0.365 \times 10^6$ mag applied to the screened calibrator-only $\langle X_i \rangle$ via cross-validation. The Hubble tension demands a mean calibrator correction of $\Delta\mu_{\rm tension} = 5\log_{10}(73.0/67.4) \approx 0.174$ mag. Two propagation routes exist, yielding different results:

*(i) SH0ES design-matrix propagation.* Propagating the endpoint-slope $\kappa_{\rm Cep}^{\rm equiv}$ through the 3,490-row SH0ES design matrix yields $H_0 = 71.77 \pm 0.99\ {\rm km\,s^{-1}\,Mpc^{-1}}$ (Paper 11, Section 3.5) — a partial reduction from 73.04, because the 37 unconstrained latent host moduli $\mu_i$ algebraically absorb host-level environmental shifts (Paper 11, Section 4.2). The maximum per-host correction with $\kappa_{\rm Cep}^{\rm equiv}$ is $\kappa_{\rm Cep}^{\rm equiv} \cdot X_{\rm max} = 0.365 \times 10^6 \times 3.28 \times 10^{-7} \approx 0.120$ mag (at M101). A propagation audit confirms: the mean calibrator correction is $+0.039 \pm 0.019$ mag (using the redshift-only WLS $\kappa_{\rm Cep} = 0.45 \times 10^6$), or $+0.035 \pm 0.030$ mag using the endpoint-closure $\kappa_{\rm Cep}^{\rm equiv}$, consistent with the maximum per-host bound.

*(ii) Unified host-level reconstruction (Step 04).* Paper 11's Step 04 bypasses the matrix degeneracy by correcting each host modulus in expansion-rate space and re-optimizing $\kappa_{\rm Cep}$ to flatten the environmental gradient ($\partial H_{0,i} / \partial u_{\phi,i} \to 0$). This yields $H_0 = 66.65 \pm 1.58\ {\rm km\,s^{-1}\,Mpc^{-1}}$, consistent with Planck at $0.45\sigma$. The Step 04 reconstruction uses a larger effective $\kappa_{\rm Cep}$ than the likelihood-derived value; the discrepancy between routes (i) and (ii) reflects the latent-$\mu_i$ absorption degeneracy documented in Paper 11, not a contradiction.

The Cepheid channel provides the directly measured calibration bias. TEP additionally predicts an independent SN timescale channel whose amplitude is constrained by the host-mass phenomenology and is directly testable through $X_i$-dependent Hubble residuals (Section 9.6). The SN channel is not required to rescue the Cepheid reconstruction; it is a separate, falsifiable prediction of the same underlying transport mechanism.

### 9.6 Channel 2: The SN Light-Curve Stretch Bias

The SALT2/SALT3 standardization relation $\mu = m_B - M_B + \alpha\,x_1 - \beta\,c + \Delta_{\rm host}$ corrects the observed peak magnitude using the light-curve stretch $x_1$, which parameterizes the timescale of photospheric diffusion through the ejecta. The stretch $x_1$ is a time-domain observable derived from the light-curve width, and is therefore governed by the local proper time rate: under TEP, a clock-rate differential in the SN host environment produces a stretch bias $\Delta x_1$ that propagates into the standardized magnitude as $\Delta m_B^{\rm SN} = \alpha\,\Delta x_1$.

The SN channel acts wherever SN light-curve stretch is standardized; its contribution to $H_0$ is set by the differential environmental bias between the calibrator-SN and Hubble-flow-SN host populations. It is therefore structurally distinct from the Cepheid channel (which operates through the period-transport calibration chain) and additive with it. Non-timescale distance indicators (TRGB, JAGB, SBF) do not carry this bias because their standardization does not involve a timescale. The two-channel structure is:

\begin{equation}
\Delta M_B^{\rm total} = \Delta M_B^{\rm Cep}
+ \Delta M_B^{\rm SN\ stretch}
\end{equation}

where $\Delta M_B^{\rm Cep}$ is the Cepheid calibration bias (measured directly from the matched-host divergence and the likelihood analysis) and $\Delta M_B^{\rm SN\ stretch} \sim 0.04$–$0.10$ mag is the predicted SN timescale bias, bounded by the observed SN Ia host-mass step. The SN stretch channel amplitude is not yet independently constrained from first principles; the range shown is bounded by the observed host-mass step. The falsifiable test — the $X_i$-step in Pantheon+ residuals (Section 10.4) — is needed before this channel counts as evidence rather than a prediction. The fiducial choice $\eta_{\rm SN} \sim 1/2$, motivated by the common rank-1 transport structure (Section 4.9), provides the structural motivation.

The SN Ia host-mass step — a residual correlation of $\sim 0.04$– $0.06$ mag between Hubble residuals and host stellar mass after SALT3 standardization (Section 2.6) — is the observational signature predicted by the SN stretch channel. The step has persisted for approximately 15 years without a unique physical explanation. Under TEP, it arises naturally: more massive hosts reside in deeper gravitational potentials, producing a larger disformal coupling and a correspondingly larger stretch bias. The TEP prediction is falsifiable: the step should correlate with the potential coordinate $X_i$ (or an equivalent bulge-concentration measure) rather than with stellar mass per se, and the correlation should persist after the SALT3 mass correction is applied. Pantheon+ provides the data to test this prediction directly.

### 9.7 Channel Amplitudes

The two-channel amplitudes are summarized in Table 7. The Cepheid channel is directly measured. The predicted host-potential dependence of SN stretch remains an independent, uncalibrated prediction to be tested. Closing this gap requires radiative-transfer simulations of SN Ia light curves in a disformal metric with environment-dependent $g_{0i}$ structure, or alternatively an empirical calibration against a sample with both measured $V_{\rm rot}$ and independent Cepheid distances permitting a direct $\Delta M_B^{\rm SN}$–$x_1$ cross-anchor.

*Table 7: Two-channel amplitude summary. Channel 1 (Cepheid period transport) is measured from the matched-host divergence and the likelihood analysis. Channel 2 (SN light-curve stretch) host-potential dependence remains an uncalibrated prediction.*

| Channel | Mechanism | Amplitude range | Observational constraint |
|---|---|---|---|
| Cepheid period transport | $\kappa_{\rm Cep} \cdot X_i$ | $\sim 0.02$–$0.09$ mag (per host) | Matched-host Cepheid–TRGB divergence (JWST $N=17$: $\Delta\mu = -0.023 \pm 0.022$, $1.02\sigma$; filter-corrected $-0.042 \pm 0.024$, $1.77\sigma$); $\kappa_{\rm Cep} = (0.45 \pm 0.22) \times 10^6$ mag (redshift-only WLS, $2.05\sigma$); M31 ($3.65\sigma$) and LMC ($3.30\sigma$) internal gradients; Step 04 reconstruction yields $H_0 = 66.65 \pm 1.58$ |
| SN light-curve stretch | $\alpha \cdot \Delta x_1(X_i)$ | SN Ia host-mass step ($0.057 \pm 0.018$ mag raw; $\sim 0.04$–$0.06$ mag after SALT3 host correction); HR channel null after $x_1$ absorption (pending decisive measured-$V_{\rm rot}$ sample test) |

The Cepheid channel is the directly measured calibration bias. The SN stretch channel remains a falsifiable host-potential prediction; an independently calibrated $x_1(X_i)$ test with a decisive measured-$V_{\rm rot}$ sample remains outstanding. The two channels are additive and both scale with $X_i$, but the paper does not depend on the SN channel to balance the amplitude budget — the Cepheid channel reconstruction (Paper 11, Step 04) already yields $H_0 = 66.65 \pm 1.58\ {\rm km\,s^{-1}\,Mpc^{-1}}$.

The two-channel taxonomy is qualitatively consistent with the range of $H_0$ values spanned by the four indicator classes (Table 1, Section 2.4): JAGB ($H_0 = 67.80$, low-mass hosts), TRGB ($68.81$, mixed), Cepheids ($73.0$, massive spirals), and SBF ($74.6$, massive early-types). Under the two-channel model, deeper-potential calibrator populations carry larger clock biases through both channels: the Cepheid channel biases the period-transport calibration, and the SN stretch channel biases the Hubble-flow SNe selected from those host populations. This observation is reported as suggestive only and is not advanced as a statistical test of the framework. A weighted linear fit of $H_0$ against the mean potential coordinate $\langle X \rangle$ for each ladder's calibrator population yields $H_0 = 68.8 + 1.7 \times 10^7 \langle X \rangle$, with the four indicators spanning $\langle X \rangle \approx +0.3 \times 10^{-7}$ (JAGB) to $+3.5 \times 10^{-7}$ (SBF). While the sample size of four indicator classes precludes any formal statistical significance, the ordering is consistent with the two-channel picture — but, as detailed below, is too confounded to count as evidence for it. The two-channel model expects this ordering to persist under refinement; because the four classes are mutually confounded, however, persistence would be suggestive rather than confirmatory even with more data, unless the confounds are broken by matching hosts across indicators. The four indicator classes are moreover deeply confounded with known method-specific systematics — JAGB and TRGB are measured in nearby, lower-mass, mixed-morphology hosts with ground- and space-based photometry distinct from the SH0ES Cepheid sample, while SBF is measured exclusively in massive, dust-free early-type galaxies using fluctuation statistics with well-documented stellar-population-age systematics — so host morphology, dust content, stellar-population age, and photometric method vary jointly with potential depth across the four classes. The ordering has been noted informally in the Hubble-tension literature and attributed to sample selection and stellar-population effects specific to each method. A plot of this ordering is available in the reproducibility archive. The two-channel model predicts that this ordering will persist under refinement, a directional expectation that future data with larger indicator samples can test. The discriminating power of the TEP framework against the void model rests on the redshift-profile falsification in Sections 7--8, not on this four-point observation.

The discriminating power of the TEP framework against the void model comes from the redshift-profile falsification in Sections 7--8, evaluated through complementary absolute-shape and relative-evolution statistics. The flat $H_0(z)$ profile rejects the published KBC gradual decay curves (digitized from Mazurenko et al. 2025) at $\Delta{\rm AIC} = +20.2$ for Gaussian, $+79.3$ for Exponential with diagonal errors; $+101.5$ and $+117.1$ over the valid $z \geq 0.05$ domain with the unbinned native $\mu$-space covariance; $+194.3$ and $+328.7$ over the full sample. The calibration-independent relative evolution shows no decline.

The indicator-specific distance divergence (Section 5) is physically suggestive ($3.30\sigma$ in the full CF4 sample) but is dataset- and reduction-dependent ($0.20\sigma$ in the R22-matched subset — a sample-size constraint, not a vanishing effect, as the central values match the TEP-predicted $\sim 0.02$–$0.05$ mag with stable sign). The two-channel structure (Table 7) shows the Cepheid channel (measured) and the SN stretch channel (remaining a falsifiable host-potential prediction awaiting a decisive measured-$V_{\rm rot}$ sample test), each bounded by an independent observational constraint. The standardized Hubble-residual channel is the subject of Section 10.

### 9.8 Standardization Suppression of the Temporal-Gradient Observable

An audit of the standard SN Ia data reduction pipeline reveals a critical mechanism that suppresses the macroscopic temporal signal: the SALT standardization process itself attenuates the pre-standardization directional signal.

Because the standard rest-frame time mapping used by SALT3 implicitly assumes that the spectroscopic redshift fully accounts for the transformation between observed and emitted light-curve timescales, the aggregate SALT3 standardization — combining the stretch correction $\alpha x_1$, the color correction $\beta c$, and the host-mass step — attenuates the pre-standardization directional signal, consistent with partial absorption of a temporal contribution. This constitutes a falsifiable prediction: the temporal signal should appear in pre-standardization SALT magnitude residuals at a specific amplitude and be attenuated in standardized ones. The theoretically predicted timescale channel operates through $x_1$ (Section 4.9), but a direct audit shows that the raw stretch coefficient itself is not significantly directional ($D_{x_1} = +0.061 \pm 0.061$, $p = 0.32$). This directional $x_1$ null is distinct from the uncalibrated host-potential $x_1(X_i)$ prediction of Section 10.4; the two tests probe different spatial structures. The suppression is instead observed in the aggregate correction, where the pre-standardization magnitude dipole ($D = -0.070 \pm 0.019$, $p_{\rm perm} < 10^{-3}$) is reduced to $D = -0.021 \pm 0.010$ ($p_{\rm perm} = 0.014$) after the full SALT3 correction is applied. The standardization therefore suppresses approximately 70% of the pre-standardization directional signal, with the residual remaining significant in the standardized residuals. Complete calibration of the $x_1$ channel requires the disformal coupling $\gamma_x$ to be constrained independently (Section 4.9).

## 10. Falsification Pathways and Future Observational Tests

The value of a physical theory lies not only in what it explains but in what it forbids. The TEP framework makes specific, quantitative predictions that can be tested with current and near-future observational facilities. This section outlines seven falsification pathways (Pathways I–VII) and auxiliary tests, each designed to either confirm or refute the TEP acoustic clock bias hypothesis against the kinematic void alternative.

### 10.1 Pathway I: Expanding the Matched Cepheid/TRGB Sample

The most decisive near-term test is expanding the matched Cepheid/TRGB galaxy sample. The current 22-galaxy CF4 sample yields $3.30\sigma$, but a four-variant audit reveals that the offset is dataset/reduction dependent: it is driven by 16 galaxies with Cepheid distances from non-SH0ES sources (not in the R22 sample). When restricted to the R22-matched subset ($N=6$, selected by position), the offset is $-0.009 \pm 0.044$ mag ($0.20\sigma$), consistent with Tully et al.'s published $-0.023 \pm 0.022$. When restricted to R22-matched galaxies with external TRGB, the offset is $-0.030 \pm 0.049$ ($0.62\sigma$). The indicator divergence is therefore physically suggestive but statistically constrained by the small sample size.

A JWST-era matched sample is constructed from 18 galaxies with both JWST NIRCam TRGB distances (CCHP F115W from Freedman et al. 2024, GO-1995, and Anand et al. 2024 F090W, GO-1685/GO-2875) and R22 Cepheid distances on the same NGC 4258 maser zero-point. Because JWST NIRCam observes both Cepheid and TRGB populations through identical optics, the $\Delta\mu = \mu_{\rm Cep} - \mu_{\rm TRGB}$ diagnostic is stripped of all telescope zero-point drift. The full-sample regression ($N=17$) yields a slope of $+2.6 \times 10^5 \pm 2.2 \times 10^5$ ($1.20\sigma$, positive — wrong sign for TEP), but the weighted mean $\Delta\mu = -0.023 \pm 0.022$ mag ($1.02\sigma$, negative — correct direction) and the reduced $\chi^2/{\rm dof} = 0.77$ indicate a well-behaved fit with no excess scatter, unlike the CF4 sample ($\chi^2/{\rm dof} = 1.71$). A differential filter offset of $+0.054$ mag between the F090W (Anand) and F115W (CCHP) TRGB calibrations is detected; correcting this offset raises the weighted mean to $-0.042 \pm 0.024$ mag ($1.77\sigma$). M101 is the highest-leverage galaxy (highest $X_i$, positive $\Delta\mu$); excluding it yields an unscreened slope of $-2.4 \times 10^5 \pm 3.5 \times 10^5$ ($0.69\sigma$, correct negative sign, consistent with TEP at $0.35\sigma$). The filter-corrected, M101-excluded weighted mean reaches $-0.060 \pm 0.026$ mag ($2.29\sigma$).

The Anand F090W subset ($N=7$) shows a negative slope ($-3.5 \times 10^5 \pm 7.4 \times 10^5$, $0.48\sigma$) with the correct TEP sign, consistent with the predicted $\kappa_{\rm Cep}$ at $0.01\sigma$. The JWST slope is reduced in both magnitude and significance compared to the CF4 compilation ($+5.4 \times 10^5$, $2.11\sigma$), suggesting the CF4 positive slope was partly driven by registration artifacts. A direct comparison confirms this diagnosis: the $X_i$ regression on the TEP-H0 raw SH0ES Cepheid + EDD/CCHP TRGB data ($N=18$, not CF4 registered) yields a slope of $-1.0 \times 10^5 \pm 3.8 \times 10^5$ ($0.27\sigma$) — the TEP-predicted negative sign — whereas the CF4 registered sample ($N=22$) yields $+5.4 \times 10^5 \pm 2.5 \times 10^5$ ($2.11\sigma$) — the wrong sign. The sign flip is concentrated in the R22-matched subsample, where CF4 zero-point corrections are largest; the non-R22 CF4 subsample retains a negative slope ($-5.5 \times 10^5$, $0.98\sigma$). CF4 registration applies host-property-dependent zero-point corrections that introduce a spurious positive correlation between $\Delta\mu$ and $X_i$, inverting the TEP signal. The JWST sample is currently too small for a decisive test, but the pristine data quality (reduced $\chi^2 < 1$) and the correct-sign Anand subset are both consistent with the TEP prediction. Expanding the JWST overlap sample to $\sim 30$ galaxies would provide a decisive test.

A same-team Cepheid comparison resolves the residual sign discrepancy. The R22 (SH0ES) Cepheid distances used above employ a maser-anchored zero-point and a multi-band P-L fitting procedure that differs from the Madore & Freedman (2023, MF2023) reduction. The JWST TRGB distances (Freedman et al. 2024) are from the same team as MF2023, so the MF2023 Cepheid + JWST TRGB combination eliminates inter-team zero-point systematics. On the $N = 13$ overlap sample, the MF2023 optical ($VI$) Cepheid distances yield an $X_i$ regression slope of $-3.42 \times 10^5 \pm 1.72 \times 10^5$ mag ($-1.98\sigma$) — the TEP-predicted negative sign — consistent with the predicted $\kappa_{\rm Cep} = 0.365 \times 10^6$ mag at $0.13\sigma$. The MF2023 NIR ($VIH$) Cepheid distances yield a weighted mean $\Delta\mu = -0.196 \pm 0.016$ mag with all 13 of 13 galaxies showing the TEP-predicted negative sign ($p = 0.00012$, $3.67\sigma$ one-sided binomial, providing independent confirmation distinct from the $3.65\sigma$ M31 internal gradient result). By contrast, the R22 Cepheid distances on the same 13 galaxies give a positive slope ($+2.60 \times 10^5$, wrong sign) and only 9 of 13 negative. The R22$-$MF2023 offset correlates with $X_i$ ($r = +0.28$ for $VIH$), indicating that the R22 P-L fitting absorbs part of the potential-dependent clock bias. This is itself a TEP prediction: different Cepheid reductions absorb the TEP signal to different degrees, depending on how the P-L relation handles the potential-dependent shift. The same-team MF2023 + JWST TRGB combination, free from inter-team zero-point systematics, recovers the correct TEP negative slope and the strongest sign-test evidence to date.

The per-host Cepheid recalibration of the Pantheon+ sample (TEP-H0, Paper 11) is the complementary test: it would show the $(1+z)^{-0.3}$ decay and the host-mass dependence directly, both of which are invisible in the global $M_B$ regime. Intra-host differential tests — comparing Cepheid and TRGB distances within the same galaxy using JWST — would test the radial gradient prediction at the individual galaxy level.

Two upcoming facilities will substantially expand the statistical reach of the redshift-profile test. The Nancy Grace Roman Space Telescope's High Latitude Time Domain Survey (HLTDS) will discover thousands of SNe Ia up to $z \sim 2$, providing high-precision light curves that can test the redshift-profile structure against the published KBC gradual decay curves. The Vera C. Rubin Observatory's Legacy Survey of Space and Time (LSST) will deliver deep host-galaxy photometry and mass profiling, enabling high-mass host stratification at $z > 0.3$ with statistical samples exceeding $10^4$ supernovae. Both surveys can test whether the $H_0(z)$ profile remains flat or shows the gradual decline predicted by the KBC/MOND model. However, the Cepheid-channel host dependence requires nearby/mid-distance Cepheid hosts with TRGB cross-checks, not high-$z$ SN surveys alone.

### 10.2 Pathway II: Peculiar Velocity Recalibration and Directional Δμ

The second falsification pathway directly tests the TEP interpretation of the CosmicFlows-4 bulk-flow anomaly as a calibration-sensitive quantity. The indicator-specific distance divergence (Section 5) shows $3.30\sigma$ in the full CF4 catalog but only $0.20\sigma$ in the R22-matched subset — the result is dataset/reduction dependent and physically suggestive but statistically constrained by the small sample size. The calibration sensitivity analysis (Section 6) shows that this compression introduces a distance-dependent shift of $-3.2 \times d$ km/s into the peculiar velocity field. The velocity catalog is calibration-sensitive, while the measured bulk-flow amplitude changes by a bounded amount when the distance indicator is switched from Cepheids to TRGB. The void model predicts the $4.6\sigma$ bulk-flow anomaly persists, because the physical motion of the galaxies is independent of the distance indicator used; the TEP framework predicts the velocity catalog is calibration-sensitive, with the bulk-flow amplitude changing by a bounded amount under recalibration.

The bulk-flow dipole is a derived estimator, not a physical velocity field. The conventional estimator $v_{\rm pec} = cz - H_0 d$ absorbs a change of distance calibration into a distance-dependent, apparently dipolar residual. A dual-calibration experiment re-calibrates the full CosmicFlows-4 Tully-Fisher catalog with both Cepheid and TRGB zero-points. When the standard $v_{\rm pec}$ estimator is used, the two calibrations give bulk flows that differ by $|{\bf \Delta B}| = 50.4$ km/s at an angle of $74^\circ$ to the CMB dipole; only $\Delta B_\parallel = +13.9$ km/s is aligned with the CMB. When an $H_0$-invariant log-distance estimator $y = 5\log_{10}(V) - \mu$ is used, the inferred bulk flow is identical for the two calibrations ($B = 290.0$ km/s), so the differential bulk flow is $\Delta B = 0.0$ km/s. The $155\ {\rm km\,s^{-1}}$ Cepheid excess is therefore an estimator artifact of the conventional $v_{\rm pec}$ estimator, not a physical kinematic flow. The candidate macroscopic temporal component is the finite-coherence feature with best-fit $L_T = 55.6$ Mpc, not a rigid dipolar gradient.

The directional $\Delta\mu$ signal in the Cepheid–TRGB offset is likewise not a robust discriminator. A compiled sample of 33 galaxies with both Cepheid and TRGB distances gives $r(\Delta\mu, \cos\theta_{\rm CMB}) = +0.329$ ($p = 0.062$), with a 3-D dipole-fit permutation $p = 0.537$. After conditioning on the screened host potential $X_i$ and R22 membership, the partial correlation of the CMB direction with $\Delta\mu$ is $r = +0.20$ ($p = 0.27$), while the $X_i$ scaling survives with $r(\Delta\mu, X_i \mid \cos\theta) = +0.225$ ($p = 0.208$). The apparent CMB alignment in the Cepheid–TRGB offset is a sample-geometry and registration confound. The calibration-sensitivity of the conventional bulk-flow estimator is a diagnostic of the indicator divergence, not evidence for a Cepheid-specific large-scale temporal dipole. The macroscopic temporal signal that does survive is the candidate finite-coherence component in the pre-standardization Pantheon+ residuals ($L_T = 55.6$ Mpc, Section 6.4), not the Cepheid–TRGB directional split.

### 10.3 Pathway III: Spatially Resolved Host Kinematics

The third falsification pathway exploits the TEP prediction that the acoustic clock bias depends on the observing geometry within each host galaxy. JWST and ground-based IFU spectroscopy can map the differential tracer ratios $q_i^{\rm clock} = r_{\rm spec} / r_{\rm Cep}$ between galactic nuclear cores and outer disk Cepheid fields. The TEP framework predicts that the observed period contraction scales with this ratio: hosts where spectroscopic calibrations are weighted toward the dense, deeply slowed core ($q_i^{\rm clock} < 1$) should exhibit larger apparent period contraction than hosts where the spectroscopic and Cepheid fields are at similar radii ($q_i^{\rm clock} \approx 1$).

This test requires: (a) spatially resolved spectroscopy of SN Ia host galaxies to measure the radial profile of the stellar velocity dispersion; (b) matching Cepheid positions to the kinematic map to compute $q_i$ for each host; and (c) testing whether the residual Cepheid distance offset correlates with $q_i$ as predicted by TEP. The void model predicts no correlation with $q_i$ (the bulk flow is a rigid-body translation that does not vary within the galaxy), while TEP predicts a positive correlation.

### 10.4 Pathway IV: The $X_i$-Step in Pantheon+ Hubble Residuals

The SN light-curve stretch channel (Section 9.6) predicts that Hubble residuals after SALT3 standardization should correlate with the potential coordinate $X_i$ of the SN host, beyond the standard host-mass correction. This is directly testable with Pantheon+ data. A preliminary test used the 1,353 Pantheon+ Hubble-flow SNe ($z > 0.01$, $\log M > 7$) with host stellar mass measurements. The host potential was estimated from measured $V_{\rm rot}$ where available (107 SNe from the HyperLEDA Vizier catalog) and from the baryonic Tully-Fisher relation ($V_{\rm rot} \approx 200\,(M_*/10^{10.5}\,M_\odot)^{1/4}\ {\rm km\,s^{-1}}$) for the remainder. The Hubble residual is computed as ${\rm HR} = \mu_{\rm SH0ES} - \mu_{\rm ref}(z_{\rm HD})$ using the flat-$\Lambda$CDM reference at $H_0 = 73.04$, $\Omega_m = 0.334$. The results are:

The standard mass step (at $\log_{10}(M_*/M_\odot) = 10.5$) is $+1.8 \pm 8.7$ mmag ($0.21\sigma$) in this sample — consistent with zero because $\mu_{\rm SH0ES}$ already incorporates a mass-step correction in the SALT3 calibration. The $X_i$ step (high-$X$ minus low-$X$) is $+7.5 \pm 50.2$ mmag ($0.15\sigma$) — in the TEP-predicted direction but not statistically significant, because screening compresses most hosts into the high-$X_i$ bin ($N_{\rm high} = 1335$, $N_{\rm low} = 18$), leaving too few low-$X_i$ hosts for a powerful step test. After removing the mass-step component, the residual $X_i$ step is $+0.8 \pm 50.5$ mmag ($0.02\sigma$) — still in the predicted direction but not statistically significant.

An improved analysis uses measured $V_{\rm rot}$ from the HyperLEDA catalog (VII/237, VII/238) queried via the Vizier HTTP API for all 1,543 Pantheon+ hosts. Measured rotation velocities (with inclination corrections from axis-ratio data) are obtained for 173 SNe: 33 calibrators and 140 Hubble-flow hosts. The remaining 1,330 Hubble-flow hosts retain the Tully-Fisher proxy. The Hubble residual is computed as ${\rm HR} = \mu_{\rm SH0ES} - \mu_{\rm ref}(z_{\rm HD})$, where $\mu_{\rm ref}$ is the flat-$\Lambda$CDM distance modulus at $H_0 = 73.04$, $\Omega_m = 0.334$, evaluated at the peculiar-velocity corrected redshift $z_{\rm HD}$. The full sample ($N = 1,470$ Hubble-flow) shows a step of $+22.3 \pm 15.1$ mmag ($+1.47\sigma$) — the TEP-predicted direction (high-$X_i$ hosts have more positive Hubble residuals, as expected when Cepheid distances are compressed in deeper potentials). Despite aggressively expanding the measured-$V_{\rm rot}$ kinematic sample with deep 21-cm blind surveys (ALFALFA, 2MTF, WALLABY), the subsample ($N = 128$ Hubble-flow) remains too structurally unbalanced ($N_{\rm high} = 121$, $N_{\rm low} = 7$) for a standalone detection ($1.06\sigma$–$2.11\sigma$, correct sign); the mass-residualized step for this subsample is $+131.1 \pm 123.6$ mmag ($+1.06\sigma$) — also in the TEP-predicted direction, with a larger amplitude consistent with the deeper potential leverage of the measured-$V_{\rm rot}$ sample.

Mass residualization is performed by sequentially fitting ${\rm HR} = a + b \cdot \log M_*$ and taking the $X_i$-step on the mass-residualized Hubble residuals. A joint OLS fit of ${\rm HR} = a + c_X \cdot X_i + c_M \cdot \log M_*$ on the full sample ($N = 1{,}470$) yields $c_X = +7.92 \times 10^4 \pm 3.75 \times 10^4$ ($+2.11\sigma$) and $c_M = -0.021 \pm 0.014$ ($1.47\sigma$), in the TEP-predicted direction after simultaneous mass correction. However, the design-matrix condition number is $\sim 10^7$, reflecting strong multicollinearity between $X_i$ and $\log M_*$ (for the $\sim 88\%$ of hosts without measured $V_{\rm rot}$, $X_i$ is generated from $\log M_*$ via the Tully-Fisher proxy). Because stellar mass physically correlates with the host potential well depth, mass-correction inevitably absorbs a significant portion of any true $X_i$ signal. The uncorrected step ($+1.47\sigma$) therefore remains the primary observable, while the sequentially residualized step ($+1.00\sigma$) provides a highly conservative lower bound. The aggressively expanded, purely measured-$V_{\rm rot}$ subsample ($N = 128$) gives consistent-sign trends ($1.06\sigma$–$2.22\sigma$) but remains completely underpowered due to the fundamental selection bias in the Pantheon+ dataset ($N_{\rm high} = 121$, $N_{\rm low} = 7$). If TEP is incorrect, the TF-proxy $X_i$-step detection must be an astrophysical confound. If TEP generates both the mass step and the $X_i$-step (as predicted by the framework), mass residualization provides a conservative lower bound; the uncorrected step is the primary TEP estimate.

The purely measured-$V_{\rm rot}$ sample is structurally unbalanced ($N_{\rm high} = 121$, $N_{\rm low} = 7$) since blind HI surveys do not intersect with the distant, low-mass hosts selected by Pantheon+. The low-$X_i$ signal thus inherently relies on the TF-proxy for $V_{\rm rot}$. Furthermore, the measured-$V_{\rm rot}$ subsample is concentrated at very low redshift (median $z = 0.020$, maximum $z = 0.064$) where peculiar velocity contamination ($\sim$100–200 mmag) is largest. HyperLEDA preferentially samples nearby massive spirals, introducing a selection bias that correlates with $X_i$. The Hubble-flow $X_i$-step with measured $V_{\rm rot}$ is therefore consistent with TEP but inconclusive because the small, nearby, unbalanced subsample does not provide a clean test. A definitive test requires a deeper $V_{\rm rot}$ catalog (e.g., SPARC, ALFALFA $\alpha$.40, or broader HyperLEDA coverage), populating the low-$X_i$ bin with Hubble-flow SNe at $z > 0.03$ where peculiar velocities are subdominant. The DHOST derivation (Section 4.6) additionally predicts that $\bar\epsilon_0$ should scale as $V_{\rm rot}^2/r^2$ rather than $V_{\rm rot}^2$ alone — a testable distinction that requires Cepheid galactocentric radii from JWST imaging. The void model predicts no $X_i$-step (the bulk flow is independent of host potential).

### 10.5 Additional Tests and Cross-Checks

Beyond the seven falsification pathways, several additional tests provide further discrimination:

Mira variable distances: Mira stars are long-period variables whose pulsation mechanism is similar to Cepheids (acoustic oscillation driven by the $\kappa$-mechanism). The TEP framework predicts that Mira distances should exhibit the same acoustic clock bias as Cepheids, while TRGB and JAGB distances should not. JWST observations of Miras in SN Ia hosts (already underway in some programs) provide an additional acoustic clock test.

Surface Brightness Fluctuations (SBF): SBF distances in the near-infrared are derived from the statistical properties of the unresolved stellar population in early-type galaxies. Because SBF is a statistical luminosity measure (not an acoustic clock), the TEP framework predicts it should behave like TRGB — without the acoustic clock's period-transport bias. The observed $H_0^{\rm SBF} = 74.6 \pm 0.9\ {\rm km\,s^{-1}\,Mpc^{-1}}$ (Garnavich et al. 2023) is consistent with this prediction when the SBF calibration lineage is traced. The SBF-Cepheid zero-point was first established by Tonry et al. (2000), who tied the SBF absolute scale to Cepheid distances in six spiral galaxies with both SBF and Cepheid measurements. Blakeslee et al. (2002) revised this calibration by $+0.06$ mag using the final HST Key Project Cepheid distances. Jensen et al. (2015) calibrated the near-infrared SBF method for WFC3/IR using 16 early-type galaxies in the Virgo and Fornax clusters, with zero-points anchored to the Cepheid distance scale. Garnavich et al. (2023) used these Jensen et al. SBF distances — explicitly calibrated to the Cepheid zero-point — to calibrate SNe Ia in 25 host galaxies and derive $H_0$. The high SBF $H_0$ inherits the Cepheid channel bias through the calibration chain: Cepheid distances $\to$ SBF zero-point $\to$ SN Ia $M_B$ $\to$ $H_0$.

A Cepheid-independent SBF calibration has recently been developed by the TRGB-SBF Project (Jensen et al. 2025), which uses JWST TRGB distances anchored to the NGC 4258 maser to set the SBF zero-point without any Cepheid input. This Cepheid-free calibration yields $H_0 = 73.8 \pm 0.7\ ({\rm stat}) \pm 2.3\ ({\rm sys})\ {\rm km\,s^{-1}\,Mpc^{-1}}$ — still elevated, and virtually identical to the Cepheid-anchored SBF result. Under the two-channel TEP model (Section 9), this is not a contradiction but a consistency check. The SBF anchor is clean (TRGB, a non-timescale indicator with no clock bias), but the Hubble-flow SNe are still standardized using SALT2/SALT3, which involves the light-curve stretch $x_1$ — a timescale. The SN stretch channel (Section 9.6) operates on the last rung of the ladder, independent of the anchor. SBF ladders calibrate SNe in the most massive (early-type) hosts, i.e., the hosts with the largest SN-channel bias. A high $H_0$ with a clean anchor is exactly what the two-channel model predicts: the TRGB anchor removes the Cepheid channel, but the SN stretch channel remains. The Jensen et al. (2025) result thus is compatible with and motivates the SN stretch-channel interpretation.

Combined Cepheid+TRGB calibration (Riess et al. 2025): the SH0ES team has combined Cepheid and TRGB calibrations in the same SN Ia host sample (55 SNe), yielding $H_0 = 73.18 \pm 0.88\ {\rm km\,s^{-1}\,Mpc^{-1}}$. A TRGB-inclusive calibration returning $\sim 73$ rather than $\sim 68$ appears, at first sight, to contradict the Cepheid-only TEP prediction. Under the two-channel model, however, this result is expected: when Cepheid and TRGB calibrations are combined on a common SN host sample, the SN stretch channel is shared by both calibrations (all SNe are standardized the same way regardless of anchor), so both converge to the same high $H_0$. The Cepheid channel adds an additional offset on top of the shared SN channel, but the SN channel alone is sufficient to keep the combined result above $\sim 73$. The two-channel model predicts that the Cepheid-minus-TRGB difference within this combined sample should be $\sim 0.02$–$0.05$ mag (the Cepheid channel only), consistent with the Riess et al. (2025) finding that the two calibrations agree at the $\sim 1\%$ level. The combined result does not falsify TEP; it is consistent with the two-channel structure, and is compatible with and motivates the SN stretch-channel interpretation.

Strong lensing time delays: Time delays in strongly lensed systems (e.g., from the TDCOSMO program) provide a geometric $H_0$ measurement that is independent of the distance ladder. The TEP framework predicts that time-delay $H_0$ should agree with the CMB value (since time delays measure the global temporal shear / apparent expansion rate, not the local distance ladder), while the void model predicts that time-delay $H_0$ should be inflated within the void. Current time-delay results ($H_0 \approx 67$--$74$ with large uncertainties) are not yet precise enough to discriminate, but future programs may reach the required precision.

Band-dependence of the Cepheid-TRGB offset (Pathway V): The disformal mechanism (Section 4.7) predicts that the TEP correction scales with the Leavitt law slope $|b|$, which differs between optical ($b_V \approx -2.76$) and near-infrared ($b_H \approx -3.26$) bands. The inter-band differential $\Delta\mu_{H-V} = -(b_H - b_V)\,\kappa_P\,X_i \approx -0.5\,\kappa_P\,X_i$ should anti-correlate with $X_i$: NIR distances should be more heavily compressed at deeper potentials, giving a negative regression slope. This prediction is specific to the disformal channel; conventional systematics (extinction, metallicity, crowding) do not naturally produce this band-dependent spatial signature.

A matched-host test is conducted using two independent samples. The primary sample uses the Madore & Freedman (2023, arXiv:2309.10859) compilation, which provides both $W(H,VI)$ NIR and $W(V,VI)$ optical Cepheid true distance moduli for 20 galaxies analysed with identical methodology, photometry, and Cepheid samples by the same team. The regression of $\Delta\mu_{\rm band} = \mu_{\rm NIR} - \mu_{\rm optical}$ on $X_i$ yields a slope of $+2.27 \times 10^5 \pm 8.6 \times 10^4$ ($2.62\sigma$, positive) — the wrong sign for TEP, which predicts a negative slope. The high $\chi^2/{\rm dof} = 6.40$ and weak Pearson correlation ($r = -0.20$, $p = 0.41$) indicate that the regression is driven by leverage points rather than a tight global trend; the single galaxy M~101 contributes 26\% of the total WLS weight and drives the positive slope. A formal M101-exclusion sensitivity run (saved in the band-dependence archive) confirms the leverage diagnosis: removing M~101 alone flips the slope to $-1.20 \times 10^6 \pm 2.47 \times 10^5$ ($-4.87\sigma$), the TEP-predicted negative sign, with the remaining 19 galaxies. The same-team comparison is susceptible to correlated systematics (shared photometry, shared metallicity corrections, shared Cepheid selection) that can mask the TEP band-dependent signal; the M101 leverage analysis isolates the effect to a single high-$X_i$ outlier whose NIR/optical differential is positive (NIR fainter), opposite the TEP prediction.

The secondary sample (Key Project optical versus R22 NIR, $N=9$, cross-team) provides a more diagnostic test because the optical and NIR distances are measured by independent teams using independent methodology, photometry, and calibrations. The cross-team regression yields a slope of $-6.2 \times 10^4 \pm 3.8 \times 10^5$ ($0.16\sigma$) — the TEP-predicted negative sign, with $\chi^2/{\rm dof} = 0.90$ indicating a good fit and Pearson $r = -0.21$. The point estimate is consistent with the TEP prediction ($-5.6 \times 10^4$ using the equivalent $\kappa_P$) at $0.02\sigma$. The large uncertainty reflects the small sample size and the cross-team zero-point offset (intercept $= +0.067$ mag), but the sign and goodness-of-fit are both consistent with the TEP prediction. The same-team positive slope is interpreted as a residual systematic in the MF2023 band differential that correlates with potential depth through galaxy properties (metallicity, extinction, crowding), masking the TEP signal in the same-team comparison.

Tracer-type dependence (Pathway VI): The $q_i$ mechanism (Section 4.4) predicts that the Cepheid period bias depends on the tracer used to measure the host systemic redshift. Hosts with H I 21cm redshifts (disk-weighted, extended) should show $q_i^{\rm clock} \approx 1$ and therefore $\Delta\mu \approx 0$, while hosts with nuclear optical redshifts (bulge-weighted, compact) should show $q_i^{\rm clock} < 1$ and the full $\Delta\mu < 0$ signal. A preliminary classification of the 22-galaxy matched sample finds $N_{\rm HI} = 14$ and $N_{\rm nuclear} = 8$. The H I subsample shows $\Delta\mu = -0.092 \pm 0.031$ mag (11/14 shorter), while the nuclear subsample shows $\Delta\mu = -0.059 \pm 0.039$ mag (6/8 shorter). The difference $\Delta\mu_{\rm nuclear} - \Delta\mu_{\rm HI} = +0.032 \pm 0.050$ ($0.64\sigma$) is opposite to the $q_i$ prediction (nuclear should be more negative) but not significant. This null result bounds the conformal $q_i$ channel to zero at the $\sim 0.05$ mag level. This null constrains the explicitly tracer-dependent conformal $q_i^{\rm clock}$ contribution. Its implications for the disformal transport term depend on the full non-radial geometry and are not determined by this preliminary test. A definitive tracer-type test requires a larger sample with unambiguous tracer classification from HyperLEDA/NED metadata.

### 10.6 Summary of Falsification Pathways

| Pathway | Observable | Void Prediction | TEP Prediction | Feasibility |
|---|---|---|---|---|
| I | Expanded Cepheid/TRGB matched sample | No indicator offset | Cepheid distances shorter; JWST sample ($N=17$): mean $\Delta\mu = -0.023 \pm 0.022$ ($1.02\sigma$), $\chi^2/{\rm dof} = 0.77$; filter-corrected weighted mean $-0.042 \pm 0.024$ ($1.77\sigma$); filter-corrected + M101-excluded weighted mean $-0.060 \pm 0.026$ ($2.29\sigma$); Anand F090W subset ($N=7$): correct-sign slope at $0.01\sigma$ consistency; same-team MF2023 $VI$ Cepheid + JWST TRGB ($N=13$): slope $-3.42 \times 10^5 \pm 1.72 \times 10^5$ ($-1.98\sigma$, correct sign, $0.13\sigma$ consistency with $\kappa_{\rm Cep}$); MF2023 $VIH$: 13/13 sign test ($3.67\sigma$ one-sided), weighted mean $-0.196 \pm 0.016$ mag | JWST TRGB (GO-1995, GO-1685); expand to $\sim 30$ galaxies |
| II | Bulk-flow estimator calibration sensitivity | No calibration dependence; bulk flow is physical | Conventional $v_{\rm pec} = cz - H_0 d$ gives a $155\ {\rm km\,s^{-1}}$ Cepheid excess; the $H_0$-invariant log-distance estimator gives $\Delta B = 0.0$ km/s; Pantheon+ favours a candidate finite-coherence component rather than the previously assumed global linear-gradient form. | Completed for the calibration differential: the indicator-dependent bulk-flow excess is an estimator artifact. The remaining common directional field is tested independently by the finite-coherence analysis; Pantheon+ favours a candidate finite-coherence component rather than the previously assumed global linear-gradient form. |
| III | $q_i$ correlation with Cepheid offset | No correlation | Positive correlation | JWST + IFU spectroscopy |
| IV | $X_i$-step in Pantheon+ Hubble residuals | No $X_i$-step | Preliminary ($N=1353$, TF+measured $V_{\rm rot}$, screened): $X_i$-step $+7.5 \pm 50.2$ mmag ($+0.15\sigma$, TEP-predicted direction; underpowered, $N_{\rm low}=18$); mass-corrected $X_i$ regression $0.71\sigma$; full sample ($N=1470$): $+22.3 \pm 15.1$ mmag ($+1.47\sigma$, TEP-predicted); joint OLS $X_i$ coefficient after mass correction $+7.92 \times 10^4 \pm 3.75 \times 10^4$ ($+2.11\sigma$, TEP-predicted); measured-$V_{\rm rot}$ expanded subsample ($N=128$, mass-residualized): $+131.1 \pm 123.6$ mmag ($+1.06\sigma$, TEP-predicted; unbalanced $N_{\rm high}=121$, $N_{\rm low}=7$) | Inconclusive with current HyperLEDA coverage; needs deeper $V_{\rm rot}$ catalog |
| Additional | Mira distances vs. TRGB | All agree | Miras biased like Cepheids | JWST programs underway |
| Additional | TRGB-calibrated SBF (Jensen et al. 2025) | All agree | High $H_0$ persists (SN stretch channel) | Confirmed: $H_0 = 73.8$ with clean anchor |
| Additional | Strong lensing time delays | Inflated within void | Consistent with CMB | TDCOSMO; precision limited |
| V | Band-dependence: optical versus NIR Cepheid offset | No band dependence | NIR compression $\sim 18\%$ larger than optical ($b_H \approx -3.26$ versus $b_V \approx -2.76$); predicted slope $\approx -5.6 \times 10^4$; cross-team test (KP vs R22, $N=9$): slope $-6.2 \times 10^4 \pm 3.8 \times 10^5$ ($0.16\sigma$, negative — correct sign), $\chi^2/{\rm dof} = 0.90$; same-team test (MF2023, $N=20$): slope $+2.27 \times 10^5$ (positive — wrong sign, driven by M~101 leverage, $\chi^2/{\rm dof} = 6.40$); M101-excluded ($N=19$): slope $-1.20 \times 10^6 \pm 2.47 \times 10^5$ ($-4.87\sigma$, correct sign) | The cross-team point estimate has the predicted negative sign and is consistent with the predicted amplitude, but is statistically uninformative at $0.16\sigma$; same-team positive slope is consistent with a leverage/correlated-systematics explanation (shared photometry, metallicity corrections); Bayesian hierarchical modelling on same-team sample finds $\sigma_{\rm int} = 0.132 \pm 0.028$ mag, confirming large unmodeled scatter in same-team differential |
| VI | Tracer-type dependence: H I versus nuclear $z$ | No tracer dependence | H I-anchored hosts show $\Delta\mu \approx 0$; nuclear-anchored show $\Delta\mu \lt 0$; preliminary test: null ($0.64\sigma$, opposite to prediction) — bounds $q_i$ channel to zero; implications for the disformal term depend on the full non-radial geometry | Needs larger sample with unambiguous tracer classification |
| VII | 2D geometric prediction: $V_{\rm rot}^4/R^2$ vs $V_{\rm rot}^2$ | No correlation with either | DHOST derivation predicts $\epsilon_{\rm env} \propto V_{\rm rot}^4/r^2$; SPARC cross-match ($N=6$): $r(\Delta\mu, V^4/R^2) = +0.615$ vs $r(\Delta\mu, V^2) = +0.162$; partial $r(V^4/R^2 \mid V^2) = +0.778$ ($p = 0.069$); $\Delta{\rm AIC} = -2.69$ (2D preferred) | Preliminary ($N=6$); needs Cepheid galactocentric radii from JWST imaging for rigorous test |

Each of these pathways provides a distinct falsification test of the TEP framework against the kinematic void hypothesis. Several can be tested with existing or near-future data, while others require expanded or deeper samples. Together, they constitute a comprehensive falsification program that can definitively distinguish between the two frameworks within the next several years.

### 10.7 Methods Summary

The analysis pipeline is implemented as a reproducible Python codebase (available at [https://github.com/matthewsmawfield/TEP-VOID](https://github.com/matthewsmawfield/TEP-VOID)). The key methodological choices are:

Data sources: CosmicFlows-4 (Tully et al. 2023) provides 38,053 galaxy group distances and peculiar velocities. Pantheon+ (Scolnic et al. 2022) provides 1,701 light curves of $\sim$1,550 distinct SNe Ia; after deduplication by CID and application of quality cuts, 1,543 unique SNe Ia with distance moduli enter the analysis. The native $1701 \times 1701$ STAT+SYS covariance matrix is used for all unbinned likelihood evaluations; the matched $1053 \times 1053$ submatrix at $z \ge 0.05$ is used for the primary void-falsification test.

$H_0$ inference: For each SN, $H_0$ is inferred by inverting the proper ΛCDM luminosity distance relation $d_L = (1+z) \cdot c/H_0 \cdot \int_0^z dz'/E(z')$, where $E(z) = \sqrt{\Omega_m(1+z)^3 + (1-\Omega_m)}$. This is valid at all redshifts, unlike the linear $cz/d_L$ approximation valid only at $z \ll 0.01$.

Error propagation: Per-SN distance modulus errors ($\sigma_\mu$) from Pantheon+ are propagated to $H_0$ via $\sigma_{H_0} = H_0 \cdot \ln(10)/5 \cdot \sigma_\mu$. The bin error is the standard error of the mean: $\sigma_{\bar{H_0}} = \sqrt{\langle \sigma_{H_0,i}^2 \rangle / N}$.

Primary model comparison: The published KBC Method-3 curves are treated as fixed predictions; both the Gaussian and Exponential void models are compared to the flat TEP/constant model with only a common zero-point nuisance, so both have $k = 1$ and the $\Delta$AIC is simply $\Delta\chi^2$. This is the headline native $\mu$-space likelihood. Secondary free-shape fits (void-Gaussian and void-Exponential with free $\sigma_z$/$z_0$ and $\Delta H_0$, and a TEP $(1+z)^{-n}$ decay with free $n$) are reported as robustness checks but are not the primary statistic. The void curves are the *published Method-3 predictions* digitized from Mazurenko, Banik & Kroupa (2025, MNRAS 536, 3232–3241, Figure 3). Analytical surrogates ($\sigma_z \approx 0.82$, $z_0 \approx 0.74$) are used only as fallback. The $\Delta$AIC is computed both with diagonal errors and with the full Pantheon+ STAT+SYS covariance matrix ($1701 \times 1701$).

Host-mass split: The host-mass split at $\log_{10}(M_*/M_\odot) = 10.0$ is not used in Section 8's boundary test because Pantheon+ uses a global $M_B$ calibration — all SNe share the same absolute magnitude regardless of host mass, so the split cannot test the TEP host-mass dependence. Section 8 tests the spatial persistence of the tension at $z > 0.25$ using the full Pantheon+ sample. The host-mass dependence of the TEP effect requires per-host Cepheid calibrations (TEP-H0, Paper 11).

$\kappa_{\rm Cep}^{\rm equiv}$: The TEP distance-modulus channel coefficient $\kappa_{\rm Cep}^{\rm equiv} = (0.365 \pm 0.304) \times 10^6\ {\rm mag}$ is imported from the companion paper TEP-H0 (Paper 11), where it is determined from the endpoint slope conversion ($\beta_X = 0$) in the host-level generative distance ladder. It is not derived within the TEP-VOID pipeline. The TEP correction in Section 9 uses this fixed value with no free parameters, applying the formula $\Delta\mu = \kappa_{\rm Cep}^{\rm equiv} \cdot X_i$ where $X_i = (U_i - U_{\rm ref})/c^2$ is the dimensionless screened potential coordinate. The period-response coefficient is $\kappa_P = -\kappa_{\rm Cep} / b$ where $b \approx -3.26$ is the near-infrared Leavitt law slope. The correction is applied through the Cepheid calibrator $\to$ $\Delta M_B$ $\to$ Pantheon+ chain: the mean correction over the calibrator hosts determines a single $\Delta M_B$, which propagates uniformly to all SNe. Because Pantheon+ uses a global $M_B$ calibration, the correction acts as a constant zero-point offset; the host-mass dependence is untestable with Pantheon+ and requires per-host Cepheid calibrations (TEP-H0, Paper 11).

### 10.8 Methodological Scope

The results of this paper divide into two epistemic categories that should be clearly distinguished. The primary contribution — the falsification of the published KBC/MOND predictions against the underlying Pantheon+ data and native covariance — is an objective statistical fact: $\Delta\chi^2 > 100$ in native $\mu$-space with the full Pantheon+ STAT+SYS covariance, $R_H$ excluded at $8.4\sigma$/$9.7\sigma$, and the void family collapsing to its flat limit when amplitude and scale are free. This result does not depend on any TEP parameter and stands independently of the auxiliary program. The secondary contribution — the auxiliary TEP supporting tests (indicator divergence, $\kappa_{\rm Cep}$, $X_i$-step, band-dependence, tracer-type) — is provisional. The auxiliary evidence is heterogeneous: the cross-team band-dependence test has the predicted negative sign but is statistically uninformative at $0.16\sigma$, while other nominal statistics exceed $3\sigma$ but provenance controls, selection effects and intrinsic-scatter modelling substantially reduce their inferential weight.

- Monopole-only scope: The $H_0(z)$ test compares the monopole (angle-averaged) distance modulus against the monopole KBC prediction. An off-center supervoid predicts anisotropic (dipolar) signals: the $H_0$ inferred from SNe in the direction of the void center should differ from that in the opposite hemisphere. The monopole test can partially evade an anisotropic void signal if the void axis is misaligned with the Pantheon+ sky coverage. A hemispheric asymmetry test (Section 6) directly evaluates this by splitting Pantheon+ by CMB dipole and bulk-flow alignment; the null dipolar residual ($\Delta H_0 = 0.00 \pm 0.45$ km/s/Mpc) confirms the monopole rejection. The published KBC predictions tested here are monopole curves; the test is therefore commensurate with the predictions being tested.

- Covariance model: The likelihood is conditional on the published Pantheon+ STAT+SYS covariance model. The zero-point-independent matched-GLS $R_H$ test provides a complementary check that is insensitive to monopole shape systematics.

- Global $M_B$ calibration: Pantheon+ uses a single global $M_B$ calibration for all SNe, meaning the Cepheid calibration bias is imprinted uniformly on all SNe regardless of host mass or redshift. This means: (a) host dependence cannot be tested through the globally calibrated Pantheon+ distance moduli or $H_0(z)$ profile; it can, however, be tested in pre-standardization/light-curve observables such as $x_1$ (Section 8 tests spatial persistence only), and (b) the $H_0(z)$ profile is expected to be flat (the bias is in the zero-point, not distance-dependent). The specific $(1+z)^{-0.3}$ TEP decay prediction cannot be tested with Pantheon+ data — it requires per-host Cepheid calibrations (TEP-H0, Paper 11).

- $\kappa_{\rm Cep}^{\rm equiv}$ is imported from TEP-H0 (Paper 11): The TEP distance-modulus channel coefficient $\kappa_{\rm Cep}^{\rm equiv} = (0.365 \pm 0.304) \times 10^6\ {\rm mag}$ is determined from the endpoint slope conversion in the companion paper's host-level generative distance ladder and applied here as a fixed parameter. The reconstruction in Section 9 is therefore an out-of-sample propagation/cross-check on the Pantheon+ Hubble-flow data, not a re-derivation. The large fractional uncertainty ($\sim 83\%$) propagates into the Section 9 zero-point shift: $\sigma_{\Delta M_B} \approx \kappa_{\rm Cep}^{\rm equiv} \langle X_i \rangle \times (0.304/0.365) \approx 0.030$ mag. The disformal transport analysis (Section 4.6) identifies the structural mechanism — the disformal term provides non-exact transport structure that allows the core-disk clock differential to produce a residual bias without generating the large conformal spectroscopic signature excluded by the core–disk line-shift bound — but does not yet predict the absolute value of $\bar\epsilon_0$ from first principles. A full derivation from the scalar-tensor action, including the $B(\mathcal{X})$ coupling function and the scalar field profile, remains a goal of the ongoing TEP programme.

- Host potential proxy: The full gravitational potential depth analysis requires rotation velocities and velocity dispersions from HyperLEDA. In this pipeline, host stellar mass is used as a proxy for potential depth. The full potential-depth analysis is in TEP-H0 (Paper 11).

- Bulk-flow calibration sensitivity is deterministic: The peculiar velocity calibration sensitivity (Observable II) is not a statistical test — the shift $\Delta v = -\Delta H_0 \cdot d$ is deterministic by construction. It quantifies how the indicator divergence propagates, but does not provide independent statistical evidence.

- $H_0(z)$ is flat, not gradually declining: The data show $H_0(z) \approx 73$ km/s/Mpc at all redshifts. This rejects the published KBC/MOND gradual decay curves (digitized from Mazurenko et al. 2025, Figure 3) by $\Delta$AIC $= +20.2$ Gaussian, $+79.3$ Exponential (diagonal errors) and $\Delta$AIC $= +101.5$ Gaussian, $+117.1$ Exponential over the valid $z \ge 0.05$ domain (unbinned native $\mu$-space, marginalized zero-point; extending to the full sample gives $+194.3$ and $+328.7$, $\chi^2_{\rm flat}=2007.7$). The flat profile is the TEP expectation for global $M_B$ calibration (the bias is in the zero-point, not distance-dependent); the $(1+z)^{-0.3}$ decay applies to the per-host Cepheid calibration regime, which requires per-host Cepheid calibrations (TEP-H0, Paper 11) to test directly and is not probed by the global $M_B$ Pantheon+ data.

- Sample size at high z: The number of SNe at $z > 0.25$ is smaller than at low z, increasing the uncertainty in the high-redshift bins. A dedicated survey (Section 10.1) would tighten these constraints.

- $(1+z)^{-0.3}$ decay index: The decay index $n \approx 0.3$ for the per-host Cepheid calibration regime is a phenomenological estimate reflecting the expected coupling of the scalar field to the matter density. A first-principles derivation from the scalar-tensor action is a goal of the ongoing TEP programme. This does not affect the void falsification results, which depend only on the void model's published gradual decline being absent from the data.

- FLRW distance-redshift relations: The FLRW luminosity-distance mapping is used here strictly as an operational observational coordinate, because both the Pantheon+ products and the published KBC $H_0(z)$ predictions are expressed in that conventional framework. The present comparison tests the KBC prediction on its own observational coordinates and does not require an assumption that FLRW expansion is the fundamental TEP cosmology. A self-consistent TEP cosmological distance-redshift relation is developed in companion papers (TEP-HUB, Paper 30; TEP-BBN, Paper 29).

- Screening mechanism: The screening functions used in the TEP pipeline are parameterized models for the environmental suppression operator $\mathcal{S}_\Sigma(\mathcal{E})$ posited in the foundational paper (Paper 0). A microscopic scalar-tensor completion that reproduces the required continuous environmental suppression operator $\mathcal S_\Sigma(\mathcal E)$ remains a theoretical goal of the TEP programme.

- Scope within the TEP corpus: This paper tests the astrophysical consequences of the TEP scalar-tensor action (the acoustic clock bias in Cepheids) against the void model. The flagship TEP observable — closed-loop residual synchronization holonomy $H_{\rm resid}$ at the $10^{-18}$–$10^{-19}$ fractional level, identified in Paper 0 — is tested in the GNSS papers (Papers 1–3) and is not duplicated here. The astrophysical and clock-network tests are complementary channels within the same framework.

## 11. Discussion: Fundamental Physics versus Kinematic Alternatives

The results of the preceding sections pose a question that extends beyond the Hubble tension itself. Having established that the published KBC/MOND kinematic-void family tested here is ruled out, the surviving anomalies — indicator divergence, potential dependence, calibration sensitivity — demand a physical interpretation. The diversity of proposed solutions reveals a deeper epistemological question: should the tension be resolved by modifying the fundamental laws of physics, or by adjusting empirical parameters within existing frameworks? This section examines the theoretical implications of the TEP framework in the context of this broader question, contrasting the first-principles scalar-tensor approach with the phenomenological nature of the competing models.

### 11.1 The Epistemology of Cosmological Modifications

A high-impact resolution of the Hubble tension cannot rely merely on pointing out localized data anomalies; it must present a unified alternative hypothesis capable of simultaneously explaining multiple, seemingly disparate tensions. A robust cosmological modification must pass stringent consistency checks across multiple probes and scales.

The three representative solution frameworks—Early Dark Energy, the kinematic void model, and the TEP acoustic clock bias—represent three distinct epistemological approaches to this challenge. Early Dark Energy modifies the early universe with a transient scalar field, requiring fine-tuned initial conditions and facing the age-of-the-Universe constraint. The kinematic void model modifies the gravitational force law (MOND) and requires a Gpc-scale local underdensity that introduces an observer-location fine-tuning. The TEP framework modifies the fundamental nature of proper time, deriving the acoustic clock bias from a scalar-tensor action without fine-tuning the observer's location or the initial conditions of the universe. The qualitative prediction (acoustic clocks biased, nuclear candles avoid the period-transport bias) follows from the action; the quantitative coupling $\kappa_{\rm Cep}$ (the distance-modulus channel coefficient defined in Section 9) is empirically determined in the companion paper.

The epistemological divide between the void model and TEP is the nature of time itself. Where standard cosmology requires fine-tuned matter voids or ad hoc force laws to preserve static metric isochrony, TEP resolves the tension by recognizing that time is dynamical. Cosmological expansion is an operational interpretation of a universe governed by dynamical temporal shear.

### 11.2 Theoretical Elegance: TEP versus MOND

The kinematic void model relies on Milgromian dynamics to form the KBC void, because standard gravity cannot build a void of that magnitude within the age of the universe. However, MOND itself relies on an empirically tuned acceleration constant ($a_0 \approx 1.2 \times 10^{-10}\ {\rm m\,s^{-2}}$) introduced purely to fit galaxy rotation curves. While MOND has had remarkable empirical success in describing the dynamics of individual galaxies, its status as a fundamental theory remains uncertain: the acceleration scale $a_0$ is not derived from a first-principles action but is inferred from phenomenological fits.

The TEP framework, by contrast, embeds the acoustic clock-bias mechanism in a scalar-tensor action and derives its leading environmental scaling. In this context, the environmental bias transformation $\tilde{g}_{\mu\nu} = A^2(\phi)\,g_{\mu\nu} + B(\mathcal{X})\,\nabla_\mu\phi\,\nabla_\nu\phi$ is a standard construction in scalar-tensor gravity, and the coupling of the scalar field to the matter stress-energy tensor is dictated by the action principle. The isochrony violation is not an empirical tweak appended to Newtonian dynamics; it is a natural consequence of relaxing the isochrony axiom within a well-defined field-theoretic framework. The conformal cancellation argument (Section 4.5) shows that the conformal term $A^2(\phi)$ alone cannot carry the effect — it cancels in frequency-transport operations and is bounded by spectroscopic constraints at the $\sim 10^{-3}$ level, approximately 10–30 times below the required amplitude. The disformal term $B(\mathcal{X})\,\nabla_\mu\phi\,\nabla_\nu\phi$ carries the effect (Section 4.7): it provides the non-exact transport structure — spatial shear and synchronization holonomy — that allows the core-disk clock differential to produce a residual bias in the de-redshifting operation, without generating the large conformal spectroscopic signature excluded by the core–disk line-shift bound. The bias is an observing-chain artifact: the host systemic redshift is measured from the strongly time-dilated core, while Cepheids reside in the less-dilated disk, producing $q_i^{\rm clock} = r_{\rm spec}/r_{\rm Cep} < 1$ and an artificially contracted rest-frame period. Local stellar physics is standard; no mechanical modification of stars is invoked.

The scalar-tensor completion (Section 4.6) specifies the coupling functions $A(\phi) = e^{\beta_A\phi/M_{\rm Pl}}$ and $B(\mathcal{X}) = (\beta_B/M_*^4)\,F(\mathcal{X}/M_*^4)$, and the quasi-static field profile perturbation $\delta\phi \approx 2\beta_A M_{\rm Pl}\,\Phi_N$ yields the consistency relation $\bar\epsilon_0 \propto \beta_A^2\,\beta_B \cdot \frac{V_{\rm rot}^2\,c^2}{r^2} \times \left(\frac{M_{\rm Pl}^2}{M_*^4}\right)$. The empirically fixed parameter $\bar\epsilon_0 \approx 6.39 \times 10^5$ (from $\kappa_{\rm Cep} = |b|\,\bar\epsilon_0\,\eta_P / \ln 10$, with $\eta_P = 1/2$), related to the action parameters through the parameterized synchronization-holonomy transport relation of Section 4.8, gives $\epsilon_{\rm env} \approx 0.064$ (6.4%) at typical Cepheid locations, whereas the empirical differential vanishes at the reference environment ($X_i \simeq 0$); physical solar-system screening is supplied by the scalar dynamics and remains subject to the mass-scale matching.

The conformal coupling $\beta_A$ is constrained by Cassini bounds ($|\beta_A| < 10^{-3}$). The disformal coupling does not generate the leading conformal spectroscopic signature excluded by the core–disk line-shift bound because it is dominated by the spatial and time-space sectors. The clock-response coefficient $\kappa_{\rm Cep}$, defined in Section 4.4 and quantified in Section 9, follows from the fitted relation $\kappa_{\rm Cep} = |b|\,\bar\epsilon_0\,\eta_P / \ln 10$, arising structurally from the combination of spatial shear and synchronization holonomy of the disformal transport. The remaining theoretical work is matching the DHOST mass scale to phenomenology, and specifying the microscopic completion that produces the continuously suppressed effective Temporal Shear and source charge required in the solar-system regime.

The redshift decay exponent $n \approx 0.3$ in the TEP temporal shear model occupies a different epistemic category from the MOND acceleration scale $a_0$. The MOND constant is a globally tuned replacement for the Newtonian force law — an empirical fit formulated originally without derivation from an underlying action. The TEP exponent $n$, by contrast, parameterizes a defined physical mechanism: the scaling of temporal shear accumulation with local matter density along the line of sight, within a scalar-tensor action whose structural form is fixed by the disformal metric transformation and the Klein-Gordon equation of motion. While a formal derivation from the scalar potential $V(\phi)$ remains an objective of the broader programme, the parameter governs a specific physical mechanism — temporal shear accumulation — rather than acting as an ad hoc gravitational patch. The distinction is structural: MOND replaces a force law with a fitted constant; TEP parameterizes a field interaction within a fixed action.

### 11.3 Observer-Location Fine-Tuning and the Copernican Tension

A significant structural burden of the void model is the observer-location fine-tuning: the Milky Way must sit remarkably close to the center of a billion-light-year underdensity. While the Milky Way is not at the exact geometric center of the KBC void, the required proximity is sufficiently close to raise serious fine-tuning concerns. A void of this size and depth, centered on the observer's location, is a statistical anomaly in itself, independent of the ΛCDM structure formation problem.

The TEP framework entirely avoids this problem. The acoustic clock bias happens locally within the deep gravitational potential wells of any massive SN Ia host galaxy. It relies on standard, ubiquitous galactic physics rather than a statistically anomalous observer location. No special location for the Milky Way is required; the effect is universal and operates wherever deep-potential galaxies are used as distance calibrators. The Copernican tension does not arise.

### 11.4 The DHOST Covariance Question

Both the MOND void model and the TEP framework require a relativistic covariant formulation to be complete. The MOND literature has addressed this through Degenerate Higher-Order Scalar-Tensor (DHOST) theories, which use disformal metric transformations to construct ghost-free scalar-tensor extensions of GR. The key physical distinction is that in the MOND/DHOST construction, the scalar field modifies the gravitational force law at low accelerations, while in the TEP framework, the scalar field modulates the proper time rate, producing the acoustic clock bias in Cepheid variables. The observational signatures are correspondingly distinct: the MOND mechanism produces kinematic effects that are indicator-independent, while the TEP mechanism produces calibration effects that are indicator-specific. The present paper does not depend on the detailed covariance structure of either framework.

A note on the distance-redshift relations used here is in order. The analysis uses standard flat-$\Lambda$CDM luminosity distance relations to invert Pantheon+ distance moduli for $H_0(z)$. The foundational TEP paper (Paper 0) proposes a non-standard cosmological architecture in which redshift is interpreted as conformal temporal shear ($1+z = A_0/A_{\rm em}$) rather than FLRW scale factor expansion. Standard FLRW distance variables are used here as the common operational framework because both the Pantheon+ products and the published KBC $H_0(z)$ predictions are expressed in that conventional framework. The present comparison tests the KBC prediction on its own observational coordinates without requiring the reader to adopt the global non-expanding TEP ontology in advance. A self-consistent TEP cosmological distance-redshift relation, developed in companion papers (TEP-HUB, Paper 30; TEP-BBN, Paper 29), would be required for a fully rigorous analysis at higher redshifts.

### 11.5 The Screening Mechanism and Local Tests

A critical question for any scalar-tensor modification is compatibility with local tests of the Equivalence Principle. Screening in TEP is a continuous environmental suppression of the observable Temporal Shear rather than a binary density-threshold transition. The canonical quantity is $\Sigma_\mu=\nabla_\mu\ln A$, whose observable projection is $\Sigma_\mu^{\rm obs}=\mathcal S_\Sigma(\mathcal E)\,\Sigma_\mu$. The environmental state $\mathcal E$ includes density, potential depth and gradients, source proximity, coherence scale and boundary geometry. Local laboratory and solar-system environments occupy the strongly saturated end of this continuous Temporal Topology, while galactic Cepheid environments sample a different projection of the same field structure. The bare coupling $\beta_A$ is not switched off; rather, the effective scalar charge and observable shear are continuously suppressed toward the local GR limit, providing the phenomenological suppression required by local tests of gravity, atomic clock comparisons, and lunar laser ranging; complete microscopic local-constraint matching depends on the screened $M_*$ completion.

The active regime—where the scalar field produces observable temporal shear—corresponds to the weakly screened region of this continuous structure: environments deep enough into a gravitational potential well that the gradient of $\phi$ is significant, but not so compact that the environmental screening factor $\mathcal S_\Sigma(\mathcal E)$ saturates to zero. The interiors of massive spiral galaxies, particularly the inner disks where most Cepheids are observed, fall precisely into this regime. The shallow-potential calibrators (LMC, SMC and Milky Way Cepheids in the solar neighbourhood) provide the low-shear baseline because the driving scalar gradients are small. Their screening state is determined independently by the continuous environmental operator $\mathcal S_\Sigma(\mathcal E)$, rather than by potential depth alone.

This continuous screening structure makes the TEP framework testable and falsifiable: the effect is not universal (which would have been detected in local tests) but appears specifically along the environmental gradient from shallow to deep gravitational potentials. The $F(\mathcal X)$ kinetic response function introduced in Section 4.6 is one disformal-sector realization within this broader Temporal Topology structure; the conformal and disformal sectors share the same $\phi$ field but their observable screening responses need not be identical, since the disformal holonomy depends additionally on $B$, boundary conditions, and the clock-network congruence. The companion paper TEP-EXP (Paper 9) develops the measurement taxonomy that distinguishes these regimes and identifies the proximity-regime screening transition as a key discriminating observable.

### 11.6 The Broader Landscape: Potential Extensions of the TEP Framework

The TEP framework's potential explanatory scope extends beyond the Hubble tension, though the claims listed below are more speculative than the void falsification results presented in this paper and rest on evidence developed in companion papers that have not yet undergone independent replication. The same scalar-tensor action that produces the acoustic clock bias in Cepheids may also predict:

- Environment-dependent clock rate variations in any acoustic oscillator, including Mira variables and RR Lyrae stars. This is a direct consequence of the conformal clock factor $A(\phi)$ and is testable with existing data.

- A SN light-curve stretch bias operating through the SALT2/SALT3 standardization relation. The light-curve stretch $x_1$ is a diffusion timescale — a clock — and inherits an environment-dependent bias under TEP. This channel (Section 9.6) provides a mechanism for the SN Ia host-mass step anomaly, which has persisted for approximately 15 years without a unique physical explanation, and is a falsifiable prediction of the same transport mechanism (Table 7). A preliminary test on 1,353 Pantheon+ Hubble-flow SNe finds an $X_i$-step of $+7.5 \pm 50.2$ mmag ($0.15\sigma$) in the TEP-predicted direction, with the mass-corrected $X_i$ regression at $0.71\sigma$ in the same direction; the test is underpowered because screening compresses the sample into the high-$X_i$ bin ($N_{\rm high}=1335$, $N_{\rm low}=18$). An expanded analysis ( $N=1,470$ Hubble-flow) gives $+22.3 \pm 15.1$ mmag ($1.47\sigma$) in the predicted direction; While the aggressively expanded measured-$V_{\rm rot}$ sample ($N=128$ Hubble-flow) remains structurally inconclusive ($1.06\sigma$, due to fundamental Pantheon+ selection biases against distant low-mass HI hosts), the TF-proxy enables a clean test using the full statistical power of the Pantheon+ catalog. A definitive test requires a deeper $V_{\rm rot}$ catalog that populates the low-$X_i$ bin with Hubble-flow SNe at $z > 0.03$.

- A possible explanation for the JWST high-redshift galaxy anomalies (companion paper TEP-JWST, Paper 12), where the temporal shear may affect the inferred ages and masses of high-redshift galaxies. The TEP-JWST evidence is correlational and subject to mass-circularity concerns; the kinematic test sample is small ($N=15$) and the Bayesian evidence is sensitive to mass orthogonalization. These results should be regarded as suggestive, not confirmatory.

- A reinterpretation of cosmological redshift as conformal temporal shear ($1+z = A_0/A_{\rm em}$), explored in the foundational TEP paper (Paper 0). This is a radical departure from standard cosmology that requires validation against BBN, CMB anisotropy, and BAO data, delegated to companion papers (TEP-BBN, Paper 29; TEP-HUB, Paper 30) and has not yet been independently verified. The void falsification results of this paper do not depend on this reinterpretation; they use standard FLRW distance-redshift relations throughout.

- A potential connection to the nature of dark energy, as the global evolution of $\phi(t)$ over cosmic time can mimic or replace the need for a cosmological constant. This remains speculative and is not tested in this paper.

The kinematic void model, by contrast, is specifically tailored to the Hubble tension and the bulk-flow anomaly. It does not naturally explain the JWST high-redshift anomalies, the indicator-specific distance divergence, or the internal radial gradients within individual galaxies. Its explanatory scope is narrower, and its theoretical assumptions (MOND, the KBC void, the observer-location fine-tuning) are more burdensome. However, the broader TEP claims listed above should not be conflated with the void falsification results of this paper: the falsification of the KBC void model is robust and does not depend on the JWST or cosmological-redshift-reinterpretation claims being correct.

A crucial logical point: the acoustic clock bias tested in this paper requires *only* the local, low-redshift coupling of the scalar field $\phi$ to the matter stress-energy tensor in galactic potential wells. It does not require the cosmological-redshift reinterpretation, the JWST high-$z$ framework, or any modification to the FLRW distance-redshift relation. The void falsification results (Sections 5--8) stand on their own as tests of the local distance ladder and should be evaluated on their own merits, independent of the broader cosmological claims of the TEP programme.

### 11.7 The Way Forward

The published KBC $H_0(z)$ curves are decisively rejected by the full Pantheon+ covariance. Over the model's stated validity domain ($z \ge 0.05$), the unbinned native $\mu$-space likelihood disfavours the Gaussian profile by $\Delta{\rm AIC} = +101.5$ and the Exponential by $+117.1$; extending to the full sample strengthens the rejection to $+194.3$ and $+328.7$. The rejection is robust to digitization uncertainty ($\pm 1.0\ {\rm km\,s^{-1}\,Mpc^{-1}}$ changes $\Delta{\rm AIC}$ by only $\sim 4$ units), to redshift frame, and to lower redshift cut. The calibration-independent relative evolution indicates that $H_0$ does not decline from $0.05 \le z < 0.15$ to $z > 0.25$ ($R_H \approx 1.009 \pm 0.006$, consistent with flat and $8.4\sigma$ from the KBC Gaussian prediction and $9.7\sigma$ from the Exponential, with KBC predictions evaluated through the matched GLS estimator). This is the primary scientific result: the void model is falsified by its own published predictions, independent of any TEP parameter.

Two supporting diagnostics reinforce this falsification. The indicator-specific distance divergence shows a statistically significant directional preference for the TEP-predicted sign ($2.39\sigma$ from 17/22 galaxies). The Xi regression gives a mixed picture: the pre-specified primary analysis (TEP-H0 raw, $N=18$, screened) and the independent CF4 non-R22 subset ($N=16$, screened) both give negative slopes, consistent with the TEP prediction. The CF4 full sample ($N=22$) gives a positive slope at $2.11\sigma$; an exclusion test demonstrates this is driven by two influential R22-matched galaxies associated with the registration-sensitive subset (M101 and NGC 5643); the differential shift is directly quantified for NGC 5643 — removing both flips the slope to $-1.55 \times 10^5$ ($0.34\sigma$, negative). The potential-scaling coefficient is $\kappa_{\rm Cep} = (0.45 \pm 0.22) \times 10^6$ mag from the TEP-H0 Step 44 redshift-only WLS regression in $H_0$ space ($2.05\sigma$ at $\sigma_v = 150$ km/s, negative as predicted), with the joint multi-block likelihood returning $\kappa_{\rm Cep} = (0.326 \pm 0.206) \times 10^6$ mag ($1.58\sigma$) as a consistency check. The strongest evidence comes from single-galaxy differential tests: M31 ($3.65\sigma$ from HST PHAT photometry, Kodric et al. 2018) and LMC ($3.30\sigma$ from OGLE-IV) internal radial Period--Luminosity gradients independently detect the predicted clock-gradient signal free from host-to-host peculiar velocity systematics. Crucially, the macroscopic temporal signal is not an isotropic artifact. A finite-coherence topological feature integrated along the line of sight mimics a $1/r$ kinematic velocity flow at large distances. Continuous optimization of the Pantheon+ raw magnitude residuals locks onto a coherence scale of $L_T = 55.6$ Mpc. A frozen projection gives a small out-of-sample improvement over the CF4 null ($\Delta\mathrm{RSS} = 17.8$), but the CF4 sample, dominated by galaxies at $D \gg L_T$ where the finite-coherence kernel becomes degenerate with $1/r$, does not discriminate the finite-coherence profile from its $1/r$ asymptote.

### 11.8 $X_i$-step Estimator Consistency

The $X_i$-step tests return consistent directional evidence across estimators: the full-sample dichotomous step ($N=1470$) gives $+22.3 \pm 15.1$ mmag ($+1.47\sigma$) in the TEP-predicted direction, and the joint OLS $X_i$ coefficient after mass correction gives $+7.92 \times 10^4 \pm 3.75 \times 10^4$ ($+2.11\sigma$). The joint coefficient retains the TEP-predicted sign at $2.11\sigma$ after inclusion of host mass, although interpretation is limited by severe $X_i$–mass multicollinearity; the measured-$V_{\rm rot}$ sample remains the decisive test. The CF4 full-sample Xi regression ($+2.11\sigma$, opposite sign) is the single contrary result; an exclusion test (Section 5.4) demonstrates this is driven by two influential R22-matched galaxies (M101 and NGC 5643) where CF4 registration shifts are largest. The present auxiliary potential-scaling evidence is therefore directionally consistent with TEP across all estimators except the registration-confounded CF4 subset. The weight of the paper rests on the $\Delta\chi^2 \gt 100$ native $\mu$-space falsification of the void model (Sections 7--8), with the auxiliary tests providing directional context rather than independent statistical power.

## 12. Conclusions

The published kinematic void profiles are rejected at high significance. Given the freedom to adjust its amplitude and scale, the void family's optimal fit collapses to a flat line. The published KBC/MOND kinematic-void family tested here is therefore ruled out. Over the model's own stated validity domain ($z \ge 0.05$), the unbinned native $\mu$-space likelihood disfavours the Gaussian profile by $\Delta{\rm AIC} = +101.5$ and the Exponential by $+117.1$, retaining all 1,053 Pantheon+ rows in range with the matched $1{,}053 \times 1{,}053$ submatrix of the native Pantheon+ STAT+SYS covariance and a marginalized common zero-point. Extending to the full sample strengthens the rejection to $+194.3$ and $+328.7$. When amplitude and scale are released, maximum likelihood occurs at zero void amplitude: the void family collapses to its flat limit ($\Delta H_0^{\rm ML} = 0$). The calibration-independent ratio $R_H = 1.009 \pm 0.006$ excludes the predicted 5% decline at $8.4\sigma$ (Gaussian) and $9.7\sigma$ (Exponential), where the KBC model predictions are evaluated through the same two-bin GLS covariance-aware estimator used for the observed $R_H$ (not arithmetic means of the KBC curve in each bin). The rejection is robust to digitization uncertainty, redshift frame, and lower redshift cut.

The surviving observational anomalies — the indicator divergence, the potential dependence, the calibration sensitivity, and the finite-coherence macroscopic temporal topology — form a combined pattern not explained by a single pure kinematic outflow, as demanded by the Temporal Equivalence Principle. The conventional $v_{\rm pec} = cz - H_0 d$ estimator produces an apparent $155\ {\rm km\,s^{-1}}$ Cepheid excess and a $2.33\sigma$ directional split; the $H_0$-invariant log-distance estimator gives $\Delta B = 0.0$ km/s, showing that the standard estimator is calibration-sensitive. The candidate macroscopic temporal component is the finite-coherence feature: continuous optimization of the pre-standardization Pantheon+ residuals locks onto a finite-coherence scale $L_T = 55.6$ Mpc. A frozen projection gives a small out-of-sample improvement over the CF4 null ($\Delta\mathrm{RSS} = 17.8$ vs null, $N = 51{,}904$), but CF4 does not discriminate the finite-coherence profile from its $1/r$ asymptote. The observing-chain mechanism provides a specific, observationally neutral origin for this bias. 17 of 22 galaxies with both Cepheid and TRGB distances show Cepheid distances shorter than TRGB ($2.39\sigma$ one-sided sign test). The Xi regression gives a negative slope on the primary analysis and on the independent CF4 non-R22 subset; the CF4 full sample gives a positive slope at $2.11\sigma$, but an exclusion test demonstrates this is driven by two influential R22-matched galaxies (M101 and NGC 5643). The potential-scaling coefficient is $\kappa_{\rm Cep} = (0.45 \pm 0.22) \times 10^6$ mag ($2.05\sigma$ at $\sigma_v = 150$ km/s from the redshift-only WLS in $H_0$ space; $1.58\sigma$ from the joint multi-block likelihood). The strongest evidence comes from single-galaxy differential tests: M31 ($3.65\sigma$ from HST PHAT photometry, Kodric et al. 2018) and LMC ($3.30\sigma$ from OGLE-IV) internal radial Period--Luminosity gradients independently detect the predicted clock-gradient signal free from host-to-host peculiar velocity systematics. TEP additionally predicts an independent SN light-curve stretch channel that provides a mechanism for the host-mass step, which has persisted for $\sim$15 years without a unique physical explanation, and is consistent with the Jensen et al. (2025) TRGB-anchored SBF result. A preliminary $X_i$-step test on 1,353 Pantheon+ Hubble-flow SNe finds $+7.5 \pm 50.2$ mmag ($0.15\sigma$) in the predicted direction with measured $V_{\rm rot}$ where available and the Tully-Fisher proxy otherwise (underpowered: screening leaves only $N_{\rm low}=18$ low-$X_i$ hosts); an expanded analysis ($N=1,470$ Hubble-flow) gives $+22.3 \pm 15.1$ mmag ($1.47\sigma$) in the predicted direction, with the joint OLS $X_i$ coefficient after mass correction at $+7.92 \times 10^4 \pm 3.75 \times 10^4$ ($2.11\sigma$). The joint coefficient retains the TEP-predicted sign at $2.11\sigma$ after inclusion of host mass, although interpretation is limited by severe $X_i$–mass multicollinearity; the measured-$V_{\rm rot}$ sample remains the decisive test. The aggressively expanded measured-$V_{\rm rot}$ subsample ($N=128$ Hubble-flow) currently remains structurally inconclusive due to fundamental Pantheon+ selection bias against distant low-mass HI hosts (unbalanced $N_{\rm high}=121$, $N_{\rm low}=7$). The quantitative development of the two channels and the definitive radial-gradient tests are given in the companion TEP-H0 paper.

### 12.1 The Three Observables

Observable III — $H_0(z)$ redshift profile (Sections 7--8), *the primary falsification*: The published KBC/MOND model predicts a gradual decline in $H_0(z)$, converging to within $1\sigma$ of Planck only at $z \gtrsim 1.8$ (Mazurenko et al. 2025). TEP predicts a flat $H_0(z) \approx 73$ when $M_B$ is global, because the Cepheid clock bias is encoded in the zero-point rather than distributed across redshift. The Pantheon+ data are flat across all redshifts, decisively disfavouring the published KBC gradual decay curves (digitized from Mazurenko et al. 2025, Figure 3) by $\Delta$AIC $= +101.5$ (Gaussian) and $+117.1$ (Exponential) over the valid $z \ge 0.05$ domain using the unbinned native $\mu$-space likelihood with a marginalized zero-point; $+194.3$ and $+328.7$ over the full sample. The rejection is robust to digitization uncertainty ($\pm 1.0\ {\rm km\,s^{-1}\,Mpc^{-1}}$ leaves $\Delta$AIC $> 190$ over the full release), to redshift frame, and to lower redshift cut. The calibration-independent relative evolution indicates that $H_0$ does not decline from $0.05 \le z < 0.15$ to $z > 0.25$ ($R_H \approx 1.009 \pm 0.006$, $8.4\sigma$ from the KBC Gaussian prediction and $9.7\sigma$ from the Exponential, with the KBC predictions evaluated through the matched GLS estimator). The void model is falsified by its own published predictions, independent of any TEP parameter.

Observable I — Indicator-specific distance divergence (Section 5): A kinematic outflow is indicator-independent, so the void model predicts that Cepheid and TRGB distances to the same galaxies should agree. TEP predicts that Cepheid distances are systematically shorter due to the observing-chain clock bias. The sign test gives a statistically significant directional preference: 17 of 22 CF4 galaxies show Cepheid distances shorter than TRGB ($p = 0.0085$, $2.39\sigma$ one-sided), with the signal stronger in the non-R22 subset (13/16, $2.30\sigma$). The Xi regression gives a mixed picture: the pre-specified primary analysis (TEP-H0 raw data, $N=18$, screened) gives a negative slope ($-1.01 \times 10^5 \pm 3.79 \times 10^5$ mag), and the independent CF4 non-R22 subset ($N=16$, screened) also gives a negative slope ($-5.46 \times 10^5 \pm 5.60 \times 10^5$ mag, $0.98\sigma$). The CF4 full sample ($N=22$) gives a positive slope at $2.11\sigma$. An exclusion test shows that two influential R22-matched galaxies in the registration-sensitive subset (M101 and NGC 5643) drive this result; the differential shift is directly quantified for NGC 5643. Removing both galaxies flips the slope to $-1.55 \times 10^5$ ($0.34\sigma$, negative). The TEP-H0 Step 44 redshift-only WLS regression in $H_0$ space yields $\kappa_{\rm Cep} = (0.45 \pm 0.22) \times 10^6$ mag ($2.05\sigma$ at $\sigma_v = 150$ km/s), consistent with the predicted negative slope. The joint multi-block likelihood returns $1.58\sigma$ as a consistency check. Single-galaxy differential tests provide the strongest evidence: M31 ($3.65\sigma$ from HST PHAT photometry, Kodric et al. 2018) and LMC ($3.30\sigma$ from OGLE-IV) internal radial Period--Luminosity gradients independently detect the predicted clock-gradient signal free from host-to-host peculiar velocity systematics. The void model has no mechanism to produce an indicator-specific offset within the same galaxy.

Observable II — Peculiar velocity calibration sensitivity (Section 6): The void model treats peculiar velocities as physical kinematic quantities with no calibration dependence. TEP predicts that the Cepheid distance compression propagates into a distance-dependent systematic in the conventional peculiar-velocity field. The calibration differential between Cepheid- and TRGB-anchored $H_0$ introduces a shift of $-3.2 \times d$ km/s in the standard $v_{\rm pec} = cz - H_0 d$ estimator. A proper $H_0$-invariant log-distance estimator removes this artifact, giving identical bulk-flow amplitudes ($B = 290.0$ km/s) under the two calibrations and a differential flow consistent with zero. The candidate macroscopic temporal component is the finite-coherence feature: continuous optimization on the pre-standardization Pantheon+ residuals yields $L_T = 55.6$ Mpc ($p < 0.001$). A frozen projection gives a small out-of-sample improvement over the CF4 null, but CF4 does not discriminate the finite-coherence profile from its $1/r$ asymptote. The host-potential-dependent extension (Section 6.1) predicts that the velocity shift correlates with $v_{\rm rot}$ and anti-correlates with group richness — a signature no pure kinematic void can produce.

### 12.2 Two-Channel TEP Correction of Pantheon+

Section 9 applies the TEP correction through two distinct channels. Channel 1 (Cepheid period transport) operates through the calibration chain: the Cepheid calibrator $\to$ $\Delta M_B^{\rm Cep} \to$ Pantheon+ route. The mean correction over the calibrator hosts determines a single $\Delta M_B^{\rm Cep} = \kappa_{\rm Cep}^{\rm equiv} \cdot \langle X_i \rangle_{\rm calibrators}$, with $\kappa_{\rm Cep}^{\rm equiv} = (0.365 \pm 0.304) \times 10^6\ {\rm mag}$ from the endpoint slope conversion in TEP-H0 (Paper 11). This zero-point shift propagates uniformly to all Pantheon+ supernovae, producing a direct calibrator-average shift of $+0.035 \pm 0.030$ mag in the TEP-predicted direction. Propagating this through the SH0ES design matrix yields $H_0 = 71.77 \pm 0.99\ {\rm km\,s^{-1}\,Mpc^{-1}}$; the residual absorption by the 37 unconstrained latent host moduli limits the matrix-level correction. Paper 11's Step 04 unified host-level reconstruction, which bypasses the matrix degeneracy by working in expansion-rate space, yields $H_0 = 66.65 \pm 1.58\ {\rm km\,s^{-1}\,Mpc^{-1}}$, consistent with Planck at $0.45\sigma$.

Channel 2 (SN light-curve stretch) operates on the Hubble-flow SNe themselves through the SALT2/SALT3 standardization relation $\mu = m_B - M_B + \alpha\,x_1 - \beta\,c + \Delta_{\rm host}$. The light-curve stretch $x_1$ is a diffusion timescale — a clock — and inherits an environment-dependent bias under TEP. The observed SN Ia host-mass step ($\sim 0.04$–$0.06$ mag) is the observational signature predicted by this channel. The SN channel is a falsifiable prediction of the same transport mechanism, not a post hoc adjustment: the Cepheid channel reconstruction already yields $H_0 = 66.65 \pm 1.58$. A preliminary test of the $X_i$-step prediction on 1,353 Pantheon+ Hubble-flow SNe finds a step of $+7.5 \pm 50.2$ mmag ($0.15\sigma$) in the TEP-predicted direction (high-$X_i$ hosts have more positive Hubble residuals), underpowered because screening compresses the sample into the high-$X_i$ bin ($N_{\rm high}=1335$, $N_{\rm low}=18$); the mass-corrected $X_i$ regression gives $0.71\sigma$ in the same direction. An expanded analysis uses measured $V_{\rm rot}$ from HyperLEDA (Vizier VII/237, VII/238) for 173 Pantheon+ hosts (33 calibrators, 140 Hubble-flow), with the Tully-Fisher proxy retained for the remaining hosts. The full sample ($N=1,470$ Hubble-flow) shows $+22.3 \pm 15.1$ mmag ($+1.47\sigma$), the TEP-predicted sign. The aggressively expanded measured-$V_{\rm rot}$-only subsample ($N=128$ Hubble-flow) remains too structurally unbalanced ($N_{\rm high}=121$, $N_{\rm low}=7$) for a standalone step; its mass-residualized step is $+131.1 \pm 123.6$ mmag ($+1.06\sigma$), in the TEP-predicted direction, with a larger amplitude consistent with the deeper potential leverage of the measured-$V_{\rm rot}$ sample. The low-$X_i$ bin is concentrated at very low redshift (median $z = 0.020$, maximum $z = 0.064$) and is contaminated by peculiar velocities. Deep 21-cm HI surveys rarely intersect with the distant, low-mass hosts selected by Pantheon+, introducing a fundamental selection bias. The Hubble-flow $X_i$-step with measured $V_{\rm rot}$ is therefore consistent with TEP but inconclusive: the small, nearby, unbalanced subsample does not provide a clean test. A definitive test requires a deeper, more complete $V_{\rm rot}$ catalog (SPARC, ALFALFA, or broader HyperLEDA coverage) that would populate the low-$X_i$ bin with Hubble-flow SNe at $z > 0.03$ where peculiar velocities are subdominant.

### 12.3 Relationship to the Companion Paper

The single-galaxy radial gradients in M31 and the LMC, and the full distance-ladder $H_0$ unification, are established in the companion paper TEP-H0 (Paper 11, DOI: 10.5281/zenodo.18209702). That paper demonstrates the TEP clock bias at $3.65\sigma$ in M31, $3.30\sigma$ in the LMC, and resolves the local $H_0$ to $66.65 \pm 1.58\ {\rm km\,s^{-1}\,Mpc^{-1}}$, consistent with Planck at $0.45\sigma$ ($0.31\sigma$ bootstrap). The Cepheid-channel coupling coefficient is measured by two complementary TEP-H0 analyses that converge: $\kappa_{\rm Cep}^{\rm equiv} = (0.365 \pm 0.304) \times 10^6$ mag (TEP-H0 endpoint slope conversion) and $\kappa_{\rm Cep} = (0.45 \pm 0.22) \times 10^6$ mag (TEP-H0 Step 44, redshift-only WLS in $H_0$ space, $2.05\sigma$ at $\sigma_v = 150$ km/s; $1.58\sigma$ from the joint multi-block likelihood). The present paper falsifies the void model using data that is partially independent of TEP-H0: the $H_0(z)$ test uses Pantheon+, the sign test uses the CF4 catalog, and the Xi regression on CF4 non-R22 data ($N = 16$) uses galaxies that do not overlap with the SH0ES host sample. The Xi regression on TEP-H0 raw data ($N = 18$) is a consistency check on the same SH0ES hosts, not an independent test.

### 12.4 Theoretical Implications

The falsification of the KBC void model has implications beyond the Hubble tension. The void model required MOND to form a $600\ {\rm Mpc}$ underdensity within the age of the universe, which standard gravity cannot do. If the void is not the explanation, the specific motivation for invoking MOND to sustain this Gpc-scale void solution is removed. The TEP framework, by contrast, is a scalar-tensor theory grounded in disformal scalar-tensor transformations and environmental screening mechanisms. The acoustic clock bias is a natural consequence of elevating proper time to a dynamical field. The quantitative coupling $\kappa_{\rm Cep}$ (the distance-modulus channel coefficient, defined in Section 4.4 and quantified in Section 9) is empirically determined in TEP-H0 (Paper 11) from the SH0ES host sample. A first-principles determination of the transport coefficient and disformal mass-scale matching from the full non-radial solution is the remaining theoretical step.

### 12.5 The Path to Definitive Confirmation

The falsification pathways outlined in Section 10 provide a clear roadmap. The most decisive tests are: (i) expanding the matched Cepheid/TRGB galaxy sample with a common geometric anchor and a single consistent Cepheid reduction pipeline — the Xi regression (Section 5.5) shows that the TEP potential-scaling signal is recovered with the correct negative sign on unconfounded data, but the simple regression is underpowered at $N=18$; (ii) per-host Cepheid recalibration of the Pantheon+ sample (TEP-H0, Paper 11) to test the $(1+z)^{-0.3}$ decay and host-mass dependence directly; and (iii) intra-host differential tests comparing Cepheid and TRGB distances within the same galaxy using JWST. Roman/LSST high-$z$ SNe can test the redshift-profile structure, but the Cepheid-channel host dependence requires nearby/mid-distance Cepheid hosts with TRGB cross-checks.

### 12.6 Final Statement

The evidence converges on several mutually reinforcing conclusions. First, the published KBC $H_0(z)$ curves are decisively rejected by the full Pantheon+ covariance ($\Delta{\rm AIC} > 100$ over the valid domain, $>190$ over the full sample). When allowed to vary, the void family collapses to a flat limit ($\Delta H_0^{\rm ML} = 0$). The calibration-independent ratio $R_H$ excludes the predicted decline at $>8.4\sigma$.

Second, a separate low-redshift directional test finds that the pre-standardization Pantheon+ residual field is better represented by a finite-coherence profile with characteristic scale $L_T \simeq 56$ Mpc along the independently measured CF4 axis than by the previously assumed global linear-gradient profile. This identifies a candidate local environmental coherence scale for the macroscopic temporal-field perturbation and motivates the independent CF4 cross-prediction test (Section 6.5). The standardization process suppresses approximately 70% of this pre-standardization directional signal, with the residual remaining significant in the standardized residuals.

Third, indicator comparisons show the directional signature expected from acoustic-clock bias, forming a combined pattern not explained by a single pure kinematic outflow ($2.39\sigma$ sign test; Xi regression negative on the primary analysis and on the independent CF4 non-R22 subset; $\kappa_{\rm Cep} = (0.45 \pm 0.22) \times 10^6$ mag, $2.1\sigma$ from redshift-only WLS; $1.6\sigma$ from joint multi-block; M31 $3.65\sigma$ and LMC $3.30\sigma$ internal gradients). Fourth, the Cepheid channel reconstruction (Paper 11, Step 04) yields $H_0 = 66.65 \pm 1.58\ {\rm km\,s^{-1}\,Mpc^{-1}}$, consistent with Planck at $0.45\sigma$. TEP additionally predicts an independent SN light-curve stretch channel that provides a mechanism for the host-mass step, which has persisted for $\sim$15 years without a unique physical explanation, and is consistent with the Jensen et al. (2025) TRGB-anchored SBF result. The host-potential dependence of the SN stretch channel remains an uncalibrated prediction pending a decisive measured-$V_{\rm rot}$ sample test.

Fifth, the conformal term cannot carry the effect without violating spectroscopic line-shift bounds. Instead, the disformal metric sector provides the spatial shear and synchronization holonomy necessary to translate the core-disk clock differential ($q_i^{\rm clock} < 1$) into an observing-chain bias. The conformal sector satisfies the relevant spectroscopic/Cassini bound; the effective galactic disformal coupling is not subject to that same leading conformal constraint, while complete local-constraint matching depends on the screened $M_*$ completion.

The remaining open issues are the $2.1\sigma$ redshift-only Cepheid coupling, independent replication of the M31 and LMC internal gradients, the inconclusive $X_i$-step with measured $V_{\rm rot}$ (selection-biased subsample), the DHOST-to-phenomenology mass-scale matching, and the need for measured rotation velocities for the full Hubble-flow sample. The falsifiable predictions — band-dependence (Pathway V, cross-team point estimate has the predicted negative sign but is statistically uninformative at $0.16\sigma$ ($N=9$), while the same-team test yields a wrong-sign positive slope that is consistent with a leverage/correlated-systematics explanation, reversing to $-4.87\sigma$ upon removal of a single galactocentric-leverage outlier (M101)), tracer-type dependence (Pathway VI, null; implications for the disformal term remain dependent on the full non-radial geometry), the JWST matched sample ($N=17$, mean $\Delta\mu = -0.023$, $1.02\sigma$, $\chi^2/{\rm dof} = 0.77$), the $X_i$-step with measured $V_{\rm rot}$, and the $V_{\rm rot}^2/r^2$ scaling of $\bar\epsilon_0$ — are testable with existing and near-future data.

The Hubble tension, in this interpretation, is not a crisis of cosmic expansion but an artifact of observation. The evidence is consistent with a two-channel clock-calibration bias. It derives from a Horndeski/kinetic-braiding scalar-tensor completion with specified coupling functions $A(\phi) = e^{\beta_A\phi/M_{\rm Pl}}$ and $B(\mathcal{X}) = (\beta_B/M_*^4)\,F(\mathcal{X}/M_*^4)$, yielding a consistency relation for $\bar\epsilon_0$ that is compatible with Cassini solar-system bounds; the DHOST natural-unit to mass-scale matching remains unresolved. The disformal transport mechanism is dominated by the spatial and time-space sectors of the disformal metric; it does not generate the leading conformal spectroscopic signature and produces a transport signature distinct from the leading conventional systematics considered here. The band-dependence cross-team point estimate returns the predicted negative sign (albeit statistically uninformative), while the same-team comparison shows the wrong sign due to correlated systematics; the JWST matched sample shows the predicted negative mean $\Delta\mu$ with scatter consistent with the model; the $X_i$-step is inconclusive due to catalog depth limitations. The quantitative development of the two channels and the definitive radial-gradient tests are given in the companion TEP-H0 paper. Within TEP, there is no physical Hubble expansion to be reconciled. The spatial universe is static and eternal; cosmological redshift records the evolution and transport of dynamical proper time. The quantity conventionally called $H_0$ is therefore an operational redshift–distance slope. The local tension arises when environment-dependent matter-clock transport is forced into a globally isochronous calibration. The KBC solution attempts to repair the tension by modifying motion within an expanding universe; the present results instead support examining the deeper premise that the observed redshift field represents expansion at all.

Finally, recognizing that complex data pipelines are subject to hidden systematics, the quantitative basis of this framework—specifically the extraction of $\kappa_{\rm Cep}$ and the rejection of the KBC void—must be externally verifiable. All scripts, exact data inputs, covariance mappings, and analysis outputs (including a known-answer test suite with injected synthetic signals validating the regression pipeline) required to reproduce the headline likelihood and $\kappa_{\rm Cep}$ calculations are archived with the project and available for independent reproduction.

## References

Riess, A. G., Anand, G. S., Yuan, W., et al. (2024a). "JWST Observations Reject Unrecognized Crowding of Cepheid Photometry as an Explanation for the Hubble Tension at $8\sigma$ Confidence." *Astrophysical Journal Letters*, 962, L17. JWST observations of $>1000$ Cepheids validating HST photometry; crowding rejected at $8.2\sigma$.

Riess, A. G., Anand, G. S., Yuan, W., et al. (2024b). "JWST Validates HST Distance Measurements: Selection of Supernova Subsample Explains Differences in JWST Estimates of Local $H_0$." *Astrophysical Journal*, 977, 120. Linearity of HST Cepheid distances at $0.994 \pm 0.010$; distance-dependent bias ruled out at $\sim 7\sigma$.

Freedman, W. L., Madore, B. F., Hoyt, T. J., et al. (2019). "The Carnegie-Chicago Hubble Program. VIII. An Independent Determination of the Hubble Constant Based on the Tip of the Red Giant Branch." *Astrophysical Journal*, 882, 34. CCHP TRGB calibration yielding $H_0 = 69.8 \pm 0.8\ ({\rm stat}) \pm 1.7\ ({\rm sys})\ {\rm km\,s^{-1}\,Mpc^{-1}}$.

Freedman, W. L., Madore, B. F., Hoyt, T. J., et al. (2025). "Status Report on the Chicago-Carnegie Hubble Program (CCHP): Measurement of the Hubble Constant Using the Hubble and James Webb Space Telescopes." *Astrophysical Journal*, 985, 203. CCHP TRGB and JAGB calibrations yielding $H_0 = 68.81 \pm 1.79\ ({\rm stat}) \pm 1.32\ ({\rm sys})\ {\rm km\,s^{-1}\,Mpc^{-1}}$ (TRGB) and $H_0 = 67.80 \pm 2.17\ ({\rm stat}) \pm 1.64\ ({\rm sys})\ {\rm km\,s^{-1}\,Mpc^{-1}}$ (JAGB).

Mazurenko, S., Banik, I., Kroupa, P., & Haslbauer, M. (2024). "A simultaneous solution to the Hubble tension and observed bulk flow within $250\ h^{-1}\ {\rm Mpc}$." *Monthly Notices of the Royal Astronomical Society*, 527, 4388&ndash;4396. MOND-driven KBC void model; simultaneous resolution of Hubble tension and CosmicFlows-4 bulk flow; $1.14\%$ significance level with external field $0.055\,a_0$.

Haslbauer, M., Banik, I., & Kroupa, P. (2020). "The KBC void and Hubble tension contradict ΛCDM on a Gpc scale—Milgromian dynamics as a possible solution." *Monthly Notices of the Royal Astronomical Society*, 499, 2845&ndash;2883. Mathematical demonstration that KBC void outflows inflate apparent redshifts by $\sim 9\%$; joint $7.09\sigma$ tension with ΛCDM.

Watkins, R., Allen, T., Bradford, C. J., et al. (2023). "Analysing the large-scale bulk flow using cosmicflows4: increasing tension with the standard cosmological model." *Monthly Notices of the Royal Astronomical Society*, 524, 1885--1892. $4.6\sigma$ bulk-flow tension with ΛCDM at $200\ h^{-1}\ {\rm Mpc}$.

Stiskalek, J., Desmond, H., & Banik, I. (2025). "Testing the local supervoid solution to the Hubble tension with direct distance tracers." *Monthly Notices of the Royal Astronomical Society*, 543, 1556&ndash;1573. Direct CF4 galaxy-by-galaxy fits find preferred void sizes $\lesssim 70$ Mpc; Gaussian and Maxwell–Boltzmann cases give $H_0 \sim 70.4$, $70.2$; exponential disfavoured by Bayesian evidence. Notes a misunderstanding in the earlier M24 bulk-flow analysis.

Keenan, R. C., Barger, A. J., & Cowie, L. L. (2013). "Evidence for a $\sim 300$ Mpc Scale Under-density in the Local Galaxy Distribution." *Astrophysical Journal*, 775, 62. Observational evidence for the KBC void: $\delta = 0.46 \pm 0.06$ underdensity extending 40--300 Mpc.

Vagnozzi, S. (2023). "Seven Hints That Early-Time New Physics Alone Is Not Sufficient to Solve the Hubble Tension." *Universe*, 9, 393. Seven distinct reasons why early-time solutions to the Hubble tension are not viable.

Planck Collaboration (2020). "Planck 2018 Results VI. Cosmological Parameters." *Astronomy & Astrophysics*, 641, A6. CMB inference of $H_0 = 67.4 \pm 0.5\ {\rm km\,s^{-1}\,Mpc^{-1}}$.

Smawfield, M. L. (2025). "Temporal Equivalence Principle: Dynamic Time & Emergent Light Speed." Preprint, Zenodo DOI: 10.5281/zenodo.16921911. Foundational TEP framework; scalar-tensor action; disformal metric transformation; synchronization holonomy.

Smawfield, M. L. (2025). "Global Time Echoes: Distance-Structured Correlations in GNSS Clocks." Preprint, Zenodo DOI: 10.5281/zenodo.17127229. (TEP-GNSS, Paper 1). GNSS clock-network test of residual synchronization holonomy at the $10^{-18}$–$10^{-19}$ fractional level.

Smawfield, M. L. (2025). "Global Time Echoes: 25-Year Analysis of CODE Precise Clock Products." Preprint, Zenodo DOI: 10.5281/zenodo.17517141. (TEP-GNSS-II, Paper 2). Quarter-century GNSS clock correlation analysis.

Smawfield, M. L. (2026). "Global Time Echoes: Raw RINEX Consistency Test." Preprint, Zenodo DOI: 10.5281/zenodo.17860166. (TEP-GNSS-RINEX, Paper 3). Raw RINEX-level consistency validation of GNSS clock correlations.

Smawfield, M. L. (2026). "The Cepheid Bias: Resolving the Hubble Tension." Preprint, Zenodo DOI: 10.5281/zenodo.18209702. (TEP-H0, Paper 11). Companion paper: 37-host endpoint likelihood; M31 and LMC differential tests; unified $H_0 = 66.65 \pm 1.58\ {\rm km\,s^{-1}\,Mpc^{-1}}$.

Smawfield, M. L. (2026). "What Do Precision Tests of General Relativity Actually Measure?" Preprint, Zenodo DOI: 10.5281/zenodo.18109760. (TEP-EXP, Paper 9). Measurement taxonomy; screening regimes; proximity-regime screening transition.

Smawfield, M. L. (2026). "Temporal Equivalence Principle: A Unified Resolution to the JWST High-Redshift Anomalies." Preprint, Zenodo DOI: 10.5281/zenodo.19000827. (TEP-JWST, Paper 12). Temporal shear effects on high-redshift galaxy ages and masses.

Smawfield, M. L. (2026). "The Mount Wilson Paradigm: Restoring the Eternal Universe via the Temporal Equivalence Principle." Preprint, Zenodo DOI: 10.5281/zenodo.21954258. (TEP-HUB, Paper 30). Cosmological redshift as conformal temporal shear; TEP distance-redshift relation on a static spatial manifold.

Smawfield, M. L. (2026). "Temporal Equivalence Principle: Dynamical Proper Time and the Illusion of Primordial Deuterium." Preprint, Zenodo DOI: 10.5281/zenodo.21841148. (TEP-BBN, Paper 29). Deuterium isotope identifiability; temporal transport framework for primordial abundance observables.

Kodric, M., Riffeser, A., Hopp, U., et al. (2018). "Cepheids in M31: The PAndromeda Cepheid Sample." *Astronomical Journal*, 156, 130. Pan-STARRS Cepheid catalog of M31: 2,686 variables used in the M31 internal radial gradient analysis.

Soszyński, I., Udalski, A., Szymański, M. K., et al. (2015). "OGLE-IV Cepheids in the Large Magellanic Cloud." *Acta Astronomica*, 65, 297&ndash;312. OGLE-IV fundamental-mode Cepheid catalog of the LMC used in the LMC radial stratification analysis.

Garnavich, P., Wood, C. M., Milne, P., Jensen, J. B., Blakeslee, J. P., et al. (2023). "Connecting Infrared Surface Brightness Fluctuation Distances to Type Ia Supernova Hosts: Testing the Top Rung of the Distance Ladder." *Astrophysical Journal*, 953, 35. IR SBF calibration yielding $H_0 = 74.6 \pm 0.9\ ({\rm stat}) \pm 2.7\ ({\rm sys})\ {\rm km\,s^{-1}\,Mpc^{-1}}$; uses Jensen et al. SBF distances as an intermediate step between Cepheids and SNe Ia.

Milgrom, M. (1983). "A Modification of the Newtonian Dynamics as a Possible Alternative to the Hidden Mass Hypothesis." *Astrophysical Journal*, 270, 365. Foundational MOND paper; acceleration scale $a_0 \approx 1.2 \times 10^{-10}\ {\rm m\,s^{-2}}$.

Langlois, D. (2019). "Degenerate Higher-Order Scalar-Tensor (DHOST) Theories." *International Journal of Modern Physics D*, 28, 1942006. Ghost-free scalar-tensor constructions via disformal metric transformations; Ostrogradsky instability avoidance.

Riess, A. G., Yuan, W., Macri, L. M., et al. (2022). "A Comprehensive Measurement of the Local Value of the Hubble Constant with 1 km s$^{-1}$ Mpc$^{-1}$ Uncertainty." *Astrophysical Journal Letters*, 934, L7. SH0ES 42-SN Ia Cepheid calibration: $H_0 = 73.0 \pm 1.0\ {\rm km\,s^{-1}\,Mpc^{-1}}$.

Scolnic, D., Brout, D., Carr, A., et al. (2022). "The Pantheon+ Analysis: The Full Data Set and Light-Curve Release." *Astrophysical Journal*, 938, 113. Pantheon+ supernova distance-redshift catalog.

Tully, R. B., Kourkchi, E., Courtois, H. M., et al. (2023). "Cosmicflows-4." *Astrophysical Journal*, 944, 94. CosmicFlows-4 peculiar-velocity catalog; 55,877 galaxies in 38,065 groups; the present analysis uses 38,053 groups from the VizieR table4.dat release after quality cuts.

Riess, A. G., Li, S., Anand, G. S., et al. (2025). "The Perfect Host: JWST Cepheid Observations in a Background-free Type Ia Supernova Host Confirm No Bias in Hubble-constant Measurements." *Astrophysical Journal Letters*, 992, L34. JWST Cycle 2 Cepheid observations in NGC 3447; combined HST+JWST calibration yields $H_0 = 73.49 \pm 0.93\ {\rm km\,s^{-1}\,Mpc^{-1}}$; HST-JWST difference consistent with zero.

Mazurenko, S., Banik, I., & Kroupa, P. (2025). "The redshift dependence of the inferred $H_0$ in a local void solution to the Hubble tension." *Monthly Notices of the Royal Astronomical Society*, 536, 3232&ndash;3241. DOI: 10.1093/mnras/stae2758. Method-3 $H_0(z)$ predictions for Gaussian, Exponential, and Maxwell&ndash;Boltzmann void density profiles from HBK20 parameters; Gaussian and Exponential profiles converge to within $1\sigma$ of Planck only at $z \gtrsim 1.8$.

Jia, X. D., Hu, J. P., & Wang, F. Y. (2023). "Evidence of a decreasing trend for the Hubble constant." *Astronomy & Astrophysics*, 674, A45. DOI: 10.1051/0004-6361/202346356. Non-parametric piecewise $H_{0,z_i}$ reconstruction from Pantheon+ combined with $H(z)$ and BAO data; declining $H_0(z)$ at $5.6\sigma$ (equal-width binning). The decline does not survive the piecewise $H_{\rm th}$ estimator with Pantheon+ SN-only data, regardless of error treatment (diagonal, full $1701 \times 1701$ STAT+SYS covariance, or full covariance with marginalized zero-point); it is driven by the $H(z)$ and BAO data.

Kenworthy, W. D., Scolnic, D., & Riess, A. G. (2019). "The Local Perspective on the Hubble Tension: Local Structure Does Not Impact Measurement of the Hubble Constant." *Astrophysical Journal*, 875, 145. DOI: 10.3847/1538-4357/ab0ebf. Used the Pantheon SN Ia sample to search for a local void signal in the Hubble flow; ruled out a local underdensity as the cause of the Hubble tension. This aligns with an independent analysis of the same dataset family.

Wang, D. (2023). "Pantheon+ Tomography and Hubble Tension." *European Physical Journal C*, 83, 813. DOI: 10.1140/epjc/s10052-023-11991-0. Independent Pantheon+ tomographic analysis finding no obvious evidence for evolution of $H_0$ or $\Omega_m$ at the $2\sigma$ level using both equal-redshift and equal-count binning, consistent with a flat $H_0(z)$ profile.

Jensen, J. B., Blakeslee, J. P., Cantiello, M., et al. (2025). "The TRGB-SBF Project. III. Refining the HST Surface Brightness Fluctuation Distance Scale Calibration with JWST." *Astrophysical Journal*, 987, 87. Cepheid-independent SBF calibration using JWST TRGB distances anchored to NGC 4258, yielding $H_0 = 73.8 \pm 0.7\ ({\rm stat}) \pm 2.3\ ({\rm sys})\ {\rm km\,s^{-1}\,Mpc^{-1}}$. Provides a clean-anchor test that motivates the two-channel TEP interpretation: the Cepheid channel is absent while the SN stretch channel remains.

Freedman, W. L., Madore, B. F., Gibson, B. K., et al. (2001). "Final Results from the Hubble Space Telescope Key Project to Measure the Hubble Constant." *Astrophysical Journal*, 553, 47. HST Key Project Cepheid calibration yielding $H_0 = 72 \pm 8\ {\rm km\,s^{-1}\,Mpc^{-1}}$; historical reference for the pre-SH0ES Cepheid distance scale.

Tully, R. B. (2015). "Galaxy Groups: A 2MASS Catalog." *Astronomical Journal*, 149, 171. Group catalog used for the richness-based screening criterion applied to the TEP-H0 Cepheid host sample (Step 03).

Jensen, J. B., Blakeslee, J. P., Ma, C., et al. (2015). "The Carnegie-Chicago Hubble Program. III. The Calibration of the Tip of the Red Giant Branch and the Surface Brightness Fluctuation Distance Scales in the Near-Infrared." *Astrophysical Journal*, 808, 91. WFC3/IR SBF calibration distances used as an intermediate step in the Garnavich et al. (2023) SBF $H_0$ determination.

Tonry, J. L., Dressler, A., Blakeslee, J. P., et al. (2000). "The SBF Survey of Galaxy Distances. IV. SBF Distances, Velocity Distances, and Hubble Constants for 300 Galaxies." *Astrophysical Journal*, 530, 625. Establishment of the SBF–Cepheid zero-point calibration using six spiral galaxies with both SBF and Cepheid distance measurements.

Blakeslee, J. P., Ajhar, E. A., & Tonry, J. L. (2002). "The SBF Survey of Galaxy Distances. VI. Calibration of the SBF $I$-band Method and Hubble Constant." *Astrophysical Journal*, 563, 714. Revision of the SBF zero-point calibration by $+0.06$ mag using final HST Key Project Cepheid distances.

## Data Availability and Reproducibility

### Open Science Commitment

This preprint is released under CC and MIT licenses. All materials required to reproduce the analysis—scripts, data references, and the manuscript source—are openly available. Feedback and collaboration are welcome.

### Repository Structure

The complete project is hosted at [https://github.com/matthewsmawfield/TEP-VOID](https://github.com/matthewsmawfield/TEP-VOID) and is structured as follows:

- *site/components/*—HTML source files for each manuscript section. These are the only files that should be edited; all other formats are auto-generated.

- *scripts/steps/*—Reproducible analysis pipeline with 48 registered step scripts organized into six blocks (data ingestion, indicator divergence and void falsification, void boundary test, TEP reconstruction / synthesis, auxiliary TEP supporting tests, and bulk-flow estimator audit / radial discriminators).

- *core/*—Shared TEP framework Python modules (scalar field, conformal scaling, screening, cosmology, constants).

- *scripts/*—Utility scripts including the pipeline runner (`run_pipeline.py`) and PDF generation (`generate_site_pdf.py`).

- *results/*—Generated outputs and figures (populated by running the pipeline).

### Reproducing the Analysis

The full analysis pipeline can be reproduced by running:

```
cd /path/to/TEP-VOID
python3 scripts/run_pipeline.py
```

This executes all 48 registered step scripts in sequence, populating `results/figures/` and `results/outputs/` with fresh data. Individual blocks or steps can be run selectively:

```
python3 scripts/run_pipeline.py --block I      # Indicator divergence only
python3 scripts/run_pipeline.py --step 40       # Single step only
```

The pipeline is fully implemented and all 48 registered steps run successfully against real published data. The pipeline structure, data sources, and analysis methodology are documented in `scripts/README.md`.

### Building the Manuscript

The manuscript site is built from the HTML component files:

```
cd site
npm install
npm run build
```

This generates the static site in `site/dist/` and the markdown version at the repository root (`31-TEP-VOID-v0.2-Valencia.md`). A PDF can be generated from the built site:

```
python3 scripts/generate_site_pdf.py
```

### Revision Notes

The headline $\Delta$AIC values reported in this version ($+101.5$/$+117.1$ at $z \ge 0.05$; $+194.3$/$+328.7$ full sample) differ from earlier preprint versions ($+91.5$/$+106.9$; $+179.4$/$+310.3$). The shift arises from a correction to the covariance submatrix extraction in step_32: the earlier version used an approximate row-index mapping that mismatched a subset of Pantheon+ rows near the $z = 0.05$ boundary. The corrected extraction uses the exact CID-based row mapping from the Pantheon+ covariance matrix, retaining all 1,053 rows in the $z \ge 0.05$ range with the matched $1{,}053 \times 1{,}053$ submatrix. The shift strengthens the rejection; the conclusion is unchanged.

### Data Sources

The analysis draws on the following publicly available datasets:

- *SH0ES Cepheid + SN Ia host sample* (Riess et al. 2022, 2024a, 2024b): 42 local SNe Ia calibrated by Cepheids, with JWST validation from programs GO-1685 and GO-1995.

- *CCHP TRGB and JAGB calibrations* (Freedman et al. 2019, 2025): HST and JWST-based TRGB and JAGB distance measurements in SN Ia hosts.

- *CosmicFlows-4 catalog* (Tully et al. 2023; Watkins et al. 2023): 55,877 galaxy distances and 38,053 group distances/peculiar velocities.

- *Pantheon+ supernova catalog* (Scolnic et al. 2022): 1,543 unique SN Ia distance-redshift measurements after deduplication by CID (raw catalog: 1,701 entries).

- *HyperLEDA and RC3 galaxy parameters*: Rotation velocities, velocity dispersions, and photometric parameters for host galaxy potential characterization.

- *M31 Pan-STARRS Cepheid catalog* (Kodric et al. 2018): 2,686 Cepheid variables in M31.

- *OGLE-IV LMC Cepheid survey* (Soszyński et al. 2015): Fundamental-mode Cepheids in the LMC.

- *HST PHAT (Panchromatic Hubble Andromeda Treasury)*: High-resolution spatial matching for M31 crowding controls.

### Companion Papers

This paper is part of the TEP Research Series. The quantitative Cepheid bias analysis (37-host endpoint likelihood, M31 and LMC differential tests, unified $H_0$ reconstruction) is developed in detail in the companion paper TEP-H0 (Paper 11), which should be consulted for the full statistical methodology and numerical results. The measurement taxonomy and screening regime analysis are developed in TEP-EXP (Paper 9). The JWST high-redshift anomalies are addressed in TEP-JWST (Paper 12).

### Citation

If you use this code or data, please cite:

```
@misc{smawfield2026void,
title        = {Cosmological Voids versus Temporal Shear:
An Empirical Falsification of Kinematic
Hubble Tension Solutions},
author       = {Smawfield, Matthew Lukin},
year         = {2026},
doi          = {10.5281/zenodo.22150139},
url          = {https://doi.org/10.5281/zenodo.22150139},
note         = {Preprint, Version v0.2 (Valencia)}
}
```

### Contact

*Matthew Lukin Smawfield*
Email: matthew@mlsmawfield.com
ORCID: [0009-0003-8219-3159](https://orcid.org/0009-0003-8219-3159)
Website: [https://mlsmawfield.com/tep/void/](https://mlsmawfield.com/tep/void/)

---

*This document was automatically generated from the TEP-VOID research site. For the interactive version with figures and enhanced formatting, visit: https://mlsmawfield.com/tep/void/*

*Related Work:*
- [TEP Theory](https://doi.org/10.5281/zenodo.16921911) (Foundational framework)
- [TEP-GNSS: Distance-Structured Correlations in GNSS Clocks](https://doi.org/10.5281/zenodo.17127229) (Paper 1 — GNSS clock-network test of synchronization holonomy)
- [TEP-GNSS-II: 25-Year Analysis of CODE Precise Clock Products](https://doi.org/10.5281/zenodo.17517141) (Paper 2 — quarter-century GNSS clock correlations)
- [TEP-GNSS-RINEX: Raw RINEX Consistency Test](https://doi.org/10.5281/zenodo.17860166) (Paper 3 — raw RINEX-level consistency validation)
- [TEP-H0: The Cepheid Bias](https://doi.org/10.5281/zenodo.18209702) (Companion paper — quantitative Cepheid bias analysis)
- [TEP-EXP: Precision Tests of GR](https://doi.org/10.5281/zenodo.18109760) (Measurement taxonomy)
- [TEP-JWST: JWST High-Redshift Anomalies](https://doi.org/10.5281/zenodo.19000827) (High-redshift galaxy ages and masses)
- [TEP-HUB: The Mount Wilson Paradigm](https://doi.org/10.5281/zenodo.21954258) (Cosmological redshift as temporal shear)
- [TEP-BBN: Primordial Deuterium](https://doi.org/10.5281/zenodo.21841148) (Deuterium isotope identifiability)

*Source code available at: https://github.com/matthewsmawfield/TEP-VOID*
