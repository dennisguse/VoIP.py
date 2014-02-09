from Modules.UIModules import VideoViewModule
import pjsua
from ConfigModules.VideoDeviceModule import VideoDeviceModule

class VideoOutgoingModule(VideoViewModule.VideoViewModule):

    def __init__(self):
        super(VideoOutgoingModule, self).__init__()

    def start(self, parameters):
        settings = VideoDeviceModule()
        windowId = pjsua.Lib.instance().start_video_preview(settings.video_capture_device, settings.video_render_device)
        pjsua.Lib.instance().resize_video_preview(settings.video_capture_device, 50, 75)
        self.showVideoPane(parameters["parentWindow"], parameters["parentContainer"], windowId);

    def dismiss(self):
        pjsua.Lib.instance().stop_video_preview()
        self.dismissVideoPane()