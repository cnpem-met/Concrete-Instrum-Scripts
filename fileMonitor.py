"""
    @author: Leonardo Rossi Leão / Rodrigo de Oliveira Neto
    @create: october, 1, 2020
    @title: File monitor
"""

# Libraries
import time
import threading
from ftplib import FTP
from csvTreatment import CsvTreatment

class FileMonitor(threading.Thread):
    
    # Constructor Method 
    def __init__(self, host, user, password, filename):
        super(FileMonitor, self).__init__()
        self.kill = threading.Event()
        self.ftp = FTP(host, user, password)
        self.filename = filename
        self.csvTreatment = CsvTreatment(self.ftp, filename)
        self.csvTreatment.start()
        
    # Get the file size
    def fileSize(self, filename):
        return self.ftp.size(filename)
    
    # Observe the indicated file size
    def run(self):
        print("Action: start file monitor")
        lastSize = self.fileSize(self.filename)
        mti = self.csvTreatment.read(self.ftp, self.filename)
        while not self.kill.is_set():
            size = self.fileSize(self.filename)
            if lastSize != size:
                print("Size changed: %d kb -> %d kb" % (lastSize, size))
                lastSize = size
            time.sleep(1)
    
    # Stop the thread FileMonitor        
    def stop(self):
        print("Action: stop file monitor")
        self.kill.set()
        self.csvTreatment.stop()