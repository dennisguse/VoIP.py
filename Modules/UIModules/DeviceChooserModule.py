from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import uic
from ConfigModules import AudioDeviceModule
import Modules.UIModules.RESOURCES as UIResources
import pjsua
import logging

#TODO Add single selector mode (in one class).
#TODO Add logging
#TODO Refactor snd to audio
#TODO Use of QVariant (with SndDevice); better solution than using device.name.
#TODO Check for updates from PJSIP?

class DeviceChooserModule(QDialog):

    def __init__(self):
        super(DeviceChooserModule, self).__init__(None)
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
        self.dialog = uic.loadUi(UIResources.RESCOURCES_UI["DeviceChooserDialog"], self)
        self.dialog.btn.clicked.connect(self.save)
        for device in self.audioDeviceList:
            print(device.name, " (Input-ID:", str(device.input_channels), " // Output-ID ", str(device.output_channels), ") Device-ID: ", str(device.device_id))
            if device.input_channels > 0:
                 self.dialog.cmbDeviceInput.addItem(device.name, device.device_id)
            if device.output_channels > 0:
                 self.dialog.cmbDeviceOutput.addItem(device.name, device.device_id)

        self.dialog.cmbDeviceInput.currentIndexChanged['QString'].connect(self.cmbInputIndexChanged)

    def cmbInputIndexChanged(self, newValue):
        #TODO Add auto update for Output automatically; requires sanity check if device exists.
        return

    def save(self):
        (inputId, ok) = self.dialog.cmbDeviceInput.itemData(self.dialog.cmbDeviceInput.currentIndex()).toInt()
        (outputId, ok) = self.dialog.cmbDeviceOutput.itemData(self.dialog.cmbDeviceOutput.currentIndex()).toInt()
        #TODO Do sanity check here (is device still there?)
        pjsua.Lib.instance().set_snd_dev(inputId, outputId)

        self.dialog.done(0)
        return

    def reject(self): #Ignore ESC
        return;