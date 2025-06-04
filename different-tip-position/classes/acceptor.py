import numpy as np

from classes import parameters

param = parameters.parameters()
# -------------------------------------------------------------------------------------
class acceptor:
    #
    """Acceptor class"""
    #
    def __init__(self,n_pos,acceptor_states,donor_states):
        #
        self.rad    = np.zeros((n_pos,acceptor_states))
        self.nonrad = np.zeros((n_pos,acceptor_states))
        self.abs    = np.zeros((n_pos,acceptor_states))
        #    
        #
        self.FQY    = np.zeros((n_pos,acceptor_states))    
        #
        rad_quantum_efficiency_vac = 0.3 # <= to that value For Zn-Pc 
                                            # as given in DOI: https://doi.org/10.1063/1.1676714
        #
        rad_0 = 1.0 / (0.1087E-07 * param.sec_to_au)  # au-1. Value in s from Amsterdam Modeling Suite vacuum TDDFT calculation
        #
        self.nonrad_0  = rad_0 / rad_quantum_efficiency_vac - rad_0
        #
        self.fluor_int = np.zeros((n_pos,donor_states))
        self.fluor_int_total = np.zeros(n_pos)
    # ---------------------------------------------------------------------------------
    def fluorescence_quantum_yield(self,n_pos,n_state):
        #
        """ Calculate fluorescence quantum yield for a given state"""
        #
        self.FQY[n_pos,n_state] = self.rad[n_pos,n_state] / (
                                    self.rad[n_pos,n_state] + 
                                    self.nonrad[n_pos,n_state] +
                                    self.nonrad_0)
# -------------------------------------------------------------------------------------

