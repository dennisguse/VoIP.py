from PyQt4 import QtCore
import sys,time
from PyQt4.QtGui import QApplication
from PyQt4.QtGui import QWidget

class LoadingThread(QtCore.QThread):
    def __init__(self):
        QtCore.QThread.__init__(self)
        self.ready = True

    def run(self):
        w = QWidget()
        w.resize(250, 150)
        w.move(300, 300)
        w.setWindowTitle('Simple')
        w.show()
        while(self.ready):
            time.sleep(0.1)

    def stop(self):
        self.ready = False
