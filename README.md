Copyright, 2013/2014
    Frank Haase (fra.haase@gmail.com)
    Dennis Guse (dennis.guse@alumni.tu-berlin.de)
The program is licensed under GPLv3 and comes WITHOUT ANY WARRANTY.

VoIP.py is a small framework to create highly configurable UIs for VoIP-telephony.
PJSIP (http://www.pjsip.org) is used as library for the SIP implementation and accessed via the available python-bindings of PJSIP.

Software Requirements:
    - Python 2.7
    - PJSIP with python-bindings:
    -- For Ubuntu you can use the following PPAs to install python-pjsip
    ---- https://launchpad.net/~dennis.guse/+archive/sip-tools
    ---- https://launchpad.net/~dennis.guse/+archive/sip-tools-beta
    - Python-xlib (for video support)

ATTENTION: The video-features are not available (yet) in the python-bindings from PJSIP (upstream).
Our patched sources for PJSIP are available here: https://github.com/dennisguse/pjsip/tree/python-video





Contents:
	1. Features
	2. Limitations

1. Features:
	1.  Calls (what else ;-) )
	2.  Easy to configure
	3. UI exchangable
	4.  Different ringtone support
	5.  Configuration of media parameters (see 4. II)
	6.  Presence support (incl. reason)
	7.  Debug support (store wave files of each call, store call statistics (using pjsip statistics),
	    store programs configuration on exit, manipulate pjsua log level)

2. Limitations:
	_____________________________________________________

	1. Program is currently limited to one call
	2. No video support (work in progress)
	3. No SIP/TLS support
	4. Codec not configurable (not yet)
	5. Wave-recording merges caller and callee (needs to be splited)
	6. One Account only


Icons are taken from here: http://commons.wikimedia.org/wiki/Category:SVG_telephone_icons