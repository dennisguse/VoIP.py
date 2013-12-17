from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import QtCore
from PyQt4 import uic
import Modules.UIModules.RESOURCES as UIResources

class CallDialog(QDialog):
    dia = None
    
    def __init__(self):
        super(CallDialog, self).__init__(None)
        self.dia = uic.loadUi(UIResources.RESCOURCES_UI["CallDialog"], self)
        
        #self.dia.butCallDialogHangup.clicked.connect(self.hangupClick)
        #self.dia.butCallDialogStats.clicked.connect(self.statsClicked)
        #self.dia.laCallDialogDest.setText(call.info().contact)
        #self.call._cb.setExternalCallDisconectEvent(self.dismiss)
        #self.clock = self.dia.lcdCallDialogTime
        #self.setTimer()
        #self.userHangup = False
        return
    
    def registerSignals(self):
        pass
        
    def hasSignalsToRegister(self):
        return True
    
    def show(self):
        self.dia.show()
    
    def hangupClick(self):
        if self.call != None:
            self.timer.destroyTimer()
        self.close()
        return
    
    def statsClicked(self):
        stats = CallStatisticsDialog.CallStatisticsDialog(self.call)
        stats.show()
        stats.exec_()
        return
    
    def setTimer(self):
        self.timer = TimerThread.TimerThread()
        self.connect(self.timer, QtCore.SIGNAL('timerSignal'), self.increaseTimeBySecond)
        self.timer.start()
        self.callTime = int(0)
        self.clock.setNumDigits(8)
        return
        
    def increaseTimeBySecond(self):
        self.callTime += 1
        self.clock.display(int(self.callTime))
        
    def dismiss(self):
        self.timer.destroyTimer()
        self.close()
    
    def isHangupClicked(self):
        self.userHangup = True
