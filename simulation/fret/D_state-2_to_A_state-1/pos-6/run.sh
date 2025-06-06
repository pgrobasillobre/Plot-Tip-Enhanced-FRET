#!/bin/bash
#PBS -l select=1:ncpus=28:mpiprocs=28:mem=100GB -q q07diamond -N fret
#######################################################################
                 ## LOAD MODULES + PREPARE SCRATCH##
#######################################################################
module load gcc/9.3.0 blas-lapack/gcc-9.3.0/3.9.0 intel/mkl/2020/2.254 intel/mpi/2019.8.254
source /home/pgrobasillobre/qm_bem/adfbashrc.sh
export scm_tmpdir=/scratch/${USER}



#######################################################################
              ## MODIFY HERE THE NAME OF THE FOLDERS ##
#######################################################################

contodir=pos-6
dovesono=/home/pgrobasillobre/calc/fret/tip-transfer/kong/tip-mols/fig-1d/freq-2.5_ev/tip-d5.0_angs/fret/D_state-2_to_A_state-1
cd "${dovesono}"

if [[ ! -d "/scratch/${USER}" ]] ; then mkdir -p "/scratch/${USER}" ; fi
#
if [[ -d "/scratch/${USER}/${contodir}" ]]; then rm -rf -- "/scratch/${USER}/${contodir}" ; fi
cp -r "${contodir}" /scratch/${USER}/ || exit 1
cd "/scratch/${USER}/${contodir}" || exit 1

## MODIFY EXECUTABLE NAME 
/home/pgrobasillobre/programs/fret_embedlab_fortran/build/FRET_Embedlab input.inp


cd .. 

rsync -avz ${contodir}/ ${dovesono}/${contodir}
rm -r -- "${contodir}"

exit 0
# finished
