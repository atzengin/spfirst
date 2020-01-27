#!/bin/usr/env python3

from math import pi
import numpy as np


def dtmfdeco(xx, fs=8000):
    """DTMFDECO   decode the DTMF waveform into keys that were pressed
        usage:    keys = dtmfdeco(xx,fs)

        xx = input waveform
        fs = sampling rate (it defaults to 8000)
        keys = list out keys pressed
    """
    xx = np.asarray(xx)

    fl = 256
    wl = 1024
    tt = np.array([[697, 697, 697, 770, 770, 770, 852, 852, 852, 941, 941, 941],
                   [1209, 1336, 1477, 1209, 1336, 1477, 1209, 1336, 1477, 1336, 1209, 1477]])

    keys = np.array([])
    rmsx = np.sqrt(np.sum(xx ** 2) / len(xx))
    old_key = 0
    old_valid = 0

    for i in np.arange(0, len(xx) - fl, fl):
        valid = 1
        hammwin = 0.54 - 0.46 * np.cos(2 * pi / (wl - 1) * (np.arange(0, wl)))
        w = hammwin * np.append(xx[i:(i + fl), ], np.zeros((1, wl - fl)))
        W = np.abs(np.fft.fft(w)) / fl * 8
        W = W[0:int(len(W) / 2)]
        W = W * (W > rmsx / 2)
        W[[0, -1]] = 0
        W = W / max(np.append(W, [0.01]))
        p = np.zeros((2, 3))
        ip = 0
        kk = np.array((np.where(W > 0))[0])
        for k in kk:
            if np.logical_and(W[k] > W[k - 1], W[k] > W[k + 1]):
                p[0, ip] = (k + 1) / wl * fs
                p[1, ip] = W[k]
                ip = ip + 1
            if ip > 3:
                valid = 0
                break

        score = np.abs(p[0, 0] - tt[0, :]) + np.abs(p[0, 1] - tt[1, :]) + 400 * (
                    np.abs(p[1, 0] - 1) + np.abs(p[1, 1] - 1) + p[1, 2])

        s = np.amin(score)
        si = np.argmin(score) + 1

        if s > 40:
            valid = 0
        if valid:
            if si != old_key:
                keys = np.append(keys, si)
                old_key = si
            else:
                old_key = 0

        return keys