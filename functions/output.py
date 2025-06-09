import sys
import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from matplotlib.ticker import ScalarFormatter, FuncFormatter
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
def plot_fluor_intensities(donor,acceptor,n_pos):
    #
    """ Plot fluorescence intensities of donor and acceptor"""

    # Define subplot titles
    positions = ['Position A', 'Position B', 'Position C']

    #
    # Define peaks at which simulated fluorescence intensities are centered
    # We consider the tip-perturbed excitation energies of the donor and acceptor
    donor_peak    = 2.16 # eV emission peak in experiment
    acceptor_peak = 2.05 # eV emission peak in experiment
    #
    min_energy = 1.99 # eV
    max_energy = 2.21 # eV
    #
    grid_points = 1000 # For the Gaussian functions
    #
    x_points = np.linspace(min_energy, max_energy, grid_points)
    #
    fontsize_tics   = 15
    fontsize_labels = 17
    fontsize_titles = 17
    #
    xlabel = 'Energy (eV)'
    ylabel = 'Fluorescence Intensity (arb. units)'

    # Adjust figure and subplots layout    
    fig, ax = plt.subplots(n_pos, 2, figsize=(8, 10))
    plt.subplots_adjust(left=0.12, hspace=0.4, wspace=0.3, top=0.9, bottom=0.08)

    for axes in ax.flat:
        axes.title.set_fontname('Times New Roman')
        axes.xaxis.label.set_fontname('Times New Roman')
        axes.yaxis.label.set_fontname('Times New Roman')
        axes.tick_params(axis='x', labelsize=fontsize_tics)  
        axes.tick_params(axis='y', labelsize=fontsize_tics)  
        for label in axes.get_xticklabels() + axes.get_yticklabels():
            label.set_fontname('Times New Roman')
    #
    plt.rcParams['font.family'] = 'Times New Roman'
    plt.rcParams['mathtext.fontset'] = 'custom'
    plt.rcParams['mathtext.rm'] = 'Times New Roman'
    plt.rcParams['mathtext.it'] = 'Times New Roman:italic'
    plt.rcParams['mathtext.bf'] = 'Times New Roman:bold'
    plt.rcParams['mathtext.sf'] = 'Times New Roman'
    plt.rcParams['mathtext.default'] = 'regular'

    
    # Add column titles
    fig.text(0.283, 0.96, 'Experiment', ha='center', va='center', fontsize=18, fontweight='bold', fontname='Times New Roman')
    fig.text(0.730, 0.96, 'Simulation', ha='center', va='center', fontsize=18, fontweight='bold', fontname='Times New Roman')

    # Set figure labels
    fig.supylabel(ylabel, fontsize=fontsize_labels, x=0.01)
    ax[-1][0].set_xlabel(xlabel, fontsize=fontsize_labels, labelpad=10.0)
    ax[-1][1].set_xlabel(xlabel, fontsize=fontsize_labels, labelpad=10.0)

    # Get the directory of this script to access the experimental data files
    base_dir = os.path.dirname(__file__)
    exp_files = [
        os.path.join(base_dir, "../data/experiment/exp-pos4.csv"),
        os.path.join(base_dir, "../data/experiment/exp-pos5.csv"),
        os.path.join(base_dir, "../data/experiment/exp-pos6.csv")
    ]

    # Load experimental data and find global max
    exp_data = []
    exp_global_max = 0
    for file in exp_files:
        try:
            df = pd.read_csv(file, delim_whitespace=True)
            energy = df.iloc[:,0].values
            intensity = df.iloc[:,1].values
            exp_data.append((energy, intensity))
            if np.max(intensity) > exp_global_max:
                exp_global_max = np.max(intensity)
        except Exception as e:
            error("Could not load {file}: {e}")
            
    # Normalize experimental data
    for i in range(len(exp_data)):
        exp_data[i] = (exp_data[i][0], exp_data[i][1] / exp_global_max)

    # Plot the normalized experimental values
    for n in range(3):
        # 
        # Plot
        ax[n][0].set_title(f'{positions[n]}',fontsize=fontsize_titles)
        ax[n][0].plot(exp_data[n][0],exp_data[n][1], color='red', label = '')

        if n == 0 or n == 1:
            ax[n][0].set_ylim(-.05, 1.05)
            ax[n][0].set_yticks(np.arange(0, 1.01, 0.25))

            # Add blue shaed area for the acceptor
            ax[n][0].axvspan(1.900, 1.907, ymin=0, ymax=1, color='blue', alpha=0.2)
        elif n == 2:
            ax[n][0].set_ylim(-0.01, 0.21)
            ax[n][0].set_yticks(np.arange(0, 0.201, 0.05))


    # For simulated data, check global normalization value
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

    # Plot the normalized simulated values
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
            
        # Set x-ticks, x-limits, y-limits and y-ticks as requested
        ax[n][1].set_xlim(1.98, 2.22)
        ax[n][1].set_xticks(np.arange(2.00, 2.21, 0.05))
        if n == 0 or n == 1:
            ax[n][1].set_ylim(-.05, 1.05)
            ax[n][1].set_yticks(np.arange(0, 1.01, 0.25))

        elif n == 2:
            ax[n][1].set_ylim(-.00035, 0.0045)
            ax[n][1].set_yticks(np.arange(0, 0.005, 0.001))
            ax[n][1].yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
            #ax[n][1].ticklabel_format(axis='y', style='sci', scilimits=(0,0))

        # Plot
        ax[n][1].set_title(f'{positions[n]}',fontsize=fontsize_titles)
        ax[n][1].plot(x_points,total_gaussian, color='red', label = '')
        #

    #plt.show()
    plt.savefig('fret_tip-position_experiment_vs_simulation.png')
