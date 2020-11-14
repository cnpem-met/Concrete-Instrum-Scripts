"""
    @author: Leonardo Rossi Leão / Rodrigo de Oliveira Neto
    @create: october, 1, 2020
    @title: File monitor
"""

# Libraries
import time
import pprint
import threading
from ftplib import FTP
from datetime import datetime
from csvTreatment import CsvTreatment

class FileMonitor(threading.Thread):
    
    # Constructor Method 
    def __init__(self, host, port, user, password, filename):
        super(FileMonitor, self).__init__()
        self.kill = threading.Event()
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.filename = filename
        self.csvTreatment = CsvTreatment()
        self.csvTreatment.start()
        self.monitor = open("monitor.txt", "a")
        
        try:
            self.ftp = FTP()
            self.ftp.connect(self.host, self.port)
            self.ftp.login(self.user, self.password)
            self.ftp.voidcmd('TYPE I')
            self.recordAction("[%s] Action: FTP connected" % self.getDateTime())
        except:
            self.recordAction("[%s] Action: Error FTP not connected" % self.getDateTime())
            
    # Get the current date and time
    def getDateTime(self):
        now = datetime.now()
        return now.strftime("%d/%m/%Y %H:%M:%S")
    
    # Record the actions in monitor.txt
    def recordAction(self, text):
        self.monitor.write(text + "\n")
        self.monitor.flush()
        
    # Get the file size
    def fileSize(self):
        try:
            return self.ftp.size(self.filename)
        except:
            self.recordAction("[%s] FTP error" % self.getDateTime())
            self.ftp.close()
            self.ftp.connect(self.host, self.port)
            self.ftp.login(self.user, self.password)
            self.ftp.voidcmd('TYPE I')
            self.recordAction("[%s] FTP reconnected" % self.getDateTime())
            return self.ftp.size(self.filename)
    
    # Realize the file manipulation
    def fileManipulation(self):
        rawData = self.csvTreatment.read(self.host, self.port, self.user, self.password, self.filename)
        dataDictionary = self.csvTreatment.separateLastData(rawData)
        pprint.pprint(dataDictionary)
    
    # Observe the indicated file size
    def run(self):
        self.recordAction("[%s] Action: start file monitor" % self.getDateTime())
        lastSize = self.fileSize()
        while not self.kill.is_set():
            size = self.fileSize()
            if lastSize != size:
                self.recordAction("[%s] Size changed: %d kb -> %d kb" % (self.getDateTime(), lastSize, size))
                lastSize = size
                self.fileManipulation()
                    
            time.sleep(1)
    
    # Stop the thread FileMonitor        
    def stop(self):
        self.recordAction("[%s] Action: stop file monitor" % self.getDateTime())
        self.kill.set()
        self.csvTreatment.stop()
        self.monitor.close()