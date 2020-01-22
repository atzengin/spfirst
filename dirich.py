#!/usr/bin/env python3

import numpy as np


def dirich(omega, L):
    """
    DIRICH   compute sin(L*omega/2)/Lsin(omega/2)   
    ------
    Usage :   D = dirich(omega, L)

    omega : argument of Dirichlet function   (works for matrix omega)
    L     : length of corresponding FIR filter

    """

    denom = np.sin(0.5 * np.asarray(omega))
    zdenom = abs(denom) < 1e-10
    D = zdenom + np.logical_not(zdenom) * np.sin((L / 2) * np.array(omega)) / (L * denom + zdenom)
    return D