"""
    @author Leonardo Rossi Leão / Rodrigo de Oliveira Neto
    @create october, 1, 2020
"""

# Libraries
import time
from fileMonitor import FileMonitor

directory = "C:/Users/leona/Desktop/Iniciação Científica/Instrumentação do concreto/"
filename = "test.txt"

fileMonitor = FileMonitor(directory, filename)
fileMonitor.start() # Start the file monitoring
    
time.sleep(30)
    
fileMonitor.stop()