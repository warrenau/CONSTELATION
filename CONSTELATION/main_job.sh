#!/bin/bash
#PBS -N Coupling_Script 
#PBS -l select=1:ncpus=4:mpiprocs=1 
#PBS -l walltime=168:00:00
#PBS -k doe
#PBS -j oe
#PBS -P ne_gen

cd $PBS_O_WORKDIR
module load  python/2.7-anaconda-2019.10

python CONSTELATIONV.py 


