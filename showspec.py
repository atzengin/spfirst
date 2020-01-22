#!/usr/bin/env python3


import numpy as np
from math import pi
import matplotlib.pyplot as plt


def showspec(x, fs=2, nargout=0):
    """
	  SHOWSPEC  Plot a simple estimate of the spectrum of a signal.
         usage:   [X,w] = SHOWSPEC(x,fs)
            x = the signal
            fs = the sample rate  (if omitted, it defaults to 2)
            X = the magnitude of the spectrum
            w = the corresponding frequency vector

         nargout default or 0 to plot the spectrum
         otherwise return X and w arrays and no spectrum is plotted.
   """
    x = np.array(x).flatten('F')
    L = int(pow(2, np.ceil(np.log2(len(x)))))
    # --
    Lx = len(x)
    HammW = 0.54 - 0.46 * np.cos(2 * pi * (np.arange(0, Lx)) / (Lx - 1))
    # --

    XX = abs(np.fft.fft(HammW * x, L)) / len(x) * 3.86
    XX = XX[0:int(L / 2)]
    ww = np.arange(0, L / 2) / L * fs

    if nargout == 0:
        plt.plot(ww, XX)
        plt.xlabel('Frequency in Hz')
        plt.ylabel('Approximate Amplitude')
        plt.grid(True)
        plt.show()
    else:
        return XX, ww
