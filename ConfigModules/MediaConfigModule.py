import pjsua2
import ConfigModules.MediaConfigConst as UserDefined

class MediaConfigModule(object):
    '''
    User configuration within the file MediaConfigConst.py
    '''


    """
    END OF CONFIGURATION
    """

    def __init__(self):
        self.clock_rate = UserDefined.clock_rate
        self.snd_clock_rate = UserDefined.snd_clock_rate
        self.snd_auto_close_time = UserDefined.snd_auto_close_time
        self.channel_count = UserDefined.channel_count
        self.audio_frame_ptime = UserDefined.audio_frame_ptime
        self.max_media_ports = UserDefined.max_media_ports
        self.quality = UserDefined.quality
        self.ptime = UserDefined.ptime
        self.no_vad = UserDefined.no_vad
        self.ilbc_mode = UserDefined.ilbc_mode
        self.tx_drop_pct = UserDefined.tx_drop_pct
        self.rx_drop_pct = UserDefined.rx_drop_pct
        self.ec_options = UserDefined.ec_options
        self.ec_tail_len = UserDefined.ec_tail_len
        self.jb_min = UserDefined.jb_min
        self.jb_max = UserDefined.jb_max
        self.enable_ice = UserDefined.enable_ice
        self.enable_turn = UserDefined.enable_turn
        self.turn_server = UserDefined.turn_server
        self.turn_conn_type = UserDefined.turn_conn_type
        self.turn_cred = UserDefined.turn_cred
        self.__mediaConfig = pjsua2.MediaConfig()
        self.implementConfiguration()

    def getMediaConfig(self):
        return self.__mediaConfig

    def implementConfiguration(self):
        members  = [attr for attr in dir(self) if not callable(getattr(self,attr)) and not attr.startswith("__") and not attr.startswith("_")]
        for member in members:
            if getattr(self, member):
                setattr(self.__mediaConfig, member, getattr(self, member))
