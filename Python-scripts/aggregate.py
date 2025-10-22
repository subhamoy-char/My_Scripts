import sys
import numpy as np
from scipy.ndimage import gaussian_filter1d
import matplotlib.pyplot as plt


atomic_masses = {
    "H": 1.00794, "C": 12.01070, "N": 14.00670, "O": 15.99940, "Na": 22.98977, 
    "S": 32.06500, "a": 22.98977}

box_volume = 77.560 * 77.560 * 77.560
tot_num_particles = 46310

def box_center_of_mass():
    total_mass = 0.0
    weighted_x = 0.0
    weighted_y = 0.0
    weighted_z = 0.0

    with open ('aggregate.pdb') as f:
        for line in f:
            if line.startswith("ATOM"):
                atom_type = line[76:78].strip()
                mass = atomic_masses[atom_type]
                x = float(line[30:38])
                y = float(line[38:46])
                z = float(line[46:54])

                total_mass += mass
                weighted_x += mass*x
                weighted_y += mass*y
                weighted_z += mass*z

    x_com = weighted_x / total_mass
    y_com = weighted_y / total_mass
    z_com = weighted_z / total_mass

    return(x_com, y_com, z_com)

center_of_mass = box_center_of_mass()

print(f"Center of Mass (X, Y, Z): {center_of_mass[0]:.3f}, {center_of_mass[1]:.3f}, {center_of_mass[2]:.3f}")
ref_center = np.array([center_of_mass])


##### Calculationg COM for SO4 group of SLES #########

def SLE_SO4_COM():
    total_mass_SLE_SO4 = 0.0
    weighted_x_SLE_SO4 = 0.0
    weighted_y_SLE_SO4 = 0.0
    weighted_z_SLE_SO4 = 0.0
    
    text_file = open("SLE.pdb", "r")
#    fout1 = open('SLE_COM_SO4.dat', "a")
    Line1 = 0
    Line2 = 4
    
    for index, text in enumerate(text_file):
        if Line1 <= index <= Line2:
            atom_type_SLE_SO4 = text[76:78].strip()
            mass_SLE_SO4 = atomic_masses[atom_type_SLE_SO4]
            
            x_SLE_SO4 = float(text[30:38])
            y_SLE_SO4 = float(text[38:46])
            z_SLE_SO4 = float(text[46:54])
            
            total_mass_SLE_SO4 += mass_SLE_SO4
            weighted_x_SLE_SO4 += mass_SLE_SO4*x_SLE_SO4
            weighted_y_SLE_SO4 += mass_SLE_SO4*y_SLE_SO4
            weighted_z_SLE_SO4 += mass_SLE_SO4*z_SLE_SO4
            
            x_com_SLE_SO4 = weighted_x_SLE_SO4 / total_mass_SLE_SO4
            y_com_SLE_SO4 = weighted_y_SLE_SO4 / total_mass_SLE_SO4
            z_com_SLE_SO4 = weighted_z_SLE_SO4 / total_mass_SLE_SO4
            
        elif index > Line2:
#            print(x_com_SLE_SO4,y_com_SLE_SO4,z_com_SLE_SO4, file=fout1)
#            print(x_com_SLE,y_com_SLE,z_com_SLE)
            total_mass_SLE_SO4 = 0.0
            weighted_x_SLE_SO4 = 0.0
            weighted_y_SLE_SO4 = 0.0
            weighted_z_SLE_SO4 = 0.0
            Line1 = Line1 + 49
            Line2 = Line2 + 49

#    fout1.close()
SLE_SO4_COM()
#################################################################

##### Calculationg ether group of SLES #########
def SLE_eth_COM():
    total_mass_SLE_eth = 0.0
    weighted_x_SLE_eth = 0.0
    weighted_y_SLE_eth = 0.0
    weighted_z_SLE_eth = 0.0
    
    text_file = open("SLE.pdb", "r")
#    fout2 = open('SLE_COM_eth.dat', "a")
    Line1 = 5
    Line2 = 11
    
    for index, text in enumerate(text_file):
        if Line1 <= index <= Line2:
            atom_type_SLE_eth = text[76:78].strip()
            mass_SLE_eth = atomic_masses[atom_type_SLE_eth]
            
            x_SLE_eth = float(text[30:38])
            y_SLE_eth = float(text[38:46])
            z_SLE_eth = float(text[46:54])
            
            total_mass_SLE_eth += mass_SLE_eth
            weighted_x_SLE_eth += mass_SLE_eth*x_SLE_eth
            weighted_y_SLE_eth += mass_SLE_eth*y_SLE_eth
            weighted_z_SLE_eth += mass_SLE_eth*z_SLE_eth
            
            x_com_SLE_eth = weighted_x_SLE_eth / total_mass_SLE_eth
            y_com_SLE_eth = weighted_y_SLE_eth / total_mass_SLE_eth
            z_com_SLE_eth = weighted_z_SLE_eth / total_mass_SLE_eth
            
        elif index > Line2:
 #           print(x_com_SLE_eth,y_com_SLE_eth,z_com_SLE_eth, file=fout2)
 #           print(x_com_SLE_eth,y_com_SLE_eth,z_com_SLE_eth)
            total_mass_SLE_eth = 0.0
            weighted_x_SLE_eth = 0.0
            weighted_y_SLE_eth = 0.0
            weighted_z_SLE_eth = 0.0
            Line1 = Line1 + 49
            Line2 = Line2 + 49

#    fout2.close()
SLE_eth_COM()

########### Calculating RDF of SO4 ether for SLES ##############

data_SLE_SO4 = np.loadtxt("SLE_COM_SO4.dat", dtype=float)
data_SLE_eth = np.loadtxt("SLE_COM_eth.dat", dtype=float)
n_frames = len(data_SLE_SO4)
r_max = 40.0                  
nbins = 200
dr = r_max / nbins
bin_edges = np.linspace(0, r_max, nbins + 1)
rdf_hist_SLE_SO4 = np.zeros(nbins)
rdf_hist_SLE_eth = np.zeros(nbins)

for t in range(n_frames):
    r_SLE_SO4 = np.linalg.norm(data_SLE_SO4[t] - ref_center) 
    if r_SLE_SO4 < r_max:
        bin_index_SLE_SO4 = int(r_SLE_SO4/dr)
        rdf_hist_SLE_SO4[bin_index_SLE_SO4] += 1

for t in range(n_frames):
    r_SLE_eth = np.linalg.norm(data_SLE_eth[t] - ref_center)
    if r_SLE_eth < r_max:
        bin_index_SLE_eth = int(r_SLE_eth/dr)
        rdf_hist_SLE_eth[bin_index_SLE_eth] += 1

radii = 0.5 * (bin_edges[1:] + bin_edges[:-1])
shell_volumes = (4/3) * np.pi * (bin_edges[1:]**3 - bin_edges[:-1]**3)
ideal_density = tot_num_particles / box_volume

rdf_SLE_SO4 = rdf_hist_SLE_SO4/(shell_volumes*n_frames*ideal_density)
rdf_SLE_eth = rdf_hist_SLE_eth/(shell_volumes*n_frames*ideal_density)

smooth_rdf_SLE_SO4 = gaussian_filter1d(rdf_SLE_SO4, 2)
smooth_rdf_SLE_eth = gaussian_filter1d(rdf_SLE_eth, 2)

plt.plot(radii, smooth_rdf_SLE_SO4, label='SO4_SLE')
plt.plot(radii, smooth_rdf_SLE_eth, label='ether_SLE')
plt.xlabel('Distance from COM of aggregate')
plt.ylabel('g(r)')
plt.title('RDF: SO4/ether of SLES')
plt.grid()
plt.legend()
plt.savefig('SLES_rdf.png')
plt.close()

########################################################################################

############# Calculating COM for CO2 for CAB ##########

def CAB_CO2_COM():
    total_mass_CO2_COM = 0.0
    weighted_x_CO2_COM = 0.0
    weighted_y_CO2_COM = 0.0
    weighted_z_CO2_COM = 0.0
    
    text_file_CAB = open("CAB.pdb", "r")
#    fout3 = open('CAB_COM_CO2.dat', "a")
    Line1 = 0
    Line2 = 14
    
    for index, text in enumerate(text_file_CAB):
        if Line1 <= index <= Line2:
            atom_type_CAB_CO2 = text[76:78].strip()
            mass_CAB_CO2 = atomic_masses[atom_type_CAB_CO2]
            
            x_CAB_CO2 = float(text[30:38])
            y_CAB_CO2 = float(text[38:46])
            z_CAB_CO2 = float(text[46:54])
            
            total_mass_CO2_COM += mass_CAB_CO2
            weighted_x_CO2_COM += mass_CAB_CO2*x_CAB_CO2
            weighted_y_CO2_COM += mass_CAB_CO2*y_CAB_CO2
            weighted_z_CO2_COM += mass_CAB_CO2*z_CAB_CO2
            
            x_com_CAB_CO2 = weighted_x_CO2_COM / total_mass_CO2_COM
            y_com_CAB_CO2 = weighted_y_CO2_COM / total_mass_CO2_COM
            z_com_CAB_CO2 = weighted_z_CO2_COM / total_mass_CO2_COM
            
        elif index > Line2:
#            print(x_com_CAB_CO2,y_com_CAB_CO2,z_com_CAB_CO2, file=fout3)
            total_mass_CAB_CO2 = 0.0
            weighted_x_CAB_CO2 = 0.0
            weighted_y_CAB_CO2 = 0.0
            weighted_z_CAB_CO2 = 0.0
            Line1 = Line1 + 62
            Line2 = Line2 + 62

#    fout3.close()
CAB_CO2_COM()
#################################################################

############# Calculating COM for CH2 for CAB ##########

def CAB_CH2_COM():
    total_mass_CH2_COM = 0.0
    weighted_x_CH2_COM = 0.0
    weighted_y_CH2_COM = 0.0
    weighted_z_CH2_COM = 0.0
    
    text_file_CAB = open("CAB.pdb", "r")
#    fout4 = open('CAB_COM_CH2.dat', "a")
    Line1 = 15
    Line2 = 23
    
    for index, text in enumerate(text_file_CAB):
        if Line1 <= index <= Line2:
            atom_type_CAB_CH2 = text[76:78].strip()
            mass_CAB_CH2 = atomic_masses[atom_type_CAB_CH2]
            
            x_CAB_CH2 = float(text[30:38])
            y_CAB_CH2 = float(text[38:46])
            z_CAB_CH2 = float(text[46:54])
            
            total_mass_CH2_COM += mass_CAB_CH2
            weighted_x_CH2_COM += mass_CAB_CH2*x_CAB_CH2
            weighted_y_CH2_COM += mass_CAB_CH2*y_CAB_CH2
            weighted_z_CH2_COM += mass_CAB_CH2*z_CAB_CH2
            
            x_com_CAB_CH2 = weighted_x_CH2_COM / total_mass_CH2_COM
            y_com_CAB_CH2 = weighted_y_CH2_COM / total_mass_CH2_COM
            z_com_CAB_CH2 = weighted_z_CH2_COM / total_mass_CH2_COM
            
        elif index > Line2:
#            print(x_com_CAB_CH2,y_com_CAB_CH2,z_com_CAB_CH2, file=fout4)
            total_mass_CAB_CH2 = 0.0
            weighted_x_CAB_CH2 = 0.0
            weighted_y_CAB_CH2 = 0.0
            weighted_z_CAB_CH2 = 0.0
            Line1 = Line1 + 62
            Line2 = Line2 + 62

#    fout4.close()
CAB_CH2_COM()
#################################################################

############# Calculating COM for NHCO for CAB ##################

def CAB_NHCO_COM():
    total_mass_NHCO_COM = 0.0
    weighted_x_NHCO_COM = 0.0
    weighted_y_NHCO_COM = 0.0
    weighted_z_NHCO_COM = 0.0
    
    text_file_CAB = open("CAB.pdb", "r")
#    fout5 = open('CAB_COM_NHCO.dat', "a")
    Line1 = 24
    Line2 = 27
    
    for index, text in enumerate(text_file_CAB):
        if Line1 <= index <= Line2:
            atom_type_CAB_NHCO = text[76:78].strip()
            mass_CAB_NHCO = atomic_masses[atom_type_CAB_NHCO]
            
            x_CAB_NHCO = float(text[30:38])
            y_CAB_NHCO = float(text[38:46])
            z_CAB_NHCO = float(text[46:54])
            
            total_mass_NHCO_COM += mass_CAB_NHCO
            weighted_x_NHCO_COM += mass_CAB_NHCO*x_CAB_NHCO
            weighted_y_NHCO_COM += mass_CAB_NHCO*y_CAB_NHCO
            weighted_z_NHCO_COM += mass_CAB_NHCO*z_CAB_NHCO
            
            x_com_CAB_NHCO = weighted_x_NHCO_COM / total_mass_NHCO_COM
            y_com_CAB_NHCO = weighted_y_NHCO_COM / total_mass_NHCO_COM
            z_com_CAB_NHCO = weighted_z_NHCO_COM / total_mass_NHCO_COM
            
        elif index > Line2:
#            print(x_com_CAB_NHCO,y_com_CAB_NHCO,z_com_CAB_NHCO, file=fout5)
            total_mass_CAB_NHCO = 0.0
            weighted_x_CAB_NHCO = 0.0
            weighted_y_CAB_NHCO = 0.0
            weighted_z_CAB_NHCO = 0.0
            Line1 = Line1 + 62
            Line2 = Line2 + 62

#    fout5.close()
CAB_NHCO_COM()
###########################################################################

########### Calculating RDF of SO4 for SLES ##############

data_CAB_CO2 = np.loadtxt("CAB_COM_CO2.dat", dtype=float)
data_CAB_CH2 = np.loadtxt("CAB_COM_CH2.dat", dtype=float)
data_CAB_NHCO = np.loadtxt("CAB_COM_NHCO.dat", dtype=float)
n_frames = len(data_CAB_CO2)
r_max = 40.0                  
nbins = 200
dr = r_max / nbins
bin_edges = np.linspace(0, r_max, nbins + 1)
rdf_hist_CAB_CO2 = np.zeros(nbins)
rdf_hist_CAB_CH2 = np.zeros(nbins)
rdf_hist_CAB_NHCO = np.zeros(nbins)

for t in range(n_frames):
    r_CAB_CO2 = np.linalg.norm(data_CAB_CO2[t] - ref_center) 
    if r_CAB_CO2 < r_max:
        bin_index_CAB_CO2 = int(r_CAB_CO2/dr)
        rdf_hist_CAB_CO2[bin_index_CAB_CO2] += 1

for t in range(n_frames):
    r_CAB_NHCO = np.linalg.norm(data_CAB_NHCO[t] - ref_center)
    if r_CAB_NHCO < r_max:
        bin_index_CAB_NHCO = int(r_CAB_NHCO/dr)
        rdf_hist_CAB_NHCO[bin_index_CAB_NHCO] += 1

radii = 0.5 * (bin_edges[1:] + bin_edges[:-1])
shell_volumes = (4/3) * np.pi * (bin_edges[1:]**3 - bin_edges[:-1]**3)
ideal_density = tot_num_particles / box_volume

rdf_CAB_CO2 = rdf_hist_CAB_CO2/(shell_volumes*n_frames*ideal_density)
rdf_CAB_NHCO = rdf_hist_CAB_NHCO/(shell_volumes*n_frames*ideal_density)

smooth_rdf_CAB_CO2 = gaussian_filter1d(rdf_CAB_CO2, 2)
smooth_rdf_CAB_NHCO = gaussian_filter1d(rdf_CAB_NHCO, 2)

plt.plot(radii, smooth_rdf_CAB_CO2, label='CAB_CO2')
plt.plot(radii, smooth_rdf_CAB_NHCO, label='CAB_NHCO')
plt.xlabel('Distance from COM of aggregate')
plt.ylabel('g(r)')
plt.title('RDF: CO2/NHCO of CAPB')
plt.grid()
plt.legend()
plt.savefig('CAPB-RDF.png')
plt.close()

########################################################################################

########################## head-to-head distance of CAPB molecule ######################

#distance between CT and C312 for CAPB molecule

fout1 = open('head.dat', "a")
fout2 = open('tail.dat', "a")

with open ('CAB.pdb') as f:
    for line in f:
        if "CT" in line:
            x_CT = float(line[30:38])
            y_CT = float(line[38:46])
            z_CT = float(line[46:54])
            print(x_CT,y_CT,z_CT, file=fout1)
        if "C312" in line:
            x_C312 = float(line[30:38])
            y_C312 = float(line[38:46])
            z_C312 = float(line[46:54])
            print(x_C312,y_C312,z_C312, file=fout2)
fout1.close()
fout2.close()

head_CAB = np.loadtxt("head.dat", dtype=float)
tail_CAB = np.loadtxt("tail.dat", dtype=float)

def head_to_head_CAB(head_CAB,tail_CAB):
    dist = head_CAB - tail_CAB
    dist_CAB = np.linalg.norm(dist, axis=1)
    return(dist_CAB)

dist_hist_CAB=head_to_head_CAB(head_CAB,tail_CAB)

plt.hist(dist_hist_CAB, bins=20, color='skyblue', edgecolor='black')
plt.xlabel('distance (ang)')
plt.ylabel('frequency')
plt.title('head-to-head distance in CAPB')
plt.savefig('head-to-head-dist-CAPB.png')
plt.show()

##################################################################################################

#distance between CT and C312 for SLES molecule (end-end-distance)

fout1 = open('head_SLES.dat', "a")
fout2 = open('tail_SLES.dat', "a")

with open ('SLE.pdb') as f:
    for line in f:
        if " S " in line:
            x_S = float(line[30:38])
            y_S = float(line[38:46])
            z_S = float(line[46:54])
            print(x_S,y_S,z_S, file=fout1)
        if " C12 " in line:
            x_C12 = float(line[30:38])
            y_C12 = float(line[38:46])
            z_C12 = float(line[46:54])
            print(x_C12,y_C12,z_C12, file=fout2)
fout1.close()
fout2.close()

head_SLES = np.loadtxt("head_SLES.dat", dtype=float)
tail_SLES = np.loadtxt("tail_SLES.dat", dtype=float)

def head_to_head_SLES(head_SLES,tail_SLES):
    dist = head_SLES - tail_SLES
    dist_SLES = np.linalg.norm(dist, axis=1)
    return(dist_SLES)

dist_hist_SLES=head_to_head_SLES(head_SLES,tail_SLES)

plt.hist(dist_hist_SLES, bins=20, color='skyblue', edgecolor='black')
plt.xlabel('distance (ang)')
plt.ylabel('frequency')
plt.title('head-to-head distance in SLES')
plt.savefig('head-to-head-dist-SLES.png')
plt.show()

#==================================================================================
