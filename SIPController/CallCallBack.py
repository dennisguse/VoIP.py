import pjsua as pj
import time
import PyQt4.QtCore
import logging, traceback
from SIPController.ControllerCallBacksHolder import ControllerCallBacksHolder

class CallCallBack(pj.CallCallback):

    def __init__(self, dumpSettings, callClear, controllerCallBack,  call=None,  pjLib=None):
        pj.CallCallback.__init__(self, call)
        self.logger = logging.getLogger("CallCallBack")
        self.callId = str(call.info().sip_call_id)
        self.logger.debug("Creating callcallback for call id: " + self.callId)
        self.lib = pjLib
        #self.callActive = False
        self.callCanceledBeforeConnect = controllerCallBack.incomingCallCanceled
        self.dumpSettings= dumpSettings
        self.userHangup = False
        self.callClear = callClear
        self.callEstablished = controllerCallBack.onCallEstablised
        self.callHasVideo = controllerCallBack.onCallHasVideo
        self.numberConfSlotsConnected = 0
        self.numberRecorderSlotsConnected = 0
        self.callEst = False
        self.call_slot = None
        self.recorderSlotInc = None
        self.recorderIDInc = None
        self.recorderSlotOut = None
        self.recorderIDOut = None


    def on_state(self):
        self.logger.info("Call is " + self.call.info().state_text + " last code =" + str(self.call.info().last_code) + "(" + self.call.info().last_reason + ")")
        if self.call.info().state == pj.CallState.DISCONNECTED:
            #TODO Disconnect ports only if they were connected (otherwise PJSIP dies.)
            #Should be fixed, but we have to test that!
            self.signalThread = None
            self.callEst = False
            self.disconnectRecorder()
            self.disconnectConfSlots()
            self.logger.debug("Disconnected conf slots!")
            if self.userHangup == False:
                self.callCanceledBeforeConnect()
            if self.dumpSettings.dumpCallStats:
                self.writeCallStats()
            self.callClear()
            self.logger.debug("Call is disconnected, active conf slots:" + str(self.numberConfSlotsConnected) + " recorder:" + str(self.numberRecorderSlotsConnected))
        elif self.call.info().state == pj.CallState.CONFIRMED:
            self.logger.info("Call established")
            self.callEstablished()
            self.callEst = True

    def on_media_state(self):
        if self.call.info().media_state == pj.MediaState.ACTIVE:
            self.logger.info("Media state changed to active")
            self.connectConfSlots()
            self.connectVideo()
        else:
            self.debugMediaState()

    def connectVideo(self):
        self.callHasVideo()

    def connectConfSlots(self):
        self.logger.info("Connecting conf slots")
        if self.recorderSlotInc:
            self.logger.debug("Disconnected previous recorder")
            self.disconnectRecorder()
        if self.call_slot:
            self.logger.debug("Disconnected previous call slot")
            self.disconnectConfSlots()
        self.call_slot = self.call.info().conf_slot
        self.lib.conf_connect(0, self.call_slot)
        self.lib.conf_connect(self.call_slot, 0)
        self.logger.debug("Connected call slot:" + str(self.call_slot))
        self.numberConfSlotsConnected = self.numberConfSlotsConnected + 1
        self.logger.debug("RECORDER " + str(self.dumpSettings.dumpWave) + " " + str(self.callEst))
        if self.dumpSettings.dumpWave == True:# and self.callEst == True: 
            t = str(time.time())
            #Use a a external module for recordings (the callback handler should emit a specific signal here)
            try:
                self.recorderIDInc = self.lib.create_recorder("./Recordings/" + self.callId + t + '_incoming.wav')
                self.recorderSlotInc = self.lib.recorder_get_slot(self.recorderIDInc)
                self.lib.conf_connect(self.call_slot, self.recorderSlotInc)
                self.recorderIDOut = self.lib.create_recorder("./Recordings/" + self.callId + t + '_outgoing.wav')
                self.recorderSlotOut = self.lib.recorder_get_slot(self.recorderIDOut)
                self.lib.conf_connect(0, self.recorderSlotOut)
                self.logger.debug("Connected recorder slot:" + str(self.recorderSlotInc))
                self.logger.debug("Connected recorder slot:" + str(self.recorderSlotOut))
                self.numberRecorderSlotsConnected = self.numberRecorderSlotsConnected + 1
            except Exception, e:
                self.logger.warning("Recorder not created!")
                print traceback.format_exc()

    def disconnectConfSlots(self):
        if self.numberConfSlotsConnected > 0:
            try:
                self.logger.info("Dis-connecting conf slots")
                self.lib.conf_disconnect(self.call_slot, 0)
                self.lib.conf_disconnect(0, self.call_slot)
                self.call_slot = None
                self.numberConfSlotsConnected = self.numberConfSlotsConnected - 1
            except:
                pass
        else:
            self.logger.error("Unable to disconnect conf slots, no conf slots connected")

    def disconnectRecorder(self):
        if self.numberRecorderSlotsConnected > 0:
            self.lib.conf_disconnect(self.call_slot, self.recorderSlotInc)
            self.lib.conf_disconnect(0, self.recorderSlotOut)
            self.lib.recorder_destroy(self.recorderIDInc)
            self.lib.recorder_destroy(self.recorderIDOut)
            self.recorderIDInc = None
            self.recorderSlotInc = None
            self.recorderIDOut = None
            self.recorderSlotOut = None
            self.numberRecorderSlotsConnected = self.numberRecorderSlotsConnected - 1


    def debugMediaState(self):
        if self.call.info().media_state == pj.MediaState.ERROR:
             self.logger.error("Media state ERROR")
        elif self.call.info().media_state == pj.MediaState.LOCAL_HOLD:
             self.logger.debug("Media state LOCAL_HOLD")
        elif self.call.info().media_state == pj.MediaState.NULL:
             self.logger.debug("Media state NULL")
        elif self.call.info().media_state == pj.MediaState.REMOTE_HOLD:
             self.logger.debug("Media state REMOTE_HOLD")
        else:
             self.logger.warning("Media state is unknown code: " + str(self.call.info().media_state))

    def getCallLevels(self):
        return self.lib.conf_get_signal_level(self.call_slot)
