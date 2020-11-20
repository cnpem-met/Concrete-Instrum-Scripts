"""
    @author Leonardo Rossi Leão / Rodrigo de Oliveira Neto
    @create november, 09, 2020
    @title: EPICS
"""

import threading
from datetime import datetime
from pcaspy import SimpleServer, Driver
from PvProperties import PvProperties as pvp

# Get the current date and time
def getDateTime():
    now = datetime.now()
    return now.strftime("%d/%m/%Y %H:%M:%S")

# Record the actions in monitor.txt
def recordAction(text):
    monitor = open("monitor.txt", "a")
    monitor.write(text + "\n")
    monitor.close()      

class EpicsDriver(Driver):
    def _init_(self):
        super(EpicsDriver, self)._init_()
        
    def write(self, reason, value):
        self.setParam(reason, value) 
        
    def read(self, reason):
        return self.getParam(reason)
        
class EpicsServer(threading.Thread):
    
    driver = None
    
    def _init_(self):
        super(EpicsServer, self)._init_()
        
    def run(self):
        server = SimpleServer()
        server.createPV("CONCRETE:", pvp.pvdb())
        EpicsServer.driver = EpicsDriver()
        recordAction("[%s] Action: EPICS server and driver started" % getDateTime())
        while True:
            server.process(0.1)