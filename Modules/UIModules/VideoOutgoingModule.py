from Modules.UIModules import VideoViewModule
import pjsua
from SIPController.VideoSettings import VideoSettings

class VideoOutgoingModule(VideoViewModule.VideoViewModule):

    def __init__(self):
        super(VideoOutgoingModule, self).__init__()

    def start(self, parameters):
        settings = VideoSettings()

        windowId = pjsua.Lib.instance().start_video_preview(settings.captureDevice, settings.renderDevice)
        self.showVideoPane(parameters["parentWindow"], parameters["parentContainer"], windowId);

    def dismiss(self):
        pjsua.Lib.instance().stop_video_preview()
        self.dismissVideoPane()