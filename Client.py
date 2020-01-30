#client side script
from socket import AF_INET, socket, SOCK_STREAM
from threading import *
import tkinter, time
import sys

def ReceiveFromServer():
    while True:
        try:
            message = client_socket.recv(Buffer_size).decode("utf8")

            if message == "-- EXIT AUTHORISE --":
                top.destroy()
                sys.exit()
                print("Exit received but not executed.")
                
            message_list.insert(tkinter.END, message)
            
        except OSError: #may be a client exit
            break
        

def send(event=None): #event passed by buttons
    #handles sending of messages
    message = my_message.get()
    my_message.set("")

    client_socket.send(bytes(message, "utf8"))
    
    if message == "{quit}":
        client_socket.close()
        top.destroy()
        top.quit()
        sys.exit()

def on_closing():
    #called when window closed
    my_message.set("{quit}")
    send()
    top.destroy()
    sys.exit()

top = tkinter.Tk()



top.title("Frontend V0.1")

messages_frame = tkinter.Frame(top)

my_message = tkinter.StringVar()
my_message.set("")

scrollbar = tkinter.Scrollbar(messages_frame)

message_list = tkinter.Listbox(messages_frame, height = 20, width = 50, yscrollcommand=scrollbar.set)

scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
message_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)

messages_frame.pack()

entry_field = tkinter.Entry(top, textvariable=my_message)
entry_field.bind("<Return>", send)
entry_field.pack()

top.protocol("WM_DELETE_WINDOW", on_closing)

host = input("Enter host: ")
port = input("Enter port: ")

if not port:
    port = 33000
else:
    port = int(port)

Buffer_size = 1024
Address = (host, port)
client_socket = socket(AF_INET, SOCK_STREAM)

tries = 0
while True:
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

#todo-
#add timestamps
#add "status"
#improve interface
