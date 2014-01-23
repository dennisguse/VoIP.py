from PyQt4 import QtCore
import pjsua as pj
from Modules.AbstractModule import AbstractModule

class RingToneModule(QtCore.QThread,  AbstractModule):
  
    def __init__(self,  pathToRingTone = './Resources/phone.wav'):
        super(RingToneModule,self).__init__()
        self.ringToneFilePath = pathToRingTone
        self.lib = pj.Lib.instance()

    def start(self):
        self.playLoop = True
        self.playerID = self.lib.create_player(self.ringToneFilePath, True)
        self.playerSlot = self.lib.player_get_slot(self.playerID)
        self.lib.conf_connect(self.playerSlot, 0)

    def dismiss(self):
        try:
            self.lib.conf_disconnect(self.playerSlot, 0)
            self.lib.player_destroy(self.playerID)
        except:
            pass

