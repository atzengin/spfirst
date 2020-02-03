#!/bin/usr/env python3

import numpy as np
from mattostr import mattostr
from math import pi


def zprint(z):
    """ZPRINT   printout complex # in rect and polar form

    usage:   zprint(z)
    z = vector of complex numbers; each one will be printed
        in a format showing real, imag, mag and phase
    """
    z = np.asmatrix(z)
    sz = np.size(z)
    one = mattostr(np.c_[z.real.reshape(sz, 1), z.imag.reshape(sz,1), abs(z).reshape(sz,1)], '%8.4g')
    two = mattostr(np.c_[np.angle(z).reshape(sz, 1), (np.angle(z)/pi).reshape(sz, 1)], '%9.3f')
    three = mattostr((np.angle(z)*180/pi).reshape(sz, 1), '%9.2f')
    final = np.c_[one, two, three]

    print(' Z =     X    +      jY     Magnitude    Phase      Ph/pi   Ph(deg)')
    print(final)
    print(' ')