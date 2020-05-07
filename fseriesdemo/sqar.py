#!/bin/usr/env python3

import numpy as np


def square(t, duty=50):
    """
    %SQUARE Square wave generation.
    SQUARE(T) generates a square wave with period 2*Pi for the
    elements of time vector T.  SQUARE(T) is like SIN(T), only
    it creates a square wave with peaks of +1 to -1 instead of
    a sine wave.
    SQUARE(T,DUTY) generates a square wave with specified duty
    cycle. The duty cycle, DUTY, is the percent of the period
    in which the signal is positive.

    For example, generate a 30 Hz square wave:
        t = 0:.0001:.0625;
        y = SQUARE(2*pi*30*t);, plot(t,y)

    """
    if (np.any(np.size(duty)) != 1):
        print('Duty parameter must be a scalar.')
        return -1
    
    # Compute values of t normalized to (0,2*pi)
    tmp = np.mod(t, 2*np.pi)

    # Compute normalized frequency for breaking up the interval (0,2*pi)
    w0 = 2*np.pi*duty/100

    # Assign 1 values to normalized t between (0,w0), 0 elsewhere
    nodd = (tmp < w0)

    # The actual square wave computation
    s = 2*nodd-1

    return s 

    








if __name__ == "__main__":
    s = square(np.arange(2, 3+1/10, 1/10 ))
    print(s)
    print(len(s))