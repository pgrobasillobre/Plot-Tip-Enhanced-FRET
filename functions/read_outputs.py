import sys
import os
import numpy as np

from classes import parameters
from functions import output
# -------------------------------------------------------------------------------------
param  = parameters.parameters()
# -------------------------------------------------------------------------------------
def extract_tddft(infile,labs=False,lrad=False,lnonrad=False):
    #
    """ Extract \Gamma_{text{rad}} and/or \Gamma_{text{nonrad}} from ADF output"""
    #
    # Check that file exists
    if not os.path.exists(infile): output.error("File " + infile + " not found")
    #
    found_abs    = False
    found_rad    = False
    found_nonrad = False
    #
    with open(infile,'r') as f:
        for line in f:
            if line.startswith(' absorption coefficient:'):
                found_abs = True
                abs = float(line.split()[2])
            if line.startswith(' radiative decay:'):
                found_rad = True
                rad = float(line.split()[2]) # s-1 (decay rate)
                rad = 1.0/rad # s (lifetime)
                rad = rad * param.sec_to_au #a.u. (lifetime)
                rad = 1.0/rad # a.u.-1 (decay rate)

            if line.startswith(' nonradiative decay:'):
                found_nonrad = True 
                nonrad = float(line.split()[2]) # s-1 (decay rate)
                nonrad = 1.0/nonrad # s (lifetime)
                nonrad = nonrad * param.sec_to_au # a.u. (lifetime)
                nonrad = 1.0/nonrad # a.u. -1 (decay rate)
                
    # 
    if (labs and not found_abs): output.error("Absorption coefficient not found for file" + infile)
    if (lrad and not found_rad): output.error("Radiative decay not found for file " + infile)
    if (lnonrad and not found_nonrad): output.error("Non radiative decay not found for file " + infile)
    #
    if (lrad and lnonrad and labs):
        return(abs,rad,nonrad)
    elif (lrad and lnonrad and not labs): 
        return(rad,nonrad)
    elif (lrad and not lnonrad and not labs):
        return(rad)
    elif (lnonrad and not lrad and not labs):
        return(nonrad)
    else:
        output.error("Case extract abs=" + str(labs) + ' rad=' + str(lrad) + ' nonrad=' + str(lnonrad) + 'not supported')
# -------------------------------------------------------------------------------------
def extract_eet(infile):
    #
    """ Extract A-D coulomb and A-NP interactions from FRET_Embedlab output"""
    #
    # Check that file exists
    if not os.path.exists(infile): output.error("File " + infile + " not found")
    #
    found_a_d_int  = False
    found_a_np_int = False
    #
    with open(infile,'r') as f:
        for line in f:
            if line.startswith('     Aceptor-Donor Coulomb :'):
                found_a_d_int = True
                a_d_int = complex(float(line.split()[3]),0.0)
            if line.startswith('     Aceptor-NP Interaction:'):
                found_a_np_int = True
                a_np_int = complex(float(line.split()[2]),float(line.split()[4]))
    #
    if not found_a_d_int and not found_a_np_int: output.error("A-D coulombd and A-NP interactions not found in " + infile)
    if not found_a_d_int:  output.error("A-D coulomb interaction not found in " + infile)
    if not found_a_np_int: output.error("A-NP interaction not found in " + infile)
    #
    v_tot = (a_d_int + a_np_int*param.rescale_np_int) * param.au_to_ev # In eV
    v_mod2 = (np.abs(v_tot))**2.0 # np.abs calculates the modulus of the complex number
    #
    gamma_eet = 2.0 * np.pi * (v_mod2 * param.spectral_overlap) * param.ev_to_au # In a.u.
    #
    return(gamma_eet)





