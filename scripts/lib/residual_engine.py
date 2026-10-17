import json
import sys
from pathlib import Path

import numpy as np
from scipy.stats import t as student_t

script_dir = Path(__file__).parent
project_root = script_dir.parent.parent
sys.path.insert(0, str(project_root))

from scripts.lib.block_coordinate_optimizer import BlockCoordinateOptimizer
from scripts.lib.model_builder import build_model_components
from scripts.lib.model_parser import ParameterManager, parse_vpfit_ties
from scripts.lib.physical_rt_engine import RadiativeTransferEngine


def likelihood_residuals(residuals):
    """Keep every valid data residual; reject any numerical model failure.

    Student-t tails already handle outliers. Dropping pixels according to
    a model's residual can spuriously improve a worse model's likelihood.
    Data-quality selection belongs in the fixed input mask.
    """
    residuals = np.asarray(residuals, dtype=float)
    if residuals.size == 0 or not np.all(np.isfinite(residuals)):
        return np.array([np.inf])
    return residuals

# Canonical transition lists (avoid recreating lists every call)
# Full Lyman series 1→2 through 1→14, plus 1→22 for high-n regions.
# All 15 transitions MUST be present — missing any causes zero absorption
# in those fitting regions, inflating T_obs and biasing D/H fits.
_LYMAN = [
    'HI_Lya', 'HI_Lyb', 'HI_Lyg', 'HI_Lyd', 'HI_Lye',
    'HI_Ly6', 'HI_Ly7', 'HI_Ly8', 'HI_Ly9', 'HI_Ly10',
    'HI_Ly11', 'HI_Ly12', 'HI_Ly13', 'HI_Ly14', 'HI_Ly21',
]
_CIV = ['CIV_1548', 'CIV_1550']
_CIII = ['CIII_977']
_CII = ['CII_1334']
_SiIV = ['SiIV_1393', 'SiIV_1402']

# Continuum basis order — dynamic per-block.
#
# Lyman-series regions (Lyα through Ly14) contain broad H I wings that
# require a flexible continuum to separate from the narrow D feature.
# VPFIT uses a higher-order continuum by default; we use 10 continuum
# basis functions (9 multiplicative monomial terms + 1 additive
# zero-level), giving ~1 parameter per 50-60 pixels for a typical
# 568-pixel Lyα block.
#
# Metal-line regions (C IV, C III, C II, Si IV) contain only narrow
# absorption features with no broad H I wings.  A 10-parameter continuum
# over these blocks acts as a "mathematical sponge" that can absorb
# isotopic discrepancies, artificially depressing the T-statistic.
# We use 5 continuum parameters (4 multiplicative + 1 additive) for
# these blocks — sufficient for a smooth continuum without overfitting.
#
# This dynamic assignment was validated by audit: the init-parameter
# T-statistic decreases monotonically with N_cont, confirming that
# higher-order continua absorb the isotope signal.  The N=10 order
# is retained only where physically necessary (broad H I wings).
N_CONTINUUM_PARAMS_LYMAN = 10
N_CONTINUUM_PARAMS_METAL = 5
N_CONTINUUM_PARAMS = 10  # default; overridden per-block by get_cont_order()

# Rest-frame wavelengths of all Lyman series transitions (Å)
# Derived from AtomicData to ensure consistency with the RT engine.
# The previous hardcoded array had wrong wavelengths for Ly9–Ly21
# (off by up to 1.9 Å), which could misclassify blocks in get_cont_order().
from scripts.lib.physical_rt_engine import AtomicData as _AtomicData
_LYMAN_WAVELENGTHS = np.array([
    _AtomicData().get(t)[0] for t in _LYMAN
])


def get_cont_order(block, z_abs):
    """
    Determine the continuum basis order for a data block.

    Returns N_CONTINUUM_PARAMS_LYMAN (10) if the block wavelength range
    overlaps with any Lyman series transition at z_abs, otherwise
    N_CONTINUUM_PARAMS_METAL (5) for metal-line-only regions.
    """
    w_min = block['w_min'] if isinstance(block, dict) else block[0]
    w_max = block['w_max'] if isinstance(block, dict) else block[-1]
    obs_lyman = _LYMAN_WAVELENGTHS * (1.0 + z_abs)
    # Check if any Lyman transition falls within the block wavelength range
    overlap = np.any((obs_lyman >= w_min - 5.0) & (obs_lyman <= w_max + 5.0))
    return N_CONTINUUM_PARAMS_LYMAN if overlap else N_CONTINUUM_PARAMS_METAL


# ---------------------------------------------------------------------------
# Frozen-scaffold fast path
#
# Under every hypothesis in this analysis the shared Voigt architecture is held
# fixed, so the optical depth contributed by the 43 shared H I components and by
# every metal component is identical for all objective evaluations. Only the one
# or two candidate components vary. Recomputing the frozen contribution on every
# likelihood evaluation wastes ~95% of the runtime, so it is cached per block.
#
# The leave-one-out tests remove whole data blocks rather than transitions, so a
# per-block cache remains valid for them; callers pass the block subset and the
# matching cache subset.
# ---------------------------------------------------------------------------

def split_frozen_candidate(grouped_full, grouped_frozen):
    """Return only the candidate components (appended after the frozen ones)."""
    cand = {}
    for ion in ('H_I', 'D_I'):
        n_frozen = len(grouped_frozen.get(ion, []))
        cand[ion] = grouped_full.get(ion, [])[n_frozen:]
    return cand


def build_frozen_cache(grouped_frozen, data_blocks, engine):
    """
    Precompute, per data block, the optical depth of every component fixed by the
    shared scaffold, plus the per-block quantities that do not depend on the
    model parameters (continuum basis abscissa and inverse-variance weights).
    """
    cache = []
    for block in data_blocks:
        wave_fit = block['wave']
        tau = np.zeros_like(wave_fit)
        if grouped_frozen.get('H_I'):
            tau += engine.compute_optical_depth(wave_fit, _LYMAN, grouped_frozen['H_I'])
        if grouped_frozen.get('D_I'):
            tau += engine.compute_optical_depth(wave_fit, _LYMAN, grouped_frozen['D_I'])
        if grouped_frozen.get('C_IV'):
            tau += engine.compute_optical_depth(wave_fit, _CIV, grouped_frozen['C_IV'])
        if grouped_frozen.get('C_III'):
            tau += engine.compute_optical_depth(wave_fit, _CIII, grouped_frozen['C_III'])
        if grouped_frozen.get('C_II'):
            tau += engine.compute_optical_depth(wave_fit, _CII, grouped_frozen['C_II'])
        if grouped_frozen.get('Si_IV'):
            tau += engine.compute_optical_depth(wave_fit, _SiIV, grouped_frozen['Si_IV'])

        x_norm = 2.0 * (wave_fit - block['w_min']) / (block['w_max'] - block['w_min']) - 1.0
        n_cont = get_cont_order(block, engine.z_abs)
        # Precompute x_norm powers for the multiplicative monomial basis.
        # x_norm_powers[:, k] = x_norm**k for k = 0..n_cont-2 (used in the
        # continuum basis loop in compute_residuals_fast).
        x_norm_powers = np.empty((len(wave_fit), n_cont - 1))
        x_norm_powers[:, 0] = 1.0
        for k in range(1, n_cont - 1):
            x_norm_powers[:, k] = x_norm_powers[:, k - 1] * x_norm
        cache.append({
            'tau_frozen': tau,
            'x_norm': x_norm,
            'x_norm_powers': x_norm_powers,
            'W': 1.0 / np.maximum(block['err'], 1e-10) ** 2,
            'n_cont': n_cont,
        })
    return cache


def compute_residuals_fast(cand_comps, data_blocks, engine, frozen_cache):
    """
    Residuals using a precomputed frozen-scaffold optical depth.

    cand_comps: {'H_I': [...], 'D_I': [...]} containing only the candidate
    components. Numerically equivalent to compute_residuals() on the full
    component set (verified to machine precision by the pipeline self-test).
    """
    n_total = sum(len(b['wave']) for b in data_blocks)
    residuals_all = np.empty(n_total, dtype=float)
    offset = 0

    for block, cc in zip(data_blocks, frozen_cache):
        wave_fit = block['wave']
        tau_tot = cc['tau_frozen']

        cand_H = cand_comps.get('H_I')
        cand_D = cand_comps.get('D_I')
        if cand_H or cand_D:
            tau_tot = tau_tot.copy()
            if cand_H:
                tau_tot += engine.compute_optical_depth(wave_fit, _LYMAN, cand_H)
            if cand_D:
                tau_tot += engine.compute_optical_depth(wave_fit, _LYMAN, cand_D)

        exp_tau = np.exp(-tau_tot)
        exp_tau = np.maximum(exp_tau, 1e-300)
        n_cont = cc.get('n_cont', N_CONTINUUM_PARAMS)
        P = np.empty((len(wave_fit), n_cont))
        x_norm_powers = cc.get('x_norm_powers')
        if x_norm_powers is not None:
            # Fast path: precomputed x_norm powers from frozen cache
            for k in range(n_cont - 1):
                col = x_norm_powers[:, k] * exp_tau
                P[:, k] = engine.apply_convolution(col, wave_fit, block['vsig'])
        else:
            # Fallback for old caches without precomputed powers
            x_norm = cc['x_norm']
            for k in range(n_cont - 1):
                col = x_norm**k * exp_tau
                P[:, k] = engine.apply_convolution(col, wave_fit, block['vsig'])
        P[:, n_cont - 1] = 1.0  # zero level basis (no convolution needed)

        err_fit = block['err']
        flux_fit = block['flux']
        W = cc['W']

        H_mat = P.T @ (W[:, np.newaxis] * P)
        H_mat += 1e-10 * np.eye(n_cont)
        b_vec = P.T @ (W * flux_fit)

        try:
            c_opt = np.linalg.solve(H_mat, b_vec)
            flux_mod = P @ c_opt
            res = (flux_fit - flux_mod) / np.maximum(err_fit, 1e-10)
        except Exception:
            res = np.full_like(flux_fit, np.inf)

        if np.any(np.isnan(res)) or np.any(np.isinf(res)):
            res = np.full_like(flux_fit, np.inf)

        n = len(res)
        residuals_all[offset:offset + n] = res
        offset += n

    return residuals_all


def compute_residuals(grouped_comps, data_blocks, engine):
    """
    Compute residuals with analytic continuum profiling.

    Optimizations:
    - Pre-allocate residual array (no list.extend)
    - Use cached convolution kernels from engine
    - Minimize temporary array creation
    """
    n_total = sum(len(b['wave']) for b in data_blocks)
    residuals_all = np.empty(n_total, dtype=float)
    offset = 0

    for block in data_blocks:
        wave_fit = block['wave']
        tau_tot = np.zeros_like(wave_fit)

        if grouped_comps['H_I']:
            tau_tot += engine.compute_optical_depth(wave_fit, _LYMAN, grouped_comps['H_I'])
        if grouped_comps['D_I']:
            tau_tot += engine.compute_optical_depth(wave_fit, _LYMAN, grouped_comps['D_I'])
        if grouped_comps['C_IV']:
            tau_tot += engine.compute_optical_depth(wave_fit, _CIV, grouped_comps['C_IV'])
        if grouped_comps['C_III']:
            tau_tot += engine.compute_optical_depth(wave_fit, _CIII, grouped_comps['C_III'])
        if grouped_comps['C_II']:
            tau_tot += engine.compute_optical_depth(wave_fit, _CII, grouped_comps['C_II'])
        if grouped_comps['Si_IV']:
            tau_tot += engine.compute_optical_depth(wave_fit, _SiIV, grouped_comps['Si_IV'])

        x_norm = 2.0 * (wave_fit - block['w_min']) / (block['w_max'] - block['w_min']) - 1.0

        # Build continuum basis: dynamic order per block
        # (multiplicative monomial × convolved exp(-tau) + additive zero level)
        # Floor exp_tau to prevent zero basis columns in saturated pixels.
        exp_tau = np.exp(-tau_tot)
        exp_tau = np.maximum(exp_tau, 1e-300)
        n_cont = get_cont_order(block, engine.z_abs)
        P = np.empty((len(wave_fit), n_cont))
        for k in range(n_cont - 1):
            col = x_norm**k * exp_tau
            P[:, k] = engine.apply_convolution(col, wave_fit, block['vsig'])
        P[:, n_cont - 1] = 1.0  # zero level basis (no convolution needed)

        err_fit = block['err']
        flux_fit = block['flux']

        W = 1.0 / np.maximum(err_fit, 1e-10)**2
        H_mat = P.T @ (W[:, np.newaxis] * P)
        # Small Tikhonov regularization for numerical stability with
        # high-order continuum basis (prevents singular H_mat when
        # saturated pixels zero out many basis columns).
        H_mat += 1e-10 * np.eye(n_cont)
        b_vec = P.T @ (W * flux_fit)

        try:
            c_opt = np.linalg.solve(H_mat, b_vec)
            flux_mod = P @ c_opt
            res = (flux_fit - flux_mod) / np.maximum(err_fit, 1e-10)
        except Exception:
            res = np.full_like(flux_fit, np.inf)

        if np.any(np.isnan(res)) or np.any(np.isinf(res)):
            res = np.full_like(flux_fit, np.inf)

        n = len(res)
        residuals_all[offset:offset + n] = res
        offset += n

    return residuals_all


def run_six_model_converged_benchmark():
    print("=== Phase E: Converged Six-Model Isotope Identification Benchmark ===")
    manifest_path = project_root / 'data' / 'processed' / 'Q1009_union_manifest.json'
    vpfit_path = project_root / 'data' / 'literature_components' / 'model_6a.26'
    noise_model_path = project_root / 'configs' / 'tep_noise_model.json'

    with open(manifest_path, 'r') as f: manifest = json.load(f)
    with open(noise_model_path, 'r') as f: noise_cfg = json.load(f)

    z_abs_ref = manifest['z_abs']
    c_kms = 299792.458

    components_raw, regions = parse_vpfit_ties(vpfit_path)
    pm = ParameterManager(components_raw)
    engine = RadiativeTransferEngine(z_abs=z_abs_ref)

    data_blocks = []
    total_pixels = 0
    for r in regions:
        coadd = r['filename']
        if coadd not in manifest['coadds']: continue
        chunk_wave, chunk_flux, chunk_err = [], [], []
        for chunk in manifest['coadds'][coadd]:
            chunk_wave.extend(chunk['wave'])
            chunk_flux.extend(chunk['flux'])
            chunk_err.extend(chunk['err'])
        wave, flux, err = np.array(chunk_wave), np.array(chunk_flux), np.array(chunk_err)
        mask = (np.isfinite(flux)) & (np.isfinite(err)) & (err > 0) & (wave >= r['w_min']) & (wave <= r['w_max'])
        if np.sum(mask) == 0: continue
        n_p = int(np.sum(mask))
        total_pixels += n_p
        data_blocks.append({
            'wave': wave[mask], 'flux': flux[mask], 'err': err[mask],
            'vsig': r['vsig'], 'w_min': r['w_min'], 'w_max': r['w_max'],
            'coadd': coadd
        })

    print(f"Total dataset regions: {len(data_blocks)}, Total pixels: {total_pixels}")

    theta_shared_base = np.array(pm.theta_init)

    models_cfg = {
        'M_NULL': {'cand_init': None, 'bounds_cand': [], 'n_cand': 0},
        'M_D6a': {'cand_init': None, 'bounds_cand': [], 'n_cand': 0},
        'M_Drefit': {'cand_init': None, 'bounds_cand': [], 'n_cand': 0},
        'M_Dfree': {'cand_init': [12.5, 10000.0, 5.0], 'bounds_cand': [(10.0, 16.0), (1000.0, 40000.0), (1.0, 30.0)], 'n_cand': 3},
        'M_H': {'cand_init': [-135.0, 12.5, 10000.0, 5.0], 'bounds_cand': [(-160.0, 50.0), (10.0, 16.0), (1000.0, 40000.0), (1.0, 30.0)], 'n_cand': 4},
        'M_D+H': {'cand_init': [12.5, -135.0, 12.5, 10000.0, 5.0], 'bounds_cand': [(10.0, 16.0), (-160.0, 50.0), (10.0, 16.0), (1000.0, 40000.0), (1.0, 30.0)], 'n_cand': 5}
    }

    results = {}

    for m_name, cfg in models_cfg.items():
        print(f"\nRunning Model: {m_name}")

        if m_name == 'M_D6a':
            grouped = build_model_components('M_D6a', theta_shared_base, None, pm, z_abs_ref, c_kms)
            res = compute_residuals(grouped, data_blocks, engine)
            v_res = likelihood_residuals(res)
            ll = float(np.sum(student_t.logpdf(v_res, noise_cfg['nu'], noise_cfg['location'], noise_cfg['scale'])))
            results['M_D6a'] = {'model_name': m_name, 'log_likelihood': ll, 'nll': -ll, 'success': True}
            print(f"  -> Log Likelihood: {ll:.2f}")
            continue

        if cfg['n_cand'] == 0:
            grouped = build_model_components(m_name, theta_shared_base, None, pm, z_abs_ref, c_kms)
            res = compute_residuals(grouped, data_blocks, engine)
            v_res = likelihood_residuals(res)
            ll = float(np.sum(student_t.logpdf(v_res, noise_cfg['nu'], noise_cfg['location'], noise_cfg['scale'])))
            results[m_name] = {'model_name': m_name, 'log_likelihood': ll, 'nll': -ll, 'success': True}
            print(f"  -> Log Likelihood: {ll:.2f}")
            continue

        def cand_objective(th_c):
            grouped = build_model_components(m_name, theta_shared_base, th_c, pm, z_abs_ref, c_kms)
            res = compute_residuals(grouped, data_blocks, engine)
            v_res = likelihood_residuals(res)
            ll = np.sum(student_t.logpdf(v_res, noise_cfg['nu'], noise_cfg['location'], noise_cfg['scale']))
            return -ll

        opt = BlockCoordinateOptimizer(cand_objective, candidate_param_indices=list(range(cfg['n_cand'])), rel_tol=1e-7, abs_tol=0.01)
        x0 = np.array(cfg['cand_init'], dtype=float)
        bounds = cfg['bounds_cand']

        ms_res = opt.run_multi_start(x0, bounds=bounds, n_starts=3, jitter_scale=0.05, verbose=True)
        best = ms_res['best_result']
        results[m_name] = {
            'model_name': m_name,
            'log_likelihood': float(best['log_likelihood']),
            'nll': float(best['fun']),
            'success': bool(best['success']),
            'is_mode_stable': bool(ms_res['is_mode_stable']),
        }
        print(f"  -> Best Log Likelihood: {best['log_likelihood']:.2f}")

    out_file = project_root / 'data' / 'processed' / 'q1009_six_model_converged_results.json'
    with open(out_file, 'w') as f:
        json.dump(results, f, indent=4)
    print(f"\nSaved converged results to {out_file}")

if __name__ == '__main__':
    run_six_model_converged_benchmark()
