import ConfigModules.BuddyConfigConst as UserDefinded

class BuddyConfigModule(object):
    '''
    User configuration within the file BuddyConfigConst.py
    '''

    def __init__(self):
        self.__buddys = []
        for buddy in UserDefinded.buddys:
            self.__buddys.append(Buddy(buddy))

    def getBuddys(self):
        return self.__buddys

class Buddy(object):

    def __init__(self, buddyUri):
        self.buddyUri = buddyUri
        self.parseNumber()

    def parseNumber(self):
        self.number = (self.buddyUri.split(":")[1]).split("@")[0]
