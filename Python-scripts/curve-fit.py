# This is the curve fit of Migules regular solution model. The W1 and W2 value for LaPO4-ZrSiO$ solid solution model are 3.27 and 3.40. The W1 and W2 value for GdPO4-ZrSiO$ solid solution model are 1.15 and 1.16. The W1 and W2 value for YbPO4-ZrSiO$ solid solution model are 0.54 and 0.54.

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

xdata = [0.0625, 0.125, 0.250, 0.500, 0.750, 0.875, 0.9375]
ydata = [0.0450, 0.0981, 0.0968, 0.1015, 0.1025, 0.0916, 0.0420]

xdata = np.asarray(xdata)
ydata = np.asarray(ydata)

def Fitting(x,W1,W2):
    y = (W1*(1-x)+W2*x)*x*(1-x)
    return y

parameters, covarience = curve_fit(Fitting,xdata,ydata)
fit_A = parameters[0]
fit_B = parameters[1]
print(fit_A)
print(fit_B)

fit_y = Fitting(xdata,fit_A,fit_B)

plt.plot(xdata, ydata, 'o')
plt.plot(xdata,fit_y,'-')
plt.show()
