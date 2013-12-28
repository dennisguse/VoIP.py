import signal
import logging
import Defines.MODES as Modes
from Modules.ModuleHandler import ModuleHandler


def main():
    logging.basicConfig(filename='VoIPPy.log',level=logging.INFO)
    logging.info("VoIPPy starting....")
    signal.signal(signal.SIGINT, signal.SIG_DFL) #This one will enable your CTRL+C

    ModuleHandler(Modes.SIMPLEVIDEO)

    logging.info("Exiting program")

if __name__ == '__main__':
    main()
