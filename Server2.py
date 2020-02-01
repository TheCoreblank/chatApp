import time, hashlib, select
from socket import AF_INET, socket, SOCK_STREAM
from threading import *

print("Imports succesful.")

print("Beginning server.")
server = socket(AF_INET, SOCK_STREAM) 

bufferSize = 1024

Host = ""
Port = 34000

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
        send(connection, "Due to your username, you need to elevate to admin")
        send(connection, "Enter authorisation")
        
        password = connection.recv(bufferSize).decode("utf8")

        setClientLabel(connection, "Processing")

        #I know it's insecure, this is for getting round the school system not evading MI5
        #                                                Hey, at least this part's secure!
        passwordHashed = hashlib.sha512(bytes((password + "289289289193819301"), "utf8")).hexdigest()

        if passwordHashed == "327c3ee9796088f90e9b5346165deb5d17a2e4112f6e57178be0646bb2d73478936cf4c0283ea78f43405a1bee04f72489d1ca146424a5c7b7288ea31ec4ea46":
            send(connection, "Your authorisation has been received.")
            print(str(name) + " has elevated to admin privileges")
            isAdmin = True
            time.sleep(0.1)
            send(connection, "Elevated to admin")

            setClientLabel(connection, "Elevated to admin")

        else:
            send(connection, "Authentication incorrect; elevation denied.")

            setClientLabel(connection, "Auth denied.")

            broadcast(bytes("Server: A certain " + name + " attempted to become admin with an incorrect password!", "utf8"))
            
    print("Manage client for " + str(address) + " , by name " + name + " STARTED")

    send(connection, "You have now entered the main chatroom.")
    send(connection, "All your messages will now be broadcasted to the chatroom.")
    
    while True:
        try:
            message = connection.recv(bufferSize).decode("utf8")

            if message:
                if message == "/wipe -a":
                    if isAdmin == True:
                        for i in range(1, 10):
                            time.sleep(0.2)
                            authCode = CalculateAuthCode()
                            broadcast(bytes(("-- WIPE AUTHORISE --" + authCode), "utf8"))

                    else:
                        send(connection, "You don't have permission to run that command.")
                        setClientLabel(connection, "Permission denied.")

                elif message == "/exit -a":
                    if isAdmin == True:
                        for i in range(1, 10):
                            time.sleep(0.2)
                            authCode = CalculateAuthCode()
                            broadcast(bytes(("-- EXIT AUTHORISE --" + authCode), "utf8"))

                    else:
                        send(connection, "You don't have permission to run that command.")
                        setClientLabel(connection, "Permission denied.")


                elif message == "/verify":
                    send(connection, CalculateAuthCode())
                        
                print(name + ": " + message)
                broadcast(bytes((name + ": " + message), "utf8"))

            else:
                remove(connection)
                
        except:
            print("Error in manage client, attempting continue.")
            continue


################################################## NOT MAIN, STARTING
#It's there cause when you are scanning the code this looks a lot like the main thread-hashing and while loops.

def HandleStartingClient(connection, address):
    time.sleep(0.2)
    setClientLabel(connection, "Referred")
    clientList.append(connection)
    time.sleep(0.2)
    setClientLabel(connection, "Name requested by server.")
    
    send(connection, "Please enter your name")
    
    name = connection.recv(bufferSize).decode("utf8")

    send(connection, ("Received your name, " + name))

    time.sleep(1)
    
    while True:
        send(connection, ("Please enter the chatroom password."))

        setClientLabel(connection, "Password required.")

        send(connection, ("Enter authorisation"))

        password = connection.recv(bufferSize).decode("utf8")

        passwordHashed = hashlib.sha512(bytes((password + "#kZTv/?#O{E+;`PWA78hP3`Q)PT*:1R>"), "utf8")).hexdigest()

        if passwordHashed == "16f6ab86817e7ce692242de2ce7c6fd8d236f70460bfe3987725fcb9748bfd15f7eb68cd0b05dc3aa89c6dba4405e6cb2a19a7f7bed0a373a3c0e3d00d03b78a":
            Thread(target=ManageClient, args=(connection, address, name)).start()
            break

        else:
            #fool teachers into thinking it's lost
            send(connection, ("Password wrong, try again in 5 seconds"))
            time.sleep(1)
            setClientLabel(connection, "5")
            time.sleep(1)
            setClientLabel(connection, "4")
            time.sleep(1)
            setClientLabel(connection, "3")
            time.sleep(1)
            setClientLabel(connection, "2")
            time.sleep(1)
            setClientLabel(connection, "1")
            
    #nameDict.append(address, name)

def send(connection, text):
    text = str(text)
    time.sleep(0.2)
    connection.send(bytes("Server [PM]: " + text, "utf8"))
    time.sleep(0.2)
    print("PM'd >> " + text)
    
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
    time.sleep(0.2)
    connection.send(bytes("[INTERNAL SET LABEL MESSAGE] " + text, "utf8"))
    time.sleep(0.2)
    
def Listen_for_clients():
    while True:
        connection, address = server.accept()
        setClientLabel(connection, "Referring to starting thread.")
        Thread(target=HandleStartingClient, args=(connection, address)).start()
        
Listen_for_clients()
server.close()
