# TEP Proper-Time Thermodynamics Theorem

This document formally derives the operational relationships between coordinate time, matter proper time, and observable frequencies under the TEP conformal scaling $\tilde{g}_{\mu\nu} = A^2(\phi) g_{\mu\nu}$. 

## 1.1 Action and Frequency Definitions

Matter universally couples to the metric $\tilde{g}_{\mu\nu} = A^2(\phi) g_{\mu\nu}$. Let $t$ be the global coordinate time, and $\tau$ the local matter proper time.

For an observer comoving in the background $g_{\mu\nu}$ with $ds^2 = -c^2 dt^2$:
$$ d\tau^2 = - \frac{d\tilde{s}^2}{c^2} = A^2 dt^2 \implies d\tau = A(\phi) dt $$

Let $\theta$ be the quantum phase of a physical oscillator. We define four distinct operational frequencies:

1.  **Local Matter Frequency ($\omega_{\rm local}$):** 
    The frequency measured using the local matter clock.
    $$ \omega_{\rm local} = - \frac{d\theta}{d\tau} = \omega_0 $$
    This is fixed by local invariant atomic physics.

2.  **Coordinate Frequency ($\omega_t$):**
    The frequency parameterized by the background coordinate time.
    $$ \omega_t = - \frac{d\theta}{dt} = - \frac{d\theta}{d\tau} \frac{d\tau}{dt} = \omega_0 A(\phi) $$
    Because $A \ll 1$ in the early universe, the coordinate rate is small. A local atomic clock is **not** physically "racing" or "fast"; its internal evolution is perfectly ordinary ($\omega_0$), but its coordinate evolution is suppressed.

3.  **Emitter-Measured Photon Frequency ($\omega_{\rm em}$):**
    A photon with wavevector $k^\mu$ is measured by an emitter with four-velocity $u^\mu_{\rm em}$ (where $\tilde{g}_{\mu\nu} u^\mu u^\nu = -c^2 \implies u^t = c/A_{\rm em}$).
    $$ \omega_{\rm em} = - k_\mu u^\mu_{\rm em} = - k_t u^t_{\rm em} = - k_t \frac{c}{A_{\rm em}} $$

4.  **Observer-Measured Photon Frequency ($\omega_{\rm obs}$):**
    The photon propagates along a null geodesic, conserving $k_t$ in a static background. The present-day observer has four-velocity $u^\mu_{\rm obs}$ (with $u^t = c/A_{\rm obs}$).
    $$ \omega_{\rm obs} = - k_\mu u^\mu_{\rm obs} = - k_t \frac{c}{A_{\rm obs}} = \omega_{\rm em} \frac{A_{\rm em}}{A_{\rm obs}} $$
    
**Conclusion:** Frequencies scale structurally as the endpoint ratio $A_{\rm em}/A_{\rm obs}$ without any double-counting of the conformal factor.

## 1.2 Local Dimensionless Invariants

Because all matter strictly couples to the single metric $\tilde{g}_{\mu\nu}$, local dimensionless ratios are perfectly preserved regardless of the value of $A(\phi)$. 

*   $E_{\rm ion} / k_B T_{\rm loc} = \text{invariant}$
*   $Q_{\rm nuc} / k_B T_{\rm loc} = \text{invariant}$
*   $\Delta \nu / \nu = \text{invariant}$

**Theorem:** A universal conformal reparameterization does not alter local dimensionless thermodynamics. A conformal factor alone cannot turn physically cold matter into physically hot matter.

## 1.3 Reaction-Count Invariance vs. Genuine Chronology

The total number of physical reactions $N$ is determined by integrating the local reaction rate $\Gamma_\tau$ over the available proper time:
$$ N = \int \Gamma_\tau d\tau = \int \left( \Gamma_\tau \right) \left( A(\phi) dt \right) $$

**Coordinate Reparameterization:** Changing the clock parameter $A(\phi)$ on a fixed physical worldline segment simply changes the coordinate description ($dt$). It **does not** physically increase the interaction probability $\Gamma_\tau$ or the integrated total $N$. If $\Gamma_\tau$ is exceedingly small (e.g. cold fusion at 2.7K), mere coordinate reparameterization cannot overcome this suppression.

**Genuinely Extended Proper Time:** However, if the TEP cosmology provides an asymptotically extended or geodesically complete past, the actual total integral bounds for $d\tau$ may be vastly larger than in standard cosmology. An eternal chronology could theoretically permit finite reaction yields even with extremely small $\Gamma_\tau$, but this represents a genuinely extended physical history, not a "fast clock" mechanism.

## Phase 1 Verdict

A universal conformal clock parameterization does not create heat or enhance nuclear reactions over the same physical proper-time interval. The simple coordinate-scaling mechanism for explaining primordial high energies is falsified.

However, this does not reject all non-hot, eternal, or steady-state TEP cosmologies that rely on genuinely extended proper-time chronologies.

**Verdict:**
```text
CLOCK_RESCALING_RESOLVED_VIA_GCE
UNDER_CURRENT_TEP_CLOCK_MAP
```

*Note: Broader non-hot cosmological alternatives, including eternal chronologies or steady-state scenarios, are formally deferred to the separate **TEP-NTH** project so they do not delay the core TEP-BBN deuterium identifiability results.*
