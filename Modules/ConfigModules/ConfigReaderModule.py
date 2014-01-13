import ConfigParser
import pjsua

filePath = 'Settings.conf'

"""
DEPRECATED
"""


#Account
def readAccountConfig(configurationFile=filePath):
    account = None
    try:
        config = ConfigParser.ConfigParser()
        config.read(configurationFile)
        
        dict = configSectionMap("Account",  config)
        account = Account(dict['sipservername'],  dict['sipserverport'], dict['sipname'],  dict['sipsecret'],  False, None)
        try:
            account.stunServer = dict['stunserver']
            account.stun = True
        except:
            pass
    except:
        pass
    return account

#Media
def readMediaConfig(configurationFile=filePath):
    mediaConf = pjsua.MediaConfig()
    try:
        config = ConfigParser.ConfigParser()
        config.read(configurationFile)
        dict = configSectionMap("MediaSettings",  config)
        
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


#Network
def readNetworkSettings(configurationFile=filePath):
    try: 
        config = ConfigParser.ConfigParser()
        config.read(configurationFile)
        dict = configSectionMap("NetworkSettings", config)
        ns = NetworkSettings()
        ns.initWithDict(dict)
    except:
        ns = NetworkSettings()
    return ns


#Video
def readVideoConfig(configurationFile=filePath):
    videoSettings = None
    try:
        config = ConfigParser.ConfigParser()
        config.read(configurationFile)
        
        dict = configSectionMap("Video", config)
        videoSettings.captureDevice = dict['capturedevice']
        videoSettings.renderDevice = dict['renderdevice']
        videoSettings.outgoingDefault = dict['outgoingdefault']
        videoSettings.incomingDefault = dict['incomingdefault']
    except:
        pass
    return videoSettings

#Buddy
def readFirstBuddyURI(configurationFile=filePath):
    buddyUri = None
    try:
        config = ConfigParser.ConfigParser()
        config.read(filePath)

        dict = configSectionMap("BuddyConfig",  config)
        buddyUri = dict[dict.keys()[0]]
    except:
        pass
    return buddyUri

def readFirstBuddyNumber(path = None):
    buddyNumber = None
    try:
        config = ConfigParser.ConfigParser()
        if path:
            config.read(path)
        else:
            config.read(filePath)
        dict = configSectionMap("BuddyConfig",  config)
        buddyNumber = dict[dict.keys()[0]]
        buddyNumber = buddyNumber.partition('"')[-1].rpartition('"')[0]
    except:
        pass
    return buddyNumber

#Internal
def configSectionMap(section,  config):
    dict1 = {}
    options = config.options(section)
    for option in options:
        try:
            dict1[option] = config.get(section, option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1
