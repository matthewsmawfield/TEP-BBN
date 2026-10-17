import numpy as np
from scipy.special import wofz

# Physical constants
c_kms = 299792.458  # km/s
e_charge = 4.803204e-10  # esu
m_e = 9.109383e-28  # g
c_cgs = 2.99792458e10  # cm/s

# Cross-section constant: (sqrt(pi) * e^2) / (m_e * c)
sigma_0 = (np.sqrt(np.pi) * e_charge**2) / (m_e * c_cgs)


def voigt_profile(x, a):
    """Compute the Voigt profile (real part of Faddeeva function)."""
    return wofz(x + 1j * a).real


def voigt_profile_vectorized(x, a):
    """Vectorized Voigt over x (a is scalar)."""
    return wofz(x + 1j * a).real


class AtomicData:
    """Atomic data for hydrogen Lyman series transitions (1s → np).

    Wavelengths: NIST ASD for n≤6, Rydberg formula with reduced-mass
    correction for n≥7.  Oscillator strengths: exact hydrogenic formula
    f(1s→np) = (2^8 · n^5 · (n−1)^(2n−4)) / (3 · (n+1)^(2n+4)).
    Damping coefficients (Γ = total A_upper): NIST / literature for n≤7,
    estimated from A(1s→np) with branching-ratio scaling for n≥8.

    References:
      - NIST ASD 5.11.1 (https://physics.nist.gov/ASD)
      - Drake & Morton (2007, ApJS 170, 251)
      - atomic_data_registry.json in data/processed/
    """
    def __init__(self):
        self.transitions = {
            # n=2  Lyα
            'HI_Lya':  (1215.6701, 0.416410, 6.265e8),
            # n=3  Lyβ
            'HI_Lyb':  (1025.7223, 0.079120, 1.897e8),
            # n=4  Lyγ
            'HI_Lyg':  (972.5368,  0.029000, 8.127e7),
            # n=5  Lyδ
            'HI_Lyd':  (949.7420,  0.013938, 4.591e7),
            # n=6  Lyε
            'HI_Lye':  (937.8010,  0.007799, 3.221e7),
            # n=7  Ly6 (Lyζ)
            'HI_Ly6':  (930.7483,  0.004814, 2.449e7),
            # n=8  Ly7 (Lyη)
            'HI_Ly7':  (926.2265,  0.003183, 2.100e7),
            # n=9  Ly8 (Lyθ)
            'HI_Ly8':  (923.1504,  0.002216, 1.832e7),
            # n=10 Ly9 (Lyι)
            'HI_Ly9':  (920.9731,  0.001605, 1.645e7),
            # n=11 Ly10 (Lyκ)
            'HI_Ly10': (919.3514,  0.001201, 1.507e7),
            # n=12 Ly11 (Lyλ)
            'HI_Ly11': (918.1294,  0.000921, 1.399e7),
            # n=13 Ly12 (Lyμ)
            'HI_Ly12': (917.1806,  0.000723, 1.311e7),
            # n=14 Ly13 (Lyν)
            'HI_Ly13': (916.4290,  0.000577, 1.238e7),
            # n=15 Ly14 (Lyξ)
            'HI_Ly14': (915.8240,  0.000469, 1.176e7),
            # n=22 Ly21 (high-n, needed for PKS1937 region 13)
            'HI_Ly21': (913.6510,  0.000148, 8.982e6),
        }
        self.transitions.update({
            'CII_1334': (1334.5323, 0.1278, 2.88e8),
            'CIII_977': (977.0201, 0.0762, 1.77e9),
            'CIV_1548': (1548.1950, 0.1899, 2.64e8),
            'CIV_1550': (1550.7700, 0.09475, 2.63e8),
            'SiIV_1393': (1393.7550, 0.5130, 8.80e8),
            'SiIV_1402': (1402.7700, 0.2550, 8.63e8),
        })

    def get(self, name):
        if name not in self.transitions:
            raise ValueError(f"Unknown transition: {name}")
        return self.transitions[name]


class RadiativeTransferEngine:
    """
    Evaluates physical multi-transition optical depth and constructs
    F(lambda) = Z(lambda) + C(lambda) * exp(-tau(lambda))

    Performance: caches convolution kernels and precomputed transition constants.
    """

    def __init__(self, z_abs):
        self.z_abs = z_abs
        self.atomic = AtomicData()
        self._kernel_cache = {}  # (id(wave), vsig) -> kernel
        self._trans_cache = {}   # transition name -> precomputed constants

    def _get_transition_constants(self, t_name):
        """Cache per-transition constants that never change."""
        if t_name not in self._trans_cache:
            lam_rest, f_osc, gamma = self.atomic.get(t_name)
            lam_rest_cm = lam_rest * 1e-8
            lam_obs_center = lam_rest * (1.0 + self.z_abs)
            self._trans_cache[t_name] = {
                'lam_rest': lam_rest,
                'f_osc': f_osc,
                'gamma': gamma,
                'lam_rest_cm': lam_rest_cm,
                'lam_obs_center': lam_obs_center,
            }
        return self._trans_cache[t_name]

    def compute_optical_depth(self, wave_obs, transitions_list, components):
        """
        Fully vectorized optical depth computation.
        All components processed simultaneously via broadcasting.

        Optimization: transitions whose observed wavelength (shifted by the
        component velocity range) falls far outside the block wavelength
        range are skipped entirely — their Voigt contribution is negligible
        (< 1e-30) at separations of many Doppler widths.  For typical Q1009
        data (50 blocks × 15 Lyman transitions, 43 H I components spanning
        v ~ -74000 to +50 km/s), only a small fraction of transition-block
        pairs actually overlap, so this saves the majority of wofz
        evaluations.
        """
        n_comps = len(components)
        if n_comps == 0:
            return np.zeros_like(wave_obs)

        # Extract component arrays once
        N_arr = np.array([c['N'] for c in components])  # (n_comps,)
        b_arr = np.array([c['b'] for c in components])  # (n_comps,)
        v_arr = np.array([c['v'] for c in components])  # (n_comps,)
        b_cgs_arr = b_arr * 1e5  # (n_comps,)

        n_pixels = len(wave_obs)
        tau_total = np.zeros(n_pixels)

        # Block wavelength bounds
        w_lo = wave_obs[0]
        w_hi = wave_obs[-1]

        # Compute the velocity range of the components.  The transition
        # wavelength for component i is lam_obs_center * (1 + v_i / c).
        # We need the full wavelength span across all components to test
        # overlap correctly.  The margin accounts for the Voigt wings:
        # at |delta_v| > 50 * b_max the profile is < 1e-500.
        v_min = v_arr.min()
        v_max = v_arr.max()
        b_max = b_arr.max()
        # Voigt wing margin: the Lorentzian damping wing can extend far
        # beyond the Gaussian core. Use a generous margin that accounts
        # for both Doppler and damping wings. For strong (damped) lines
        # the wing can contribute at hundreds of km/s. Use 5000 km/s as
        # a safe minimum, scaled up for large b values.
        _WING_MARGIN_KMS = max(100.0 * b_max, 5000.0)

        for t_name in transitions_list:
            tc = self._get_transition_constants(t_name)
            lam_rest_cm = tc['lam_rest_cm']
            lam_obs_center = tc['lam_obs_center']
            f_osc = tc['f_osc']
            gamma = tc['gamma']

            # Compute the wavelength range of this transition across all
            # components, including the Voigt wing margin.
            lam_c_min = lam_obs_center * (1.0 + v_min / c_kms)
            lam_c_max = lam_obs_center * (1.0 + v_max / c_kms)
            margin_ang = max(lam_c_min, lam_c_max) * _WING_MARGIN_KMS / c_kms

            # Skip if the transition's wavelength range (across all
            # components + wings) does not overlap the block range.
            if lam_c_max + margin_ang < w_lo or lam_c_min - margin_ang > w_hi:
                continue

            # lam_c for each component: (n_comps,)
            lam_c_arr = lam_obs_center * (1.0 + v_arr / c_kms)

            # delta_v: (n_comps, n_pixels) — broadcast
            # delta_v[i,j] = c * (wave[j] - lam_c[i]) / lam_c[i]
            delta_v = c_kms * (wave_obs[np.newaxis, :] - lam_c_arr[:, np.newaxis]) / lam_c_arr[:, np.newaxis]

            # x: (n_comps, n_pixels)
            x = delta_v / b_arr[:, np.newaxis]

            # a: (n_comps,) — one per component
            a_arr = (gamma * lam_rest_cm) / (4.0 * np.pi * b_cgs_arr)

            # Voigt: broadcast wofz over (n_comps, n_pixels)
            z = x + 1j * a_arr[:, np.newaxis]  # (n_comps, n_pixels)
            V = wofz(z).real  # (n_comps, n_pixels)

            # tau0: (n_comps,)
            tau0_arr = N_arr * f_osc * lam_rest_cm * (sigma_0 / b_cgs_arr)

            # Sum over components: (n_pixels,)
            tau_total += (tau0_arr[:, np.newaxis] * V).sum(axis=0)

        return tau_total

    def compute_optical_depth_split(self, wave_obs, transitions_list,
                                     fixed_components, free_components):
        """
        Compute optical depth with fixed and free components separately.
        fixed_components: precomputed tau contribution (cached).
        free_components: list of dicts computed fresh each call.
        Returns total tau = tau_fixed + tau_free.
        """
        tau_total = np.zeros_like(wave_obs)
        if fixed_components is not None:
            tau_total += fixed_components
        tau_total += self.compute_optical_depth(wave_obs, transitions_list, free_components)
        return tau_total

    def apply_continuum_and_zero(self, tau, wave, cont_params, zero_level):
        w_min, w_max = wave[0], wave[-1]
        if w_min == w_max:
            x_norm = np.zeros_like(wave)
        else:
            x_norm = 2.0 * (wave - w_min) / (w_max - w_min) - 1.0
        C = np.polynomial.chebyshev.chebval(x_norm, cont_params)
        return zero_level + C * np.exp(-tau)

    def _get_kernel(self, wave, sigma_kms):
        """Cache convolution kernel by wave array identity and sigma."""
        key = (id(wave), sigma_kms)
        if key not in self._kernel_cache:
            dv_kms = c_kms * np.median(np.diff(wave) / wave[:-1])
            if dv_kms <= 0 or sigma_kms <= 0:
                self._kernel_cache[key] = None
            else:
                n_pixels = int(np.ceil(5.0 * sigma_kms / dv_kms))
                v_grid = np.arange(-n_pixels, n_pixels + 1) * dv_kms
                kernel = np.exp(-0.5 * (v_grid / sigma_kms)**2)
                kernel /= np.sum(kernel)
                self._kernel_cache[key] = kernel
        return self._kernel_cache[key]

    def apply_convolution(self, flux, wave, sigma_kms):
        """Convolve with cached Gaussian kernel."""
        if sigma_kms <= 0:
            return flux
        kernel = self._get_kernel(wave, sigma_kms)
        if kernel is None:
            return flux
        # Use 'full' mode and crop to center so the output always matches
        # the input length, even when the kernel is wider than the data
        # (which can happen for short spectral blocks from overlapping
        # wavelength regions).
        full = np.convolve(flux, kernel, mode='full')
        start = (len(kernel) - 1) // 2
        return full[start:start + len(flux)]


if __name__ == '__main__':
    engine = RadiativeTransferEngine(z_abs=2.5042)
    wave = np.linspace(4250, 4270, 1000)
    components = [
        {'N': 10**17.36, 'b': 18.0, 'v': 0.0},
        {'N': 10**14.0, 'b': 12.0, 'v': -80.0},
    ]
    tau = engine.compute_optical_depth(wave, ['HI_Lya'], components)
    flux = engine.apply_continuum_and_zero(tau, wave, [1.0, 0.0, 0.0], 0.0)
    print(f"Max tau: {np.max(tau):.2f}")
    print(f"Min flux: {np.min(flux):.4f}")
