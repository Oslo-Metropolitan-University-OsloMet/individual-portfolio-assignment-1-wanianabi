import socket
import threading
import random

#Individual Portfolio Assignment 1 - s348819 Wania Nabi

#Task 1: TCP Client
#Referring to Socket Bots.pdf for full elaboration of the assignment

#Conversation starter
print("Hello, let's get started!\nChoose one of the bots below:\n 1) Alice \n 2) Bob \n 3) Dora \n 4) Chuck\n"
      "(Want to leave? Write Goodbye to end the conversation)\n")

#Users input -chosen bot
nickname = input("\nWhich bot do you choose?")


#Define socket
host = socket.gethostbyname(socket.gethostname())
#Connect to host and port
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Only 4 different botnames (client names) accepted, other botnames will not connect to the server
if nickname == "alice" or nickname == "bob" or nickname == "dora" or nickname == "chuck":
    client.connect((host, 55555))  # connects the bot to the server
    print("Successfully connected!")
else:
    print("Try again! You have to choose one of the bots above.")


#Bot functions, imported from Socket Bots.pdf assignment p. 3
def alice(a, b = None):
    return "I think {} sounds great!".format(a + "ing")


def bob(a, b = None):
    if b is None:
        return "Not sure about {}. Don't i get a choice?".format(a + "ing")
    return "Sure, both {} and {} seems ok to me".format(a, b + "ing")


def dora(a, b = None):
    alternatives = ["coding", "singing", "sleeping", "fighting"]
    b = random.choice(alternatives)
    res = "Yea, {} is an option. Or we could do some {}.".format(a, b)
    return res, b


def chuck(a, b = None):
    action = a + "ing"
    bad_things = ["fighting", "bickering", "yelling", "complaining"]
    good_things = ["singing", "hugging", "playing", "working"]

    if action in bad_things:
        return "YESS! Time for {}".format(action)
    elif action in good_things:
        return "What? {} sucks. Not doing that.".format(action)
    return "I don't care!"


#This function will receive messages from the server, gives the suggested action and the bots response to it
def getAction():
    while True:
        data = client.recv(1024).decode('ascii')
        print(data)
        message = data.split()
        action = message[len(message) - 2]
        print("Alice: {}".format(alice(action)))
        print("Bob: {}".format(bob(action)))
        print("Dora: {}".format(dora(action)[0]))
        print("Chuck: {}".format(chuck(action)))
        break


#Gets botname and sends it to the server
def nick():
    message = client.recv(1024).decode('ascii')
    #Checks if the message to server is nickname, anything else gets printed out (do not need it)
    if message == 'NICK':
        client.send(nickname.encode('ascii'))
    else:
        print(message)


#Client receive data from the server
def receive():
    while True:
        try:
            nick()
            getAction()

        except:
            print("An error occurred!")
            client.close()
        break

#Runs a while loop to run input functions, asks for next message after sending the first one
def write():
    while True:
        message = f'{nickname}: {input("")}'
        client.send(message.encode('ascii'))


#Threads for being able to receive and write
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
