# Author: Andrea Irwin
# Class: CS 372-400 SP23
# Client-side of the chat/game programming project

# Citation for chat room environment set up:
# Date: 6/1/23
# Adapted from CS 372 Project 1 and from BioGem
# Source URL: https://www.biob.in/2018/04/simple-server-and-client-chat-using.html


import socket


def setUpClientChat():
    """
    Parameters: none
    Returns: none

    Sets up an instance of client-side access to a chat with a server
    """
    print('\nWelcome to the [Game] Chat Room')

    # Set up the client socket and data that sends to server
    with socket.socket() as clientSocket:
        socketHost = 'localhost'

        # Select the address of the server to connect to in chat
        hostAddress = input('Enter server address: ')
        name = input('Enter your name: ')
        port = 3120

        # Bind port number to the socket and connect to server's chat room
        try:
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

        chatRoom(clientSocket)

def chatRoom(clientSocket):

    # As long as chat room is open, server and client send messages back and forth
    while True:

        # Receiving incoming messages from the server
        serverMessage = clientSocket.recv(4096)
        serverMessage = serverMessage.decode()
        print('Server :', serverMessage)

        # If the server exits the session ends on the client side too
        if serverMessage == 'Left chat room':
            print('Shutting down \n')
            break
        myMessage = input('Enter message : ')

        # If client exits it sends a last message to the server to let them know
        if myMessage == '/q':
            myMessage = 'Left chat room'
            clientSocket.send(myMessage.encode())
            print('Shutting down \n')
            break
        clientSocket.send(myMessage.encode())  # Sending a message to server


if __name__ == '__main__':
    setUpClientChat()
