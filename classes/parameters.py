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
        self.fwhm =  0.021 # FWHM in eV for emission spectra
        #
        self.spectral_overlap = 0.02968170793445411
        #
        self.rescale_np_int = 1.0 # Rescale nanoparticle-acceptor interaction
        #sys.exit()
