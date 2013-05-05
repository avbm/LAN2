#!/usr/bin/python3
from socket import *
import os, sys
import datetime
import threading

if(len(sys.argv) > 1):
    serverPort = int(sys.argv[1])
else:
    serverPort = 13000
serverDataPortStart = serverPort #set to zeroth port of node-servers
serverSocketBase = socket(AF_INET,SOCK_STREAM)
serverSocketBase.bind(('',serverPort))
serverSocketBase.listen(1)
maxClients = 5
clientSocketState = maxClients * [0]
#print(clientSocketState)
serverSocket = maxClients * [0]
for x in range(maxClients):
    serverSocket[x] = socket(AF_INET,SOCK_STREAM)
    serverSocket[x].bind(('',(serverDataPortStart+x+1)))
    serverSocket[x].listen(1) 
print("The server is ready to recieve")


def resolve_command(command, connectionSocket):
    connectionSocket = connectionSocket
    returnVal = 0
    if 1==1: #place holder in case while has to be implemented at some later time
        if command == "help":
            #enter command options and help menu here
            response = """This is a list of available server commands
            1. help : brings up this menu
            2. server exit : exits both server and client processes
            3. get <filename> : gets <filename> from server
            4. put <filename> : puts <filename> to server
            5. list : lists the contents of working directory at server
            6. bye / quit : Either of the commands can be used to exit client
            """
            connectionSocket.send(bytearray(response.encode("utf-8")))
            connectionSocket.close()
#getSocket
        elif command == "getSocket":
            response = str(clientSocketState.index(0) + 1 + serverDataPortStart)
            clientSocketState[clientSocketState.index(0)] = 1
            connectionSocket.send(bytearray(response.encode("utf-8")))
            connectionSocket.close()
#releaseSocket
        elif command.split()[0] == "releaseSocket":
            response = " ".join(command.split()[1:]) #deletes the preceding command name
            tempSocket = int(response)
            clientSocketState[tempSocket - 1 - serverDataPortStart] = 0  
            #response = "socket clear"
            #print(response)
            #connectionSocket.send(bytearray(response.encode("utf-8")))
            connectionSocket.close()
#server exit
        elif command == "server exit":
            response = "TCPServer exiting"
            connectionSocket.send(bytearray(response.encode("utf-8")))
            connectionSocket.close()
            returnVal = 1
#list
        elif (command.split()[0]).lower() == "list":
            if(len(command.split()) > 1):
                response = os.listdir(command.split()[1].lower())
            else:
                response = os.listdir('.')
            temp = ''
            #print(response)
            #for x in response:
            #    temp =  '\n  ' + temp + str(x) 
            temp = "\n  " + "\n  ".join(response)
            #print(temp)
            connectionSocket.send(bytearray(temp.encode("utf-8")))
            connectionSocket.close()
#cd
        elif (command.split()[0]).lower() == "cd":
            os.chdir(command.split()[1])
            response = "Working directory changed to: " + str(os.getcwd())
            connectionSocket.send(bytearray(response.encode("utf-8")))
            connectionSocket.close()
#get
        elif (command.split()[0]).lower() == "get":
            myfileName = command.split()[1] #deletes the preceding command name
            myfile = open(myfileName, "rb")
            response = myfile.read()
            fileSize = len(response)
            connectionSocket.send(bytearray((str(fileSize)+" StartFile").encode("utf-8")))
            connectionSocket.send(bytearray(response))
            myfile.close()
            connectionSocket.close()
            print("  File: "+myfileName+" sent")
#put
        elif type(command) != type("string"):
            if(command.split()[0].decode("utf-8")).lower() == "put":
                myfileName = command.split()[1].decode("utf-8")
                fileSize = command.split()[2].decode("utf-8")
                print(" Filesize at sender: " + str(fileSize) + " bytes")
                #print(fileSize)
                fileSize = int(fileSize)#.decode("utf-8"))
                #response = connectionSocket.recv(fileSize)
                if (len(command.split()) > 4):
                    dataPosition = command.find(" StartFile".encode("utf-8"))
                    myfileContent = command[(dataPosition + len(" StartFile".encode("utf-8")) ):]
                    #print(myfileContent)
                #myfileContent += response
                #else:
                #    myfileContent = response
                #    print("File size recieved: " + str(len(myfileContent)))
                myfileContent = connectionSocket.recv(1024)
                while len(myfileContent) < fileSize:
                    myfileContent += connectionSocket.recv(1024)
                    print(" "+str(int(len(myfileContent)*100.0/fileSize)) + "% Transfer Complete", end="\r")
                print(" File size recieved: " + str(len(myfileContent)) + " bytes")
                myfile = open(myfileName, 'wb')
                myfile.write(myfileContent)
                myfile.close()
                connectionSocket.close()
                print("  File: "+myfileName+" received")
        else:
            response = "Unknown Command"
            connectionSocket.send(bytearray(response.encode("utf-8")))
            connectionSocket.close()
    return returnVal 

class serverThread (threading.Thread):
    def __init__(self, threadID):
        self.threadID = threadID
        threading.Thread.__init__(self)
    def run(self):
        while 1:
            #workingDir = os.getcwd()
            connectionSocket, addr = serverSocket[self.threadID].accept()
            command = connectionSocket.recv(1024)
            print('Thread Recieved: ', command)
            #print(len(command.split()))
            if(command.split()[0].decode("utf-8")).lower() != "put": #skips decode if command is put
                command = command.decode("utf-8")
            #print(command)
            returnVal = resolve_command(command,connectionSocket)
            if(returnVal==1):
                break


#initializing threads for clients
for x in range(maxClients):
    temp = serverThread(x)
    temp.start()



while 1:
    connectionSocket, addr = serverSocketBase.accept()
    command = connectionSocket.recv(1024)
    print('Main Recieved: ', command)
    command = command.decode("utf-8")
    #print(command)
    returnVal = resolve_command(command,connectionSocket)
    if(returnVal==1):
        break
for x in range(maxClients):
    serverSocket[x].close()
serverSocketBase.close()


