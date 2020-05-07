#!/bin/usr/env python3

import numpy as np


def fullwave(t, T, signal):
    """ FULLWAVE creates a full-wave rectified Sine/Cosine wave """

    # 1 == sine  &  2 == cosine
    if(signal == 1):
        yy = np.sin(np.pi/T*t)
    elif(signal == 2):
        yy = np.cos(np.pi/T*t)
    else:
        print('Unknown signal type')


    yy = np.abs(yy)

    return yy

if __name__ == "__main__":
    pass