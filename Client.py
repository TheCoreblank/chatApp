#client side script
from socket import AF_INET, socket, SOCK_STREAM
from threading import *
import tkinter, time
import sys, hashlib

lastUpIndicator = 0
isUp = False

def CalculateAuthCode():
    authCode = int(int(time.time()) / int(10))
    authCode = hashlib.sha512(bytes(authCode, "utf8")).hexdigest()
    return authCode
    
def ReceiveFromServer():
    while True:
        try:
            message = client_socket.recv(Buffer_size).decode("utf8")

            if "-- EXIT AUTHORISE --" in message:
                print("Received auth message...")
                
                if CalculateAuthCode() in message:
                    print("Auth correct. Exiting.")
                    WipeList()
                    top.destroy()
                    sys.exit()

                else:
                    print("Auth incorrect. Not responded.")

            if "-- WIPE AUTHORISE --" in message:
                print("Received auth message...")
                authCode = int(int(time.time()) / int(10))
                if CalculateAuthCode() in message:
                    print("Auth correct. Wiping..")
                    WipeList()

                else:
                    print("Auth incorrect. Not responded.")

                    
            message_list.insert(tkinter.END, message)

            if message_list.size() > backlogLength:
                message_list.delete(0)
            
        except OSError: #may be a client exit
            break
        

def send(event=None): #event passed by buttons
    #handles sending of messages
    message = my_message.get()
    my_message.set("")

    client_socket.send(bytes(message, "utf8"))

    if message == "{wipe}":
        WipeList()
    
    if message == "{quit}":
        WipeList()
        client_socket.close()
        top.destroy()
        top.quit()
        sys.exit()
    
def on_closing():
    #called when window closed
    WipeList()
    my_message.set("{quit}")
    send()
    top.destroy()
    sys.exit()

def WipeList():
    message_list.delete(0, tkinter.END)
    message_list.delete(0)
    
top = tkinter.Tk()



top.title("Frontend V0.1")

messages_frame = tkinter.Frame(top)

my_message = tkinter.StringVar()
my_message.set("")

scrollbar = tkinter.Scrollbar(messages_frame)

listHeight = int(input("List height? 20 is sensible> "))
listWidth = int(input("List width? 50 is sensible... > "))
message_list = tkinter.Listbox(messages_frame, height = listHeight, width = listWidth, yscrollcommand=scrollbar.set)

scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
message_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)

messages_frame.pack()

entry_field = tkinter.Entry(top, textvariable=my_message)
entry_field.bind("<Return>", send)
entry_field.pack()

top.protocol("WM_DELETE_WINDOW", on_closing)

backlogLength = int(input("What length should the backlog be before removing the end? > "))
host = input("Enter host: ")
port = input("Enter port: ")

if not port:
    port = 34000
else:
    port = int(port)

Buffer_size = 1024
Address = (host, port)
client_socket = socket(AF_INET, SOCK_STREAM)

tries = 0

    
while True:
    if tries < 20:
       tries = tries + 1
       
    try:
        client_socket.connect(Address)
        print("Succesful connection established.")
        break
        
    except ConnectionRefusedError:
        print("Connection refused. Retrying in " + str(tries) + " seconds.")
        time.sleep(tries)
        continue

receive_thread = Thread(target=ReceiveFromServer)
receive_thread.start()

tkinter.mainloop()  # Starts GUI execution.
