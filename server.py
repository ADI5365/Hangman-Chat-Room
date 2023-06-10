# Author: Andrea Irwin
# Class: CS 372-400 SP23
# Server-side of the chat/game programming project

# Citation for chat room environment set up:
# Date: 6/1/23
# Adapted from CS 372 Project 1 and from Geeks for Geeks
# Source URL: https://www.geeksforgeeks.org/with-statement-in-python/

# Citation for basic hangman game outline:
# Date: 6/9/23
# Adapted from Python for Beginners
# Source URL: https://www.pythonforbeginners.com/code-snippets-source-code/game-hangman

# Citation for hangman art:
# Date: 6/10/23
# Used hangman art bank from chrishorton GitHub, in reverse order
# Source URL: https://gist.github.com/chrishorton/8510732aa9a80a03c829b09f12e20d9c


import socket
import time
from textwrap import dedent


class HangmanGameServer():
    """
    Class implementing the server side of a Hangman game chat room
    """

    def __init__(self):
        """
        Parameters: none
        Returns: none

        Initializer method for the HangmanGameServer class
        """

        # Global scope variables - chat
        self.socketHost = 'localhost'
        self.initialSocket = None
        self.connSocket = None
        self.port = 3120
        self.clientName = ''

        # Global scope variables - game
        self.secretWord = ''
        self.turns = 10
        self.guesses = ''
        self.notGuessed = 0
        self.HANGMANART = ['''
             +---+
             |   |
             O   |
            /|\  |
            / \  |
                 |
             =========''', '''
             +---+
             |   |
             O   |
            /|\  |
            /    |
                 |
             =========''', '''
             +---+
             |   |
             O   |
            /|\  |
                 |
                 |
             =========''', '''
             +---+
             |   |
             O   |
            /|   |
                 |
                 |
             =========''', '''
             +---+
             |   |
             O   |
             |   |
                 |
                 |
             =========''', '''
             +---+
             |   |
             O   |
                 |
                 |
                 |
             =========''', '''
             +---+
             |   |
                 |
                 |
                 |
                 |
             =========''', '''
             +---+
                 |
                 |
                 |
                 |
                 |
             =========''', '''
             
                 |
                 |
                 |
                 |
                 |
             =========''', '''
        
               
                 
                
                 
                 
             =========''']

    def setUpServerChat(self):
        """
        Parameters: none
        Returns: none

        Sets up an instance of server-side access to a chat with a client
        """
        print('\nWelcome to the Hangman Chat Room')
        time.sleep(1)

        # Set up socket connection with a client and launch the chat room
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as self.initialSocket:
            self.initialSocket.setsockopt(
                socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.connSocket = self.launchSocket()
            self.clientName = self.clientConnect()
            self.chatRoom()

    def launchSocket(self):
        """
        Parameters: none
        Returns: the new server-side socket

        Listens for client requests to connect on initial socket
        then launches a socket per each client
        """
        try:
            # Bind port number to the socket and listen for client requests to connect
            self.initialSocket.bind((self.socketHost, self.port))
            self.initialSocket.listen(1)
            print('\nServer listening on:',
                  self.socketHost, 'on port:', self.port)

            # Accepting a client request and setting up new separate socket
            newSocket, addr = self.initialSocket.accept()
            print('Received connection from (', addr[0], ',', addr[1], ')\n')
            return newSocket

        # Server's socket setup for the connection request failed to bind/connect
        except:
            print('Error: socket failed to launch')
            return

    def clientConnect(self):
        """
        Parameters: none
        Returns: the client's username

        Listens on the new socket for the client's username to complete connection
        """
        try:
            # When the client sets up the chat on their side, connection established
            newClient = self.connSocket.recv(4096)
            newClient = newClient.decode()
            print(newClient, 'has connected to the chat room\nEnter /q to exit')
            print('Please wait for input prompt before entering message to send\n')
            return newClient

        # Client failed to connect or exited before entering a username
        except:
            print('Error: client has failed to connect')
            return

    def chatRoom(self):
        """
        Parameters: none
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
                self.connSocket.send(myMessage.encode())
                print('Shutting down \n')
                break
            # Sending message to client
            self.connSocket.send(myMessage.encode())

            # Receiving incoming client messages
            clientMessage = self.connSocket.recv(4096)
            clientMessage = clientMessage.decode()
            print(self.clientName, ':', clientMessage)

            # If the client exits the session ends on the server side too
            if clientMessage == 'Left chat room':
                print('Shutting down \n')
                break
            elif clientMessage.lower() == 'play hangman':
                try:
                    self.hangmanGame()
                finally:
                    continue

    def hangmanGame(self):
        """
        Parameters: none
        Returns: none

        Implements the hangman game within the chat room when requested by the client
        """
        # Set up the game environment
        gameMsg = dedent("""\
            Welcome to a game of hangman!\n \
            Guess letters to fill in the secret word\n \
            You can make up to 10 wrong guesses\n \
            Type "1" to start""")
        self.connSocket.send(gameMsg.encode())
        self.secretWord = input('Choose a word for ' + self.clientName + ' to guess: ')
        self.validateSecretWord()

        # Print the word with all letters changed to empty slots for the client
        printStart = ''
        for char in self.secretWord:
            printStart += '_'
        sendTo = printStart + '\nHere are the currently revealed letters. Guess a letter\n'
        self.connSocket.send(sendTo.encode())
        print(self.clientName, 'is making a guess')

        self.gameLogic()

    def validateSecretWord(self):
        """
        Parameters: none
        Returns: none

        Validates the secret word to guess has only letters, no numbers or symbols
        """
        secretWordValid = False
        while secretWordValid is False:
            if not self.secretWord.isalpha():
                self.secretWord = input('Invalid. Please enter a word with only letters: ')
            else:
                secretWordValid = True

    def gameLogic(self):
        """
        Parameters: none
        Returns: none

        Implements the bulk of the game logic - making guesses, decrementing turns,
        and ending/exiting the game
        """
        while self.turns > 0:

            # Receiving the client's letter guess on each turn
            clientGuess = self.connSocket.recv(4096).decode()
            clientGuess = str(clientGuess)
            if clientGuess == '1':
                continue
            elif clientGuess == '/q':
                print(self.clientName, ' has left the chat room')
                break

            clientGuess = self.validateClientGuess(clientGuess)  # Validate client's guess

            print('Guessed letter: ', clientGuess, '\n')
            self.guesses += clientGuess
            self.checkGuess(clientGuess)  # Check to see if guess is correct or not, or game over

    def validateClientGuess(self, guess):
        """
        Parameters: one parameter, the client's latest guess
        Returns: none

        Validates client guess is a single letter, no numbers or symbols
        """
        guessIsValid = False
        while guessIsValid is False:
            if not guess.isalpha() or len(guess) > 1:
                invalidGuess = 'Invalid guess. Please enter a single alpha letter'
                self.connSocket.send(invalidGuess.encode())

                # Receive new guess until valid
                guess = self.connSocket.recv(4096).decode()  
                guess = str(guess)
            else:
                guessIsValid = True
                return guess

    def checkGuess(self, guess):
        """
        Parameters: one parameter, the client's latest guess
        Returns: none

        Takes the client's guess to check if the letter is in the secret word
        or not, and check if the game has been won or lost on the latest turn
        """
        # For wrong letters removes a turn and lets client know to guess again
        if guess not in self.secretWord:
            self.turns -= 1
            print(f"{self.clientName} has lost a turn. They have {self.turns} guesses left.\n")
            wrongLetter = f"Wrong letter. You have {self.turns} more guesses\n{self.HANGMANART[self.turns]}"
            self.connSocket.send(wrongLetter.encode())

            # When turns run out, game is over and returns to the chat room
            if self.turns == 0:
                print(self.clientName, ' has lost. Exiting to the chat room...')
                gameOver = f"You lose.\n{self.HANGMANART[self.turns]}\nExiting to the chat room..."
                self.connSocket.send(gameOver.encode())
                self.chatRoom()
        else:
            printWord = self.printWord()
            print(printWord)

            # The client has guessed all the letters - the game ends and returns to regular chat
            if self.notGuessed == 0 or '_' not in printWord:
                print(self.clientName, ' has won! Exiting to the chat room...')
                gameWon = 'You won! Exiting to the chat room...'
                self.connSocket.send(gameWon.encode())
                self.chatRoom()

    def printWord(self):
        """
        Parameters: none
        Returns: none

        Prints out the secretWord with revealed letters and underscores
        to represent unguessed letters
        """
        printedGuesses = ''

        # Printing out the whole word with unguessed letters blurred out
        for char in self.secretWord:
            if char in self.guesses:
                printedGuesses += char
            else:
                printedGuesses += '_'
                self.notGuessed += 1

        sendTo = printedGuesses + '\nHere are the currently revealed letters. Guess a letter\n'
        self.connSocket.send(sendTo.encode())
        return printedGuesses


if __name__ == '__main__':
    chatGame = HangmanGameServer()
    chatGame.setUpServerChat()
