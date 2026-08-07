# TEP-BBN Formal Model Definitions

To ensure strict testing of the standard primordial deuterium hypothesis against the Temporal Equivalence Principle (TEP), the data models (M0, M1, M2, M3, Mnull) are mathematically locked. 

The goal of TEP-BBN is to test whether the standard primordial deuterium interpretation is invariant under absorber-scale proper-time shear. Therefore, the physical models are constructed to directly pit standard D/H against the TEP proper-time shift field, without granting either model undue parametric freedom.

---

## The Target Observable

All models attempt to fit regions of interest containing apparent neutral Deuterium (D I) Lyman absorption. The models describe the observed flux $F(v)$ via:

$$ F(v) = \left( \sum_{k=0}^2 c_k \cdot x^k \right) \times \exp\left(-\tau(v)\right) $$

where $c_k$ defines a shared quadratic continuum, and the optical depth $\tau(v)$ is computed as the sum of Voigt profiles representing standard hydrogen (H I) components plus whichever extra absorption structure (D I, TEP shifted H I, or interlopers) the model specifies.

### Shared Nuisance Structure
All models share identical nuisance flexibility:
- **Continuum:** 3 parameters ($c_0, c_1, c_2$).
- **Instrumental/Wavelength:** Global velocity zero-point shift ($v_{shift}$) and global LSF scaling ($lsf_{scale}$).
- **Primary H I Components:** Frozen velocity ($v_i$), column density ($N_i$), and physical alignment strengths ($g_i$), except where explicitly modulated.

---

## Model Hierarchy

### M0: Standard Primordial D/H
**Role:** The standard cosmological baseline.
**Physical meaning:** Primordial deuterium is present at a single, globally constant abundance ratio D/H across all kinematic components. No TEP proper-time shear is active.
**Parameters:** $\text{D\_to\_H}$ (free).
**Optical Depth Addition:** 
For each main H I component $i$:
$$ v_{d,i} = v_{i} - 82.0 \text{ km/s} $$
$$ N_{d,i} = N_{i} \times \text{D\_to\_H} $$

### M1: TEP Replacement (The "Kill" Model)
**Role:** The clean discovery model.
**Physical meaning:** No primordial deuterium exists. The absorption structure historically identified as D I is exclusively ordinary H I shifted by TEP proper-time shear $\alpha$.
**Parameters:** $\alpha$ (free, but strictly constrained by prior).
**Optical Depth Addition:**
For each main H I component $i$:
$$ v_{d,i} = v_i - 82.0 \text{ km/s} + c \cdot \alpha \cdot (g_i - g_{primary}) $$
$$ N_{d,i} = N_i \times 2.5\times 10^{-5} $$
*(Note: $N_{d,i}$ is hard-fixed to the expected strength of the shifted component to remove abundance-fitting degrees of freedom, preventing the model from acting as a garbage collector).*

### M2: Mixed Contamination (Conserved Absorption-Budget Mixture)
**Role:** Transition/contamination model.
**Physical meaning:** Real primordial deuterium exists alongside TEP phantom lines, but their combined absorption is constrained by a conserved optical-depth budget. This prevents M2 from simply adding unphysical amounts of extra absorption to win over simpler models.
**Parameters:** $f_D$ (mixing fraction, free $0 \le f_D \le 1$), $\alpha$ (free, strictly constrained by prior).
**Optical Depth Addition:**
M2 is a mixture model where the total additional optical depth is a linear combination of standard D and TEP phantom structure:
$$ \tau_{total} = f_D \cdot \tau_D + (1 - f_D) \cdot \tau_{TEP} $$
where:
1. $\tau_D$ is generated at $v_{d,i} = v_i - 82.0 \text{ km/s}$, with nominal $N_{d,i} = N_i \times 2.5\times 10^{-5}$
2. $\tau_{TEP}$ is generated at $v_{p,i} = v_i - 82.0 \text{ km/s} + c \cdot \alpha \cdot (g_i - g_{primary})$, with nominal $N_{p,i} = N_i \times 2.5\times 10^{-5}$

*(If $f_D \approx 1$, standard D/H survives. If $f_D \approx 0$, TEP completely replaces D. Intermediate values indicate a contaminated D/H inference.)*

### M3: Ordinary H I Interloper
**Role:** The core adversarial control model.
**Physical meaning:** No primordial deuterium exists. The apparent D I structure is merely an unrelated foreground or background ordinary hydrogen cloud coincidentally landing near the expected isotope shift.
**Parameters:** $v_{int}, N_{int}, b_{int}$ (all free).
**Optical Depth Addition:**
A single extra H I Voigt profile:
$$ \tau_{int} = N_{int} \cdot \Phi(v - v_{int}, b_{int}) $$

### Mnull: Continuum Control
**Role:** Detection baseline.
**Physical meaning:** No absorption exists at the expected D location; only continuum noise.
**Parameters:** None (beyond shared nuisances).
**Optical Depth Addition:** None.

---

## Forbidden Assumptions
To ensure the deuterium pillar is subjected to an honest invariance test, the following practices are explicitly forbidden:
1. Treating D/H literature values as direct observations.
2. Assuming all absorber components share one global clock frame.
3. Assuming the isotope shift is the only possible source of -82 km/s structure.
4. Fixing continuum from a standard D/H fit without re-marginalizing.
5. Using VPFIT component choices that already presuppose D.
6. Treating H I interlopers as secondary or weak by default.
7. Allowing TEP parameters to be fitted after unblinding the D window.
8. Treating one-system success as cosmological proof.
