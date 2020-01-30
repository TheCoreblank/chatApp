from socket import AF_INET, socket, SOCK_STREAM
from threading import *

Clients = {}
Addresses = {}

Host = ""
Port = 34000
Buffer_size = 1024
Address = (Host, Port)

Server = socket(AF_INET, SOCK_STREAM)
Server.bind(Address)

def accept_incoming_connections():
    #sets up handling incoming clients
    while True:
        client, clientAddress = Server.accept()
        print(str(clientAddress) + " connected.")
        
        client.send(bytes("Greetings!", "utf8"))
        client.send(bytes("Enter {exit} to exit.", "utf8"))
        client.send(bytes("Please enter your name", "utf8"))
        #yes, weird syntax. It's an actual way to write to a dictionary
        Addresses[client] = clientAddress

        Thread(target=handle_client, args=(client,)).start()

def handle_client(client):
    #handles client connections
    name = client.recv(Buffer_size).decode("utf8")
    client.send(bytes(("Received your name! Welcome " + name), "utf8"))
    
    #welcomeMessage = "Welcome " + name + "!"
    #broadcast(bytes(welcomeMessage, "utf8"))
    
    message = name + " has joined!"
    broadcast(bytes(message, "utf8"))

    #yes, this again
    Clients[client] = name
    
    while True:
        incomingMessage = client.recv(Buffer_size)
        
        if not incomingMessage == bytes("{quit}", "utf8"):
            broadcast(incomingMessage, name+": ")

        else:
            client.send(bytes("{quit}", "utf8"))
            client.close()
            del client[client]
            broadcast(bytes(name + " has left the chat. Byeee!"))
            break

    broadcast(bytes("Connection closed to client " + name, "utf8"))

def broadcast(msg, prefix=""):
    #broadcasts to *all* clients
    for client in Clients:
        client.send(bytes(prefix, "utf8")+msg)

    print("Broadcasted:      " + str(msg))

def main():
    Server.listen(500)
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    print("Closing")
    Server.close()

main()
