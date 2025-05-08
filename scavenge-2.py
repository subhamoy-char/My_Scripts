import os
import ase
from pathlib import PurePath
from glob import iglob
from ase.io import read, write
from ase.neighborlist import neighbor_list, first_neighbors
    
for pathname in iglob("fort*"):
    input_file = read(pathname, format='vasp')
    cell = input_file.get_cell()
    total_atoms = len(input_file)
    cutoff = {('P', 'V'): 1.60}
    i = neighbor_list('i', input_file, cutoff)
    if len(i)==0:
        pass
    else:
        for index in i:
            if (input_file[index].symbol=='P'):
                input_file[index].symbol='C'
            else:
                pass
            del input_file[[atom.index for atom in input_file if atom.symbol == 'V']]
            output_file = write(PurePath('/MyData/FCAp/Equn-4/112-supercell/from-vaspkit/CO3-substitution/scan/modify_poscars',pathname),input_file,format='vasp',direct=True,sort=True)

##### other important commands #######
#    print(input_file.get_scaled_positions())
#    input_file[0].symbol = 'Ga'
#    j = first_neighbors(total_atoms, i)
#    print(input_file.get_chemical_symbols())
#    print(input_file)
