from PyQt4.QtCore import *
import logging

#Call Signals
CALL_CONNECT = 'connectCall'
CALL_HANGUP = 'hangupCurrentCall'
CALL_NUMBER = 'callNumber'
CALL_INCOMING = 'inCallSig'
CALL_INCOMING_CANCELED = 'inCallCanceled'
CALL_OUTGOING_CANCELED = 'outCallCanceled'

CALL_SHOW_VIDEO = 'callShowVideo'
CALL_SIGNAL_LEVEL_CHANGE = 'callSignalLevelChange'
CALL_SIGNAL_LEVEL_REQUEST = 'callSignalLevelRequest'
CALL_ESTABLISHED = 'callEstablished'
CALL_RETRY_VIDEO = 'retryVideo'

#Presence Signals
BUDDY_STATE_CHANGED = 'buddyStateChanged'
OWN_ONLINE_STATE_CHANGED = 'ownOnlineStateChanged'

#Modules Signals
MODULE_LOAD = 'module_load'
MODULE_ACTIVATE = 'module_activate'
MODULE_DISMISS = 'module_dismiss'

#Register State Signals
REGISTER_REQUEST_INITIAL_STATE = 'regInitialState'
REGISTER_STATE_CHANGE = 'regStateChanged'

#Misc
CLOSE = 'close'
STARTUP_ERROR = "startup_error"

def emit(sender, signalName,  param1 = None,  param2 = None):
    logging.getLogger("SIGNALS").info(sender.__class__.__name__ + " " + signalName)
    if param2:
        sender.emit(SIGNAL(signalName),  param1,  param2)
    elif param1:
        sender.emit(SIGNAL(signalName),  param1)
    else:
        sender.emit(SIGNAL(signalName))
