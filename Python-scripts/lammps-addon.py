#### Import Libraries ####################
import csv
import numpy as np 
import re
###### Creating files ####################
def my_function():
	#import csv
	#import numpy as np
	#import re
    	file_out = open("data-new", "w")
    	file1_out = open("data1-new.txt", mode = 'w')
    	atypes = ""
    	natoms = ""
    	charge_list = ()
    	charge_type1 = (0.945)
    	charge_type2 = (1.890)
    	charge_type3 = (1.890)
    	charge_type4 = (-0.945)
    	with open("coo", 'r') as file_input:
        	contents = file_input.read()
        	character = 'Atoms'
        	result = contents.split(character)
        	file_out.write(result[0])
        	file_out.write('Atoms')
        	file1_out.write(result[1])
        	file_out.close()
        	file1_out.close()
    	store = np.genfromtxt(r'data1-new.txt', skip_header=2, dtype=None)
    	tot_atoms = store['f1']
    	for i in range(len(tot_atoms)):
        	if tot_atoms[i] == 1:
            		charge_list = charge_list + (charge_type1,)
        	elif tot_atoms[i] == 2:
            		charge_list = charge_list + (charge_type2,)
        	elif tot_atoms[i] == 3:
            		charge_list = charge_list + (charge_type3,)
        	elif tot_atoms[i] == 4:
            		charge_list = charge_list + (charge_type4,)
    	final_tuple = [(a[0], a[1], b, a[2], a[3], a[4]) for a, b in zip(store, charge_list)]
    	file_out = open("data-new", "r")
    	with open ("data.pos", "w") as out:
        	out.write(file_out.read())
        	out.write('\n \n')
        	out.write('\n'.join('{}\t{}\t{}\t{}\t{}\t{}'.format(a[0], a[1], a[2], a[3], a[4], a[5]) for a in final_tuple))
        	out.close()
        	file_out.close()
my_function()
