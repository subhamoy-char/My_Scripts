# With that script, we can count number of Fe, Al, total coordination number for
# a central atom.

from ovito.io import import_file
from ovito.data import CutoffNeighborFinder

node = import_file("./All-POSCARs/XDATCAR")

cutoff = 3.15

for frame in range(node.source.num_frames):
	data = node.compute(frame)
	finder = CutoffNeighborFinder(cutoff, data)
	for index in range(data.number_of_particles):
		Fe = 0
		Al = 0
		for neigh in finder.find(index):
			if neigh.index <= 159:
				Fe += 1
			else:
				Al += 1
		print(index,Fe,Al,Fe+Al,sep=',')
