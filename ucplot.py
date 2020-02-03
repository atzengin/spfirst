#!/bin/usr/env python3

import numpy as np
import matplotlib.pyplot as plt


def ucplot(radius, center=None, arg3=None):
    """UCPLOT   Plot a circle with specified center and radius
    usage:
        huc = ucplot( radius, center, linetype )
        radius: (default = 1)
        center: complex number (x+j*y) (default = 0)
        linetype: any valid MATLAB type (see help plot)
            huc: handle to plot of the circle

	See also ZVECT
    """

    linetype = 'b:'
    rad = 1.0
    cent = 0

    if None in (center, arg3):
        if type(radius) == str:
            print('raduis')
            linetype = radius;
        else:
            rad = radius
    elif center is not None and arg3 is None:
        rad = radius
        if type(center) == str: linetype = center
        else: cent = center
    if not None in (radius, center, arg3):
        rad = radius; cent = center; linetype = arg3

    ucircle = rad * np.exp(1j * np.linspace(0, 2*np.pi, 100)) + cent;
    
    u = plt.plot(ucircle.real, ucircle.imag, linetype)
    plt.axis('equal')
    plt.show()

    return u