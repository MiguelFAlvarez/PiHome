import socket
import os
from threading import Thread

TCP_IP = '192.168.1.113'
TCP_PORT = 5015
BUFFER_SIZE = 1024

statusData = [0] * 100

onCode = [5313843, 5313987, 5314307, 5315843, 5321987]
offCode = [5313852, 5313996, 5314316, 5315852, 5321996]

def clientThread(clientSocket, address):
    while True:
        command = clientSocket.recv(BUFFER_SIZE)
        if not data: break
	
		#Update command: Simply return status data to client
		if command[1]==0: #status update command
			clientSocket.send(statusData)
			
        #Light control command[1] = light command, command[2] = 0 toggle, 1 on, 2 off, command[3] = light number
		if command[1]==1: #light command
			if command[2]==0:	#toggle
				if statusData[command[3]+9]==0 #if off, turn on
					print ("Turning on light ", command[3])
					os.system("/home/pi/PiHome/rfoutlet/codesend %d" % onCode[command[3]-1])
					statusData[command[3]+9]=1
				if statusData[command[3]+9]==1 #if on, turn off
					print ("Turning off light ", command[3])
					os.system("/home/pi/PiHome/rfoutlet/codesend %d" % offCode[command[3]-1])
					statusData[command[3]+9]=0
			if command[2]==1:	#turn on
				print ("Turning on light ", command[3]+1)
				os.system("/home/pi/PiHome/rfoutlet/codesend %d" % onCode[command[3]-1])
				statusData[command[3]+9]=1
			if command[2]==2:	#turn off
				print ("Turning off light ", command[3]+1)
				os.system("/home/pi/PiHome/rfoutlet/codesend %d" % offCode[command[3]-1])
				statusData[command[3]+9]=0
        
			clientSocket.send(statusData)
		
		#Thermostat command: command[1] = thermstat cmd,  command[2] = 0 fan auto, 1 fan off,  command[3] = 0 cool, 1 off, 2 heat, command[4] = temp set 0-100
		if command[1]==2: #thermostat command
			statusData[1] = command[2]	#Fan status: fan auto, fan off
			statusData[2] = command[3]	#Temp mode: cool, off, heat
			statusData[3] = command[4]	#Set temp: 0-100 F
			clientSocket.send(statusData)
    clientSocket.close()
    print ("socket closed:", address)
    


                 
#Initialize status array
#Temp statusData[1:9] will be set to 0 if no sensor is used 

#Lights statusData[10:29] will be initialized to 0 (off)

#Doors statusData[30:49] will be set to 2 if not used


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

