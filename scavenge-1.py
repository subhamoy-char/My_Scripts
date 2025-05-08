import os
import shutil
from glob import iglob
from ase.io import read, write
from ase.neighborlist import neighbor_list
    
for pathname in iglob("fort*"):
    input_file = read(pathname, format='vasp')
    cell = input_file.get_cell()
    total_atoms = len(input_file)
    cutoff = {('V', 'V'): 2.60, ('Si', 'V'):1.60}
    i = neighbor_list('i', input_file, cutoff)
    if len(i)==0:
        pass
    else:
        shutil.move(pathname,"/MyData/FCAp/Si-doped-brithollite/112-supercell-Equn-4/from-vaspkit/CO3-substitution/scan/fault-structure")
