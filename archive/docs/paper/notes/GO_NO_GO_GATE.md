# Phase 4B-1 Real-Data Evidence: Go / No-Go Gate

The pipeline is currently executing the decisive **Phase 4A++ nested synthetic validation**. Do not proceed to Phase 4B-1 (real-data evidence) until `step_13c_nested_synthetic_adversarial_validation.py` has completed and the results strictly satisfy all of the following conditions.

## Go/No-Go Criteria

**GO to Phase 4B-1 only if:**
1. `M3_exact_D` false TEP upper 95% bound < 0.05.
2. `M0` false TEP upper 95% bound < 0.05.
3. `Mnull` false TEP upper 95% bound < 0.01.
4. No S/N stratum shows a concentrated false-positive cluster.
5. False wins, if any, are not within $\log Z$ numerical uncertainty (i.e. decisive logZ margins).
6. Alpha prior audit passes (frozen, blinded, physically derived).
7. M2 definition is locked and unambiguous as the addition model (Standard D + TEP phantom lines).

*Procedural Rule:* The Go/No-Go gate is valid only when `MODEL_DEFINITIONS_M0_M1_M2_M3.md` and the active code implementation are identical. Any mismatch between written model definitions and code invalidates the formal gate and downgrades the run to diagnostic status.

## If `step_13c` Passes

If the criteria are met, the synthetic adversarial gate has passed. Real-spectrum prototype testing is then admissible.
**Next steps:**
1. Phase 4B-0 diagnostic port → inspect Pettini profile mapping.
2. Prepare Phase 4B-1 real-spectrum likelihood script.

*Note: Even passing this gate constitutes an invariance test, not an immediate declaration of deuterium collapse.*

## If `step_13c` Fails

If the upper bound of the exact-D false TEP rate remains above 0.05, do not proceed to real data. Debug in this exact order:
1. Check M2 definition (ensure it isn't gaining unphysical flexibility).
2. Check M0/M3 exact-D degeneracy metric.
3. Check M3 prior volume penalty (is the interloper prior paying too heavy a penalty?).
4. Check line detectability by S/N.
5. Check whether secondary TEP phantom components are below detectability.
6. Check $\log Z$ uncertainty/tie classification.
7. Check alpha prior derivation and whether it is too broad/narrow for the claimed physics.
