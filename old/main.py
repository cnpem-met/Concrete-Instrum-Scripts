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
port = 21
user = decode.decrypt(str.encode(cred[264:364])).decode()
password = decode.decrypt(str.encode(cred[539:639])).decode()
filename = "MTI.csv"
print(password)

# Start the software
file = open("start.txt", "r");
start = bool(file.read())
file.close()

#host = "192.168.56.1"
#port = 8021
#user = decode.decrypt(str.encode(cred[264:364])).decode()
#password = decode.decrypt(str.encode(cred[539:639])).decode()
#filename = "MTI.csv"

if start == "banana":
    # Instantiates a monitoring object
    fileMonitor = FileMonitor(host, port, user, password, filename)
    fileMonitor.start() # Start the file monitoring
    while start == True:
        time.sleep(60)
        file = open("start.txt", "r");
        start = bool(int(file.read()))
        file.close()

print("Finishing")
fileMonitor.stop()
