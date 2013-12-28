from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import uic
from ConfigModules import AudioDeviceModule
import Modules.UIModules.RESOURCES as UIResources
import pjsua
import logging

class DeviceChooserModule(QDialog):

    def __init__(self):
        super(DeviceChooserModule, self).__init__(None)
        self.sndDevices = None
        return

    def hasSignalsToRegister(self):
        return False

    def start(self):
        currentSettings = AudioDeviceModule.AudioDeviceModule().getAudioDeviceSettings()
        if currentSettings.playbackDevId == None or currentSettings.captureDevId == None:
            self.initDialog()
            self.dialog.show()
            self.dialog.exec_()

    def dismiss(self):
        pass

    def initDialog(self):
        self.dia = uic.loadUi(UIResources.RESCOURCES_UI["DeviceChooserDialog"], self)
        self.dialog.btn.clicked.connect(self.save)
        self.lib = pjsua.Lib.instance()
        self.sndDevices = self.lib.enum_snd_dev()
        for device in self.sndDevices:
            print(device.name, " (Input-ID:", str(device.input_channels), " // Output-ID ", str(device.output_channels), ") Device-ID: ", str(device.device_id))
            if device.input_channels > 0:
                 self.dialog.cmbDeviceInput.addItem(device.name)
            if device.output_channels > 0:
                 self.dialog.cmbDeviceOutput.addItem(device.name)

    def save(self):
        inputId = 0 	#Default device
        outputId = 0	#Default device
        for device in self.sndDevices: #TODO Check for sndDevice updates.
            if self.dialog.cmbDeviceInput.currentText() == device.name:
                inputId = device.device_id
            if self.dialog.cmbDeviceOutput.currentText() == device.name:
                outputId = device.device_id
        self.lib.set_snd_dev(inputId, outputId)

        self.dialog.done(0)

    def reject(self): #Ignore ESC
        return;