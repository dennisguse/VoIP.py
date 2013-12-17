class MetaA(type):
    def __getitem__(cls, param):
        return cls._config.get(param)

class RESCOURCES_MAINUI(object):
    __metaclass__=MetaA
    mainPath="./Modules/MainUIModules/UIResources/"
    _config = dict( \
    Expert = mainPath + "MainUIExpert.ui", \
    Simple = mainPath + "MainUISimple.ui",  \
    SimpleVideo = mainPath + "MainUISimpleVideo.ui",  \
    Standard = mainPath + "MainUIStandard.ui"  \
    )
