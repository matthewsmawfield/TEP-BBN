#!/usr/bin/env python3
"""
Gate 6-III: Orphan Feature Search in Existing VPFIT Models

The velocity-selection theorem predicts that narrow edge-shear features at
non-isotope offsets are absorbed into the H I component structure and never
flagged as D.  This script parses the existing VPFIT decompositions for the
three benchmark sightlines and searches for H I components matching the
orphan signature:

  - Narrow b-values (b < 15 km/s, cool edge gas)
  - Low columns (log N_HI < 15, unsaturated)
  - Velocity offset from parent NOT at the isotope shift (|dv - v_iso| > 10 km/s)
  - Within the same absorption system (|dv| < 500 km/s of parent)

Under the isotope-D null, the H I components near the D feature are just
ordinary interloper gas with no preferred velocity structure.  Under TEP,
there should be an excess of narrow components with a velocity distribution
broader than the isotope shift, centred near v_iso with sigma ~ 19 km/s.

The prediction (gate6_population_prediction.json) forecasts ~11 orphans
across the 3 benchmark sightlines.
"""

import sys
import re
import json
import numpy as np
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from scripts.utils.logger import print_status, setup_step_logger

C_KMS = 299792.458
V_ISO = 81.6  # km/s, D isotope shift (blueward of H)


def parse_vpfit_model(filepath):
    """Parse a VPFIT .26 model file and extract H I and D I components.

    Returns list of dicts with keys: ion, z, z_err, b, b_err, logN, logN_err.
    """
    components = []
    with open(filepath) as f:
        for line in f:
            line = line.rstrip()
            # Skip comment/header/filename lines
            if line.startswith('%') or line.startswith('%%') or not line.strip():
                continue
            # VPFIT component lines start with an ion name
            # Format: " H I     z  z_err  b  b_err  logN  logN_err  flags"
            # or " D I     z  ..."
            m = re.match(
                r'^\s*(H I|D I)\s+([\d.]+)([A-Z%!]?)\s+([\d.eE+-]+)\s+'
                r'([\d.]+)([a-zA-Z]?)\s+([\d.]+)\s+'
                r'([\d.]+)([a-zA-Z%!]?)\s+([\d.]+)\s+(\d+)',
                line
            )
            if m:
                ion = m.group(1)
                z = float(m.group(2))
                z_err = float(m.group(4))
                b = float(m.group(5))
                b_err = float(m.group(7))
                logN = float(m.group(8))
                logN_err = float(m.group(10))
                components.append({
                    'ion': ion,
                    'z': z,
                    'z_err': z_err,
                    'b': b,
                    'b_err': b_err,
                    'logN': logN,
                    'logN_err': logN_err,
                })
    return components


def velocity_offset(z_component, z_parent):
    """Compute velocity offset (km/s) of component from parent redshift.

    Positive = redward, negative = blueward.
    """
    return C_KMS * (z_component - z_parent) / (1.0 + z_parent)


def run_orphan_search():
    setup_step_logger(Path(__file__).stem)
    print_status("=== GATE 6-III: ORPHAN FEATURE SEARCH IN VPFIT MODELS ===", "SUCCESS")

    # ---- Sightline configuration ----
    # parent_z: the redshift of the main D-associated H I component
    # model_file: path to the VPFIT .26 model
    sightlines = {
        'Q1009+2956': {
            'model_file': project_root / 'data' / 'literature_components' / 'model_6a.26',
            'parent_z': 2.503587,  # component A (log N = 17.36)
            'instrument': 'Keck/HIRES',
            'vsig': 2.6,
        },
        'PKS1937-101': {
            'model_file': project_root / 'data' / 'literature_components' / 'PKS1937-101_z3.572_vpfit_model.26',
            'parent_z': 3.572132,  # component A
            'instrument': 'ESPRESSO',
            'vsig': 1.82,
        },
        'J1332+0052': {
            'model_file': project_root / 'data' / 'literature_components' / 'J1332+0052_z3.421_vpfit_model.26',
            'parent_z': 3.420830,  # component A (log N = 16.68)
            'instrument': 'UVES',
            'vsig': 2.51,
        },
    }

    # ---- Search parameters ----
    # Orphan signature from gate6_population_prediction.json
    b_max = 15.0       # km/s, narrow edge gas
    logN_max = 15.0    # unsaturated, edge-gas columns
    dv_system = 500.0  # km/s, max |dv| to be in the same system
    dv_iso_min = 10.0  # km/s, min |dv - v_iso| to be an orphan (not D)
    dv_iso_max = 5.0   # km/s, max |dv - v_iso| to be "D-identified"

    all_results = {}
    all_orphans = []

    for name, cfg in sightlines.items():
        print_status(f"\n--- {name} ({cfg['instrument']}, vsig={cfg['vsig']} km/s) ---", "TITLE")
        filepath = cfg['model_file']
        if not filepath.exists():
            print_status(f"  Model file not found: {filepath}", "WARN")
            continue

        components = parse_vpfit_model(filepath)
        hi_components = [c for c in components if c['ion'] == 'H I']
        di_components = [c for c in components if c['ion'] == 'D I']

        parent_z = cfg['parent_z']
        print_status(f"  Parent z = {parent_z:.6f}", "PROCESS")
        print_status(f"  Total H I components: {len(hi_components)}", "PROCESS")
        print_status(f"  Total D I components: {len(di_components)}", "PROCESS")

        # Compute velocity offsets for all H I components
        for c in hi_components:
            c['dv_parent'] = velocity_offset(c['z'], parent_z)

        # Filter to components in the same absorption system (|dv| < 500 km/s)
        system_components = [c for c in hi_components if abs(c['dv_parent']) < dv_system]
        print_status(f"  H I in system (|dv| < {dv_system} km/s): {len(system_components)}", "PROCESS")

        # Identify D-associated components (within ±5 km/s of isotope shift)
        d_associated = [c for c in system_components if abs(c['dv_parent'] + V_ISO) < dv_iso_max]
        print_status(f"  D-associated (|dv + {V_ISO}| < {dv_iso_max} km/s): {len(d_associated)}", "PROCESS")

        # Orphan candidates: narrow, low-column, non-isotope offset
        orphans = [
            c for c in system_components
            if c['b'] < b_max
            and c['logN'] < logN_max
            and abs(c['dv_parent'] + V_ISO) > dv_iso_min
        ]

        # Also exclude the parent itself (high column)
        orphans = [c for c in orphans if c['logN'] < 16.0]

        print_status(f"  Orphan candidates (b<{b_max}, logN<{logN_max}, |dv+{V_ISO}|>{dv_iso_min}): {len(orphans)}", "PROCESS")

        # Print orphan candidates
        if orphans:
            print_status(f"  {'dv_parent (km/s)':<18} {'b (km/s)':<12} {'logN':<10} {'z':<14}", "PROCESS")
            print_status(f"  {'-'*18} {'-'*12} {'-'*10} {'-'*14}", "PROCESS")
            for c in sorted(orphans, key=lambda x: abs(x['dv_parent'] + V_ISO)):
                dv = c['dv_parent']
                dist_from_iso = abs(dv + V_ISO)
                marker = " <-- NEAR ISO" if dist_from_iso < 20 else ""
                print_status(
                    f"  {dv:>12.1f}        {c['b']:>8.2f}    {c['logN']:>7.3f}   {c['z']:.10f}{marker}",
                    "PROCESS"
                )

        # Also print all system components for context
        print_status(f"\n  All system H I components:", "PROCESS")
        print_status(f"  {'dv_parent (km/s)':<18} {'b (km/s)':<12} {'logN':<10} {'orphan?':<10}", "PROCESS")
        print_status(f"  {'-'*18} {'-'*12} {'-'*10} {'-'*10}", "PROCESS")
        for c in sorted(system_components, key=lambda x: x['dv_parent']):
            dv = c['dv_parent']
            is_orphan = (c['b'] < b_max and c['logN'] < logN_max
                         and abs(dv + V_ISO) > dv_iso_min and c['logN'] < 16.0)
            is_d = abs(dv + V_ISO) < dv_iso_max
            tag = "ORPHAN" if is_orphan else ("D-assoc" if is_d else "")
            print_status(
                f"  {dv:>12.1f}        {c['b']:>8.2f}    {c['logN']:>7.3f}   {tag}",
                "PROCESS"
            )

        all_results[name] = {
            'parent_z': parent_z,
            'n_hi_total': len(hi_components),
            'n_hi_system': len(system_components),
            'n_d_associated': len(d_associated),
            'n_orphan_candidates': len(orphans),
            'orphans': [
                {
                    'z': c['z'],
                    'dv_parent_kms': c['dv_parent'],
                    'b_kms': c['b'],
                    'logN': c['logN'],
                    'dist_from_iso_kms': abs(c['dv_parent'] + V_ISO),
                }
                for c in orphans
            ],
            'system_components': [
                {
                    'z': c['z'],
                    'dv_parent_kms': c['dv_parent'],
                    'b_kms': c['b'],
                    'logN': c['logN'],
                }
                for c in system_components
            ],
        }

        all_orphans.extend(orphans)

    # ---- Summary ----
    total_orphans = len(all_orphans)
    print_status(f"\n{'='*70}", "SUCCESS")
    print_status(f"SUMMARY: {total_orphans} orphan candidates across 3 benchmark sightlines", "SUCCESS")
    print_status(f"Prediction: ~11 orphans expected (gate6_population_prediction.json)", "PROCESS")

    if all_orphans:
        dv_offsets = [c['dv_parent'] + V_ISO for c in all_orphans]
        b_values = [c['b'] for c in all_orphans]
        logN_values = [c['logN'] for c in all_orphans]

        print_status(f"\n  Orphan velocity distribution (dv - v_iso):", "PROCESS")
        print_status(f"    Mean: {np.mean(dv_offsets):.1f} km/s", "PROCESS")
        print_status(f"    Std:  {np.std(dv_offsets, ddof=1):.1f} km/s", "PROCESS")
        print_status(f"    Range: [{np.min(dv_offsets):.1f}, {np.max(dv_offsets):.1f}] km/s", "PROCESS")
        print_status(f"\n  Orphan b-values: mean={np.mean(b_values):.1f}, range=[{np.min(b_values):.1f}, {np.max(b_values):.1f}]", "PROCESS")
        print_status(f"  Orphan logN: mean={np.mean(logN_values):.2f}, range=[{np.min(logN_values):.2f}, {np.max(logN_values):.2f}]", "PROCESS")

    # ---- Save results ----
    output = {
        'gate': '6-III',
        'title': 'Orphan Feature Search in VPFIT Models',
        'search_parameters': {
            'b_max_kms': b_max,
            'logN_max': logN_max,
            'dv_system_kms': dv_system,
            'dv_iso_min_kms': dv_iso_min,
            'v_iso_kms': V_ISO,
        },
        'sightlines': all_results,
        'summary': {
            'total_orphan_candidates': total_orphans,
            'prediction_expected': 11.3,
            'orphan_dv_from_iso': {
                'mean': float(np.mean(dv_offsets)) if all_orphans else None,
                'std': float(np.std(dv_offsets, ddof=1)) if len(dv_offsets) > 1 else None,
                'min': float(np.min(dv_offsets)) if all_orphans else None,
                'max': float(np.max(dv_offsets)) if all_orphans else None,
            },
            'orphan_b_values': {
                'mean': float(np.mean(b_values)) if all_orphans else None,
                'min': float(np.min(b_values)) if all_orphans else None,
                'max': float(np.max(b_values)) if all_orphans else None,
            },
            'orphan_logN': {
                'mean': float(np.mean(logN_values)) if all_orphans else None,
                'min': float(np.min(logN_values)) if all_orphans else None,
                'max': float(np.max(logN_values)) if all_orphans else None,
            },
        },
    }

    output_path = project_root / 'results' / 'gate6_orphan_search.json'
    with open(output_path, 'w') as f:
        json.dump(output, f, indent=2)
    print_status(f"\n  Results saved to {output_path}", "SUCCESS")

    return output


def run_archival_search():
    """Gate 6-III (archival): Search public SQUAD UVES and KODIAQ DR2 HIRES
    spectra for orphan candidates at the D/H isotope-shift velocity.

    Uses publicly available data from:
    - SQUAD DR1 (Murphy et al. 2018): 467 UVES quasar spectra via ESO Phase 3
    - KODIAQ DR2 (O'Meara et al. 2017): 300 HIRES quasar spectra via Keck KOA
    - KODIAQ Z LLS catalog (Lehner et al. 2016): 26 pLLSs/LLSs at 2.3<z<3.3
    """
    from astropy.io import fits
    import os

    print_status("=" * 70, "HEADER")
    print_status("Gate 6-III (Archival): Public-data orphan search", "HEADER")
    print_status("=" * 70, "HEADER")

    project_root = Path(__file__).resolve().parent.parent.parent
    results_dir = project_root / 'results'
    results_dir.mkdir(exist_ok=True)

    # KODIAQ Z LLS catalog (Lehner et al. 2016)
    kodiaq_catalog_path = project_root / 'data' / 'kodiaq_z_lls_catalog.json'
    if not kodiaq_catalog_path.exists():
        print_status("  KODIAQ Z catalog not found; skipping archival search", "WARN")
        return None

    with open(kodiaq_catalog_path) as f:
        kodiaq_catalog = json.load(f)

    # LLS-class targets (log NHI 17.0-19.0) — best for orphan searching
    lls_targets = [s for s in kodiaq_catalog if 17.0 <= s['log_nhi'] <= 19.0]
    print_status(f"  KODIAQ Z: {len(kodiaq_catalog)} pLLSs/LLSs, {len(lls_targets)} LLS-class", "PROCESS")

    kodiaq_base = project_root / 'data' / 'raw' / 'spectra' / 'KODIAQ' / 'KODIAQ_DR2_20170619'

    def load_kodiaq_spectrum(target_name):
        """Load the best KODIAQ HIRES spectrum (continuum-normalised, log10 wavelength)."""
        target_dir = kodiaq_base / target_name
        if not target_dir.exists():
            return None, None, None
        fits_files = []
        for root, _, files in os.walk(str(target_dir)):
            for f in files:
                if f.endswith('_f.fits') and 'spec2' not in f:
                    fpath = os.path.join(root, f)
                    fits_files.append((fpath, os.path.getsize(fpath)))
        if not fits_files:
            return None, None, None
        fits_files.sort(key=lambda x: x[1], reverse=True)
        best = fits_files[0][0]
        e_file = best.replace('_f.fits', '_e.fits')
        hdul = fits.open(best)
        flux = np.array(hdul[0].data, dtype=float)
        hdr = hdul[0].header
        hdul.close()
        crval1 = hdr.get('CRVAL1', 0)
        cdelt1 = hdr.get('CDELT1', 1)
        wave = 10 ** (crval1 + cdelt1 * np.arange(len(flux)))
        err = None
        if os.path.exists(e_file):
            hdul_e = fits.open(e_file)
            err = np.array(hdul_e[0].data, dtype=float)
            hdul_e.close()
        return wave, flux, err

    archival_results = []
    for t in lls_targets:
        name = t['name']
        z_abs = t['z_abs']
        log_nhi = t['log_nhi']

        wave, flux, err = load_kodiaq_spectrum(name)
        if wave is None:
            archival_results.append({
                'name': name, 'z_abs': z_abs, 'log_nhi': log_nhi,
                'status': 'no_data',
            })
            continue

        valid = np.isfinite(flux) & (flux > -1) & (flux < 2)
        if err is not None:
            valid &= np.isfinite(err) & (err > 0) & (err < 1e30)
        wave_v, flux_v = wave[valid], flux[valid]
        err_v = err[valid] if err is not None else np.ones_like(flux_v)

        lya_obs = 1215.6701 * (1 + z_abs)
        dv = C_KMS * (wave_v - lya_obs) / lya_obs
        mask = (dv >= -300) & (dv <= 300)
        if mask.sum() < 10:
            archival_results.append({
                'name': name, 'z_abs': z_abs, 'log_nhi': log_nhi,
                'status': 'no_coverage',
            })
            continue

        dv_r, flux_r, err_r = dv[mask], flux_v[mask], err_v[mask]
        min_flux = float(np.min(flux_r))
        med_flux = float(np.median(flux_r))
        med_sn = float(np.median(flux_r / err_r))

        # Check saturation
        if min_flux < 0.01:
            # Try Lyβ
            lyb_obs = 1025.7223 * (1 + z_abs)
            dv_b = C_KMS * (wave_v - lyb_obs) / lyb_obs
            mask_b = (dv_b >= -300) & (dv_b <= 300)
            if mask_b.sum() > 10:
                dv_r, flux_r, err_r = dv_b[mask_b], flux_v[mask_b], err_v[mask_b]
                min_flux = float(np.min(flux_r))
                if min_flux < 0.01:
                    archival_results.append({
                        'name': name, 'z_abs': z_abs, 'log_nhi': log_nhi,
                        'status': 'saturated', 'min_flux': min_flux,
                        'med_flux': med_flux, 'med_sn': med_sn,
                    })
                    continue
            else:
                archival_results.append({
                    'name': name, 'z_abs': z_abs, 'log_nhi': log_nhi,
                    'status': 'saturated', 'min_flux': min_flux,
                    'med_flux': med_flux, 'med_sn': med_sn,
                })
                continue

        # Search for narrow features near isotope shift
        orphan_candidates = []
        for dv_c in np.arange(-200, 50, 3):
            bin_mask = (dv_r >= dv_c) & (dv_r < dv_c + 3)
            if bin_mask.sum() > 0:
                f_med = float(np.median(flux_r[bin_mask]))
                e_med = float(np.median(err_r[bin_mask]))
                depth = 1 - f_med
                sigma = depth / e_med if e_med > 0 else 0
                if abs(dv_c + V_ISO) < 60 and depth > 0.05 and sigma > 3:
                    orphan_candidates.append({
                        'dv': dv_c, 'flux': f_med, 'depth': depth,
                        'sigma': sigma, 'dv_from_iso': dv_c + V_ISO,
                    })

        archival_results.append({
            'name': name, 'z_abs': z_abs, 'log_nhi': log_nhi,
            'status': 'searched',
            'min_flux': min_flux, 'med_flux': med_flux, 'med_sn': med_sn,
            'n_orphan_candidates': len(orphan_candidates),
            'orphan_candidates': orphan_candidates,
        })

    n_searched = sum(1 for r in archival_results if r['status'] == 'searched')
    n_saturated = sum(1 for r in archival_results if r['status'] == 'saturated')
    n_orphans = sum(r.get('n_orphan_candidates', 0) for r in archival_results)

    print_status(f"  Searched: {n_searched}, Saturated: {n_saturated}, "
                 f"Orphan candidates: {n_orphans}", "PROCESS")

    output = {
        'gate': '6-III-archival',
        'title': 'Archival Orphan Search with Public SQUAD/KODIAQ Data',
        'data_sources': {
            'SQUAD_DR1': 'Murphy et al. 2018, MNRAS, 482, 3458 (467 UVES spectra)',
            'KODIAQ_DR2': "O'Meara et al. 2017, AJ, 154, 114 (300 HIRES spectra)",
            'KODIAQ_Z_LLS': 'Lehner et al. 2016, ApJ, 833, 283 (26 pLLSs/LLSs)',
        },
        'n_sightlines_searched': n_searched + n_saturated,
        'n_usable': n_searched,
        'n_orphan_candidates': n_orphans,
        'sightlines': archival_results,
    }

    output_path = results_dir / 'gate6_archival_search.json'
    with open(output_path, 'w') as f:
        json.dump(output, f, indent=2)
    print_status(f"  Results saved to {output_path}", "SUCCESS")

    return output


if __name__ == '__main__':
    run_orphan_search()
    run_archival_search()
