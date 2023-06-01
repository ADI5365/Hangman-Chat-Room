# Author: Andrea Irwin
# Class: CS 372-400 SP23
# Server-side of the chat/game programming project

# Citation for chat room environment set up:
# Date: 6/1/23
# Adapted from CS 372 Project 1 and from BioGem
# Source URL: https://www.biob.in/2018/04/simple-server-and-client-chat-using.html


import time
import socket


def setUpChat_Server():
    """
    Parameters: none
    Returns: none

    Sets up an instance of a server-side access to a chat with a client
    """
    print('\nWelcome to the [Game] chat room\n')
    print('Initializing....\n')
    time.sleep(1)

    # Set up the server socket and data to send to clients
    serverSocket = socket.socket()
    socketHost = socket.gethostname()
    ip = socket.gethostbyname(socketHost)
    serverPort = 3120
    
    # Bind the port number to this socket
    # Set up to listen for client requests to connect to the chat
    try:
        serverSocket.bind((socketHost, serverPort))
        print(socketHost, '(', ip, ')\n')
        clientName = input(str('Enter your name: '))

        serverSocket.listen(1)
        print('\nWaiting for client requests to connect...\n')
        connSocket, addr = serverSocket.accept()
        print('Received connection from ', addr[0], '(', addr[1], ')\n')
    except:
        print('Error: socket failed to launch')

    # When the client sets up the chat environment on their side 
    # the connection is established
    try:
        socketName = connSocket.recv(1024)
        socketName = socketName.decode()
        print(socketName,
              'has connected to the chat room\nEnter [e] to exit chat room\n')
        connSocket.send(clientName.encode())
    except:
        print('Error: client has failed to connect')

    # As long as the chat room is open, the server and client take turns
    # sending messages back and forth
    while True:
        message = input(str('Me : '))  
        if message == '[e]':
            message = 'Left chat room'
            connSocket.send(message.encode())
            print('\n')
            break
        connSocket.send(message.encode())  # Sending message to client
        message = connSocket.recv(1024)
        message = message.decode()
        print(socketName, ':', message)  # Client incoming messages


if __name__ == '__main__':
    setUpChat_Server()
