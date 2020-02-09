import tkinter, time
from tkinter import messagebox
"""
class GUI:
    #stolen from the internet. I *hate* tkinter. Everything outside of the gui class is mine. 
    cal = Tk()
    cal.title("Notepad")
    cal.geometry("555x344")
    m1=Menu(cal,tearoff=0,font="italic 10 ")
    m2=Menu(m1,tearoff=0,font="italic 10 ")
    m2.add_command(label="New File",font="italic 10")
    m2.add_separator()
    m2.add_command(label="Open",font="italic 10")
    m2.add_separator()
    m2.add_command(label="Save",font="italic 10 ")
    m2.add_command(label="Save as",font="italic 10")
    m2.add_separator()
    m2.add_command(label="Page Setup",font="egyptian 10")
    m2.add_cascade(label="Exit")
    m1.add_cascade(label="File",menu=m2)
    cal.config(menu=m1)

    m3=Menu(m1,tearoff=0)
    m3.add_command(label="Cut",font="italic 10 ")
    m3.add_separator()
    m3.add_command(label="Copy",font="italic 10 ")
    m3.add_separator()
    m3.add_command(label="Paste",font="italic 10")
    m3.add_command(label="go to",font="italic 10")
    m3.add_separator()
    m3.add_command(label="Select All",font="italic 10")
    m3.add_separator()
    m3.add_command(label="Delete",font="italic 10")
    cal.config(menu=m1)
    m1.add_cascade(label="Exit",menu=m3,font="italic 10 ")
    m4=Menu(m1,tearoff=0)
    m4.add_command(label="Font..",font="italic 10")
    m4.add_separator()
    m4.add_command(label="Word Wrap",font="italic 10")

    cal.config(menu=m1)
    m1.add_cascade(label="View",menu=m4,font="italic 10")
    m5=Menu(m1,tearoff=0)
    m5.add_command(label="Status Bar",font="italic 10")
    cal.config(menu=m1)
    m1.add_cascade(label="Format",menu=m5,font="italic 10")
    m6=Menu(m1,tearoff=0)
    m6.add_command(label="View Help",font="italic 10")
    m6.add_separator()
    m6.add_command(label="About Help",font="italic 10")
    cal.config(menu=m1)
    m1.add_cascade(label="Help",menu=m6,font="italic 10")

    #from here, it's mine
    messages_frame = messages_frame = Frame(cal)
    messages_frame.configure(background="black")
    message_list = Listbox(messages_frame, height = 344, width = 555)
    message_list.configure(background="black")
    message_list.insert(END, "Hello")


GUI.cal.mainloop()

"""

def send():
    a = 1

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
entry_field.bind("<Return>", send)
entry_field.configure(background="white")
entry_field.pack()

send_button = tkinter.Button(top, text="Send", command=send)
send_button.configure(background="white")
send_button.pack()

statusLabel = tkinter.Label(top, text="-")
statusLabel.configure(background="white")
statusLabel.pack()

tkinter.mainloop()