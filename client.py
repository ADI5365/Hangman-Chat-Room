# Author: Andrea Irwin
# Class: CS 372-400 SP23
# Client-side of the chat/game programming project


import time
import socket


def setUpChat_Client():
    """
    Parameters: none
    Returns: none

    Sets up an instance of a client-side access to a chat with a server
    """
    print("\nWelcome to the [Game] Chat Room\n")
    print("Initialising....\n")
    time.sleep(1)

    client_socket = socket.socket()
    socket_host = socket.gethostname()
    ip = socket.gethostbyname(socket_host)
    print(socket_host, "(", ip, ")\n")

    host_address = input(str("Enter server address: "))
    name = input(str("\nEnter your name: "))
    port = 4230
    print("\nTrying to connect to ", host_address, "(", port, ")\n")

    time.sleep(1)
    client_socket.connect((host_address, port))
    print("Connected...\n")

    client_socket.send(name.encode())
    user_name = client_socket.recv(4096)
    user_name = user_name.decode()
    print(user_name, "has joined the chat room\nEnter [e] to exit chat room\n")

    while True:
        message = client_socket.recv(4096)
        message = message.decode()
        print(user_name, ":", message)
        message = input(str("Me : "))
        if message == "[e]":
            message = "Left chat room!"
            client_socket.send(message.encode())
            print("\n")
            break
        client_socket.send(message.encode())


if __name__ == '__main__':
    setUpChat_Client()
