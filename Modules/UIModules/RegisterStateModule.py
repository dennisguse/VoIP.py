from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import uic
from Modules.AbstractModule import AbstractModule
import Modules.UIModules.RESOURCES as UIResources

class RegisterStateDialog(QDialog,  AbstractModule):
    
    def __init__(self,  parent = None):
        super(RegisterStateDialog, self).__init__(parent)
        self.dia = uic.loadUi(UIResources.RESCOURCES_UI["RegisterDialog"], self)
        return
    
    def start(self, optionalParameter = None):
        if optionalParameter == None:
            pass
        else:
            pass
        self.dia.show()        
        self.dia.exec_()
    
    def dismiss(self):        
        self.dia.close()
        pass
    

    
