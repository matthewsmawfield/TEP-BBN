# Current Pipeline Status

Phase 4A+ remains failed under BIC because exact-D M3 produces false TEP wins above threshold. This is not interpreted as evidence against TEP; it is interpreted as a model-selection and degeneracy diagnostic. Phase 4A++ nested validation is now the formal gate. No Phase 4B-1 real-data evidence claim is allowed until nested evidence bounds the exact-D false TEP rate below 0.05 at 95% confidence.

## Alpha Prior History Clean-up

The earlier `[0.00068, 0.00078]` range was diagnostic and is superseded. The formal validation prior is `[0.0005, 0.0009]`, derived without D-window leakage and frozen before nested validation.

## Procedural Mismatch Notice
Important procedural note: the currently running `step_13c` nested validation evaluates the replacement-M2 implementation that was active at code freeze. A later documentation update defined M2 as a conserved-budget mixture model. Therefore this run is diagnostic unless the model-definition document is reverted to replacement-M2 or the code is rerun under the locked addition/mixed-M2 definition.
