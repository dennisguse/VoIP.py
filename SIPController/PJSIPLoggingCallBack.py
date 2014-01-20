#Callback-Handler for PJSIP.
#Forwards PJSIP log messages to python logging.
#PJSIP-logging-levels are forwarded as follows:
#
#PJSIP-Level -> Python-Level
#0: None		NOTSET (0)
#1:		CRITICAL (50)
#2:		WARNING (40)
#3:		ERROR (30)
#4:		INFO (20)
#5:		DEBUG (10)
#6: Strace	

import logging

logger = logging.getLogger("PJSIP")
def log(level,message,length):
    return
    if level <= 10:
        logger.debug(message)
    elif level <= 20:
        logger.info(message)
    elif level <= 30:
        logger.error(message)
    elif level <= 40:
        logger.warning(message)
    elif level <= 50:
        logger.critical(message)


