import logging

class ControllerCallBacksHolder(object):

    def __init__(self,  connectIncomingCall = None,  incomingCallCanceled = None, onCallEstablished = None,  outgoingCallCanceled = None, connectRegStateChanged = None, callHasVideo = None):
        self.__connectIncomingCall = connectIncomingCall
        self.__incomingCallCanceled = incomingCallCanceled
        self.__onCallEstablished = onCallEstablished
        self.__outgoingCallCanceled = outgoingCallCanceled
        self.__connectRegStateChanged = connectRegStateChanged
        self.__callHasVideo = callHasVideo
        self.logger = logging.getLogger('CallBacksHolder')

    def connectIncomingCall(self):
        if self.__connectIncomingCall:
            self.__connectIncomingCall()
        else:
            self.logger.debug("No 'connectIncomingCall' callback")

    def incomingCallCanceled(self):
        if self.__incomingCallCanceled:
            self.__incomingCallCanceled()
        else:
            self.logger.debug("No 'incomingCallCanceld' callback")

    def onCallEstablised(self):
        if self.__onCallEstablished:
            self.__onCallEstablished()
        else:
            self.logger.debug("No 'onCallEstablished' callback")

    def onOutgoingCallCanceled(self):
        if self.__outgoingCallCanceled:
            self.__outgoingCallCanceled()
        else:
            self.logger.debug("No 'onOutgoingCallCanceled' callback")

    def onRegStateChanged(self, isRegistrated = False, regStatus = None, regReason = None):
        if self.__connectRegStateChanged:
            self.__connectRegStateChanged(isRegistrated, regStatus, regReason)
        else:
            self.logger.debug("No 'onRegStateChanged' callback")

    def onCallHasVideo(self):
        if self.__callHasVideo:
            self.__callHasVideo()
        else:
            self.logger.debug("No 'onCallHasVideo' callback")