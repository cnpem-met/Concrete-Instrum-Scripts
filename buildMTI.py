# -*- coding: utf-8 -*-

"""
    @author: Leonardo Rossi Leão / Rodrigo de Oliveira Neto
    @create: october, 1, 2020
    @title: File monitor
"""

# Libraries
import os
import csv
import time
import pandas
import threading
from datetime import datetime
from epicsConcrete import EpicsServer
from calibration import Calibration as cal
from PvProperties import PvProperties as pvp

# Record the actions in monitor.txt
def recordAction(text):
    monitor = open("monitorRawData.txt", "a")
    monitor.write(text + "\n")
    monitor.close()
    
# Get the file size
def fileSize(filename):
    fileStats = os.stat(filename)
    return fileStats.st_size

# Get the current date and time
def getDateTime():
    now = datetime.now()
    return now.strftime("%d/%m/%Y %H:%M:%S")

# Update the Process Variables in Epics
def updateEpicsPV(muxId, channel, subChannel, value):
    pvName = pvp.pvName(muxId, channel, subChannel)
    if pvName != "Dis.":
        try:
            EpicsServer.driver.write(pvName, float(value))
        except:
            recordAction("[%s] Erro: value convertion in mux: %s, channel: %s, subchannel: %s" 
                         % (getDateTime(), muxId, channel, subChannel))
    
# Apply calibration curves in values
def convertValues(muxData):
    muxId = muxData[0]
    dataToConvert = muxData[4:]
    for i in range(len(dataToConvert)):
        sensor = cal.muxHeader["mux%d" % muxId][i//2]
        if "Dis" not in dataToConvert[i]:
            # Convertion to subchannel A
            if i % 2 == 0:
                if sensor == "PT100":
                    dataToConvert[i] = cal.convertPT100(dataToConvert[i])
                elif sensor == "VWS2100":
                    dataToConvert[i] = cal.convertVWS2100((i//2) + 1, dataToConvert[i])
                else:
                    dataToConvert[i] = cal.convertVWTS6000(muxId, (i//2) + 1, dataToConvert[i])
                updateEpicsPV(muxId, (i//2) + 1, "A", dataToConvert[i])
            # Convertion to subchannel B
            else:
                dataToConvert[i] = cal.convertChannelB(dataToConvert[i])
                updateEpicsPV(muxId, (i//2) + 1, "B", dataToConvert[i])
                
        
    return muxData[:4] + dataToConvert

# Convert the data received in a list
def fileManipulation(directory, filename):
    rawData = pandas.read_csv(directory + filename)
    # Start the array of mux data with Mux ID
    muxData = [int(filename.replace("DT", "").replace(".CSV", "").replace(".csv", ""))]
    lastData = rawData.tail(1).values[0][0].split(";|;")
    # Append the data in the muxData list
    for value in lastData:
        if ";" in value:
            for subvalue in value.split(";"):
                muxData.append(subvalue)
        else:
            muxData.append(value)
    return (muxData, convertValues(muxData))

muxAtivo = cal.MUXactivated

# Update MTI file with the data of acquisition
def updateMTI(acquisition, converted = False):
    listToSet = []
    muxIDs = list(acquisition.keys())
    muxIDs.sort()
    # Create a unique list from the dictionary
    for muxId in muxIDs:
        for value in acquisition[muxId][0]:
            listToSet.append(value)
    # Update the MTI file
    filename = "mti.csv"
    output = "[%s] Action: MTI updated" % getDateTime()
    if converted == True:
        filename = "mti_conv.csv"
        output = "[%s] Action: MTI Converted updated" % getDateTime()
    noHeader = False
    if os.path.exists(filename) == False:
        noHeader = True
    with open(filename, "a") as mtiFile:
        writer = csv.writer(mtiFile, dialect="excel", lineterminator = '\n')
        if noHeader == True:
            writer.writerow(cal.createHeader())
        writer.writerow(listToSet)
    recordAction(output)

class FileMonitor(threading.Thread):
    
    # Constructor Method 
    def __init__(self):
        super(FileMonitor, self).__init__()
        self.kill = threading.Event()
        self.server = EpicsServer()
        self.server.start()
        self.muxIds = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29]
        self.directory = "/usr/data/ftp-concrete/"
        #self.directory = "C:/Users/leonardo.leao/Desktop/usr/data/ftp-concrete/"
        self.acquisition = {}
        self.acquisitionConverted = {}
        
    # 
    def setDataToAcq(self, muxId, muxData, muxDataConverted):
        if muxId not in self.acquisition.keys():
            self.acquisition[muxId] = []
            self.acquisitionConverted[muxId] = []
        self.acquisition[muxId].append(muxData)
        self.acquisitionConverted[muxId].append(muxDataConverted)
    
    #
    def delFirstPosition(self):
        for muxId in self.muxIds:
            del self.acquisition[muxId][0]
            del self.acquisitionConverted[muxId][0]
            
    #
    def isComplete(self):
        for muxId in self.muxIds:
            if muxId in self.acquisition.keys():
                if len(self.acquisition[muxId]) == 0:
                    return False
            else:
                return False
        return True
        
    # Set values to acquisition attribute
    def setAcquisition(self, muxData, muxDataConverted):
        muxId = muxData[0]
        if self.isComplete():
            updateMTI(self.acquisition)
            updateMTI(self.acquisitionConverted, True)
            self.delFirstPosition()
        self.setDataToAcq(muxId, muxData, muxDataConverted)
    
    # Observe the indicated file size
    def run(self):
        recordAction("[%s] Action: start file monitor" % getDateTime())
        
        # Create a dictionary with the filenames e theirs sizes
        filesToWatch = {} 
        for filename in os.listdir(self.directory):
            if "DT" in filename:
                filesToWatch[filename] = fileSize(self.directory + filename)
        
        while not self.kill.is_set():
            
            for filename in filesToWatch:
                actualSize = fileSize(self.directory + filename)
                if actualSize != filesToWatch[filename]:
                    recordAction("[%s] Size changed in %s: %d kb -> %d kb" % (getDateTime(), filename, filesToWatch[filename], actualSize))
                    filesToWatch[filename] = actualSize
                    muxData, muxDataConverted = fileManipulation(self.directory, filename)
                    self.setAcquisition(muxData, muxDataConverted)
                    
            time.sleep(1)
    
    # Stop the thread FileMonitor        
    def stop(self):
        recordAction("[%s] Action: stop file monitor" % getDateTime())
        self.kill.set()
        
if __name__ == "__main__":
    threadFM = FileMonitor()
    threadFM.start()
