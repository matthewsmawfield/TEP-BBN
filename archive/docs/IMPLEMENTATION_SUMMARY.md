# TEP-BBN Implementation Summary

**Date**: 2026-07-06
**Status**: Phase 1 (Feasibility) and Phase 2 (Protocol) Complete
**Next Phase**: Phase 3 (One-Absorber Prototype) - pending real data

---

## Completed Work

### Phase 1: Gate 0 Magnitude Feasibility Test ✅

**Document**: `notes/gate_0_magnitude_feasibility.md`

**Results**:
- Required ΔlnA: $2.7 \times 10^{-4}$
- Required velocity shift: 82 km/s
- T2 shear model (column-density gradient) produces shear ~10⁻⁴
- **Verdict**: CONTINUE - shear amplitude is in correct order of magnitude

**Conclusion**: The T2 model produces shear amplitudes consistent with the required deuterium isotope shift, justifying proceeding to full spectral fitting.

---

### Phase 2: TEP-BBN Protocol Paper Infrastructure ✅

#### 1. Voigt-Profile Fitting Infrastructure ✅

**File**: `scripts/utils/voigt_fitting.py`

**Models Implemented**:
- **M0**: Standard H I + D I Voigt model (baseline)
- **M1**: H I only + temporal-shear shifted component (phantom D test)
- **M2**: Hybrid: real D/H plus temporal-shear nuisance field (bias test)
- **M3**: H I-only ordinary velocity-interloper model (critical for identifiability)

**Functions**:
- `voigt_profile()`: Compute Voigt profile
- `standard_dh_model()`: M0 implementation
- `temporal_shear_model()`: M1 implementation
- `hybrid_model()`: M2 implementation
- `h_interloper_model()`: M3 implementation
- `multi_component_model()`: Multi-component fitting
- `chi_squared()`: Goodness-of-fit metric
- `reduced_chi_squared()`: Reduced chi-squared

#### 2. TEP Shear Models (T0-T4) ✅

**File**: `scripts/utils/dla_analysis.py`

**Models Implemented**:
- **T0**: No temporal shear (baseline)
- **T1**: Constant shear across absorber
- **T2**: Shear proportional to column-density gradient
- **T3**: Shear tied to gravitational/environmental potential
- **T4**: Multi-component stochastic shear field

**Functions**:
- `shear_model_t0()`: Zero shear field
- `shear_model_t1()`: Constant shear field
- `shear_model_t2()`: Column-density gradient shear
- `shear_model_t3()`: Environmental potential shear
- `shear_model_t4()`: Stochastic shear field
- `column_density_gradient()`: Compute gradients
- `environmental_correlation()`: Test environmental correlations
- `absorber_complexity_metric()`: Complexity metric

#### 3. Pre-Registration Protocol ✅

**Document**: `notes/pre_registration_protocol.md`

**Sections**:
1. System selection criteria (redshift, S/N, instrument, continuum)
2. Model definitions (M0-M3 with full parameter specifications)
3. Priors (all parameters with ranges and justifications)
4. Fitting ranges and convergence criteria
5. Evidence thresholds (ΔlnZ decision rules)
6. Null test protocols (A-E with thresholds)
7. Exclusion rules (system and component)
8. Spectral-only likelihood rule (no BBN priors)
9. Prior-volume discipline (no post-hoc tuning)
10. Data provenance requirements (checksums, versions, logs)
11. Version control (git tags, commit hashes)
12. Pre-registration date and sign-off

**Critical Rules**:
- No BBN priors in main evidence comparison
- ΔlnA priors fixed from Gate 0 before fitting
- Full data provenance tracking required
- Random seeds for reproducibility

#### 4. Null Tests ✅

**File**: `scripts/utils/null_tests.py`

**Tests Implemented**:
- **Test A**: Metal-line coherence (correlation > 0.5 threshold)
- **Test B**: Multi-Lyman consistency (χ² range < 2.0 threshold)
- **Test C**: Environmental correlation (correlation > 0.3 threshold)
- **Test D**: Component asymmetry (asymmetry > 10 km/s threshold)
- **Test E**: Blind injection (80% success rate threshold)

**Functions**:
- `metal_line_coherence()`: Test A implementation
- `multi_lyman_consistency()`: Test B implementation
- `environment_correlation_test()`: Test C implementation
- `component_asymmetry()`: Test D implementation
- `blind_injection()`: Test E implementation

#### 5. Isotopic Shift Formalism ✅

**File**: `scripts/utils/isotopic_shift.py`

**Functions**:
- `temporal_shear_shift()`: Convert ΔlnA to velocity shift
- `deuterium_gate_velocity()`: Return 82 km/s target
- `required_delta_ln_A()`: Return 2.7×10⁻⁴ target
- `isotopic_shift_formula()`: Full formula
- `compare_to_deuterium_gate()`: Compare to target

---

## Pipeline Steps (14 Steps) ✅

**File**: `scripts/run_pipeline.py`

**Steps Implemented**:
1. Literature data registry
2. Spectra data download
3. Atomic data download
4. Data ingestion and standardization
5. Data validation
6. **Gate 0: Magnitude feasibility test** ✅
7. Standard D/H fit (M0)
8. H I interloper fit (M3)
9. Temporal-shear fit (M1)
10. Hybrid fit (M2)
11. Nested sampling evidence comparison
12. Null tests
13. Posterior predictive checks
14. Figure generation and claim-gate analysis

**Status**: All step files created as placeholders with proper structure. Steps 6-14 have model infrastructure ready.

---

## Repository Structure ✅

**Updated Structure**:
```
TEP-BBN/
├── core/                    # Shared physics modules (unchanged)
├── scripts/
│   ├── steps/              # 14 pipeline steps (updated for ISO)
│   ├── utils/              # Updated utilities
│   │   ├── isotopic_shift.py    # ✅ Implemented
│   │   ├── voigt_fitting.py     # ✅ Implemented (M0-M3)
│   │   ├── dla_analysis.py      # ✅ Implemented (T0-T4)
│   │   ├── null_tests.py        # ✅ Implemented (A-E)
│   │   └── logger.py            # ✅ Updated header
│   └── run_pipeline.py     # ✅ Updated for 14-step ISO pipeline
├── data/                   # Data directories (ready)
├── results/                # Results directories (ready)
├── site/                   # Manuscript builder
│   ├── components/         # ✅ Updated for ISO manuscript
│   └── index.html         # ✅ Updated for ISO
├── notes/                  # ✅ New directory
│   ├── gate_0_magnitude_feasibility.md
│   └── pre_registration_protocol.md
├── README.md               # ✅ Updated for ISO
├── VERSION.json            # ✅ Updated for ISO
├── CITATION.cff            # ✅ Updated for ISO
├── requirements.txt        # ✅ Updated for ISO
└── plan                    # ✅ Updated with completed work
```

---

## Key Scientific Decisions ✅

### 1. Identifiability (Gate -1)
- **M3 model** (H I interloper) is critical to distinguish temporal shear from ordinary velocity blending
- Implemented in `voigt_fitting.py`

### 2. Magnitude Feasibility (Gate 0)
- **PASSED**: T2 model produces shear ~10⁻⁴, consistent with required 2.7×10⁻⁴
- Documented in `notes/gate_0_magnitude_feasibility.md`

### 3. Pre-Registration
- **COMPLETED**: Full protocol documented in `notes/pre_registration_protocol.md`
- Prevents after-the-fit tuning
- Ensures reproducibility

### 4. Spectral-Only Likelihood
- **RULE ENFORCED**: No BBN priors in main evidence comparison
- D/H priors must be spectral-only

### 5. Prior-Volume Discipline
- **RULE ENFORCED**: ΔlnA priors fixed from Gate 0 before fitting
- No post-hoc tuning allowed

---

## Next Steps (Phase 3: One-Absorber Prototype)

**Prerequisites**:
1. Select one clean D/H absorber from literature
2. Download high-resolution spectra from public archives
3. Download atomic data from NIST/VALD

**Implementation**:
1. Run steps 01-05 (data download and validation)
2. Run step 06 (Gate 0 - already passed)
3. Run steps 07-10 (M0, M3, M1, M2 fitting)
4. Run step 11 (nested sampling evidence comparison)
5. Run step 12 (null tests)
6. Run step 13 (posterior predictive checks)
7. Run step 14 (figure generation)

**Decision Gate**:
- If M0 decisively wins: non-Gamow branch weakens
- If M2 improves fit: continue to multi-system
- If M1 wins: major result (phantom D supported)
- If M3 beats M1: temporal shear not distinguished from velocity blending

**Strict Rule**:
> The first absorber result must be treated as a pipeline validation, not a discovery claim.

---

## Phase 4: Multi-Absorber Expansion (Future)

**Only if Phase 3 is not negative**

**Look for**:
- Consistent ΔlnA across systems
- Environmental correlation
- Metal-line coherence
- Residual improvement
- Redshift dependence
- Robustness to priors

**Decision Gate**:
- If consistent signal across systems: non-Gamow branch becomes viable
- If no consistent signal: thermal compatibility branch remains

---

## Phase 5: Hoyle-Compatible TEP (Future)

**Only after TEP-BBN shows signal**

**Paper**: TEP-HY (Hoyle-Compatible Temporal Cosmology)

**Must model**:
- Helium abundance
- Metal abundances
- Gas recycling
- Deuterium destruction
- Local deuterium sources

**Cannot simply say**: "infinite time solves helium"

---

## Current Status

**Phase 1**: ✅ Complete (Gate 0 passed)
**Phase 2**: ✅ Complete (protocol infrastructure ready)
**Phase 3**: ⏳ Pending (requires real data)
**Phase 4**: ⏳ Pending (after Phase 3)
**Phase 5**: ⏳ Pending (after Phase 4)

**Overall Progress**: 40% complete (infrastructure ready, awaiting data)

---

## Critical Success Factors

1. **Gate 0 passed** ✅ - Magnitude feasibility confirmed
2. **M3 model implemented** ✅ - Identifiability addressed
3. **Pre-registration complete** ✅ - Prevents tuning
4. **Null tests ready** ✅ - Physical consistency checks
5. **All models implemented** ✅ - M0-M3, T0-T4

**Remaining**: Real data analysis (Phases 3-5)

---

**Prepared by**: Matthew Lukin Smawfield
**Date**: 2026-07-06
**Status**: Ready for Phase 3 when data becomes available
