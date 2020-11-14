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
        
        try:
            self.ftp = FTP()
            self.ftp.connect(self.host, self.port)
            self.ftp.login(self.user, self.password)
            self.ftp.voidcmd('TYPE I')
            print("Action: FTP connected")
        except:
            print("Action: Error FTP not connected")
        
    # Get the file size
    def fileSize(self):
        try:
            return self.ftp.size(self.filename)
        except:
            print("FTP error")
            self.ftp.close()
            self.ftp.connect(self.host, self.port)
            self.ftp.login(self.user, self.password)
            self.ftp.voidcmd('TYPE I')
            print("FTP reconnected")
            return self.ftp.size(self.filename)
    
    # Realize the file manipulation
    def fileManipulation(self):
        rawData = self.csvTreatment.read(self.host, self.port, self.user, self.password, self.filename)
        dataDictionary = self.csvTreatment.separateLastData(rawData)
        pprint.pprint(dataDictionary)
    
    # Observe the indicated file size
    def run(self):
        print("Action: start file monitor")
        lastSize = self.fileSize()
        while not self.kill.is_set():
            size = self.fileSize()
            if lastSize != size:
                print("Size changed: %d kb -> %d kb" % (lastSize, size))
                lastSize = size
                self.fileManipulation()
                    
            time.sleep(1)
    
    # Stop the thread FileMonitor        
    def stop(self):
        print("Action: stop file monitor")
        self.kill.set()
        self.csvTreatment.stop()