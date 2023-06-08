# Author: Andrea Irwin
# Class: CS 372-400 SP23
# Client-side of the chat/game programming project

# Citation for chat room environment set up:
# Date: 6/1/23
# Adapted from CS 372 Project 1 and from BioGem
# Source URL: https://www.biob.in/2018/04/simple-server-and-client-chat-using.html


import time
import socket


print('\nWelcome to the [Game] Chat Room')
print('Initializing....\n')
time.sleep(1)

# Set up the client socket and data that sends to server
with socket.socket() as clientSocket:
    socketHost = 'localhost'
    ip = socket.gethostbyname(socketHost)

    # Select the address of the server to connect to in chat
    hostAddress = input(str('Enter server address: '))
    name = input(str('Enter your name: '))
    port = 3120

    # Bind the port number to this socket
    # Set up to connect to the server's chat room
    try: 
        time.sleep(1)
        clientSocket.connect((hostAddress, port))
        print('Connected to: ', socketHost, 'on port: ', port, '\n')
    except:
        print('Error: socket failed to launch')

    # Put in client username and enter the chat room
    try:
        clientSocket.send(name.encode())
        print('Server has joined the chat room\nEnter /q to exit chat\n')
        print(
            'Wait for input prompt before entering message to send\nNote: to start a game of [game] type "play [game]"\n')
    except:
        print('Error: failed to connect')

    # As long as the chat room is open, the server and client take turns
    # sending messages back and forth
    while True:
        
        # Receiving incoming messages from the server
        serverMessage = clientSocket.recv(4096)
        serverMessage = serverMessage.decode()
        print('Server :', serverMessage)

        # If the server exits the session ends on the client side too
        if serverMessage == 'Left chat room':
            print('Shutting down \n')
            break
        myMessage = input(str('Enter message : '))

        # If client exits it sends a last message to the server to let them know
        if myMessage == '/q':
            myMessage = 'Left chat room'
            clientSocket.send(myMessage.encode())
            print('Shutting down \n')
            break
        clientSocket.send(myMessage.encode())  # Sending a message to server
