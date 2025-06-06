import sys

class parameters:
    #
    """Parameters class"""
    #
    def __init__(self):
       #
        self.au_to_sec        = 2.418884254E-17
        self.sec_to_au        = 1.0 / self.au_to_sec
        #
        self.au_to_ev         = 27.211324570273
        self.ev_to_au         = 1.0 / self.au_to_ev
        #
        self.fwhm =  0.008 # FWHM in eV for emission spectra
        #
        self.spectral_overlap = 0.02968170793445411 # FretLab allows to introduce this as parameter but
                                                    # I have fixed it to "1" in order to add it within 
                                                    # this post-process
                                                    #
                                                    # Computed from experimental data of:
                                                    #    - Zn-Pc absorption
                                                    #    - Pt-Pc emission
                                                    #
                                                    # Reference paper: https://doi.org/10.1038/s41565-022-01142-z
                                                    #
                                                    # Spectral Overlap code: https://github.com/pgrobasillobre/SpectralOverlap
