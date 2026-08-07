"""
Temporal Equivalence Principle (TEP) shear model implementation

Implements the TEP shear model that can mimic the deuterium isotope shift
through temporal variation of fundamental constants.
"""

import numpy as np
from scipy.integrate import quad
import json
from pathlib import Path

class TEPShearModel:
    """
    Temporal Equivalence Principle shear model.
    
    This model implements the temporal shear effect that can mimic
    the deuterium isotope shift through time-varying fundamental constants.
    """
    
    def __init__(self, alpha_variation_rate=1e-15, mu_variation_rate=1e-15):
        """
        Initialize TEP shear model.
        
        Parameters
        ----------
        alpha_variation_rate : float
            Rate of fine-structure constant variation (per year)
        mu_variation_rate : float
            Rate of proton-to-electron mass ratio variation (per year)
        """
        self.alpha_variation_rate = alpha_variation_rate
        self.mu_variation_rate = mu_variation_rate
        
        # Physical constants
        self.alpha_0 = 1/137.035999084  # Fine-structure constant
        self.mu_0 = 1836.15267343  # Proton-to-electron mass ratio
        
        # Deuterium properties
        self.deuterium_isotope_shift = 0.000082  # D/H isotope shift (fractional)
        self.lyman_alpha_wavelength = 1215.6699  # Lyman alpha wavelength (Å)
    
    def calculate_temporal_shear(self, time_years):
        """
        Calculate temporal shear factor.
        
        Parameters
        ----------
        time_years : float
            Time in years (can be positive or negative)
        
        Returns
        -------
        float
            Temporal shear factor
        """
        # Calculate variation in alpha and mu
        delta_alpha = self.alpha_variation_rate * time_years
        delta_mu = self.mu_variation_rate * time_years
        
        # Calculate shear factor
        # The shear factor depends on how the isotope shift scales with constants
        shear_factor = 1 + delta_alpha + delta_mu * 0.5
        
        return shear_factor
    
    def calculate_wavelength_shift(self, wavelength, time_years):
        """
        Calculate wavelength shift due to temporal shear.
        
        Parameters
        ----------
        wavelength : float
            Rest wavelength (Å)
        time_years : float
            Time in years
        
        Returns
        -------
        float
            Wavelength shift (Å)
        """
        shear_factor = self.calculate_temporal_shear(time_years)
        
        # Wavelength scales with shear factor
        shifted_wavelength = wavelength * shear_factor
        
        # Return the shift, not the shifted wavelength
        wavelength_shift = shifted_wavelength - wavelength
        
        return wavelength_shift
    
    def calculate_d_h_mimicry(self, time_years):
        """
        Calculate the time required for TEP shear to mimic D/H isotope shift.
        
        Parameters
        ----------
        time_years : float
            Time in years
        
        Returns
        -------
        dict
            Mimicry results
        """
        # Calculate wavelength shift for Lyman alpha
        wavelength_shift = self.calculate_wavelength_shift(
            self.lyman_alpha_wavelength,
            time_years
        )
        
        # Calculate fractional shift
        fractional_shift = wavelength_shift / self.lyman_alpha_wavelength
        
        # Compare to deuterium isotope shift
        mimicry_ratio = fractional_shift / self.deuterium_isotope_shift
        
        return {
            'time_years': time_years,
            'wavelength_shift': wavelength_shift,
            'fractional_shift': fractional_shift,
            'deuterium_isotope_shift': self.deuterium_isotope_shift,
            'mimicry_ratio': mimicry_ratio,
            'can_mimic': mimicry_ratio >= 1.0
        }
    
    def find_mimicry_time(self, target_shift=None):
        """
        Find the time required to achieve a target wavelength shift.
        
        Parameters
        ----------
        target_shift : float, optional
            Target fractional wavelength shift (default: deuterium isotope shift)
        
        Returns
        -------
        float
            Time in years
        """
        if target_shift is None:
            target_shift = self.deuterium_isotope_shift
        
        # Solve for time: target_shift = (alpha_rate + 0.5*mu_rate) * time
        total_rate = self.alpha_variation_rate + 0.5 * self.mu_variation_rate
        required_time = target_shift / total_rate
        
        return required_time
    
    def calculate_ln_a_variation(self, time_years):
        """
        Calculate variation in ln(A) due to temporal shear.
        
        This is the key quantity for TEP-BBN analysis: the change in
        the natural logarithm of the absorption line amplitude.
        
        Parameters
        ----------
        time_years : float
            Time in years
        
        Returns
        -------
        float
            Variation in ln(A)
        """
        # Calculate shear factor
        shear_factor = self.calculate_temporal_shear(time_years)
        
        # ln(A) variation scales with shear factor
        # This is the quantity that should be compared to D/H measurements
        delta_ln_a = np.log(shear_factor)
        
        return delta_ln_a
    
    def calculate_required_shear_for_d_h(self, dh_ratio):
        """
        Calculate the required shear to produce a given D/H ratio.
        
        Parameters
        ----------
        dh_ratio : float
            D/H ratio (e.g., 2.527e-5)
        
        Returns
        -------
        dict
            Required shear parameters
        """
        # The required ln(A) variation to mimic D/H
        # This is based on the relationship between D/H and absorption line amplitudes
        required_delta_ln_a = np.log(dh_ratio / 2.527e-5)  # Normalized to Cooke et al. value
        
        # Calculate required time
        total_rate = self.alpha_variation_rate + 0.5 * self.mu_variation_rate
        required_time = required_delta_ln_a / total_rate
        
        return {
            'dh_ratio': dh_ratio,
            'required_delta_ln_a': required_delta_ln_a,
            'required_time_years': required_time,
            'required_shear_factor': np.exp(required_delta_ln_a)
        }
    
    def generate_shear_model_spectrum(self, wavelength, flux, time_years):
        """
        Generate a spectrum with temporal shear applied.
        
        Parameters
        ----------
        wavelength : array
            Wavelength array (Å)
        flux : array
            Flux array (normalized)
        time_years : float
            Time in years
        
        Returns
        -------
        dict
            Sheared spectrum
        """
        # Calculate shear factor
        shear_factor = self.calculate_temporal_shear(time_years)
        
        # Apply wavelength shift
        sheared_wavelength = wavelength * shear_factor
        
        # Interpolate flux to new wavelength grid
        from scipy.interpolate import interp1d
        interp_func = interp1d(wavelength, flux, kind='linear', fill_value='extrapolate')
        sheared_flux = interp_func(sheared_wavelength)
        
        return {
            'wavelength': sheared_wavelength,
            'flux': sheared_flux,
            'shear_factor': shear_factor,
            'time_years': time_years
        }
    
    def compare_shear_to_deuterium(self, wavelength, flux, time_years):
        """
        Compare TEP shear model to deuterium absorption.
        
        Parameters
        ----------
        wavelength : array
            Wavelength array (Å)
        flux : array
            Flux array (normalized)
        time_years : float
            Time in years
        
        Returns
        -------
        dict
            Comparison results
        """
        # Generate sheared spectrum
        sheared_spectrum = self.generate_shear_model_spectrum(wavelength, flux, time_years)
        
        # Calculate wavelength shift
        wavelength_shift = sheared_spectrum['wavelength'] - wavelength
        
        # Calculate flux difference
        flux_difference = sheared_spectrum['flux'] - flux
        
        # Calculate chi-squared between sheared and original
        chi2 = np.sum(flux_difference**2)
        
        return {
            'shear_factor': sheared_spectrum['shear_factor'],
            'wavelength_shift': wavelength_shift,
            'flux_difference': flux_difference,
            'chi2': chi2,
            'can_mimic': self.calculate_d_h_mimicry(time_years)['can_mimic']
        }


def main():
    """Example usage of TEP shear model."""
    # Initialize model
    model = TEPShearModel()
    
    print("TEP Shear Model initialized")
    print(f"  Alpha variation rate: {model.alpha_variation_rate:.2e} /year")
    print(f"  Mu variation rate: {model.mu_variation_rate:.2e} /year")
    print()
    
    # Calculate mimicry time for deuterium isotope shift
    mimicry_time = model.find_mimicry_time()
    print(f"Time to mimic deuterium isotope shift: {mimicry_time:.2e} years")
    print()
    
    # Calculate ln(A) variation for different times
    times = [1e6, 1e7, 1e8, 1e9]
    print("ln(A) variation for different times:")
    for time in times:
        delta_ln_a = model.calculate_ln_a_variation(time)
        print(f"  {time:.0e} years: {delta_ln_a:.2e}")
    print()
    
    # Calculate required shear for typical D/H ratio
    dh_ratio = 2.527e-5
    required_shear = model.calculate_required_shear_for_d_h(dh_ratio)
    print(f"Required shear for D/H = {dh_ratio:.2e}:")
    print(f"  Required Δln(A): {required_shear['required_delta_ln_a']:.2e}")
    print(f"  Required time: {required_shear['required_time_years']:.2e} years")
    print()
    
    print("TEP shear model ready for analysis")


if __name__ == '__main__':
    main()
