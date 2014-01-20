from PyQt4.QtGui import *
from PyQt4.QtCore import *
from Modules.AbstractModule import AbstractModule
from Xlib import X, display, Xutil
import Xlib
import pjsua as pj
from SIPController.VideoSettings import VideoSettings

class VideoPreviewModule(AbstractModule): #TODO QX11EmbedContainer inherit from.
    def __init__(self, parent = None):
        self.settings = VideoSettings()

    def hasSignalsToRegister(self):
        return False

    def getSignals(self):
        return None

    def start(self, parentWindow, parentUI):
        self.widget = QX11EmbedContainer(parentWindow)
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
            print (self.widget.winId())
            win.reparent(self.widget.winId(), 0, 0)
            #win.reparent(self.winId, 0, 0)
            print(win.get_wm_name())
            win.raise_window()
            win.set_wm_normal_hints(flags=(Xutil.PPosition | Xutil.PSize | Xutil.PMinSize),min_width=50,min_height=50)
            hints = win.get_wm_normal_hints()
        else:
            print("Not successful")

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