for i in fort*;
do
mkdir CAL-$i
cd CAL-$i
mkdir sym
cp ../$i sym/
find_symmetry-quinary.sh sym/$i
tot_num=`grep -w "Wyckoff position" sym/$i-lattice_0.001.cif | wc -l`
Na=`grep -w "Wyckoff position" sym/$i-lattice_0.001.cif | grep "Na" | wc -l`
Ca=`grep -w "Wyckoff position" sym/$i-lattice_0.001.cif | grep "Ca" | wc -l`
P=`grep -w "Wyckoff position" sym/$i-lattice_0.001.cif | grep "P" | wc -l`
O=`grep -w "Wyckoff position" sym/$i-lattice_0.001.cif | grep "O" | wc -l`
F=`grep -w "Wyckoff position" sym/$i-lattice_0.001.cif | grep "F" | wc -l`
a=`grep -w "_cell_length_a" sym/$i-lattice_0.001.cif | awk '{ print $2 }'`
b=`grep -w "_cell_length_b" sym/$i-lattice_0.001.cif | awk '{ print $2 }'`
c=`grep -w "_cell_length_c" sym/$i-lattice_0.001.cif | awk '{ print $2 }'`
alpha=`grep -w "_cell_angle_alpha" sym/$i-lattice_0.001.cif | awk '{ print $2 }'`
beta=`grep -w "_cell_angle_beta" sym/$i-lattice_0.001.cif | awk '{ print $2 }'`
gamma=`grep -w "_cell_angle_gamma" sym/$i-lattice_0.001.cif | awk '{ print $2 }'`
cat >>INSOD <<EOF
#Title
FAP

# a,b,c,alpha,beta,gamma
$a $b $c $alpha $beta $gamma

# nsp: Number of species
5

# symbol(1:nsp): Atom symbols
Na Ca P O F

# natsp0(1:nsp): Number of atoms for each species (enough to specify those in the asymmetric unit)
$Na $Ca $P $O $F

# coords0(1:nat0,1:3): Coordinates of each atom (one line per atom)
EOF
grep -A$tot_num "_atom_site_fract_symmform" sym/$i-lattice_0.001.cif | awk '{ print $5,"\t"$6,"\t"$7 }' | sed '1d' >>INSOD
echo >> INSOD
cat >>INSOD <<EOF
# na,nb,nc (supercell definition)
1 1 1

# sptarget: Species to be substituted
4

# nsubs: Number of substitutions in the supercell
4

# newsymbol(1:2): Symbol of atom to be inserted in the selected position,
#                 symbol to be inserted in the rest of the positions for the same species.
V O

# FILER, MAPPER
# # FILER:   0 (no calc files generated), 1 (GULP), 2 (METADISE), 11 (VASP), 12 (CASTEP)
# # MAPPER:  0 (no mapping, use currect structure), >0 (map to structure in MAPTO file)
# # (each position in old structure is mapped to MAPPER positions in new structure)
11 0

# If FILER=1 then:
# ishell(1:nsp) 0 core only / 1 core and shell (for the species listed in symbol(1:nsp))
0 0 1 0
# newshell(1:2) 0 core only / 1 core and shell (for the species listed in newsymbol(1:2))
0 0
EOF
cd ..
done
