import time, hashlib, sys, string, pickle
from socket import AF_INET, socket, SOCK_STREAM
from threading import *

class Server():
    def PrivateMessageFromServer(Username):
        #TODO Private message from server
        a = 1
    
    def Broadcast(Username):
        #TODO Broadcast
        a = 1        


    def InternalMessage(Username):
        #TODO Internal message
        a = 1

    def PingCheck(Username):
        #TODO Ping check
        a = 1

    def Encode(Text):
        return bytes(Text, "utf8")

class Cryptography():
    def KeyExchange():
        #TODO Key exchange
        a = 1

    def Encrypt(text, publicKey):
        #TODO Encryption
        a = 1

    def Decrypt(text, privateKey):
        #TODO Decryption
        a = 1

    def HashPassword(text):
        return str(hashlib.sha512(bytes(str(text) + "f8weucrwirun3wurifiwshfklhwifiwfhownowur8o2rn82u8onu328cu482bu82u48b23u89", "utf8")).hexdigest())

class Accounts():
    AccountList = []
    #Account specifications:
    #A example account
    #{
    #    Username : "Alex"
    #    Password : "sjfhjsbfh9w8fn028h02n etc",
    #    PendingPms : {Sender: "Luke", Message : "Hello!"},
    #    isAdmin : True
    #    isOnline : True
    #    isOP: True
    #    connectionObject: {IP : 127.0.0.1, PROTOCOL : TCP, NOTES : "I am not copying an entire sockets connection object"}
    #}

    def ReadAccountList():
        SaveFile = open("accounts", "rb")
        Accounts.AccountList = pickle.load(SaveFile)

    def SaveAccountListToFile():
        SaveFile = open("accounts", "wb")
        pickle.dump(Accounts.AccountList, SaveFile)

    def NewAccount(UsernameInput, PasswordInput, isAdminInput, isOpInput):
        #TODO New account
        Accounts.ReadAccountList()
        Accounts.AccountList.append({"Username" : UsernameInput, "Password" : PasswordInput, "isAdmin" : isAdminInput, "isOnline" : True, "isOP" : isOpInput})
        Accounts.SaveAccountListToFile()

    def GetAccountData(UsernameInput, key):
        Accounts.ReadAccountList()
        for account in Accounts.AccountList:
            if account.get("Username") == UsernameInput:
                return account.get(key)

        Accounts.SaveAccountListToFile()
        #TODO Get account data

    def PushAccountData(UsernameInput, key, value):
        ReadAccountList()
        for account in Accounts.AccountList:
            if account.get("Username") == UsernameInput:
                account.update({key : value})

        SaveAccountListToFile()
        #TODO Push account data

    def DeleteAccount(UsernameInput, PasswordInput):
        ReadAccountList()
        AccountListB = Accounts.AccountList
        for account in AccountList:
            if account.get("Username") == UsernameInput:
                if account.get("Password") == PasswordInput:
                    AccountListB.remove(account)
        
        Accounts.AccountList = AccountListB
        SaveAccountListToFile()
        #TODO Account deletion

class Dev():
    def AddAccount():
        Username = input("Username: ")
        Password = input("Password: ")
        Password = Cryptography.HashPassword(Password)
        IsAdmin = True
        IsOp = False
        Accounts.NewAccount(Username, Password, IsAdmin, IsOp)


    def GetAccountInfo():
        Username = input("Username: ")
        print(str(Accounts.GetAccountData(Username, "isAdmin")))

    def ChangeAccount():
        Username = input("Username: ")
        key = input("Key: ")
        value = input("Value: ")

        #TODO CURRENT make this work

class Main():
    def PrintLog(text):
        text = str(text)
        print(text)
        LogFile = open("log.txt", "a")
        LogFile.write(text)
        #TODO PrintLog

    def ManageClient(Username):
        #TODO Manage client
        a = 1

    def AcceptIncomingConnections():
        #TODO Accept incoming connections
        a = 1

    def PeriodicPing():
        #TODO Periodic ping
        a = 1

    def PMManager():
        #TODO PM manager
        a = 1
    
Dev.GetAccountInfo()