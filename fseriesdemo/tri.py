#!/bin/usr/env python3

import numpy as np



def tri(T, sT, Ns):
    """
        TRI   Generate samples of a triangular waveform with period T seconds, 
        sampling frequency sT samples/second, and Ns samples.
    """

    x = -1 + 4*np.abs(np.round(np.arange(0, Ns, 1)/sT/T) - np.arange(0, Ns, 1)/sT/T)
    return x

if __name__ == "__main__":

    x = tri(10, 10, 10)
    print(x)