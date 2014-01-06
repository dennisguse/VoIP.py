from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import uic
from ConfigModules import AudioDeviceModule
import Modules.UIModules.RESOURCES as UIResources
import pjsua
import logging

#TODO Merge with DeviceChooserModule
#TODO Add logging
#TODO Use of QVariant (with SndDevice); better solution than using device.name.
#TODO Check for updates from PJSIP?

class DeviceChooserModuleSimple(QDialog):

    def __init__(self):
        super(DeviceChooserModuleSimple, self).__init__(None)
        self.logger = logging.getLogger("DeviceChooserSimple")
        self.audioDeviceList = pjsua.Lib.instance().enum_snd_dev()
        return

    def hasSignalsToRegister(self):
        return False

    def start(self):
        currentSettings = AudioDeviceModule.AudioDeviceModule().getAudioDeviceSettings()
        if currentSettings.playbackDevId == None or currentSettings.captureDevId == None: #TODO Check for not existing
            self.initDialog()
            self.dialog.exec_()

    def dismiss(self):
        pass

    def initDialog(self):
        self.logger.info("Opening dialog")

        self.dialog = uic.loadUi(UIResources.RESCOURCES_UI["DeviceChooserDialogSimple"], self)
        self.dialog.btn.clicked.connect(self.save)
        for device in self.audioDeviceList:
            self.logger.debug(device.name, " (Input-Channels:", str(device.input_channels), " // Output-Channels ", str(device.output_channels), ") Device-ID: ", str(device.device_id))
            if (device.input_channels > 0) and (device.output_channels > 0):
                 self.dialog.cmbDeviceInput.addItem(device.name, device.device_id)

    def save(self):
        (deviceId, ok) = self.dialog.cmbDeviceInput.itemData(self.dialog.cmbDeviceInput.currentIndex()).toInt()

        self.logger.info("User selected: " + str(deviceId))
        #TODO Do sanity check here (is device still there?)
        pjsua.Lib.instance().set_snd_dev(deviceId, deviceId)

        self.dialog.done(0)
        return

    def reject(self): #Ignore ESC
        return;