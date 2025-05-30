import pandas as pd
from scipy.optimize import leastsq
import numpy as np
np.set_printoptions(threshold=np.inf)
df = pd.read_csv('helmholtz-volume.dat', delim_whitespace = True, comment = '#', chunksize = 9)

def Vinet(parameters, vol):
    'From Phys. Rev. B 28, 5480 (1983)'
    E0, B0, BP, V0 = parameters

    x = (vol / V0) ** (1.0 / 3)
    xi = 3.0 / 2 * (BP - 1)

    E = E0 + 9 * B0 * V0 / (xi**2) * (1 + (xi * (1 - x) - 1) * np.exp(xi * (1 - x)))
    
    return E

def objective(pars, y, x):
    err =  y - Vinet(pars, x)
    return err

for chunk in df:
	energy = chunk['H'].values
	vols = chunk['V'].values
	e1 = energy[4]
	v1 = vols[4]
	x0 = [e1, 1.0, 4.0, v1]
	plsq = leastsq(objective, x0, args=(energy, vols))
	print 'Fitted parameters = {0}'.format(plsq[0])
