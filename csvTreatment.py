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
        teste = pd.read_csv("ftp://%s:%s@%s/%s" % (user, password, host, filename), error_bad_lines=False)
        print("File update!")
        
    def run(self):
        while not self.kill.is_set():
            running = "sim"
        
    # Stop the thread CsvTreatment        
    def stop(self):
        print("Action: stop csv treatment")
        self.kill.set()