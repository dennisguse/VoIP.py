#TODO Copyright (C) 
#TODO Lisence

Quick Info:
	_____________________________________________________

	Installation steps (examples are valid for gentoo):
		1. install python-2.7 if missing
		2. install pyqt 	($ emerge dev-python/PyQt4)
		3. install pjsua, you will find a detailed documentation here:
		   http://trac.pjsip.org/repos/wiki/Python_SIP/Build_Install
		   ($ cd your-pjsip-root-dir
		    $ ./configure && make dep && make
		    $ cd pjsip-apps/src/python
		    $ sudo make)
		4. install pyaudio (emerge dev-python/pyaudio)
	or install: https://launchpad.net/~dennis.guse/+archive/sip-tools

Contents:
	_____________________________________________________

	1. Features
	2. Limitations
	3. Advanced Configuration Possibilities

1. Features:
	_____________________________________________________
	
	1.  Calls (what else ;-) )
	
	3.  STUN support
	4.  UDP/TCP support (SIP)
	5.  Different ringtone support
	6.  Configuration of media parameters (see 4. II)
	7.  Presence support (incl. reason)
	8.  Debug support (store wave files of each call, store call statistics (using pjsip statistics),
	    store programs configuration on exit, manipulate pjsua log level)
	9.  Different sound devices (possible to choose the input and output 
	    sound device via parameter)
	10. UI exchangable


2. Limitations:
	_____________________________________________________

	1. Program is currently limited to one call
	2. No video support
	3. No SIP/TLS support
	4. Codec not configurable (not yet)
	5. Wave-recording merges caller and callee (needs to be splited)

3. Advanced Configuration Possibilities
	_____________________________________________________

	There are two files used to configure the program manually:
	I. telSimple.db
		The telSimple.db holds the account data. It is a sqlite data base
		and can be simply edited with "$ sqlite telSimple.db"
		There is only one table could accounts.
		To view the data enter the command "SELECT * FROM accounts;"
		Fields:
			a) sipServerAddress -> address of the sip server
			b) sipPort -> the listing port of the sip server
			c) sipName -> user name to register the account
			d) sipSecret -> password to register the account
			e) stunServer -> STUN server address, NO if there is no
					 STUN server
			f) isActive -> True if the choosen account is active
				       There can be only on active account!
			g) transportType -> currently not in use
			h) callStatistics -> currently not in use
			i) securityEnabled -> currently not in use
			j) securityMode -> currently not in use
			k) machineCertPath -> currently not in use
			l) privateKeyPath -> currently not in use
		Example to create a new user:
			"INSTERT INTO accounts (sipServerAddress,sipPort,
			 sipName, sipSecret, stunServer, isActive, transportType,
			 callStatistics, securityEnabled, securityMode,
			 machineCertPath, privateKeyPath) VALUES 
			 ("testServer.com", 5060, "testPasswd", NO, "false", "UDP",
			 "NO", "NO", "NO", "NO", "NO");"
	II. Settings.conf
		The Settings.conf is a ini file divided into the following chapters
		(all following example parameters are the standard parameters):
			a) [RingtoneConfig]
			   ringtone = ./Ringtones/phone.wav
			   #The path to the ringtone file 

			b) [BuddyConfig]
			   10 = "10" <sip:10@192.168.0.107>
			   #A buddy URI, used for presence

			c) [DumpSettings]
			   wave = False
			   #If true wave files of every call will be stored
			   callstats = False
			   #If true call statistics of every call will be stored
			   lastactivesettings = True
			   #If true the programs configuration will be written to disk if on exit
			   pjloglevel = 0
			   #The level for the pjsua library (0-5)

			d) [MediaConfig] 
			   #For detailed parameter information go to:
			   #http://www.pjsip.org/python/pjsua.htm#MediaConfig
			   clockrate = 16000
			   sndclockrate = 0
			   sndautoclosetime = 1
			   channelcount = 1
			   audioframeptime = 20
			   maxmediaports = 254
			   quality = 8
			   ptime = 0
			   novad = 0
			   ilbcmode = 30
			   txdroppct = 0
			   rxdroppct = 0
			   ecoptions = 0
			   ectaillen = 200
			   jbmin = -1
			   jbmax = -1
			   enableice = 0
			   enableturn = 0
			   turnserver = 
			   turnconntype = 17
			   turncred = None

			e) [SoundDeviceSettings]
			   captureid = -1
			   #The id of the capture sound device
			   playbackid = -2
			   #The id of the playback sound device

			f) [NetworkSettings]
			   tcp = False
			   #If true TCP will be used, otherwise UDP
			   ipv6 = False
			   #Currently not in use
			   networkport = None
			   #Currently not in use
			g) [CodecSettings]
			   #A list of all available codecs
			   #For parameter description visit:
			   #http://www.pjsip.org/python/pjsua.htm#CodecInfo
			   speex/16000/1:priority = 130
			   speex/16000/1:clock_rate = 16000
			   speex/16000/1:channel_count = 1
			   speex/16000/1:avg_bps = 27800
			   speex/16000/1:frm_ptime = 1645215764
			   speex/16000/1:ptime = 98
			   speex/16000/1:pt = 0
			   speex/16000/1:vad_enabled = 1
			   speex/16000/1:plc_enabled = 1
