##########  Import OVITO modules  ##########
from ovito.io import *
from ovito.modifiers import *
############################################
###### Import NumPy module #######
import numpy
############################################

########### Print total output #############
numpy.set_printoptions(threshold=numpy.inf)
############################################

# Load a simulation snapshot of a Al-1200K (NPT).
node = import_file("../RDF/XDATCAR")

# Set atomic radii (required for polydisperse Voronoi tessellation).
atypes = node.source.particle_properties.particle_type.type_list
atypes[0].radius = 1.26        # Fe atomic radius (atom type 1 in input file)
atypes[1].radius = 1.43        # Al atomic radius (atom type 2 in input file)

fout = open("voronoi.dat","a")
fout.write("X\n")

for frame in range(node.source.num_frames):

	# Set up the Voronoi analysis modifier.
	voro = VoronoiAnalysisModifier(
	    compute_indices = True,
	    use_radii = True,
	   edge_count = 10, # Length after which Voronoi index vectors are truncated
	   edge_threshold = 0.05
	)
	node.modifiers.append(voro)
                      
	# Let OVITO compute the results.
	node.compute(frame)

	# Make sure we did not lose information due to truncated Voronoi index vectors.
	if voro.max_face_order > voro.edge_count:
	    print("Warning: Maximum face order in Voronoi tessellation is {0}, "
                 "but computed Voronoi indices are truncated after {1} entries. "
       	         "You should consider increasing the 'edge_count' parameter to {0}."
         	 .format(voro.max_face_order, voro.edge_count))
	    # Note that it would be possible to automatically increase the 'edge_count'
	    # parameter to 'max_face_order' here and recompute the Voronoi tessellation:
	    #   voro.edge_count = voro.max_face_order
	    #   node.compute()

	# Access computed Voronoi indices as NumPy array.
	# This is an (N)x(edge_count) array.
	voro_indices = node.output.particle_properties['Voronoi Index'].array
	print(numpy.array2string(voro_indices, formatter={'int_kind':'{0:3d}'.format}).replace('[[',' ').replace('[','').replace(']',''), file=fout)
fout.close()
