# Author: Andrea Irwin
# Class: CS 372-400 SP23
# Client-side of the chat/game programming project

# Citation for chat room environment set up:
# Date: 6/1/23
# Adapted from CS 372 Project 1 server and client environment set up
# and from https://www.biob.in/2018/04/simple-server-and-client-chat-using.html


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
    client_socket = socket.socket()
    socket_host = socket.gethostname()
    ip = socket.gethostbyname(socket_host)
    print(socket_host, "(", ip, ")\n")

    # Select the address of the server to connect to in chat
    host_address = input(str('Enter server address: '))
    name = input(str('\nEnter your name: '))
    port = 3120

    # Bind the port number to this socket
    # Set up to connect to the serverr's chat room
    try: 
        print('\nTrying to connect to ', host_address, '(', port, ')\n')
        time.sleep(1)
        client_socket.connect((host_address, port))
        print('Connected...\n')
    except:
        print('Error: socket failed to launch')

    # Put in client username and enter the chat room
    try:
        client_socket.send(name.encode())
        user_name = client_socket.recv(1024)
        user_name = user_name.decode()
        print(user_name, 'has joined the chat room\nEnter [e] to exit chat room\n')
    except:
        print('Error: failed to connect')

    # As long as the chat room is open, the server and client take turns
    # sending messages back and forth
    while True:
        message = client_socket.recv(1024)  # Server incoming messages
        message = message.decode()
        print(user_name, ':', message)
        message = input(str('Me : '))
        if message == '[e]':
            message = 'Left chat room'
            client_socket.send(message.encode())
            print('\n')
            break
        client_socket.send(message.encode())  # Sending back a message to server


if __name__ == '__main__':
    setUpChat_Client()
