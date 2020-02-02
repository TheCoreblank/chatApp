import time, hashlib, select, sys, string
from socket import AF_INET, socket, SOCK_STREAM
from threading import *
from random import *

#set out vars
DoRun = True

sleepTime = 0.1

print("Imports successful.")

print("Beginning server.")
server = socket(AF_INET, SOCK_STREAM) 

#can be changed, but seems OK for this kind of thing
bufferSize = 1024

Host = ""
Port = 34000

server.bind((Host, Port))

server.listen(1000)
print("Success.")

#holds socket objects, also known as black magic
clientList = []

#holds base usernames that have been set as banned
blocklist = []

#If someone's name is in this when the main loop checks, they will be removed from the list and kicked.
kicklist = []

#list of names connected
namelist = []

#contains name:message combinations
pendingPms = {}

#the client has a identical function. This stops my friends sending fake shutdown messages, pretending to be the server
def CalculateAuthCode():
    authCode = int(int(time.time()) / int(10))
    authCode = hashlib.sha512(bytes(str(authCode), "utf8")).hexdigest()
    return str(authCode)

#calculates the characters that go at the front of the names so the fuckery that happens when two people
#have the same name is as hard to trigger as possible. If a client disconnects non-cleanly, it often keeps
#their names in the names list, which is why we didn't filter that way. 
def CalculateNameAppend(length):
    alphabet = list("abcdefghijklmnopqrstuvwxyz1234567890!'£%^&*()@/#ABCDEFGHIJKLMNOPQRSTUVWXYZ")

    result = ""
    
    for i in range(0, length):
        result = result + choice(alphabet)

    return result

#main function!
def ManageClient(connection, address, name):
    errorCount = 0
    isAdmin = False
    try:
        setClientLabel(connection, "Referred to main thread")
        #Yes, I know I should have made an all lowercase copy of name and made it half as long.
        #checks if they should be made admin, then requests auth
        if "Alex" in name or "System" in name or "sudo" in name or "Sudo" in name or "Server" in name or "server" in name or "system" in name or "Admin" in name or "Administrator" in name or "Root" in name or "admin" in name or "administrator" in name or "root" in name or "Admin" == name or "Administrator" == name or "Root" == name or "admin" == name or "administrator" == name or "root" == name:    
            send(connection, "Due to your username, you need to elevate to admin")
            #the phrase "enter authorisation" triggers the client to change the input field to stars
            send(connection, "Enter authorisation")
            
            #receives their reply
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

        #when a PM is in the buffer, this handles it. It's in a different thread so it doesn't get blocked
        #by waiting for the client to reply
        Thread(target=HandlePMs, args=(connection, name)).start()

        send(connection, "You have now entered the main chatroom.")
        send(connection, "Your messages will now be broadcasted to all users.")

    except:
        print("Error in preperation for main thread loop. Passing to save")
        errorCount = errorCount + 1
        if errorCount > 10:
            try:
                send(connection, "Your error count has exceeded 10 and the")
                send(connection, "automated abort will shortly disconnect you")
                send(connection, "to protect the other threads and main server.")

            except:
                pass

            remove(connection, name)
        pass
    
    while True:
        try:
            #this isn't how it's intended, but it's there anyway incase someone uses it wrong
            if name in blocklist and isAdmin == False:
                send(connection, "You have been banned.")
                remove(connection, name)
                break

            #removes you if you are in the kicklist
            if name in kicklist and isAdmin == False:
                kicklist.remove(name)
                send(connection, "You have been kicked.")
                remove(connection, name)
                break

            try:
                message = connection.recv(bufferSize).decode("utf8")
            except:
                remove(connection, name)
                break

            if message:
                print(name + ": " + message)
                #if not command, send the message to everyone else-including the sender.
                if not "/status" in message and not "/broadcast" in message and not "/verify" in message and not "/ban" in message and not "/unban" in message and not "/pm" in message and not "/faketext" in message:
                    broadcast(bytes((name + ": " + message), "utf8"))

                #PM system
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
                
                #banning system
                if "/ban" in message:
                    if isAdmin == True:
                        blocklist.append(message[5:])
                        send(connection, ("Successfully added " + message[5:] + " to blocklist."))
                        print("Added " + message[5:] + " to the blocklist.")
                    else:
                        send(connection, "You don't have permission to run that command.")

                #unbanning system
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

                #kick system
                if "/kick" in message:
                    if isAdmin == True:
                        kicklist.append(message[6:])
                        send(connection, ("Successfully added " + message[6:] + " to kicklist."))
                        print("Added " + message[6:] + " to the kicklist.")
                    else:
                        send(connection, "You don't have permission to run that command.")


                #returns server info
                if "/status" in message:
                    time.sleep(0.2)
                    send(connection, "Port: " + str(Port))
                    time.sleep(0.2)
                    send(connection, "Your IP: " + str(address))
                    time.sleep(0.2)
                    send(connection, "Your name: " + name)
                    time.sleep(0.2)
                    send(connection, "Your Admin Status: " + str(isAdmin))

                #way to pretend you are the server
                if "/broadcast" in message:
                    if isAdmin == True:
                        broadcast(bytes((message[11:]), "utf8"))

                    else:
                        send(connection, "You don't have permission to run that command.")
                        
                #wipes everyone's screens. I'll go in depth in the auth for this one
                if message == "/wipe -a" or message == "/clear -a":
                    if isAdmin == True:
                        for i in range(1, 10):
                            time.sleep(0.2)
                            #get an auth code from the time (10 second change)
                            authCode = CalculateAuthCode()
                            #broadcast wipe authorise plus the auth code, 10 times just in case
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
                    #the client will print it's auth code too. This is more for diagnostics than security
                    send(connection, CalculateAuthCode())

                #I hope you can work out what this does...
                elif message == "/quit" or message == "/exit":
                    remove(connection, name)
                    break


                #lists everyone in namelist.
                elif message == "/here" or message == "/namelist" or message == "/users":
                    send(connection, str(len(namelist)) + " in list.")
                    time.sleep(0.4)
                    send(connection, "Users listed are necessarily online.")
                    for name in namelist:
                        time.sleep(0.4)
                        send(connection, name)

                #for remote shutdown, if the sockets module has a vuln somehow or all this talking
                #lark is getting on my nerves.
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
                                    DoRun = False
                                    sys.exit()

                                else:
                                    broadcast(bytes(("SERVER: " + name + " attempted remote server shutdown."), "utf8"))
                                    remove(connection, name)
                                    time.sleep(0.5)
                                    broadcast(bytes("SERVER: REQUEST DENIED, CLIENT REMOVED.", "utf8"))
                                    break
                                    
                    else:
                        broadcast(bytes(("SERVER: " + name + " attempted remote server shutdown.", "utf8")))
                        remove(connection, name)
                        break

            else:
                remove(connection, name)
                    
        except:
            print("Error in manage client, attempting continue.")
            errorCount = errorCount + 1
            if errorCount > 10:
                print("Error count has exceeded 10, aborting thread thread.")

                try:
                    send(connection, "Your error count has exceeded 10 and the")
                    send(connection, "automated abort will shortly disconnect you")
                    send(connection, "to protect the other threads and main server.")

                except:
                    pass

                remove(connection, name)
                break

            continue

    print("Exited main thread")

#PM handling thread. Pretty self explanatory.
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

#first thread assigned to someone. It gets name and refers to the main thread. It's partially here
#just cause that function is so long. I
def HandleStartingClient(connection, address):
    try:
        time.sleep(0.2)
        clientList.append(connection)
        setClientLabel(connection, "Name requested by server.")
        
        send(connection, "Please enter your name")
        
        name = connection.recv(bufferSize).decode("utf8")

        if name in blocklist:
            send(connection, "Username banned")

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

    except:
        print("Exitting starting thread due to error")
        try:
            send(connection, "An error has occurred. Please try to reconnect.")
        except:
            if name:
                remove(connection, name)
            else:
                remove(connection, "")
            pass

        if name:
            remove(connection, name)
        else:
            remove(connection, "")
        pass
    
#sends message to all clients
def broadcast(message):
    if DoRun == True:
        for client in clientList:
            try:
                client.send(message)
            except:
                print("Error in broadcast. Can not remove name, not given to function")
                client.close()
                remove(client, "")

#removes a connection
def remove(connection, name):
    connection.close()
    if connection in clientList:
        clientList.remove(connection)
        try:
            namelist.remove(name)
        except:
            print("Name not found when removing client")

#sets the label at the bottom of the client. 
def setClientLabel(connection, text):
    try:
        time.sleep(sleepTime)
        connection.send(bytes("[INTERNAL SET LABEL MESSAGE] " + text, "utf8"))
        time.sleep(sleepTime)
    except:
        print("Error in setting client label - - removing connection")
        remove(connection, "")
        pass
    
#passes off incoming connections to threads. For the only directly run function, it's pretty pathetic!
def Listen_for_clients():
    while True:
        connection, address = server.accept()
        setClientLabel(connection, "Referring to starting thread.")
        Thread(target=HandleStartingClient, args=(connection, address)).start()
        
Listen_for_clients()
server.close()
