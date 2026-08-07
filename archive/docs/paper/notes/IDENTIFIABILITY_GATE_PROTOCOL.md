# Identifiability Gate Protocol

To avoid post-hoc line fitting, TEP-BBN imposes a strict prior-predictive identifiability gate (Gate -1). The proper-time feature vector ($g_i$) and the amplitude prior ($\alpha_{\rm shear}$) must be fixed *before* D-window unblinding. 

A model is allowed to proceed to evidence testing (M1/M2 vs M0/M3) only if its predicted interval satisfies all of the following conditions:
1. **Blinded Feature Vector:** The feature vector is frozen before D-window unblinding, constructed exclusively from metal-line structure and non-D Lyman lines.
2. **Independent Amplitude Prior:** The $\alpha$ prior is derived independently of the D-window location, using TEP screening theory and DLA density scales.
3. **Correct Sign and Containment:** The prior-predictive interval contains the observed D-like feature with the theoretically required shift sign (blueward for sparse components relative to dense ones).
4. **Information Content:** The predicted interval must cover $< 25\%$ of the plausible velocity search window. A prediction that spans the entire window is uninformative.
5. **Robustness (Null Test):** The shuffled-feature false-positive rate must be $< 0.05$. A random assignment of $g_i$ must have a low probability of successfully predicting the location interval.

By defining these gates in advance, we ensure an adversarial and rigorously falsifiable test.
