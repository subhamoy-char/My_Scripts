#!/bin/bash
FILENAME=$1
cp $1 CONTCAR.org
ATOM1=`sed -n '6p' $1 | awk '{print $1}'`
ATOM2=`sed -n '6p' $1 | awk '{print $2}'`
ION1=`sed -n '7p' $1 | awk '{print $1}'`
ION2=`sed -n '7p' $1 | awk '{print $2}'`
NIONS=`echo "$ION1 + $ION2" | bc -l`
CrysForm=$ATOM1$ION1$ATOM2$ION2
sed -i '1c '"$CrysForm"'' $1
sed -i '2c 0.001' $1
sed -i '3i 1' $1
sed -i '7c 2' $1
sed -i '8c P' $1
sed -i '9c '"$NIONS"'' $1
sed -i '10i '"$ION1*$ATOM1 $ION2*$ATOM2"'' $1
mv $1 $1.in
findsym <$1.in>$CrysForm.cif
###
###
cp CONTCAR.in CONTCAR.tolerance
###
###
for k in 0.001 0.002 0.005 0.01 0.02 0.05 0.1 0.2 0.4 0.5
do
sed -i '2c '"$k"'' CONTCAR.tolerance
findsym <CONTCAR.tolerance> CONTCAR-$k.cif
echo $k >>tolerance 
cat CONTCAR-$k.cif | grep "Space Group" >>SG-info
paste tolerance SG-info > SG-wrt-tolerance
done
