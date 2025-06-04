import sys
import numpy as np
import matplotlib.pyplot as plt

from classes import acceptor, donor, parameters
from functions import calcs

param = parameters.parameters()
# -------------------------------------------------------------------------------------
def error(error_message):
    print("")
    print("")
    print("   ERROR: " + error_message)
    print("")
    print("")
    sys.exit()
# -------------------------------------------------------------------------------------
def plot_fluor_intensities(donor,acceptor,n_pos,positions):
    #
    """ Plot fluorescence intensities of donor and acceptor"""
    #
    # Define plotting options
    donor_peak    = 1.945 # eV emission peak in experiment
    acceptor_peak = 1.902 # eV emission peak in experiment
    #
    min_energy = 1.85 # eV
    max_energy = 2.00 # eV
    #
    grid_points = 1000 # For the Gaussian functions
    #
    x_points = np.linspace(min_energy, max_energy, grid_points)
    #n
    fig, ax = plt.subplots(n_pos, 1, figsize=(4, 9))
    #
    xlabel = 'Incident Photon Frequency (eV)'
    ylabel = 'Normalized Fluorescence Intensity (arb. units)'
    #
    plt.rcParams['font.family'] = 'Times New Roman'
    plt.rcParams['mathtext.fontset'] = 'custom'
    plt.rcParams['mathtext.rm'] = 'Times New Roman'
    plt.rcParams['mathtext.it'] = 'Times New Roman:italic'
    plt.rcParams['mathtext.bf'] = 'Times New Roman:bold'
    plt.rcParams['mathtext.sf'] = 'Times New Roman'
    plt.rcParams['mathtext.default'] = 'regular'

    fontsize_axes   = 13
    fontsize_labels = 15
    fontsize_text   = 20

    ax[-1].set_xlabel(xlabel, fontsize=fontsize_labels, labelpad=10.0)
    
    # Check global normalization value
    norm = 0
    for n in range(n_pos):
        #
        # Create Gaussian functions for plotting the fluorescence intensities
        donor_gaussian   = calcs.single_gaussian(x_points,grid_points,donor_peak,donor.fluor_int_total[n],    param.fwhm,min_energy,max_energy)
        acceptor_gaussian = calcs.single_gaussian(x_points,grid_points,acceptor_peak,acceptor.fluor_int_total[n],param.fwhm,min_energy,max_energy)
        #
        # Create total Gaussian and normalize
        total_gaussian = donor_gaussian + acceptor_gaussian
        #
        if np.max(total_gaussian) > norm: norm = np.max(total_gaussian)

    # Plot the values
    for n in range(n_pos):
        #
        # Create Gaussian functions for plotting the fluorescence intensities
        donor_gaussian   = calcs.single_gaussian(x_points,grid_points,donor_peak,donor.fluor_int_total[n],    param.fwhm,min_energy,max_energy)
        acceptor_gaussian = calcs.single_gaussian(x_points,grid_points,acceptor_peak,acceptor.fluor_int_total[n],param.fwhm,min_energy,max_energy)
        #
        # Create total Gaussian and normalize
        total_gaussian = donor_gaussian + acceptor_gaussian
        #
        total_gaussian = total_gaussian/norm
        # 
        # Plot
        ax[n].set_title(f'{positions[n]}')
        ax[n].plot(x_points,total_gaussian, color='red', label = '')
        #

    plt.show()
