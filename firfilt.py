#!/bin/usr/env python3

import numpy as np
from scipy.signal import upfirdn


def firfilt(bb, xx):
    """ FIRFILT   FIR filter implemented as a difference equation

    usage:   yy = firfilt(bb, xx)

    implements the FIR filter difference equation:

                   M-1
                   __
                   \
           y[n]=   /  b[k] * x[n-k]
                   --
                   k=0

     The length of the resulting vector is  length(bb)+length(xx)-1.

    """
    bb = np.asarray(bb)
    xx = np.asarray(xx)

    y = upfirdn(bb, xx)

    return y