import logging
import PJSIPLoggingCallBack

import pjsua as pj
from ConfigModules import AccountConfigModule, AudioDeviceModule, DumpSettingsModule, MediaConfigModule, NetworkSettingsModule, CodecConfigurationModule, VideoDeviceModule
import SIPController.AccountCallBack as accountCallB
import SIPController.CallCallBack as CallCallBack
import SIPController.PresenceCallBack as PresenceCallBack
import SIPController.ControllerCallBacksHolder as ControllerCallBacksHolder
import Defines.SIP_STATUS_CODES as SIP_CODES


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
        self.pjLib = None
        self.pjCallCallBack = None
        self.currentCall = None
        self.accountInfo = None
        self.transport = None
        self.recordWav = 0
        self.accountBuddys = None
        if controllerCallBack:
            self.controllerCallBack = controllerCallBack
        else:
            self.controllerCallBack = ControllerCallBacksHolder()
        self.initFromConfiguration()
        self.initLib()

        #TODO REMOVE!!!!!!!!! Must be done via Configuration
        CodecConfigurationModule.applyConfiguration(self.pjLib)
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
            self.pjLib = pj.Lib()
            uaCfg = pj.UAConfig()
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

            self.pjLib.init(uaCfg, log_cfg = pj.LogConfig(level=5, callback=PJSIPLoggingCallBack.log), media_cfg=self.mediaConfig)

            if self.audioDevice.captureDevId != None and self.audioDevice.playbackDevId != None: #TODO make this via module / callback or whatever.
                self.pjLib.set_snd_dev(self.audioDevice.captureDevId, self.audioDevice.playbackDevId)
            self.pjLib.start()
        except:
            self.pjLib.destroy()
            self.pjLib = None
            self.logger.error("PJSIP could not be started.")
            sys.exit(-1)
        return

    def registerClient(self):
        """
        Registers the client
        """
        if self.accountInfo is not None:
            self.initTransport()

            try:
                lck = self.pjLib.auto_lock()
                acc_cfg = pj.AccountConfig()
                acc_cfg.id = self.accountInfo.getSipAddress()
                acc_cfg.reg_uri = self.accountInfo.getSipRegURI()
                acc_cfg.video_outgoing_default = self.videoDevice.video_outgoing_default
                acc_cfg.video_capture_device = self.videoDevice.video_capture_device
                acc_cfg.video_render_device = self.videoDevice.video_render_device
                acc_cfg.vid_out_auto_transmit = self.videoDevice.vid_out_auto_transmit
                acc_cfg.vid_in_auto_show =  self.videoDevice.vid_in_auto_show
                acc_cfg.auth_cred = [pj.AuthCred("*", str(self.accountInfo.sipName), str(self.accountInfo.sipSecret))] #No better way using bindings?
                if self.networkSettings != None:
                    if self.networkSettings.tcp == True:
                        acc_cfg.proxy.append("<"+ str(self.accountInfo.getSipAddress()) +";lr;transport=tcp>") #Haeh?
                self.pjAccount = self.pjLib.create_account(acc_cfg)
                self.pjAccount.set_basic_status(True)
                self.pjAccountCb  = accountCallB.AccountCallBack(self.onIncommingCall, self.onRegStateChanged, self.pjAccount)
                self.pjAccount.set_callback(self.pjAccountCb)
                del lck
            except pj.Error, e:
                self.logger.error("Error while registration: ", e)

        else:
            self.logger.info('Account informations are not complete')
        return

    def registerBuddys(self):
        if self.accountBuddys.hasBuddys():
            for buddy in self.accountBuddys:
                self.addBuddy(buddy.buddyURI,  buddy.changeOnlineStatus)

    def addBuddy(self,  buddyURI,  buddyOnStateChange = None):
        buddy = self.pjAccount.add_buddy(buddyURI,  PresenceCallBack.PresenceCallBack(None, buddyOnStateChange))
        buddy.subscribe()

    def initTransport(self):
        if self.networkSettings.tcp == True:
           transportType = pj.TransportType.TCP
        else:
           transportType = pj.TransportType.UDP

        if self.networkSettings.networkPort is not None:
           self.transport = self.pjLib.create_transport(transportType, pj.TransportConfig(int(self.networkSettings.networkPort)))
        else:
           self.transport = self.pjLib.create_transport(transportType)

    def callNumber(self, number):
        """
        Calls the given number.
        @type number: number
        @param number: The number to call
        """
        self.logger.info("Trying to call sip: " + str(number) + "@" + str(self.accountInfo.sipServerAddress))
        if self.currentCall == None:
            toCall = "sip:" + str(number) + "@" + str(self.accountInfo.sipServerAddress)
            self.logger.info('Calling ' + toCall)
            self.currentCall = self.pjAccount.make_call(str(toCall), self.pjCallCallBack)
            self.currentCallCallback = CallCallBack.CallCallBack(self.dumpSettings, self.callClear, self.controllerCallBack,  self.currentCall,  self.pjLib)
            self.currentCall.set_callback(self.currentCallCallback)
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
        if self.currentCall != None:
            self.currentCall.userHangup = True
            self.currentCall.hangup(SIP_CODES.SIP_OK)
            self.currentCall = None
            self.currentCallCallback = None
        else:
            try:
                self.pjAccountCb.hangup(SIP_CODES.SIP_OK)
            except:
                pass
        return

    def freeLib(self):
        """
        Destroys the SIP library.
        """
        try:
            self.pjLib.destroy()
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
            if self.pjAccount.info().reg_status == SIP_CODES.SIP_OK:
                reg = True
            self.controllerCallBack.onRegStateChanged(reg, self.pjAccount.info().reg_status,  self.pjAccount.info().reg_reason)

    def onIncommingCall(self,  call = None):
        if self.currentCall != None:
            call.hangup(SIP_CODES.SIP_BUSY_HERE) #TODO loggging
        else:
            self.currentCall = call
            self.logger.info('Incoming call from ' + self.currentCall.info().remote_uri)
            self.currentCallCallback = CallCallBack.CallCallBack(self.dumpSettings, self.callClear, self.controllerCallBack,  self.currentCall,  self.pjLib)
            self.currentCall.set_callback(self.currentCallCallback)
            self.controllerCallBack.connectIncomingCall()
            self.logger.debug("SipController informed about incomming call")

    def callClear(self):
        self.currentCall = None
        self.currentCallCallback = None

    def setPresenceStatus(self, is_online, activity=0, pres_text="", rpid_id=""):
        self.pjAccount.set_presence_status(is_online,  activity,  pres_text,  rpid_id)

    def setBasicPresenceStatus(self, is_online):
        self.pjAccount.set_basic_status(is_online)

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
            return self.currentCall.info().remote_uri
        except:
            return None

    def reinitLibWithNewMedia(self,  mediaConf): #TODO Merge with init? 
        self.mediaConf = mediaConf
        self.freeLib()
        self.initLib()
        self.registerClient()