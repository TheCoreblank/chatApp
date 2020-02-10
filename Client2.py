import tkinter, time
from tkinter import messagebox
import hashlib
from threading import *
from socket import AF_INET, socket, SOCK_STREAM

class Communications():
    HashNextMessage = False
    sendpings = False
    def InternalSend(text):
        client_socket.send(Communications.Encode(text))

    def Send(event=None):
        message = GUI.my_message.get()
        GUI.my_message.set("")

        if message == "/wipe" or message == "/clear":
            GUI.WipeList()

        elif message == "/exit" or message == "/quit":
            Communications.InternalSend("/quit")
            client_socket.close()
            GUI.top.destroy()
            GUI.top.quit()
            sys.exit()

        elif Communications.HashNextMessage == False:
            Communications.InternalSend(message)
        
        else:
            GUI.SetLabelStatus("Hashing...")
            Communications.HashNextMessage = False
            print("Hashing message")
            #Good joke, "securely." If anyone is reading this:
            #I try my best, but only consider trusting me with
            #passwords once I have a Computer Science degree. 
            #I just looked it up in a book and went through some StackOverflow posts.
            message = Cryptography.Hash(message)
            Communications.InternalSend(message)
            GUI.SetLabelStatus(" ")
            GUI.entry_field["show"] = ""


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
                    GUI.SetLabelStatus("Hashing next message...")
                    GUI.entry_field["show"] = "*"

            elif "[SERVER INTERNAL-INTERNAL]" in message:
                if "SENDPINGS=TRUE" in message:
                    Communications.sendpings = True

            else:
                GUI.message_list.insert(tkinter.END, message)

    def Encode(text):
        return bytes(text, "utf8")
        
class Cryptography:
    def Hash(text):
        #PBKDF2
        salt = "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"       
        #Don't remove comment                                                     65536 × 8
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
    top = tkinter.Tk()

    #disguise that shit
    top.title("untitled - Notepad")
    top.call('wm', 'iconphoto', top._w, tkinter.PhotoImage(file='wordlogo.png'))
    top.configure(background="white") 

    menu = tkinter.Menu(top,tearoff=0,font="italic 10 ")
    menu.add_command(label="File",font="italic 10")
    menu.add_separator()
    menu.add_command(label="Edit",font="italic 10")
    menu.add_separator()
    menu.add_command(label="Format",font="italic 10")
    menu.add_separator()
    menu.add_command(label="View",font="italic 10")
    menu.add_separator()
    menu.add_command(label="Help",font="italic 10")
    menu.add_separator()

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

    def WipeList():
        GUI.message_list.delete(0, tkinter.END)

    def SetLabelStatus(text):
        GUI.statusLabel["text"] = text
        print("Set label status to " + text)

    def LengthCheckThread():
        while True:
            time.sleep(0.1)
            if GUI.message_list.size() > backlogLength:
                GUI.message_list.delete(0)

#<copied code> Copied from Client2 because it's pretty good code, if I say so myself. 
#default settings
backlogLength = 20
host = "127.0.0.1"
#host = "86.31.133.208"
#host = "192.168.0.35"
port = 34000

#now this is a brilliant thing you can do in python that is 100% from the internet.
if not port:
    port = 443

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