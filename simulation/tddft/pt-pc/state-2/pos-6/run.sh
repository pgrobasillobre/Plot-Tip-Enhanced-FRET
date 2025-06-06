#!/bin/bash
#PBS -l select=1:ncpus=96:mpiprocs=96:mem=400GB -q q14aurora -N 1-Pt-Pc
#######################################################################
                 ## LOAD MODULES + PREPARE SCRATCH##
#######################################################################
module load gcc/8.3.0 blas-lapack/gcc-8.3.0/3.9.0 intel/mkl/2020/2.254 intel/mpi/2019.8.254
source /home/pgrobasillobre/qm_bem/amsbashrc.sh
export SCM_TMPDIR=/scratch/${USER}



#######################################################################
              ## MODIFY HERE THE NAME OF THE FOLDERS ##
#######################################################################

contodir=pos-6
dovesono=/home/pgrobasillobre/calc/fret/tip-transfer/kong/tip-mols/fig-1d/freq-2.5_ev/tip-d5.0_angs/pt-pc/state-2
cd "${dovesono}"

if [[ ! -d "/scratch/${USER}" ]] ; then mkdir -p "/scratch/${USER}" ; fi
#
if [[ -d "/scratch/${USER}/${contodir}" ]]; then rm -rf -- "/scratch/${USER}/${contodir}" ; fi
cp -r "${contodir}" /scratch/${USER}/ || exit 1
cd "/scratch/${USER}/${contodir}" || exit 1

## MODIFY EXECUTABLE NAME 
   ./pt-pc_cam-b3lyp_tzp.run > pt-pc_cam-b3lyp_tzp.log

rm -rf ams.results

cd .. 

rsync -avz ${contodir}/ ${dovesono}/${contodir}
rm -r -- "${contodir}"

exit 0
# finished
