from PyQt4.QtGui import QDialog as QDialog
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from Modules.AbstractModule import AbstractModule
from Xlib import X, display, Xutil
import Xlib
import pjsua as pj
from SIPController.VideoSettings import VideoSettings


class VideoCallModule(AbstractModule):
    def __init__(self, parent = None):
        self.settings = VideoSettings()
        self.parent = parent
        self.widget = None

    def hasSignalsToRegister(self):
        return False

    def getSignals(self):
        return None

    def start(self, parameters):
        if not self.widget:
            self.initWin(parameters[1], parameters[2])
            print(self.widget.winId())
        self.winIDExtern = parameters[0]
        self.resizeEvent()
        self.reparentWindow(self.winIDExtern)



    def initWin(self, parentWindow, parentUI):
        self.widget = QX11EmbedContainer(parentWindow)x
        parentUI.addWidget(self.widget)
        self.widget.resizeEvent.connect(self.resizeEvent)

    def dismiss(self):
        try:
            self.widget.close()
            self.widget.destroy()
            self.retryCounter = 0
        except:
            pass
        self.widget = None

    def reparentWindow(self, winId):
        try:
            win = self.getWin(int(winId))
            if win:
                win.map()
                win.raise_window()
                win.reparent(self.widget.winId(), 0, 0)
                print(win.get_wm_name())
                win.raise_window()
                win.set_wm_normal_hints(flags=(Xutil.PPosition | Xutil.PSize | Xutil.PMinSize),min_width=50,min_height=50)
                #hints = win.get_wm_normal_hints()
            else:
                print("Not successfull reparented window")
                #self.reparentWindow(windId)
        except:
            pass

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

    def resizeEvent(self, event=None):
        print ("!!!!!!!!!!!!!!!!!!!!!!!!!!!GOT EVENT")
        height = self.widget.size.height
        width = self.widget.size.width
        pj.Lib.instance().vid_win_set_size(self.winIDExtern, width, height)
