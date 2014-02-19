
'''
will some day be a library of regression functions 

A. Richards
'''

### make imports
import numpy as np 
import sys,numpy,scipy.stats

def get_1D_linear_fit(xdata,ydata):
    matrix = []

    if type(xdata) != np.array([]):
        xdata = np.array([xdata]).transpose()

    n,d = xdata.shape

    for i in range(n):
        matrix.append([1.0, xdata[i,0]]) # for y = a + bx

    coeffs = scipy.linalg.basic.lstsq(matrix,ydata)[0]
    #print "fitting data to simple line equation y = a + bx"

    yFit =coeffs[0] + (coeffs[1] * xdata)

    return yFit,coeffs

def get_3D_linear_fit(xdata,ydata):
    matrix = []
    n,d = xdata.shape

    # for t = m0 + (m1 * x1) + (m2 * x2) + (m3 * x3) 
    for i in range(n):
        matrix.append([1.0, x[i,0], x[i,1], x[i,2]]) 

    coeffs = scipy.linalg.basic.lstsq(matrix,ydata)[0]
    print "fitting data to equation: t = m0 + (m1 * x1) + (m2 * x2) + (m3 * x3)"
    yFit = coeffs[0] + (coeffs[1] * xdata[:,0]) + (coeffs[2] * xdata[:,1]) + (coeffs[3] * xdata[:,2])
    return yFit,coeffs

def get_quadratic_fit(self,xdata_orig,ydata_orig):

    matrix = []
    for x in xdata:
        matrix.append([1.0, x,x**2]) # for y = a + bx + cx^2

    coeffs = scipy.linalg.basic.lstsq(matrix,ydata)[0]
    print "fitting data to equation y = a + bx + cx^2"

    yFit =coeffs[0] + (coeffs[1] * xdata) + (coeffs[2] * xdata**2)

    return yFit,coeffs
