import numpy as np
import os
import sys

from classes import donor, acceptor, eet, parameters
from functions import read_outputs, output, calcs

# ---------------------------------------------------- #
# ---------------------- INPUTS ---------------------- #
#
results_folder = '/home/pablo/Dropbox/posdoc/fret/tip-transfer/kong/tip-min1-mols/fig-1d/calc/fret-2.5_ev/results'
#
positions = ['pos-4', 'pos-5', 'pos-6'] # These positions are related with fig-1d of the paper: https://doi.org/10.1038/s41565-022-01142-z
#
n_states_donor   = 2
n_states_acceptor = 2
#
# ---------------------------------------------------- #
#
# ==================================================== #
# ===================== PROGRAM ====================== #
#
# -------------------- Initialize -------------------- #
param = parameters.parameters()
#
donor   = donor.donor(len(positions),n_states_donor)
acceptor = acceptor.acceptor(len(positions),n_states_acceptor,n_states_donor)
#
eet = eet.eet(len(positions),n_states_donor,n_states_acceptor)
# ---------------------------------------------------- #
#
# -- Read donor TDDFT characteristics (modified A-D position)
n_pos = 0
for position in positions:
    #
    for d_state in range(n_states_donor):
        #
        results_folder_donor = results_folder + '/tddft/pt-pc/state-' + str(d_state+1) + '/' + str(position) + '/pt-pc_cam-b3lyp_tzp.log'
        #
        donor.abs[n_pos,d_state], donor.rad[n_pos,d_state], donor.nonrad[n_pos,d_state] = read_outputs.extract_tddft(results_folder_donor,labs=True,lrad=True,lnonrad=True)
        #
    n_pos += 1
#
# -- Read acceptor TDDFT characteristics (modified A-D position)
n_pos = 0
for position in positions:
    #
    for a_state in range(n_states_acceptor):
        #
        results_folder_acceptor = results_folder + '/tddft/zn-pc/state-' + str(a_state+1) + '/' + str(position) + '/zn-pc_cam-b3lyp_tzp.log'
        #
        acceptor.abs[n_pos,a_state], acceptor.rad[n_pos,a_state], acceptor.nonrad[n_pos,a_state] = read_outputs.extract_tddft(results_folder_acceptor,labs=True,lrad=True,lnonrad=True)
        #
        acceptor.fluorescence_quantum_yield(n_pos,a_state)
        #
    n_pos += 1
#
# --- Read EET and calculate accumulative values for
#     each state-D to state-A combination at each A-D position
#
n_pos = 0
#
for position in positions:
    #
    for d_state in range(n_states_donor):
        #
        eta_sum = 0.0
        gamma_eet_sum = 0.0
        eet_times_fqy_sum = 0.0
        for a_state in range(n_states_acceptor):
            #
            results_folder_eet = results_folder + '/fret/D_state-' + str(d_state+1) + '_to_A_state-' + str(a_state+1) + '/' + position + '/input.log'
            #
            # EET quantities
            eet.Gamma_EET[n_pos,d_state,a_state] = read_outputs.extract_eet(results_folder_eet)
            eet.eta_EET[n_pos,d_state,a_state] = calcs.eta_EET(n_pos,d_state,a_state,eet,donor,acceptor)
            #
            gamma_eet_sum = gamma_eet_sum + eet.Gamma_EET[n_pos,d_state,a_state]
            eet_times_fqy_sum = eet_times_fqy_sum + eet.eta_EET[n_pos,d_state,a_state] * acceptor.FQY[n_pos,a_state]
            #
            # This is to check we don't have RET efficiency > 100%
            eta_sum = eta_sum + eet.eta_EET[n_pos,d_state,a_state]
            #
            if (eta_sum > 1.0): 
               output.error('charge transfer efficiency higher than 100%') 
               sys.exit() 

        #
        # Fluorescence intensities calculation
        #
        donor.fluor_int[n_pos,d_state] = donor.abs[n_pos,d_state] * (donor.rad[n_pos,d_state] /
                                                                    (gamma_eet_sum +
                                                                     donor.nonrad[n_pos,d_state] +
                                                                     donor.rad[n_pos,d_state] +
                                                                     donor.nonrad_0))

        acceptor.fluor_int[n_pos,d_state] = donor.abs[n_pos,d_state] * eet_times_fqy_sum

    #
    # Total donor/acceptor intensity as sum of all intensities of
    # degenerated excited states for each distance
    donor.fluor_int_total[n_pos] = np.sum(donor.fluor_int[n_pos,:])
    acceptor.fluor_int_total[n_pos] = np.sum(acceptor.fluor_int[n_pos,:])
    #
    n_pos += 1

# Plot normalized tip-mediated fluorescence Acceptor-Donor intensities
output.plot_fluor_intensities(donor,acceptor,len(positions))


