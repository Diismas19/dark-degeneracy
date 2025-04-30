#!/bin/bash
#SBATCH --job-name=vitor-cobaya-int				#Nome job com o nome do aluno/prof
#SBATCH --nodes=1						#Numero de Nós
#SBATCH --ntasks=4						#Numero total de tarefas MPI/OPENMP
#SBATCH --partition z1-short,ry-short			#Fila (partition) a ser utilizada
#SBATCH --output %x-slurm_job-%j.out
#SBATCH --error  %x-slurm_job-%j.err
#SBATCH --cpus-per-task=8
#SBATCH --exclusive

## Mandar para o scratch
echo $SLURM_SUBMIT_DIR
cd $SLURM_SUBMIT_DIR
scratch_dir='/local-scratch/'${SLURM_JOB_NAME}
mkdir -p $scratch_dir
cp -r * $scratch_dir
cd $scratch_dir
rm *slurm_job*

## Comando

conda activate vitor

export OMP_NUM_THREADS=8
export OMP_PLACES=threads
export OMP_PROC_BIND=spread

time mpirun -n 4 -c 8 cobaya-run -r int.yaml

while [ $? -ne 0 ]; do
  echo 'Crashed!'
  echo "Trying again"
  time mpirun -n 4 -c 8 cobaya-run -r int.yaml
done

## Do scratch para a home
home_dir=${SLURM_SUBMIT_DIR}/${SLURM_JOB_NAME}
mkdir -p $home_dir
mv ${scratch_dir}/* $home_dir
echo 'Done! \o/'