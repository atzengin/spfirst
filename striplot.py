#!/bin/usr/env python3

from math import ceil

import matplotlib.pyplot as plt
import numpy as np


def striplot(x, fs, n=400.0, ntick=0.0, xmax=None):
    """STRIPLOT    plot long signal in horizontal strips
                ( good for multi-line speech wfms )
    Usage:  striplot(X, FS, N)  plots waveform X with N pts/line
        FS = sampling rate (Hertz); used only for labeling
        ALL traces are auto-scaled to the max signal value
        h is the graphics handle for the plot.
    striplot(X, FS, N, NTICK)
                    puts markers every NTICK samples
    striplot(X, FS, N, NT, XMAX)
                uses XMAX as the value for scaling

    NOTE: the x-axis is always labeled with (time) indices.
        the y-axis labels are NOT AMPLITUDE, rather they
        are the INDEX OFFSET to the start of each row.
    see also WP, WATERF
    """

    x = np.asarray(x)
    if x.ndim == 1:
        x.shape = (len(x), 1)

    x = x / (np.amax(np.abs(x)))    # Normalize sample amplitude

    xmax = (np.amax(np.abs(x)))

    lenx = (len(x))                 # (DATA-TYPE)
    nrows = ceil((lenx / n))
    if lenx < n * nrows:
        ri = np.arange(len(x) - 1, n * nrows).astype(int)
        x = np.resize(x, (int(n * nrows), 1))
        x[np.ix_(ri)] = 0           # Need to zero pad
        lenx = int(n * nrows)
    del_t = 1.0 / fs

    # [1;1] = MATLAB
    # m_ones = np.array([1,1]).reshape(2, 1)
    m_ones = np.vstack((1, 1))

    yscale = -n * del_t
    zeroy = yscale * m_ones * np.arange(0, nrows, 1)
    half = 0.5
    offsets = (half * yscale) * m_ones * np.ones((1, int(nrows)))

    sepy = np.array(zeroy - offsets)
    sepy = np.append(sepy, np.array(zeroy[:, int(nrows - 1)]) + (half * yscale) * m_ones, axis=1)
    if ntick > 0:
        nnt = 0
    else:
        xtick = ytick = 0
    if xmax < 1:  # To prevent overlap of plots
        xmax = 1.0

    scale = half / xmax
    x = np.reshape(x, (int(n), int(nrows)))

    for i in range(int(nrows)):
        x[:, i] = -yscale * scale * x[:, i] + yscale * (i + 1 - 1)

    ends = del_t * np.array([0.00, n - 1.00], dtype=np.float64)
    plt.plot(del_t * np.linspace(0, int(n - 1), num=int(n - 1) - 0 + 1), x, '-b', ends, sepy, ':y', ends, zeroy, '--b',
             xtick, ytick, ':r')
    ax = np.hstack((ends.T, (nrows - 0.5) * yscale, -0.5 * yscale))
    plt.show()
    plt.axis(ax)