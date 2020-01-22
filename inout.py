#!/usr/bin/env python3

import numpy as np
from striplot import striplot


def inout(x, y, nstart, npts, nsect):
    """
	INOUT    plot LONG input & output signals together
	-----      put them on alternate lines in a strip plot
	usage:
	   inout(xin, yout, nstart, npts, nsect)
	
      xin = INPUT signal vector
      yout = OUTPUT signal vector
      nstart = STARTING sample number in both sigs
      npts = number of points to plot PER LINE
      nsect = number of in/out PAIRS of LINES
         (for best results use nsect = 4) <====
	
	   NOTE: the signals x[n] & y[n] are plotted over the index
         range:  n = nstart -->  n = nstart + npts*nsect - 1
	
	   see also STRIPLOT

   """

    if nsect > 8:
        print(">>WARNING(INOUT): are you sure you want NSECT this large?")
    p = []
    x = np.array(x).flatten('F')
    y = np.array(y).flatten('F')
    L = max(len(x), len(y))
    for i in range(1, nsect + 1):
        n1 = nstart + (i - 1) * npts
        n2 = n1 + npts - 1
        if L < n2:
            print(">>WARNING(INOUT): trying to go past end of signal(s)")
            break
        p = np.concatenate([p, x[n1 - 1:n2], y[n1 - 1:n2]])
    striplot(p, 1, npts)