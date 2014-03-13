import pjsua2 as pj
import threading, random
from SIPController.Call import Call

class Account(pj.Account):
    
    def __init__(self, on_incoming_call, reg_state_callback):
        pj.Account.__init__(self)
        self.randId = random.randint(1, 9999)
        self.cfg =  pj.AccountConfig()
        self.connectRegStateCallback = reg_state_callback
        self.connectIncomingCallback = on_incoming_call
        self.currentIncomingCall = None
        self.currentCallCallback = None

    def onIncomingCall(self, callprm):
        if self.connectIncomingCallback != None:
            self.currentCall = Call(self, callprm.callId)
            self.connectIncomingCallback(self.currentCall)
        return

    def onRegState(self, prm):
        if self.connectRegStateCallback != None:
            self.connectRegStateCallback()

        
