#!/bin/bash
#PBS -N Serpent_Source 
#PBS -l select=80:ncpus=48:mpiprocs=1 
#PBS -l walltime=168:00:00
#PBS -k doe
#PBS -j oe
#PBS -P ne_gen

cd $PBS_O_WORKDIR
module load  use.exp_ctl
module load serpent/2.1.31-intel-19.0_ACE_KERMA_fix


mpirun sss2 ./coupledTreat -omp 48