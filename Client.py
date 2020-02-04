#client side script
#TODO Make the UI fit in with google docs
from socket import AF_INET, socket, SOCK_STREAM
from threading import *
import tkinter, time
from tkinter import messagebox
import sys, hashlib

#not sure. I am scared to remove it, so I'll keep it. 
isUp = False

DoCustom = input("Do you want to do default or custom setup? C/D > ")

if DoCustom == "C":
    DoCustom = True

elif DoCustom == "D":
    DoCustom = False

else:
    DoCustom = False
    print("Non Y/N answer, defaulting to default")

if DoCustom:
    allowRemoteAccess = input("Do you want to allow admins to remotely shut down or wipe if teachers come? Y/N > ")

    if allowRemoteAccess == "Y":
        allowRemoteAccess = True

    elif allowRemoteAccess == "N":
        allowRemoteAccess = False

    else:
        allowRemoteAccess = True
        print("Non Y/N answer, defaulting to yes")

#There is an identical one on the server, it means my friends can't pretend to 
#send commands as the server without knowing python

def CalculateAuthCode():
    authCode = int(int(time.time()) / int(10))
    authCode = hashlib.sha512(bytes(str(authCode), "utf8")).hexdigest()
    authCode = str(authCode)
    return authCode

#does pretty much everything. Writes stuff from the server to the list, unless it's an internal message, in which case it authenticates and runs
def ReceiveFromServer():
    while True:
        try:
            #receive *and* decode
            message = client_socket.recv(Buffer_size).decode("utf8")
            #if it is a auth prompt, set the entry field to stars
            if "Enter authorisation" in message or "password required" in message:
                print("Set entry mode to auth")
                SetLabelStatus("Enter password")
                entry_field["show"] = "*"

            else:
                entry_field["show"] = ""

            #if it receives an exit authorise, it authenticates then exits.
            if "-- EXIT AUTHORISE --" in message and allowRemoteAccess == True:
                SetLabelStatus("Received remote close, verifying auth code")
                print("Received auth message...")
                
                if CalculateAuthCode() in message:
                    SetLabelStatus("Auth code correct. Exiting...")
                    print("Auth correct. Exiting.")
                    WipeList()
                    top.destroy()
                    sys.exit()

                else:
                    print("Auth incorrect. Not responded.")
                    SetLabelStatus("Auth incorrect.")

            #same as above, but for wipe
            if "-- WIPE AUTHORISE --" in message and allowRemoteAccess == True:
                print("Received auth message...")
                SetLabelStatus("Received remote wipe, verifying auth code")
                if CalculateAuthCode() in message:
                    SetLabelStatus("Auth correct, wiping.")
                    print("Auth correct. Wiping..")
                    WipeList()
                    message_list.delete(0)
                    SetLabelStatus("Only talk about the work or you will be banned.")

                else:
                    SetLabelStatus("Auth incorrect.")
                    print("Auth incorrect. Not responded.")

            #triggers fake text, renamed so if teachers see the message they aren't suspicious
            if "-- AUTHORISE 42 --" in message and allowRemoteAccess == True:
                print("Received 42 message...")
                SetLabelStatus("Received remote 42, verifying auth code")
                if CalculateAuthCode() in message:
                    SetLabelStatus("Auth correct")
                    InsertFakeText()

                else:
                    SetLabelStatus("Auth incorrect")
                    print("Auth incorrect. Not responded.")
            
            if "[INTERNAL SET LABEL MESSAGE]" in message:
                #28 is the length of "[INTERNAL SET LABEL MESSAGE]" + 1.
                #and the crazy symbol list thingy removes everything before 28. 
                #it's a part of the python language I barely know. I can do
                #stuff like this, but anything more complex and I'm off to
                #stack overflow.
                SetLabelStatus(message[28:])

            #if it's not internal, write it in the feed. 
            if not "-- WIPE AUTHORISE --" in message and not "-- EXIT AUTHORISE --" in message and not "[INTERNAL SET LABEL MESSAGE]" in message and not "-- AUTHORISE 42 --" in message:
                message_list.insert(tkinter.END, message)
            
        except OSError: #may be a client exit
            break
        
#sends to the server. Note it doesn't write it's own messages to the feed.
#it sends to the server, server sends them back, it writes them down. It simplifies 
#the process server side and it a obvious way of knowing if your connection is working.

#also, this event thing? It's extremely annoying. I spent half an hour thinking I was passing messages to it
#and the server was the one being weird cause it doesn't show errors! It's a tkinter requirement. 
def send(event=None): 
    #handles sending of messages
    SetLabelStatus("Sending...")
    #gets from message box
    message = my_message.get()
    my_message.set("")

    #if not client command, send
    if not "sudo shutdown server" in message and not "/help" in message:
        client_socket.send(bytes(message, "utf8"))

    SetLabelStatus("Sent.")

    #if internal command, do shit
    #wipes. 
    if message == "/wipe" or message == "/clear":
        SetLabelStatus("Received, wiping")
        WipeList()
        SetLabelStatus("")
    
    #exits
    if message == "/exit" or message == "/quit":
        SetLabelStatus("Quitting.")
        WipeList()
        client_socket.close()
        top.destroy()
        top.quit()
        sys.exit()

    #the client side of the verify. It's more for debug, it writes it's auth code and tells the server
    #to send it's (just the command sent earlier does that) so you can compare them
    if message == "/verify":
        message_list.insert(tkinter.END, "Client [LOCAL]: " + CalculateAuthCode())

    #inserts a bunch of stilted, totally unconvincing fake "lesson friendly" chatter. 
    if message == "/faketext" or message == "/faketext -a":
        InsertFakeText()
    
    #if you are sending the shutdown message, send an auth code, cause that thing's the highest security
    #there is in this joke so we need to use the totally secure, impossible to fake method of
    #hashing the time then sending a password over the internet in plain text before finally hashing it
    #at destination. You know, I really should add cryptography, it's just I can't be bothered to
    #implement key exchanges. All the crypto libraries are stupidly contrived too, I just want to go
    #"Here's the public key, now encrypt it."
    if "sudo shutdown server" in message:
        client_socket.send(bytes(("sudo shutdown server " + CalculateAuthCode()), "utf8"))

    #yeah, totally not cause I can't work out how to make scrolling reliable enough to fit enough data
    #in for a help page
    if "/help" in message:
        message_list.insert(tkinter.END, "Read the readme, you dimwit. ")
        message_list.insert(tkinter.END, "https://github.com/AlexAndHisScripts/chatApp")

#aforementioned unconvincing shit
def InsertFakeText():
    WipeList()
    message_list.insert(tkinter.END, "1: Can you send me the link for the website?")
    message_list.insert(tkinter.END, "2: bit.ly/HA&42&fU got the free url shortener,")
    message_list.insert(tkinter.END, "2: it'll expire in a min")
    message_list.insert(tkinter.END, "1: Thanks")
    message_list.insert(tkinter.END, "1: Want to play DnD at break?")

#tkinter stuff. When I close the window, tell the server so it can remove you properly.
def on_closing():
    #called when window closed
    WipeList()
    my_message.set("{quit}")
    send()
    top.destroy()
    sys.exit()

#I don't know why this is a function
def WipeList():
    message_list.delete(0, tkinter.END)

#locally set the label. I spammed this in the server script though,
#it'll usually be on *something* server assigned. Yes, I realise that italics
#don't work in comments.
def SetLabelStatus(text):
    statusLabel["text"] = text

#removes the end. This runs as a seperate thread
def MessageListTrim():
    while True:
        time.sleep(0.1)
        if message_list.size() > backlogLength:
                message_list.delete(0)

#tkinter magic. 95% from stackoverflow. I figure you can work out the syntax in 6 months
#as well as I can now, so I won't bother.
top = tkinter.Tk()

#disguise that shit
top.title("Word")
top.call('wm', 'iconphoto', top._w, tkinter.PhotoImage(file='wordlogo.png'))
top.configure(background="white")


messages_frame = tkinter.Frame(top)
messages_frame.configure(background="white")

my_message = tkinter.StringVar()
my_message.set("")

scrollbar = tkinter.Scrollbar(messages_frame)
scrollbar.configure(background="white")

if DoCustom == True:
    listHeight = int(input("List height? 20 is sensible> "))
    listWidth = int(input("List width? 50 is sensible... > "))

else:
    listHeight = 20
    listWidth = 50
message_list = tkinter.Listbox(messages_frame, height = listHeight, width = listWidth, yscrollcommand=scrollbar.set)
message_list.configure(background="white")

scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
message_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)

messages_frame.pack()

entry_field = tkinter.Entry(top, textvariable=my_message, width = listWidth)
entry_field.bind("<Return>", send)
entry_field.configure(background="white")
entry_field.pack()

send_button = tkinter.Button(top, text="Send", command=send)
send_button.configure(background="white")
send_button.pack()

statusLabel = tkinter.Label(top, text="-")
statusLabel.configure(background="white")
statusLabel.pack()

top.protocol("WM_DELETE_WINDOW", on_closing)

#phew, end of that tkinter stuff. 
#I hope this doesn't need explaining
if DoCustom == True:
    backlogLength = int(input("What length should the backlog be before removing the end? > "))
    host = input("Enter host: ")
    port = input("Enter port: ")

else:
    #default settings
    backlogLength = 20
    host = "127.0.0.1"
    #host = "86.31.133.208"
    #host = "192.168.0.35"
    port = 34000
    allowRemoteAccess = True

#now this is a brilliant thing you can do in python that is 100% from the internet.
if not port:
    port = 34000

else:
    port = int(port)

Buffer_size = 1024
Address = (host, port)
#AF_INET means TCP
client_socket = socket(AF_INET, SOCK_STREAM)

tries = 0

#tries to connnect. 
while True:
    if tries < 20:
       tries = tries + 1
       
    try:
        print("Attempting to connect")
        client_socket.connect(Address)
        print("Successful connection established.")
        break
        
    except ConnectionRefusedError:
        print("Connection refused. Retrying in " + str(tries) + " seconds.")
        SetLabelStatus("Error. Retrying in " + str(tries) + " seconds.")
        time.sleep(tries)
        continue

#lol, I set this before I started the gui...
SetLabelStatus("Starting receive thread.")
Thread(target=ReceiveFromServer).start()

#starts message cropper
Thread(target=MessageListTrim).start()
SetLabelStatus("Done!")

tkinter.mainloop()  # Starts GUI execution.
