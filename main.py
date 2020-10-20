"""
    @author: Leonardo Rossi Leão / Rodrigo de Oliveira Neto
    @create: october, 1, 2020
    @title: main
"""

# Libraries
import time
from fileMonitor import FileMonitor
from cryptography.fernet import Fernet

# Open the credentials
cred = open("credentials.txt").read()
decode = Fernet(cred[132:176])

# Connection FTP attributes
host = "13.94.133.22"
port = ""
user = decode.decrypt(str.encode(cred[264:364])).decode()
password = decode.decrypt(str.encode(cred[539:639])).decode()
filename = "MTI.csv"

host = "192.168.56.1"
port = 8021
user = decode.decrypt(str.encode(cred[264:364])).decode()
password = decode.decrypt(str.encode(cred[539:639])).decode()
filename = "MTI.csv"

# Instantiates a monitoring object
fileMonitor = FileMonitor(host, port, user, password, filename)
fileMonitor.start() # Start the file monitoring
    
time.sleep(100000)

fileMonitor.stop()
