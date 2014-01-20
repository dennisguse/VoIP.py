from Modules.UIModules import VideoViewModule
import pjsua
from SIPController.VideoSettings import VideoSettings

class VideoOutgoingModule(VideoViewModule):

    def start(self, parameters):
        settings = VideoSettings()

        windowId = pjsua.Lib().instance.start_video_preview(settings.captureDevice, settings.renderDevice)
        self.showVideoPane(parameters["parentVideo"], parameters["parentContainer"], windowId);

    def dismiss(self):
        pjsua.Lib().instance().stop_video_preview()
        self.dismissVideoPane()

a=VideoOutgoingModule()