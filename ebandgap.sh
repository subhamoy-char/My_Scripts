#!/bin/bash
#
echo ""
echo ""
FILENAME=$1
NKPT=`grep NKPT $1 | awk '{print $4}'`
echo "Number of K points:" $NKPT
echo ""
VBMax=`grep NELECT $1 | awk '{print ($3 * 0.5)}'`
echo "VBMax is:" $VBMax
echo ""
VB=`grep "^     "$VBMax"     " $1 | tail -$NKPT | sort -n -k 2 | tail -1 | awk '{print $2}'`
echo "VB "--" valence band energy:" $VB
echo ""
CBMin=`echo "$VBMax+1" | bc -l | awk '{print $1}'`
echo "CBMin is:" $CBMin
echo ""
CB=`grep "^     "$CBMin"     " $1 | tail -$NKPT | sort -n -k 2 | head -1 | awk '{print $2}'`
echo "CB -- conduction band energy:" $CB
echo ""
BANDGAP=`echo "$CB - $VB" | bc -l | awk '{print $1}'`
echo "Electronic BAND-GAP in eV is :" $BANDGAP
echo ""
echo "done"
echo ""

