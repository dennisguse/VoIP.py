import logging, sys, signal, traceback
from PyQt4.QtCore import QObject
from PyQt4.QtCore import SIGNAL
from PyQt4.QtCore import QThread
from SIPController.SipController import SipController
from Defines import SIGNALS
from SIPController.ControllerCallBacksHolder import ControllerCallBacksHolder

def singleton(cls):
        return cls()

@singleton
class SignalHandler(QObject):
    
    def __init__(self):
        super(QObject, self).__init__()
    
    def init(self, registerNewModule ,  activateModule ,  dismissModule):
        self.logger = logging.getLogger('SignalHandler')
        self.logger.debug("Init")
        self.registerNewModule = registerNewModule
        self.activateModule = activateModule
        self.dismissModule = dismissModule
        self.signalSource = None
        self.controllerCallBacks = ControllerCallBacksHolder(self.onIncomingCall, self.onIncomingCallCanceled, self.onCallEstablished, self.onOutgoingCallCanceled, self.onRegStateChanged, self.onCallHasVideo)
        self.sipController = SipController(self.controllerCallBacks)
        self.establishedCall = False

    def getInstance(self):
        return self

    def setIncomingSignalSource(self, signalSource):
        self.signalSource = signalSource
        self.registerStandardSignals()
        self.signalSource.registerNewModules()

    def registerStandardSignals(self):
        self.logger.debug("Connecting signals")
        self.connect(self.signalSource, SIGNAL(SIGNALS.MODULE_LOAD), self.registerNewModule)
        self.connect(self.signalSource, SIGNAL(SIGNALS.MODULE_ACTIVATE), self.activateModule)
        self.connect(self.signalSource, SIGNAL(SIGNALS.MODULE_DISMISS), self.dismissModule)
        self.connect(self.signalSource, SIGNAL(SIGNALS.CLOSE), self.onCloseLibSignal)
        self.connect(self.signalSource, SIGNAL(SIGNALS.CALL_NUMBER), self.onCallSignal)
        self.connect(self.signalSource, SIGNAL(SIGNALS.CALL_CONNECT), self.onConnectCallSignal)
        self.connect(self.signalSource, SIGNAL(SIGNALS.CALL_HANGUP), self.onHangupCallSignal)
        self.connect(self.signalSource, SIGNAL(SIGNALS.REGISTER_REQUEST_INITIAL_STATE), self.sipController.onRegStateChanged)
        self.connect(self.signalSource, SIGNAL(SIGNALS.CALL_SIGNAL_LEVEL_REQUEST), self.onSignalLevelChangeRequest)
        self.connect(self.signalSource, SIGNAL(SIGNALS.OWN_ONLINE_STATE_CHANGED), self.onOwnOnlineStatusChange)
        self.connect(self.signalSource, SIGNAL(SIGNALS.REGISTER), self.sipController.registerClient)

    def registerNewSignal(self, signalSource, signalName, signalCallBack = None, internalMethodToCall = None):
        self.logger.debug("Register new signal: " + str(signalSource) + ":" + signalName)
        if signalCallBack:
            print("Register signal:" + signalName + str(signalSource))
            self.connect(signalSource,  SIGNAL(signalName),  signalCallBack)
        elif internalMethodToCall:
            self.connect(signalSource,  SIGNAL(signalName),  getattr(self, internalMethodToCall))

    ####################################
    #     Incoming signal section      #
    ####################################

    def onCloseLibSignal(self):
        try:
            self.sipController.freeLib()
        except:
            ex = sys.exc_info()[0]
            self.logger.error("Unable to free lib: " + traceback.format_exc())
        return

    def onCallSignal(self, numberToCall):
        self.logger.info("Calling number: " + numberToCall)
        try:
            self.sipController.callNumber(numberToCall)
        except:
            ex = sys.exc_info()[0]
            self.logger.error("Unable to call " + numberToCall + ": " + str(ex))

    def onConnectCallSignal(self):
        self.logger.info("Accept incoming call")
        try:
            self.sipController.currentCall.answer()
            self.logger.debug("Accepting call:" + self.sipController.currentCall.info().remote_contact)
            self.logger.debug("With call id:" + self.sipController.currentCall.info().sip_call_id)
            self.logger.debug("With state:" + self.sipController.currentCall.info().state_text)
            self.logger.debug("Valid:" + self.sipController.currentCall.is_valid())
            self.logger.debug("Call excepted by SipController")
        except:
            ex = sys.exc_info()[0]
            self.logger.error("Unable to connect current call")

    def onHangupCallSignal(self):
        self.logger.info("Hangup call")
        try:
            self.sipController.hangup()
        except:
            ex = sys.exc_info()[0]
            self.logger.error("Unable to hangup call")

    def onOwnOnlineStatusChange(self, isOnline=False):
        if isOnline:
            self.logger.info("Setting own online status to online")
        else:
            self.logger.info("Settting own online status to offline")
        self.sipController.setPresenceStatus(isOnline)

    ####################################
    #     Outgoing signal section      #
    ####################################

    def onIncomingCall(self):
        self.logger.info("Incoming call")
        self.emit(SIGNAL(SIGNALS.CALL_INCOMING),  self.sipController.getCurrentCallingNumber())

    def onIncomingCallCanceled(self):
        self.logger.info("Incoming call hangup before anwsering")
        self.emit(SIGNAL(SIGNALS.CALL_INCOMING_CANCELED))

    def onOutgoingCallCanceled(self):
        self.logger.info("Outgoing call canceled")
        self.emit(SIGNAL(SIGNALS.CALL_OUTGOING_CANCELED))

    def onRegStateChanged(self, isActive, reg_code, reg_reason):
        self.logger.info("Registation state changed to: " + str(bool(isActive)))
        self.emit(SIGNAL(SIGNALS.REGISTER_STATE_CHANGE),  isActive, reg_code, reg_reason)

    def onBuddyStateChanged(self, stateText, buddyURI = None):
        if buddyURI:
            self.logger.info("Buddy " + buddyURI + " state changed: " + str(stateText))
            self.emit(SIGNAL(SIGNALS.BUDDY_STATE_CHANGED), stateText, buddyURI)
        else:
            self.logger.info("Buddy state changed: " + str(stateText))
            self.emit(SIGNAL(SIGNALS.BUDDY_STATE_CHANGED), stateText)

    def onCallEstablished(self):
        self.logger.info("Call established")
        self.emit(SIGNAL(SIGNALS.CALL_ESTABLISHED))


    def onSignalLevelChangeRequest(self):
        if self.sipController.currentCallCallback:
            self.emit(SIGNAL(SIGNALS.CALL_SIGNAL_LEVEL_CHANGE), self.sipController.currentCallCallback.getCallLevels())

    def onCallHasVideo(self):
        self.logger.debug("Video-stream count: " + str(self.sipController.currentCall.info().vid_cnt)) #TODO CHECK WHY 0
        self.emit(SIGNAL(SIGNALS.CALL_SHOW_VIDEO), self.sipController.getCurrentCallVideoStream())
        self.logger.debug("Call has video with win id: " + str(self.sipController.getCurrentCallVideoStream()))