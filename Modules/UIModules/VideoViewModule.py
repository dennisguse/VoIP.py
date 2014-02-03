import logging
import Xlib.display

from PyQt4.QtGui import *
from Modules.AbstractModule import AbstractModule
from ConfigModules.VideoDeviceModule import VideoDeviceModule

class VideoViewModule(AbstractModule):
    def __init__(self):
        self.logger = logging.getLogger("VideoViewModule")
        self.settings = VideoDeviceModule()
        self.widget = None;

    def hasSignalsToRegister(self):
        return False

    def getSignals(self):
        return None

    def showVideoPane(self, parentWindow, parentContainer, windowId):
        if self.widget is None:  # We need to create the widget as this is the first call.
            self.widget = QX11EmbedContainer(parentWindow)
            parentContainer.addWidget(self.widget)
        self.reparentWindow(windowId)

    def dismissVideoPane(self):
        try:
            self.widget.close()
            self.widget.destroy()
        except:
            pass
        self.widget = None

    def reparentWindow(self, winId):
        win = self.getWin(int(winId))
        if win:
            win.map()
            win.raise_window()
            win.reparent(self.widget.winId(), 0, 0)
            win.get_wm_name()  # For unknown reason is this required!
        else:
            self.logger.error("Could not re-parent window.")

    def getWin(self, winId):
        display = Xlib.display.Display()
        root = display.screen().root
        winList = [root]
        while len(winList) != 0:
            win = winList.pop(0)
            if win.id == winId:
                return win
            win_children = win.query_tree().children
            if win_children != None:
                winList += win_children
        return None

class QX11EmbedContainerAspect(QX11EmbedContainer):
    def _init__(self, parent=None):
        QX11EmbedContainer.__init__(self, parent)
        policy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        policy.setHeightForWidth(True)
        policy.setWidthForHeight(True)

        self.setSizePolicy(policy)

    def heightForWidth(self, height):
        return height;