from PyQt4 import QtCore
import pjsua2 as pj
from Modules.AbstractModule import AbstractModule
from SIPController.Endpoint import Endpoint as ep

class RingToneModule(QtCore.QThread,  AbstractModule):
  
    def __init__(self,  pathToRingTone = './Resources/phone.wav'):
        super(RingToneModule,self).__init__()
        self.ringToneFilePath = pathToRingTone


    def start(self):
        self.player = pj.AudioMediaPlayer()
        self.play_med = ep.instance.audDevManager().getPlaybackDevMedia()
        self.player.createPlayer(self.ringToneFilePath)
        self.player.startTransmit(self.play_med)


    def dismiss(self):
        try:
            self.player.stopTransmit(self.play_med)
        except:
            pass

