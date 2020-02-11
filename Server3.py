import time, hashlib, sys, string
from socket import AF_INET, socket, SOCK_STREAM
from threading import *
import hashlib

class LowLevelCommunications():
    #for before the client is logged in
    def Encode(Text):
        try:
            Text = str(Text)
            PrintLog("Encoding: " + Text)
            return bytes(Text, 'utf8')
        except:
            PrintLog("Error encoding")

    def SendServerPM(connection, text):
        time.sleep(0.2)
        text = str(text)
        try:
            PrintLog("Sending low level message PM")
            ToSend = "[SERVER INTERNAL-LOW LEVEL-PM MESSAGE]" + text
            connection.send(LowLevelCommunications.Encode(ToSend))
        except:
            PrintLog("Error sending low level message PM")
            connection.close()

        time.sleep(0.2)
        

    def SendInternalMessage(connection, text):
        time.sleep(0.2)
        text = str(text)
        try:
            PrintLog("Sending low level internal message")
            ToSend = "[SERVER INTERNAL-LOW LEVEL-INTERNAL]" + text
            connection.send(LowLevelCommunications.Encode(ToSend))

        except:
            PrintLog("Error sending low level internal PM, exiting")
            connection.close()
            pass

        time.sleep(0.2)

    
class HighLevelCommunications():
    def PrivateMessageFromServer(Username, Text):
        hadError = False
        Text = str(Text)
        Username = str(Username)
        PrintLog("Sending to " + Username + " : " + Text)
        try:
            Connection = Accounts.GetAccountData(Username, "ConnectionObject")
        except:
            PrintLog("Could not get connection for Server PM name, passing and not sending")
            hadError = True
            pass

        try:
            if hadError == False:
                toSend = "[SERVER INTERNAL-PM MESSAGE]" + Text
                Connection.send(HighLevelCommunications.Encode(toSend))
            else:
                PrintLog("Had error earlier, not sending")
        except:
            PrintLog("Error sending PM")
            Accounts.IncreaseErrorCount(Username)
    
    def Broadcast(Text):
        Text = str(Text)
        #try:
        for account in Accounts.AccountList:
            try:
                if Accounts.GetAccountDataFromObject(account, "isOnline") == True:
                    Connection = Accounts.GetAccountDataFromObject(account, "ConnectionObject")
                    ToSend = HighLevelCommunications.Encode("[SERVER INTERNAL-BROADCAST]" + str(Text))
                    Connection.send(ToSend)
            except:
                PrintLog("Error in broadcast : loop")
                try:
                    Username = Accounts.GetAccountDataFromObject(account, "Username")
                    Accounts.IncreaseErrorCount(Username)
                except:
                    pass
                continue

        PrintLog("Broadcasted " + Text)
        #except:
        #    PrintLog("Error in broadcast")
        #    pass


    def InternalMessage(Username, Text):
        hadError = False
        Text = str(Text)
        Username = str(Username)
        PrintLog("Sending internal message to " + Username + " : " + Text)
        try:
            Connection = Accounts.GetAccountData(Username, ConnectionObject)
        except:
            PrintLog("Could not get connection for internal message name, passing and not sending")
            hadError = True
            Accounts.IncreaseErrorCount(Username)
            pass

        try:
            if hadError == False:
                toSend = "[SERVER INTERNAL-INTERNAL]" + Text
                Connection.send(HighLevelCommunications.Encode(toSend))
            else:
                PrintLog("Had error earlier, not sending")
        except:
            PrintLog("Error sending internal message")
            Accounts.IncreaseErrorCount(Username)

    def Encode(Text):
        try:
            Text = str(Text)
            PrintLog("Encoding: " + Text)
            return bytes(Text, 'utf8')
        except:
            PrintLog("Error encoding")

class Accounts():
    AccountList = []
    #Account specifications:
    #A example account
    #{
    #    Username : 'Alex'
    #    Password : 'sjfhjsbfh9w8fn028h02n etc',
    #    PendingPms : {Sender: 'Luke', Message : 'Hello!'},
    #    isAdmin : True,
    #    isOnline : True,
    #    ConnectionObject: {IP : 127.0.0.1, PROTOCOL : TCP, NOTES : 'I am not copying an entire sockets connection object'}
    #}

    def ReadAccountList():
        a = 1
        #if I ever reimplement, I have the calls already done

    def PopulateFile():
        SaveFile = open("accounts", "wb")
        toDump = [{"Username" : "Placeholder-jshgfiowjfiowfo2nwfo"}]

    def NewAccount(UsernameInput, PasswordInput, isAdminInput):
        try:
            UsernameInput = str(UsernameInput)
            PasswordInput = str(PasswordInput)
            isAdminInput = str(isAdminInput)

            #Accounts.ReadAccountList()
            Accounts.AccountList.append({'Username' : UsernameInput, 'Password' : PasswordInput, 'isAdmin' : isAdminInput, 'isOnline' : False})
            #Accounts.SaveAccountListToFile
        except:
            try:
                PrintLog("Error creating new account, username: " + str(UsernameInput))
            except:
                PrintLog("Error creating new account, error printing username")

    def GetAccountDataFromObject(Account, Key):
        #Accounts.ReadAccountList()
        try:
            Key = str(Key)
            toReturn = Account.get(Key)
            return toReturn
        
        except:
            PrintLog("Error getting account data from object")

    def GetAccountData(UsernameInput, key):
        try:
            returned = False
            UsernameInput = str(UsernameInput)
            key = str(key)

            #Accounts.ReadAccountList()
            for account in Accounts.AccountList:
                if account.get('Username') == UsernameInput:
                    return account.get(key)
                    returned = True

            if returned == False:
                PrintLog("Could not find data when searching " + str(username) + " for " + str(key))
                return ""

            #Accounts.SaveAccountListToFile

        except:
            try:
                PrintLog("Error getting account data for " + str(username))
            except:
                PrintLog("Error getting account data, error printing name")

    def IncreaseErrorCount(UsernameInput):
        CurrentErrorCount = Accounts.GetAccountData(UsernameInput, "ErrorCount")
        if not CurrentErrorCount == None:
            Accounts.PushAccountData(UsernameInput, "ErrorCount", (CurrentErrorCount + 1))

    def PushAccountData(UsernameInput, key, value):
        #Accounts.ReadAccountList()
        UsernameInput = str(UsernameInput)
        key = str(key)
        for account in Accounts.AccountList:
            if account.get('Username') == UsernameInput:
                account.update({key : value})

        #Accounts.SaveAccountListToFile

    def DeleteAccount(UsernameInput, PasswordInput):
        UsernameInput = str(UsernameInput)
        PasswordInput = str(PasswordInput)

        #Accounts.ReadAccountList()
        AccountListB = Accounts.AccountList
        for account in AccountList:
            if account.get('Username') == UsernameInput:
                if account.get('Password') == PasswordInput:
                    AccountListB.remove(account)
        
        Accounts.AccountList = AccountListB
        #Accounts.SaveAccountListToFile

    def InitAccountList():
        Accounts.PopulateFile()
        Accounts.ReadAccountList()
        print(str(len(Accounts.AccountList)))

class Main():
    def ManageClientHighLevel(Username):
        NoError = True
        try:
            HighLevelCommunications.PrivateMessageFromServer(Username, "Welcome to the chatroom.")
        except:
            PrintLog("Error at start of high level manage client")
            connection.close()
            NoError = False

        Accounts.PushAccountData(Username, "LastSeen", time.time())
        Accounts.PushAccountData(Username, "isOnline", True)

        while NoError == True and Accounts.GetAccountData(Username, "ErrorCount") < 10 and Accounts.GetAccountData(Username, "isOnline") == True:
            try:
                connection = Accounts.GetAccountData(Username, "ConnectionObject")
                message = connection.recv(BufferSize).decode("utf8")

                if message:
                    if message == "[PING: REPLY URGENTLY]":
                        #Yes I kind of cheated by circumventing the rest of the script and delays to prevent message concat, but...
                        #I didn't divide it by 2, so it's fair, OK?
                        connection.send(bytes("[PING: URGENT REPLY]", "utf8"))

                    Accounts.PushAccountData(Username, "LastSeen", time.time())
                    Accounts.PushAccountData(Username, "isOnline", True)

                    if"/pm" in message:
                        HighLevelCommunications.PrivateMessageFromServer(Username, "Who do you want to send the PM to?")
                        while not "[CLIENT PING UPDATE]" in message:
                            ToSendPmTo = connection.recv(BufferSize).decode("utf8")
                        ToSendExists = False
                        ToSendOnline = False

                        for account in Accounts.AccountList:
                            if Accounts.GetAccountDataFromObject(account, "Username") == ToSendPmTo:
                                ToSendExists = True
                                if Accounts.GetAccountDataFromObject(account, "isOnline") == True:
                                    ToSendOnline = True

                        if ToSendExists == False:
                            HighLevelCommunications.PrivateMessageFromServer(Username, "User does not exist.")

                        if ToSendExists == True and ToSendOnline == False:
                            HighLevelCommunications.PrivateMessageFromServer(Username, "User exists, but is not online")

                        if ToSendExists == True and ToSendOnline == True:
                            HighLevelCommunications.PrivateMessageFromServer(Username, "What do you want to send?")
                            while not "[CLIENT PING UPDATE]" in message:
                                PmToSend = connection.recv(BufferSize).decode("utf8")

                            Accounts.PushAccountData(ToSendPmTo, "PendingPms", {"Sender" : Username, "Message" : PmToSend, "HasAnswered" : False})

                            HighLevelCommunications.PrivateMessageFromServer(Username, "Added to buffer.")

                    elif "/bug report" in message:
                        HighLevelCommunications.PrivateMessageFromServer(Username, "What would you like to report?")
                        reply = connection.recv(BufferSize).decode("utf8")
                        BugReportsFile = open('bugReports.txt', 'a')
                        BugReportsFile.write("---- BUG REPORT: SENDER " + str(Username) + " TIME:" + str(time.time()) + " ---- \n")
                        BugReportsFile.write(str(reply) + "\n")
                        BugReportsFile.write("</BUG REPORT> \n")
                        BugReportsFile.close()
                        HighLevelCommunications.PrivateMessageFromServer(Username, "Saved.")

                    elif "/feature request" in message:
                        HighLevelCommunications.PrivateMessageFromServer(Username, "What would you like to request?")
                        reply = connection.recv(BufferSize).decode("utf8")
                        FeatureRequestsFile = open('featureRequests.txt', "a")
                        FeatureRequestsFile.write("---- FEATURE REQUEST: SENDER " + str(Username) + " TIME: " + str(time.time()) + " ----\n")
                        FeatureRequestsFile.write(str(reply) + "\n")
                        FeatureRequestsFile.write("</FEATURE REQUEST> \n")
                        FeatureRequestsFile.close()
                        HighLevelCommunications.PrivateMessageFromServer(Username, "Saved.")

                    elif "/exit" in message or "/quit" in message:
                        Accounts.PushAccountData(Username, "isOnline", False)
                        break

                    elif not "[CLIENT PING UPDATE]" in message and not "[PING: REPLY URGENTLY]" in message:
                        PrintLog(Username + ": " + message)
                        HighLevelCommunications.Broadcast(Username + ": " + message)

            except:
                PrintLog("Error in manage client, exiting")
                break

        connection = Accounts.GetAccountData(Username, "ConnectionObject")
        connection.close()
        Accounts.PushAccountData(Username, "ConnectionObject", "")

    def AcceptIncomingConnections():
        while True:
            connection, address = server.accept()
            str(connection)
            PrintLog("Accepted connection from " + str(address) + " , referring")
            Thread(target=Main.WelcomeNewConnections, args=(connection, address)).start()

    def WelcomeNewConnections(connection, address):
        try:
            LowLevelCommunications.SendServerPM(connection, "Make a new account (M), or sign in (S)")
            ContinueConnectionProcess = True
        except:
            PrintLog("Error sending to new client. Removing client.")
            connection.close()
            ContinueConnectionProcess = False
        
        try:
            if ContinueConnectionProcess == True:
                response = connection.recv(BufferSize).decode("utf8")
                if response == "M":
                    Thread(target=Main.NewAccountProcess, args=(connection, address)).start()

                else:
                    Thread(target=Main.SignInProcess, args=(connection, address)).start()


        except:
            PrintLog("Error in welcome new connections. Removing client")
            connection.close()

    def SignInProcess(connection, address):
        try:
            while True:
                try:
                    LowLevelCommunications.SendServerPM(connection, "Please enter username, be careful about whitespace: ")
                    Username = connection.recv(BufferSize).decode("utf8")

                    DoesAccountExist = False

                    for account in Accounts.AccountList:
                        if Accounts.GetAccountDataFromObject(account, "Username") == Username:
                            DoesAccountExist = True

                    if DoesAccountExist == True:
                        break

                    else:
                        LowLevelCommunications.SendServerPM(connection, "That account doesn't exist.")

                except:
                    PrintLog("Error in sign in : Username pick loop, closing connection")
                    connection.close()
                    break
            
            #Double negative because it sometimes returns "none"
            if not Accounts.GetAccountData(Username, "isOnline") == True and DoesAccountExist == True:
                while True:
                    LowLevelCommunications.SendInternalMessage(connection, "PASSWORD ENTRY FIELD")
                    time.sleep(0.2)
                    LowLevelCommunications.SendServerPM(connection, "Enter password, be careful about whitespace.")

                    Password = connection.recv(BufferSize).decode("utf8")
                    PrintLog("Received [Hashed] password: " + str(Password))

                    #Doesn't work if you just don't send your captured pw on or change it, but it's worth it anyway
                    if len(Password) < 50:
                        PrintLog("PASSWORD IS LESS THAN 50 CHARACTERS: PASSWORD MAY NOT BE HASHED: LINK MAY BE COMPROMISED.")
                        PrintLog("COMPROMISE TIME: " + time.time())
                        while True:
                            LowLevelCommunications.SendServerPM(connection, "YOUR LINK TO THE SERVER MAY BE COMPROMISED")
                            LowLevelCommunications.SendServerPM(connection, "IF YOU USE THIS PASSWORD ANYWHERE ELSE, CHANGE IT.")
                            time.sleep(5)

                    
                    if Accounts.GetAccountData(Username, "Password") == Password:
                        Accounts.PushAccountData(Username, "ConnectionObject", connection)
                        HighLevelCommunications.PrivateMessageFromServer(Username, "If you can read this, you successfully identified. Type 'continue' to continue.")
                        reply = connection.recv(BufferSize).decode("utf8")
                        print(str(Username))
                        if reply == "continue":
                            Accounts.PushAccountData(Username, "ErrorCount", 0)
                            Thread(target=Main.ManageClientHighLevel, args=(Username,)).start()
                            break

                        else:
                            connection.close()

                    else:
                        LowLevelCommunications.SendServerPM(connection, "Password incorrect.")

            else:
                LowLevelCommunications.SendServerPM(connection, "You are online somewhere else.")
                connection.close()
        except:
            PrintLog("Error in signin")
            connection.close()

    def NewAccountProcess(connection, address):
        try:
            LowLevelCommunications.SendServerPM(connection, "Please enter phrase to auth new account")
            response = connection.recv(BufferSize).decode("utf8")
        except:
            PrintLog("Error in NewAccountProcess, closing connection")
            connection.close()

        #try:
        if response == "Hello":
            try:
                while True:
                    InUse = False
                    LowLevelCommunications.SendServerPM(connection, "Please enter your new username: ")
                    response = connection.recv(BufferSize).decode("utf8")
                    Username = response

                    if " " in Username:
                        InUse = True
                        LowLevelCommunications.SendServerPM(connection, "Remove that whitespace!")

                    for account in Accounts.AccountList:
                        if Accounts.GetAccountDataFromObject(account, "Username") == Username:
                            LowLevelCommunications.SendServerPM(connection, "Sorry! That username is already in use.")
                            InUse = True

                    bannedWords = ["Marlwood is great", "Admin", "Server", "admin", "server"]
                    for word in bannedWords:
                        if word in Username:
                            LowLevelCommunications.SendServerPM(connection, "Username is in a blacklist.")
                            InUse = True

                    if "42" in Username:
                        LowLevelCommunications.SendServerPM(connection, "42! Nice!")
                    
                    if InUse == False:
                        break

            except:
                PrintLog("Error")
                connection.close()

            try:
                LowLevelCommunications.SendServerPM(connection, "Username received: " + Username)

                if InUse == False:
                    LowLevelCommunications.SendInternalMessage(connection, "PASSWORD ENTRY FIELD")
                    LowLevelCommunications.SendServerPM(connection, "Please enter your new password: ")
                    response = connection.recv(BufferSize).decode("utf8")
                    Password = response
                    PrintLog("Received [Hashed] password: " + str(Password))

                    #Doesn't work if you just don't send your captured pw on or change it, but it's worth it anyway
                    if len(Password) < 50:
                        PrintLog("PASSWORD IS LESS THAN 50 CHARACTERS: PASSWORD MAY NOT BE HASHED: LINK MAY BE COMPROMISED.")
                        PrintLog("COMPROMISE TIME: " + time.time())
                        while True:
                            LowLevelCommunications.SendServerPM(connection, "YOUR LINK TO THE SERVER MAY BE COMPROMISED")
                            LowLevelCommunications.SendServerPM(connection, "IF YOU USE THIS PASSWORD ANYWHERE ELSE, CHANGE IT.")
                            time.sleep(5)

                    loops = 0
                    while loops < 32:
                        loops = loops + 1
                        LowLevelCommunications.SendServerPM(connection, "Do you want to elevate to admin? Y/N: ")
                        response = connection.recv(BufferSize).decode("utf8")
                        if response == "Y":
                            LowLevelCommunications.SendInternalMessage(connection, "PASSWORD ENTRY FIELD")
                            LowLevelCommunications.SendServerPM(connection, "Password: ")

                            response = connection.recv(BufferSize).decode("utf8")
                            #
                            # Doesn't work if you just don't send your captured pw on or change it, but it's worth it anyway
                            if len(response) < 50:
                                PrintLog("PASSWORD IS LESS THAN 50 CHARACTERS: PASSWORD MAY NOT BE HASHED: LINK MAY BE COMPROMISED.")
                                PrintLog("COMPROMISE TIME: " + time.time())
                                while True:
                                    LowLevelCommunications.SendServerPM(connection, "YOUR LINK TO THE SERVER MAY BE COMPROMISED")
                                    LowLevelCommunications.SendServerPM(connection, "IF YOU USE THIS PASSWORD ANYWHERE ELSE, CHANGE IT.")
                                    time.sleep(5)
                            
                            #replace as you wish. Use the ClientV2Implementation() function in Hash Testing.py to calculate.
                            if response == "b97cd8e783380b48e41b26237ca60c8ef2bb3f7339c895e304185885e9f8ba30972a8ec9ba7740077c5b8f862912611e4fbc4824b285a2e55b24c719149d3905":
                                IsAdmin = True
                                LowLevelCommunications.SendServerPM(connection, "Successful admin elevation")
                                break

                            else:
                                IsAdmin = False
                                LowLevelCommunications.SendServerPM(connection, "Password wrong.")

                        else:
                            IsAdmin = False
                            break
                
                else:
                    connection.close()

                time.sleep(0.5)
                LowLevelCommunications.SendServerPM(connection, "Creating account...")
                #waits for a bit to stop spamming
                time.sleep(1)
                Accounts.NewAccount(Username, Password, IsAdmin)
                time.sleep(1)
                Accounts.PushAccountData(Username, "ConnectionObject", connection)
                Accounts.PushAccountData(Username, "isOnline", False)
                HighLevelCommunications.PrivateMessageFromServer(Username, "If you can read this, your account creation worked.")
                time.sleep(0.2)
                HighLevelCommunications.PrivateMessageFromServer(Username, "Enter the word 'continue' to sign in")
                try:
                    response = connection.recv(BufferSize).decode("utf8")
                except:
                    PrintLog("Error getting response from client")
                    connection.close()

                if response == "continue":
                    Thread(target=Main.SignInProcess, args=(connection, address)).start()

                else:
                    connection.close()
            except:
                connection.close()
                PrintLog("Error in account creation")

        else:
            connection.close()
    #except:
    #    PrintLog("Error in account creation, exiting")    
    #    connection.close()  

class PMManager:
    def PMManager():
        PrintLog("PM Manager started")
        while True:
            try:
                time.sleep(5)
                for Account in Accounts.AccountList:
                    if not Accounts.GetAccountDataFromObject(Account, "PendingPms") == None:
                        if Accounts.GetAccountDataFromObject(Account, "isOnline") == True:
                            Username = Accounts.GetAccountDataFromObject(Account, "Username")
                            PendingPMobject = Accounts.GetAccountData(Username, "PendingPms")
                            if PendingPMobject.get("HasAnswered") == False:
                                HighLevelCommunications.PrivateMessageFromServer(Username, "You have received a private message.")
                                time.sleep(0.25)
                                HighLevelCommunications.PrivateMessageFromServer(Username, "Name: " + str(PendingPMobject.get("Sender")))
                                time.sleep(0.25)
                                HighLevelCommunications.PrivateMessageFromServer(Username, "Message: " + str(PendingPMobject.get("Message")))
                                time.sleep(0.25)
                                Accounts.PushAccountData(Username, "PendingPms", None)

                            else:
                                PrintLog("PM MANAGER: Already answered")

                        else:
                            PrintLog("Not online, not sending PM")

            except TypeError:
                continue
            
            except:
                PrintLog("Error in PM manager, can not increase log")

#NOTE Not in any class because I want it to be readily accessed and it doesn't belong to any in particular
def PrintLog(text):
    text = str(text)
    print(text)
    text = str(time.time()) + " : " + text + "\n"
    LogFile = open('log.txt', 'a')
    LogFile.write(text)

class PingManager:
    def PingManager():
        while True:
            time.sleep(10)
            for account in Accounts.AccountList:
                if Accounts.GetAccountDataFromObject(account, "isOnline") == True:
                    lastSeen = Accounts.GetAccountDataFromObject(account, "LastSeen")
                    difference = time.time() - lastSeen

                    if difference > 30:
                        Username = Accounts.GetAccountDataFromObject(account, "Username")
                        Accounts.PushAccountData(Username, "isOnline", False)

server = socket(AF_INET, SOCK_STREAM) 
Port = input("Port: ")
if not Port:
    Port = 34000
    PrintLog("Defaulted")

else:
    Port = int(Port)
    PrintLog("Port set to " + str(Port))

Host = ""
BufferSize = 2048
try:
    server.bind((Host, Port))
except:
    if Port == 34000:
        Port = 34001
        PrintLog("Set port to 34001 due to error")

    elif Port == 34001:
        Port = 34000
        PrintLog("Set port to 34000 due to error")

    server.bind((Host, Port))
server.listen(1000)

def PrintPeriodic():
    while True:
        time.sleep(0.5)
        PrintLog(str(Accounts.GetAccountData("Alex", "isOnline")))

PrintLog("--SCRIPT RESTART-- SERVER VERSION: 3 -- TIME: " + str(time.time()))

Accounts.InitAccountList()

Thread(target=PMManager.PMManager).start()

Thread(target=PingManager.PingManager).start()

#Thread(target=PrintPeriodic).start()

Main.AcceptIncomingConnections()