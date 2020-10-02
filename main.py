"""
    @author: Leonardo Rossi Leão / Rodrigo de Oliveira Neto
    @create: october, 1, 2020
    @title: main
"""

# Libraries
import time
from fileMonitor import FileMonitor

host = "13.94.133.22"
user = "MTI"
password = "M*T*I123"
filename = "MTI.csv"

fileMonitor = FileMonitor(host, user, password, filename)
fileMonitor.start() # Start the file monitoring
    
time.sleep(30)
    
fileMonitor.stop()