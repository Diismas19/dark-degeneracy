#!/bin/bash
#SBATCH --job-name=vitor_teste				#Nome job com o nome do aluno/prof
#SBATCH --nodes=1						#Numero de Nós
##SBATCH --ntasks=4		(comentado)				#Numero total de tarefas MPI/OPENMP
#SBATCH --partition dev		#Fila (partition) a ser utilizada
#SBATCH --output %x-slurm_job-%j.out
#SBATCH --error  %x-slurm_job-%j.err
##SBATCH --cpus-per-task=8 (comentado)

##SBATCH --exclusive (comentado)

## Mandar para o scratch
echo $SLURM_SUBMIT_DIR
cd $SLURM_SUBMIT_DIR
scratch_dir='/local-scratch/'${SLURM_JOB_NAME}
mkdir -p $scratch_dir
cp -r * $scratch_dir
cd $scratch_dir
rm *slurm_job*

## Comando
source /home/valerio/anaconda3/bin/activate vitor

# # export OMP_NUM_THREADS=8
# # export OMP_PLACES=threads
# # export OMP_PROC_BIND=spread

cobaya-run teste.yaml

while [ $? -ne 0 ]; do
  echo 'Crashed!'
  echo "Trying again"
  cobaya-run -r teste.yaml
done

## Do scratch para a home
home_dir=${SLURM_SUBMIT_DIR}/${SLURM_JOB_NAME}
mkdir -p $home_dir
mv ${scratch_dir}/* $home_dir
echo 'Done! \o/'
