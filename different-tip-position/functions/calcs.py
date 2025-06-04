import sys
import numpy as np

from classes import donor, acceptor, eet
# -------------------------------------------------------------------------------------
def eta_EET(n_pos,d_state,a_state,EET,D,A):
    #
    """Calculate Electronic Energy Transfer (EET) efficiency"""
    #
    eet_efficiency = (EET.Gamma_EET[n_pos,d_state,a_state]/
                      (EET.Gamma_EET[n_pos,d_state,a_state] + 
                       D.rad[n_pos,d_state] +
                       D.nonrad[n_pos,d_state] + 
                       D.nonrad_0))
    #
    return(eet_efficiency)
# -------------------------------------------------------------------------------------
def single_gaussian(energies,grid_points, exc, osc, fwhm, min_energy, max_energy):
    #
    """Define a Gaussian function to plot our calculated fluorescence peak"""
    #
    # Shape of the gaussian: f(x) = (1 / (σ * √(2π))) * exp(-((x - μ)^2) / (2σ^2))
    # (weighted by oscillator strength)

    # Calculate the standard deviation (sigma) from the FWHM
    sigma = fwhm / (2 * np.sqrt(2 * np.log(2)))

    # Calculate the Gaussian convolution
    gaussian = osc / (sigma * np.sqrt(2 * np.pi)) * np.exp(-((energies - exc) ** 2) / (2 * sigma**2))

    return gaussian
