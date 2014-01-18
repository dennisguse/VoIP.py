import pjsua as pj
import threading

class AccountCallBack(pj.AccountCallback):
    
    def __init__(self, on_incoming_call, reg_state_callback, pj_account):
        pj.AccountCallback.__init__(self, pj_account)
        self.connectRegStateCallback = reg_state_callback
        self.connectIncomingCallback = on_incoming_call
        self.currentIncomingCall = None
        self.currentCallCallback = None     
        return
    
    def on_incoming_call(self, call):
        if self.connectIncomingCallback != None:
            self.currentIncomingCall = call
            self.connectIncomingCallback(call)
        return
    
    def on_reg_state(self):
        if self.connectRegStateCallback != None:
            self.connectRegStateCallback()

    def wait(self):
        self.sem = threading.Semaphore(0)
        self.sem.acquire()
        return
        
    def hangup(self, code = 200):
        if self.currentCallCallback:
            self.currentCallCallback.userHangup = True
            self.currentCallCallback = None
        self.currentIncomingCall.hangup(code)
        self.currentIncomingCall = None
        
