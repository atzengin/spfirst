#!/bin/usr/env python3

import matplotlib.pyplot as plt
import matplotlib as mat
import numpy as np
from math import isnan, sqrt


def zvect(zFrom, zTo=None, arg3=None, arg4=None):
    """ZVECT   Plot vectors in complex z-plane from zFrom to zTo

    common usage:  zvect(Z) 
        displays each element of Z as an arrow emanating from the origin.

    usage:   HV = zvect(zFrom, <zTo>, <LTYPE>, <SCALE>)

        zFrom:  is a vector of complex numbers; each one will be
                the starting location of an arrow.
        zTo:  is a vector of complex numbers; each one will be
                the ending point of an arrow starting at zFrom.
        LTYPE: string containing any valid line type (see PLOT)            
        SCALE: controls size of arrowhead (default = 1.0)
                (order of LTYPE and SCALE args doesn't matter)
            HV: output handle from graphics of vector plot

        ** If either zFrom or zTo is a scalar all vectors will
            start or end at that point.

        See also ZCAT.
    """
    zFrom = np.asarray(zFrom)
    zTo = np.asarray(zTo)
    scale = 1.0
    linetype = 'b-'
    if zTo is None:
        zTo = zFrom; zFrom = 0*zTo
    elif zTo is not None:
        if type(zTo) == str:
            linetype = zTo; zTo = zFrom; zFrom = 0*zTo
        elif len(zTo) == 0:
            zTo = zFrom; zFrom = 0*zTo
        elif len(zTo) == 1:
            zTo = zTo * np.ones(zFrom.shape)
    elif zTo and arg3 is not None:
        if type(arg3) == str:
            linetype = arg3
        else:
            scale = arg3
    else:
        if type(arg3) == str:
            linetype = arg3; scale = arg4
        else:
            scale = arg3; linetype = arg4
    
    jkl = np.where(np.logical_not(np.isnan(zTo - zFrom)))[0]
    if len(jkl) == 0:
        exit('cannot plot NaNs')

    zTo = zTo[jkl]
    zFrom = zFrom[jkl]
    if len(zFrom) == 1:
        zFrom = zFrom * np.ones(zTo.shape)
    elif len(zTo) == 1:
        zTo = zTo * np.ones(zFrom.shape)
    
    if len(zFrom) != len(zTo):
        exit('ZVECT: zFrom and zTo must be same length.')
    
    tt = np.r_[zFrom, zTo]
    # zmx = max(abs(tt))
    jkl = np.where(tt == max(tt))[0]
    figsize = max(abs(tt - tt[jkl]))
    arrow = scale * (np.vstack((-1, 0, -1)) + 1j*np.vstack((1/4,0,-1/4)))
    
    dz = zTo - zFrom
    dzm = abs(dz)
    zmax = max(dzm)
    zscale = np.mean(np.r_[zmax, figsize])
    scz = 0.11 + 0.77 * (dzm / zscale -1) ** 6
    tt = np.array(np.ones((3,1))* zTo + arrow * (scz * dz))

    h = plt.plot(np.vstack((zFrom, zTo)).real, np.vstack((zFrom, zTo)).imag, linetype, tt.real , tt.imag, linetype)
    num_zzz = len(zFrom)

    for kk in range(num_zzz):
        kolor = plt.get(h[kk], 'color')
        plt.setp(h[kk+num_zzz], 'color', kolor)
    
    plt.axis('equal')


    plt.show()
    return h