# Bounded Convergence Adjudication Report

This report evaluates the `dynesty` nested sampler convergence under the strictly frozen validation criteria.

## Raw Audit Results

| Data seed | nlive | Sampler seed | Classification | $\Delta\log Z$ | $\alpha$ mean | $\alpha$ std | Lower edge | Upper edge | max logL | null logL | ESS | ncall |
| --------- | ----: | -----------: | -------------- | ----: | -----: | ----: | ---------- | ---------- | -----------: | --: | --: | --: |
| 1001 | 100 | 50001 | TEP_POSITIVE | 5.37 | 0.000675 | 0.000124 | False | False | 2813.27 | 2810.12 | 2 | 98229 |
| 1001 | 100 | 50002 | TEP_POSITIVE | 5.66 | 0.000679 | 0.000128 | False | False | 2813.21 | 2811.18 | 2 | 98175 |
| 1001 | 100 | 50003 | TEP_POSITIVE | 5.86 | 0.000669 | 0.000127 | False | False | 2813.22 | 2810.61 | 2 | 95342 |
| 1001 | 300 | 50001 | TEP_POSITIVE | 8.80 | 0.000675 | 0.000138 | False | False | 2812.65 | 2806.07 | 4 | 100624 |
| 1001 | 300 | 50002 | TEP_POSITIVE | 9.10 | 0.000676 | 0.000132 | False | False | 2812.92 | 2805.22 | 4 | 100715 |
| 1001 | 300 | 50003 | TEP_POSITIVE | 11.39 | 0.000653 | 0.000121 | False | False | 2813.07 | 2803.26 | 4 | 100680 |
| 1001 | 600 | 50001 | TEP_POSITIVE | 15.16 | 0.000702 | 0.000131 | False | False | 2812.68 | 2799.38 | 6 | 101302 |
| 1001 | 600 | 50002 | TEP_POSITIVE | 27.07 | 0.000663 | 0.000103 | False | False | 2812.90 | 2788.43 | 6 | 101231 |
| 1001 | 600 | 50003 | TEP_POSITIVE | 31.11 | 0.000647 | 0.000121 | False | False | 2813.07 | 2783.48 | 6 | 101331 |
| 1002 | 100 | 50001 | REAL_NEGATIVE | 4.51 | 0.000694 | 0.000117 | False | False | 2775.78 | 2774.81 | 2 | 95948 |
| 1002 | 100 | 50002 | REAL_NEGATIVE | 3.05 | 0.000696 | 0.000110 | False | False | 2775.79 | 2775.93 | 2 | 97509 |
| 1002 | 100 | 50003 | REAL_NEGATIVE | 3.20 | 0.000686 | 0.000112 | False | False | 2775.75 | 2775.32 | 2 | 98765 |
| 1002 | 300 | 50001 | TEP_POSITIVE | 8.54 | 0.000658 | 0.000120 | False | False | 2775.62 | 2768.18 | 4 | 100678 |
| 1002 | 300 | 50002 | TEP_POSITIVE | 6.14 | 0.000687 | 0.000098 | False | False | 2775.43 | 2770.65 | 4 | 100674 |
| 1002 | 300 | 50003 | TEP_POSITIVE | 11.75 | 0.000698 | 0.000106 | False | False | 2775.30 | 2764.29 | 4 | 100683 |
| 1002 | 600 | 50001 | TEP_POSITIVE | 26.74 | 0.000697 | 0.000120 | False | False | 2773.71 | 2748.57 | 6 | 101301 |
| 1002 | 600 | 50002 | REAL_NEGATIVE | 22.49 | 0.000644 | 0.000135 | True | False | 2775.39 | 2753.97 | 6 | 101285 |
| 1002 | 600 | 50003 | TEP_POSITIVE | 14.47 | 0.000694 | 0.000130 | False | False | 2774.55 | 2762.18 | 6 | 101253 |
| 1008 | 100 | 50001 | TEP_POSITIVE | 6.53 | 0.000661 | 0.000119 | False | False | 2813.95 | 2810.02 | 2 | 99556 |
| 1008 | 100 | 50002 | REAL_NEGATIVE | 4.35 | 0.000655 | 0.000118 | False | False | 2813.79 | 2811.56 | 2 | 97231 |
| 1008 | 100 | 50003 | TEP_POSITIVE | 6.13 | 0.000651 | 0.000116 | False | False | 2813.80 | 2811.93 | 2 | 96455 |
| 1008 | 300 | 50001 | TEP_POSITIVE | 8.55 | 0.000650 | 0.000113 | False | False | 2813.61 | 2806.30 | 4 | 100753 |
| 1008 | 300 | 50002 | TEP_POSITIVE | 8.70 | 0.000658 | 0.000116 | False | False | 2813.06 | 2806.93 | 4 | 100696 |
| 1008 | 300 | 50003 | TEP_POSITIVE | 16.69 | 0.000660 | 0.000130 | False | False | 2813.02 | 2798.81 | 4 | 100695 |
| 1008 | 600 | 50001 | TEP_POSITIVE | 23.21 | 0.000663 | 0.000099 | False | False | 2812.16 | 2790.65 | 6 | 101249 |
| 1008 | 600 | 50002 | TEP_POSITIVE | 21.36 | 0.000693 | 0.000105 | False | False | 2812.95 | 2792.94 | 6 | 101331 |
| 1008 | 600 | 50003 | REAL_NEGATIVE | 23.36 | 0.000626 | 0.000113 | True | False | 2813.69 | 2791.75 | 7 | 101292 |

## Frozen Criteria Evaluation

### Data Seed 1001, `nlive`=100
- **Classification Stability**: PASS (['TEP_POSITIVE', 'TEP_POSITIVE', 'TEP_POSITIVE'])
- **Evidence Stability (M2)**: PASS (Max diff: 0.69)
- **Delta logZ Stability**: PASS (Max diff: 0.49)
- **Edge Flag Stability**: PASS ([False, False, False])

### Data Seed 1001, `nlive`=300
- **Classification Stability**: PASS (['TEP_POSITIVE', 'TEP_POSITIVE', 'TEP_POSITIVE'])
- **Evidence Stability (M2)**: PASS (Max diff: 0.21)
- **Delta logZ Stability**: PASS (Max diff: 2.59)
- **Edge Flag Stability**: PASS ([False, False, False])

### Data Seed 1001, `nlive`=600
- **Classification Stability**: PASS (['TEP_POSITIVE', 'TEP_POSITIVE', 'TEP_POSITIVE'])
- **Evidence Stability (M2)**: PASS (Max diff: 0.89)
- **Delta logZ Stability**: FAIL (Max diff: 15.95)
- **Edge Flag Stability**: PASS ([False, False, False])

### Data Seed 1002, `nlive`=100
- **Classification Stability**: PASS (['REAL_NEGATIVE', 'REAL_NEGATIVE', 'REAL_NEGATIVE'])
- **Evidence Stability (M2)**: PASS (Max diff: 0.47)
- **Delta logZ Stability**: PASS (Max diff: 1.46)
- **Edge Flag Stability**: PASS ([False, False, False])

### Data Seed 1002, `nlive`=300
- **Classification Stability**: PASS (['TEP_POSITIVE', 'TEP_POSITIVE', 'TEP_POSITIVE'])
- **Evidence Stability (M2)**: PASS (Max diff: 0.85)
- **Delta logZ Stability**: PASS (Max diff: 5.61)
- **Edge Flag Stability**: PASS ([False, False, False])

### Data Seed 1002, `nlive`=600
- **Classification Stability**: FAIL (['TEP_POSITIVE', 'REAL_NEGATIVE', 'TEP_POSITIVE'])
- **Evidence Stability (M2)**: PASS (Max diff: 1.50)
- **Delta logZ Stability**: FAIL (Max diff: 12.26)
- **Edge Flag Stability**: FAIL ([False, True, False])

### Data Seed 1008, `nlive`=100
- **Classification Stability**: FAIL (['REAL_NEGATIVE', 'TEP_POSITIVE', 'TEP_POSITIVE'])
- **Evidence Stability (M2)**: PASS (Max diff: 0.52)
- **Delta logZ Stability**: PASS (Max diff: 2.19)
- **Edge Flag Stability**: PASS ([False, False, False])

### Data Seed 1008, `nlive`=300
- **Classification Stability**: PASS (['TEP_POSITIVE', 'TEP_POSITIVE', 'TEP_POSITIVE'])
- **Evidence Stability (M2)**: PASS (Max diff: 0.31)
- **Delta logZ Stability**: PASS (Max diff: 8.14)
- **Edge Flag Stability**: PASS ([False, False, False])

### Data Seed 1008, `nlive`=600
- **Classification Stability**: FAIL (['TEP_POSITIVE', 'TEP_POSITIVE', 'REAL_NEGATIVE'])
- **Evidence Stability (M2)**: PASS (Max diff: 1.35)
- **Delta logZ Stability**: PASS (Max diff: 2.01)
- **Edge Flag Stability**: FAIL ([False, False, True])
