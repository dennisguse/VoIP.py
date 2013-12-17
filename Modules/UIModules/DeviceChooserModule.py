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
        return

    def hasSignalsToRegister(self):
        return False

    def start(self):
        currentSettings = AudioDeviceModule.AudioDeviceModule().getAudioDeviceSettings()
        if currentSettings.playbackDevId == None or currentSettings.captureDevId == None:
            self.initDialog()
            self.dia.show()
            self.dia.exec_()

    def dismiss(self):
        pass

    def initDialog(self):
        self.dia = uic.loadUi(UIResources.RESCOURCES_UI["DeviceChooserDialog"], self)
        self.dia.btn.clicked.connect(self.save)
        self.lib = pjsua.Lib.instance()
        sndDevices = self.lib.enum_snd_dev()
        for device in sndDevices:
            if "(hw:" not in device.name: #Valid deviceId available?
                 continue
            if device.input_channels > 0:
                 self.dia.cmbDeviceInput.addItem(device.name)
            if device.output_channels > 0:
                 self.dia.cmbDeviceOutput.addItem(device.name)

    def save(self):
        self.lib.set_snd_dev(self.getId(self.dia.cmbDeviceInput.currentText(), 0),\
                                           self.getId(self.dia.cmbDeviceOutput.currentText(), 1))
        self.dia.close()
        self.showWaring()

    def getId(self, text, position):
        if position == 0:
            return int(text.split("(hw:")[1][0])
        else:
            return int(text.split("(hw:")[1][2])

    def showWaring(self):
	return
        diaWaring = QMessageBox()
        diaWaring.setWindowTitle('Attention!')
        diaWaring.setText('Because of the incredible laziness of the developer you have to set the device id by your self in the file:\n Modules.ConfigModules.AudioDeviceModule\nIf you want to avoid if dialog')
        diaWaring.show()
        diaWaring.exec_()