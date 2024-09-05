
import numpy as np
import os
import sys

from classes import donor, aceptor, eet, parameters
from functions import read_outputs, output, calcs

# ---------------------------------------------------- #
# ---------------------- INPUTS ---------------------- #
results_folder = '/home/pablo/Dropbox/3rd-year/research/sveva-fret/calc/paper/kong/wfqfmubem/results/stm-d20/mol-tip-d5.0/donor-2.914-aceptor-2.869_ev/results'
#
positions = ['pos-1', 'pos-4', 'pos-6']
#
n_states_donor   = 2
n_states_aceptor = 2
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
aceptor = aceptor.aceptor(len(positions),n_states_aceptor,n_states_donor)
#
eet = eet.eet(len(positions),n_states_donor,n_states_aceptor)
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
# -- Read aceptor TDDFT characteristics (modified A-D position)
n_pos = 0
for position in positions:
    #
    for a_state in range(n_states_aceptor):
        #
        results_folder_aceptor = results_folder + '/tddft/zn-pc/state-' + str(a_state+1) + '/' + str(position) + '/zn-pc_cam-b3lyp_tzp.log'
        #
        aceptor.abs[n_pos,a_state], aceptor.rad[n_pos,a_state], aceptor.nonrad[n_pos,a_state] = read_outputs.extract_tddft(results_folder_aceptor,labs=True,lrad=True,lnonrad=True)
        #
        aceptor.fluorescence_quantum_yield(n_pos,a_state)
        #
    n_pos += 1
    #
#
# --- Read EET and calculate accumulative values for
#     each state-D to state-A combination at each A-D position
n_pos = 0
for position in positions:
    #
    for d_state in range(n_states_donor):
        #
        eta_sum = 0.0
        gamma_eet_sum = 0.0
        eet_times_fqy_sum = 0.0
        for a_state in range(n_states_aceptor):
            #
            results_folder_eet = results_folder + '/fret/D_state-' + str(d_state+1) + '_to_A_state-' + str(a_state+1) + '/' + position + '/input.log'
            #
            # EET quantities
            eet.Gamma_EET[n_pos,d_state,a_state] = read_outputs.extract_eet(results_folder_eet)
            eet.eta_EET[n_pos,d_state,a_state] = calcs.eta_EET(n_pos,d_state,a_state,eet,donor,aceptor)
            #
            gamma_eet_sum = gamma_eet_sum + eet.Gamma_EET[n_pos,d_state,a_state]
            eta_sum = eta_sum + eet.eta_EET[n_pos,d_state,a_state]
            #
            #if (eta_sum > 1.0): sys.exit() # Avoid sum of eta bigger than 1
            #
            eet_times_fqy_sum = eet_times_fqy_sum + eet.eta_EET[n_pos,d_state,a_state]* aceptor.FQY[n_pos,a_state]
            #
        # Fluorescence intensities
        # 
        #debugpgi set limit
        #
        donor.fluor_int[n_pos,d_state] = donor.fluor_int[n_pos,d_state] + donor.abs[n_pos,d_state] * (donor.rad[n_pos,d_state] / 
                                                                                                      (gamma_eet_sum + 
                                                                                                       donor.nonrad[n_pos,d_state] + 
                                                                                                       donor.rad[n_pos,d_state] +
                                                                                                       donor.nonrad_0))
        #
        aceptor.fluor_int[n_pos,d_state] = donor.abs[n_pos,d_state] * eet_times_fqy_sum
        #
        
    #
    # Total donor/aceptor intensity as sum of all intensities of
    # degenerated excited states for each position
    donor.fluor_int_total[n_pos] = np.sum(donor.fluor_int[n_pos,:])
    aceptor.fluor_int_total[n_pos] = np.sum(aceptor.fluor_int[n_pos,:])
    #
    n_pos += 1
#
#
# -- Plot fluorescence Aceptor-Donor intensities
output.plot_fluor_intensities(donor,aceptor,len(positions),positions)



