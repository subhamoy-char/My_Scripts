import sys
import numpy as np  # Importing the numpy library for handling arrays and mathematical operations
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq, fftshift
from scipy.ndimage import gaussian_filter
from scipy import integrate
import math

np.set_printoptions(suppress=True,threshold=sys.maxsize)
vacf_array = np.loadtxt('fft_input.dat', usecols=1)
time_array = np.loadtxt('fft_input.dat', usecols=0)
freq_pnma = np.loadtxt('total_dos-Pnma.dat', usecols=0, skiprows=0)
gw_pnma = np.loadtxt('total_dos-Pnma.dat', usecols=1, skiprows=0)
N = 500
T = 0.014
y_ft = fft(vacf_array)
x_ft = fftfreq(N, T)[:N//2]
print(x_ft)
raw_data = 2.0/N * np.abs(y_ft[:N//2])
print(integrate.simpson(gw_pnma))
plt.plot(x_ft, gaussian_filter(raw_data/np.max(raw_data),sigma=1.0))
plt.plot(freq_pnma,gw_pnma/np.max(gw_pnma))
plt.grid()
plt.show()
