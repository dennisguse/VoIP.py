import logging, time
from Modules.MainUIModules.AbstractUIModule import AbstractUIModule
from PyQt4.QtCore import *
from PyQt4 import uic, QtGui
from Defines import SIGNALS
from Defines.MODULES import MODULES
from Modules.UIModules import ImagePlayer
import Modules.UIModules.RESOURCES as UIResources
import Modules.MainUIModules.RESOURCES as MainUIResources
from ConfigModules import BuddyConfigModule

# Will replace SimpleVideoUI in the next updates
class SimpleVideoUI2(AbstractUIModule,  QtGui.QWidget):

    MODULES_TO_LOAD = ['ErrorDialog',  'WaveRecordModule',  'RingToneModule', 'SingleBuddyModule',
                       'VideoIncomingModule', 'VideoOutgoingModule', 'DeviceChooserModuleSimple', 'SystrayModule']

    def __init__(self, signalSource, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.logger = logging.getLogger("SimpleVideoUI")
        self.signalSource = signalSource
        self.initLayout()
        self.connectButtons()
        self.connectSignals()
        self.numberToCall = BuddyConfigModule.BuddyConfigModule().getBuddys()[0].number

    def initLayout(self):
        self.layout = QtGui.QVBoxLayout()
        self.resize(500,500)
        self.setMinimumSize(500,500)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setLayout(self.layout)
        self.videomgmt = VideoWindowMgmt(self)
        self.layout.addWidget(self.videomgmt)

    def resizeEvent(self, event):
        calcSize = QSize(10, 10)
        calcSize.scale(event.size(), Qt.KeepAspectRatio)
        self.resize(calcSize)

    def registerNewModules(self):
        for module in self.MODULES_TO_LOAD:
            SIGNALS.emit(self, SIGNALS.MODULE_LOAD, module, MODULES[module])
        self.emit(SIGNAL(SIGNALS.MODULE_ACTIVATE),  'WaveRecordModule')
        self.emit(SIGNAL(SIGNALS.MODULE_ACTIVATE),  'DeviceChooserModule')
        self.emit(SIGNAL(SIGNALS.MODULE_ACTIVATE),  'SingleBuddyModule')
        self.emit(SIGNAL(SIGNALS.MODULE_ACTIVATE),  'SystrayModule', {"ui":self})

    def connectButtons(self):
        self.videomgmt.rbOnline.toggled.connect(self.onManuallyStatusChange)

    def connectSignals(self):
        self.connect(self.signalSource, SIGNAL(SIGNALS.CALL_INCOMING), self.onIncomingCall)
        self.connect(self.signalSource, SIGNAL(SIGNALS.CALL_INCOMING_CANCELED), self.onIncomingCallCanceled)
        self.connect(self.signalSource, SIGNAL(SIGNALS.CALL_OUTGOING_CANCELED), self.onOutgoingCallCanceled)
        self.connect(self.signalSource, SIGNAL(SIGNALS.REGISTER_STATE_CHANGE), self.onRegStateSignal)
        self.connect(self.signalSource, SIGNAL(SIGNALS.BUDDY_STATE_CHANGED), self.onBuddyStateChanged)
        self.connect(self.signalSource, SIGNAL(SIGNALS.CALL_SHOW_VIDEO), self.showCallVideo)
        self.connect(self.signalSource, SIGNAL(SIGNALS.CALL_ESTABLISHED), self.onEstablished)

    def onIncomingCall(self,  incomingCallerNumber):
        logging.info("Got incoming call from: " + incomingCallerNumber)
        self.emit(SIGNAL(SIGNALS.MODULE_ACTIVATE),  'RingToneModule',  None)
        self.videomgmt.btnCall.setText("Anruf annehmen")
        self.videomgmt.btnCall.clicked.disconnect()
        self.videomgmt.btnCall.clicked.connect(self.btnIncomingCallAccept)

    def onIncomingCallCanceled(self):
        self.emit(SIGNAL(SIGNALS.MODULE_DISMISS),  'RingToneModule')
        self.videomgmt.btnCall.setText("Anrufen")
        self.videomgmt.btnCall.clicked.disconnect()
        self.videomgmt.btnCall.clicked.connect(self.btnStartCall)

    def onOutgoingCallCanceled(self):
        self.videomgmt.btnCall.setText("Anrufen")
        self.emit(SIGNAL(SIGNALS.MODULE_DISMISS), 'VideoCallModule')
        self.emit(SIGNAL(SIGNALS.MODULE_DISMISS), 'SignalbarModule')
        self.videomgmt.btnCall.clicked.disconnect()
        self.videomgmt.btnCall.clicked.connect(self.btnStartCall)

    def onRegStateSignal(self, isActive, reg_code, reg_reason): #Mehrfach aufrufen?
        if isActive == True:
            #Enable UI
            self.videomgmt.btnCall.setEnabled(True)
            self.videomgmt.btnCall.clicked.connect(self.btnStartCall)
            ImagePlayer.gifMovie(self.videomgmt.regState,  UIResources.RESCOURCES_PIC["Online"])
        else:
            #Disable UI and error message
            self.videomgmt.btnCall.setEnabled(False)
            ImagePlayer.gifMovie(self.videomgmt.regState,  UIResources.RESCOURCES_PIC["LoadAnimation"])
        self.videomgmt.regState.setToolTip("RegCode: " + str(reg_code) + " RegReason: " + reg_reason)

    def onBuddyStateChanged(self, state_code, state_text):
        self.videomgmt.control.onBuddyStateChanged(state_code, state_text)

    def closeEvent(self, event):
        logging.info("Program close requested")
        self.emit(SIGNAL(SIGNALS.CLOSE))

    def btnStartCall(self):
        SIGNALS.emit(self, SIGNALS.CALL_NUMBER, self.numberToCall)
        self.videomgmt.btnCall.setText("Auflegen")
        self.videomgmt.btnCall.clicked.disconnect()
        self.videomgmt.btnCall.clicked.connect(self.btnHangup)

    def btnIncomingCallAccept(self):
        SIGNALS.emit(self, SIGNALS.CALL_CONNECT)
        self.emit(SIGNAL(SIGNALS.MODULE_DISMISS),  self.MODULES_TO_LOAD[2])
        self.videomgmt.btnCall.setText("Auflegen")
        self.videomgmt.btnCall.clicked.disconnect()
        self.videomgmt.btnCall.clicked.connect(self.btnHangup)

    def btnHangup(self):
        SIGNALS.emit(self, SIGNALS.CALL_HANGUP)
        self.emit(SIGNAL(SIGNALS.MODULE_DISMISS), 'VideoCallModule')
        self.emit(SIGNAL(SIGNALS.MODULE_DISMISS), 'SignalbarModule')
        self.videomgmt.btnCall.setText("Anrufen")
        self.videomgmt.btnCall.clicked.disconnect()
        self.videomgmt.btnCall.clicked.connect(self.btnStartCall)
        self.disableCallButton()

    def disableCallButton(self):
        self.videomgmt.btnCall.setEnabled(False)
        QTimer.singleShot(500, self.enableCallButton )

    def enableCallButton(self):
        self.videomgmt.btnCall.setEnabled(True)

    def showCallVideo(self, winID):
        #self.emit(SIGNAL(SIGNALS.MODULE_ACTIVATE), 'VideoIncomingModule', {"windowId": winID, "parentWindow": self, "parentContainer": self.__ui.videoIncoming})
        pass

    def showWindow(self):
        self.show()
        self.logger.info("Simple Video UI is up and running")
        self.emit(SIGNAL(SIGNALS.REGISTER_REQUEST_INITIAL_STATE))
        self.emit(SIGNAL(SIGNALS.MODULE_ACTIVATE), 'VideoOutgoingModule', {"parentWindow": self.videomgmt.preview, "parentContainer": self.videomgmt.preview.layout})

    def onEstablished(self):
        #self.emit(SIGNAL(SIGNALS.MODULE_ACTIVATE),  'SignalbarModule', {"parent":self, "parentLayout":self.__ui.gridLayout, "signalSource": self.signalSource})
        pass

    def onManuallyStatusChange(self):
        if self.videomgmt.rbOnline.isChecked() == False:
            SIGNALS.emit(self, SIGNALS.OWN_ONLINE_STATE_CHANGED, False)
        else:
            SIGNALS.emit(self, SIGNALS.OWN_ONLINE_STATE_CHANGED, True)


class VideoWindowMgmt(QtGui.QWidget):

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.black)
        self.setPalette(p)
        self.setAutoFillBackground(True)
        hbox = QtGui.QHBoxLayout()
        self.setLayout(hbox)
        self.setMouseTracking(True)
        self.setControl()
        self.setPreview()
        self.timer = Timer(4)
        self.connect(self.timer, SIGNAL("BEEPBEEP"), self.hideControl)
        self.timer.start()
        self.btnCall = self.control.ui.btnCall
        self.regState = self.control.ui.lblRegState
        self.rbOnline = self.control.ui.rbOnline

    def showWindow(self):
        self.show()

    def hide(self):
        self.setVisible(False)

    def setControl(self):
        self.control = VideoControlWindow(self)
        self.adjustControl()

    def setPreview(self):
        self.preview = PreviewWindow(self)
        self.preview.showWindow()
        self.adjustPreview()

    def hideControl(self):
        self.control.hide()

    def showControl(self):
        self.control.appear()
        self.adjustControl()

    def resizeEvent(self, event):
        calcSize = QSize(10, 10)
        calcSize.scale(event.size(), Qt.KeepAspectRatio)
        self.resize(calcSize)
        self.adjustControl()
        self.adjustPreview()

    def mouseMoveEvent(self, event):
        self.showControl()
        self.timer.addTime(5)
        if self.timer.running == False:
            self.timer.start()

    def adjustControl(self):
        size = self.size()
        adjustedHeigth = size.height() - 50
        adjustedWidth = (size.width() / 2) - 170
        if adjustedHeigth < 0:
            adjustedHeigth = size.height() - 100
        if adjustedWidth < 0:
            adjustedWidth = 0
        self.control.move(adjustedWidth , adjustedHeigth)

    def adjustPreview(self):
        size = self.size()
        adjustedHeigth = size.height() - 200
        adjustedWidth = size.width() - 170
        if adjustedHeigth < 0:
            adjustedHeigth = size.height() - 100
        if adjustedWidth < 0:
            adjustedWidth = 0
        self.preview.move(adjustedWidth , adjustedHeigth)

    def show(self):
        self.show()

class PreviewWindow(QtGui.QWidget):

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.green)
        self.setPalette(p)
        self.setAutoFillBackground(True)
        self.layout = QtGui.QHBoxLayout()
        self.setLayout(self.layout)
        self.resize(150,150)
        self.setMinimumSize(150,150)
        self.setMaximumSize(150,150)


    def showWindow(self):
        self.show()


class IncomingVideoWindow(QtGui.QWidget):

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.blue)
        self.setPalette(p)
        self.setAutoFillBackground(True)

    def showWindow(self):
        self.show()

class VideoControlWindow(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = uic.loadUi("./Modules/UIModules/UIResources/VideoControlDialog.ui",self)
        self.ui.btnCall.setEnabled(False)
        self.ui.btnCall.setText("Anrufen")

    def showWindow(self):
        self.show()

    def hide(self):
        self.setVisible(False)

    def appear(self):
        self.setVisible(True)


    def onBuddyStateChanged(self, state_code, state_text):
        self.ui.lblBuddy.setToolTip("BuddyState: " + str(state_text))
        if state_text == "Ready":
            ImagePlayer.gifMovie(self.ui.lblBuddy,  UIResources.RESCOURCES_PIC["Online"])
            self.ui.lblBuddy.setEnabled(True)
        elif state_text == "Not online":
            self.ui.lblBuddy.setEnabled(False)
            ImagePlayer.gifMovie(self.ui.lblBuddy, UIResources.RESCOURCES_PIC["Offline"])
        elif state_text == "Busy":
            ImagePlayer.gifMovie(self.ui.lblBuddy, UIResources.RESCOURCES_PIC["Busy"])


class Timer(QThread):

    def __init__(self, time):
        QThread.__init__(self)
        self.time = time
        self.running = False

    def run(self):
        self.running = True
        while self.time > 0:
            time.sleep(1)
            self.time -= 1
        self.emit(SIGNAL("BEEPBEEP"))
        self.running = False

    def addTime(self, time):
        if self.time < 5:
            self.time += time
        if self.time > 5:
            self.time = 5