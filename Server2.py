import time, hashlib, select, sys, string
from socket import AF_INET, socket, SOCK_STREAM
from threading import *
from random import *
DoRun = True

sleepTime = 0.1

print("Imports succesful.")

print("Beginning server.")
server = socket(AF_INET, SOCK_STREAM) 

bufferSize = 1024

Host = ""
Port = 34001

server.bind((Host, Port))

server.listen(100)
print("Success.")

clientList = []

blocklist = []

kicklist = []

namelist = []

pendingPms = {}

def CalculateAuthCode():
    authCode = int(int(time.time()) / int(10))
    authCode = hashlib.sha512(bytes(str(authCode), "utf8")).hexdigest()
    return str(authCode)

def CalculateNameAppend(length):
    alphabet = list(string.printable) + list(string.printable.upper())

    result = ""
    
    for i in range(0, length):
        result = result + choice(alphabet)

    return result

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

            broadcast(bytes("Server: " + name + " got the admin password wrong.", "utf8"))

            remove(connection, name)
            
    print("Manage client for " + str(address) + " , by name " + name + " STARTED")

    send(connection, "Starting PM thread...")

    Thread(target=HandlePMs, args=(connection, name)).start()

    if name in pendingPms:
        time.sleep(5)

    send(connection, "You have now entered the main chatroom.")
    send(connection, "Your messages will now be broadcasted to all users.")
    
    while True:
        #try:
        if name in blocklist:
            send(connection, "You have been banned.")
            remove(connection, name)
            break

        if name in kicklist:
            kicklist.remove(name)
            send(connection, "You have been kicked.")
            remove(connection, name)
            break

        
        message = connection.recv(bufferSize).decode("utf8")

        if message:
            print(name + ": " + message)
            if not "/broadcast" in message and not "/verify" in message and not "/ban" in message and not "/unban" in message and not "/pm" in message and not "/faketext" in message:
                broadcast(bytes((name + ": " + message), "utf8"))

                
            if "/pm" in message:
                nameToPm = message[4:]

                if nameToPm in namelist:
                    send(connection, ("What do you want to send? Your next message is private"))
                    reply = connection.recv(bufferSize).decode("utf8")

                    pendingPms[nameToPm] = (name + " : " + reply)

                    send(connection, ("Added to buffer."))

                    SetLabelStatus("PM sent")

                else:
                    send(connection, ("This person isn't online right now"))
            
            if "/ban" in message:
                if isAdmin == True:
                    blocklist.append(message[5:])
                    send(connection, ("Successfully added " + message[5:] + " to blocklist."))
                    print("Added " + message[5:] + " to the blocklist.")
                else:
                    send(connection, "You don't have permission to run that command.")

            if "/unban" in message:
                DoSuccess = True
                if isAdmin == True:
                    try:
                        blocklist.remove(message[7:])
                    except:
                        send(connection, ("Error, it seems " + message[7:] + " is not banned."))
                        DoSuccess = False

                    if DoSuccess == True:
                        send(connection, ("Successfully removed " + message[7:] + " from blocklist."))
                    print("Removed " + message[7:] + " from the blocklist.")

                else:
                    send(connection, ("You don't have permission to run that command"))
                    broadcast(bytes(name + " attempted to unban " + message[5:]))


            if "/kick" in message:
                if isAdmin == True:
                    kicklist.append(message[6:])
                    send(connection, ("Successfully added " + message[6:] + " to kicklist."))
                    print("Added " + message[6:] + " to the kicklist.")
                else:
                    send(connection, "You don't have permission to run that command.")

            if "/broadcast" in message:
                if isAdmin == True:
                    broadcast(bytes((message[11:]), "utf8"))

                else:
                    send(connection, "You don't have permission to run that command.")
                    
            if message == "/wipe -a" or message == "/clear -a":
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


            elif message == "/faketext -a":
                if isAdmin == True:
                    for i in range(1, 10):
                        time.sleep(0.2)
                        authCode = CalculateAuthCode()
                        #uses this so if a teacher catches it mid wipe they don't see "authorise faketext"
                        broadcast(bytes(("-- AUTHORISE 42 --" + authCode), "utf8"))

            elif message == "/verify":
                send(connection, CalculateAuthCode())

            elif message == "/quit" or message == "/exit":
                remove(connection, name)
                break

            elif message == "/here" or message == "/namelist" or message == "/users":
                send(connection, str(len(namelist)) + " in list.")
                time.sleep(0.4)
                send(connection, "Users listed are necessarily online.")
                for name in namelist:
                    time.sleep(0.4)
                    send(connection, name)

            elif "sudo shutdown server" in message:
                print("Received sudo shutdown server")
                if isAdmin == True:
                    if CalculateAuthCode() == message[21:]:
                            send(connection, "This requires root priveleges, even higher than admin.")
                            send(connection, "Enter authorisation")
                            reply = connection.recv(bufferSize).decode("utf8")

                            passwordHashed = hashlib.sha512(bytes((reply + "84902340829048290480928409834902849028409284902890428390482304820948"), "utf8")).hexdigest()
                            
                            if passwordHashed == "ea600e271bcc401cba82320e3e53842cfd23b316aeaa6d41b73f3f5492dccff72bede7f03307eb00487e509c69a820129ccaaa38ef8160ff6d36987f67e67c1e":
                                broadcast(bytes("This server is shutting down by remote command", "utf8"))
                                print("Exiting due to sudo shutdown server command.")
                                sys.exit()
                                DoRun = False

                            else:
                                broadcast(bytes(("SERVER: " + name + " attempted remote server shutdown."), "utf8"))
                                remove(connection, name)
                                time.sleep(0.5)
                                broadcast(bytes("SERVER: REQUEST DENID, CLIENT REMOVED.", "utf8"))
                                break
                                
                else:
                    broadcast(bytes(("SERVER: " + name + " attempted remote server shutdown.", "utf8")))
                    blocklist.append(name)
                    remove(connection, name)
                    broadcast(bytes(("SERVER: REQUEST DENIED, USER BANNED.", "utf8")))
                    break

        else:
            remove(connection, name)
            
        #except:
        #    print("Error in manage client, attempting continue.")
        #    continue

    print("Exitted main thread")

def HandlePMs(connection, name):
    time.sleep(5)
    while True:
        if name in pendingPms:
            send(connection, "-----------------------------", False)
            send(connection, "Incoming private message: ", False)
            setClientLabel(connection, "PM has arrived.")
            send(connection, pendingPms[name], False)
            send(connection, "-----------------------------", False)

            del pendingPms[name]

        time.sleep(0.2)

def HandleStartingClient(connection, address):
    time.sleep(0.2)
    clientList.append(connection)
    setClientLabel(connection, "Name requested by server.")
    
    send(connection, "Please enter your name")
    
    name = connection.recv(bufferSize).decode("utf8")

    if name in blocklist:
        send(connection, "You have been banned.")
        send(connection, "Don't tell yourselfs you are all clever thinking")
        send(connection, "of using a new account; there's no way round it.")

    else:
        name = (CalculateNameAppend(4) + "-" + name)

        namelist.append(name)
    
        send(connection, ("Received your name, " + name))

        time.sleep(0.2)
        
        Thread(target=ManageClient, args=(connection, address, name)).start()
        
    #nameDict.append(address, name)

def send(connection, text, Show=True):
    if DoRun == True:
        text = str(text)
        time.sleep(sleepTime)
        if Show == True:
            connection.send(bytes("Server [PM]: " + text, "utf8"))
        else:
            connection.send(bytes(text, "utf8"))
            
        time.sleep(sleepTime)
        print("PM'd >> " + text)
    
def broadcast(message):
    if DoRun == True:
        for client in clientList:
            try:
                client.send(message)
            except:
                print("Error in broadcast.")
                client.close()
                remove(client, name)

def remove(connection, name):
    connection.close()
    if connection in clientList:
        clientList.remove(connection)
        namelist.remove(name)

def setClientLabel(connection, text):
    time.sleep(sleepTime)
    connection.send(bytes("[INTERNAL SET LABEL MESSAGE] " + text, "utf8"))
    time.sleep(sleepTime)
    
def Listen_for_clients():
    while True:
        connection, address = server.accept()
        setClientLabel(connection, "Referring to starting thread.")
        Thread(target=HandleStartingClient, args=(connection, address)).start()
        
Listen_for_clients()
server.close()
