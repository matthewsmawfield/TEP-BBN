# Q1009+2956 Manifest Validation Report
Generated: 2026-07-19T14:50:37.384191Z

## Data Conventions & Provenance
- **Wavelength Grid**: Strictly monotonic, Vacuum (standard KODIAQ convention)
- **Heliocentric Correction**: Applied (standard KODIAQ convention)
- **Flux Normalization**: Unnormalized raw flux units (continuum required during fitting)
- **Error Interpretation**: 1-sigma flux uncertainties
- **Instrumental Gaussian Sigma**: 2.5 - 3.0 km/s (depends on binning, will be free/profiled in RT fit)

## Raw File Provenance
- `q1011p2941_C1x1.dat`: SHA-256 `a379b504802cfa414ca289e0e722c2e039c162c60b840adff7ddbca24fbb1018`
- `q1011p2941_C1x2.dat`: SHA-256 `7be63c993104d19ead31da37e7596ddccb0af373a472638331a94d86cb1b206f`
- `q1011p2941_C5x1.dat`: SHA-256 `440e2498a8621c0d63bec2d8da573b790536bb28afa96d9291902d0cb9ddad0f`
- `q1011p2941_C5x2.dat`: SHA-256 `94c84bfbacd534b7f1c4090a1c4741c90f15f077e2d3568fc027dff144199b0d`


## Coverage & Masking
To prevent duplicated likelihood pixels from overlapping windows (e.g. Ly13/Ly14), we construct a union mask across all requested transitions for each coadd. Pixels are grouped into contiguous chunks and evaluated exactly once.

### q1011p2941_C1x1.dat
- **Total Native Pixels**: 183323
- **Wavelength Range**: 3156.62 - 7032.63 Å
- **Monotonic Grid**: True
- **Pixels in Union Mask**: 4584
- **Contiguous Chunks**: 12
- **Negative/Invalid Errors in Mask**: 0

### q1011p2941_C1x2.dat
- **Total Native Pixels**: 74212
- **Wavelength Range**: 3128.86 - 5955.26 Å
- **Monotonic Grid**: True
- **Pixels in Union Mask**: 2311
- **Contiguous Chunks**: 12
- **Negative/Invalid Errors in Mask**: 9

### q1011p2941_C5x1.dat
- **Total Native Pixels**: 151214
- **Wavelength Range**: 3074.81 - 5953.59 Å
- **Monotonic Grid**: True
- **Pixels in Union Mask**: 4586
- **Contiguous Chunks**: 12
- **Negative/Invalid Errors in Mask**: 19

### q1011p2941_C5x2.dat
- **Total Native Pixels**: 73891
- **Wavelength Range**: 3137.50 - 5969.79 Å
- **Monotonic Grid**: True
- **Pixels in Union Mask**: 2301
- **Contiguous Chunks**: 12
- **Negative/Invalid Errors in Mask**: 15

## Transition Inclusions
- **Ly_alpha**: 4254.42 - 4265.00 Å (Rest: 1215.67 Å)
- **Ly_beta**: 3591.10 - 3597.10 Å (Rest: 1025.72 Å)
- **Ly_gamma**: 3403.95 - 3411.03 Å (Rest: 972.53 Å)
- **Ly_6**: 3259.30 - 3264.20 Å (Rest: 930.74 Å)
- **Ly_13**: 3209.81 - 3212.89 Å (Rest: 916.42 Å)
- **Ly_14**: 3208.08 - 3210.20 Å (Rest: 915.82 Å)
- **Ly_21_24**: 3199.50 - 3201.25 Å (Rest: 913.0 Å)
- **C_II_1334**: 4672.00 - 4680.00 Å (Rest: 1334.5323 Å)
- **C_III_977**: 3419.00 - 3427.00 Å (Rest: 977.0201 Å)
- **C_IV_1548**: 5422.00 - 5430.00 Å (Rest: 1548.195 Å)
- **C_IV_1550**: 5431.00 - 5439.00 Å (Rest: 1550.77 Å)
- **Si_IV_1393**: 4881.00 - 4889.00 Å (Rest: 1393.755 Å)
- **Si_IV_1402**: 4913.00 - 4921.00 Å (Rest: 1402.77 Å)