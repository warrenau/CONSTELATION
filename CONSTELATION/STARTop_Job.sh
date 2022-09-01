#!/bin/bash
#PBS -N Star_Couple
#PBS -l select=1:ncpus=48:mpiprocs=48
#PBS -l walltime=168:00:00
#PBS -k doe
#PBS -j oe
#PBS -P ne_gen

cd $PBS_O_WORKDIR
source /etc/profile.d/modules.sh
module load  star-ccm-plus/15.04.010_01-gcc-9.3.0-stjm

starccm+ -batchsystem pbs -batch load_dataTop.java -rsh ssh 01.14.2021_STARTop.sim
