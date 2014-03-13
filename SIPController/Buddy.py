import pjsua2 as pj

class Buddy(pj.Buddy):

    def __init__(self, onStateCallback):
        pj.Buddy.__init__(self)
        self.onStateCallback = onStateCallback

    def onBuddyState(self):
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! buddy state changed!")
        info = self.getInfo()
        self.onStateCallback(info.presStatus.status, info.presStatus.statusText)