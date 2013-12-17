from Modules.MainUIModules.AbstractUIModule import AbstractUIModule
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import uic, QtGui
from Defines import SIGNALS
from Defines.MODULES import MODULES
import Modules.MainUIModules.RESOURCES as MainUIResources

class StandardUI(AbstractUIModule,  QtGui.QWidget):
    
    MODULES_TO_LOAD = ['IncomingCallDialog',  'ErrorDialog']
    
    def __init__(self, signalSource):        
        QtGui.QWidget.__init__(self, None)        
        self.__ui = uic.loadUi(MainUIResources.RESCOURCES_MAINUI["Standard"], self)
        self.signalSource = signalSource
        self.connectSignals()
        self.connectButtons()
        self.connectLineEdits()
        
        #self.__settingsWidget = SettingsWidget.SettingsWidget(self.__ui,  self.account)
        #self.__secureWidget = SecurityWidget.SecurityWidget(self.__ui,  self.account)
        
    def registerNewModules(self):
        for module in self.MODULES_TO_LOAD:
            SIGNALS.emit(self, SIGNALS.MODULE_LOAD, module , MODULES[module])     
        
    def registerNewSignals(self):
        print ("Trying to register costume signals")
        
    def connectButtons(self):
        """
        Connect all UI buttons.
        """
        self.__ui.butCall0.clicked.connect(self.butNumberClicked)
        self.__ui.butCall1.clicked.connect(self.butNumberClicked)
        self.__ui.butCall2.clicked.connect(self.butNumberClicked)
        self.__ui.butCall3.clicked.connect(self.butNumberClicked)
        self.__ui.butCall4.clicked.connect(self.butNumberClicked)
        self.__ui.butCall5.clicked.connect(self.butNumberClicked)
        self.__ui.butCall6.clicked.connect(self.butNumberClicked)
        self.__ui.butCall7.clicked.connect(self.butNumberClicked)
        self.__ui.butCall8.clicked.connect(self.butNumberClicked)
        self.__ui.butCall9.clicked.connect(self.butNumberClicked)
        self.__ui.butCallCall.clicked.connect(self.butCallClicked)
        self.__ui.butCallHangup.clicked.connect(self.butHangupClicked)
#        self.__ui.butFriends.clicked.connect(self.showFriendsList)

    def connectSignals(self):
        """
        Connect all incoming signals.
        """        
        self.connect(self.signalSource,  SIGNAL(SIGNALS.CALL_INCOMING),  self.onIncomingCall)        
        self.connect(self.signalSource,  SIGNAL(SIGNALS.CALL_INCOMING_CANCELED),  self.onIncomingCallCanceled)       

    def connectLineEdits(self):
        """
        Connect all line edit UI elements.
        """
        self.__ui.leCallNumber.returnPressed.connect(self.onLineEditNumberEnter)

    def  onIncomingCall(self,  incomingCallerNumber):
        """
        Shows a dialog if there is an incoming call.
        Emits the signal to play and stop (if the dialog is closed) the ring tone
        """
        self.emit(SIGNAL(SIGNALS.MODULE_ACTIVATE),  'IncomingCallDialog',  incomingCallerNumber)

    def onIncomingCallCanceled(self):
        self.emit(SIGNAL(SIGNALS.MODULE_DISMISS),  'IncomingCallDialog')

    def onLineEditNumberEnter(self):
        """
        If the user presses enter the number form the numbers field will be called.
        """
        self.butCallClicked()  

    def closeEvent(self, event):
        """
        Emits the signal to close the program.
        """
        self.emit(SIGNAL(SIGNALS.CLOSE))

    def butNumberClicked(self):
        """
        Inserts the clicked number in the number field.
        """
        if self.__ui.leCallNumber.text() != None:
            self.__ui.leCallNumber.insert(self.sender().text())
        else:
            self.__ui.leCallNumber.setText(self.sender().text())

    def butCallClicked(self):
        """
        Starts to call the specified number.
        If the user didn't entered a number a warning will be displayed.
        """
        if self.__ui.leCallNumber.text() != None and len(self.__ui.leCallNumber.text()) != 0:
            self.emit(SIGNAL(SIGNALS.CALL_NUMBER),  self.__ui.leCallNumber.text())
        else: 
            self.showError("No number specified!")
        
    def butHangupClicked(self):
        """
        Clear the number the user entered in the number field.
        """
        self.ui.leCallNumber.setText("")
    
    def showError(self, text = "There was an error.", title = "Error!"):
        """
        Shows an error message box.
        @type text: string
        @param text: The text of the message box
        @type title: string
        @param title: The title of the message box
        @note: Default message box has the title 'Error!' and the text 'There was an error'
        """
        self.emit(SIGNAL(SIGNALS.MODULE_ACTIVATE),  'ErrorDialog',  [title,  text])

    def showWindow(self):
        """
        Shows this UI
        """
        self.__ui.show()
        self.__ui.laRegState.setStyleSheet('background-color: red')
    
    
