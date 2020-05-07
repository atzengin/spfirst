#!/bin/usr/env python3

import sys

from PySide2.QtWidgets import QApplication
from PyQt5.QtCore import QObject
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtCore import QUrl, pyqtProperty, pyqtSlot, pyqtSignal, QVariant

import numpy as np
from math import pi
from sqar import square
from tri import tri
from fullwave import fullwave
from halfwave import halfwave

import matplotlib.pyplot as plt

class FourierSeries(QObject):
    def __init__(self):
        QObject.__init__(self)
        self._yval = 0
        self._timeaxis = 0
        self._synthesized = 0
        self._abs_mag_vec = 0
        self._ang_mag = 0
        self._fs = 0




    sig_yval = pyqtSignal(list)             # yval signal
    sig_timeaxis = pyqtSignal(list)         # timeaxis signal
    sig_synthesized = pyqtSignal(list)      # synthesized signal
    sig_abs_mag_vec = pyqtSignal(list)      # mag_vec signal
    sig_ang_mag = pyqtSignal(list)          # ang_mag signal
    sig_fs = pyqtSignal(list)                # fs signal



    def setFs(self, fs):
        if self._fs != fs:
            self._fs = fs

        self.sig_fs.emit(self._fs)


    def getFs(self):
        return self._fs


    def setAngMag(self, mag_vec):
        if self._ang_mag != mag_vec:
            self._ang_mag = mag_vec
        self.sig_ang_mag.emit(self._ang_mag)


    def getAngMag(self):
        return self._ang_mag


    def setAbsMag(self, mag_vec):
        if self._abs_mag_vec != mag_vec:
            self._abs_mag_vec = mag_vec
        self.sig_abs_mag_vec.emit(self._abs_mag_vec)

    def getAbsMag(self):
        return self._abs_mag_vec

    def setSynthesized(self, synthesized):
        if self._synthesized != synthesized:
            self._synthesized = synthesized
        self.sig_synthesized.emit(self._synthesized)

    def getSynthesized(self):
        return self._synthesized

    def setTimeaxis(self, tt):
        if self._timeaxis != tt:
            self._timeaxis = tt
        self.sig_timeaxis.emit(self._timeaxis)

    def getTimeaxis(self):
        return self._timeaxis

    def setYval(self, yval):
        if self._yval != yval:
            self._yval = yval
        self.sig_yval.emit(self._yval)

    def getYval(self):
        return self._yval

    @pyqtSlot(int, int)          #      Dikkat!! eger qml'den veri almak istiyorsan slot()'da degisken sayasi ve veri tiplerini belirlemen gerek.
    def updateYval(self, cbx_value, T0):
#        print(cbx_value, T0)
        timeaxis = np.arange(-30, 30+0.1, 0.1)
        freq = 1/T0
        self.setTimeaxis(timeaxis.tolist())

        if(cbx_value == 0):
            #   Square wave
            yval = square(2*np.pi*freq*timeaxis)
            self.setYval(yval.tolist())
        elif(cbx_value == 1):
            #   Triangle wave
            timeaxis = timeaxis[timeaxis >= 0]
            yval = np.asmatrix(tri(10/freq, 1, len(timeaxis)))
            yval = np.asarray(-np.c_[np.fliplr(yval[0:, 1:]), yval]).T
            self.setYval(yval.tolist())
        elif(cbx_value == 2):
            #   Ramp wave
            T = 1/freq
            timeaxis = timeaxis[timeaxis >= 0]
            yval = np.asmatrix((np.mod(timeaxis+T/2, T) - T/2) / T*2)
            yval =  np.asarray(np.c_[-np.fliplr(yval[0:, 1:]), yval]).T
            self.setYval(yval.tolist())
        elif(cbx_value == 3):
            #   Full-wave Rectified Sine wave
            #   1 == sine wave (third parameter of fullwave func.)
            yval = fullwave(timeaxis, 1/freq, 1)
            self.setYval(yval.tolist())
        elif(cbx_value == 4):
            #   Full-wave Rectified Cosine wave
            #   2 == cosine wave (third parameter of fullwave func.)
            yval = fullwave(timeaxis, 1/freq, 2)
            self.setYval(yval.tolist())
        elif(cbx_value == 5):
            #   Half-wave Rectified Sine wave
            #   1 == sine wave (third parameter of halfwave func.)
            yval = halfwave(timeaxis, 1/freq, 1)
            self.setYval(yval.tolist())
        elif(cbx_value == 6):
            #   Half-wave Rectified Cosine wave
            #   1 == cosine wave (third parameter of halfwave func.)
            yval = halfwave(timeaxis, 1/freq, 2)
            self.setYval(yval.tolist())

    @pyqtSlot(int, int, int)
    def updateSynthesized(self, coeff_value, cbx_value, T0):
        timeaxis = np.arange(-30, 30+0.1, 0.1)
        freq = 1/T0
        freqs = np.array([])
        rec_final = np.zeros((1, len(timeaxis)))
        mag_vec = []
        self.setTimeaxis(timeaxis.tolist())

        if cbx_value == 0:
            # --------------- Square wave ------------------#
            for n in range(-coeff_value,coeff_value+1):
                # print(n)
                if n == 0 or np.mod(n, 2) == 0:
                    mag_spec = 0
                else:
                    mag_spec = (-2*1j) / (n*np.pi)

                rec_sig = mag_spec * np.exp(1j*2*np.pi*freq*n*timeaxis)
                freqs = np.append(freqs, freq * n)
                mag_vec = np.r_[mag_vec, mag_spec]
                rec_final = np.add(rec_final, rec_sig)
            rec_final = rec_final.T
            self.setSynthesized(np.real(rec_final).reshape(1,np.size(rec_final)).T.tolist())      # Dikkat
            mag_vec[np.abs(mag_vec) < np.sqrt(np.spacing(1))] = 0
            self.setAbsMag(np.abs(mag_vec).tolist())
            self.setAngMag(np.angle(mag_vec).tolist())
            self.setFs(freqs.tolist())
        elif cbx_value == 1:
            # --------------- Triangle wave ----------------------

            for n in range(-coeff_value,coeff_value+1):
                if n == 0 or np.mod(n, 2) == 0:
                    mag_spec = 0
                else:
                    mag_spec = 4 / ((n*np.pi)**2)

                rec_sig = mag_spec * np.exp(1j*2*np.pi*freq*n*timeaxis)
                freqs = np.append(freqs, freq * n)
                mag_vec = np.r_[mag_vec, mag_spec]
                rec_final = np.add(rec_final, rec_sig)
            self.setSynthesized(np.real(rec_final).reshape(1,np.size(rec_final)).T.tolist())      # Dikkat
            mag_vec[np.abs(mag_vec) < np.sqrt(np.spacing(1))] = 0
            self.setAbsMag(np.abs(mag_vec).tolist())
            self.setAngMag(np.angle(mag_vec).tolist())
            self.setFs(freqs.tolist())
        elif cbx_value == 2:
            # --------------- Ramp/Sawtooth wave -----------------

            for n in range(-coeff_value,coeff_value+1):
                if n == 0:
                    mag_spec = 0
                else:
                    mag_spec = ((-1)**n) * (1j)/ (n*np.pi)

                rec_sig = mag_spec * np.exp(1j*2*np.pi*freq*n*timeaxis)
                freqs = np.append(freqs, freq * n)
                mag_vec = np.r_[mag_vec, mag_spec]
                rec_final = np.add(rec_final, rec_sig)
            self.setSynthesized(np.real(rec_final).reshape(1,np.size(rec_final)).T.tolist())      # Dikkat
            mag_vec[np.abs(mag_vec) < np.sqrt(np.spacing(1))] = 0
            self.setAbsMag(np.abs(mag_vec).tolist())
            self.setAngMag(np.angle(mag_vec).tolist())
            self.setFs(freqs.tolist())

        elif cbx_value == 3 or cbx_value == 4:
            # ------------------- Full-wave Rectified (Sine / Cosine)----------------
            for n in range(-coeff_value,coeff_value+1):
                # We dont need to have special case

                # Sine wave coeff
                mag_spec = -(np.exp(-1j*2*np.pi*n) + 1)/(np.pi*(4*n**2 -1))
                if cbx_value == 4:
                    # Cosine wave
                # mag_spec = np.exp(-1j*n*np.pi)*mag_spec
                    mag_spec = 2*np.cos(n*np.pi) / (np.pi*(1-4*n**2))

                rec_sig = mag_spec * np.exp(1j*2*np.pi*freq*n*timeaxis)
                freqs = np.append(freqs, freq * n)
                mag_vec = np.r_[mag_vec, mag_spec]
                rec_final = np.add(rec_final, rec_sig)
            self.setSynthesized(np.real(rec_final).reshape(1,np.size(rec_final)).T.tolist())      # Dikkat
            self.setAbsMag(np.abs(mag_vec).tolist())
            self.setAngMag(np.angle(mag_vec).tolist())
            self.setFs(freqs.tolist())

        elif cbx_value == 5 or cbx_value == 6:
            # -------------------- Half-wave Rectified (Sine / Cosine)-------------------
            for n in range(-coeff_value,coeff_value+1):
                # Cosine wave coeffs
                if n == 0:
                    mag_spec = 1/(np.pi)
                elif n == -1 or n == 1:
                    mag_spec = 1/4
                else:
                    mag_spec = (np.cos(n*np.pi/2))/np.pi/(1-n**2)

                # Change coefficient depending cosine / sine
                if cbx_value == 5:
                    # Sine wave
                    mag_spec = np.exp(-1j*n*np.pi/2)*mag_spec

                rec_sig = mag_spec * np.exp(1j*2*np.pi*freq*n*timeaxis)
                freqs = np.append(freqs, freq * n)
                mag_vec = np.r_[mag_vec, mag_spec]
                rec_final = np.add(rec_final, rec_sig)

            self.setSynthesized(np.real(rec_final).reshape(1,np.size(rec_final)).T.tolist())      # Dikkat
            mag_vec[np.abs(mag_vec) < np.sqrt(np.spacing(1))] = 0
            self.setAbsMag(np.abs(mag_vec).tolist())
            self.setAngMag(np.angle(mag_vec).tolist())
            self.setFs(freqs.tolist())
        else:
            print('Invalid Signal Type')



    #   pyqtProperty
    yval = pyqtProperty(list, getYval, notify=sig_yval)
    timeaxis = pyqtProperty(list, getTimeaxis, notify=sig_timeaxis)
    synthesized = pyqtProperty(list, getSynthesized, notify=sig_synthesized)
    abs_mag = pyqtProperty(list, getAbsMag, notify=sig_abs_mag_vec)
    ang_mag = pyqtProperty(list, getAngMag, notify=sig_ang_mag)
    fs = pyqtProperty(list, getFs, notify=sig_fs)




if __name__ == "__main__":
    app = QApplication(sys.argv)
    engine = QQmlApplicationEngine()
    FS = FourierSeries()
    engine.rootContext().setContextProperty("FS", FS)
    engine.load(QUrl("fseriesdemo.qml"))
    sys.exit(app.exec_())
