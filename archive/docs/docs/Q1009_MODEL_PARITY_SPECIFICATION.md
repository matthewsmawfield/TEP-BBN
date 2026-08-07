# Q1009+2956 Six-Model Parity and Parameter Specification

## 1. Executive Summary

This document specifies the exact component architectures, parameter ties, degrees of freedom, and model-selection complexity rules across the six model hypotheses evaluated in the Q1009+2956 forensic audit.

## 2. Hypothesis Definitions and Parameter Roles

| Model Identifier | Label | Candidate Component Description | Candidate Degrees of Freedom |
| :--- | :--- | :--- | :--- |
| $M_{\mathrm{NULL}}$ | `NO_CANDIDATE_COMPONENT` | No candidate D or replacement H component present. | None (0 parameters) |
| $M_{\mathrm{D6a}}$ | `PUBLISHED_CONVENTIONAL_D_MODEL` | Exact published `model_6a.26` deuterium architecture (3 D components locked to H parent velocity, column ratio, and thermal width). | Frozen literature parameters |
| $M_{\mathrm{Drefit}}$ | `REFITTED_CONVENTIONAL_D_MODEL` | Same published `model_6a` 3-component D architecture, with all shared physical parameters symmetrically re-optimized. | Shared physical baseline |
| $M_{\mathrm{Dfree}}^{(j)}$ | `MATCHED_FLEXIBILITY_SPECTROSCOPIC_D_MODEL` | One candidate physical D component associated with parent H component $j$. Velocity fixed at $v_{\mathrm{parent}} - 81.6\text{ km/s}$. Column density $N_{\mathrm{D}}$ untied and free. Thermal width $b_{\mathrm{D}}^2 = b_{\mathrm{turb}}^2 + k_B T / m_p$. | $N_{\mathrm{D}}, T, b_{\mathrm{turb}}$ (3 parameters) |
| $M_{\mathrm{H}}$ | `ORDINARY_H_INTERLOPER_MODEL` | One candidate ordinary H component. Velocity $v_{\mathrm{H}}$ free over preregistered absorber range. Column density $N_{\mathrm{H}}$ free. Thermal width $b_{\mathrm{H}}^2 = b_{\mathrm{turb}}^2 + 2 k_B T / m_p$. | $v_{\mathrm{H}}, N_{\mathrm{H}}, T, b_{\mathrm{turb}}$ (4 parameters) |
| $M_{\mathrm{D+H}}^{(j)}$ | `PHYSICAL_D_PLUS_H_INTERLOPER` | Physical candidate D component associated with parent H component $j$, plus an additional ordinary H component. | $N_{\mathrm{D}}, v_{\mathrm{H}}, N_{\mathrm{H}}, T, b_{\mathrm{turb}}$ (5 parameters) |

## 3. Parameter Categorization and AIC Degree-of-Freedom Accounting

For exact model comparison, parameter counts are strictly partitioned and reported as follows:

- $n_{\mathrm{phys}}$: Explicit physical parameters optimized numerically via L-BFGS-B (line redshifts, column densities, Doppler parameters, turbulent velocities, temperatures).
- $n_{\mathrm{cal}}$: Explicit calibration parameters (wavelength registration offsets, LSF width scaling).
- $n_{\mathrm{cont}}$: Analytically profiled continuum polynomial coefficients.
- $n_{\mathrm{zero}}$: Analytically profiled zero-level offset coefficients.
- $n_{\mathrm{fixed}}$: Parameters held constant at literature values (atomic transition wavelengths, oscillator strengths, damping constants).
- $n_{\mathrm{tied}}$: Parameters constrained by exact linear or physical ties (e.g. metal redshift ties, thermal Doppler relations).
- $n_{\mathrm{total}}$: Total estimated parameters ($n_{\mathrm{phys}} + n_{\mathrm{cal}} + n_{\mathrm{cont}} + n_{\mathrm{zero}}$) used in Information Criteria ($AIC = 2 n_{\mathrm{total}} - 2 \log L$).

## 4. Parent Association Selection and Complexity Penalties

For $M_{\mathrm{Dfree}}^{(j)}$ and $M_{\mathrm{D+H}}^{(j)}$, if multiple candidate parent H components $j \in \{1, 2, \dots, K\}$ are physically plausible:

1. Each candidate parent association is evaluated as an explicit discrete model $M_{\mathrm{Dfree}}^{(j)}$.
2. Post-hoc selection of the best parent association applies a model-selection complexity penalty of $\ln(K)$ log-likelihood units (equivalent to $2 \ln K$ AIC units) to account for discrete search over parent candidates.
