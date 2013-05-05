ESE 548 Project 2
====
Implementing an FTP server and client
Amod Mulay
id# 109017301

Notes:
1. These scripts are designed to be used with python3 (version 3.3.1) and will NOT work with python2. The scripts have been tested on a linux host. It is possible that some commands will not work on a windows host because of difference in path conventions.   
2. The server script assumes that it has maxClient no. of sockets free consecutively starting from serverPortBase
3. The "server exit" command is broken for the multi-threaded version of the scripts
4. The maximum number of supported clients can be specified by modifying the maxClient variable (default set to 5)
5. The current multi-threading implementation is very crude, inefficient and not secure 
6. username/password has been implemented but it is very crude. It only acts for authentication but is very poor in terms of security since passwords are stored and tranmitted in cleartext
7. All the extra credit work except seperate socket/port for data has been implemented
8. Data transfer takes place in 1KB buffers and hence might take some time for very large files.
9. The server and client scripts are located in thier respective directories so obviously you have to navigate(cd) to those directories to execute the scripts.

USAGE INSTRUCTIONS
1. ./FTPserver.py <port> #assumes that /usr/bin/python points to python3 binary
    or run "python3 TCPServer.py <port> ". <port> is an optional argument and defaults to 13000. eg. "./FTPserver.py 13010" 
2. "./FTPclient.py <server ip> <server port>" or "python3 TCPClient.py <server ip> <server port>". <server ip> and <sever port> are optional arguments and default to "localhost" and 13000 respectively. eg."./FTPclient.py 127.0.0.1 13010" OR "./FTPclient.py 127.0.0.1" which will use the default port 13000.
3. enter multiple commands as you wish. To see a list of supported commands type "help"
4. to exit client type "quit" or "bye"
5. you can try using the client script from multiple machines but the sever ip has to be specified( default is localhost)


List of supported commands
1. help : brings up help menu
2. server exit : exits both server and client processes
3. get <filename> : gets <filename> from server
4. put <filename> : puts <filename> to server
5. list : lists the contents of working directory at server
6. cd <path>: changes working directory to <path>
7. bye / quit : Either of the commands can be used to exit client

  