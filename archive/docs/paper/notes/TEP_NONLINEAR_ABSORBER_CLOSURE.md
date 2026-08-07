# TEP Nonlinear Absorber Closure Candidate Protocol

Any candidate nonlinear closure proposed to generate the required phantom-deuterium displacement must formally satisfy this evaluation protocol before being integrated into the TEP-BBN observable framework. The closure must not simply tune a vacuum jump to $2.72 \times 10^{-4}$ manually; the amplitude must arise from independently constrained parameters or be reported as a rigid predictive parameter.

## Candidate Closure Mechanisms
Potential mechanisms include, but are not limited to:
* Symmetry-breaking phase transitions (e.g., Symmetron)
* Kinetic screening
* Domain-wall solutions
* Disformal transitions
* Non-exact covariance transport

## A. The Action
Specify the complete candidate action, including:
1. The conformal coupling $A(\phi)$
2. The disformal coupling $B(\phi)$
3. The potential $V(\phi)$
4. Kinetic terms

## B. The Field Equation
Derive the static or quasi-static absorber equation governing the field $\phi$ within the effective density environment:
$$ \mathcal{E}_\phi[\phi; \rho, \nabla\rho, \text{boundary data}] = 0 $$

## C. Q1009 Solution Family
Solve the field equation across the explicit Q1009 Lyman-Limit System physical brackets ($L \in [0.01, 30]$ kpc, $\log N_{\rm HI} \approx 17.36$).
Calculate the total resulting shift:
$$ \Delta \ln A $$
*(Note: Do not merely calculate the local gradient $\nabla \ln A$ without integrating across the geometric boundary).*

## D. Required Properties
A successful closure must simultaneously satisfy:
* Amplitude constraint: $|\Delta \ln A| \sim 2.72 \times 10^{-4}$
* Stable field solution
* No uncontrolled fifth force (must evade all relevant bounds)
* Consistency with Solar System screening constraints
* Reasonable physical transition width relative to the absorber geometry
* Reasonable probability of naturally producing the observed component configuration
* No predicted (but unobserved) much larger shifts elsewhere in typical spectra
* Compatibility with all other active TEP sectors
