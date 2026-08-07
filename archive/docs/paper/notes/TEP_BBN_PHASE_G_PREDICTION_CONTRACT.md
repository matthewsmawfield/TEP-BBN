# Sealed Phase G Prediction Contract

This document seals the executable TEP prediction rule derived strictly on Development systems (Q1009 and Q0913), before any candidate candidate-window exposure.

## 1. Status and Level
**Status:** `TEP_PREDICTION_RULE_DERIVED`
**Prediction Level:** `LEVEL 2` (Component association, sign, null/non-null status, cross-system ranking)
**Rule Class:** `DEVELOPMENT_CALIBRATED_TEP_RULE`

## 2. The Prediction Rule

The executable function (implemented in `scripts/steps/step_22_phase_g1_derivation.py`) evaluates sealed, permitted non-D input manifests (`measured_feature_vector_{sys_id}.json`) and applies the following rule:

* **Rule A (Component & Null Status):** The component with the highest documented environmental proxy score (`g_i`) is designated as the target. If the maximum `g_i` is extremely low (`< 0.01`), the system is flagged as explicitly NULL.
* **Rule B (Sign & Ranking):** The TEP effect uniformly produces a `BLUEWARD` apparent velocity shift. Systems are ranked continuously by their maximum `g_i` score to predict the relative magnitude of the TEP displacement.
* **Rule C (Velocity Distribution):** Omitted. At Level 2, an absolute velocity prior distribution is not robustly derivable.

## 3. Permitted Inputs
The rule reads exclusively from `measured_feature_vector_{sys_id}.json`. Candidate-window masking ensures that no velocity kinematics in the D-sensitive region influence the prediction.

## 4. Hash Fingerprints
**Prediction Implementation:** `scripts/steps/step_22_phase_g1_derivation.py`
**System Roles Hash:** `phase_g_system_roles.json` (Commit: `pre-phase-g-freeze`)
**Prediction Output File:** `data/processed/phase_g_dev_predictions.json`

## 5. Execution Mandate
With this contract sealed, the pipeline must process all assigned Retrospective and Untouched Confirmation systems through the exact same script without modification, securely logging their independent prediction hashes prior to candidate-window unblinding.
