#!/bin/usr/env python3

import numpy as np 

def sprintf(s, A):

    A = np.asmatrix(A)
    STR = np.array([])
    a = A.reshape(np.size(A)).tolist()

    for i in a[0]:
        STR = np.append(STR, s % i)

    return STR