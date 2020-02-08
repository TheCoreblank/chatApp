import time, hashlib, sys, string, pickle
from socket import AF_INET, socket, SOCK_STREAM
from threading import *

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
            PrintLog("Error sending low level internal PM, passing")
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

class Cryptography():
    def HashPassword(text):
        i = 0
        while True:
            i = i + 1
            text = str(hashlib.sha512(bytes(str(text) + str(i) + 'f8weucrwirun3wurifiwshfkfdsifjisdjfisjfiosjflsjfiljdslkfjllhwifiwfhownowur8o2rn82u8onu328cu482bu82u48b23u89', 'utf8')).hexdigest())
            if i == 128:
                break

        return str(text)
        
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
        #BROKEN, SO NOT RUNNING
        SaveFile = open('accounts', 'rb')
        Accounts.AccountList = pickle.load(SaveFile)

    def SaveAccountListToFile():
        #BROKEN, SO NOT RUNNING
        SaveFile = open('accounts', 'wb')
        AccountsListNoSockets = Accounts.AccountList

        for account in Accounts.AccountList:
            try:
                del account["ConnectionObject"]
            except KeyError:
                PrintLog("Connection object not found to delete")

        print(str(AccountsListNoSockets))

        pickle.dump(AccountsListNoSockets, SaveFile)

    def PopulateFile():
        SaveFile = open("accounts", "wb")
        toDump = [{"Username" : "Placeholder-jshgfiowjfiowfo2nwfo"}]
        pickle.dump(toDump, SaveFile)

    def NewAccount(UsernameInput, PasswordInput, isAdminInput):
        try:
            UsernameInput = str(UsernameInput)
            PasswordInput = str(PasswordInput)
            isAdminInput = str(isAdminInput)

            #Accounts.ReadAccountList()
            Accounts.AccountList.append({'Username' : UsernameInput, 'Password' : PasswordInput, 'isAdmin' : isAdminInput, 'isOnline' : True})
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
            HighLevelCommunications.InternalMessage(Username, "SENDPINGS=TRUE")
            HighLevelCommunications.PrivateMessageFromServer(Username, "Welcome to the chatroom.")
        except:
            PrintLog("Error at start of high level manage client")
            connection.close()
            NoError = False

        while NoError == True and Accounts.GetAccountData(Username, "ErrorCount") < 10:
            try:
                connection = Accounts.GetAccountData(Username, "ConnectionObject")
                message = connection.recv(BufferSize).decode("utf8")

                if message:
                    if "[PING INTERNAL]" in message:
                        PingManager.LastPingUpdate = time.time()
                        Accounts.PushAccountData(Username, "isOnline", True)


                    elif "/pm" in message:
                        HighLevelCommunications.PrivateMessageFromServer(Username, "Who do you want to send the PM to?")
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
                            PmToSend = connection.recv(BufferSize).decode("utf8")

                            Accounts.PushAccountData(ToSendPmTo, "PendingPms", {"Sender" : Username, "Message" : PmToSend, "HasAnswered" : False})

                            HighLevelCommunications.PrivateMessageFromServer(Username, "Added to buffer.")


                    else:
                        PrintLog(Username + ": " + message)
                        HighLevelCommunications.Broadcast(Username + ": " + message)
                        Accounts.PushAccountData(Username, "isOnline", True)

            except:
                PrintLog("Error in manage client, exiting")
                break

    def AcceptIncomingConnections():
        while True:
            connection, address = server.accept()
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

            
        while True:
            LowLevelCommunications.SendServerPM(connection, "Enter password, be careful about whitespace.")
            time.sleep(0.2)
            LowLevelCommunications.SendInternalMessage(connection, "PASSWORD ENTRY FIELD")

            Password = connection.recv(BufferSize).decode("utf8")
            
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

    def NewAccountProcess(connection, address):
        try:
            LowLevelCommunications.SendServerPM(connection, "Please enter phrase to auth new account")
            response = connection.recv(BufferSize).decode("utf8")
        except:
            PrintLog("Error in NewAccountProcess, closing connection")
            connection.close()

        #try:
        if response == "Hello":
            while True:
                InUse = False
                LowLevelCommunications.SendServerPM(connection, "Please enter your new username: ")
                response = connection.recv(BufferSize).decode("utf8")
                Username = response

                if " " in Username:
                    InUse = True
                    LowLevelCommunications.SendServerPM(connection, "Remove that whitespace!")

                #TODO Check this works
                for account in Accounts.AccountList:
                    if Accounts.GetAccountDataFromObject(account, "Username") == Username:
                        LowLevelCommunications.SendServerPM(connection, "Sorry! That username is already in use.")
                        InUse = True
                
                if InUse == False:
                    break

            LowLevelCommunications.SendServerPM(connection, "Username received: " + Username)

            if InUse == False:
                LowLevelCommunications.SendServerPM(connection, "Please enter your new password: ")
                LowLevelCommunications.SendInternalMessage(connection, "PASSWORD ENTRY FIELD")
                response = connection.recv(BufferSize).decode("utf8")
                Password = response

                loops = 0
                while loops < 32:
                    loops = loops + 1
                    LowLevelCommunications.SendServerPM(connection, "Do you want to elevate to admin? Y/N: ")
                    response = connection.recv(BufferSize).decode("utf8")
                    if response == "Y":
                        LowLevelCommunications.SendServerPM(connection, "Password: ")
                        #FIXME placeholder pw, will obviously be hashed in the future
                        response = connection.recv(BufferSize).decode("utf8")

                        if response == "Password1!":
                            IsAdmin = True
                            LowLevelCommunications.SendServerPM(connection, "Successful admin elevation")
                            break

                        else:
                            IsAdmin = False
                            LowLevelCommunications.SendServerPM(connection, "Password wrong.")

                    else:
                        IsAdmin = False
                        break

                time.sleep(0.5)
                LowLevelCommunications.SendServerPM(connection, "Creating account...")
                #waits for a bit to stop spamming
                time.sleep(1)
                Accounts.NewAccount(Username, Password, IsAdmin)
                time.sleep(1)
                Accounts.PushAccountData(Username, "ConnectionObject", connection)
                HighLevelCommunications.PrivateMessageFromServer(Username, "If you can read this, your account creation worked.")
                time.sleep(0.2)
                HighLevelCommunications.PrivateMessageFromServer(Username, "Enter the word 'continue' to sign in")
                try:
                    response = connection.recv(BufferSize).decode("utf8")
                except:
                    PrintLog("Error getting response from client")

                if response == "continue":
                    Thread(target=Main.SignInProcess, args=(connection, address)).start()

                else:
                    connection.close()

            else:
                connection.close()

        else:
            connection.close()
        #except:
        #    PrintLog("Error in account creation, exiting")    
        #    connection.close()  

class PMManager:
    def PMManager():
        #FIXME PM manager
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
class PingManager:
    LastPingUpdate = 0
    def PingManager():
        #TODO Ping manager
        a = 1

#NOTE Not in any class because I want it to be readily accessed and it doesn't belong to any in particular
def PrintLog(text):
    text = str(text)
    print(text)
    LogFile = open('log.txt', 'a')
    LogFile.write(text)

server = socket(AF_INET, SOCK_STREAM) 
Port = int(input("Port: "))
Host = ""
BufferSize = 2048
server.bind((Host, Port))
server.listen(1000)

Accounts.InitAccountList()

Thread(target=PMManager.PMManager).start()

Main.AcceptIncomingConnections()

#NOTES:
#Fix it allowing accounts of same name, and strip whitespace when checking
#Fix it breaking when you exit the client
#Do sign in 