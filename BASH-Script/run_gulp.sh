for i in fort*
do
mkdir CAL-$i
cp $i CAL-$i
cd CAL-$i
str="$i"
cat >>gulp.gin <<EOF
opti conp prop
title
FAP
end
vectors
EOF
sed -n "3,5p" $str >>gulp.gin
#if ("sed -n '6p' $str | awk '{print $1}'" == "Zr" || "sed -n '6p' $str | awk '{print $2}'" == "Gd" || "sed -n '6p' $str | awk '{print $3}'" == "O" || "sed -n '6p' $str | awk '{print $4}'" == "O"); then
tail -n +9 $str >coordinates.dat
U=`sed -n '6p' $str | awk '{print $1}'`
U_num=`sed -n '7p' $str | awk '{print $1}'`
Ca=`sed -n '6p' $str | awk '{print $2}'`
Ca_num=`sed -n '7p' $str | awk '{print $2}'`
UCa=`echo "$U_num+$Ca_num" | bc`
Si=`sed -n '6p' $str | awk '{print $3}'`
Si_num=`sed -n '7p' $str | awk '{print $3}'`
UCaSi=`echo "$U_num+$Ca_num+$Si_num" | bc`
P=`sed -n '6p' $str | awk '{print $4}'`
P_num=`sed -n '7p' $str | awk '{print $4}'`
UCaSiP=`echo "$U_num+$Ca_num+$Si_num+$P_num" | bc`
O=`sed -n '6p' $str | awk '{print $5}'`
O_num=`sed -n '7p' $str | awk '{print $5}'`
UCaSiPO=`echo "$U_num+$Ca_num+$Si_num+$P_num+$O_num" | bc`
F=`sed -n '6p' $str | awk '{print $6}'`
F_num=`sed -n '7p' $str | awk '{print $6}'`
UCaSiPOF=`echo "$U_num+$Ca_num+$Si_num+$P_num+$O_num+$F_num" | bc`
echo "fractional" >>gulp.gin
cat coordinates.dat | gawk 'NR<='$U_num' {print "U","\t""core","\t"$1,"\t"$2,"\t"$3}' >>gulp.gin
cat coordinates.dat | gawk 'NR>'$U_num' && NR<='$UCa' {print "Ca","\t""core","\t"$1,"\t"$2,"\t"$3}' >>gulp.gin
cat coordinates.dat | gawk 'NR>'$UCa' && NR<='$UCaSi' {print "Si","\t""core","\t"$1,"\t"$2,"\t"$3}' >>gulp.gin
cat coordinates.dat | gawk 'NR>'$UCaSi' && NR<='$UCaSiP' {print "P","\t""core","\t"$1,"\t"$2,"\t"$3}' >>gulp.gin
cat coordinates.dat | gawk 'NR>'$UCaSiP' && NR<='$UCaSiPO' {print "O","\t""core","\t"$1,"\t"$2,"\t"$3}' >>gulp.gin
cat coordinates.dat | gawk 'NR>'$UCaSiPO' && NR<='$UCaSiPOF' {print "F","\t""core","\t"$1,"\t"$2,"\t"$3}' >>gulp.gin
cat coordinates.dat | gawk 'NR>'$UCaSiP' && NR<='$UCaSiPO' {print "O","\t""shel","\t"$1,"\t"$2,"\t"$3}' >>gulp.gin
cat coordinates.dat | gawk 'NR>'$UCaSiPO' && NR<='$UCaSiPOF' {print "F","\t""shel","\t"$1,"\t"$2,"\t"$3}' >>gulp.gin
cat >>gulp.gin <<EOF
species
Na core 1.000
Ca core	2.000
P core 1.180
F core 1.380
Si core 0.180
F shel -2.380 
O core 0.587
O shel -1.632
U core 4.000 
buck
Ca core O shel 1550.0 0.29700 0.0 0.0 20.0
Ca core F shel 1272.8 0.29970 0.0 0.0 20.0
Na core O shel 1540.00 0.269355 0.0 0.0 20.0
Na core F shel 917.74 0.279036 0.0 0.0 20.0
O shel O shel 16372.0 0.21300 3.47 0.0 20.0
O shel F shel 583833.7 0.21163 7.68 0.0 20.0
F shel F shel 99731834.0 0.12013 17.02423 0.0 20.0
U core O shel 1331.0 0.347975 0.0 0.0 20.0
U core F shel 1567.0 0.334216 0.0 0.0 20.0
morse
P core O core 3.470 2.030 1.600 0.0 2.00
Si core O core 4.8300 1.8840 1.6200 0.0 2.00
three
P core O core O core 1.322626 109.470000 1.300 1.300 2.200
Si core O core O core 2.097240 109.470000 1.300 1.300 2.200 
spring
F 101.2000
O 507.4000
EOF
cat gulp.gin >gulp1.gin | sed -i '10s/U/Na/' gulp1.gin
cat gulp.gin >gulp2.gin | sed -i '11s/U/Na/' gulp2.gin
for j in 1 2
do
mkdir $j
mv gulp$j.gin $j/
cd $j
echo $i/$j
mpirun -np 24 gulp gulp$j
SPE=`grep -A2 "  Start of bulk optimisation :" gulp$j.gout | tail -1 | awk '{ print $4 }'`
FE=`grep -w "Final energy" gulp$j.gout | awk '{ print $4 }'`
Fgnorm=`grep -w "Final Gnorm" gulp$j.gout | awk '{ print $4 }'`
Vol=`grep -w "Non-primitive cell volume =" gulp$j.gout | tail -1 |  awk '{ print $5 }'`
Formula=`grep -w "Formula" gulp$j.gout | awk '{ print $3 }'`
Lat_prm=`grep -A8 "  Final cell parameters and derivatives :" gulp$j.gout | tail -6 | awk '{ print $2 }' | tr '\n' ' '`
echo $i/$j $SPE $FE $Lat_prm $Vol $Fgnorm $Formula >> ../../summary.out
cd ..
done
cd ..
done
