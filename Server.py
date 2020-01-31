from socket import AF_INET, socket, SOCK_STREAM
from threading import *
import hashlib, time, sys

Clients = {}
Addresses = {}

Host = ""
Port = 34000
Buffer_size = 1024
Address = (Host, Port)

Server = socket(AF_INET, SOCK_STREAM)
Server.bind(Address)

ToDelete = []

def CalculateAuthCode():
    authCode = int(int(time.time()) / int(10))
    authCode = hashlib.sha512(bytes(authCode, "utf8")).hexdigest()
    return authCode

def accept_incoming_connections():
    #sets up handling incoming clients
    while True:
        client, clientAddress = Server.accept()
        print(str(clientAddress) + " connected.")

        client.send(bytes("Greetings!", "utf8"))
        time.sleep(0.1)
        client.send(bytes("Enter {quit} to exit.", "utf8"))
        time.sleep(0.1)
        client.send(bytes("Please enter your name", "utf8"))
        
        #yes, weird syntax. It's an actual way to write to a dictionary
        Addresses[client] = clientAddress
        print("Beginning handling for client")
        Thread(target=handle_client, args=(client,)).start()
    
def handle_client(client):
    try:
        #handles client connections
        name = client.recv(Buffer_size).decode("utf8")

        isAdmin = False

        if "Admin" in name or "Administrator" in name or "Root" in name or "admin" in name or "administrator" in name or "root" in name or "Admin" == name or "Administrator" == name or "Root" == name or "admin" == name or "administrator" == name or "root" == name:
            client.send(bytes("Enter authorisation", "utf8"))

            #I honestly don't give a shit about password interception... it's a low security password, I just don't want people on github annoying me about "you left it in plaintext" or logging into some decades old account
            password = client.recv(Buffer_size).decode("utf8")

            password = hashlib.sha512(bytes(password, "utf8")).hexdigest()
            
            if password == "17ee1174ab412b3c5a85373aa6c7b73dd8dfdfaf8e5978ab55602f2f75fab21aae057f9c6649c9a7ab592f56be63766057043021f472036fe42c2b733f1953d5":
                isAdmin = True
                client.send(bytes("Your authorisation has been received.", "utf8"))
                time.sleep(0.1)
                print(str(name) + " has elevated to admin privileges")

            else:
                client.send(bytes("Authorisation denied; the code is incorrect.", "utf8"))
                time.sleep(0.1)
                client.send(bytes("Non authorised users are not allowed to be", "utf8"))
                time.sleep(0.1)
                client.send(bytes("called admin or have admin priveleges", "utf8"))
                time.sleep(0.1)
                client.send(bytes("Closing connection.", "utf8"))
                time.sleep(0.1)
                broadcast(bytes("A certain " + name + " attempted to log into the admin without auth!", "utf8"))
                print(str(name) + " attempted to elevate to admin and failed.")
        
        client.send(bytes(("Received your name! Welcome " + name), "utf8"))
        
        #welcomeMessage = "Welcome " + name + "!"
        #broadcast(bytes(welcomeMessage, "utf8"))
        
        message = name + " has joined!"
        broadcast(bytes(message, "utf8"))

        #yes, this again
        Clients[client] = name

    except BrokenPipeError:
        print("Broken pipe, closing")
        client.close()
        ToDelete.append(client)
        
    ##########main loop###############

    while True:
        try:
            incomingMessage = client.recv(Buffer_size)
            
            if not incomingMessage == bytes("{quit}", "utf8") or not incomingMessage == bytes("{wipe}", "utf8"):
                broadcast(incomingMessage, name+": ")

            else:
                client.close()
                del Clients[client]
                break


            if incomingMessage == bytes("Exit -a", "utf8"):
                if isAdmin == True:
                    time.sleep(0.2)
                    for i in range(1, 5):
                        authCode = int(int(time.time()) / int(10))
                        broadcast(bytes(("-- EXIT AUTHORISE --" + CalculateAuthCode(), "utf8")))
                        time.sleep(0.5)
                        
                else:
                    time.sleep(0.2)
                    broadcast(bytes(" - - - - - " + name + " just attempted to exit. No authorisation was supplied so it didn't happen.", "utf8"))

            if incomingMessage == bytes("Wipe -a", "utf8"):
                if isAdmin == True:
                    time.sleep(0.2)
                    for i in range(1, 5):
                        authCode = int(int(time.time()) / int(10))
                        broadcast(bytes(("-- WIPE AUTHORISE --" + CalculateAuthCode(), "utf8")))
                        time.sleep(0.5)
                        
                else:
                    time.sleep(0.2)
                    broadcast(bytes(" - - - - - " + name + " just attempted to wipe. No authorisation was supplied so it didn't happen.", "utf8"))


                    
        except:
            print("Broken pipe error")
            print("Closing connection to save server")
            client.close()
            ToDelete.append(client)
            break
        
    print("Connection closed to client " + name)
    for toDel in ToDelete:
        del Clients[toDel]

def broadcast(msg, prefix=""):
    #broadcasts to *all* clients
    for client in Clients:
        try:
            client.send(bytes(prefix, "utf8")+msg)
        except BrokenPipeError:
            print("Broken pipe, closing.")
            client.close()
            ToDelete.append(client)
            pass

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
