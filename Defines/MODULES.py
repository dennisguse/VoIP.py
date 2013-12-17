class MetaA(type):
    def __getitem__(cls, param):
        return cls._config.get(param)

class MODULES(object):
    __metaclass__=MetaA
    _config = dict( \
    RegisterStateDialog = './Modules/UIModules/RegisterStateModule.py', \
    CallDialog = './Modules/UIModules/CallDialogModule.py',  \
    IncomingCallDialog = './Modules/UIModules/IncomingCallDialogModule.py',  \
    ErrorDialog = './Modules/UIModules/ErrorDialogModule.py',  \
    RingToneModule = './Modules/CallModules/RingToneModule.py',  \
    WaveRecordModule = './Modules/CallModules/WaveRecordModule.py', \
    SingleBuddyModule = './Modules/PresenceModules/SingleBuddyModule.py', \
    VideoPreviewModule = './Modules/UIModules/VideoPreviewModule.py', \
    DeviceChooserModule = './Modules/UIModules/DeviceChooserModule.py', \
    VideoCallModule = './Modules/UIModules/VideoCallModule.py'
    )
    
