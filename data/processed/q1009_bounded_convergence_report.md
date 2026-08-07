# Bounded Convergence Audit Report

**Status:** `NESTED_SAMPLER_NOT_QUALIFIED`

The 3x3x3 bounded convergence audit (`data_seeds`={1001, 1008, 1002}, `nlive`={100, 300, 600}, `sampler_seeds`={50001, 50002, 50003}) has completed under the frozen configuration (`96c9b56`).

## Results Summary

The nested sampler failed to achieve computational convergence for all three `nlive` settings across the three datasets.

### `nlive=100`
- **Likelihood Closure:** FAILED. Found `max_logL` values between -1453.5 and 397.8, while the injected true likelihoods were ~1300. The sampler completely missed the dominant likelihood peak.
- **Classification Stability:** FAILED. Every dataset yielded both `TEP_POSITIVE` and `REAL_NEGATIVE` classifications depending solely on the sampler seed.
- **Evidence Stability:** FAILED. Variations in $\Delta\log Z$ exceeded 3000 units.

### `nlive=300`
- **Likelihood Closure:** FAILED. `max_logL` ranged from -1119.6 to 530.1.
- **Classification Stability:** FAILED for seeds 1008 and 1002.
- **Evidence Stability:** FAILED. $\Delta\log Z$ still fluctuated by over 2000 units across sampler seeds.

### `nlive=600`
- **Likelihood Closure:** FAILED. `max_logL` ranged from -351.3 to 109.1.
- **Classification Stability:** FAILED for all three datasets.
- **Evidence Stability:** FAILED. $\Delta\log Z$ fluctuated by 1000–1700 units.

## Conclusion

The evidence integration is entirely driven by sampler stochasticity rather than the data. The dimensionality of the joint continuum model (16 parameters with local background terms) causes catastrophic sampler starvation for the standard `dynesty` slice sampler, even at `nlive=600`.

As prespecified, the pipeline stops here. The `nlive` parameter will not be escalated informally. Further scientific redesign (e.g., analytically profiling continuum coefficients or deploying a different sampler algorithm) is required before a formal campaign can commence.
