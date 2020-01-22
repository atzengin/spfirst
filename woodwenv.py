#!/usr/bin/env python3

import numpy as np


def woodwenv(a, s, r, Fs):
    """
     WOODWENV	produces amplitude and mod. index envelope functions
          for woodwinds
     usage: [y1,y2] = woodwenv(a,s,r,Fs);
          where a = attack TIME
               s = sustain TIME
               r = release TIME
               Fs = sampling frequency (Hz)
          returns:
               y1 = amplitude envelope
               y2 = modulation index envelope
     note: attack is exponential, sustain is constant,
          release is exponential

     """

    ta = np.arange(0, a, 1 / Fs)
    y1 = np.exp(ta / a * 1.5) - 1
    y1 = y1 / max(y1)

    y1 = np.concatenate([y1, np.ones(round(s * Fs))])
    tr = np.arange(0, r / 2, 1 / Fs)
    y3 = np.exp((r / 2 - tr) / r * 3) - 1
    y3 = y3 / max(y3) / 2
    y4 = 1 - y3[::-1]

    y2 = np.concatenate([y1, np.ones(round(r * Fs))])
    y1 = np.concatenate([y1, y4, y3, [0]])

    ln = min(len(y1), len(y2))
    y1 = y1[:ln:]
    y2 = y2[:ln:]
    return y1, y2