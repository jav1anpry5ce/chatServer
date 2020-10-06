import socket
import threading
from threading import Timer
from DataEncrypt import DataEncrypt
data = DataEncrypt()

# Connection Data
host = 'localhost'
port = 5050

# Starting Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

# Lists For Clients and Their Nicknames
clients = []
nicknames = []

# Sending Messages To All Connected Clients
def broadcast(message):
    for client in clients:
        client.send(data.encryptData(message))

# Handling Messages From Clients
def handle(client):
    while True:
        try:
            # Check to see if client left chat
            message = client.recv(1024)
            message = data.decryptData(message)
            if message == "\\dis":
                index = clients.index(client)
                clients.remove(client)
                client.close()
                nickname = nicknames[index]
                broadcast('{} left!'.format(nickname))
                print('{} left!'.format(nickname))
                nicknames.remove(nickname)
                break
            # Broadcast Messages
            else:
                broadcast(message)
        except:
            # Removing And Closing Clients
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast('{} left!'.format(nickname))
            nicknames.remove(nickname)
            break

# Receiving / Listening Function
def receive():
    while True:
        try:
            # Accept Connection
            client, address = server.accept()
            print("Connected from {}".format(str(address)))

            # Request And Store Nickname
            client.send(data.encryptData("NICK"))
            nickname = client.recv(1024)
            nickname = data.decryptData(nickname)
            nicknames.append(nickname)
            clients.append(client)

            # Print And Broadcast Nickname
            print("Using the nickname is {}".format(nickname))
            client.send(data.encryptData("You are now connected to server!"))
            broadcast("{} joined!".format(nickname))

            # Start Handling Thread For Client
            thread = threading.Thread(target=handle, args=(client,))
            thread.start()
        except:
            print("Host couldn't connect!")

print(f"Server is listing on ip address: {host} with port: {port}")
receive()
