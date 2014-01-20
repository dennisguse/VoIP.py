from PyQt4.QtGui import *
from PyQt4.QtCore import *
from Modules.AbstractModule import AbstractModule
from Defines import SIGNALS
import time, sys

class SignalbarModule(QObject, AbstractModule):

    def __init__(self):
        super(SignalbarModule, self).__init__()
        self.txBar = None
        self.rxBar = None

    def hasSignalsToRegister(self):
        return True

    def getSignals(self):
        return [[SIGNALS.CALL_SIGNAL_LEVEL_REQUEST,  None,  'onSignalLevelChangeRequest']]

    def start(self, parameters):

        if self.txBar == None:
            hbox = QHBoxLayout(parameters["parent"])
            self.txBar = QProgressBar(parameters["parent"])
            self.rxBar = QProgressBar(parameters["parent"])
            hbox.addWidget(self.txBar)
            hbox.addWidget(self.rxBar)
            parameters["parentLayout"].addLayout(hbox,0,0)
            self.connect(parameters["signalSource"], SIGNAL(SIGNALS.CALL_SIGNAL_LEVEL_CHANGE), self.showSignalLevel)
            self.signalLevelThread = SignalLevelThread(self.requestSignalUpdate)
            self.signalLevelThread.start()



    def dismiss(self):
        self.signalLevelThread.stop()
        self.signalLevelThread = None

    def showSignalLevel(self, level):
        self.txBar.setValue(int(level[0] * 100))
        self.rxBar.setValue(int(level[1] * 100))

    def requestSignalUpdate(self):
        self.emit(SIGNAL(SIGNALS.CALL_SIGNAL_LEVEL_REQUEST))

class SignalLevelThread(QThread):

    def __init__(self, requestUpdate):
        QThread.__init__(self)
        self.requestStop = False
        self.requestUpdate = requestUpdate

    def run(self):
        while self.requestStop == False:
            self.requestUpdate()
            time.sleep(0.1)

    def stop(self):
        self.requestStop = True