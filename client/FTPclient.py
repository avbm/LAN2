#!/usr/bin/python3
from socket import *
import os, sys
#from time import clock
if(len(sys.argv) > 1):
    serverName = sys.argv[1]
else:
    serverName = 'localhost'
if(len(sys.argv) > 2):
    serverPortBase = int(sys.argv[2])
else:
    serverPortBase = 13000
command = "getSocket"
clientSocket = socket(AF_INET,SOCK_STREAM)
clientSocket.connect((serverName, serverPortBase))
clientSocket.send(bytearray(command.encode("utf-8")))
#startTime = clock()
response = clientSocket.recv(1024)
response = response.decode("utf-8")
print("Session socket:"+response)
serverPort = int(response)
clientSocket.close()
while 1: 
    command = input('Enter Command:')   
    if command.lower() == "bye" or command.lower() == "quit":
        clientSocket = socket(AF_INET,SOCK_STREAM)
        clientSocket.connect((serverName, serverPort))
        command = "releaseSocket " + str(serverPort)
        clientSocket.send(bytearray(command.encode("utf-8")))
        break
    elif command.lower() == "server exit":
        clientSocket = socket(AF_INET,SOCK_STREAM)
        clientSocket.connect((serverName, serverPortBase))
        #command = "releaseSocket " + str(serverPort)
        clientSocket.send(bytearray(command.encode("utf-8")))
        break
    elif (command.split()[0]).lower() == "get":
        clientSocket = socket(AF_INET,SOCK_STREAM)
        clientSocket.connect((serverName, serverPort))
        myfileName = command.split()[1]
        clientSocket.send(bytearray("list".encode("utf-8")))
        fileList = clientSocket.recv(1024).decode("utf-8")
        #print(fileList)
        #print(fileList.split('\n  '))
        #print(" "+myfileName )
        #print(myfileName in fileList.split('\n  '))
        fileExists = "False"
        for x in fileList.split('\n  '):
            if x == myfileName:
                fileExists = "True"
        if fileExists == "True":
            clientSocket = socket(AF_INET,SOCK_STREAM)
            clientSocket.connect((serverName, serverPort))
            clientSocket.send(bytearray(command.encode("utf-8")))
            response = clientSocket.recv(1024)
            fileSize = int(response.split()[0].decode("utf-8"))
            #print(fileSize)
            #fileSize = int(fileSize.decode("utf-8"))
            #response = clientSocket.recv(fileSize)
            print(" Filesize at sender: " + str(fileSize) + " bytes")
            if (len(response.split()) > 1):
                    dataPosition = response.find(" StartFile".encode("utf-8"))
                    myfileContent = response[(dataPosition + len(" StartFile".encode("utf-8")) ):]
            else:
                myfileContent = clientSocket.recv(1024)
            while len(myfileContent) < fileSize:
                myfileContent += clientSocket.recv(1024)
                print(" "+str(int(len(myfileContent)*100.0/fileSize)) + "% Transfer Complete", end="\r")
            print(" File size recieved: " + str(len(myfileContent)) + " bytes")
            #myfileContent = response
            myfile = open(myfileName, 'wb')
            myfile.write(myfileContent)
            myfile.close()
            print("  File: "+myfileName+" received")
        else:
            print(" File "+myfileName+" not found at server")
    elif (command.split()[0]).lower() == "put":
        clientSocket = socket(AF_INET,SOCK_STREAM)
        clientSocket.connect((serverName, serverPort))
        myfileName = " ".join(command.split()[1:])#deletes the preceding command name
        #print(myfileName)
        if os.path.isfile(myfileName) == False:
            print(" File "+myfileName+" not found")
        else:
            myfile = open(myfileName, "rb")
            myfileContent = myfile.read()
            fileSize = len(myfileContent)
            clientSocket.send(bytearray((command+" "+str(fileSize)+" StartFile").encode("utf-8")))
            #clientSocket.send(bytearray((" "+str(fileSize)+" ").encode("utf-8")))
            clientSocket.send(bytearray(myfileContent))
            myfile.close()
            clientSocket.close()
            print("  File: "+myfileName+" sent")
    else:
        clientSocket = socket(AF_INET,SOCK_STREAM)
        clientSocket.connect((serverName, serverPort))
        clientSocket.send(bytearray(command.encode("utf-8")))
        #startTime = clock()
        response = clientSocket.recv(1024)
        response = response.decode("utf-8")
        print("Server response:"+response)
        clientSocket.close()
        if command == "server exit":
            break
print("Exited Client") 
