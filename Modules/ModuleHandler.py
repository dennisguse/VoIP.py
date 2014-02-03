import imp, logging, sys, time
from Modules.MainUIModules.UILoaderModule import UILoader
from Modules.MainCliModules.MainCliModule import MainCli
from Modules.SignalHandler import SignalHandler
from Modules.UIModules.LoadingThread import LoadingThread

from Defines import SIGNALS
from PyQt4.QtCore import SIGNAL


class ModuleHandler(object):

    def __init__(self, mode, configurationFile="Settings.conf"):
        self.logger = logging.getLogger('ModuleHandler')
        self.classes = {} #The module classes (no instances) which can be used in the program
        self.objects = {} #The instances of the classes/modules.
        self.mode = mode

        if mode == "cli":
            self.logger.info("Starting in cli-mode:" + configurationFile)
            self.mode = MainCli()
        else:
            self.logger.info("Starting in uiMode(" + mode  + "): " + configurationFile)
            self.signalHandler = SignalHandler.getInstance() #TODO: add configurable configuration path: via CMD configurationFile
            self.signalHandler.init(self.module_load,  self.module_start,  self.module_dismiss)

            self.mode = UILoader(self.signalHandler, mode)
            self.signalHandler.setIncomingSignalSource(self.mode.ui)

        self.mode.start()

    def is_module_loaded(self,  moduleName):
        try:
            self.classes[moduleName]
            return True
        except:
            self.logger.debug("Module " + moduleName + " is not loaded!")
            return False

    def module_load(self,  moduleName,  modulePath):
        '''Loads the module, module name and path are given.
        The class will be loaded and a instance created.
        If the modules has to register signals this will be done here too.
        Modules must have a signal name. A own callback method or an internal callback method is optional.'''

        if self.is_module_loaded(moduleName):
            self.logger.warning("Module " + moduleName + " has already been loaded!")
            return
        self.logger.info("Loading module with name: " + moduleName)

        module = imp.load_source(moduleName, modulePath)
        self.classes[moduleName] = getattr(module, moduleName)
        self.objects[moduleName] = self.classes[moduleName]()

        if self.objects[moduleName].hasSignalsToRegister():
            for signal in self.objects[moduleName].getSignals():
                self.signalHandler.registerNewSignal(self.objects[moduleName],  signal[0],  signal[1],  signal[2])


    def module_start(self,  moduleName,  optionalParamenter = None, optionalParameter2 = None): #TODO Use hashmap for parameters, so that modules can easily access data.
        self.logger.debug("Activate Module " + moduleName)

        if not self.is_module_loaded(moduleName):
            self.logger.warning("Module " + moduleName + " is not loaded!")
            return

        if optionalParamenter != None and optionalParameter2 == None:
            self.objects[moduleName].start(optionalParamenter)
        elif optionalParamenter != None and  optionalParameter2 != None:
            self.objects[moduleName].start(optionalParamenter, optionalParameter2)
        else:
            self.objects[moduleName].start()


    def module_dismiss(self,  moduleName):
        self.logger.debug("Dismissing Module " + moduleName)
        if self.is_module_loaded(moduleName):
            self.objects[moduleName].dismiss()
        else:
            self.logger.error("The module " + moduleName + " can't be dismissed! Module is not loaded!")