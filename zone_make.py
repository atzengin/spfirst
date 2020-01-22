#!/usr/bin/env python3

import numpy as np
from math import pi


def zone_make(N, shift=None):
    """
    ZONE_MAK      Creates an N by N zone-plate image
    usage:
        y = create_zone(N, <shift>)
        y = output image
        N = size of image (N by N)
    shift =  shift of the center of the image
              (DEFAULT = N/2 puts center in center)
    NOTE:
      To display the image "img":
      1. Load the colormap with a linear grayscale (only needs to
      be done once) using the  command "colormap(gray(256))".
      2. Display the image y using the MATLAB command
      "image(y)" or "imagesc(y)".

  """

    if shift == None: shift = N / 2

    imax = 256 * (1 - 10 * np.finfo(float).eps)
    x = np.ones((N, 1)) * (np.arange(0, N))
    x = pow((x - shift), 2)
    kx = pi / N
    img = np.floor(imax * (np.cos(kx * (x + x.transpose())) + 1))
    return img

    """
    we are actually implementing the following 
    linear-FM equation:
    img = A*cos(k*(r^2 + c^2));
    where:
    r = row in image
    c = column in image
  
    """
