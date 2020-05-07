#!/bin/usr/env python3

import sys
from PySide2.QtWidgets import QApplication
from PyQt5.QtCore import QObject

from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtCore import QUrl, pyqtProperty, pyqtSlot, pyqtSignal, QVariant
import numpy as np
from math import pi

import matplotlib.pyplot as plt

class Sindrill(QObject):
    def __init__(self):
        QObject.__init__(self)
        self._title = "Chart title"
        self._amplitude = [1, 2][np.random.randint(0,2)]
        self._frequency = [500,1000][np.random.randint(0,2)]
        self._phase = ['-pi/2', '0', 'pi/2'][np.random.randint(0,3)]
        self._duration = np.arange(([-2, -1, 0][np.random.randint(0,3)]) / self._frequency, ([1, 2][np.random.randint(0,2)]) / self._frequency+1/(100*self._frequency)
            , 1/(100*self._frequency)).tolist()
        self._xt = self._amplitude * np.sin(2*np.pi*self._frequency*np.asarray(self._duration) + eval(self._phase)).tolist()
        self._answ = 0
        self.ampAnsw = 0
        self.f0Answ = 0
        self.phiAnsw = 0


#     get A, f0 and phi
    @pyqtSlot(str,str, str)
    def getvalues(self, A, f0, phi):
        self.setvalues(float(A), float(f0), phi)

    def setvalues(self,A, f0, phi):
        self.ampAnsw = A
        self.f0Answ = f0
        self.phiAnsw = eval(phi)

    sigxt = pyqtSignal(list)        # xt signal
    sigt = pyqtSignal(list)         # duration signal
    sigamp = pyqtSignal(int)        # amp signal
    siganswer = pyqtSignal(list)    # answer signal
    sigphase = pyqtSignal(str)      # phase signal
    sigfrequency = pyqtSignal(int)  # freq signal


    def setFrequency(self, frequency):
        if self._frequency != frequency:
            self._frequency = frequency
        self.sigfrequency.emit(self._frequency)

    def getFrequency(self):
        return self._frequency

    def setPhase(self, phi):

        if self._phase != phi:
            self._phase = phi
        self.sigphase.emit(self._phase)

    def getPhase(self):
        return self._phase

    def setAnswer(self, answ):
        if self._answ != answ:
            self._answ = answ
        self.siganswer.emit(self._answ)

    def getAnswer(self):
        return self._answ

    def setAmplitude(self, amp):
        if self._amplitude != amp:
            self._amplitude = amp
        self.sigamp.emit(self._amplitude)

    def getAmplitude(self):
        return self._amplitude

    def setT(self, tt):
        if self._duration != tt:
            self._duration = tt
        self.sigt.emit(self._duration)

    def getT(self):
        return self._duration

    def setXt(self, xt):
        if self._xt != xt:
            self._xt = xt
        self.sigxt.emit(self._xt)

    def getXt(self):
        return self._xt


    @pyqtSlot()
    def updateAnswer(self):
        answ = self.ampAnsw * np.cos(2*np.pi*self.f0Answ*np.asarray(self._duration) + self.phiAnsw)
        self.setAnswer(answ.tolist())

    @pyqtSlot()
    def updateXt(self):
        self.setAmplitude([1, 2][np.random.randint(0,2)])
        self.setFrequency([500,1000][np.random.randint(0,2)])
        self.setPhase(['-pi/2', '0', 'pi/2'][np.random.randint(0,3)])
        startPoint = ([-2, -1, 0][np.random.randint(0,3)]) / self._frequency
        endPoint = ([1, 2][np.random.randint(0,2)]) / self._frequency
        self.setT(np.arange(startPoint, endPoint + 1/(100*self._frequency), 1/(100*self._frequency)).tolist())
        # print(self._amplitude, ' ', self._frequency, ' ', self._phase)
        self.setXt((self._amplitude * np.sin(2*np.pi*self._frequency*np.asarray(self._duration) + eval(self._phase) )).tolist())

    @pyqtSlot()
    def updatePro(self):
        self.setAmplitude([1, 5, 10, 25, 100][np.random.randint(0,5)])
        self.setFrequency([60, 100, 250, 500,1000][np.random.randint(0,5)])
        lst = np.array(np.arange(-30, 31, 1), dtype=str)
        phase = [i + '*pi/24' for i in lst]
        self.setPhase(phase[np.random.randint(0,5)])
        startPoint = ([-2, -1, 0][np.random.randint(0,3)]) / self._frequency
        endPoint = ([1, 2][np.random.randint(0,2)]) / self._frequency
        self.setT(np.arange(startPoint, endPoint + 1/(100*self._frequency), 1/(100*self._frequency)).tolist())
        # print(self._amplitude, ' ', self._frequency, ' ', self._phase)
        self.setXt((self._amplitude * np.sin(2*np.pi*self._frequency*np.asarray(self._duration) + eval(self._phase) )).tolist())

    #   pyqtProperty
    xt = pyqtProperty(list, getXt, notify=sigxt)
    duration = pyqtProperty(list, getT, notify=sigt)
    A = pyqtProperty(int, getAmplitude, notify=sigamp)
    answer = pyqtProperty(list, getAnswer, notify=siganswer)
    phi = pyqtProperty(str, getPhase, notify=sigphase)
    freq = pyqtProperty(int, getFrequency, notify=sigfrequency)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    engine = QQmlApplicationEngine()
    sindrill = Sindrill()
    engine.rootContext().setContextProperty("sindrill", sindrill)
    engine.load(QUrl("sindrill.qml"))
    sys.exit(app.exec_())