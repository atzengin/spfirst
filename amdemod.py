#!/bin/usr/env python3

import numpy as np


def amdemod(xx, fc, fs, tau=0.97):
    """ AMDEMOD Demodulate an amplitude modulated waveform
        using a simple scheme consisting of a rectifier
        followed by a leaky first-order hold scheme.
               dd = amdemod(xx,fc,fs,tau)
        where
        xx = the input AM waveform to be demodulated
        fc = carrier frequency
        fs = sampling frequency
        tau = time constant of the RC circuit (OPTIONAL)
             (default value is tau=0.97)
        dd = demodulated message waveform
    """
    xx = np.asarray(xx)
    dd = np.zeros(len(xx))
    dd[0] = xx[0]
    for i in range(1, len(xx)):
        dd[i] = dd[i - 1] * tau
        dd[i] = max(xx[i], dd[i])

    return dd