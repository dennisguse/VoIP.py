#!/usr/bin/python

import signal
import logging
from Modules.ModuleHandler import ModuleHandler

def main():
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(name)s.%(funcName)s():%(lineno)s | %(message)s', datefmt='%H:%M:%S',)
    signal.signal(signal.SIGINT, signal.SIG_DFL) #This one will enable your CTRL+C
    ModuleHandler("simpleVideo2")

if __name__ == '__main__':
    main()
