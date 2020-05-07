#!/bin/usr/env python3

import numpy as np

def halfwave(t, T, signal):
    """ HALFWAVE creates a half-wave rectified sine/cosine wave. """

    # 1 == sine  &  2 == cosine
    if(signal == 1):
        yy = np.sin(2*np.pi/T*t)
    elif(signal == 2):
        yy = np.cos(2*np.pi/T*t)
    else:
        print('Unknown signal type')
    
    for i in range(len(yy)):
        if(yy[i] < 0):
            yy[i] = 0
    
    return yy




if __name__ == "__main__":
    pass