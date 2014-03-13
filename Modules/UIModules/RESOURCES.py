class MetaA(type):
    def __getitem__(cls, param):
        return cls._config.get(param)

class RESCOURCES_UI(object, metaclass=MetaA):
    mainPath="./Modules/UIModules/UIResources/"
    _config = dict( \
    AccountDialog = mainPath + "AccountDialog.ui", \
    BuddyDialog = mainPath + "BuddyDialog.ui",  \
    CallDialog = mainPath + "CallDialog.ui",  \
    DynamicUI = mainPath + "DynamicUI.ui",  \
    IncomingCallDialog = mainPath + "IncomingCallDialog.ui"  ,\
    LoadingUI = mainPath + "LoadingUI.ui", \
    MediaSettingsWidget = mainPath + "MediaSettingsWidget.ui", \
    RegisterDialog = mainPath + "RegisterDialog.ui", \
    DeviceChooserDialog = mainPath + "DeviceChooserDialog.ui", \
    DeviceChooserDialogSimple = mainPath + "DeviceChooserDialogSimple.ui", \
    StatisticDialog = mainPath + "StatisticsDialog.ui"
    )

class RESCOURCES_PIC(object, metaclass=MetaA):
    mainPath="./Modules/UIModules/UIResources/"
    _config = dict( \
    Busy = mainPath + "busy.png",  \
    LoadAnimation = mainPath + "LoadAni.gif", \
    Offline = mainPath + "offline.png", \
    Online = mainPath + "online.png"
    )