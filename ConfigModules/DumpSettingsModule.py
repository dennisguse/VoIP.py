import ConfigModules.DumpSettingsConst as UserDefined

class DumpSettingsModule(object):
    '''
    User configuration within the file DumpSettingsConst.py
    '''

    def __init__(self):
        self.dumpWave = UserDefined.dumpWave
        self.dumpCallStats = UserDefined.dumpCallStats
        self.dumpLastActiveSettings = UserDefined.dumpLastActiveSettings
        self.pjLogLevel = UserDefined.pjLogLevel
        self.__dumpSettings = DumpSettings()
        self.implementConfiguration()

    def getDumpSettings(self):
        return self.__dumpSettings

    def implementConfiguration(self):
        members  = [attr for attr in dir(self) if not callable(getattr(self,attr)) and not attr.startswith("__") and not attr.startswith("_")]
        for member in members:
            if getattr(self, member):
                setattr(self.__dumpSettings, member, getattr(self, member))


class DumpSettings(object):

    def __init__(self):
        self.dumpWave = False
        self.dumpCallStats = False
        self.dumpLastActiveSettings = False
        self.pjLogLevel = 5
