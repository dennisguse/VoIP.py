import ConfigModules.VideoDeviceConst as UserDefinded

class VideoDeviceModule(object):
    '''
    User configuration within the file VideoDeviceConst.py
    '''

    def __init__(self):
        self.video_outgoing_default = UserDefinded.video_outgoing_default
        self.video_capture_device = UserDefinded.video_capture_device
        self.video_render_device = UserDefinded.video_render_device
        self.vid_out_auto_transmit = UserDefinded.vid_out_auto_transmit
        self.vid_in_auto_show =  UserDefinded.vid_in_auto_show
