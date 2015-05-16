import socket
import os
from threading import Thread

TCP_IP = '192.168.1.113'
TCP_PORT = 5015
BUFFER_SIZE = 1024

onCode = [5313843, 5313987, 5314307, 5315843, 5321987]
offCode = [5313852, 5313996, 5314316, 5315852, 5321996]

def clientThread(clientSocket, address):
    while True:
        data = clientSocket.recv(BUFFER_SIZE)
        if not data: break

        #Light control data[1] = light command, data[2] = on or off, data[3] = which switch
        if data[1]==1 and data[2]==0:
            print ("Turning on light ", data[3]+1)
            os.system("/home/pi/PiHome/rfoutlet/codesend %d" % onCode[data[3]])
        if data[1]==1 and data[2]==1:
            print ("Turning off light ", data[3]+1)
            os.system("/home/pi/PiHome/rfoutlet/codesend %d" % offCode[data[3]])
        print ("received data:", data)
        #clientSocket.send("Turning off light ", data[3]+1)
    clientSocket.close()
    print ("socket closed:", address)
    


                 
# create an INET, STREAMing socket
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# bind the socket to a public host, and a well-known port
serverSocket.bind((TCP_IP, TCP_PORT))
# become a server socket
serverSocket.listen(5)

while True:
    print ("Waiting for Connection")
    # accept connections from outside
    (clientSocket, address) = serverSocket.accept()
    print ('Connection address:',  address)
    # now do something with the clientsocket
    # in this case, we'll pretend this is a threaded server
    #ct = clientThread(clientSocket, address)
    ct = Thread(target = clientThread, args = (clientSocket, address))
    ct.start()
serverSocket.close()

