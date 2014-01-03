import signal
import logging
from optparse import OptionParser
from Modules import ModuleHandler

def main():
    logging.basicConfig(filename='VoIPPy.log',level=logging.INFO)
    logging.getLogger().addHandler(logging.StreamHandler())

    parser = OptionParser()
    parser.add_option("-m", "--mode", action="store", dest="mode", required=True, help="The start mode (cli, stupid, standard), UI flag must be set", metavar="MODE")
    (options, self.args) = parser.parse_args()

    ModuleHandler(options.MODE)

if __name__ == '__main__':
    main()
