import logging

class AbstractModule(object):
    
    def hasSignalsToRegister(self):
        logging.info("UI Module has no signals to register")
        return False
    
    def getSignals(self):
        logging.info("UI Module has no predifined signals")
        return None
        
    def start(self):
        raise NotImplementedError
        
    def dismiss(self):
        raise NotImplementedError
        
