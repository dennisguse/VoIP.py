import pjsua2

def applyConfiguration(endPoint):
         endPoint.codecSetPriority("speex/16000/1", 130)
         endPoint.codecSetPriority("speex/8000/1", 129)

         endPoint.codecSetPriority("speex/32000/1", 128)
         endPoint.codecSetPriority("iLBC/8000/1", 128)
         endPoint.codecSetPriority("GSM/8000/1", 128)
         endPoint.codecSetPriority("PCMU/8000/1", 128)
         endPoint.codecSetPriority("PCMA/8000/1", 128)
         endPoint.codecSetPriority("G722/16000/1", 1)

         endPoint.codecSetPriority("L16/44100/1", 1)
         endPoint.codecSetPriority("L16/44100/2", 1)
         endPoint.codecSetPriority("L16/16000/1", 1)
         endPoint.codecSetPriority("L16/16000/2", 1)
         endPoint.codecSetPriority("L16/8000/1", 1)
         endPoint.codecSetPriority("L16/8000/2", 1)