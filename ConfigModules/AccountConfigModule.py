import ConfigModules.AccountConfigConst as UserDefinded

class AccountConfigModule(object):
    '''
    User configuration within the file AccountConfigConst.py
    '''

    def __init__(self):
        self.sipServerAddress = UserDefinded.sipServerAddress
        self.sipServerPort = UserDefinded.sipServerPort
        self.sipName = UserDefinded.sipName
        self.sipSecret = UserDefinded.sipSecret
        self.stun = UserDefinded.stun
        self.stunServer = UserDefinded.stunServer
        self.__account = Account()
        self.implementConfiguration()

    def getAccountSettings(self):
        return self.__account

    def implementConfiguration(self):
        notNullList = ["sipServerAddress", "sipServerPort", "sipName"]
        members  = [attr for attr in dir(self) if not callable(getattr(self,attr)) and not attr.startswith("__") and not attr.startswith("_")]
        for member in members:
            if getattr(self, member):
                setattr(self.__account, member, getattr(self, member))
            else:
                if member in notNullList:
                    raise AttributeError("Server address, server port or user name can't be None!")


class Account(object):
    
    def __init__(self):
        self.sipServerAddress = None
        self.sipServerPort = None
        self.sipName = None
        self.sipSecret = None
        self.stun = False
        self.stunServer = None

    def hasStunSupport(self):
        return self.stun
        
    def getSipAddress(self):
        """
        Provides the SIP address.
        Format: sip:example@exampleServer.com
        @rtype: string
        @return: The SIP address
        """
        sipA = "sip:" + str(self.sipName) + "@" + str(self.sipServerAddress)
        return sipA
        
    def getSipRegURI(self):
        """
        Provides the SIP URI.
        Format: sip:exampleServer.com
        @rtype: string
        @return: The SIP URI
        """
        regUri = "sip:" + str(self.sipServerAddress)
        return regUri
