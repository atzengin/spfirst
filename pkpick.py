#!/bin/usr/env python3

from math import inf, pi

import numpy as np


def pkpick(x, thresh=-inf, number=-1):
    """PKPICKER      pick out the peaks in a vector
    Usage:  [peaks,locs] = pkpick( x, thresh, number )
        peaks   :  peak values
        locs    :  location of peaks (index within a column)
        x       :  input data  (if complex, operate on mag)
        thresh  :  reject peaks below this level
        number  :  max number of peaks to return

    see also PKINTERP
    """

    x = np.asarray(x)
    if x.ndim == 1:
        x = np.asarray([x])
    M, N = x.shape
    if M == 1:
        x = x.transpose()  # Make it a single column
        M, N = x.shape
    if np.any((np.imag(x) != 0)):
        x = abs(x)

    for kk in range(N):
        mask = np.diff(np.sign(np.diff(np.r_[x[0, N - 1] - 1, x[:, N - 1], x[M - 1, N - 1] - 1])))
        mask.shape = (len(mask), 1)

        # expected value : jkl[0] = row numbers & jkl[1] = column numbers
        jkl = np.where(np.logical_and(mask < 0, x >= thresh))

        if number > 0 and len(jkl) >= thresh:
            # tt = np.sort(-x[jkl])         # not used
            ii = np.argsort(-x[jkl])
            jkl = jkl[ii[np.arange(0, number)]]
            jkl = np.sort(jkl)  # Sort by index

        L = len(jkl[0])

        peaks = np.zeros((L, N))
        locs = np.zeros((L, N))
        peaks = np.array(peaks) + np.array(x[jkl]).reshape(len(jkl[0]), 1)
        locs = np.array(locs) + np.array((jkl[0] * jkl[1]) + (jkl[0] + jkl[1])).reshape(len(jkl[0]), 1)

    return peaks, locs