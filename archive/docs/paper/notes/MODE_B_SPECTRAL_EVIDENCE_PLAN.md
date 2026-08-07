# Mode B Spectral Evidence Plan

## Purpose
Mode B transitions TEP-BBN from a theoretical feasibility pipeline into an empirical evidence generator. Once Gate -1 identifiability passes, Mode B will apply the independent proper-time feature to real spectra.

## Recommended Path for Q0913+072

**Best Near-Term Strategy:** Use published reduced spectra combined with a VPFIT-style model.

| Path | Recommendation |
| :--- | :--- |
| Published reduced spectra + VPFIT-style model | Best near-term |
| ESO Reflex reduction + custom fitter | Good but slower |
| Current Python reduction | Engineering only, not evidence |

## The Real Milestone
The next milestone is **not** to prove Hoyle right. It is:
**Gate -1 passed for at least one independent feature.**

A valid milestone looks like this:
> "For Q0913+072, a proper-time feature defined before fitting from metal-line/component structure predicts the sign and approximate component location of the D-like absorption. This feature cannot be fully absorbed into ordinary H I velocity blending. Proceed to M0/M1/M2/M3 spectral evidence comparison."

## Implementation Requirements
- Do not use current Python reduction (Step 06) for publication claims.
- The proper-time shear $\delta a_i$ must be fixed or tightly bound by the metal-line structure *before* the M2 (TEP DLA) model is run.
- Compare M2 (TEP DLA) against M3 (H I Interloper) rigorously.
