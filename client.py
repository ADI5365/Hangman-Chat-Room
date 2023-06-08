# Author: Andrea Irwin
# Class: CS 372-400 SP23
# Client-side of the chat/game programming project

# Citation for chat room environment set up:
# Date: 6/1/23
# Adapted from CS 372 Project 1 and from Geeks for Geeks
# Source URL: https://www.geeksforgeeks.org/with-statement-in-python/

# Citation for textwrap:
# Date 6/8/23
# Information on dedent from textwrap taken from Python Morsels
# Source URL: https://www.pythonmorsels.com/dedent/


import time
import socket
from textwrap import dedent


def setUpClientChat():
    """
    Parameters: none
    Returns: none

    Sets up an instance of client-side access to a chat with a server
    """
    print('\nWelcome to the Hangman Chat Room')
    time.sleep(1)

    # Set up the client socket and data that sends to server
    with socket.socket() as clientSocket:
        try:
            hostAddress = input('Enter server address: ')
            port = 3120

            # Bind port number to the socket and connect to server's chat room
            clientSocket.connect((hostAddress, port))
            print('Connected to: ', hostAddress, 'on port: ', port, '\n')
        except:
            print('Error: socket failed to launch')

        # Put in client username and enter the chat room
        try:
            username = input('Enter your name: ')
            clientSocket.send(username.encode())

            print(dedent("""\
                Server has joined the chat room
                Enter /q to exit chat
                Please wait for input prompt before entering message to send
                Note: to start a game of hangman, type "play hangman"\n"""
            ))
        except:
            print('Error: failed to connect')

        chatRoom(clientSocket)


def chatRoom(clientSocket):
    """
    Parameters: one parameter, client's socket
    Returns: none

    Opens a chat room environment between a server and client 
    from which a game of hangman can be launched
    """
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
