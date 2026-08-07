# TEP-BBN First-Principles Observable Note

## 1. The Foundational Action and Metric
In the Temporal Equivalence Principle (TEP) framework, all standard model fields (including atomic matter and electromagnetic fields) couple to the causal matter metric $\tilde{g}_{\mu\nu}$, which is related to the gravitational metric $g_{\mu\nu}$ via the disformal transformation:
$$ \tilde{g}_{\mu\nu} = A^2(\phi) g_{\mu\nu} + B(\phi) \nabla_\mu \phi \nabla_\nu \phi $$
where $\phi$ is the dynamical scalar temporal field, $A(\phi)$ is the conformal coupling, and $B(\phi)$ is the disformal coupling.

## 2. Absorption Resonance
An absorption line is formed when an incoming photon satisfies the local atomic resonance condition in the absorber's rest frame:
$$ -k_\mu u^\mu_{\rm abs} = \omega_{\rm HI} $$
where $k_\mu$ is the photon four-momentum, $u^\mu_{\rm abs}$ is the absorber's four-velocity in the effective matter metric, and $\omega_{\rm HI}$ is the locally measured invariant atomic transition frequency.

The observer ultimately measures an observed frequency:
$$ \omega_{\rm obs} = -k_\mu u^\mu_{\rm obs} $$

## 3. Pure Static Conformal Limit
Consider the special case of a static, purely conformal matter metric ($B=0$ and $\partial_t \tilde{g}_{\mu\nu} = 0$):
$$ d\tilde{s}^2 = -A^2(\mathbf{x}) dt^2 + A^2(\mathbf{x}) d\mathbf{x}^2 $$
Because this effective photon metric possesses a timelike Killing symmetry ($\partial_t$), Noether's theorem guarantees that the associated Killing energy is exactly conserved along the photon's null geodesic:
$$ E = -k_t = \text{constant} $$
A static local observer (or absorber) with four-velocity $u^\mu = (1/A, \vec{0})$ measures a local frequency:
$$ \omega_{\rm local} = -k_\mu u^\mu = \frac{E}{A} $$
The local absorption resonance condition at component $i$ is therefore:
$$ E_i = A_i \omega_{\rm HI} $$
This dictates that a photon capable of being absorbed by component $i$ must have a conserved Killing energy $E_i = A_i \omega_{\rm HI}$.

When that specific photon reaches the observer, its measured frequency is:
$$ \omega_{{\rm obs}, i} = \frac{E_i}{A_{\rm obs}} = \frac{A_i}{A_{\rm obs}} \omega_{\rm HI} $$

For two distinct absorber components (1 and 2), the ratio of their observed frequencies is:
$$ \frac{\omega_{{\rm obs}, 2}}{\omega_{{\rm obs}, 1}} = \frac{A_2}{A_1} $$

## 4. General Disformal Observability
The conservation of $k_t$ strictly requires a timelike Killing symmetry of the effective metric governing photon propagation. In the general case:
$$ \tilde{g}_{\mu\nu} = A^2 g_{\mu\nu} + B \nabla_\mu \phi \nabla_\nu \phi $$
If the field gradient $\nabla_\mu \phi$ is time-dependent, or if the spatial orientation of the gradient breaks the symmetry, $k_t$ need not be conserved. Even for a stationary disformal metric, the local lapse and null cone structure depend on $B(\phi)$. The observable ratio may instead involve an effective lapse $N_{\rm eff}(A, B, \nabla \phi)$. The exact observability in the general disformal case remains open and requires a separate derivation using the effective photon Hamiltonian.

## 5. Sign Convention and Identifiability
In the static conformal derivation:
$$ \omega_{\rm obs} \propto A_{\rm abs} \quad \text{and} \quad \lambda_{\rm obs} \propto A_{\rm abs}^{-1} $$
Therefore, for a secondary hydrogen component to appear blueward (higher frequency, shorter wavelength) of the primary component, we require $A_{\rm secondary} > A_{\rm primary}$.
To mimic the deuterium isotope displacement:
$$ \frac{\Delta \lambda}{\lambda} \simeq -\frac{81.6}{299,792} \simeq -2.72 \times 10^{-4} $$
This corresponds to a positive difference in the logarithmic clock rate:
$$ \Delta \ln A = \ln \left( \frac{A_{\rm secondary}}{A_{\rm primary}} \right) \simeq +2.72 \times 10^{-4} $$
This relation introduces a fundamental degeneracy with ordinary kinematics:
$$ \Delta v_{\rm obs} = \Delta v_{\rm kin} - c \Delta \ln A $$

### Verdicts
**`OBSERVABLE_FROM_CONFORMAL_ENDPOINT_RATIO`** (CONDITIONAL ON A STATIONARY PURE-CONFORMAL MATTER-FRAME LIMIT)
**`GENERAL DISFORMAL/TIME-DEPENDENT OBSERVABLE: NOT YET DERIVED`**
