import pjsua as pj
import time
import PyQt4.QtCore
import logging
from SIPController.ControllerCallBacksHolder import ControllerCallBacksHolder

class CallCallBack(pj.CallCallback):

    def __init__(self, dumpSettings, callClear, controllerCallBack,  call=None,  pjLib=None):
        pj.CallCallback.__init__(self, call)
        self.logger = logging.getLogger("CallCallBack")
        self.logger.debug("Creating callcallback for call id: " + call.info().sip_call_id)
        self.lib = pjLib
        self.recorderID = None
        #self.callActive = False
        self.callCanceledBeforeConnect = controllerCallBack.incomingCallCanceled
        self.dumpSettings= dumpSettings
        self.userHangup = False
        self.callClear = callClear
        self.callEstablished = controllerCallBack.onCallEstablised
        self.numberConfSlotsConnected = 0
        self.numberRecorderSlotsConnected = 0
        self.callEst = False
        self.call_slot = None
        self.recorderSlot = None


    def on_state(self):
        self.logger.info("Call is " + self.call.info().state_text + " last code =" + str(self.call.info().last_code) + "(" + self.call.info().last_reason + ")")
        if self.call.info().state == pj.CallState.DISCONNECTED:
            #TODO Disconnect ports only if they were connected (otherwise PJSIP dies.)
            #Should be fixed, but we have to test that!
            self.signalThread = None
            self.callEst = False
            #if self.callActive == True:
            self.disconnectRecorder()
            self.disconnectConfSlots()
            self.logger.debug("Disconnected conf slots!")
            #else:
            #    self.callCanceledBeforeConnect()
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
        else:
            self.debugMediaState()

    def connectConfSlots(self):
        self.logger.info("Connecting conf slots")
        if self.recorderSlot:
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
        if self.dumpSettings.dumpWave == True:
            file_name = time.time()
            try:   
                self.recorderID = self.lib.create_recorder(str(file_name) + '.wav')
                self.recorderSlot = self.lib.recorder_get_slot(self.recorderID)
                self.lib.conf_connect(self.call_slot, self.recorderSlot)
                self.lib.conf_connect(self.recorderSlot, self.call_slot)
                self.logger.debug("Connected recorder slot:" + str(self.recorderSlot))
                self.numberRecorderSlotsConnected = self.numberRecorderSlotsConnected + 1
            except:
                self.logger.warning("Recorder not created!")

    def disconnectConfSlots(self):
        if self.numberConfSlotsConnected > 0:
            self.logger.info("Dis-connecting conf slots")
            self.lib.conf_disconnect(self.call_slot, 0)
            self.lib.conf_disconnect(0, self.call_slot)
            self.call_slot = None
            self.numberConfSlotsConnected = self.numberConfSlotsConnected - 1
        else:
            self.logger.error("Unable to disconnect conf slots, no conf slots connected")

    def disconnectRecorder(self):
        if self.numberRecorderSlotsConnected > 0:
            self.lib.conf_disconnect(self.call_slot, self.recorderSlot)
            self.lib.conf_disconnect(self.recorderSlot, self.call_slot)
            self.lib.recorder_destroy(self.recorderID)
            self.recorderID = None
            self.recorderSlot = None
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