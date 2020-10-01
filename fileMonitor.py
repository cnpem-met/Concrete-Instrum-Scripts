"""
    @author Leonardo Rossi Leão / Rodrigo de Oliveira Neto
    @create october, 1, 2020
"""

# Libraries
import os
import time
import threading

def main():

    directory = "C:/Users/leona/Desktop/Iniciação Científica/Instrumentação do concreto/"
    filename = "test.txt"

    fileMonitor = FileMonitor(directory, filename)
    fileMonitor.start() #Start the file monitoring
    
    time.sleep(30)
    
    fileMonitor.stop()


class FileMonitor(threading.Thread):
    
    # Constructor Method 
    def __init__(self, directory, filename):
        super(FileMonitor, self).__init__()
        self.kill = threading.Event()
        self.directory = directory
        self.filename = filename
        
    # Get the file size
    def fileSize(self, directory, filename):
        return os.path.getsize(directory + filename)
    
    # Observe the indicated file size
    def run(self):
        print("Action: start file monitor")
        lastSize = self.fileSize(self.directory, self.filename)
        while not self.kill.is_set():
            size = self.fileSize(self.directory, self.filename)
            if lastSize != size:
                print("Size changed: %d kb -> %d kb" % (lastSize, size))
                lastSize = size
            time.sleep(1)
    
    # Stop the thread FileMonitor        
    def stop(self):
        print("Finalizando a Thread_Mseed")
        self.kill.set()
        
if __name__ == "__main__":
    main()