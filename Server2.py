import time, hashlib, select
from socket import AF_INET, socket, SOCK_STREAM
from threading import *

print("Imports succesful.")

print("Beginning server.")
server = socket(AF_INET, SOCK_STREAM) 

bufferSize = 1024

Host = ""
Port = 30008

server.bind((Host, Port))

server.listen(100)
print("Success.")

clientList = []


def CalculateAuthCode():
    authCode = int(int(time.time()) / int(10))
    authCode = hashlib.sha512(bytes(str(authCode), "utf8")).hexdigest()
    return str(authCode)

def ManageClient(connection, address, name):
    isAdmin = False
    setClientLabel(connection, "Referred to main thread")
    
    if "Alex" in name or "System" in name or "Server" in name or "server" in name or "system" in name or "Admin" in name or "Administrator" in name or "Root" in name or "admin" in name or "administrator" in name or "root" in name or "Admin" == name or "Administrator" == name or "Root" == name or "admin" == name or "administrator" == name or "root" == name:    
        connection.send(bytes("Enter authorisation", "utf8"))
        
        password = connection.recv(bufferSize).decode("utf8")

        setClientLabel(connection, "Processing")

        #I know it's insecure, this is for getting round the school system not evading MI5
        #                                                Hey, at least this part's secure!
        passwordHashed = hashlib.sha512(bytes((password + "289289289193819301"), "utf8")).hexdigest()

        if passwordHashed == "327c3ee9796088f90e9b5346165deb5d17a2e4112f6e57178be0646bb2d73478936cf4c0283ea78f43405a1bee04f72489d1ca146424a5c7b7288ea31ec4ea46":
            isAdmin = True
            connection.send(bytes("Your authorisation has been received.", "utf8"))
            print(str(name) + " has elevated to admin privileges")
            time.sleep(0.1)
            connection.send(bytes("Elevated to admin", "utf8"))

            setClientLabel(connection, "Elevated to admin")

        else:
            connection.send(bytes("Auth denied.", "utf8"))

            setClientLabel(connection, "Auth denied.")

            broadcast(bytes("A certain " + name + " attempted to become admin with an incorrect password!", "utf8"))
            
    print("Manage client for " + str(address) + " , by name " + name + " STARTED")
    
    while True:
        try:
            message = connection.recv(bufferSize).decode("utf8")

            if message:
                if message == "wipe -a":
                    if isAdmin == True:
                        authCode = CalculateAuthCode()
                        broadcast(bytes(("-- WIPE AUTHORISE --" + authCode), "utf8"))

                    else:
                        connection.send("You don't have permission to perform that command.")
                        setClientLabel(connection, "Permission denied.")

                elif message == "exit -a":
                    if isAdmin == True:
                        authCode = CalculateAuthCode()
                        broadcast(bytes(("-- EXIT AUTHORISE --" + authCode), "utf8"))

                    else:
                        connection.send("You don't have permission to perform that command.")
                        setClientLabel(connection, "Permission denied.")
                        
                print(name + ": " + message)
                broadcast(bytes((name + ": " + message), "utf8"))

            else:
                remove(connection)
                
        except:
            print("Error in manage client, attempting continue.")
            continue

def HandleStartingClient(connection, address):
    time.sleep(0.2)
    setClientLabel(connection, "Referred")
    clientList.append(connection)
    connection.send(bytes("Please enter your name", "utf8"))
    name = connection.recv(bufferSize).decode("utf8")
    connection.send(bytes("Received your name, " + name, "utf8"))
    
    Thread(target=ManageClient, args=(connection, address, name)).start()
        
    #nameDict.append(address, name)

def broadcast(message):
    for client in clientList:
        try:
            client.send(message)
        except:
            print("Error in broadcast.")
            client.close()
            remove(client)

def remove(connection):
    if connection in clientList:
        clientList.remove(connection)

def setClientLabel(connection, text):
    time.sleep(0.1)
    connection.send(bytes("[INTERNAL SET LABEL MESSAGE] " + text, "utf8"))
    time.sleep(0.1)
    
def Listen_for_clients():
    while True:
        connection, address = server.accept()
        setClientLabel(connection, "Referring to starting thread.")
        Thread(target=HandleStartingClient, args=(connection, address)).start()
        
Listen_for_clients()
server.close()
