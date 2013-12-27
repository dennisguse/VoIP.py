import logging
from PyQt4.QtCore import QObject
from PyQt4.QtCore import SIGNAL
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
        self.registerNewModule = registerNewModule
        self.activateModule = activateModule
        self.dismissModule = dismissModule
        self.signalSource = None
        self.controllerCallBacks = ControllerCallBacksHolder(self.onIncomingCall, self.onIncomingCallCanceled, self.onCallEstablished, self.onOutgoingCallCanceled, self.onRegStateChanged)
        self.sipHandler = SipController(self.controllerCallBacks)
        self.establishedCall = False

    def getInstance(self):
        return self
    
    def setIncomingSignalSource(self, signalSource):
        self.signalSource = signalSource        
        self.registerStandardSignals()
        self.signalSource.registerNewModules()

    def registerStandardSignals(self):
        self.connect(self.signalSource, SIGNAL(SIGNALS.MODULE_LOAD), self.registerNewModule)
        self.connect(self.signalSource, SIGNAL(SIGNALS.MODULE_ACTIVATE), self.activateModule)
        self.connect(self.signalSource, SIGNAL(SIGNALS.MODULE_DISMISS), self.dismissModule)
        self.connect(self.signalSource, SIGNAL(SIGNALS.CLOSE), self.onCloseLibSignal)
        self.connect(self.signalSource, SIGNAL(SIGNALS.CALL_NUMBER), self.onCallSignal)
        self.connect(self.signalSource, SIGNAL(SIGNALS.CALL_CONNECT), self.onConnectCallSignal)
        self.connect(self.signalSource, SIGNAL(SIGNALS.CALL_HANGUP), self.onHangupCallSignal)
        self.connect(self.signalSource, SIGNAL(SIGNALS.REGISTER_REQUEST_INITIAL_STATE), self.sipHandler.onRegStateChanged)
        self.connect(self.signalSource, SIGNAL(SIGNALS.CALL_SIGNAL_LEVEL_REQUEST), self.onSignalLevelChangeRequest)

    def registerNewSignal(self, signalSource, signalName, signalCallBack = None, internalMethodToCall = None):
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
            self.sipHandler.freeLib()
        except:
            self.logger.debug("Unable to free lib")
        return

    def onCallSignal(self,  numberToCall):
        self.logger.info("Calling number: " + numberToCall)
        try:
            self.sipHandler.callNumber(numberToCall)
        except:
            self.logger.error("Unable to call " + numberToCall)
        
    def onConnectCallSignal(self):
        try:
            self.sipHandler.currentCall.answer()
        except:
            self.logger.error("Unable to connect current call")
    
    def onHangupCallSignal(self):
        try:
            self.sipHandler.hangup()
        except:
            self.logger.error("Unable to hangup call")
    
    ####################################
    #     Outgoing signal section      #
    ####################################
    
    def onIncomingCall(self):
        self.logger.info("Incoming call")
        self.emit(SIGNAL(SIGNALS.CALL_INCOMING),  self.sipHandler.getCurrentCallingNumber())
        
    def onIncomingCallCanceled(self):
        self.logger.info("Incoming call canceled")
        self.emit(SIGNAL(SIGNALS.CALL_INCOMING_CANCELED))
        
    def onOutgoingCallCanceled(self):
        self.logger.info("Outgoing call canceled")
        self.emit(SIGNAL(SIGNALS.CALL_OUTGOING_CANCELED))
        
    def onRegStateChanged(self,  isActive,  reg_code,  reg_reason):        
        self.logger.info("Registation state changed to: " + str(bool(isActive)))
        self.emit(SIGNAL(SIGNALS.REGISTER_STATE_CHANGE),  isActive, reg_code, reg_reason)

    def onBuddyStateChanged(self, stateText, buddyURI = None):
        if buddyURI:
            self.logger.info("Buddy" + buddyURI + " state changed: " + stateText)
            self.emit(SIGNAL(SIGNALS.BUDDY_STATE_CHANGED), stateText, buddyURI)
        else:
            self.logger.info("Buddy state changed: " + stateText)
            self.emit(SIGNAL(SIGNALS.BUDDY_STATE_CHANGED), stateText)

    def onCallEstablished(self):
        self.emit(SIGNAL(SIGNALS.CALL_ESTABLISHED))
        if self.sipHandler.currentCall.info().vid_cnt != 0:
            print("SIGNAL HANDLER CALL EST")
            self.emit(SIGNAL(SIGNALS.CALL_SHOW_VIDEO), self.sipHandler.getCurrentCallVideoStream())


    def onSignalLevelChangeRequest(self):
        if self.sipHandler.currentCallCallback:
            self.emit(SIGNAL(SIGNALS.CALL_SIGNAL_LEVEL_CHANGE), self.sipHandler.currentCallCallback.getCallLevels())

