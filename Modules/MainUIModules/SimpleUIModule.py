import logging
import time

from Modules.MainUIModules.AbstractUIModule import AbstractUIModule
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import uic, QtGui
from Defines import SIGNALS
from PyQt4.QtCore import SIGNAL
from Defines.MODULES import MODULES
from Modules.UIModules import ImagePlayer
from Modules.ConfigModules.ConfigReaderModule import readFirstBuddyNumber
import Modules.UIModules.RESOURCES as UIResources
import Modules.MainUIModules.RESOURCES as MainUIResources


class SimpleUI(AbstractUIModule,  QtGui.QWidget):
    
    MODULES_TO_LOAD = ['ErrorDialog',  'WaveRecordModule',  'RingToneModule', 'SingleBuddyModule',
                       'DeviceChooserModule']
    
    def __init__(self, signalSource, parent=None):
        QtGui.QWidget.__init__(self, parent)   
        self.signalSource = signalSource
        self.__ui = uic.loadUi(MainUIResources.RESCOURCES_MAINUI["Simple"], self)
        self.connectButtons()
        self.connectSignals()
        self.numberToCall = readFirstBuddyNumber()
        
    def registerNewModules(self):        
        for module in self.MODULES_TO_LOAD:
            SIGNALS.emit(self, SIGNALS.MODULE_LOAD, module, MODULES[module])
        self.emit(SIGNAL(SIGNALS.MODULE_ACTIVATE),  'WaveRecordModule')
        self.emit(SIGNAL(SIGNALS.MODULE_ACTIVATE),  'DeviceChooserModule')
        self.emit(SIGNAL(SIGNALS.MODULE_ACTIVATE),  'SingleBuddyModule')


    def connectButtons(self):
        pass #is done on demand
 
    def connectSignals(self):
        self.connect(self.signalSource, SIGNAL(SIGNALS.CALL_INCOMING), self.onIncomingCall)
        self.connect(self.signalSource, SIGNAL(SIGNALS.CALL_INCOMING_CANCELED), self.onIncomingCallCanceled)
        self.connect(self.signalSource, SIGNAL(SIGNALS.CALL_OUTGOING_CANCELED), self.onOutgoingCallCanceled)
        self.connect(self.signalSource, SIGNAL(SIGNALS.REGISTER_STATE_CHANGE), self.onRegStateSignal)
        self.connect(self.signalSource, SIGNAL(SIGNALS.BUDDY_STATE_CHANGED), self.onBuddyStateChanged)
    
    def onIncomingCall(self,  incomingCallerNumber):
        logging.info("Got incoming call from: " + incomingCallerNumber)
        self.emit(SIGNAL(SIGNALS.MODULE_ACTIVATE),  'RingToneModule',  None)
        self.__ui.btn.setText("Anruf annehmen")
        self.__ui.btn.clicked.disconnect()
        self.__ui.btn.clicked.connect(self.btnIncomingCallAccept)
        
    def onIncomingCallCanceled(self):
        self.emit(SIGNAL(SIGNALS.MODULE_DISMISS),  'RingToneModule')
        self.__ui.btn.setText("Anrufen")
        self.__ui.btn.clicked.disconnect()
        self.__ui.btn.clicked.connect(self.btnStartCall)

    def onOutgoingCallCanceled(self):
        self.__ui.btn.setText("Anrufen")
        self.__ui.btn.clicked.disconnect()
        self.__ui.btn.clicked.connect(self.btnStartCall)

    def onRegStateSignal(self, isActive, reg_code, reg_reason): #Mehrfach aufrufen?
        if isActive == True:            
            #Enable UI 
            self.__ui.btn.setEnabled(True)
            self.__ui.btn.clicked.connect(self.btnStartCall)
            ImagePlayer.gifMovie(self.__ui.regState,  UIResources.RESCOURCES_PIC["Online"])
        else:
            #Disable UI and error message
            self.__ui.btn.setEnabled(False)                     
            ImagePlayer.gifMovie(self.__ui.regState,  UIResources.RESCOURCES_PIC["LoadAnimation"])
        self.__ui.regState.setToolTip("RegCode: " + str(reg_code) + " RegReason: " + reg_reason)

    def onBuddyStateChanged(self, stateText):
        self.__ui.lblBuddy.setToolTip("BuddyState: " + stateText)
        if stateText == "Ready":
            ImagePlayer.gifMovie(self.__ui.lblBuddy,  UIResources.RESCOURCES_PIC["Online"])
            self.__ui.btn.setEnabled(True)
        elif stateText == "Not online":
            self.__ui.btn.setEnabled(False)
            ImagePlayer.gifMovie(self.__ui.lblBuddy, UIResources.RESCOURCES_PIC["Offline"])
        elif stateText == "Busy":
            ImagePlayer.gifMovie(self.__ui.lblBuddy, UIResources.RESCOURCES_PIC["Busy"])

    def closeEvent(self, event):
        logging.info("Program close requested")
        self.emit(SIGNAL(SIGNALS.CLOSE))

    def btnStartCall(self):
        SIGNALS.emit(self, SIGNALS.CALL_NUMBER, self.numberToCall)
        self.__ui.btn.setText("Auflegen")
        self.__ui.cbPreview.setCheckable(False)
        self.__ui.btn.clicked.disconnect()
        self.__ui.btn.clicked.connect(self.btnHangup)
        
    def btnIncomingCallAccept(self):
        SIGNALS.emit(self, SIGNALS.CALL_CONNECT)     
        self.emit(SIGNAL(SIGNALS.MODULE_DISMISS),  self.MODULES_TO_LOAD[2])    
        self.__ui.btn.setText("Auflegen")
        self.__ui.cbPreview.setCheckable(False)
        self.__ui.btn.clicked.disconnect()        
        self.__ui.btn.clicked.connect(self.btnHangup)
    
    def btnHangup(self):
        SIGNALS.emit(self, SIGNALS.CALL_HANGUP)
        self.disableSignalLevelBars()
        self.__ui.btn.setText("Anrufen")
        self.__ui.btn.clicked.disconnect()
        self.__ui.btn.clicked.connect(self.btnStartCall)

    def showWindow(self):   
        self.__ui.show()
        logging.info("Stupid UI is up and running")
        self.emit(SIGNAL(SIGNALS.REGISTER_REQUEST_INITIAL_STATE))


