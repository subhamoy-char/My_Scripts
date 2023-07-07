#!/bin/bash
cat >summary.dat <<EOF1
P       Entahlpy        L_x     L_y     L_z     Volume  Pressure
EOF1
for i in 10 50000 100000 150000 200000 250000 300000 350000 400000 450000 500000  
do
Entahlpy=`awk '!/#/ { sum += $3 } END { if (NR > 0) print sum / NR }' log.lammps-$i`
L_x=`awk '!/#/ { sum += $4 } END { if (NR > 0) print sum / NR }' log.lammps-$i`
L_y=`awk '!/#/ { sum += $5 } END { if (NR > 0) print sum / NR }' log.lammps-$i`
L_z=`awk '!/#/ { sum += $6 } END { if (NR > 0) print sum / NR }' log.lammps-$i`
Volume=`awk '!/#/ { sum += $10 } END { if (NR > 0) print sum / NR }' log.lammps-$i`
Pressure=`awk '!/#/ { sum += $13 } END { if (NR > 0) print sum / NR }' log.lammps-$i`
cat >>summary.dat <<EOF2
$i	$Entahlpy	$L_x	$L_y	$L_z	$Volume	$Pressure
EOF2
done
