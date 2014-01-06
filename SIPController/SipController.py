import logging

import pjsua as pj
from ConfigModules import AccountConfigModule, AudioDeviceModule, DumpSettingsModule, MediaConfigModule, NetworkSettingsModule
import SIPController.AccountCallBack as accountCallB
import SIPController.CallCallBack as CallCallBack
import SIPController.PresenceCallBack as PresenceCallBack
import SIPController.CodecList as CodecList
import SIPController.ControllerCallBacksHolder as ControllerCallBacksHolder


class SipController(object):
    """
    Handles the SIP interactions of the client.
    """

    #TODO remove codec list
    def __init__(self, controllerCallBack = None, codecList = None):
        """
        Initializes the sip handler.
        """
        self.pjAccount = None
        self.pjAccountCb = None
        self.pjLib = None
        self.pjCallCallBack = None
        self.currentCall = None
        self.log_cb = None
        self.accountInfo = None
        self.transport = None

        self.loglevel = 0
        self.recordWav = 0
        self.accountBuddys = None
        self.logger = logging.getLogger('SipController') #TODO


        self.codecList = codecList #TODO write module



        if controllerCallBack:
            self.controllerCallBack = controllerCallBack
        else:
            self.controllerCallBack = ControllerCallBacksHolder()



        self.initFromConfiguration()
        self.initLib()
        self.registerClient()
        return

    def initFromConfiguration(self):
        self.mediaConf = MediaConfigModule.MediaConfigModule().getMediaConfig()
        self.networkSettings = NetworkSettingsModule.NetworkSettingsModule().getNetworkSettings()
        self.accountInfo = AccountConfigModule.AccountConfigModule().getAccountSettings()
        self.dumpSettings = DumpSettingsModule.DumpSettingsModule().getDumpSettings()
        self.audioDevice = AudioDeviceModule.AudioDeviceModule().getAudioDeviceSettings()

    def log_cb(self,level,message):
        """
        Logs all pjsua informations on the console
        """
        #TODO Not yet used.
        self.logger.info(level + " " + message)

    def initLib(self):
        """
        Initializes the SIP library.
        """
        try:
            self.pjLib = pj.Lib()
            uaCfg = pj.UAConfig()
            uaCfg.max_calls = 2 #TODO Should onyl be 1 or at least configurable...
            if self.accountInfo.hasStunSupport():
                uaCfg.stun_host = str(self.accountInfo.stunServer)            
                if self.mediaConf is None:
                    self.pjLib.init(uaCfg, log_cfg = pj.LogConfig(level=int(self.dumpSettings.pjLogLevel), callback=self.log_cb))
                else:
                    self.pjLib.init(uaCfg, log_cfg = pj.LogConfig(level=int(self.dumpSettings.pjLogLevel), callback=self.log_cb), media_cgf=self.mediaConf)
                self.logger.info("STUN enabled")
            else:
                if self.mediaConf is None:
                    self.pjLib.init(uaCfg, log_cfg = pj.LogConfig(level=int(self.dumpSettings.pjLogLevel), callback=self.log_cb))
                else:
                    self.pjLib.init(uaCfg, log_cfg = pj.LogConfig(level=int(self.dumpSettings.pjLogLevel), callback=self.log_cb), media_cfg=self.mediaConf)
            if self.audioDevice.captureDevId != None and self.audioDevice.playbackDevId != None:
                self.pjLib.set_snd_dev(self.audioDevice.captureDevId, self.audioDevice.playbackDevId)
            self.pjLib.start()
        except:
            self.pjLib.destroy()
            self.pjLib = None
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


                #TODO
                acc_cfg.video_outgoing_default = True
                acc_cfg.video_capture_device = 0
                acc_cfg.video_render_device = -2


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
        buddy = self.pjAccount.add_buddy(buddyURI,  PresenceCallBack.PresenceCallBack(None,  buddyOnStateChange))
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
            self.currentCall.hangup(200)
            self.currentCall = None
            self.currentCallCallback = None
            #self.pjLib.recorder_destroy(self.recorderID) #TODO Check if needed.
        else:
            try:
                self.pjAccountCb.hangup(200) #TODO Use status code?
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
            if self.pjAccount.info().reg_status == 200:
                reg = True
            self.controllerCallBack.onRegStateChanged(reg, self.pjAccount.info().reg_status,  self.pjAccount.info().reg_reason)

    def onIncommingCall(self,  call = None):
        if self.currentCall != None:
            call.hangup(468) #TODO status code and loggging
        else
            self.currentCall = call

            self.logger.info('Incoming call from ' + self.currentCall.info().remote_uri)
            self.currentCallCallback = CallCallBack.CallCallBack(self.dumpSettings, self.callClear, self.controllerCallBack,  self.currentCall,  self.pjLib)
            self.currentCall.set_callback(self.currentCallCallback)
            self.controllerCallBack.connectIncomingCall()

    def callClear(self):
        self.currentCall = None
        self.currentCallCallback = None

    def setPresenceStatus(self, is_online, activity="", pres_text="", rpid_id=""):
        self.pjAccount.set_presence_status(is_online,  activity,  pres_text,  rpid_id)

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

    def reinitLibWithNewMedia(self,  mediaConf):
        self.freeLib()
        self.initLib()
        self.registerClient()

    def listCodecs(self):
        if self.codecList == None:
            self.codecList = CodecList.CodecList()
            self.codecList.initWithList(self.pjLib.enum_codecs())
            self.codecList.printList()
            #sc = SipConfigParser.SipConfigParser()
            #sc.writeCodecList(self.codecList)