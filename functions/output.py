import sys
import numpy as np
import matplotlib.pyplot as plt

from classes import aceptor, donor, parameters
from functions import calcs

param = parameters.parameters()
# -------------------------------------------------------------------------------------
def error(error_message):
    print("")
    print("")
    print("   " + error_message)
    print("")
    print("")
    sys.exit()
# -------------------------------------------------------------------------------------
def plot_fluor_intensities(donor,aceptor,n_pos):
    #
    """ Plot fluorescence intensities of donor and aceptor"""
    #
    # Define plotting options
    donor_peak   = 1.945 # eV emission peak
    aceptor_peak = 1.902 # eV emission peak
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
    
    # Plot the values
    for n in range(n_pos):
        #
        # Set limits
        ax[n].set_xlim(min_energy,max_energy+0.001)
        ax[n].set_ylim(0.0,1.0 + 0.1)
        #
        ax[n].set_xticks(np.arange(min_energy,max_energy+0.001,0.2))
        ax[n].set_yticks(np.arange(0.0,1.1,0.5))
        #
        # Create Gaussian functions for plotting the fluorescence intensities
        donor_gaussian   = calcs.single_gaussian(x_points,grid_points,donor_peak,donor.fluor_int_total[n],    param.fwhm,min_energy,max_energy)
        aceptor_gaussian = calcs.single_gaussian(x_points,grid_points,aceptor_peak,aceptor.fluor_int_total[n],param.fwhm,min_energy,max_energy)
        #
        # Create total Gaussian and normalize
        total_gaussian = donor_gaussian + aceptor_gaussian
        #
        norm = np.max(total_gaussian)
        #
        total_gaussian = total_gaussian/norm
        # 
        # Plot
        ax[n].set_title(f'pos-{n}')
        ax[n].plot(x_points,total_gaussian, color='red', label = '')
        #

    #
    plt.show()
    #plt.savefig('/home/pablo/Desktop/plot.png')
