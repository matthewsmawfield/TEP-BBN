# Q1009 Primary Test Specification

This document defines the formal, deterministic primary test intended to resolve whether the Temporal Equivalence Principle (TEP) explains the high-redshift Q1009 absorption structure better than a conventional cosmological model.

## Primary Scientific Hypothesis
The prespecified TEP component geometry explains the Q1009 D-window and its secondary predicted structure better than conventional alternatives.

## Frozen Models

### H0: Conventional Explanation
H0 represents the strongest reasonable conventional model, assuming hot-Big-Bang nucleosynthesis and potential ordinary hydrogen interlopers.
*   **Deuterium**: Included as a freely scaling ordinary deuterium feature.
*   **Contaminants**: Included as conventional H I interloper absorption with physically allowed centroid and width parameters.
*   **Registration**: Subject to a single shared registration shift parameter across the four exposures.
*   **Continuum**: Represented by a locally additive, quadratic function.
*   **Instrumental Resolution**: Frozen to nominal LSF (with pre-registered sensitivity checks).
*   **Constraints**: Metal component positions (C1-C5) and widths derived independently of the D-window are rigidly frozen.

### H1: Primary-only TEP
H1 tests whether the primary TEP phantom effect alone can masquerade as deuterium without the predictive power of secondary structures.
*   **Primary Feature**: Included as the core temporal shift effect at the primary component (alpha, $f_D$).
*   **Secondary Geometry**: Explicitly excluded. No secondary phantom components are simulated.
*   **Nuisance Parameters**: Utilizes the exact same continuum, registration, and resolving-power freedom as H2.

### H2: Full TEP
H2 is the complete TEP prediction.
*   **Primary Feature**: Included.
*   **Secondary Geometry**: Included. The exact three-component geometry derived from non-D metals is enforced.
*   **Constraints**: Relative component positions are rigidly fixed. Relative strengths follow the prespecified TEP strength law.
*   **No Post-hoc Additions**: No additional secondary components may be added to soak up residual variance in the D-window.

## Core Tests and Statistics

The evaluation employs maximum log-likelihood ratios resulting from a strictly deterministic optimization sequence.

1.  **Primary Model Comparison**: 
    $$T_{\mathrm{full}} = 2\left[ \log L(H2) - \log L(H0) \right]$$
    *Tests whether the full TEP geometry possesses strictly greater explanatory power than the conventional framework.*

2.  **Secondary Information Additivity**:
    $$T_{\mathrm{secondary}} = 2\left[ \log L(H2) - \log L(H1) \right]$$
    *Tests whether the secondary geometry independently contributes explanatory power over the primary TEP phantom core.*

3.  **Held-Out Predictive Power**:
    $$S_{\mathrm{held}} = 2\left[ \log L_{\mathrm{held}}(H2) - \max\left(\log L_{\mathrm{held}}(H0), \log L_{\mathrm{held}}(H1)\right) \right]$$
    *Equivalently: $S_{\mathrm{held}} = \min(\chi^2_{\mathrm{held}}(H0), \chi^2_{\mathrm{held}}(H1)) - \chi^2_{\mathrm{held}}(H2)$*
    *Fit is performed strictly on frozen training pixels. The resulting maximum likelihood parameters are used to blindly evaluate the likelihood in held-out secondary windows without refitting.*

## Thresholds and Empirical Calibration
Rather than utilizing nested sampling evidence ($\log Z$) or fragile posterior-standard-deviation edges, the test calibrates statistical significance directly through Monte Carlo simulations.

*   **Calibration Sample**: The threshold $t_{\mathrm{full}}$ for $T_{\mathrm{full}}$ is established via the empirical 99th percentile of 1,000 $H0$-generating (null) simulations.
*   **False Positive Requirement**: $\le 4$ out of $1,000$ null simulations may trigger positive identification across all gates, yielding an empirical $FPR \le 1\%$ (one-sided 95% upper bound).
*   **Recovery Power**: At the central injection $\alpha = 0.0007$, $\ge 90\%$ of trials must be successfully recovered as `TEP_SUPPORTED`.

## Frozen Analysis Constraints
Prior to initiating the calibration phase or unblinding the Q1009 target data, the following elements are rigidly **frozen**:
*   Training pixels
*   Held-out secondary pixels
*   Excluded pixels
*   Masks
*   Velocity reference
*   Parameter bounds
*   Optimization sequence (starting points, grid nodes)
*   Convergence tolerances

## Final Decision Gates
A single execution runs on Q1009, generating one of four discrete categories:

*   `TEP_SUPPORTED`: $T_{\mathrm{full}} \ge t_{\mathrm{full}}$ AND $T_{\mathrm{secondary}} > 0$ AND $S_{\mathrm{held}} > 0$ AND all fits converged AND robust to minor LSF/Registration shifts.
*   `CONVENTIONAL_SUPPORTED`: $H0$ clearly wins, or $H2$ fails to provide the prespecified secondary improvement.
*   `INCONCLUSIVE`: The statistics hover near boundaries, or robustness variations materially alter the categorization.
*   `NUMERICAL_FAILURE`: The deterministic optimizer failed to converge or reached unphysical bounds indicating a pathological surface.
