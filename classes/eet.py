import numpy as np

class eet:
    #
    """EET class"""
    #
    def __init__(self,n_pos,n_states_D,n_states_A):
       #
       self.Gamma_EET = np.zeros((n_pos,n_states_D,n_states_A))
       self.eta_EET   = np.zeros((n_pos,n_states_D,n_states_A))