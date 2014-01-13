import pjsua

def applyConfiguration(pjLib):
         pjLib.set_codec_priority("speex/16000/1", 130)
         pjLib.set_codec_priority("speex/8000/1", 129)

         pjLib.set_codec_priority("speex/32000/1", 128)
         pjLib.set_codec_priority("iLBC/8000/1", 128)
         pjLib.set_codec_priority("GSM/8000/1", 128)
         pjLib.set_codec_priority("PCMU/8000/1", 128)
         pjLib.set_codec_priority("PCMA/8000/1", 128)
         pjLib.set_codec_priority("G722/16000/1", 1)

         pjLib.set_codec_priority("L16/44100/1", 1)
         pjLib.set_codec_priority("L16/44100/2", 1)
         pjLib.set_codec_priority("L16/16000/1", 1)
         pjLib.set_codec_priority("L16/16000/2", 1)
         pjLib.set_codec_priority("L16/8000/1", 1)
         pjLib.set_codec_priority("L16/8000/2", 1)