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
        # Use pandas to read a csv file from an FTP server
        mti = pd.read_csv("ftp://%s:%s@%s/%s" %
                            (self.user, self.password, self.host, self.filename), 
                            error_bad_lines=False, header=False)
        print("Action: file imported")
        return(mti)
    
    # Separate data into a dictionary
    def newMux(mux):
        channel = 1 # Variable to control de number of channels
        # Initialize mux dictionary with basic informations
        muxDictionary = {
            "Id": mux[0],
            "Datetime": mux[1],
            "Volt": mux[2],
            "Temperature": mux[3]} 
        # Scroll the channels and set the info into the dictionary
        for i in range(4, len(mux)):
            if i % 2 == 0:
                muxDictionary["Ch%d%s" % (channel, "A")] = mux[i]
            else:
                muxDictionary["Ch%d%s" % (channel, "B")] = mux[i]
                channel += 1
        print(muxDictionary)
            
    
    # Get the last line of csv and separate data into a dictionary
    def separateLastData(self, rawData):
        mux = []
        setId = 0
        tableLine = rawData.tail(1).values[0] 
        # Scroll the vector looking for a new mux
        for i in range(len(tableLine) - 1):
            if ":" in str(tableLine[i]): # Identify a datetime cell
                if setId != 0:
                    self.newMux(mux)
                mux = []; setId += 1
                mux.append(setId); mux.append(tableLine[i])
                print("Action: reading a new mux [%s]" % str(tableLine[i]))
            else:
                mux.append(tableLine[i])
                
            
        self.newMux(tableLine)
        
    def run(self):
        while not self.kill.is_set():
            pass
        
    # Stop the thread CsvTreatment        
    def stop(self):
        print("Action: stop csv treatment")
        self.kill.set()