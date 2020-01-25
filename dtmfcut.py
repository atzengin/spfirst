#!/bin/usr/env python3


from math import pi
from scipy.signal import upfirdn
import numpy as np


def dtmfcut(xx, fs):
    """DTMFCUT   find the DTMF tones within x[n]
    usage:
        indx = dtmfmain(xx,fs)

    length of nstart = M = number of tones found
        nstart is the set of STARTING indices
        nstop is the set of ENDING indices
        xx = input signal vector
        fs = sampling frequency

    Looks for silence regions which must at least 10 millisecs long.
    Also the tones must be longer than 100 msec
    """
    xx = np.asarray(xx)

    xx = (xx / max(np.abs(xx)))     # normalize xx
    Lx = len(xx)

    if (0.01 * fs) == 0.5:
        Lz = 1
    else:
        Lz = round(0.01*fs)

    setpoint = 0.02     # make everything below 2% zero
    xx = upfirdn(np.ones(Lz)/ Lz, np.abs(xx))
    xx = np.diff(((xx > setpoint) * 1))
    jkl = np.asarray(np.where(xx != 0))

    if xx[jkl.take(0)] < 0:
        jkl = np.insert(jkl, 0, 1)
    if x[jkl.take(-1)] > 0:
        jkl = np.append(jkl, Lx-1)

    indx = np.array([-1, -1]).reshape(2,1)
    while len(jkl) > 1:
        if jkl[1] > (jkl[0] + 10 * Lz):
            indx = np.append(indx, np.vstack((jkl[[0, 1]])), axis=1)
        jkl = np.delete(jkl, [0, 1])

    nstart = indx[0,1:]
    nstop = indx[1,1:]
    return nstart, nstop