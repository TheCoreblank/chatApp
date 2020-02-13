import tkinter, time
from tkinter import messagebox
import hashlib
from threading import *
from socket import AF_INET, socket, SOCK_STREAM
from time import strftime
import os

class PingTest():
    FirstCapture = 0
    SecondCapture = 0

class Communications():
    HashNextMessage = False
    sendpings = False
    freezeMessagesBecauseOfFakeText = False

    #Speed restrictions
    lastMessageTransmitTime = 0
    messagesPerSecond = 5
    messageRestrictionPeriod = 1 / messagesPerSecond
    restrictionPeriodPunishment = 2
    nextAllowedMessageTime = 0

    def InternalSend(text):
        client_socket.send(Communications.Encode(text))

    def Send(event=None):
        message = GUI.my_message.get()
        GUI.my_message.set("")
        IsMessageToEarly = False

        if Communications.freezeMessagesBecauseOfFakeText == True and not "/faketext" in message and not "/wipe" in message and not "/status" in message:
            GUI.message_list.insert(tkinter.END, message)
            GUI.FakeTextList.append(message)

        if Communications.nextAllowedMessageTime > time.time():
            IsMessageToEarly = True
            GUI.message_list.insert(tkinter.END, "You are sending messages too quickly. Wait " + str(Communications.restrictionPeriodPunishment) + " seconds..")
            Communications.nextAllowedMessageTime = time.time() + Communications.restrictionPeriodPunishment
            GUI.SetLabelStatus("You can write again at " + str(Communications.nextAllowedMessageTime))

        if message == "/wipe" or message == "/clear":
            GUI.WipeList()

        elif "/faketext" in message:
            if "-end" in message and Communications.freezeMessagesBecauseOfFakeText == True:
                GUI.SwitchToMessageMode()
            elif Communications.freezeMessagesBecauseOfFakeText == False and not "-end" in message:
                GUI.FakeText()

        elif "/status" in message:
            if Communications.freezeMessagesBecauseOfFakeText == True:
                GUI.SetLabelStatus("Notepad Mode")

            if Communications.freezeMessagesBecauseOfFakeText == False:
                GUI.SetLabelStatus("Chat Mode")

        elif "/ping" in message and IsMessageToEarly == False:
            PingTest.FirstCapture = time.time()
            Communications.InternalSend("[PING: REPLY URGENTLY]")
            Communications.nextAllowedMessageTime = time.time() + Communications.messageRestrictionPeriod

        elif message == "/exit" or message == "/quit":
            Communications.InternalSend("/quit")
            client_socket.close()
            GUI.top.destroy()
            GUI.top.quit()
            sys.exit()

        elif Communications.HashNextMessage == False and IsMessageToEarly == False and Communications.freezeMessagesBecauseOfFakeText == False:
            Communications.InternalSend(message)
            Communications.nextAllowedMessageTime = time.time() + Communications.messageRestrictionPeriod
        
        elif IsMessageToEarly == False and Communications.freezeMessagesBecauseOfFakeText == False:
            Communications.HashNextMessage = False
            print("Hashing message")
            #Good joke, "securely." If anyone is reading this:
            #I try my best, but only consider trusting me with
            #passwords once I have a Computer Science degree. 
            #I just looked it up in a book and went through some StackOverflow posts.
            message = Cryptography.Hash(message)
            Communications.InternalSend(message)
            GUI.entry_field["show"] = ""
            Communications.nextAllowedMessageTime = time.time() + Communications.messageRestrictionPeriod
        
        if not "/faketext" in message and not "/wipe" in message and not "/clear" in message and not "/status" in message:
            GUI.SetLabelStatus("Sent: " + message)


    def PeriodicPing():
        while True:
            time.sleep(10)
            if Communications.sendpings == True:
                Communications.InternalSend("[CLIENT PING UPDATE]")
    
    def Receive():
        while True:
            #blocks the thread
            message = client_socket.recv(Buffer_size).decode("utf8")

            print(str(message))

            #These are ordered in most>least often received to increase efficiency.
            #For a broadcast, it only has to check the first one. In the rare case of
            #a "Pings on" message, it takes longer.

            if "EVERYONE OPEN FAKETEXT, ID CODE: e325482c26c995caad73f1987ff5c1b8c94fb9e68f9608f87949b81c5dfb2255f7939e8aaef8e0e82db45a293a1c61d79262bd05d2d72ec06e6bb7ee88d4d1af" in message:
                GUI.FakeText()

            if "EVERYONE EXIT NOW, ID CODE: e325482c26c995caad73f1987ff5c1b8c94fb9e68f9608f87949b81c5dfb2255f7939e8aaef8e0e82db45a293a1c61d79262bd05d2d72ec06e6bb7ee88d4d1af" in message:
                GUI.FakeText()
                os._exit(1)

            if Communications.freezeMessagesBecauseOfFakeText == False:
                if "[PING: URGENT REPLY]" in message:
                    PingTest.SecondCapture = time.time()

                    Difference = PingTest.SecondCapture - PingTest.FirstCapture
                    Difference = Difference * 1000
                    Difference = str(Difference)[:5]

                    GUI.message_list.insert(tkinter.END, "Ping:")
                    GUI.message_list.insert(tkinter.END, Difference + "ms")

                if "Welcome to the chatroom" in message:
                    Communications.sendpings = True

                if "[SERVER INTERNAL-BROADCAST]" in message:
                    message = message[27:]
                    GUI.message_list.insert(tkinter.END, message)

                elif "[SERVER INTERNAL-PM MESSAGE]" in message:
                    message = message[28:]
                    message = "SERVER[PM-H]: " + message 
                    GUI.message_list.insert(tkinter.END, message)

                elif "[SERVER INTERNAL-LOW LEVEL-PM MESSAGE]" in message:
                    message = message[38:]
                    message = "Server[PM-L]: " + message
                    GUI.message_list.insert(tkinter.END, message)
                
                elif "[SERVER INTERNAL-LOW LEVEL-INTERNAL]" in message:
                    if "PASSWORD ENTRY FIELD" in message:
                        Communications.HashNextMessage = True
                        GUI.entry_field["show"] = "*"
                        GUI.SetLabelStatus("Securely hashing and encrypting next message with over 524,288 iterations")

                    if "Enter auth to access" in message:
                        Communications.InternalSend("RESPONSE, SERVER CLIENT CONTAINS REMOTE SHUTDOWN.")

                else:
                    GUI.message_list.insert(tkinter.END, message)

    def Encode(text):
        return bytes(text, "utf8")
        
class Cryptography:
    def Hash(text):
        #PBKDF2
        salt = "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"       

        text = hashlib.pbkdf2_hmac('sha512', bytes(text, "utf8"), bytes(salt, "utf8"), 524288).hex()
        
        #My own iterating implementation, low security but a nice extra
        i = 0 
        while True:
            i = i + 1
            text = str(hashlib.sha512(bytes(str(text) + str(i) + str(salt) + 'f8weucrwirun3wurifiwshfkfdsifjisdjfisjfiosjflsjfiljdslkfjllhwifiwfhownowur8o2rn82u8onu328cu482bu82u48b23u89', 'utf8')).hexdigest())
            if i == 8192:
                break
        
        return str(text)


class GUI:
    FakeTextList = ["Notes: "]
    MessageList = ""
    top = tkinter.Tk()

    #disguise that shit
    top.title("untitled - Notepad")
    #top.call('wm', 'iconphoto', top._w, tkinter.PhotoImage(file='wordlogo.png'))
    top.configure(background="white") 

    menu = tkinter.Menu(top,tearoff=0,font="italic 10 ")

    fileMenu = tkinter.Menu(menu)
    fileMenu.add_command(label="New", font="italic 10")
    fileMenu.add_command(label="Open...", font="italic 10")
    fileMenu.add_command(label="Save", font="italic 10")
    fileMenu.add_command(label="Save As...", font="italic 10")
    fileMenu.add_command(label="Page Setup...", font="italic 10")
    fileMenu.add_command(label="Print...", font="italic 10")
    fileMenu.add_command(label="Exit", font="italic 10")
    menu.add_cascade(label="File",font="italic 10", menu=fileMenu)

    editMenu = tkinter.Menu(menu)
    editMenu.add_command(label="Undo")
    editMenu.add_command(label="Cut")
    editMenu.add_command(label="Copy")
    editMenu.add_command(label="Paste")
    editMenu.add_command(label="Delete")
    #editMenu.add_seperator()
    editMenu.add_command(label="Find")
    editMenu.add_command(label="Find Next")
    editMenu.add_command(label="Replace")
    editMenu.add_command(label="Go to")
    #editMenu.add_seperator()
    editMenu.add_command(label="Select All")
    editMenu.add_command(label="Time/Date")

    menu.add_cascade(label = "Edit", font="italic 10", menu = editMenu)

    formatMenu = tkinter.Menu(menu)

    formatMenu.add_command(label="Word Wrap")
    formatMenu.add_command(label="Font")

    menu.add_cascade(label = "Format", font = "italic 10", menu = formatMenu)

    menu.add_separator()

    viewMenu = tkinter.Menu(menu)
    viewMenu.add_command(label = "Status Bar")
    
    menu.add_cascade(label = "View", font = "italic 10", menu = viewMenu)
    menu.add_separator()

    helpMenu = tkinter.Menu(menu)
    helpMenu.add_command(label="View Help")
    helpMenu.add_command(label="About Notepad")
    menu.add_cascade(label = "Help", font = "italic 10", menu = helpMenu)

    top.config(menu=menu)

    messages_frame = tkinter.Frame(top)
    messages_frame.configure(background="white")

    my_message = tkinter.StringVar()
    my_message.set("")

    scrollbar = tkinter.Scrollbar(messages_frame)
    scrollbar.configure(background="white")

    listHeight = 20
    listWidth = 100
    message_list = tkinter.Listbox(messages_frame, height = listHeight, width = listWidth, yscrollcommand=scrollbar.set)
    message_list.configure(background="white")

    scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
    message_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)

    messages_frame.pack()

    entry_field = tkinter.Entry(top, textvariable=my_message, width = (listWidth))
    entry_field.bind("<Return>", Communications.Send)
    entry_field.configure(background="white")
    entry_field.pack()

    statusLabel = tkinter.Label(top, text="-")
    statusLabel.configure(background="white")
    statusLabel.pack()

    top.protocol("WM_DELETE_WINDOW", "GUI.on_closing")

    def on_closing():
        Communications.InternalSend("/exit")
        top.destroy()

    def WipeList():
        GUI.message_list.delete(0, tkinter.END)
        GUI.SetLabelStatus("Ln 0, Col 0")

    def SetLabelStatus(text):
        GUI.statusLabel["text"] = text
        print("Set label status to " + text)

    def LengthCheckThread():
        while True:
            time.sleep(0.1)
            if GUI.message_list.size() > backlogLength:
                GUI.message_list.delete(0)

    def GetListData():
        return list(GUI.message_list.get(0, tkinter.END))

    def WriteListData(messageList):
        GUI.WipeList()
        for line in messageList:
            GUI.message_list.insert(tkinter.END, line)

    def FakeText():
        GUI.MessageList = GUI.GetListData()
        GUI.WipeList()
        GUI.SetLabelStatus("Untitled - Notepad - "  + strftime("%Y-%m-%d"))
        Communications.freezeMessagesBecauseOfFakeText = True
        for line in GUI.FakeTextList:
            GUI.message_list.insert(tkinter.END, line)

    def SwitchToMessageMode():
        Communications.freezeMessagesBecauseOfFakeText = False
        GUI.WipeList()
        GUI.WriteListData(GUI.MessageList)


print("Please enter your faketext. Newlines are defined by + symbols.")
fakeText = input("> ")
fakeText = fakeText.split("+")
GUI.FakeTextList = fakeText

#<copied code> Copied from Client2 because it's pretty good code, if I say so myself. 
#default settings
backlogLength = 20
host = "127.0.0.1"
#host = "86.31.133.208"
#host = "192.168.0.35"
port = 34000

#now this is a brilliant thing you can do in python that is 100% from the internet.
if not port:
    port = 34000

else:
    port = int(port)

Buffer_size = 2048
Address = (host, port)
#AF_INET means TCP
client_socket = socket(AF_INET, SOCK_STREAM)

tries = 0

#tries to connect. 
#*Auto adapting port technologies to compensate for pre-allocated ports* this could be from a shitty hacking movie
while True:
    try:
        print("Attempting to connect")
        client_socket.connect(Address)
        print("Successful connection established.")
        break

    except ConnectionRefusedError:
        if port == 34000:
            port = 34001
            print("Port set to 34001")

        elif port == 34001:
            port = 34000
            print("Port set to 34000")

        Address = (host, port)
        print("Connection refused. Retrying in " + str(tries) + " seconds.")
        time.sleep(tries)

        if tries < 20:
            tries = tries + 1

        continue

#</copied code>
Thread(target=Communications.PeriodicPing).start()
Thread(target=Communications.Receive).start()
Thread(target=GUI.LengthCheckThread).start()

tkinter.mainloop()
