"""
    @author Leonardo Rossi Leão / Rodrigo de Oliveira Neto
    @create october, 1, 2020
    @title: CSV functions
"""
# Libraries
import pandas as pd
import threading

class CsvTreatment(threading.Thread):
    
    # Constructor Method
    def __init__(self, ftp, filename):
        super(CsvTreatment, self).__init__()
        self.kill = threading.Event()
        self.ftp = ftp
        self.filename = filename

    # Read the csv file
    def read(self, ftp, filename):
        localfile = open(filename, 'wb')
        ftp.retrbinary('RETR ' + filename, localfile.write, 1024)
        localfile.close()
        print("File update!")
        
    def run(self):
        while not self.kill.is_set():
            running = "sim"
        
    # Stop the thread CsvTreatment        
    def stop(self):
        print("Action: stop csv treatment")
        self.kill.set()