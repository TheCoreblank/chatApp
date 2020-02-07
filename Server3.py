import time, hashlib, sys, string
from socket import AF_INET, socket, SOCK_STREAM
from threading import *

class Server():
    def PrivateMessageFromServer(Username):
        #TODO Private message from server
    
    def Broadcast(Username):
        #TODO Broadcast

    def InternalMessage(Username):
        #TODO Internal message
    
    def PingCheck(Username):
        #TODO Ping check

    def Encode(Text):
        return bytes(Text, "utf8")

class Cryptography():
    def KeyExchange():
        #TODO Key exchange

    def Encrypt(text, publicKey):
        #TODO Encryption

    def Decrypt(text, privateKey):
        #TODO Decryption

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
        AccountList = []
        SaveFile = open("accounts.txt", "r")
        AccountList = list(SaveFile.read())

    def SaveAccountListToFile():
        SaveFile = open("accounts.txt", "w")
        SaveFile.write(AccountList)

    def NewAccount(UsernameInput, PasswordInput, isAdminInput, isOpInput):
        #TODO New account
        ReadAccountList()
        AccountList.append({Username : UsernameInput, Password : PasswordInput, isAdmin : isAdminInput, isOnline : True, isOP : isOpInput})
        SaveAccountListToFile()

    def GetAccountData(UsernameInput, key):
        ReadAccountList()
        for account in AccountList:
            if account[Username] == UsernameInput:
                return account[key]

        SaveAccountListToFile()
        #TODO Get account data

    def PushAccountData(UsernameInput, key, value):
        ReadAccountList()
        for account in AccountList:
            if account[Username] == UsernameInput:
                account.update({key : value})

        SaveAccountListToFile()
        #TODO Push account data

    def DeleteAccount(UsernameInput, PasswordInput):
        ReadAccountList()
        AccountListB = AccountList
        for account in AccountList:
            if account[Username] == UsernameInput:
                if account[Password] == PasswordInput:
                    AccountListB.remove(account)

        AccountList = AccountListB
        SaveAccountListToFile()
        #TODO Account deletion

class Dev():
    def AccountsTesting:
        Username = input("Username: ")
        Password = input("Password: ")
        Password = HashPassword(Password)
        #continue


class Main():
    def PrintLog(text):
        text = str(text)
        print(text)
        LogFile = open("log.txt", "a")
        LogFile.write(text)
        #TODO PrintLog

    def ManageClient(Username):
        #TODO Manage client

    def AcceptIncomingConnections():
        #TODO Accept incoming connections

    def PeriodicPing():
        #TODO Periodic ping

    def PMManager():
        #TODO PM manager
    
