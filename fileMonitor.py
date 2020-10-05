"""
    @author: Leonardo Rossi Leão / Rodrigo de Oliveira Neto
    @create: october, 1, 2020
    @title: File monitor
"""

# Libraries
import time
import threading
import pandas as pd
from ftplib import FTP
from csvTreatment import CsvTreatment

class FileMonitor(threading.Thread):
    
    # Constructor Method 
    def __init__(self, host, user, password, filename):
        super(FileMonitor, self).__init__()
        self.kill = threading.Event()
        self.host = host
        self.user = user
        self.password = password
        self.filename = filename
        self.ftp = FTP(host, user, password)
        self.csvTreatment = CsvTreatment()
        self.csvTreatment.start()
        
    # Get the file size
    def fileSize(self):
        return self.ftp.size(self.filename)
    
    # Realize the file manipulation
    def fileManipulation(self):
        teste = pd.read_csv("ftp://%s:%s@%s/%s" %
                            (self.user, self.password, self.host, self.filename), 
                            error_bad_lines=False)
        print("Action: file imported")
    
    # Observe the indicated file size
    def run(self):
        print("Action: start file monitor")
        lastSize = self.fileSize()
        while not self.kill.is_set():
            size = self.fileSize()
            if lastSize != size:
                lastSize = size
                print("Size changed: %d kb -> %d kb" % (lastSize, size))
                self.fileManipulation()
            time.sleep(1)
    
    # Stop the thread FileMonitor        
    def stop(self):
        print("Action: stop file monitor")
        self.kill.set()
        self.csvTreatment.stop()