import logging

class AbstractUIModule():
    
    def __init__(self):
        pass
        
    def registerNewSignals(self):
        logging.info("UI Modules doesn't require to register new signals")
        
    def registerNewModules(self):
        logging.info("UI Modules doesn't require to register new modules")

    def onIncomingCall(self,  incomingCallerNumber):
        logging.info("Program can not handle incoming calls!")    
    
    def onIncomingCallCanceled(self):
        logging.info("Program can not handle canceled incoming calls!")
        
    def onOutgoingCallCanceled(self):
        logging.info("Program can not handle canceled outgoing calls!")
        
    def onRegStateSignal(self,  isActive):
        logging.info("Program is not capable of registration events!")
    
    def closeEvent(self, event):
        raise NotImplementedError

    def showWindow(self):
        raise NotImplementedError
