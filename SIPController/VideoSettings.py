from Modules.ConfigModules import ConfigReaderModule


class VideoSettings(object):
    def __init__(self):
        self.captureDevice = -1
        self.renderDevice = -2
        self.outgoingDefault = False
        self.incomingDefault = False
        self.readSettings()

    def readSettings(self):
        try:
            ConfigReaderModule.readVideoConfig(self)
        except:
            pass
