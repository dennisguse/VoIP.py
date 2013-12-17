import pjsua

class MediaConfigModule(object):

    """
    CONFIGURE HERE!
    """
    clock_rate = None
    snd_clock_rate = None
    snd_auto_close_time = None
    channel_count = None
    audio_frame_ptime = None
    max_media_ports = None
    quality = None
    ptime = None
    no_vad = True
    ilbc_mode = None
    tx_drop_pct = None
    rx_drop_pct = None
    ec_options = None
    ec_tail_len = None
    jb_min = None
    jb_max = None
    enable_ice = None
    enable_turn = None
    turn_server = None
    turn_conn_type = None
    turn_cred = None
    """
    END OF CONFIGURATION
    """

    def __init__(self):
        self.__mediaConfig = pjsua.MediaConfig()
        self.implementConfiguration()

    def getMediaConfig(self):
        return self.__mediaConfig

    def implementConfiguration(self):
        members  = [attr for attr in dir(self) if not callable(getattr(self,attr)) and not attr.startswith("__") and not attr.startswith("_")]
        for member in members:
            if getattr(self, member):
                setattr(self.__mediaConfig, member, getattr(self, member))
