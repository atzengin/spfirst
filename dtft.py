#!/bin/usr/env python3

from math import pi, ceil

import numpy as np


def dtft(h, N):
    """DTFT   calculate DTFT at N equally spaced frequencies
  Usage:   [H, W] = dtft(h, N)
    h : finite-length input vector, whose length is L
    N : number of frequencies for evaluation over [-pi,pi)
          ==> constraint: N >= L
    H : DTFT values (complex)
    W : (2nd output) vector of freqs where DTFT is computed

    """

    h = np.asarray(h)
    N = int(np.fix(N))
    L = len(h)
    if N < L:
        print('DTFT: # data samples cannot exceed # freq samples')
    W = (2 * pi / N) * np.arange(0, N, 1)
    mid = int(ceil(N / 2) + 1)
    W[mid - 1:N] = W[mid - 1:N] - 2 * pi
    W = np.fft.fftshift(W)
    H = np.fft.fftshift(np.fft.fft(h, N))
    return H, W