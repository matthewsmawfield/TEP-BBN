# Mode A Results Summary

## Verdict
Mode A is structurally sound and complete. The pipeline computes the required proper-time coupling for Q0913+072 to mimic the observed D/H isotope shift ($\Delta \ln A = 2.735 \times 10^{-4}$). 

**Crucially, the pipeline correctly blocks any claims against primordial deuterium at this stage.** 
Because an unconstrained proper-time shift ($\delta a_i$) is mathematically degenerate with an ordinary kinematic velocity shift ($v_{{\rm kin},i}$), Mode A results are labeled `literature_feasibility` and `toy_only`, with `claim_allowed: False`.

## What This Result Means
A TEP proper-time explanation of the D/H offset is not obviously impossible at the level of required amplitude (especially under compact-cloud toy assumptions). However, because the proper-time term remains degenerate with ordinary velocity structure without an independent predictor, the result is not evidence against primordial deuterium.

## Next Decisive Task: Mode B
The next stage is to define:
$$ \delta a_i = \alpha g_i $$
where $g_i$ is a feature vector fixed *before looking at or fitting the D absorption feature*. Mode B will introduce a frozen feature vector, blinding of the D window, and formal Bayesian model comparison between M0 (Standard D/H), M1 (TEP-driven shift, no D), M2 (Real D/H + TEP), and M3 (H I Interloper).
