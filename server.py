import socket
import threading
import sys
import random

#Individual Portfolio Assignment 1 - s348819 Wania Nabi

#Task 1: TCP Client
#Referring to Socket Bots.pdf for full elaboration of the assignment

#Needed data for connection
host = socket.gethostbyname(socket.gethostname())
port = 55555

#Start server by connecting the host and port
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

#Output when successfully connected
print("The chat server started on port " + str(port) + " and on host " + str(host) + "!")

#client list and nickname list
clients = []
nicknames = []

#Action suggestions sent to clients
action = random.choice(["work", "sleep", "play", "cry", "hug", "fight"])

#Broadcast method to send messages to all connected clients
def broadcast(message):
    for client in clients:
        client.send(message)


#Sends action suggestions to all connected clients
def send():
    message = "\n" + "Would you like to " + format(action) + " ?" + "\n"
    for client in clients:
        client.send(message.encode('ascii'))


#Handles messages coming from an individual client and then sending to all connected clients
def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f'{nickname} left the chat!'.encode('ascii'))
            nicknames.remove(nickname)
            break

#Main method
def receive():
    while True:
        #Accepting clients
        client, address = server.accept()
        print(f'Connected with {str(address)}')

        #'NICK' so client sets nickname - gets clients nickname and save to server list
        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        print(f'Client nickname is {nickname}!')
        broadcast(f'{nickname} joined the chat!'.encode('ascii'))

        #Number of connected clients
        nmbC = len(clients)

        #Makes it possible to connect to multiple clients
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

#Running receive (main) method
receive()
