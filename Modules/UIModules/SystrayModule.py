from PyQt4.QtGui import *
from Modules.AbstractModule import AbstractModule

class SystrayModule(AbstractModule):

    def __init__(self):
        super(AbstractModule, self).__init__()
        self.ui = None;
        self.systray_icon = QSystemTrayIcon(QIcon('./Resources/Pictograms-nps-telephone-2.svg'))
        self.systray_icon.activated.connect(self.trayActivated)

    def hasSignalsToRegister(self):
        return False

    def getSignals(self):
        return None


    def start(self, parameters):
        self.ui = parameters["ui"] # TODO Check type!
        self.systray_icon.show()

    def dismiss(self):
        self.ui = None
        self.systray_icon = None


    def trayActivated(self):
        if self.ui is None:
            return

        if self.ui.isVisible():
            self.ui.hide()

        else:
            self.ui.show()
            self.ui.raise_()