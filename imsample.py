#!/usr/bin/env python3


import numpy as np


def imsample(xx, P):
  """
    IMSAMPLE    Function for sub-sampling an image
      usage:  yy = imsample(xx,P)
      xx = input image to be sampled
      P = sub-sampling period(a small integer like 2, 3, etc.)
      yy = output image

  """
  M, N = np.shape(xx)
  S = np.zeros((M, N))
  S[0:M:P, 0:N:P] = np.ones((len(np.arange(0, M, P)), len(np.arange(0, N, P))))
  yy = np.multiply(xx, S)
  return yy