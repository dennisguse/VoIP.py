import signal
import logging
from optparse import OptionParser
from Modules import ModuleHandler

def main():
    signal.signal(signal.SIGINT, signal.SIG_DFL) #This one will enable your CTRL+C

    logging.basicConfig(filename='VoIPPy.log',level=logging.INFO)

    parser = OptionParser()
    parser.add_option("-m", "--mode", action="store", dest="mode", required=True, help="The start mode (cli, stupid, standard), UI flag must be set", metavar="MODE")
    (options, self.args) = parser.parse_args()

    logging.info("VoIPPy starting....")
    ModuleHandler(options.MODE)

    logging.info("Exiting program")

if __name__ == '__main__':
    main()
