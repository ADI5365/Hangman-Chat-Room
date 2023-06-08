# Author: Andrea Irwin
# Class: CS 372-400 SP23
# Server-side of the chat/game programming project

# Citation for chat room environment set up:
# Date: 6/1/23
# Adapted from CS 372 Project 1 and from BioGem
# Source URL: https://www.biob.in/2018/04/simple-server-and-client-chat-using.html


import time
import socket


print('\nWelcome to the [Game] chat room')
print('Initializing....')
time.sleep(1)

# Set up the server socket and data to send to clients
with socket.socket() as serverSocket:
    socketHost = 'localhost'
    ip = socket.gethostbyname(socketHost)
    port = 3120

    # Bind the port number to this socket
    # Set up to listen for client requests to connect to the chat
    try:
        serverSocket.bind((socketHost, port))
        serverSocket.listen(1)
        print('\nServer listening on:', socketHost, 'on port:', port)
        connSocket, addr = serverSocket.accept()
        print('Received connection from (', addr[0], ',', addr[1], ')\n')
    except:
        print('Error: socket failed to launch')

    # When the client sets up the chat environment on their side
    # the connection is established
    try:
        socketName = connSocket.recv(4096)
        socketName = socketName.decode()
        print(socketName, 'has connected to the chat room\nEnter /q to exit\n')
                
    except:
        print('Error: client has failed to connect')

    # As long as the chat room is open, the server and client take turns
    # sending messages back and forth
    while True:
        myMessage = input(str('Enter message : '))

        # If server exits it sends a last message to the client to let them know
        if myMessage == '/q':
            myMessage = 'Left chat room'
            connSocket.send(myMessage.encode())
            print('Shutting down \n')
            break
        connSocket.send(myMessage.encode())  # Sending message to client

        # Receiving incoming client messages
        clientMessage = connSocket.recv(4096)
        clientMessage = clientMessage.decode()
        print(socketName, ':', clientMessage)

        # If the client exits the session ends on the server side too
        if clientMessage == 'Left chat room':
            print('Shutting down \n')
            break
