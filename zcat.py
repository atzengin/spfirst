#!/bin/usr/env python3

import numpy as np
from zvect import zvect
import matplotlib.pyplot as plt


def zcat(z, arg2=None, arg3=None):
    """ZCAT   Plot vectors in z-plane end-to-end

    usage:    hv = zcat(Z, <LTYPE>, <SCALE>)

        Z = vector of complex numbers; each complex # is displayed
            as a vector, with the arrows placed end-to-end
        LTYPE: string containing any valid line type (see PLOT)            
        SCALE: varies size of arrowhead (default = 1.0)
            (order of LTYPE and SCALE args doesn't matter)
        hv: output handle from graphics of vector plot

	See also ZVECT
    """

    z = np.asarray(z)
    linetype = 'b-'
    scale = 1.0

    if arg2 is not None and arg3 is None:
        if type(arg2) == str:
            linetype = arg2
        else:
            scale = arg2

    elif (arg2 is not None and arg3 is not None):
        if type(arg3) == str:
            linetype = arg2; scale = arg3
        else:
            linetype = arg3; scale = arg2

    z2 = np.cumsum(z)
    L = len(z2)
    z1 = np.append([0], z2[0:L - 1])
    print(z2)
    h = zvect(z1, z2, linetype, scale)
    plt.show()

    return h