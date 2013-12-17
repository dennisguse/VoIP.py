from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import uic
from Modules.MainUIModules.AbstractUIModule import AbstractUIModule
import Modules.UIModules.RESOURCES as UIResources

class IncomingCallDialog(QDialog, AbstractUIModule):
    
    def __init__(self, callerNumber = "No number to display", parent = None):
        super(IncomingCallDialog, self).__init__(parent)
        self.dia = uic.loadUi(UIResources.RESCOURCES_UI["IncomingCallDialog"], self)
        self.dia.pbAccept.clicked.connect(self.acceptClicked)
        self.dia.pbDecline.clicked.connect(self.DeclinedClicked)
        self.dia.laNumber.setText(callerNumber)                
        return
        
    def start(self,  optionalParameter = None):
        if optionalParameter:
            self.dia.laNumber.setText(optionalParameter)
        self.dia.show()
        
    def dismiss(self):
        self.close()
    
    def hasSignalsToRegister(self):
        return True
    
    def getSignals(self):
        return [['INCOMINGCALLDIALOGACCEPT',  None,  'onConnectCallSignal'],  ['INCOMINGCALLDIALOGDECLINED',  None,  'onHangupCallSignal']]
    
    def acceptClicked(self):        
        self.emit(SIGNAL("INCOMINGCALLDIALOGACCEPT"))
        self.close()
        return
    
    def DeclinedClicked(self):
        self.emit(SIGNAL("INCOMINGCALLDIALOGDECLINED"))
        self.close()
        return    
