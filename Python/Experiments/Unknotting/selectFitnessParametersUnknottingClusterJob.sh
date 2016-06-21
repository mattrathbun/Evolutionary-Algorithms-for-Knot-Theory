#!/bin/sh

#PBS -q default #select the default queue

#PBS -l nodes=1 #use only one node

#PBS -l walltime=24:00:00 #cancel the job after this much time if still running.

#PBS -l mem=1gb #expected memory usage

#PBS -o selectFitnessParametersUnknottingOutput.txt #name of the final output file (whatever you like)

#PBS -N R_1 #name of the job, set to whatever you like

#PBS -j oe #combine output and error into the same file

#PBS -V #verbose

cd ${HOME}/Evolutionary-Algorithms-for-Knot-Theory/Python/Experiments/Unknotting #change to the directory containing the code

### Count the number of nodes and processors used

NPROCS='wc -l < $PBS_NODEFILE'

NNODES='uniq $PBS_NODEFILE | wc -l'

### Display the job context

echo Running on host 'hostname'

echo Time is 'date'

echo Directory is 'pwd'

echo Using ${NPROCS} processors across ${NNODES} nodes

### Command to run the job

mpirun -np 1 -hostfile $PBS_NODEFILE /share/apps/python-2.7.8/bin/python < selectFitnessParametersUnknotting.py| tee selectFitnessParametersUnknottingOutput.txt

### Replace AddressOfR with /share/apps/R/R-3.1.1/bin/R