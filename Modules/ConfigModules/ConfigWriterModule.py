import pjsua
import ConfigParser
from SIPController import NetworkSettings
from SIPController import CodecList
from TelSimpleModules import BuddyList
from TelSimpleModules import DumpSettings


"""
DEPRECATED
"""


class SipConfigParser(object):
    
    def __init__(self,  filePath = 'Settings.conf'):
        self.__filePath = filePath
        if self.__filePath == None:
            self.__filePath ='Settings.conf'
        
    def readMediaConfig(self):
        mediaConf = pjsua.MediaConfig()
        try:
            config = ConfigParser.ConfigParser()
            config.read(self.__filePath)
            dict = self.configSectionMap("MediaConfig",  config)
            mediaConf.channel_count = dict['channelcount']
            mediaConf.snd_clock_rate = dict['sndclockrate']
            mediaConf.clock_rate = dict['clockrate']
            mediaConf.ptime = dict['ptime']
            mediaConf.ilbc_mode = dict['ilbcmode']
            mediaConf.turn_conn_type = dict['turnconntype']
            mediaConf.turn_cred = dict['turncred']
            mediaConf.max_media_ports = dict['maxmediaports']
            mediaConf.turn_server = dict['turnserver']
            mediaConf.tx_drop_pct = dict['txdroppct']
            mediaConf.jb_min = dict['jbmin']
            mediaConf.jb_max = dict['jbmax']
            mediaConf.rx_drop_pct = dict['rxdroppct']
            mediaConf.enable_turn = dict['enableturn']
            mediaConf.ec_tail_len = dict['ectaillen']
            mediaConf.audio_frame_ptime = dict['audioframeptime']
            mediaConf.enable_ice = dict['enableice']
            mediaConf.no_vad = dict['novad']
            mediaConf.quality = dict['quality']
            mediaConf.ec_options = dict['ecoptions']
            mediaConf.snd_auto_close_time = dict['sndautoclosetime']
        except:
            pass
        return mediaConf

    def writeMediaConfig(self,  mediaConf):
        self.deleteSection('MediaConfig')
        cfgFile = open(self.__filePath, 'a')
        config = ConfigParser.ConfigParser()
        config.add_section('MediaConfig')
        config.set('MediaConfig', 'ClockRate',  mediaConf.clock_rate)        
        config.set('MediaConfig', 'SNDClockRate',  mediaConf.snd_clock_rate)
        config.set('MediaConfig', 'SndAutoCloseTime',  mediaConf.snd_auto_close_time)
        config.set('MediaConfig', 'ChannelCount',  mediaConf.channel_count)
        config.set('MediaConfig', 'AudioFramePTime',  mediaConf.audio_frame_ptime)
        config.set('MediaConfig', 'MaxMediaPorts',  mediaConf.max_media_ports)
        config.set('MediaConfig', 'Quality',  mediaConf.quality)
        config.set('MediaConfig', 'PTime',  mediaConf.ptime)
        config.set('MediaConfig', 'NoVAD',  mediaConf.no_vad)
        config.set('MediaConfig', 'ILBCMode',  mediaConf.ilbc_mode)
        config.set('MediaConfig', 'TxDropPct',  mediaConf.tx_drop_pct)
        config.set('MediaConfig', 'RxDropPct',  mediaConf.rx_drop_pct)
        config.set('MediaConfig', 'EcOptions',  mediaConf.ec_options)
        config.set('MediaConfig', 'EcTailLen',  mediaConf.ec_tail_len)
        config.set('MediaConfig', 'JbMin',  mediaConf.jb_min)
        config.set('MediaConfig', 'JbMax',  mediaConf.jb_max)
        config.set('MediaConfig', 'EnableIce',  mediaConf.enable_ice)
        config.set('MediaConfig', 'EnableTurn',  mediaConf.enable_turn)
        config.set('MediaConfig', 'TurnServer',  mediaConf.turn_server)
        config.set('MediaConfig', 'TurnConnType',  mediaConf.turn_conn_type)
        config.set('MediaConfig', 'TurnCred',  mediaConf.turn_cred)
        config.write(cfgFile)
        cfgFile.close()
        
    def readBuddyListDict(self):
        config = ConfigParser.ConfigParser()
        config.read(self.__filePath)
        dict = self.configSectionMap("BuddyConfig",  config)
        return dict
        
    def readBuddyList(self):
        buddy = BuddyList.BuddyList()
        return buddy
        
    
    def writeBuddyList(self,  buddyList):
        self.deleteSection('BuddyConfig')
        cfgFile = open(self.__filePath, 'a')
        config = ConfigParser.ConfigParser()
        config.add_section('BuddyConfig')
        for buddy in buddyList:
            config.set('BuddyConfig',  str(buddy.buddyName), str(buddy))
        config.write(cfgFile)
        cfgFile.close()
    
    def readCodecList(self):
        try: 
            config = ConfigParser.ConfigParser()
            config.read(self.__filePath)
            dict = self.configSectionMap("CodecSettings",  config)
            cl = CodecList.CodecList()
            cl.initWithDict(dict)
        except:
            cl = CodecList.CodecList()
        return cl
        
    def writeCodecList(self, codecList):
        self.deleteSection('CodecSettings')
        cfgFile = open(self.__filePath, 'a')
        config = ConfigParser.ConfigParser()
        config.add_section('CodecSettings')
        for i in range(0,  codecList.getNumberOfCodecs()):
            config.set('CodecSettings',  str(codecList[i].name) + ':priority',  codecList[i].priority)
            config.set('CodecSettings',  str(codecList[i].name) + ':clock_rate',  codecList[i].clock_rate)
            config.set('CodecSettings',  str(codecList[i].name) + ':channel_count',  codecList[i].channel_count)
            config.set('CodecSettings',  str(codecList[i].name) + ':avg_bps',  codecList[i].avg_bps)
            config.set('CodecSettings',  str(codecList[i].name) + ':frm_ptime',  codecList[i].frm_ptime)
            config.set('CodecSettings',  str(codecList[i].name) + ':ptime',  codecList[i].ptime)
            config.set('CodecSettings',  str(codecList[i].name) + ':pt',  codecList[i].pt)
            config.set('CodecSettings',  str(codecList[i].name) + ':vad_enabled',  codecList[i].vad_enabled)
            config.set('CodecSettings',  str(codecList[i].name) + ':plc_enabled',  codecList[i].plc_enabled)
        config.write(cfgFile)
        cfgFile.close()
    
    def readNetworkSettings(self):
        try: 
            config = ConfigParser.ConfigParser()
            config.read(self.__filePath)
            dict = self.configSectionMap("NetworkSettings",  config)
            ns = NetworkSettings.NetworkSettings()
            ns.initWithDict(dict)
        except:
            ns = NetworkSettings.NetworkSettings()
        return ns

    def writeNetworkSettings(self,  networkSettings):
        self.deleteSection('NetworkSettings')
        cfgFile = open(self.__filePath, 'a')
        config = ConfigParser.ConfigParser()
        config.add_section('NetworkSettings')
        if networkSettings.networkPort != None:
            config.set('NetworkSettings', 'NetworkPort',  networkSettings.networkPort)        
        config.set('NetworkSettings', 'TCP',  networkSettings.tcp)        
        config.set('NetworkSettings',  'IPV6',  networkSettings.ipv6)
        config.write(cfgFile)
        cfgFile.close()
        
    def writeRingtoneSettings(self,  ringtonePath = None):
        self.deleteSection('RingtoneConfig')
        cfgFile = open(self.__filePath, 'a')
        config = ConfigParser.ConfigParser()
        config.add_section('RingtoneConfig')
        if ringtonePath == None:
            config.set('RingtoneConfig', 'Ringtone',  'None')        
        else:
            config.set('RingtoneConfig', 'Ringtone',  ringtonePath)        
        config.write(cfgFile)
        cfgFile.close()

    def readRingtoneSettings(self):
        try: 
            config = ConfigParser.ConfigParser()
            config.read(self.__filePath)
            dict = self.configSectionMap("RingtoneConfig",  config)
            ringtone = dict['ringtone']
        except:
            ringtone = None
        return ringtone
    
    def readSoundDeviceSettings(self):
        settings = None
        try:
            config = ConfigParser.ConfigParser()
            config.read(self.__filePath)
            dict = self.configSectionMap("SoundDeviceSettings",  config)
            settings.dumpWave = int(dict['captureid'])
            settings.dumpCallStats = int(dict['playbackid'])
        except:
            pass
        return settings

    def writeSoundDeviceSettings(self,  captureID,  playbackID):
        self.deleteSection('SoundDeviceSettings')
        cfgFile = open(self.__filePath, 'a')
        config = ConfigParser.ConfigParser()
        config.add_section('SoundDeviceSettings')
        config.set('SoundDeviceSettings', 'captureid',  captureID)        
        config.set('SoundDeviceSettings', 'playbackid',  playbackID)
        config.write(cfgFile)
        cfgFile.close()

        
    def readDumpSettings(self):
        settings = DumpSettings.DumpSettings()
        try:
            config = ConfigParser.ConfigParser()
            config.read(self.__filePath)
            dict = self.configSectionMap("DumpSettings",  config)
            settings.dumpWave = self.toBool(dict['wave'])
            settings.dumpCallStats = self.toBool(dict['callstats'])
            settings.dumpLastActiveSettings = self.toBool(dict['lastactivesettings'])
            settings.pjLogLevel = int(dict['pjloglevel'])
        except:
            pass
        return settings

    def writeDumpSetings(self,  dumpSettings):
        self.deleteSection('DumpSettings')
        cfgFile = open(self.__filePath, 'a')
        config = ConfigParser.ConfigParser()
        config.add_section('DumpSettings')
        config.set('DumpSettings', 'wave',  dumpSettings.dumpWave)        
        config.set('DumpSettings', 'callstats',  dumpSettings.dumpCallStats)
        config.set('DumpSettings', 'lastactivesettings',  dumpSettings.dumpLastActiveSettings)
        config.set('DumpSettings', 'pjloglevel',  dumpSettings.pjLogLevel)
        config.write(cfgFile)
        cfgFile.close()

    def deleteSection(self,  section):
        config = ConfigParser.SafeConfigParser()
        try:
            config.read(self.__filePath)
            config.remove_section(section)
            cfgFile = open(self.__filePath, 'w')
            config.write(cfgFile)
            cfgFile.close()
        except:
            pass
    
    def configSectionMap(self,  section,  config):
        dict1 = {}
        options = config.options(section)
        for option in options:
            try:
                dict1[option] = config.get(section, option)
            except:
                print("exception on %s!" % option)
                dict1[option] = None
        return dict1

    def toBool(self,  string):
        return string.lower() in ("true",  "1",  "y")
