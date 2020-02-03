#!/bin/usr/env python3 

import numpy as np
from pkpick import pkpick


def pkinterp(x, locs=None):
    """PKINTERP     interpolate to refine a peak position

   usage:  [peaks,pos] = pkinterp( x, locs )

         peaks    =  peak values
         pos      =  location of peaks (between samples)
         x        =  input data  (if complex, operate on mag)
         locs     =  location of peaks (from PKPICK)
                      if this arg not present, call pkpick

   see also PKPICK
   """
    x = np.asarray(x)

    if x.ndim == 1:
        x = np.array([x])

    if locs is None:
        tt, locs = pkpick(x)

    M, N = x.shape
    if M == 1:
        x = x.T
        M, N = x.shape

    if np.any((np.imag(x) != 0)):
        x = abs(x)
    pos = []
    peaks = []
    for kk in range(N):
        ii = np.where(locs[:, kk] == 0)
        if not np.size(ii) == 0:
            peaks = np.zeros((np.amax(ii[0]) + 1, kk + 1))
            pos = np.zeros((np.amax(ii[0]) + 1, kk + 1))
            pos[ii[0], kk] = 0
            peaks[ii[0], kk] = x[ii[0], kk]

        ii = np.where((locs[:, kk] == M - 1))
        if not np.size(ii) == 0:
            peaks = np.zeros((np.amax(ii[0]) + 1, kk + 1))
            pos = np.zeros((np.amax(ii[0]) + 1, kk + 1))
            pos[ii[0], kk] = M - 1
            peaks[ii[0], kk] = x[ii[0], kk]

        ii = np.where(np.logical_and(locs[:, kk] != 1, locs[:, kk] != M - 1))
        jj = locs[ii, kk].astype(int)

        alfa = -x[jj, kk] + 0.5 * x[jj - 1, kk] + 0.5 * x[jj + 1, kk]

        if np.any(alfa > 0):
            print('PKINTERP: trying to fit a valley (alfa>0)')
        beta = 0.5 * (x[jj + 1, kk] - x[jj - 1, kk])
        pos[ii[0], kk] = jj - 0.5 * beta / (alfa + (alfa == 0)) * (alfa < 0)
        peaks[ii[0], kk] = x[jj, kk] - 0.25 * beta * beta / alfa

    return pos, peaks
