# Author: Andrea Irwin
# Class: CS 372-400 SP23
# Client-side of the chat/game programming project

# Citation for chat room environment set up:
# Date: 6/1/23
# Adapted from CS 372 Project 1 and from BioGem
# Source URL: https://www.biob.in/2018/04/simple-server-and-client-chat-using.html


import time
import socket


def setUpChat_Client():
    """
    Parameters: none
    Returns: none

    Sets up an instance of a client-side access to a chat with a server
    """
    print('\nWelcome to the [Game] Chat Room\n')
    print('Initializing....\n')
    time.sleep(1)

    # # Set up the client socket tand data that sends to server
    clientSocket = socket.socket()
    socketHost = 'localhost'
    ip = socket.gethostbyname(socketHost)
    print(socketHost, "(", ip, ")\n")

    # Select the address of the server to connect to in chat
    hostAddress = input(str('Enter server address: '))
    name = input(str('\nEnter your name: '))
    port = 3120

    # Bind the port number to this socket
    # Set up to connect to the serverr's chat room
    try: 
        print('\nTrying to connect to ', hostAddress, '(', port, ')\n')
        time.sleep(1)
        clientSocket.connect((hostAddress, port))
        print('Connected...\n')
    except:
        print('Error: socket failed to launch')

    # Put in client username and enter the chat room
    try:
        clientSocket.send(name.encode())
        username = clientSocket.recv(4096)
        username = username.decode()
        print(username, 'has joined the chat room\nEnter /q to exit chat room\n')
    except:
        print('Error: failed to connect')

    # As long as the chat room is open, the server and client take turns
    # sending messages back and forth
    while True:
        message = clientSocket.recv(4096)  # Server incoming messages
        message = message.decode()
        print(username, ':', message)
        message = input(str('Me : '))
        if message == '/q':
            message = 'Left chat room'
            clientSocket.send(message.encode())
            print('\n')
            break
        clientSocket.send(message.encode())  # Sending back a message to server

    # End the session once one of the hosts exits the chat
    clientSocket.close()


if __name__ == '__main__':
    setUpChat_Client()
