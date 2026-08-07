#!/bin/bash
# TEP-BBN Cleanup and Implementation Script
# This script removes TEP-TH artifacts and completes the TEP-BBN implementation

set -e  # Exit on error

echo "=========================================="
echo "TEP-BBN Cleanup and Implementation"
echo "=========================================="
echo ""

cd "/Users/matthewsmawfield/www/Temporal Equivalence Principle/TEP-BBN"

echo "Step 1: Removing TEP-TH step files..."
cd scripts/steps
rm -f step_00_temporal_horizon_mapping.py
rm -f step_01_matter_frame_curvature.py
rm -f step_02_geodesic_completeness.py
rm -f step_03_effective_stress_energy.py
rm -f step_04_full_bbn_abundances.py
rm -f step_05_recombination_visibility.py
rm -f step_06_cmb_blackbody_origin.py
rm -f step_07_entropy_arrow.py
rm -f step_08_primordial_perturbation_boundary.py
rm -f step_09_temporal_horizon_claim_gate.py
rm -f step_09b_native_tensor_integration.py
rm -f th_common.py
echo "✓ TEP-TH step files removed"
echo ""

echo "Step 2: Removing TEP-TH manuscript files..."
cd ../..
rm -f 27-TEP-TH-v0.2-Thika.md
rm -f 27-TEP-TH-v0.2-Thika.pdf
rm -f manuscripts/27-TEP-TH-v0.2-Thika.md
rm -f site/public/docs/27-TEP-TH-v0.2-Thika.pdf
echo "✓ TEP-TH manuscript files removed"
echo ""

echo "Step 3: Removing TEP-TH site components..."
cd site/components
rm -f 2_temporal_horizon_mapping.html
rm -f 10_perturbation_boundary.html
rm -f 13_conclusion.html
rm -f 13a_falsifiable_predictions.html
rm -f 15_reproducibility.html
rm -f 15a_parameter_dictionary.html
echo "✓ TEP-TH site components removed"
echo ""

echo "Step 4: Removing TEP-TH utility scripts..."
cd ../../scripts/utils
rm -f check2_audit.py
rm -f full_audit.py
rm -f process_pdf.py
rm -f README_LOGGING.md
rm -f verbose_logger.py
echo "✓ TEP-TH utility scripts removed"
echo ""

echo "Step 5: Removing TEP-TH derivation scripts..."
cd ../derivations
rm -f symbolic_proposition1.py
rm -f radiation_era_consistency.py
echo "✓ TEP-TH derivation scripts removed"
echo ""

echo "Step 6: Removing TEP-TH result files..."
cd ../../results
rm -f step_09_temporal_horizon_claim_gate.json
echo "✓ TEP-TH result files removed"
echo ""

echo "Step 7: Removing test scripts..."
cd ..
rm -f test_gate_0.py
rm -f run_gate_0.py
echo "✓ Test scripts removed"
echo ""

echo "Step 8: Verifying TEP-BBN structure..."
echo "Checking scripts/steps/..."
cd scripts/steps
expected_steps=("step_01_literature_registry.py" "step_02_spectra_download.py" "step_03_atomic_data.py" "step_04_data_ingestion.py" "step_05_data_validation.py" "step_06_gate_0_feasibility.py" "step_07_standard_dh_fit.py" "step_08_h_interloper_fit.py" "step_09_temporal_shear_fit.py" "step_10_hybrid_fit.py" "step_11_nested_sampling.py" "step_12_null_tests.py" "step_13_posterior_checks.py" "step_14_figures_claim_gates.py")
for step in "${expected_steps[@]}"; do
    if [ -f "$step" ]; then
        echo "  ✓ $step"
    else
        echo "  ✗ $step (MISSING)"
    fi
done
echo ""

echo "Step 9: Verifying TEP-BBN utilities..."
cd ../utils
expected_utils=("logger.py" "isotopic_shift.py" "voigt_fitting.py" "dla_analysis.py" "null_tests.py")
for util in "${expected_utils[@]}"; do
    if [ -f "$util" ]; then
        echo "  ✓ $util"
    else
        echo "  ✗ $util (MISSING)"
    fi
done
echo ""

echo "Step 10: Verifying TEP-BBN site components..."
cd ../../site/components
expected_components=("0_abstract.html" "1_introduction.html" "2_spectroscopic_isochrony.html" "3_temporal_shear_formalism.html" "4_voigt_models.html" "5_null_tests.html" "6_bayesian_comparison.html" "7_conclusion.html")
for comp in "${expected_components[@]}"; do
    if [ -f "$comp" ]; then
        echo "  ✓ $comp"
    else
        echo "  ✗ $comp (MISSING)"
    fi
done
echo ""

echo "=========================================="
echo "Cleanup Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Download real FITS files from KOA (see DATA_ACQUISITION_REQUIREMENTS.md)"
echo "2. Download real atomic data from NIST/VALD"
echo "3. Run: python scripts/steps/step_02_spectra_download.py"
echo "4. Run: python scripts/steps/step_03_atomic_data.py"
echo "5. Run: python scripts/steps/step_04_data_ingestion.py"
echo "6. Run: python scripts/steps/step_05_data_validation.py"
echo "7. Proceed to analysis (steps 06-14)"
echo ""
