from Modules.MainUIModules.SimpleUIModule import SimpleUI
from Modules.MainUIModules.StandardUIModule import StandardUI
from Modules.MainUIModules.SimpleVideoUIModule import SimpleVideoUI
from PyQt4.QtGui import QApplication
import sys

class UILoader(object):

    def __init__(self, signalSource,  uiMode = None):
        self.app = QApplication(sys.argv)
        #modeOptions = {MODES.STANDARD: StandardUI, MODES.STUPID: SimpleUI, MODES.SIMPLEVIDEO: SimpleVideoUI}
        #try:
        #    self.ui = modeOptions[uiMode](signalSource)
        #except:
        #    self.ui = modeOptions[MODES.STUPID](signalSource)

        #TODO Remove string comparison and use check for available classes.
        if uiMode == "simpleVideo":
            self.ui = SimpleVideoUI(signalSource)
        elif uiMode == "simple":
            self.ui = SimpleUI(signalSource)

    def start(self):
        self.app.setActiveWindow(self.ui)
        self.ui.showWindow()
        self.app.exec_()