import pjsua as pj
import time
import PyQt4.QtCore
import logging
from SIPController.ControllerCallBacksHolder import ControllerCallBacksHolder

class CallCallBack(pj.CallCallback):

    def __init__(self, dumpSettings, callClear, controllerCallBack,  call=None,  pjLib=None):
        pj.CallCallback.__init__(self, call)
        self.logger = logging.getLogger("CallCallBack")
        self.lib = pjLib
        self.recorderID = None
        self.callActive = False
        self.callCanceledBeforeConnect = controllerCallBack.incomingCallCanceled
        self.dumpSettings= dumpSettings
        self.userHangup = False
        self.callClear = callClear
        self.callEstablished = controllerCallBack.onCallEstablised
        self.numberConfSlotsConnected = 0
        self.numberRecorderSlotsConnected = 0


    def on_state(self):
        self.logger.info("Call is " + self.call.info().state_text + " last code =" + str(self.call.info().last_code) + "(" + self.call.info().last_reason + ")")
        if self.call.info().state == pj.CallState.DISCONNECTED:
            #TODO Disconnect ports only if they were connected (otherwise PJSIP dies.)
            #Should be fixed, but we have to test that!
            self.signalThread = None
            if self.callActive == True:
                self.disconnectConfSlots()
                self.logger.debug("Disconnected conf slots!")
            else:
                self.callCanceledBeforeConnect()
            if self.userHangup == False:
                self.callCanceledBeforeConnect()
            if self.dumpSettings.dumpCallStats:
                self.writeCallStats()
            self.callClear()
            self.disconnectRecorder()
        elif self.call.info().state == pj.CallState.CONFIRMED:
            self.logger.info("Call established")
            self.callEstablished()

    def on_media_state(self):
        if self.call.info().media_state == pj.MediaState.ACTIVE:
            if self.callActive == False:
                self.callActive = True
                self.connectConfSlots()
            else:
                self.logger.debug("Re-connected conf slots!")
                try:
                    self.disconnectConfSlots()
                except:
                    #TODO double check here
                    print("No conf slots to disconnect")
                self.connectConfSlots()
        else:
            self.debugMediaState()

    def connectConfSlots(self):
        self.logger.info("Connecting conf slots")
        self.call_slot = self.call.info().conf_slot
        self.lib.conf_connect(0, self.call_slot)
        self.lib.conf_connect(self.call_slot, 0)
        self.numberConfSlotsConnected = self.numberConfSlotsConnected + 1
        if self.dumpSettings.dumpWave == True:
            file_name = time.time()
            try:   
                self.recorderID = self.lib.create_recorder(str(file_name) + '.wav')
                recorderSlot = self.lib.recorder_get_slot(self.recorderID)
                self.lib.conf_connect(self.call_slot, recorderSlot)
                self.lib.conf_connect(recorderSlot, self.call_slot)
                self.numberRecorderSlotsConnected = self.numberRecorderSlotsConnected + 1
            except:
                print("Recorder not created!")

    def disconnectConfSlots(self):
        if self.numberConfSlotsConnected > 0:
            self.logger.info("Dis-connecting conf slots")
            self.lib.conf_disconnect(self.call_slot, 0)
            self.lib.conf_disconnect(0, self.call_slot)
            self.numberConfSlotsConnected = self.numberConfSlotsConnected - 1
        else:
            self.logger.error("Unable to disconnect conf slots, no conf slots connected")

    def disconnectRecorder(self):
        #TODO Do it via callback?
        if self.recorderID:
            recorderSlot = self.lib.recorder_get_slot(self.recorderID)
            if self.numberRecorderSlotsConnected > 0:
                self.lib.conf_disconnect(self.call_slot, recorderSlot)
                self.lib.conf_disconnect(recorderSlot, self.call_slot)
                self.recorderID = None
            else:
                self.logger.error("Unable to disconnect recorder slots, no recorder slots connected")

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


    def writeCallStats(self):
        #StatisticWriter.writeStats(self.call.dump_status())
        pass

    def getCallLevels(self):
        return self.lib.conf_get_signal_level(self.call_slot)

    def __del__(self):
        while self.numberRecorderSlotsConnected > 0:
            self.disconnectRecorder()
        while self.numberConfSlotsConnected > 0:
            sefl.disconnectConfSlots()
