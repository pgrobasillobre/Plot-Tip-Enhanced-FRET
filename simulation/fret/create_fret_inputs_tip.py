import sys
import os
import glob



a_index = [42,56] # These are the atoms for which state-1 and state-2 transition dipoles must be aligned
d_index = [28,42]


# -----------------------------------------------
def read_transdip(file_name,state):

   found_transdip = False
   found_sticks   = False
   end_read       = False

   transdip = []
   with open(file_name, 'r') as f:
      lines = f.readlines()

      for line in lines:
         if (found_transdip and found_sticks and len(line.split())==0): break

         if(found_transdip and found_sticks and len(line.split())>1):
            if int(line.split()[0]) == state:
               transdip.append(float(line.split()[3]))
               transdip.append(float(line.split()[4]))
               transdip.append(float(line.split()[5]))

         if line.startswith(' no.  E/eV          f                       mu (x,y,z)'):              found_transdip = True
         if line.startswith(' ------------------------------------------------------------------'): found_sticks = True

   if len(transdip) == 0:
         print('')
         print('')
         print(f'   Transdip not found for state {state} in file {file_name}')
         print('')
         print('')
         sys.exit()

   return(transdip)
# -----------------------------------------------
def read_atom_from_runfile(file_name,idx):

   i = 0
   atoms_found = False
   atoms_found_end = False
   coords = []
   with open(file_name, 'r') as f:
      lines = f.readlines()

      for line in lines:
         if (atoms_found and not atoms_found_end):
            i += 1
            if (i == idx):
               coords.append(float(line.split()[1])) 
               coords.append(float(line.split()[2]))
               coords.append(float(line.split()[3]))


         if line.lower().startswith('  atoms'): atoms_found = True
         if line.lower().startswith('  end'):   atoms_found_end = True

      if (atoms_found == False):
         print('')
         print(f'   Atoms not found in file {file_name}')
         print('')
         print('')
         sys.exit()

      if (len(coords) == 0):
         print('')
         print('   Coordinates not found')
         print('')
         print('')
         sys.exit()

   return(coords)
# -----------------------------------------------
def create_run(dovesono, contodir, where_run):
   with open(where_run + '/run.sh','w') as out:
      out.write('#!/bin/bash\n')
      out.write('#PBS -l select=1:ncpus=28:mpiprocs=28:mem=100GB -q q07diamond -N fret\n')
      out.write('#######################################################################\n')
      out.write('                 ## LOAD MODULES + PREPARE SCRATCH##\n')
      out.write('#######################################################################\n')
      out.write('module load gcc/9.3.0 blas-lapack/gcc-9.3.0/3.9.0 intel/mkl/2020/2.254 intel/mpi/2019.8.254\n')
      out.write('source /home/pgrobasillobre/qm_bem/adfbashrc.sh\n')
      out.write('export scm_tmpdir=/scratch/${USER}\n')
      out.write('\n')
      out.write('\n')
      out.write('\n')
      out.write('#######################################################################\n')
      out.write('              ## MODIFY HERE THE NAME OF THE FOLDERS ##\n')
      out.write('#######################################################################\n')
      out.write('\n')
      out.write('contodir=' + contodir + '\n')
      out.write('dovesono=' + dovesono + '\n') 
      out.write('cd "${dovesono}"\n')
      out.write('\n')
      out.write('if [[ ! -d "/scratch/${USER}" ]] ; then mkdir -p "/scratch/${USER}" ; fi\n')
      out.write('#\n')
      out.write('if [[ -d "/scratch/${USER}/${contodir}" ]]; then rm -rf -- "/scratch/${USER}/${contodir}" ; fi\n')
      out.write('cp -r "${contodir}" /scratch/${USER}/ || exit 1\n')
      out.write('cd "/scratch/${USER}/${contodir}" || exit 1\n')
      out.write('\n')
      out.write('## MODIFY EXECUTABLE NAME \n')
      out.write('/home/pgrobasillobre/programs/fret_embedlab_fortran/build/FRET_Embedlab input.inp\n')
      out.write('\n')
      out.write('\n')
      out.write('cd .. \n')
      out.write('\n')
      out.write('rsync -avz ${contodir}/ ${dovesono}/${contodir}\n')
      out.write('rm -r -- "${contodir}"\n')
      out.write('\n')
      out.write('exit 0\n')
      out.write('# finished\n')

   os.system('chmod +x ' + where_run + '/run.sh')
# -----------------------------------------------



# Check if there are already calculation folders
if (os.path.exists('D_state-1_to_A_state-1') or
    os.path.exists('D_state-1_to_A_state-2') or
    os.path.exists('D_state-2_to_A_state-1') or
    os.path.exists('D_state-2_to_A_state-2')):

   print('')
   print('   ----------------------------')
   print('   Folder for input files found')
   print('   ----------------------------')
   print('')

   erase_results = input('   Do you want to delete it and continue? (y/n)  ')
   if(erase_results == "y" or erase_results == "yes"):
      os.system(f'rm -rf D_state-*')
      print(' ')


# Create calculation folders
#os.system('mkdir D_state-1_to_A_state-1  D_state-1_to_A_state-2  D_state-2_to_A_state-1  D_state-2_to_A_state-2')

#os.system('mkdir D_state-1_to_A_state-1/pos-1  D_state-1_to_A_state-1/pos-2  D_state-1_to_A_state-1/pos-3  D_state-1_to_A_state-1/pos-4  D_state-1_to_A_state-1/pos-5  D_state-1_to_A_state-1/pos-6')
#os.system('mkdir D_state-1_to_A_state-2/pos-1  D_state-1_to_A_state-2/pos-2  D_state-1_to_A_state-2/pos-3  D_state-1_to_A_state-2/pos-4  D_state-1_to_A_state-2/pos-5  D_state-1_to_A_state-2/pos-6')
#os.system('mkdir D_state-2_to_A_state-1/pos-1  D_state-2_to_A_state-1/pos-2  D_state-2_to_A_state-1/pos-3  D_state-2_to_A_state-1/pos-4  D_state-2_to_A_state-1/pos-5  D_state-2_to_A_state-1/pos-6')
#os.system('mkdir D_state-2_to_A_state-2/pos-1  D_state-2_to_A_state-2/pos-2  D_state-2_to_A_state-2/pos-3  D_state-2_to_A_state-2/pos-4  D_state-2_to_A_state-2/pos-5  D_state-2_to_A_state-2/pos-6')

#os.system('mkdir D_state-1_to_A_state-1/pos-1 D_state-1_to_A_state-1/pos-4  ')
#os.system('mkdir D_state-1_to_A_state-2/pos-1 D_state-1_to_A_state-2/pos-4  ')
#os.system('mkdir D_state-2_to_A_state-1/pos-1 D_state-2_to_A_state-1/pos-4  ')
#os.system('mkdir D_state-2_to_A_state-2/pos-1 D_state-2_to_A_state-2/pos-4  ')

os.system('mkdir D_state-1_to_A_state-1/pos-5  D_state-1_to_A_state-1/pos-6')
os.system('mkdir D_state-1_to_A_state-2/pos-5  D_state-1_to_A_state-2/pos-6')
os.system('mkdir D_state-2_to_A_state-1/pos-5  D_state-2_to_A_state-1/pos-6')
os.system('mkdir D_state-2_to_A_state-2/pos-5  D_state-2_to_A_state-2/pos-6')





#Create run files
state_folders = ['D_state-1_to_A_state-1','D_state-1_to_A_state-2','D_state-2_to_A_state-1','D_state-2_to_A_state-2']
#pos_folders      = ['pos-1', 'pos-2', 'pos-3', 'pos-4', 'pos-5', 'pos-6']
pos_folders      = ['pos-5', 'pos-6']


dovesono_i = '/home/pgrobasillobre/calc/fret/tip-transfer/kong/tip-mols/fig-1d/freq-2.5_ev/tip-d5.0_angs'

for state_folder in state_folders:
   for contodir in pos_folders:
      dovesono = dovesono_i + '/fret/' + state_folder

      where_run = state_folder + '/' + contodir + '/'

      create_run(dovesono, contodir,where_run)


states = [1, 2]
d_align_dipole = []
a_align_dipole = []
# First donor state
counter_d_state = 0
for i in states:
   # Second aceptor state
   counter_a_state = 0
   for j in states:
      # Run over all positions
      for pos in pos_folders:

         #donor
         d_run_file_path = glob.glob(dovesono_i + '/pt-pc/state-' + str(i) + '/' +  pos + '/*run')[0] 
         d_align_dipole = read_atom_from_runfile(d_run_file_path,d_index[counter_d_state])

         d_log_file_path = glob.glob(dovesono_i + '/pt-pc/state-' + str(i) + '/' +  pos + '/*log')[0] 
         d_transdip = read_transdip(d_log_file_path,i)

         #acceptor
         print(dovesono_i + '/zn-pc/state-' + str(j) + '/' +  pos + '/*run')
         a_run_file_path = glob.glob(dovesono_i + '/zn-pc/state-' + str(j) + '/' +  pos + '/*run')[0] 
         a_align_dipole = read_atom_from_runfile(a_run_file_path,a_index[counter_a_state])

         #print(dovesono_i + '/zn-pc/state-' + str(j) + '/' +  pos + '/*log')
         print(dovesono_i + '/zn-pc/state-' + str(j) + '/' +  pos + '/*log')
         a_log_file_path = glob.glob(dovesono_i + '/zn-pc/state-' + str(j) + '/' +  pos + '/*log')[0] 
         a_transdip = read_transdip(a_log_file_path,j)

         name = 'D_state-'+str(i)+'_to_A_state-'+str(j) + '/' + pos + '/input.inp'

         with open(name, 'w') as inp:
            inp.write(f'aceptor density: {dovesono_i}/zn-pc/state-' + str(j) + '/' + pos + '/zn-pc_trans_dens_' + str(j) + '.cube'  + '\n')
            inp.write(f'donor density:   {dovesono_i}/pt-pc/state-' + str(i) + '/' + pos + '/pt-pc_trans_dens_' + str(i) + '.cube'  + '\n')
            inp.write('cutoff: 1.0e-20\n')
            inp.write(f'nanoparticle:    {dovesono_i}/pt-pc/state-' + str(i) + '/' + pos + '/pt-pc_cam-b3lyp_tzp.log  \n')
            inp.write('spectral overlap: 1.0\n')
            inp.write('!\n')
            inp.write('rotation axys: z\n')
            inp.write('!\n')
            #inp.write(f'aceptor transition dipole:  {a_transdip[0]}  {a_transdip[1]}  {a_transdip[2]}\n')
            inp.write(f'aceptor transition dipole:  {a_transdip[0]}  {a_transdip[1]}  0.0\n')

            inp.write(f'aceptor transition dipole align with:  {a_align_dipole[0]}  {a_align_dipole[1]}  {a_align_dipole[2]}\n')

            inp.write('!\n')
            #inp.write(f'donor transition dipole:  {d_transdip[0]}  {d_transdip[1]}  {d_transdip[2]}\n')
            inp.write(f'donor transition dipole:  {d_transdip[0]}  {d_transdip[1]}  0.0\n')

            inp.write(f'donor transition dipole align with:  {d_align_dipole[0]}  {d_align_dipole[1]}  {d_align_dipole[2]}\n')

            inp.write('!\n')
            inp.write('debug: 1\n')



      counter_a_state += 1

   counter_d_state += 1





