from Modules.UIModules import VideoViewModule
from Modules import AbstractModule

class VideoIncomingModule(VideoViewModule.VideoViewModule):

    def __init__(self):
        super(VideoIncomingModule, self).__init__()

    def start(self, parameters):
        self.showVideoPane(parameters["parentWindow"], parameters["parentContainer"], parameters["windowId"])

    def dismiss(self):
        self.dismissVideoPane()
