import os
import shutil
import ase
from glob import iglob
from ase.io import read, write
from ase.neighborlist import neighbor_list, first_neighbors
from pathlib import PurePath
    
def vac_elemination():
    for pathname in iglob("fort*"):
        input_file = read(pathname, format='vasp')
        cell = input_file.get_cell()
        total_atoms = len(input_file)
        cutoff = {('V', 'V'): 2.60, ('Si', 'V'):1.60}
        i = neighbor_list('i', input_file, cutoff)
        if len(i)==0:
            pass
        else:
            shutil.move(pathname,"./fault-structure")

vac_elemination()

def carbonate_replace():
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
                output_file = write(PurePath('./modify-poscars',pathname),input_file,format='vasp',direct=True,sort=True)

carbonate_replace()
