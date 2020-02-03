#!/bin/usr/env python3

import numpy as np
from sprintf import sprintf


def mattostr (x,style=None):
   """MATTOSTR
   -------
   usage:  mattostr(X,STYLE)
   convert an entire matrix X to formatted numbers,
       using a C format in STYLE, e.g., '%3.f'
   """
   x = np.asmatrix(x)
   N, M = x.shape

   tt = sprintf(style, x)
   Lt =  len(tt)
   y = np.reshape(tt, (N,M))
   return y