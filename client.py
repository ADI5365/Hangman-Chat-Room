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


class HangmanGameClient():
    """
    Class implementing the client side of a Hangman game chat room
    """

    def __init__(self):
        """
        Initializer method for the HangmanGameClient class
        """
        self.hostAddress = ''
        self.port = 3120
        self.username = ''
        self.clientSocket = None

    def setUpClientChat(self):
        """
        Parameters: none
        Returns: none

        Sets up an instance of client-side access to a chat with a server
        """
        print('\nWelcome to the Hangman Chat Room')
        time.sleep(1)

        # Set up the client socket and data that sends to server
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as setupSocket:
            setupSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.clientSocket = setupSocket
            self.launchSocket()
            self.username = self.serverConnect()
            self.chatRoom()

    def launchSocket(self):
        """
        Parameters: none
        Returns: none

        Launches the client's socket to connect to the server program
        """
        # Bind port number to the socket and connect to server's chat room
        try:
            self.hostAddress = input('Enter server address: ')
            self.clientSocket.connect((self.hostAddress, self.port))
            print('Connected to: ', self.hostAddress, 'on port: ', self.port, '\n')
        except:
            print('Error: socket failed to launch')

    def serverConnect(self):
        """
        Parameters: none
        Returns: none

        Completes setup with client's username for the chat room
        """
        # Put in client username and enter the chat room
        try:
            self.username = input('Enter your name: ')
            self.clientSocket.send(self.username.encode())

            print(dedent("""\
                Server has joined the chat room
                Enter /q to exit chat
                Please wait for input prompt before entering message to send
                Note: to start a game of hangman, type "play hangman"\n"""
            ))
        except:
            print('Error: failed to connect')

    def chatRoom(self):
        """
        Parameters: none
        Returns: none

        Opens a chat room environment between a server and client 
        from which a game of hangman can be launched
        """
        # As long as chat room is open, server and client send messages back and forth
        while True:

            # Receiving incoming messages from the server
            serverMessage = self.clientSocket.recv(4096)
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
                self.clientSocket.send(myMessage.encode())
                print('Shutting down \n')
                break
            self.clientSocket.send(myMessage.encode())  # Sending a message to server


if __name__ == '__main__':
    chatGame = HangmanGameClient()
    chatGame.setUpClientChat()
