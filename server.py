# Author: Andrea Irwin
# Class: CS 372-400 SP23
# Server-side of the chat/game programming project

# Citation for chat room environment set up:
# Date: 6/1/23
# Adapted from CS 372 Project 1 and from Geeks for Geeks
# Source URL: https://www.geeksforgeeks.org/with-statement-in-python/


import socket
import time


def setUpServerChat():
    """
    Parameters: none
    Returns: none

    Sets up an instance of server-side access to a chat with a client
    """
    print('\nWelcome to the Hangman Chat Room')
    time.sleep(1)

    # Set up the server socket and data to send to clients
    with socket.socket() as serverSocket:
        try:
            socketHost = 'localhost'
            port = 3120

            # Bind port number to the socket and listen for client requests to connect
            serverSocket.bind((socketHost, port))
            serverSocket.listen(1)  # Listening for incoming client requests
            print('\nServer listening on:', socketHost, 'on port:', port)

            connSocket, addr = serverSocket.accept()
            print('Received connection from (', addr[0], ',', addr[1], ')\n')
        except:
            print('Error: socket failed to launch')

        # When the client sets up the chat on their side, connection established
        try:
            clientName = connSocket.recv(4096)
            clientName = clientName.decode()
            print(clientName, 'has connected to the chat room\nEnter /q to exit')
            print('Please wait for input prompt before entering message to send\n')
        except:
            print('Error: client has failed to connect')

        chatRoom(connSocket, clientName)


def chatRoom(connSocket, clientName):
    """
    Parameters: two parameters, server's socket and client's username
    Returns: none

    Opens a chat room environment between a server and client 
    from which a game of hangman can be launched
    """
    # As long as chat room is open, server and client send messages back and forth
    while True:
        myMessage = input('Enter message : ')

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
        print(clientName, ':', clientMessage)

        # If the client exits the session ends on the server side too
        if clientMessage == 'Left chat room':
            print('Shutting down \n')
            break
        elif clientMessage == 'play hangman':
            hangmanGame(connSocket)


def hangmanGame(connSocket):
    """
    Parameters: none
    Returns: none

    Implements the hangman game within the chat room when requested by the client
    """

    # Set up the game environment
    gameMsg = 'Welcome to a game of hangman!\n'
    connSocket.send(gameMsg.encode())
    secretWord = input('Choose a word for the client to guess: ')
    time.sleep(1)

    guesses = ''
    turns = 10
    printedGuesses = ''

    while turns > 0:
        notGuessed = 0

        # Printing out the whole word with unguessed letters blurred out
        for char in secretWord:
            if char in guesses:
                printedGuesses += char
            else:
                printedGuesses += '_'
                notGuessed += 1
        connSocket.send(printedGuesses)

        # The client has guessed all the letters - the game ends and returns to regular chat
        if notGuessed == 0:
            gameWon = 'You won! The game will now exit back to the chat room'
            connSocket.send(gameWon)
            print('The client has won! The game is over and is exiting to the chat room')
            break
        
        guessMsg = 'Guess a letter'
        connSocket.send(guessMsg).encode()

        # Receiving the client's letter guess on each turn
        clientGuess = connSocket.recv(4096)
        clientGuess = clientGuess.decode()

        if clientGuess == '\q':
            print('Client has left game')
            break
        guesses += clientGuess

        if clientGuess not in secretWord:
            turns -= 1
            wrongLetter = 'Wrong letter. You have', turns, 'more guesses'
            connSocket.send(wrongLetter)

            if turns == 0:
                gameOver = 'No more guesses left. You lose. The game will now exit back to the chat room'
                connSocket.send(gameOver)


if __name__ == '__main__':
    setUpServerChat()
