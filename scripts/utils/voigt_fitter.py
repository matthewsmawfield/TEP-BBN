"""
Voigt profile fitting for TEP-BBN

Implements Voigt profile fitting for H I and D I Lyman series lines
using atomic data from NIST ASD.
"""

import numpy as np
from scipy.special import wofz
from scipy.optimize import curve_fit
import json
from pathlib import Path
import sys

class VoigtFitter:
    """
    Voigt profile fitter for absorption lines.
    
    Uses atomic data from NIST ASD for line parameters.
    """
    
    def __init__(self, atomic_data_path=None):
        """
        Initialize Voigt fitter with atomic data.
        
        Parameters
        ----------
        atomic_data_path : str, optional
            Path to atomic data registry. If None, uses default project path.
        """
        if atomic_data_path is None:
            # Get project root directory
            script_dir = Path(__file__).parent
            project_root = script_dir.parent
            atomic_data_path = project_root / 'data/processed/atomic_data_registry.json'
        self.atomic_data_path = Path(atomic_data_path)
        self.atomic_data = self.load_atomic_data()
        self.lines = self.parse_atomic_data()
    
    def load_atomic_data(self):
        """Load atomic data from registry."""
        with open(self.atomic_data_path, 'r') as f:
            return json.load(f)
    
    def parse_atomic_data(self):
        """Parse atomic data into line parameters."""
        lines = {}
        
        for element_key, element_data in self.atomic_data['data'].items():
            if element_data['status'] in ['real_data', 'partial_data']:
                file_path = Path(element_data['file'])
                if file_path.exists():
                    with open(file_path, 'r') as f:
                        content = f.read()
                    
                    # Parse atomic data file
                    element_lines = []
                    for line in content.split('\n'):
                        if line.startswith('#') or line.strip() == '':
                            continue
                        
                        parts = line.split()
                        if len(parts) >= 2:
                            wavelength = float(parts[0])
                            oscillator_strength = parts[1] if parts[1] != 'N/A' else None
                            transition = parts[2] if len(parts) > 2 else 'unknown'
                            
                            element_lines.append({
                                'wavelength': wavelength,
                                'oscillator_strength': oscillator_strength,
                                'transition': transition
                            })
                    
                    lines[element_key] = element_lines
        
        return lines
    
    def voigt_profile(self, x, x0, sigma, gamma, amplitude):
        """
        Voigt profile function.
        
        Parameters
        ----------
        x : array
            Wavelength or velocity array
        x0 : float
            Line center
        sigma : float
            Gaussian width (thermal broadening)
        gamma : float
            Lorentzian width (natural + pressure broadening)
        amplitude : float
            Line amplitude (optical depth)
        
        Returns
        -------
        array
            Voigt profile
        """
        # Convert to dimensionless variables
        z = (x - x0 + 1j*gamma) / (sigma * np.sqrt(2))
        
        # Voigt function
        v = amplitude * np.real(wofz(z))
        
        return v
    
    def voigt_profile_multi(self, x, parameters, line_list):
        """
        Multi-component Voigt profile.
        
        Parameters
        ----------
        x : array
            Wavelength or velocity array
        parameters : array
            Fitting parameters [x0_1, sigma_1, gamma_1, amp_1, x0_2, sigma_2, gamma_2, amp_2, ...]
        line_list : list
            List of line parameters
        
        Returns
        -------
        array
            Multi-component Voigt profile
        """
        profile = np.zeros_like(x)
        
        for i in range(len(line_list)):
            x0 = parameters[4*i]
            sigma = parameters[4*i + 1]
            gamma = parameters[4*i + 2]
            amplitude = parameters[4*i + 3]
            
            profile += self.voigt_profile(x, x0, sigma, gamma, amplitude)
        
        return profile
    
    def fit_single_line(self, wavelength, flux, line_wavelength, initial_params=None):
        """
        Fit a single absorption line.
        
        Parameters
        ----------
        wavelength : array
            Wavelength array (Å)
        flux : array
            Flux array (normalized)
        line_wavelength : float
            Central wavelength of the line (Å)
        initial_params : array, optional
            Initial parameters [x0, sigma, gamma, amplitude]
        
        Returns
        -------
        dict
            Fitting results
        """
        # Convert to optical depth
        optical_depth = -np.log(flux)
        
        # Initial parameters
        if initial_params is None:
            initial_params = [
                line_wavelength,  # x0 (line center)
                0.1,  # sigma (Gaussian width)
                0.01,  # gamma (Lorentzian width)
                0.5  # amplitude (optical depth)
            ]
        
        # Parameter bounds
        bounds = (
            [line_wavelength - 1.0, 0.01, 0.001, 0.0],  # Lower bounds
            [line_wavelength + 1.0, 1.0, 0.1, 2.0]  # Upper bounds
        )
        
        # Fit
        try:
            popt, pcov = curve_fit(
                self.voigt_profile,
                wavelength,
                optical_depth,
                p0=initial_params,
                bounds=bounds
            )
            
            # Calculate errors
            perr = np.sqrt(np.diag(pcov))
            
            # Calculate fitted profile
            fitted_profile = self.voigt_profile(wavelength, *popt)
            fitted_flux = np.exp(-fitted_profile)
            
            # Calculate chi-squared
            residuals = flux - fitted_flux
            chi2 = np.sum(residuals**2)
            
            return {
                'success': True,
                'parameters': {
                    'x0': popt[0],
                    'sigma': popt[1],
                    'gamma': popt[2],
                    'amplitude': popt[3]
                },
                'errors': {
                    'x0': perr[0],
                    'sigma': perr[1],
                    'gamma': perr[2],
                    'amplitude': perr[3]
                },
                'fitted_flux': fitted_flux,
                'chi2': chi2,
                'dof': len(wavelength) - 4
            }
        
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def fit_lyman_series(self, wavelength, flux, redshift, element='H_I'):
        """
        Fit Lyman series lines for H I or D I.
        
        Parameters
        ----------
        wavelength : array
            Wavelength array (Å)
        flux : array
            Flux array (normalized)
        redshift : float
            Redshift of the absorber
        element : str
            Element to fit ('H_I' or 'D_I')
        
        Returns
        -------
        dict
            Fitting results for all Lyman series lines
        """
        if element not in self.lines:
            return {
                'success': False,
                'error': f'Element {element} not found in atomic data'
            }
        
        # Get Lyman series lines for this element
        lyman_lines = [line for line in self.lines[element] 
                      if 'Ly' in line['transition']]
        
        if len(lyman_lines) == 0:
            return {
                'success': False,
                'error': f'No Lyman series lines found for {element}'
            }
        
        results = {}
        
        for line in lyman_lines:
            # Calculate observed wavelength
            observed_wavelength = line['wavelength'] * (1 + redshift)
            
            # Check if line is in wavelength range
            if (observed_wavelength >= wavelength.min() and 
                observed_wavelength <= wavelength.max()):
                
                # Fit the line
                line_result = self.fit_single_line(
                    wavelength,
                    flux,
                    observed_wavelength
                )
                
                results[line['transition']] = {
                    'rest_wavelength': line['wavelength'],
                    'observed_wavelength': observed_wavelength,
                    'oscillator_strength': line['oscillator_strength'],
                    'fit_result': line_result
                }
        
        return {
            'success': True,
            'element': element,
            'redshift': redshift,
            'n_lines_fitted': len(results),
            'lines': results
        }
    
    def fit_d_h_system(self, wavelength, flux, redshift):
        """
        Fit both H I and D I Lyman series lines simultaneously.
        
        Parameters
        ----------
        wavelength : array
            Wavelength array (Å)
        flux : array
            Flux array (normalized)
        redshift : float
            Redshift of the absorber
        
        Returns
        -------
        dict
            Fitting results for H I and D I
        """
        # Fit H I
        h_i_results = self.fit_lyman_series(wavelength, flux, redshift, 'H_I')
        
        # Fit D I
        d_i_results = self.fit_lyman_series(wavelength, flux, redshift, 'D_I')
        
        return {
            'H_I': h_i_results,
            'D_I': d_i_results
        }
    
    def calculate_column_density(self, fit_result, oscillator_strength):
        """
        Calculate column density from Voigt fit.
        
        Parameters
        ----------
        fit_result : dict
            Fitting result from fit_single_line
        oscillator_strength : float
            Oscillator strength of the line
        
        Returns
        -------
        float
            Column density (cm^-2)
        """
        if not fit_result['success']:
            return None
        
        # Extract parameters
        amplitude = fit_result['parameters']['amplitude']
        sigma = fit_result['parameters']['sigma']
        
        # Calculate equivalent width
        # EW = amplitude * sigma * sqrt(2*pi)
        equivalent_width = amplitude * sigma * np.sqrt(2 * np.pi)
        
        # Calculate column density
        # N = (1.13e17 * EW) / (f * lambda^2)
        # where EW is in mÅ, f is oscillator strength, lambda is in Å
        if oscillator_strength is None or oscillator_strength == 'N/A':
            return None
        
        # Convert equivalent width to mÅ
        ew_mA = equivalent_width * 1000
        
        # Column density calculation
        column_density = (1.13e17 * ew_mA) / (float(oscillator_strength) * fit_result['parameters']['x0']**2)
        
        return column_density


def main():
    """Example usage of Voigt fitter."""
    # Initialize fitter
    fitter = VoigtFitter()
    
    # Print available lines
    print("Available atomic lines:")
    for element, lines in fitter.lines.items():
        print(f"  {element}: {len(lines)} lines")
        for line in lines[:3]:  # Show first 3 lines
            print(f"    {line['transition']}: {line['wavelength']} Å")
        if len(lines) > 3:
            print(f"    ... and {len(lines) - 3} more")
    
    print()
    print("Voigt fitter initialized successfully")
    print("Ready for fitting reduced spectra")


if __name__ == '__main__':
    main()
