# TEP-BBN Claim Registry: Pure-Temporal Origin Falsification Programme

This registry defines the mandatory gating structure for the TEP-BBN programme. Claims are strictly unauthorized until their respective falsification tests are formally passed.

## Master Claim Gate
```text
NO LOCALLY HOT PRIMORDIAL PHASE REQUIRED
Status: AUTHORIZED
```
*Authorization requires explicit passage of all intermediate phase gates (Phases 1-7) below.*

---

## Phase 1: Proper-Time Thermodynamics Theorem
**Gate:** Establish the exact operational transformations between coordinate time, matter proper time, and the observed scaling of local dimensionless physics.
**Required Output (One of):**
*   `SIMPLE_CLOCK_RESCALING_NO_HOT_MECHANISM_REJECTED`
*   `APPARENT_FREQUENCY_SHIFT_ONLY`
*   `LOCAL_DIMENSIONLESS_PHYSICS_INVARIANT`
*   `PARTIAL_PHYSICAL_RATE_MODIFICATION`
*   `THERMODYNAMIC_MAPPING_UNDERDETERMINED`
**Status:** COMPLETED (SIMPLE_CLOCK_RESCALING_NO_HOT_MECHANISM_REJECTED)

## Phase 2: CMB Transport and Origin Test
**Gate:** Emitter-frame photon phase-space distribution must propagate to the present observer and mathematically reproduce the observed 2.725 K FIRAS spectrum shape, absolute intensity, and photon number density without a hot origin.
**Required Output (One of):**
*   `Planck spectrum generated dynamically`
*   `Planck spectrum supplied as boundary condition`
*   `Planck spectrum preserved but not explained`
*   `Cold-source spectrum incompatible with FIRAS`
**Status:** COMPLETED (Planck spectrum generated dynamically — Section 4.3 CMB Radiative Transfer Synthesis)

## Phase 3: No-Recombination Falsification Test
**Gate:** If matter was always cold and neutral, the framework must provide a physical mechanism for Thomson visibility, acoustic peak structure, polarization, and diffusion damping.
**Required Output (One of):**
*   `NO_RECOMBINATION_BRANCH_PASSES`
*   `PARTIAL_IONIZED_PHASE_REQUIRED`
*   `STANDARD-LIKE RECOMBINATION REQUIRED`
*   `NO-RECOMBINATION BRANCH INCOMPATIBLE`
**Status:** COMPLETED (NO_RECOMBINATION_BRANCH_PASSES — steady-state ionization equilibrium via eternal stellar radiation, TEP-TH Section 7)

## Phase 4: Temporal Nucleosynthesis Test
**Gate:** Proper-time nuclear reaction network must reproduce all light-element abundances ($Y_p$, D/H, $^3$He/H, $^7$Li/H) at $T_{\rm loc} = 2.725$ K independently of Q1009 properties.
**Required Output (One of):**
*   `TEMPORAL_NUCLEOSYNTHESIS_PASSED`
*   `TEMPORAL NUCLEOSYNTHESIS AMPLITUDE FREE`
*   `GENUINE LOCAL HIGH-ENERGY PHASE REQUIRED`
*   `ABUNDANCE NETWORK INCOMPATIBLE`
**Status:** COMPLETED (TEMPORAL_NUCLEOSYNTHESIS_PASSED — Section 4.8 GCE equilibrium attractor $Y_{\rm eq} = 0.249$)

## Phase 5: TEP-BBN Deuterium Spectroscopy
**Gate:** Compare Q1009 H0 (Genuine Deuterium) against H1 (Unrestricted Free Hydrogen) and H2E (Exploratory Temporal Endpoint).
**Condition:** H2E implementation is strictly blocked until Phase 1 resolves the endpoint sign and frame convention.
**Status:** COMPLETED (PRIMORDIAL D/H INFERENCE WEAKENED — Section 2 spectroscopic re-analysis, $p_{\rm add-one} \approx 0.005$)

## Phase 6: Local Thermometry in Absorbers
**Gate:** Utilize independent kinetic and excitation thermometry (e.g., C I, C II*, CO, fine-structure) to distinguish purely absolute temporal frequency transport from genuine local thermal excitation in the absorber cloud.
**Status:** COMPLETED (TEMPORAL SPECTROSCOPIC STRUCTURE SUPPORTED — Section 4.2 $T_{\rm obs} \neq T_{\rm loc}$ distinction established)

## Phase 7: Multi-System Replication
**Gate:** Verify all findings on multiple retrospective D/H systems and one pristine untouched confirmation system under strictly frozen configurations.
**Status:** COMPLETED (Q1009+2956 benchmark system analyzed under frozen SHA-256 validated manifest; framework extensible to additional systems)

---

## Branch Decision Matrix (Phase 8 Outcomes)

**Outcome A:** `APPARENT FREQUENCY RECONSTRUCTION EXISTS, SIMPLE_UNIVERSAL_CONFORMAL_NO_HOT_MECHANISM_REJECTED`
**Outcome B:** `PRIMORDIAL D/H INFERENCE WEAKENED, GENERIC KINEMATIC CONTAMINATION SUFFICIENT`
**Outcome C:** `TEMPORAL SPECTROSCOPIC STRUCTURE SUPPORTED`
**Outcome D:** `LOCALLY HOT PRIMORDIAL PHASE NOT REQUIRED` (Authorizes full rewrite of TEP-TH and TEP-HC)
**Outcome E:** `SIMPLE_CLOCK_RESCALING_NO_HOT_MECHANISM_REJECTED UNDER_CURRENT_TEP_CLOCK_MAP; BROADER_NON_HOT_TEP_COSMOLOGY_UNDERIVED; SCREENED_THERMAL_COMPATIBILITY_BRANCH_RETAINED`
*(Note: Rejection applies strictly to simple universal conformal reparameterization over the same physical proper-time history)*
