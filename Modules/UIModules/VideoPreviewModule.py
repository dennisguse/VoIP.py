from PyQt4.QtGui import *
from Modules.AbstractModule import AbstractModule
import Xlib
import pjsua as pj
import logging

from SIPController.VideoSettings import VideoSettings

class VideoPreviewModule(AbstractModule):
    def __init__(self, parent = None):
        self.logger = logging.getLogger("VideoShowModule")
        self.settings = VideoSettings()
        self.widget = None;

    def hasSignalsToRegister(self):
        return False

    def getSignals(self):
        return None

    def start(self, parentWindow, parentUI):
        if (self.widget != None):
            self.logger.error("Cannot re-use VideoShowModule.")
            return

        self.widget = QX11EmbedContainerAspect(parentWindow)
        parentUI.addWidget(self.widget)

        self.lib = pj.Lib.instance()
        previewWinID = self.lib.start_video_preview(self.settings.captureDevice, self.settings.renderDevice)
        self.reparentWindow(previewWinID)

    def dismiss(self):
        self.lib = pj.Lib.instance()
        self.lib.stop_video_preview()
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
            win.get_wm_name() #For unknown reason is this required!
        else:
            self.logger.error("Could not reparent window.")

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
        print("BLA2")
        return height;