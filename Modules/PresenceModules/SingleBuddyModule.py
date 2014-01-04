import logging
from Modules.AbstractModule import AbstractModule
from Modules.SignalHandler import SignalHandler
from PyQt4.QtCore import *
from Modules.ConfigModules.ConfigReaderModule import readFirstBuddyURI
from Defines import SIGNALS

class SingleBuddyModule(QObject,AbstractModule):

    def __init__(self):
        super(SingleBuddyModule, self).__init__()
        self.logger = logging.getLogger('SingleBuddyModule')

    def start(self,  optionalParameter = None):
        if optionalParameter:
            self.buddyURI = optionalParamter
        else:
            self.buddyURI = readFirstBuddyURI()
        if self.buddyURI:
            self.logger.info("Starting to track buddy with URI " + self.buddyURI)
            SignalHandler.getInstance().sipController.addBuddy(self.buddyURI, self.onBuddyStateChanged)

    def hasSignalsToRegister(self):
        return True

    def getSignals(self):
        return [[SIGNALS.BUDDY_STATE_CHANGED, None, 'onBuddyStateChanged']]

    def dismiss(self):
        self.logger.info("Stopping to track buddy")

    def onBuddyStateChanged(self, stateText):
        self.logger.info("Buddy module detected buddy state change")
        self.emit(SIGNAL(SIGNALS.BUDDY_STATE_CHANGED), stateText)
