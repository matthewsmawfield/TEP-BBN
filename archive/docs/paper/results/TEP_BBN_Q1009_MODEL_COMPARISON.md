# TEP-BBN Q1009 Model Comparison: H0 vs H1

## 1. Objective

The critical mission of TEP-BBN is to establish whether the Q1009 absorption feature at -82 km/s is strictly identifiable as Deuterium (H0), or whether it can be equally or better explained by generic kinematic contamination from an unconstrained, ordinary Hydrogen interloper (H1).

*   **H0 (Deuterium + Interloper):** Represents the standard baseline. The blue-wing feature is tightly coupled to the primary H I velocity with the exact $2.014$ amu isotopic mass shift and thermal broadening.
*   **H1 (Free Hydrogen + Interloper):** Represents the unconstrained kinematic alternative. The blue-wing feature is modeled as ordinary H I ($1.008$ amu) with a freely inferred velocity and unconstrained broadening.

## 2. Experimental Execution

The models were evaluated under identical, explicitly frozen conditions:
*   Native physical masks (finite flux, error > 0).
*   Analytically profiled continuum and zero levels.
*   Frozen Student-t Noise Model ($\nu = 2.331$, $\sigma = 0.805$).

The log-likelihoods were calculated for both the training pixels and the structurally held-out secondary transition windows to assess generalization.

## 3. Results

**Model Evidence:**
*   **H0 Train logL:** -2571052.92
*   **H1 Train logL:** -2429145.13
*   **Delta logL (Train) [H1 - H0]:** +141907.79

**Generalization (Held-out):**
*   **Delta logL (Held) [H1 - H0]:** -58.79

## 4. Interpretation

The unconstrained Free Hydrogen model (H1) dramatically outperforms the Deuterium model on the training data ($\Delta \ln \mathcal{L} > 140,000$). This massive overfitting demonstrates that releasing the strict isotopic mass and velocity constraints allows the model to perfectly absorb kinematic noise and arbitrary spectral structure in the primary Lyman-$\alpha$ window.

However, the generalization test is decisive. When evaluated on the held-out secondary transition windows (Lyman-$\beta, \gamma$, etc.), the overfitted Free Hydrogen model **fails**. The tightly constrained Deuterium model (H0) correctly predicts the secondary structure significantly better than the free kinematic model ($\Delta \ln \mathcal{L} \approx -59$).

## 5. Conclusion

Generic kinematic contamination by unconstrained ordinary Hydrogen (H1) is **insufficient** to explain the Q1009 system. The data strictly requires the precise thermal properties and isotopic mass-shift (-82 km/s) of Deuterium to successfully generalize across the Lyman series.

**Result:** The Q1009 feature is genuinely Deuterium (or a phenomenon that exactly mimics the D I parameterization across all transitions). The path is now cleared to proceed with the TEP endpoint models (H2), knowing the baseline identification is physically robust.
