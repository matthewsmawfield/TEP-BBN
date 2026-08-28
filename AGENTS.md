# AGENTS.md — TEP-BBN Pipeline

## Project Overview

The TEP-BBN (Temporal Equivalence Principle — Big Bang Nucleosynthesis) pipeline
tests whether observed D/H ratios in quasar absorption-line systems are
consistent with BBN predictions, or whether a "pure-temporal" origin (variable
constants) provides a better fit.

## Sightline Registry

| Sightline     | z_abs    | Instrument | R      | Reference                          | Config                          |
|---------------|----------|------------|--------|------------------------------------|---------------------------------|
| Q1009+2956    | 2.5042   | UVES       | 115000 | Zavarygin et al. 2018 (SQUAD DR1)  | configs/sightlines/Q1009+2956.json  |
| PKS1937-101   | 3.572    | ESPRESSO   | 70000  | Cooke et al. 2024 (arXiv:2402.05586) | configs/sightlines/PKS1937-101.json |
| J1332+0052    | 3.4211   | UVES       | 50800  | Riemer-Sørensen et al. 2024 (arXiv:2401.12797) | configs/sightlines/J1332+0052.json |

## Key Commands

### Reproduce all results (provenance verification only)
```bash
python scripts/reproduce.py --all --verify-only
```

### Full reproduction (build models + run Gates 2 & 3)
```bash
python scripts/reproduce.py --all
python scripts/reproduce.py --sightline PKS1937-101
```

### Build VPFIT model files
```bash
python scripts/steps/build_pks1937_model.py
python scripts/steps/build_j1332_model.py
```

### Run individual gates
```bash
python scripts/steps/step_02_q1009.py --sightline Q1009+2956
python scripts/steps/step_03_significance.py --sightline Q1009+2956
```

### Ingest new sightline data
```bash
python scripts/ingest_sightline.py --sightline PKS1937-101 --skip-download
```

## Architecture

### Pipeline Stages
1. **Ingest** (`ingest_sightline.py`): Download/coadd spectra, build union manifest
2. **Build model** (`build_*_model.py`): Parse LaTeX tables, write VPFIT .26 files
3. **Gate 2** (`step_02_q1009.py`): Spectroscopic fit verification (T_obs)
4. **Gate 3** (`step_03_significance.py`): Monte Carlo significance calibration

### Core Libraries (`scripts/lib/`)
- `physical_rt_engine.py`: Voigt profile radiative transfer with full Lyman series
- `model_parser.py`: VPFIT .26 file parser with tie structure
- `model_builder.py`: 6-model hypothesis framework (M_NULL, M_D6a, M_Drefit, M_Dfree, M_H, M_D+H)
- `doppler_physics.py`: Thermal + turbulent Doppler broadening
- `block_coordinate_optimizer.py`: Block coordinate descent optimizer

### Atomic Data
The `AtomicData` class in `physical_rt_engine.py` contains 15 Lyman series
transitions (1→2 through 1→14, plus 1→22) with:
- **Wavelengths**: NIST ASD for n≤6, Rydberg formula (reduced-mass corrected) for n≥7
- **Oscillator strengths**: Exact hydrogenic formula
  `f(1s→np) = (2^8 · n^5 · (n−1)^(2n−4)) / (3 · (n+1)^(2n+4))`
- **Damping coefficients (Γ)**: NIST/literature for n≤7, branching-ratio scaling for n≥8

**CRITICAL**: All 15 transitions must be passed to `compute_optical_depth()` for
any sightline with high-order Lyman series regions. Missing transitions cause
zero absorption in those regions, inflating T_obs.

### D Velocity Offset
The D isotope velocity offset is -81.6 km/s (exact reduced-mass calculation).
All sightline configs use -81.6. This MUST be passed to `build_model_components()`
via the `d_velocity_offset_kms` parameter. Never hardcode this value.

### vsig Convention
The `vsig` field in .26 files and manifests is the Gaussian **sigma** (standard
deviation) in km/s, NOT the FWHM. The conversion is: sigma = c / (2.35482 * R).
Passing FWHM instead of sigma inflates the convolution kernel by 2.35x.

### z_abs Source of Truth
The pipeline uses `cfg.get("z_abs", manifest["z_abs"])` as the reference redshift.
The config z_abs is authoritative; the manifest z_abs may be rounded.

## Known Issues (Fixed)

1. **Missing Lyman transitions** (CRITICAL, fixed 2026-08-27): Lyδ, Lyε, Ly7-Ly12
   were missing from `AtomicData`, causing zero absorption in 6/13 PKS1937 regions.
2. **Wrong oscillator strengths** (CRITICAL, fixed 2026-08-27): Ly13, Ly14, Ly21
   had f-values ~1.7× too large.
3. **Hardcoded D velocity offset** (HIGH, fixed 2026-08-27): `step_02`, `step_03`,
   and `model_builder.py` hardcoded -81.6 km/s instead of reading from config.
4. **Dropped components** (HIGH, fixed in build_pks1937_model.py): 3 "Unknown"
   components silently dropped due to LaTeX parsing error.
5. **Duplicate interlopers** (HIGH, fixed in build_pks1937_model.py): 4 interloper
   components duplicated.
6. **Missing J1332 build script** (CRITICAL, fixed 2026-08-27): Created
   `build_j1332_model.py` from Riemer-Sørensen et al. 2024 Table 3.
7. **Missing reproduce.py** (CRITICAL, fixed 2026-08-27): Created single entry
   point for reproducibility verification.
8. **PKS1937 vsig was FWHM not sigma** (CRITICAL, fixed 2026-08-27): .26 file had
   vsig=4.28 (FWHM) instead of 1.82 (sigma). Convolution kernel was 2.35x too wide.
9. **J1332 manifest z_abs rounded** (CRITICAL, fixed 2026-08-27): Manifest had
   z_abs=3.42 instead of 3.4210863, causing 73.7 km/s velocity offset in all
   calculations. Fixed manifest and made pipeline prefer config z_abs.
10. **Q1009 d_velocity_offset was -82.0** (MEDIUM, fixed 2026-08-27): Changed to
    -81.6 for consistency with exact isotope shift.
11. **parent_window_kms=None** (HIGH, fixed 2026-08-27): Q1009 and J1332 configs
    had `parent_window_kms: None`, causing `cfg.get()` to return None. Fixed to
    1000.0 and changed code to use `cfg.get("parent_window_kms") or 1000.0`.
12. **finalize_manuscript_numbers.py used parent 0** (MEDIUM, fixed 2026-08-27):
    Used `h_comps[0]` instead of auto-detected D parent for isotope RMS calculation.
13. **J1332 manifest resolving_power wrong** (LOW, fixed 2026-08-27): Had 47000
    instead of 50800.

## File Layout

```
configs/
  sightlines/           # Per-sightline configuration (z_abs, bounds, multistart)
  TEP_BBN_FOUNDATION_FREEZE.json
data/
  raw/                  # Raw FITS files (not in git)
  raw/literature_source/  # arXiv source tarballs with provenance
  literature_components/  # VPFIT .26 model files
  processed/            # Union manifests with coadded spectra
results/                # Gate 2/3 output ledgers
scripts/
  lib/                  # Core physics libraries
  steps/                # Pipeline step scripts
  reproduce.py          # Reproducibility entry point
  ingest_sightline.py   # Data ingestion tool
```
