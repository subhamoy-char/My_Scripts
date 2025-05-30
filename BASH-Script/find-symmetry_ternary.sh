#### This script will be applicable only for new version of FINDSYM #######
#!/bin/bash
FILENAME=$1
cat >>cif-vs-tolerance.info <<EOF
Lattice_tolerance	Space_Group
EOF
for k in 0.00001 0.00005 0.0001 0.0005 0.001 0.005 0.01 0.05;
do
cp $1 $1-lattice_$k.in
ATOM1=`sed -n '6p' $1 | awk '{print $1}'`
ATOM2=`sed -n '6p' $1 | awk '{print $2}'`
ATOM3=`sed -n '6p' $1 | awk '{print $3}'`
ION1=`sed -n '7p' $1 | awk '{print $1}'`
ION2=`sed -n '7p' $1 | awk '{print $2}'`
ION3=`sed -n '7p' $1 | awk '{print $3}'`
Total_ions=`echo "$ION1+$ION2+$ION3" | bc`
sed -i '1,2d' $1-lattice_$k.in
sed -i '1 i !useKeyWords' $1-lattice_$k.in
sed -i '2 i !title' $1-lattice_$k.in
sed -i '3 i Sample input file to identify_space_group.' $1-lattice_$k.in
sed -i '4 i !latticeTolerance' $1-lattice_$k.in
sed -i '5 i '"$k"'' $1-lattice_$k.in
sed -i '6 i !latticeBasisVectors' $1-lattice_$k.in
sed -i '10 i !unitCellCentering' $1-lattice_$k.in
sed -i '11 i P' $1-lattice_$k.in
sed -i '12 i !atomCount' $1-lattice_$k.in
sed -i '13 i '"$Total_ions"'' $1-lattice_$k.in
sed -i '14 i !atomType' $1-lattice_$k.in
sed -i '15 i '"$ION1*$ATOM1 $ION2*$ATOM2 $ION3*$ATOM3"'' $1-lattice_$k.in
sed -i '16 i !atomPosition' $1-lattice_$k.in
sed -i '17,19d' $1-lattice_$k.in
findsym $1-lattice_$k.in >$1-lattice_$k.cif
symmetry=`grep -w "Space Group:" findsym.log | awk '{ print $5 }'`
cat >>cif-vs-tolerance.info <<EOF
$k	$symmetry
EOF
done
