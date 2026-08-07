# TEP-BBN Deep Scan Issues and Fixes

**Date**: 2026-07-06
**Status**: Issues identified, fixes documented

---

## Critical Issues Found

### 1. Old TEP-TH Step Files (HIGH PRIORITY)

**Problem**: The scripts/steps/ directory contains old TEP-TH step files that should be removed.

**TEP-TH files to remove**:
- step_00_temporal_horizon_mapping.py
- step_01_matter_frame_curvature.py
- step_02_geodesic_completeness.py
- step_03_effective_stress_energy.py
- step_04_full_bbn_abundances.py
- step_05_recombination_visibility.py
- step_06_cmb_blackbody_origin.py
- step_07_entropy_arrow.py
- step_08_primordial_perturbation_boundary.py
- step_09_temporal_horizon_claim_gate.py
- step_09b_native_tensor_integration.py
- th_common.py

**TEP-BBN files to keep**:
- step_01_literature_registry.py ✅
- step_02_spectra_download.py ✅
- step_03_atomic_data.py ✅
- step_04_data_ingestion.py ✅
- step_05_data_validation.py ✅
- step_06_gate_0_feasibility.py ✅
- step_07_standard_dh_fit.py ✅
- step_08_h_interloper_fit.py ✅
- step_09_temporal_shear_fit.py ✅
- step_10_hybrid_fit.py ✅
- step_11_nested_sampling.py ✅
- step_12_null_tests.py ✅
- step_13_posterior_checks.py ✅
- step_14_figures_claim_gates.py ✅

**Fix**: Remove all TEP-TH step files from scripts/steps/

**Command to run**:
```bash
cd "/Users/matthewsmawfield/www/Temporal Equivalence Principle/TEP-BBN/scripts/steps"
rm step_00_temporal_horizon_mapping.py
rm step_01_matter_frame_curvature.py
rm step_02_geodesic_completeness.py
rm step_03_effective_stress_energy.py
rm step_04_full_bbn_abundances.py
rm step_05_recombination_visibility.py
rm step_06_cmb_blackbody_origin.py
rm step_07_entropy_arrow.py
rm step_08_primordial_perturbation_boundary.py
rm step_09_temporal_horizon_claim_gate.py
rm step_09b_native_tensor_integration.py
rm th_common.py
```

---

### 2. TEP-TH Manuscript Files (HIGH PRIORITY)

**Problem**: TEP-TH manuscript files are in the TEP-BBN repository.

**Files to remove**:
- 27-TEP-TH-v0.2-Thika.md (root)
- 27-TEP-TH-v0.2-Thika.pdf (root)
- manuscripts/27-TEP-TH-v0.2-Thika.md
- site/public/docs/27-TEP-TH-v0.2-Thika.pdf

**Fix**: Remove all TEP-TH manuscript files

**Command to run**:
```bash
cd "/Users/matthewsmawfield/www/Temporal Equivalence Principle/TEP-BBN"
rm 27-TEP-TH-v0.2-Thika.md
rm 27-TEP-TH-v0.2-Thika.pdf
rm manuscripts/27-TEP-TH-v0.2-Thika.md
rm site/public/docs/27-TEP-TH-v0.2-Thika.pdf
```

---

### 3. TEP-TH Site Components (HIGH PRIORITY)

**Problem**: Site components contain TEP-TH content that should be removed.

**TEP-TH components to remove**:
- site/components/2_temporal_horizon_mapping.html
- site/components/10_perturbation_boundary.html
- site/components/13_conclusion.html
- site/components/13a_falsifiable_predictions.html
- site/components/15_reproducibility.html
- site/components/15a_parameter_dictionary.html

**TEP-BBN components to keep**:
- site/components/0_abstract.html ✅
- site/components/1_introduction.html ✅
- site/components/2_spectroscopic_isochrony.html ✅
- site/components/3_temporal_shear_formalism.html ✅
- site/components/4_voigt_models.html ✅
- site/components/5_null_tests.html ✅
- site/components/6_bayesian_comparison.html ✅
- site/components/7_conclusion.html ✅

**Fix**: Remove TEP-TH site components

**Command to run**:
```bash
cd "/Users/matthewsmawfield/www/Temporal Equivalence Principle/TEP-BBN/site/components"
rm 2_temporal_horizon_mapping.html
rm 10_perturbation_boundary.html
rm 13_conclusion.html
rm 13a_falsifiable_predictions.html
rm 15_reproducibility.html
rm 15a_parameter_dictionary.html
```

---

### 4. TEP-TH Utility Scripts (MEDIUM PRIORITY)

**Problem**: Scripts/utils/ contains TEP-TH specific utilities.

**Files to remove**:
- scripts/utils/check2_audit.py
- scripts/utils/full_audit.py
- scripts/utils/process_pdf.py
- scripts/utils/README_LOGGING.md
- scripts/utils/verbose_logger.py

**TEP-BBN utilities to keep**:
- scripts/utils/logger.py ✅
- scripts/utils/isotopic_shift.py ✅
- scripts/utils/voigt_fitting.py ✅
- scripts/utils/dla_analysis.py ✅
- scripts/utils/null_tests.py ✅

**Fix**: Remove TEP-TH utility scripts

**Command to run**:
```bash
cd "/Users/matthewsmawfield/www/Temporal Equivalence Principle/TEP-BBN/scripts/utils"
rm check2_audit.py
rm full_audit.py
rm process_pdf.py
rm README_LOGGING.md
rm verbose_logger.py
```

---

### 5. TEP-TH Derivation Scripts (MEDIUM PRIORITY)

**Problem**: Scripts/derivations/ contains TEP-TH specific derivations.

**Files to remove**:
- scripts/derivations/symbolic_proposition1.py
- scripts/derivations/radiation_era_consistency.py

**Fix**: Remove TEP-TH derivation scripts

**Command to run**:
```bash
cd "/Users/matthewsmawfield/www/Temporal Equivalence Principle/TEP-BBN/scripts/derivations"
rm symbolic_proposition1.py
rm radiation_era_consistency.py
```

---

### 6. TEP-TH Results Files (MEDIUM PRIORITY)

**Problem**: Results/ contains TEP-TH specific output files.

**Files to remove**:
- results/step_09_temporal_horizon_claim_gate.json

**Fix**: Remove TEP-TH result files

**Command to run**:
```bash
cd "/Users/matthewsmawfield/www/Temporal Equivalence Principle/TEP-BBN/results"
rm step_09_temporal_horizon_claim_gate.json
```

---

### 7. TEP-TH Site Configuration (LOW PRIORITY)

**Problem**: Site configuration files reference TEP-TH.

**Files to check**:
- site/package.json (references TEP-TH)
- site/styles.css (references TEP-TH)
- site/build.js (references TEP-TH)
- site/dev-server.js (references TEP-TH)
- site/html-to-markdown.js (references TEP-TH)
- site/public/sitemap.xml (references TEP-TH)
- site/public/robots.txt (references TEP-TH)

**Fix**: Update site configuration for TEP-BBN

---

### 8. TEP-TH Reference in README (LOW PRIORITY)

**Problem**: README.md contains TEP-TH references.

**Fix**: Update README.md to reference TEP-BBN only

---

### 9. TEP-TH Reference in plan (ACCEPTABLE)

**Problem**: plan file contains TEP-TH references in strategic context.

**Status**: This is acceptable - the plan discusses the relationship between TEP-TH and TEP-BBN.

**Fix**: No action needed

---

### 10. TEP-TH Manuscripts in manuscripts/ (ACCEPTABLE)

**Problem**: manuscripts/ contains TEP-C0 and TEP-HC manuscripts.

**Status**: These are reference papers for the TEP series, acceptable to keep.

**Fix**: No action needed

---

## Summary of Required Actions

### High Priority (Must Fix)
1. Remove 11 TEP-TH step files from scripts/steps/
2. Remove 4 TEP-TH manuscript files
3. Remove 6 TEP-TH site components

### Medium Priority (Should Fix)
4. Remove 5 TEP-TH utility scripts
5. Remove 2 TEP-TH derivation scripts
6. Remove 1 TEP-TH result file

### Low Priority (Can Fix)
7. Update site configuration files
8. Update README.md references

### Acceptable (No Action Needed)
9. TEP-TH references in plan (strategic context)
10. TEP-C0 and TEP-HC manuscripts (reference papers)

---

## Verification Checklist

After fixes, verify:

- [ ] scripts/steps/ contains only 14 TEP-BBN step files
- [ ] No TEP-TH manuscript files in root or manuscripts/
- [ ] site/components/ contains only 8 TEP-BBN components
- [ ] scripts/utils/ contains only 5 TEP-BBN utilities
- [ ] No TEP-TH derivation scripts
- [ ] No TEP-TH result files
- [ ] README.md references TEP-BBN only
- [ ] Site configuration updated for TEP-BBN

---

## Current Status

**Issues Found**: 10 categories
**High Priority**: 3 categories (21 files)
**Medium Priority**: 3 categories (8 files)
**Low Priority**: 2 categories (configuration)
**Acceptable**: 2 categories (strategic references)

**Overall Assessment**: Repository needs cleanup to remove TEP-TH artifacts before proceeding with TEP-BBN analysis.

---

**Prepared by**: Matthew Lukin Smawfield
**Date**: 2026-07-06
**Status**: Issues identified, fixes documented
