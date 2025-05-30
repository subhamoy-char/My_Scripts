#!/bin/sh
#PBS -N test
#PBS -q mini
#PBS -l nodes=1:ppn=20
#PBS -j oe
#
echo ""
#Reading Settings and Variables
source /home/subhamoy/.bashrc
cd $PBS_O_WORKDIR
ulimit -s unlimited
export OMP_NUM_THREADS=1
###
cat $PBS_NODEFILE > pbs_nodes
NPROCS=`wc -l < $PBS_NODEFILE`
NNODES=`uniq $PBS_NODEFILE | wc -l`
echo Running on host `hostname`
echo Directory is `pwd`
echo Using ${NPROCS} processors across ${NNODES} nodes
###
export VASP_BIN='/home/subhamoy/Software/VASP/bin/vaspEDD/vasp_std'
echo Start time is `date`
#
echo "Job Started"
#
mpirun -np ${NPROCS} $VASP_BIN >STDOUT
#
echo End time is `date`
#end

for i in {2..20..2};
do
mkdir $i-GPa
cd $i-GPa
cp ../{POSCAR,KPOINTS} .
pstress=`echo "$i*10" | bc`
cat >INCAR <<EOF
PREC = ACCURATE
ENCUT = 400
PSTRESS = $pstress
EOF
cd ..
done
