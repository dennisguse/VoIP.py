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
            self.dia.show()
            self.dia.exec_()

    def dismiss(self):
        pass

    def initDialog(self):
        self.dia = uic.loadUi(UIResources.RESCOURCES_UI["DeviceChooserDialog"], self)
        self.dia.btn.clicked.connect(self.save)
        self.lib = pjsua.Lib.instance()
        self.sndDevices = self.lib.enum_snd_dev()
        for device in self.sndDevices:
            print("New device:")
            print(device.name)
            print("Input: " + str(device.input_channels))
            print("Output: " + str(device.output_channels))
            print("ID: " + str(device.device_id))
            #if "(hw:" not in device.name: #Valid deviceId available?
            #     continue
            if device.input_channels > 0:
                 self.dia.cmbDeviceInput.addItem(device.name)
            if device.output_channels > 0:
                 self.dia.cmbDeviceOutput.addItem(device.name)

    def save(self):
        inputId = 0
        outputId = 0
        for device in self.sndDevices:
            if self.dia.cmbDeviceInput.currentText() == device.name:
                inputId = device.device_id
            if self.dia.cmbDeviceOutput.currentText() == device.name:
                outputId = device.device_id
        self.lib.set_snd_dev(inputId, outputId)
        self.dia.close()
        #self.showWaring()

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