class AudioDeviceModule(object):

    """
    CONFIGURE HERE!
    """
    captureDevId = None
    playbackDevId = None
    """
    END OF CONFIGURATION
    """

    def __init__(self):
        self.__audioDev = AudioDevice()
        self.implementConfiguration()

    def getAudioDeviceSettings(self):
        return self.__audioDev

    def implementConfiguration(self):
        members  = [attr for attr in dir(self) if not callable(getattr(self,attr)) and not attr.startswith("__") and not attr.startswith("_")]
        for member in members:
            if getattr(self, member) != None:
                setattr(self.__audioDev, member, getattr(self, member))

class AudioDevice(object):
    
    def __init__(self):
        self.captureDevId = None
        self.playbackDevId = None

