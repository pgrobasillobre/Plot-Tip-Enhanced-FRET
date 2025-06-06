import numpy as np
import sys

from classes import parameters

param = parameters.parameters()
# -------------------------------------------------------------------------------------
class donor:
    #
    """Donor class"""
    #
    def __init__(self,n_pos,donor_states):
        #
        self.rad    = np.zeros((n_pos,donor_states))
        self.nonrad = np.zeros((n_pos,donor_states))
        self.abs    = np.zeros((n_pos,donor_states))
        #
        self.FQY    = np.zeros((n_pos,donor_states))
        #
        rad_quantum_efficiency_vac = 5.0E-4 # Experimental Pt-Pc data approximated to that of Pd-Pc -- DOI: https://doi.org/10.1063/1.1676714
        #
        rad_0 = 1.0 / (0.9639E-08 * param.sec_to_au)  # au-1. Value in s from Amsterdam Modeling Suite vacuum TDDFT calculation
        #
        self.nonrad_0  = rad_0 / rad_quantum_efficiency_vac - rad_0
        #
        self.fluor_int = np.zeros((n_pos,donor_states))
        self.fluor_int_total = np.zeros(n_pos)
# -------------------------------------------------------------------------------------
