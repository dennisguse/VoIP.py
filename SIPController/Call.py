import pjsua2 as pj
import time
import PyQt4.QtCore
import logging, traceback
from SIPController.ControllerCallBacksHolder import ControllerCallBacksHolder
from SIPController.Endpoint import Endpoint as ep

DIALTONE_PATH = './Resources/dialtone.wav'


class Call(pj.Call):

    def __init__(self, account, callId = pj.PJSUA_INVALID_ID, dumpSettings = None, callClear = None, controllerCallBack = None):
        pj.Call.__init__(self, account, callId)
        self.logger = logging.getLogger("CallCallBack")
        self.callId = callId
        #self.callActive = False
        self.setCallBacks(dumpSettings, callClear, controllerCallBack)
        self.userHangup = False
        self.ringing = False
        self.inactive = False
        self.recorderIn = None
        self.recorderOut = None

    def setCallBacks(self, dumpSettings, callClear, controllerCallBack):
        self.callClear = callClear
        self.dumpSettings= dumpSettings
        if controllerCallBack is not None:
            self.callEstablished = controllerCallBack.onCallEstablised
            self.callHasVideo = controllerCallBack.onCallHasVideo
            self.callCanceledBeforeConnect = controllerCallBack.incomingCallCanceled

    def hangup(self):
        self.hangup(200)

    def hangup(self, statuscode):
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!HANGUO!!!!!!!!!!!!!!!!!!!!!!!!")
        call_prm = pj.CallOpParam()
        call_prm.statusCode = statuscode
        super(Call, self).hangup(call_prm)
        self.inactive = True

    def answerCall(self):
        call_prm = pj.CallOpParam()
        call_prm.statusCode = 200
        self.answer(call_prm)
        self.inactive = False

    def answerWithRinging(self):
        call_prm = pj.CallOpParam()
        call_prm.statusCode = 180
        self.answer(call_prm)
        self.inactive = False

    def onCallState(self, prm):
        print("on state")
        #ci = self.getInfo()
        #if (ci.state is pj.PJSIP_INV_STATE_EARLY and self.ringing is False):
        #    self.startRinging()
        #elif (ci.state is not pj.PJSIP_INV_STATE_EARLY and self.ringing is True):
        #    self.stopRinging()
        #if ci.state is pj.PJSIP_INV_STATE_DISCONNECTED:
        #    self.callCanceledBeforeConnect()
        #    self.inactive = True
        #    if self.recorderIn is not None:
        #        ep.instance.audDevManager().getPlaybackDevMedia().stopTransmit(self.recorderIn)
        #        self.recorderIn = None
        #    if self.recorderOut is not None:
        #        ep.instance.audDevManager().getCaptureDevMedia().stopTransmit(self.recorderOut)
        #        self.recorderOut = None

    def onCallMediaState(self, prm):
        print("!!!!!!!ON MEDIA STATE")
        #ci = self.getInfo()
        #for i in range(0, len(ci.media)):
        #    mi = ci.media[i]
        #    if mi.type == pj.PJMEDIA_TYPE_AUDIO and (mi.status == pj.PJSUA_CALL_MEDIA_ACTIVE or mi.status == pj.PJSUA_CALL_MEDIA_REMOTE_HOLD):
        #        if self.dumpSettings.dumpWave is True:
        #            self.recorderOut = pj.AudioMediaRecorder()
        #            self.recorderIn = pj.AudioMediaRecorder()
        #            t = str(time.time())
        #            self.recorderOut.createRecorder("./Recordings/" + str(ci.id) + t + "_outgoing.wav")
        #            self.recorderIn.createRecorder("./Recordings/" + str(ci.id) + t + "_inc.wav")
        #            ep.instance.audDevManager().getCaptureDevMedia().startTransmit(self.recorderOut)
        #            ep.instance.audDevManager().getPlaybackDevMedia().startTransmit(self.recorderIn)
        #        m = self.getMedia(mi.index)
        #        am = pj.AudioMedia.typecastFromMedia(m)
        #        ep.instance.audDevManager().getCaptureDevMedia().startTransmit(am)
        #        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! Connecting ports")
        #        am.startTransmit(ep.instance.audDevManager().getPlaybackDevMedia())

    def connectVideo(self):
        self.callHasVideo()


    def disconnectRecorder(self):
        pass


    def debugMediaState(self):
        pass

    def getCallLevels(self):
        #return self.lib.conf_get_signal_level(self.call_slot)
        pass

    def startRinging(self):
        self.ringing = True
        self.playerRinging = pj.AudioMediaPlayer()
        self.medRinging = ep.instance.audDevManager().getPlaybackDevMedia()
        self.playerRinging.createPlayer(DIALTONE_PATH)
        self.playerRinging.startTransmit(self.medRinging)

    def stopRinging(self):
        self.ringing = False
        self.playerRinging.stopTransmit(self.medRinging)
        self.playerRinging = None
        self.medRinging = None