from PyQt4.QtGui import *
from PyQt4.QtCore import *

class ErrorDialog(QDialog):
    
    def __init__(self):
        super(ErrorDialog, self).__init__(None)
        self.dia = QMessageBox()
        return

    def hasSignalsToRegister(self):
        return False
    
    def start(self, optionalParameter = None):
        if optionalParameter == None:
            self.dia.setWindowTitle(optionalParameter[0])
            self.dia.setText(optionalParameter[1])
        else:
            self.dia.setWindowTitle('Error')
            self.dia.setText('There was an error')
        self.dia.show()        
        self.dia.exec_()
    
    def dismiss(self):
        pass
    

    
