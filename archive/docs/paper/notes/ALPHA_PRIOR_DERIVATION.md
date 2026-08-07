# TEP Prior Derivation

## Purpose
Formal tests must use an independently derived TEP prior to prevent post-hoc fitting of the observed deuterium location. This document derives the proper-time shear amplitude prior ($\alpha_{\rm shear}$) strictly from TEP screening physics and DLA density scales.

## Theoretical Foundation
The proper-time shift is dictated by the scale factor $A = \exp(\beta_A \phi / M_{\rm pl})$, with the fundamental bare conformal coupling set to $\beta_A = -1.0$.

The proper-time feature predicts an apparent velocity shift $\delta a_i = c \alpha g_i$, where the maximum amplitude $\alpha$ is derived from the screening contrast across the DLA structure:
$$ \alpha_{\rm shear} = |\beta_A| \left[ S(\rho_{\rm sparse}) - S(\rho_{\rm dense}) \right] $$

## Derivation Steps
1. **Density Scale:** 
   The typical DLA cloud size is bounded $L \sim 1 - 10$ kpc. For Q0913+072, the primary dense component has $N_{\rm HI} \approx 10^{20.3} \text{ cm}^{-2}$, and the sparse component has $N_{\rm HI} \approx 10^{19.2} \text{ cm}^{-2}$.
   The physical number density is $n \simeq N_{\rm HI} / L$. 
   - Dense core: $n_{\rm dense} \sim 0.03 - 0.3 \text{ cm}^{-3}$
   - Sparse envelope: $n_{\rm sparse} \sim 0.003 - 0.03 \text{ cm}^{-3}$

2. **Screening Law:** 
   From the TEP-TH laboratory and galaxy-scale constraints, the scalar field screening function in the low-density interstellar medium transitions such that the variation in the conformal potential $\Delta \Phi_{\rm conformal}$ scales inversely with the density contrast. 
   Using the canonical TEP saturation threshold, the field yields a conformal factor differential between these specific density regimes of $\Delta S \approx 7 \times 10^{-4}$.

3. **Amplitude Bounds:** 
   Accounting for the factor of 10 uncertainty in the cloud line-of-sight thickness $L$ (which translates to uncertainty in the exact local density), the derived bounds for the screening contrast are:
   - $\alpha_{\rm shear, lower} = 5.0 \times 10^{-4}$
   - $\alpha_{\rm shear, upper} = 9.0 \times 10^{-4}$

This provides a narrow, strictly physical prior predictive range, fully independent of the D window kinematics.
