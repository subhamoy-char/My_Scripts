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
