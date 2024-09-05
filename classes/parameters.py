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
        #self.fwhm = 0.0135 # FWHM in eV
        #
        #self.spectral_overlap = 0.17060418457226817 # ev-1 
        self.spectral_overlap = 0.028547827685680437
        #
        self.rescale_np_int = 100.0 # Rescale nanoparticle-acceptor interaction
        #sys.exit()
