import pjsua

class CodecList(object):
    
    def __init__(self):
        self.__codecList = []
        
    def __getitem__(self, key):
        return self.__codecList[key]

    def initWithDict(self,  dict):
        param = pjsua.CodecParameter
        param.ptime = 0
        param.vad_enabled = False
        param.plc_enabled = False
        self.addCodec('g722/16000/1',  param)
        
        
    def initWithList(self,  list):
        for codec in list:
            self.__codecList.append(codec)

    def addCodec(self,  codecName,  param):
        codec = pjsua.CodecInfo
        #codec.name
        self.__codecList.append(codec)
        
    def changePriority(self, codecName,  priority):
        pass

    def removeCodec(self,  codecName):
        pass
        
    def changeCodecParam(self, codecName,   codecParam):
        pass
        
    def getNumberOfCodecs(self):
        return len(self.__codecList)
        
    def printList(self):
        for codec in self.__codecList:
            print codec.name
    
    def checkIfCodecInList(self, codecName):
        pass

