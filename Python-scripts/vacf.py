#!/usr/bin/env python

#######   PLEASE READ THE FOLLOWING INSTRUCTION BEFORE RUNNING SCRIPT   #######
###                                                                         ### 
###  NOTE: The position file needs to align before run total VACF script!!  ###
###                                                                         ###
###    The Format for Running This Script:                                  ###
###    ./VACF_KW.py INPUT_FILE_NAME DELTA_T OUTPUT_FILE_NAME                ###
###                                                                         ###
###    The values need to input manually when runing this script            ###
###                                                                         ### 
###    (1) INPUT_FILE_NAME: The POSITION.xyz file                           ###
###                     (NOTE: do NOT need to re-split the Position file)   ###
###                                                                         ###
###    (2) DELTA_T: The Time_step set in simulation, in unit of fs          ###
###                                                                         ###
###    (3) OUTPUT_FILE_NAME: The Name of the Output File.                   ###
###                    (NOTE: do NOT need to type ">" sign!)                ###
###                                                                         ###
###    After inputing the above mentioned values, the program will list     ### 
###  the atoms and their corresponding indices (only the first 35 atoms     ###
###  will show if the system is too large).                                 ###
###    And then the program will ask the user to enter the type of mode,    ###
###  e.g. "s": stretch, "b": bend, "w": wag, ect. and the indices of the    ###
###  atoms in order to choose the group of atoms involve the mode (the      ###
###  partial VACF). If the user enter "all" or "-1", the program will       ###
###  choose all atoms to calcluate the total VACF.                          ### . 
###    Consequently, the program will ask the user to enter the type of     ###
###  window function, e.g. "Gaussian", "BlackmanHarris", "Hamming "or       ###
###  "Hann", ect.                                                           ###    
###    After all steps of inputs finishing, the calculation begins.         ### 
###  (https://github.com/LePingKYXK/Velocity-ACF/blob/master/VACF.py)       ###
###                                                                         ###
###############################  Let's Try It! ################################


from __future__ import division
from scipy import signal
import math
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import sys
import time

fname = sys.argv[1]
delta_t = float(sys.argv[2]) * 1e-15
fout = sys.argv[3]




#### The functions will be used are listed as follows

def information(fname):
    ''' fetch the munber of atoms and the elements information
    from the first block of the input file. It looks duplicate,
    but it would be more convenient for the following steps.
    '''
    elements = []
    with open(fname,'r') as fo:
        Natom = int(fo.next())
        fo.next()
        for i in xrange(Natom):
            line = fo.next()
            info = line.split()[0]
            elements.append(info)
    elements = np.array(elements)
    indices = np.where(elements)[0]
    return (Natom, elements, indices)


def screen_print(Natom, elements, indices):
    species = set(elements)
    fmt1 = 'There are {:d} kinds of elements, which are '\
            + '{:s}, ' * len(species)
    print "\nNumber of atoms in this system: ", Natom
    print fmt1.format(len(species), *species)

    if len(elements) >= 30:
        print "Too many elements in this system," \
              " only the first 30 elements will print on the screen."
        print "The elements and the corresponding indices are: "
        pfmt2 = 'Element:' + '{:>3s}, ' * len(elements[:30])
        pfmt3 = ' Index: ' + '{:>3d}, ' * len(indices[:30])
        print pfmt2.format(*elements[:30])
        print pfmt3.format(*indices[:30])
    elif len(elements) < 30:
        print "The elements and the corresponding indices are: "
        pfmt2 = 'Element:' + '{:>3s}, ' * len(elements)
        pfmt3 = ' Index: ' + '{:>3d}, ' * len(indices)
        print pfmt2.format(*elements)
        print pfmt3.format(*indices)
    else: #### e.g. elements == []
        sys.exit("WARNING! No element! Please check the input file.")


selection_notes = "\n  (NOTE: The input values are the IDs of the molecule,"\
                  " which should in range from 0 to the max N of the system.\n"\
                  "         The total number of your inputs should in range 2 to 4 (including boundary).\n"\
                  "         Here, 2 digitals (IDs) represent the diatomic stretch, \n"\
                  "               3 digitals (IDs) mean the bend mode (triatomic angle), \n"\
                  "               4 digitals (IDs) indicate the dihedral angle,\n"\
                  "\n  Please enter the IDs: \n"
def select_atoms(selection_notes):
    mode_available = ('s','b','w','r')
    custom_inputs = raw_input(selection_notes)
    fmt = '\n The indices of the atoms you chose are: '\
              + '{:s} ' * len(custom_inputs)
    print fmt.format(*custom_inputs)
    print "Program will deal with the selected atoms according to your inputs.\n"
    #print "\n ###########", custom_inputs, type(custom_inputs)
    #print "@@@@@@@", len(custom_inputs[1:]) <= 4
    if custom_inputs == "all" or custom_inputs == "-1":
        return ("mode", Natom)
    elif custom_inputs[0] in mode_available \
         and max(map(int, custom_inputs[1:].split())) <= Natom \
         and len(custom_inputs[1:].split()) <= 4:
        mode, sel = custom_inputs[0], custom_inputs[1:]
        #print "custom_inputs", custom_inputs, type(custom_inputs)
        #print "mode", mode
        #print  "selected atoms", sel
        return (mode, map(int, sel.split()))


def read_data(fname, sel):
    with open(fname, 'r') as fo:
        timestep = 0
        coords = []
        
        for line in fo:
            try:
                fo.next()
            except StopIteration:
                break
            if isinstance(sel, int) and sel == Natom:
                for n in xrange(sel):
                    line = fo.next()
                    info = line.split()
                    coords.append(info[1:])
                timestep += 1
        
            elif isinstance(sel, list) and len(sel) >= 2:
                for k in xrange(max(sel) + 1):
                    line = fo.next()
                    info = line.split()
                    coords.append(info[1:])
                timestep += 1
                try:
                    for k in xrange(Natom - max(sel) - 1):
                        fo.next()
                except StopIteration:
                    break
        coords = np.asfarray(coords, dtype=np.float64).reshape(timestep,-1,3)
    #if isinstance(sel, list) and len(sel) == 1 and sel[0] == Natom:
    if isinstance(sel, int) and sel == Natom:
        return coords
    elif isinstance(sel, list) and len(sel) >= 2:
        return coords[:,np.array(sel),:]
    




def calc_derivative(array_1D, delta_t):
    ''' The derivatives of the angle_array were obtained by using the
    finite differences method.
    '''
    dx = np.repeat(delta_t, len(array_1D))
    return np.gradient(array_1D, dx)


def calc_bond(data):
    return np.linalg.norm((data[:,0,:] - data[:,1,:]), axis=1)


def calc_angle(data):
    v1 = data[:,0,:] - data[:,1,:]
    v2 = data[:,2,:] - data[:,1,:]
    
    dot = (v1 * v2).sum(axis=1)
# calculate the dot product using Einstein summation
#    dot = np.einsum("ij,ij->i", v1,v2)

    norm1 = np.linalg.norm(v1,axis=1)
    norm2 = np.linalg.norm(v2,axis=1)
    theta = np.arccos(dot/(norm1 * norm2))
    return np.degrees(theta)


def calc_dihedral(data):
    ''' The order of the input elements is the natural definition.
    A --> B --> C --> D
    '''
    v1 = data[:,1,:] - data[:,0,:]
    v2 = data[:,2,:] - data[:,1,:]
    v3 = data[:,3,:] - data[:,2,:]

    n1 = np.cross(v1,v2)
    n2 = np.cross(v2,v3)

    dot = (n1 * n2).sum(axis=1)
    norm1 = np.linalg.norm(n1,axis=1)
    norm2 = np.linalg.norm(n2,axis=1)
    
    phi = np.arccos(dot / (norm1 * norm2))
    return np.degrees(phi)


def calc_wag(data):
    ''' The order for the wag or "rock" mode is first choose the angle of 3 atoms,
    and then choose one atom of the "handle".
    
    '''
    v1 = data[:,0,:] - data[:,1,:]
    norm1 = np.linalg.norm(v1,axis=1)
#    v1 = v1 / norm1[:,np.newaxis]
    
    v2 = data[:,2,:] - data[:,1,:]
    norm2 = np.linalg.norm(v2,axis=1)
#    v2 = v2 / norm2[:,np.newaxis]

    v_sum = v1 + v2
    norm_sum = np.linalg.norm(v_sum,axis=1)

    v3 = data[:,3,:] - data[:,1,:]
    norm3 = np.linalg.norm(v3,axis=1)
#    v3 = v3 / norm3[:,np.newaxis]
    
    dot = (v_sum * v3).sum(axis=1)
    theta = np.arccos(dot / (norm_sum * norm3))
    return np.degrees(theta)


window_function_name = '\n  Please enter the name of the window function.\n'\
                       '  Gaussian, Hamming, Hann, Blackman-Harris.\n'

standard = '\n Please enter a number in range 500--4000.\n'\
           '  The larger the number, the narrower the line-shape.\n'\
           '  (e.g. the value of 4000 produces FWHM around 10 cm^-1 for a 20-ps-traj.)\n'

def choose_window(data, window_function_name):
    kind = raw_input(window_function_name)
    if kind == 'Gaussian':
        sigma = 2 * math.sqrt(2 * math.log(2))
        std = float(raw_input(standard))
        window_function = signal.gaussian(len(data), std/sigma, sym=False)
    
    elif kind == 'Blackman-Harris':
        window_function = signal.blackmanharris(len(data), sym=False)
    
    elif kind == 'Hamming':
        window_function = signal.hamming(len(data), sym=False)
    
    elif kind == 'Hann':
        window_function = signal.hann(len(data), sym=False)
    
    return window_function


def zero_padding(sample_data):
    ''' A series of Zeros will be padded to the end of the dipole moment
    array (before FFT performed), in order to obtain a array with the
    length which is the "next power of two" of numbers.
    
    #### Next power of two is calculated as: 2**math.ceil(math.log(x,2))
    #### or Nfft = 2**int(math.log(len(data_array)*2-1, 2))
    '''
    return int(2 ** math.ceil(math.log(len(sample_data), 2)))


def calc_ACF(array_1D):
    # Normalization
    yunbiased = array_1D - np.mean(array_1D, axis=0)
    ynorm = np.sum(np.power(yunbiased,2), axis=0)
#    print "the average value of input data array", ynorm
    
    autocor = signal.fftconvolve(array_1D,
                                 array_1D[::-1],
                                 mode='full')[len(array_1D)-1:] / ynorm
    return autocor


def calc_FFT(array_1D, window):
    '''
    This function is for calculating the "intensity" of the ACF at each frequency
    by using the discrete fast Fourier transform.
    '''
####
#### http://stackoverflow.com/questions/20165193/fft-normalization
####
    #window = choose_window(array_1D, "Gaussian")
    WE = sum(window) / len(array_1D)
    wf = window / WE
    # convolve the blackman-harris window function.
    
    sig = array_1D * wf
	
    # A series of number of zeros will be padded to the end of the \
    # VACF array before FFT.
    N = zero_padding(sig)

    yfft = np.fft.fft(sig, N, axis=0) / len(sig)
#    yfft = np.fft.fft(data, n=int(N_fft), axis=0)/len(data) # no window func.
    print "shape of yfft", np.shape(yfft)
    return np.square(np.absolute(yfft))


def save_results(fout, wavenumber, intensity):
    with open(fout, "w") as fw:
        title = ("Wavenumber", "IR Intensity", "cm^-1", "a.u.")
        np.savetxt(fout, np.c_[wavenumber,intensity],
                   fmt="%10.5f %15.5e",
                   header="{0:>10}{1:>16}\n{2:^11}{3:^20}".format(*title),
                   comments='')


######## Plot The Spectrum by Using Matplotlib module ########
def visualization(derivative, ACF, wavenumber, intensity):
    derivative = derivative * delta_t
    plt.subplot(3,1,1)
    L1 = np.arange(len(derivative))
    plt.plot(L1, derivative, color='red', linewidth=1.5)
    plt.axis([0, len(derivative), 
              1.1*np.min(derivative), 1.1*np.max(derivative)], fontsize=15)
    plt.xlabel("Data Points", fontsize=15)
    plt.ylabel("Derivative of Dipole (a.u.)", fontsize=15)

    plt.subplot(3,1,2)
    L2 = np.arange(len(ACF))
    plt.plot(L2, ACF, color='red', linewidth=1.5)
    plt.axis([0, len(ACF), 1.1*np.min(ACF), 1.1*np.max(ACF)], fontsize=15)
    plt.xlabel("Data Points", fontsize=15)
    plt.ylabel("vel-VACF (a.u.)", fontsize=15)

    plt.subplot(3,1,3)
    plt.plot(wavenumber, intensity, color='black', linewidth=1.5)
    plt.axis([0, 4000,
              np.min(intensity), 1.1*np.max(intensity[:4001])],fontsize=15)
    plt.xlabel("Wavenumber (cm$^{-1}$)", fontsize=15)
    plt.ylabel("Intensity (a.u.)", fontsize=15)
    plt.subplots_adjust(hspace = 0.5)
    plt.show()



########################
#delta_t = 0.5 * 1e-15
#Fs = 1/delta_t
#T = 50.0
#scaling_factor = 0.968

######## The constants will be used in this script ########
c = 2.9979245899e10 # speed of light in vacuum in [cm/s], from Wikipedia.
#kB = 0.6950347      # Boltzman constant in [cm^-1/K], from Wikipedia.
#h_bar = 6.283185    # Reduced Planck constant in atomic unit, where h == 2*pi
#beta = 1.0/(kB * T) #                        




######## The main program ########
if __name__ == "__main__":
    Natom, elements, indices = information(fname)
    screen_print(Natom, elements, indices)
    # Test. Input 3 numbers in range from 0 to 8.
    mode, sel = select_atoms(selection_notes)
    print "selected atoms", sel
    
    start = time.clock()
    
    data = read_data(fname, sel)
    #print "check point 01: data", data, np.shape(data)
    # data is a 3-D array contained coordinates of selected atoms in whole trajectory.
    read_data_time = time.clock() - start

    print "\nData-reading Completed! \
           Used time: %.5f second.\
           \nThe trajectory has %d time steps" %(read_data_time, len(data))

    window = choose_window(data, window_function_name)
    parsing = time.clock()

    if sel == Natom:
        print "Program will deal with all atoms one by one."
        for i in range(len(data[0,:,:])):
            print '\n The atom %d has Completed.' %i
            normal_vectors = np.linalg.norm(data, axis=-1)
            #print "#### shape of the normal_vectors #####", np.shape(normal_vectors)
            print "#== The shape of the each atom array ==#", np.shape(normal_vectors[:,i])
            derivative = calc_derivative(normal_vectors[:,i], delta_t)
            ACF = calc_ACF(derivative)
            #print "#=== shape of the ACF ===#", np.shape(ACF)
            yfft_i = calc_FFT(ACF, window)
            if i == 0:
                yfft = yfft_i
            else:
                yfft += yfft_i
        print "\ncheck point 04: yfft = \n", yfft, np.shape(yfft)
        
    else:
        if mode == 's' and len(sel) == 2:
            values = calc_bond(data)
        elif mode == 'b' and len(sel) == 3:
            values = calc_angle(data)
        elif mode == 'r' and len(sel) == 4:
            values = calc_dihedral(data)
        elif mode == 'w' and len(sel) == 4:
            values = calc_wag(data)
        else:
            print "Error!"
        # All values are 1-D data-arrays.
        derivative = calc_derivative(values, delta_t)
        ACF = calc_ACF(derivative)
        yfft = calc_FFT(ACF, window)
        
    wavenumber = np.fft.fftfreq(len(yfft), delta_t * c)[0:int(len(yfft) / 2)]
#    wavenumber = wavenumber * scaling_factor

    intensity = yfft[0:int(len(yfft)/2)]

    #### Normalized the intensity
#    norm_intensity = intensity / max(intensity)
    save_results(fout,wavenumber,intensity)
    finish = time.clock()
    print "Work Completed! Used time: %.5f second." %(finish - parsing)
    visualization(derivative, ACF, wavenumber, intensity)
