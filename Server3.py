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
    
    def Broadcast(Text):
        Text = str(Text)
        try:
            for account in Accounts.AccountList():
                try:
                    if Accounts.GetAccountDataFromObject(account, "isOnline") == True:
                        Connection = Accounts.GetAccountDataFromObject(account, "ConnectionObject")
                        ToSend = HighLevelCommunications.Encode("[SERVER INTERNAL-BROADCAST]" + str(Text))
                        Connection.send(ToSend)
                except:
                    PrintLog("Error in broadcast : loop")
                    continue

            PrintLog("Broadcasted " + Text)
        except:
            PrintLog("Error in broadcast")
            pass


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
            pass

        try:
            if hadError == False:
                toSend = "[SERVER INTERNAL-INTERNAL]" + Text
                Connection.send(HighLevelCommunications.Encode(toSend))
            else:
                PrintLog("Had error earlier, not sending")
        except:
            PrintLog("Error sending internal message")

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
    #    connectionObject: {IP : 127.0.0.1, PROTOCOL : TCP, NOTES : 'I am not copying an entire sockets connection object'}
    #}

    def ReadAccountList():
        try:
            SaveFile = open('accounts', 'rb')
            Accounts.AccountList = pickle.load(SaveFile)
        except:
            PrintLog("Error reading account list from file, passing")
            pass

    def SaveAccountListToFile():
        try:
            SaveFile = open('accounts', 'wb')
            pickle.dump(Accounts.AccountList, SaveFile)
        except:
            PrintLog("Error saving account list to file, passing")
            pass

    def PopulateFile():
        SaveFile = open("accounts", "wb")
        toDump = [{"Username" : "Placeholder-jshgfiowjfiowfo2nwfo"}]
        pickle.dump(toDump, SaveFile)

    def NewAccount(UsernameInput, PasswordInput, isAdminInput):
        try:
            UsernameInput = str(UsernameInput)
            PasswordInput = str(PasswordInput)
            isAdminInput = str(isAdminInput)

            Accounts.ReadAccountList()
            Accounts.AccountList.append({'Username' : UsernameInput, 'Password' : PasswordInput, 'isAdmin' : isAdminInput, 'isOnline' : True})
            Accounts.SaveAccountListToFile()
        except:
            try:
                PrintLog("Error creating new account, username: " + str(UsernameInput))
            except:
                PrintLog("Error creating new account, error printing username")

    def GetAccountDataFromObject(Account, Key):
        Accounts.ReadAccountList()
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

            Accounts.ReadAccountList()
            for account in Accounts.AccountList:
                if account.get('Username') == UsernameInput:
                    return account.get(key)
                    returned = True

            if returned == False:
                PrintLog("Could not find data when searching " + str(username) + " for " + str(key))
                return ""

            Accounts.SaveAccountListToFile()

        except:
            try:
                PrintLog("Error getting account data for " + str(username))
            except:
                PrintLog("Error getting account data, error printing name")

    def PushAccountData(UsernameInput, key, value):
        Accounts.ReadAccountList()
        UsernameInput = str(UsernameInput)
        key = str(key)
        for account in Accounts.AccountList:
            if account.get('Username') == UsernameInput:
                account.update({key : value})

        Accounts.SaveAccountListToFile()

    def DeleteAccount(UsernameInput, PasswordInput):
        UsernameInput = str(UsernameInput)
        PasswordInput = str(PasswordInput)

        Accounts.ReadAccountList()
        AccountListB = Accounts.AccountList
        for account in AccountList:
            if account.get('Username') == UsernameInput:
                if account.get('Password') == PasswordInput:
                    AccountListB.remove(account)
        
        Accounts.AccountList = AccountListB
        Accounts.SaveAccountListToFile()

class Dev():
    def AddAccount():
        Username = input('Username: ')
        Password = input('Password: ')
        Password = Cryptography.HashPassword(Password)
        IsAdmin = True
        IsOp = False
        Accounts.NewAccount(Username, Password, IsAdmin)


    def GetAccountInfo():
        Username = input('Username: ')
        print(str(Accounts.GetAccountData(Username, 'isAdmin')))

    def ChangeAccountInfo():
        Username = input('Username: ')
        key = input('Key: ')
        value = input('Value: ')

        Accounts.PushAccountData(Username, key, value)

class Main():
    def ManageClient(Username):
        #TODO Manage client
        a = 1

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
                        LowLevelCommunications.SendServerPM(connection, "Identified account.")
                        DoesAccountExist = True

                if DoesAccountExist == True:
                    break

                else:
                    LowLevelCommunications.SendServerPM(connection, "That account doesn't exist.")

            except:
                PrintLog("Error in sign in : Username pick loop, closing connection")
                connection.close()
                break

            
        try:
            while True:
                LowLevelCommunications.SendServerPM(connection, "Enter password, be careful about whitespace.")
                time.sleep(0.5)
                LowLevelCommunications.SendInternalMessage(connection, "PASSWORD ENTRY FIELD")

                Password = connection.recv(BufferSize).decode("utf8")
                
                if Accounts.GetAccountData(Username, "Password") == Password:
                    Accounts.PushAccountData(Username, "ConnectionObject", connection)
                    HighLevelCommunications.PrivateMessageFromServer(Username, "If you can read this, you successfully identified. Type 'continue' to continue.")
                    reply = connection.recv(BufferSize).decode("utf8")
                    if "continue" in reply:
                        Thread(target=Main.ManageClient, args=(Username)).start()

                    else:
                        connection.close()

                else:
                    LowLevelCommunications.SendServerPM(connection, "Password incorrect.")

        except:
            connection.Close()

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
                time.sleep(2.5)
                Accounts.NewAccount(Username, Password, IsAdmin)
                time.sleep(1)
                Accounts.PushAccountData(Username, "ConnectionObject", connection)
                HighLevelCommunications.PrivateMessageFromServer(Username, "If you can read this, your account creation worked.")
                time.sleep(0.2)
                HighLevelCommunications.PrivateMessageFromServer(Username, "Enter the word 'continue' to sign in")
                response = connection.recv(BufferSize).decode("utf8")
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

    def PMManager():
        #TODO PM manager
        a = 1

#NOTE Not in any class because I want it to be readily accessed and it doesn't belong to any in particular
def PrintLog(text):
    text = str(text)
    print(text)
    LogFile = open('log.txt', 'a')
    LogFile.write(text)

#TODO Proper, server V2-Like remove function

server = socket(AF_INET, SOCK_STREAM) 
Port = int(input("Port: "))
Host = ""
BufferSize = 2048
server.bind((Host, Port))
server.listen(1000)

#For a bunch of stuff to work, the accounts file needs to be populated. Run if you deleted it.
#Accounts.PopulateFile()

Main.AcceptIncomingConnections()

#NOTES:
#Fix it allowing accounts of same name, and strip whitespace when checking
#Fix it breaking when you exit the client
#Do sign in 