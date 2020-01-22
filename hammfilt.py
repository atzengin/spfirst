#!/usr/bin/env python3

from math import pi
import numpy as np


def hammfilt(N, WhHat, hilo="X"):
    """
        HAMMFILT   FIR filter design with a Hamming window
                works for lowpass, highpass, and bandpass cases
        usage:   hh = hammfilt( N, WhHat, hilo )
        
            N = filter ORDER (Length-1)
        WhHat = approximate cutoff frequencies (as omega hat)
                if WhHat is a 2-element vector, the filter is BPF
                if WhHat is a scalar, filter is LPF or HPF
        hilo = string to indicate type of filter
                for a HPF, use 'high'; otherwise, nothing
            hh = filter coefficients. (N+1) element vector.
        
        EXAMPLE:   hh = hammfilt(24,[0.2*pi,0.4*pi])
        
        designs a length-25 BPF with a "passband" from 0.2pi to 0.4pi.
        NOTE: the "actual" passband will be narrower because it is
                defined by the ripple size in the passband. The values
                specified in WhHat will be where the magnitude response is 0.5
        
        SAMPLE TEST CALLS:
        hh=hammfilt(35,[0.3*pi]);[HH,ww]=freqz(hh,1,1024);plot(ww/pi,abs(HH))
        hh=hammfilt(38,0.3*pi,"high");[HH,ww]=freqz(hh,1,1024);plot(ww/pi,abs(HH))
        hh=hammfilt(55,[.3,.5]*pi);[HH,ww]=freqz(hh,1,1024);plot(ww/pi,abs(HH))
	
        """

    if hilo.lower() == "high":
        if len(WhHat) == 1:
            if N % 2: print(">>HAMMFILT: even length HPF not possible");            exit()
            WhHat[0] = pi - WhHat[0]
        else:
            print(">>HAMMFILT: trying to specify HPF and BPF simultaneously");
            exit()

    L = N + 1
    Lm2 = (L - 1) / 2
    nn = np.arange(0, L) - Lm2
    nn = nn + (nn == 0) * 1e-8

    if len(WhHat) == 1:
        hh = (0.54 - 0.46 * np.cos(2 * pi * (np.arange(0, L) / (L - 1)))) * np.sin(WhHat * nn) / (pi * nn)
        if hilo.lower() == "high": hh = hh * np.cos(pi * nn)
    elif len(WhHat) == 2:
        wc = (WhHat[0] + WhHat[1]) / 2
        wn = (max(WhHat) - min(WhHat)) / 2
        hh = (0.54 - 0.46 * np.cos(2 * pi * (np.arange(0, L) / (L - 1)))) * (2 * np.cos(wc * nn)) * np.sin(wn * nn) / (
                pi * nn)
    else:
        print(">>HAMMFILT: bandedge frequency vector incorrect")
    return hh
