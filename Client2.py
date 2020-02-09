import tkinter, time
from tkinter import messagebox

class Communications:
    def Send(event=None):
        a = 1
        #TODO Send

    def PeriodicPing():
        a = 1
        #TODO Periodic ping
    
    def Receive():
        a = 1
        #TODO Receive

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

    entry_field = tkinter.Entry(top, textvariable=my_message, width = (listWidth-6))
    entry_field.bind("<Return>", Communications.Send)
    entry_field.configure(background="white")
    entry_field.pack()

    def WipeList():
        a = 1
        #TODO Wipelist


tkinter.mainloop()

