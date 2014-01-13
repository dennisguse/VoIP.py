import ConfigModules.NetworkSettingsConst as UserDefined

class NetworkSettingsModule(object):
    '''
    User configuration within the file NetworkSettingsConst.py
    '''

    def __init__(self):
        self.tcp = UserDefined.tcp
        self.networkPort = UserDefined.networkPort
        self.ipv6 = UserDefined.ipv6
        self.__networkSettings = NetworkSettings()
        self.implementConfiguration()

    def getNetworkSettings(self):
        return self.__networkSettings

    def implementConfiguration(self):
        members  = [attr for attr in dir(self) if not callable(getattr(self,attr)) and not attr.startswith("__") and not attr.startswith("_")]
        for member in members:
            if getattr(self, member):
                setattr(self.__networkSettings, member, getattr(self, member))


class NetworkSettings(object):

    def __init__(self,  networkPort = None,  tcp = False,  ipv6 = False):
        self.tcp = False
        self.networkPort = 5062
        self.ipv6 = False

    def isDefault(self):
        if self.networkPort == None and self.tcp == False and self.ipv6 == False:
            return True
        else:
            return False