import logging, signal

from Modules.MainUIModules.AbstractUIModule import AbstractUIModule
from PyQt4.QtCore import *
from PyQt4 import uic, QtGui
from Defines import SIGNALS
from PyQt4.QtCore import SIGNAL
from Defines.MODULES import MODULES
from Modules.UIModules import ImagePlayer
import Modules.UIModules.RESOURCES as UIResources
import Modules.MainUIModules.RESOURCES as MainUIResources
from ConfigModules import BuddyConfigModule


class SimpleUI(AbstractUIModule,  QtGui.QWidget):
    
    MODULES_TO_LOAD = ['ErrorDialog',  'WaveRecordModule',  'RingToneModule', 'SingleBuddyModule',
                       'DeviceChooserModuleSimple', 'SystrayModule']
    
    def __init__(self, signalSource, parent=None):
        QtGui.QWidget.__init__(self, parent)   
        self.signalSource = signalSource
        self.__ui = uic.loadUi(MainUIResources.RESCOURCES_MAINUI["Simple"], self)
        self.move(QtGui.QApplication.desktop().screen().rect().center()- self.rect().center()) #Move window to center
        self.connectButtons()
        self.connectSignals()
        self.numberToCall = BuddyConfigModule.BuddyConfigModule().getBuddys()[0].number
        self.__ui.checkBox.stateChanged.connect(self.onManuallyStatusChange)
        self.__ui.btn.setStyleSheet('QPushButton {color: white; background-color: green}')

    def registerNewModules(self):        
        for module in self.MODULES_TO_LOAD:
            SIGNALS.emit(self, SIGNALS.MODULE_LOAD, module, MODULES[module])
        self.emit(SIGNAL(SIGNALS.MODULE_ACTIVATE),  'WaveRecordModule')
        self.emit(SIGNAL(SIGNALS.MODULE_ACTIVATE),  'DeviceChooserModuleSimple')
        self.emit(SIGNAL(SIGNALS.REGISTER))
        self.emit(SIGNAL(SIGNALS.MODULE_ACTIVATE),  'SingleBuddyModule')
        self.emit(SIGNAL(SIGNALS.MODULE_ACTIVATE),  'SystrayModule', {"ui":self})



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
        self.__ui.btn.setStyleSheet('QPushButton {color: white; background-color: blue}')
        self.__ui.btn.clicked.disconnect()
        self.__ui.btn.clicked.connect(self.btnIncomingCallAccept)
        
    def onIncomingCallCanceled(self):
        self.emit(SIGNAL(SIGNALS.MODULE_DISMISS),  'RingToneModule')
        self.__ui.btn.setStyleSheet('QPushButton {color: white; background-color: green}')
        self.__ui.btn.setText("Anrufen")
        self.__ui.btn.clicked.disconnect()
        self.__ui.btn.clicked.connect(self.btnStartCall)

    def onOutgoingCallCanceled(self):
        self.__ui.btn.setText("Anrufen")
        self.__ui.btn.setStyleSheet('QPushButton {color: white; background-color: green}')
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

    def onBuddyStateChanged(self, state_code, state_text):
        self.__ui.lblBuddy.setToolTip("BuddyState: " + state_text)
        if state_text == "Ready":
            ImagePlayer.gifMovie(self.__ui.lblBuddy,  UIResources.RESCOURCES_PIC["Online"])
            self.__ui.btn.setEnabled(True)
            if self.__ui.btn.text() == "Anrufen":
                self.__ui.btn.setStyleSheet('QPushButton {color: white; background-color: green}')
        elif state_text == "Not online":
            self.__ui.btn.setEnabled(False)
            ImagePlayer.gifMovie(self.__ui.lblBuddy, UIResources.RESCOURCES_PIC["Offline"])
            self.__ui.btn.setStyleSheet('QPushButton {color: white; background-color: grey}')
        elif state_text == "Busy":
            ImagePlayer.gifMovie(self.__ui.lblBuddy, UIResources.RESCOURCES_PIC["Busy"])

    def closeEvent(self, event):
        logging.info("Program close requested")
        self.__ui.setVisible(False)
        self.emit(SIGNAL(SIGNALS.CLOSE))

    def btnStartCall(self):
        SIGNALS.emit(self, SIGNALS.CALL_NUMBER, self.numberToCall)
        self.__ui.btn.setText("Auflegen")
        self.__ui.btn.setStyleSheet('QPushButton {color: white; background-color: red}')
        self.__ui.btn.clicked.disconnect()
        self.__ui.btn.clicked.connect(self.btnHangup)
        
    def btnIncomingCallAccept(self):
        SIGNALS.emit(self, SIGNALS.CALL_CONNECT)     
        self.emit(SIGNAL(SIGNALS.MODULE_DISMISS),  self.MODULES_TO_LOAD[2])    
        self.__ui.btn.setText("Auflegen")
        self.__ui.btn.setStyleSheet('QPushButton {color: white; background-color: red}')
        self.__ui.btn.clicked.disconnect()        
        self.__ui.btn.clicked.connect(self.btnHangup)
    
    def btnHangup(self):
        SIGNALS.emit(self, SIGNALS.CALL_HANGUP)
        self.__ui.btn.setStyleSheet('QPushButton {color: white; background-color: green}')
        self.__ui.btn.setText("Anrufen")
        self.__ui.btn.clicked.disconnect()
        self.__ui.btn.clicked.connect(self.btnStartCall)
        self.disableCallButton()

    def disableCallButton(self):
        self.__ui.btn.setEnabled(False)
        QTimer.singleShot(500, self.enableCallButton )

    def enableCallButton(self):
        self.__ui.btn.setEnabled(True)

    def onManuallyStatusChange(self):
        if self.__ui.checkBox.isChecked() == False:
            SIGNALS.emit(self, SIGNALS.OWN_ONLINE_STATE_CHANGED, False)
        else:
            SIGNALS.emit(self, SIGNALS.OWN_ONLINE_STATE_CHANGED, True)

    def showWindow(self):   
        self.__ui.show()
        logging.info("SimpleUI is up and running")
        self.emit(SIGNAL(SIGNALS.REGISTER_REQUEST_INITIAL_STATE))


