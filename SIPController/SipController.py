import logging
import SIPController.PJSIPLoggingCallBack
import sys
import pjsua2 as pj
from ConfigModules import AccountConfigModule, AudioDeviceModule, DumpSettingsModule, MediaConfigModule, NetworkSettingsModule, CodecConfigurationModule, VideoDeviceModule
from SIPController import Account
import SIPController.CallCallBack as CallCallBack
from SIPController.Call import Call
from SIPController import Endpoint
from SIPController.Buddy import Buddy
import SIPController.PresenceCallBack as PresenceCallBack
import SIPController.ControllerCallBacksHolder as ControllerCallBacksHolder
import Defines.SIP_STATUS_CODES as SIP_CODES
from PyQt4 import QtCore

class SipController(object):
    """
    Handles the SIP interactions of the client.
    """

    def __init__(self, controllerCallBack = None, codecList = None):
        """
        Initializes the sip handler.
        """
        self.logger = logging.getLogger('SipController')
        self.pjAccount = None
        self.pjAccountCb = None
        #self.pjLib = None
        self.ep = None
        self.pjCallCallBack = None
        self.currentCall = None
        self.accountInfo = None
        #self.transport = None
        self.recordWav = 0
        self.accountBuddys = None
        if controllerCallBack:
            self.controllerCallBack = controllerCallBack
        else:
            self.controllerCallBack = ControllerCallBacksHolder()
        self.initFromConfiguration()
        self.initLib()

        #TODO REMOVE!!!!!!!!! Must be done via Configuration
        CodecConfigurationModule.applyConfiguration(self.ep)
        return

    def initFromConfiguration(self):
        self.mediaConfig = MediaConfigModule.MediaConfigModule().getMediaConfig()
        self.networkSettings = NetworkSettingsModule.NetworkSettingsModule().getNetworkSettings()
        self.accountInfo = AccountConfigModule.AccountConfigModule().getAccountSettings()
        self.dumpSettings = DumpSettingsModule.DumpSettingsModule().getDumpSettings()
        self.audioDevice = AudioDeviceModule.AudioDeviceModule().getAudioDeviceSettings()
        self.videoDevice = VideoDeviceModule.VideoDeviceModule()

    def initLib(self):
        """
        Initializes the SIP library.
        """
        try:
            self.ep = Endpoint.Endpoint()
            self.ep.libCreate()
            self.epConfig = pj.EpConfig()
            self.epConfig.uaConfig.threadCnt = 0
            self.epConfig.uaConfig.mainThreadOnly = True
            #self.epConfig.logConfig.writer = self.logger
            self.epConfig.logConfig.filename = "/tmp/testVOIP.log"
            self.epConfig.logConfig.fileFlags = pj.PJ_O_APPEND
            self.epConfig.logConfig.level = 6
            self.epConfig.logConfig.consoleLevel = 6
            uaCfg = pj.UaConfig()
            uaCfg.max_calls = 32 #TODO Should onl be 1 or at least configurable... (at the moment it is a bug in the base lib...)
            #its a "bug" in PJSIP; call.hangup does not remove the call *immediately*, but waits up 32s until the call is removed from call array.
            #Therefore an incoming call might overwrite the already used (but hangup) callslot.
            #Therefore the call_id of both calls is the same(!) and the timeout callback of the hangup call will kill the callback handler of the currently running call.
            #Since pjsua uses the call->user_data struct of pjsip to store the reference to the python call reference....
            #And then we are stuck....
            #It is a race condition.

            if self.accountInfo.hasStunSupport(): #STUN
                uaCfg.stun_host = str(self.accountInfo.stunServer)
                self.logger.info("STUN enabled")

            if self.mediaConfig is None: #MediaConfiguration
                self.mediaConfig = pjsua.MediaConfig() #TODO Make mediaconfig mandatory and handle this in class

            self.epConfig.uaConfig.userAgent = "VoIP.py-" + self.ep.libVersion().full;
            self.ep.libInit(self.epConfig)

            #TODO
            if self.audioDevice.captureDevId != None and self.audioDevice.playbackDevId != None: #TODO make this via module / callback or whatever.
                self.pjLib.set_snd_dev(self.audioDevice.captureDevId, self.audioDevice.playbackDevId)
            #END


            self.ep.libStart()
        except Exception as e:
            print(e)
            self.ep = None
            self.logger.error("PJSIP could not be started.")
            sys.exit(-1)
        return

    def _onTimer(self):
        self.ep.libHandleEvents(10)
        shoot = QtCore.QTimer()
        shoot.singleShot(50, self._onTimer)

    def registerClient(self):
        """
        Registers the client
        """
        if self.accountInfo is not None:
            self.initTransport()
            try:
                acc_cfg = pj.AccountConfig()
                acc_cfg.idUri = self.accountInfo.getSipAddress()
                acc_cfg.priority = 0
                #acc_cfg.video_outgoing_default = self.videoDevice.video_outgoing_default
                #acc_cfg.video_capture_device = self.videoDevice.video_capture_device
                #acc_cfg.video_render_device = self.videoDevice.video_render_device
                #acc_cfg.vid_out_auto_transmit = self.videoDevice.vid_out_auto_transmit
                #acc_cfg.vid_in_auto_show =  self.videoDevice.vid_in_auto_show
                cred = pj.AuthCredInfo()
                cred.scheme = "digest"
                cred.realm = "*"
                cred.username = str(self.accountInfo.sipName)
                cred.data = str(self.accountInfo.sipSecret)
                acc_cfg.sipConfig.authCreds.append(cred)
                acc_cfg.regConfig.registrarUri = self.accountInfo.getSipRegURI()
                self.pjAccount = Account.Account(self.onIncommingCall, self.onRegStateChanged)
                self.pjAccount.create(acc_cfg, True);

            except pj.Error as e:
                self.logger.error("Error while registration: ", e)

        else:
            self.logger.info('Account informations are not complete')
        return

    def registerBuddys(self):
        if self.accountBuddys.hasBuddys():
            for buddy in self.accountBuddys:
                self.addBuddy(buddy.buddyURI,  buddy.changeOnlineStatus)

    def addBuddy(self,  buddyURI,  buddyOnStateChange = None):
        buddycfg = pj.BuddyConfig()
        buddycfg.uri = buddyURI
        self.buddy = Buddy(buddyOnStateChange)
        self.buddy.create(self.pjAccount, buddycfg)
        self.buddy.subscribePresence(True)
        self.pjAccount.addBuddy(self.buddy)

    def initTransport(self):
        if self.networkSettings.tcp == True:
            transportType = pj.PJSIP_TRANSPORT_TCP
        else:
           transportType = pj.PJSIP_TRANSPORT_UDP
        transportConfig = pj.TransportConfig()
        if self.networkSettings.networkPort is not None:
           transportConfig.port = self.networkSettings.networkPort
        self.ep.transportCreate(transportType, transportConfig)

    def callNumber(self, number):
        """
        Calls the given number.
        @type number: number
        @param number: The number to call
        """
        self.logger.info("Trying to call sip: " + str(number) + "@" + str(self.accountInfo.sipServerAddress))
        if self.currentCall is None or self.currentCall.inactive is True:
            toCall = "sip:" + str(number) + "@" + str(self.accountInfo.sipServerAddress)
            self.logger.info('Calling ' + toCall)
            self.currentCall = Call(self.pjAccount, pj.PJSUA_INVALID_ID, self.dumpSettings, self.callClear, self.controllerCallBack)
            prm = pj.CallOpParam(True)
            self.currentCall.makeCall(str(toCall), prm)
            return self.currentCall
        else:
            self.logger.warning("Only one call is allowed!")
            raise

    def hangup(self):
        """
        Hangs up the current call.
        It's also save to use if there is no current call.
        """
        self.logger.info("Hangup current call")
        if self.currentCall is not None and self.currentCall.inactive is False:
            self.currentCall.userHangup = True
            self.currentCall.hangup(SIP_CODES.SIP_OK)
            self.currentCall.inactive = True
        else:
            try:
                print("TODO NOT IMPLEMENTED IN NEW LIB")
                self.pjAccountCb.hangup(SIP_CODES.SIP_OK)
            except:
                pass
        return

    def freeLib(self):
        """
        Destroys the SIP library.
        """
        try:
            if (self.currentCall is not None):
                self.currentCall.hangup()
            if (self.pjAccount is not None):
                self.pjAccount.setRegistration(False)
            self.ep.libDestroy()
        except:
            pass
        self.pjLib = None
        return

    def onRegStateChanged(self):
        """
        Calls the method, given with the method pointer, if the registration state change.
        """
        reg = False
        if self.pjAccount != 0:
            if self.pjAccount.getInfo().regIsActive == True:
                reg = True
            self.controllerCallBack.onRegStateChanged(reg, self.pjAccount.getInfo().regIsActive,  self.pjAccount.getInfo().regStatusText)
        self._onTimer()

    def onIncommingCall(self,  call = None):
        if self.currentCall != None:
            call.hangup(SIP_CODES.SIP_BUSY_HERE) #TODO loggging
        else:
            self.currentCall = call
            self.logger.info('Incoming call from ' + self.currentCall.getInfo().remoteUri)
            self.currentCall.setCallBacks(self.dumpSettings, self.callClear, self.controllerCallBack)
            self.currentCall.answerWithRinging()
            self.controllerCallBack.connectIncomingCall()
            self.logger.debug("SipController informed about incomming call")


    def callClear(self):
        self.currentCall = None
        self.currentCallCallback = None

    def setPresenceStatus(self, pj_status, pres_text="Unknown"):
        status = pj.PresenceStatus()
        status.statusText = pres_text
        status.status = pj_status
        self.pjAccount.setOnlineStatus(status)

    def getRegState(self): #TODO Refactor to getRegistrationState
        """
        Provides the registration state of the client.
        @rtype: bool
        @return: True if the client is registered
        """
        try:
            return self.pjAccount.info().reg_active
        except:
            self.logger.info('No active account')

    def getRegStateCode(self):
        try:
            return self.pjAccount.info().reg_status
        except:
            self.logger.info('No active account')

    def getRegStateReason(self):
        try:
            return self.pjAccount.info().reg_reason
        except:
            self.logger.info('No active account')

    def getCurrentCallVideoStream(self):
        return self.currentCall.get_remote_video()

    def connectCurrentCall(self):
        self.pjAccountCb.currentIncomingCall.answer()


    def getCurrentCallingNumber(self):
        """
        Provides the number of the calling party if there currently is a call.
        @rtype: string
        @return: The number of the calling party or None if there currently is no call
        """
        try:
            return self.currentCall.getInfo().remoteUri
        except:
            return None

    def reinitLibWithNewMedia(self,  mediaConf): #TODO Merge with init?
        self.mediaConf = mediaConf
        self.freeLib()
        self.initLib()
        self.registerClient()
