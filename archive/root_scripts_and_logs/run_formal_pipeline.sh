#!/bin/bash
set -e

MANIFEST="data/processed/Q1009+2956_z2.504_HIRES_spectrum_manifest.json"

echo "=== 1. Registration Audit ==="
python scripts/steps/step_20e_q1009_registration_audit.py $MANIFEST

echo "=== 2. Formal Power Campaign ==="
python scripts/steps/step_21_formal_power_campaign.py $MANIFEST

echo "Power campaign completed. Real classification is gated and must be run manually after reviewing the power report."
