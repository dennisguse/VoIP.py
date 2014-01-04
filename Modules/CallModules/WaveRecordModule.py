import logging
from Modules.AbstractModule import AbstractModule
from Modules.SignalHandler import SignalHandler


class WaveRecordModule(AbstractModule):
    
    def __init__(self):
        super(WaveRecordModule, self).__init__()        
        self.logger = logging.getLogger('WaveRecordModule')
        pass
        
    def start(self,  optionalParameter = None):
        self.recordWave()        
        self.logger.info("Starting to record each call!")
        
    def dismiss(self):
        self.logger.info("Stopping to record calls!")
        
    def recordWave(self):
        SignalHandler.getInstance().sipController.dumpSettings.dumpWave = True
        
    def stopRecordWave(self):
        SignalHandler.getInstance().sipController.dumpSettings.dumpWave = False
