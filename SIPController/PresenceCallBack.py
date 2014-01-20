import pjsua as pj

class PresenceCallBack(pj.BuddyCallback):
    
    def __init__(self, buddy = None,  buddyFunctionPointer = None):
        pj.BuddyCallback.__init__(self, buddy)
        self.__bodyFunctionToCall = buddyFunctionPointer
        
    def on_state(self):
        if self.__bodyFunctionToCall  != None:
            self.__bodyFunctionToCall(self.buddy.info().online_status, self.buddy.info().online_text)