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
from ConfigModules import BuddyConfigModule

class SimpleVideoUI(AbstractUIModule,  QtGui.QWidget):
    
    MODULES_TO_LOAD = ['ErrorDialog',  'WaveRecordModule',  'RingToneModule', 'SingleBuddyModule',
                       'VideoPreviewModule', 'VideoCallModule', 'DeviceChooserModuleSimple']
    
    def __init__(self, signalSource, parent=None):
        QtGui.QWidget.__init__(self, parent)   
        self.signalSource = signalSource
        self.__ui = uic.loadUi(MainUIResources.RESCOURCES_MAINUI["SimpleVideo"], self)
        self.connectButtons()
        self.connectSignals()
        self.numberToCall = BuddyConfigModule.BuddyConfigModule().getBuddys()[0].number
        self.signalLevelThread = None
        self.disableSignalLevelBars()
        self.__ui.cbOwnStatus.currentIndexChanged.connect(self.onManuallyStatusChange)
        
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
        self.connect(self.signalSource, SIGNAL(SIGNALS.CALL_SHOW_VIDEO), self.showCallVideo)
        self.connect(self.signalSource, SIGNAL(SIGNALS.CALL_ESTABLISHED), self.onEstablished)
        self.connect(self.signalSource, SIGNAL(SIGNALS.CALL_SIGNAL_LEVEL_CHANGE), self.showSignalLevel)
    
    def onIncomingCall(self,  incomingCallerNumber):
        try:
            #self.emit(SIGNAL(SIGNALS.MODULE_DISMISS), 'VideoPreviewModule')
            pass
        except:
            pass
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
        self.disableSignalLevelBars()
        self.emit(SIGNAL(SIGNALS.MODULE_DISMISS), 'VideoCallModule')
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
        try:
            #self.emit(SIGNAL(SIGNALS.MODULE_DISMISS), 'VideoPreviewModule')
            pass
        except:
            pass
        SIGNALS.emit(self, SIGNALS.CALL_NUMBER, self.numberToCall)
        self.__ui.btn.setText("Auflegen")
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
        self.emit(SIGNAL(SIGNALS.MODULE_DISMISS), 'VideoCallModule')
        self.disableSignalLevelBars()
        self.__ui.btn.setText("Anrufen")
        self.__ui.btn.clicked.disconnect()
        self.__ui.btn.clicked.connect(self.btnStartCall)
        self.disableCallButton()

    def disableCallButton(self):
        self.__ui.btn.setEnabled(False)
        self.timer = AsyncTimer()
        self.connect( self.timer, SIGNAL("TIMER_END"), self.enableCallButton )
        self.timer.start()

    def enableCallButton(self):
        self.__ui.btn.setEnabled(True)



    def showCallVideo(self, winID):
        self.emit(SIGNAL(SIGNALS.MODULE_ACTIVATE), 'VideoCallModule', [winID, self, self.__ui.videoIncoming])

    def showWindow(self):   
        self.__ui.show()
        logging.info("Simple Video UI is up and running")
        self.emit(SIGNAL(SIGNALS.REGISTER_REQUEST_INITIAL_STATE))
        self.emit(SIGNAL(SIGNALS.MODULE_ACTIVATE), 'VideoPreviewModule', self, self.__ui.videoOutgoing)

    def showSignalLevel(self, level):
        self.__ui.pbTx.setValue(int(level[0] * 100))
        self.__ui.pbRx.setValue(int(level[1] * 100))

    def requestSignalUpdate(self):
        self.emit(SIGNAL(SIGNALS.CALL_SIGNAL_LEVEL_REQUEST))

    def onEstablished(self):
        self.__ui.pbRx.setEnabled(True)
        self.__ui.pbTx.setEnabled(True)
        self.signalLevelThread = SignalLevelThread(self.requestSignalUpdate)
        self.signalLevelThread.start()

    def disableSignalLevelBars(self):
        self.__ui.pbRx.setValue(0)
        self.__ui.pbTx.setValue(0)
        self.__ui.pbRx.setDisabled(True)
        self.__ui.pbTx.setDisabled(True)
        try:
            self.signalLevelThread.stop()
            self.signalLevelThread = None
        except:
            pass

    def onManuallyStatusChange(self, status):
        if status == 1:
            SIGNALS.emit(self, SIGNALS.OWN_ONLINE_STATE_CHANGED, False)
        else:
            SIGNALS.emit(self, SIGNALS.OWN_ONLINE_STATE_CHANGED, True)

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

class AsyncTimer(QThread):

    def __init__(self, timeToSleep=2):
        QThread.__init__(self)
        self.timeToSleep = timeToSleep

    def run(self):
        time.sleep(self.timeToSleep)
        self.emit(SIGNAL("TIMER_END"))
