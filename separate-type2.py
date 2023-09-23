from __future__ import print_function
import numpy as np
text_file = open("XDATCAR", "r")
Line1 = 0
Line2 = 264
fout = open('chk1.dat', "w")
for index, text in enumerate(text_file):
	if Line1 <= index < Line2:
		print(text, end="", file=fout)
	elif index == Line2:
		Line1 = Line1 + 26400
		Line2 = Line2 + 26400
		fout.close()
		fout = open('chk%d.dat'%(Line2/264), "w")
fout.close()

#d = np.loadtxt('chk.dat',usecols=range(0,3))
#e = np.split(d,10)
#def rmsd(I,F):
#	return np.sqrt(1./256.*((I-F)**2).sum())
#rmsd_val = rmsd(c,e)
#print(rmsd_val)
