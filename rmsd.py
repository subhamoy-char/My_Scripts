from __future__ import print_function
import numpy as np

c = np.loadtxt('ref.dat',usecols=range(0,3))

def rmsd(I,F):
	return np.sqrt(1./256.*((I-F)**2).sum())

text_file = open("XDATCAR", "r")
Line1 = 8
Line2 = 265
fout = open('chk.dat', "w")
for index, text in enumerate(text_file,1):
#	if index <= Line1:
#		continue
        if Line1 < index < Line2:
                print(text, end="", file=fout)
	elif index == Line2: 
		Line1 = Line1 + 257
		Line2 = Line2 + 257
		fout.close()
		d = np.loadtxt('chk.dat',usecols=range(0,3))
		rmsd_val = rmsd(c,d)
		print(rmsd_val)
		fout = open('chk.dat', "w")
fout.close()
d = np.loadtxt('chk.dat',usecols=range(0,3))
rmsd_val = rmsd(c,d)
print(rmsd_val)
