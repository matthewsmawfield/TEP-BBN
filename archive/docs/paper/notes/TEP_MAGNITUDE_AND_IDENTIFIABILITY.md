# TEP Magnitude and Identifiability Gate

## 1. Required Observable Magnitude
As derived in the TEP-BBN Observable Note, reconstructing the $-81.6$ km/s displacement of deuterium as temporally shifted ordinary hydrogen requires a precise differential clock factor between the primary core and the sparse envelope:
$$ |\Delta \ln A| \simeq 2.72 \times 10^{-4} $$

## 2. Derivation from the Foundational Action
The static field equation for the temporal scalar $\phi$ follows from the variation of the total action (Einstein-Hilbert + Scalar + Matter):
$$ \nabla^2 \phi = \frac{dV(\phi)}{d\phi} + \rho \frac{dA(\phi)}{d\phi} $$
We parameterize the conformal coupling as $\ln A(\phi) = \frac{\beta}{M_{\rm pl}} \phi$.
The field minimizes the effective potential $V_{\rm eff}(\phi) = V(\phi) + \rho A(\phi)$.

## 3. Propagation of Local Q1009 LLS Properties
Q1009+2956 is a Lyman-Limit System (LLS). The primary H I component has column density $\log N_{\rm HI} \approx 17.36$.
Because the line-of-sight path length $L$ is physically unresolved, we evaluate the density $n = N_{\rm HI} / L$ over a plausible bracket:
* $L = 0.01$ kpc $\implies n \approx 2.3 \text{ cm}^{-3}$
* $L = 1.0$ kpc $\implies n \approx 0.023 \text{ cm}^{-3}$
* $L = 30.0$ kpc $\implies n \approx 0.0008 \text{ cm}^{-3}$

The local Newtonian potential difference across this structure is roughly:
$$ \Delta \Phi_N \sim G \mu m_p N_{\rm HI} L $$
For $L = 1$ kpc, the dimensionless gravitational potential is microscopically small: $\frac{\Delta \Phi_N}{c^2} \sim 3 \times 10^{-14}$.

## 4. Evaluation of the Linear Weak-Field Closure
If the field linearly tracks the local matter density without undergoing a nonlinear phase transition (a standard weak-field chameleon response), the field excursion is bounded by the Newtonian potential:
$$ \Delta \ln A \approx 2 \beta^2 \frac{\Delta \Phi_N}{c^2} $$
Even if we saturate the local bounds with a massive bare coupling $\beta \sim 10$, the resulting shift is $\Delta \ln A \sim 10^{-12}$.
**This is approximately eight orders of magnitude too small to generate the required $2.72 \times 10^{-4}$ shift.**

## 5. Requirement for Nonlinear Closure
The failure of the linear weak-field tracking means the required displacement must originate from a nonlinear absorber mechanism (such as spontaneous symmetry breaking, kinetic screening, disformal transport, or non-exact covariance transport). 

If the effect arises from a saturated discrete temporal phase transition (where the field shifts between discrete vacua), the conformal jump is dictated strictly by the cosmological vacuum expectation value rather than the local absorber mass. 

This leads to a conditional prediction:
> If the effect arises from a saturated discrete temporal phase transition, inferred non-kinematic offsets may cluster around one or more preferred values, rather than varying continuously with local Newtonian potential.

### Verdict
**`MAGNITUDE_NOT_DERIVABLE_FROM_CURRENT_CLOSURE`**

The ordinary weak-field, locally sourced conformal response does not generate the required phantom-deuterium displacement. The required amplitude relies on a nonlinear closure mechanism that must be independently derived and specified.
