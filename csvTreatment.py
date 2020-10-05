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
    def __init__(self):
        super(CsvTreatment, self).__init__()
        self.kill = threading.Event()

    # Read the csv file
    def read(self, host, user, password, filename):
        mti = pd.read_csv("ftp://%s:%s@%s/%s" %
                            (self.user, self.password, self.host, self.filename), 
                            error_bad_lines=False, header=False)
        print("Action: file imported")
        return(mti)
    
    def separateLastData(self, rawData):
        captation = {}
        tableLine = rawData.tail(1).values[0]
        captation["date"] = tableLine[0]
        
    def run(self):
        while not self.kill.is_set():
            pass
        
    # Stop the thread CsvTreatment        
    def stop(self):
        print("Action: stop csv treatment")
        self.kill.set()