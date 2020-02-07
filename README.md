# chatApp

A work-in-progress chat app designed to circumvent school systems.

  

Includes numerous anti-detection and plausible denial features.

Currently unencrypted, although passwords are not stored in plain text.

  

# Known problems

Found when I tested it with someone else who wasn't using it as intended

- Kicking doesn't work. Like, it tells you you've been kicked... then it... kinda... lets you continue as normal.

- When someone exits, you take over their account

- People not on the name list are totally there communicating. It's broken.

- It's broken.

- everything is broken

- Spamming is extremely easy

- Messages don't wrap to the next line

- When you have a high ping, you don't see the first "what is your name" message

- Everything is broken

- When doing PM's, kicks, bans, etc it gets the name from all the characters past a certain point... including spaces.

- You can have two people with the same names

  

# To do

- Rewrite it
  

# What I want when I remake it.

- Connection: name list

- Accounts system

- Encryption, at least for sending passwords

- Make your own client write your message to the list and the server send to everyone but you

- Fewer features: It's bloated

- Proper authentication

- A database with names, connection objects, and (Hashed and salted) password

- Don't use tkinter: I hate it.

- USE CLASSES. SERIOUSLY.


# Rebuild roadmap

- Tomorrow, I will look into my graphical framework, crypto libraries, and make a proper plan of the accounts system and how everything will communicate. I will list every function in the server; the client can be more ambigious, it doesn't do as much.

  

- The school week and weekend after that (I have school, it'll be slow) I want to make accounts and databases work: I want to fake (with input() and print()) the whole process of first connecting, enter the password to be allowed to make an account, enter your name, give it a password (hashed and salted) and then come back another time, log in, enter password, etc.

  

- The school week after that I want to make a dev client for communicating with my new server while I write it and build the server's core network backend (No more raw UTF8 and writing everything you receive: No, this is gonna be my own protocol, and it might even have emojis!), with cryptography in mind.

  

- The weekend after that I want to finish that.

  

- The school week after that I want to put in proper cryptography/finish that. By the end of it, I want my dev clients talking to each other!

  

- Then over the weekend after that, I want to get the backend for the proper client going (Designed from the ground up with my new protocols, instead of things slapped on in the dev version.)

  

- For 3 weeks after that I want to put together the disguised client. Properly disguised, not this "Looks like word in the taskbar" bullshit.

  

# Notes, per the first day (OK, more like hour) of the rebuild roadmap

- OK, I know the type of database I am going to use. It's extremely sophisticated. It's a set of dictionaries in a list saved to a file. I did research it, and considering I am only going to have like 10 pieces of data I'll be OK.


# My functions/classes

# Server communications
<<<<<<< HEAD
- privateMessageFromServer(Username) - It'll extrapolate the rest by accessing the database. 
- broadcast(Username) - Sends to all users but the username. 
- InternalMessage(Username) - This sends an internal message, such as "Ping" or "You have been kicked" or "Set the input - mode to stars, we're receiving a password."
- IsOnline(Username) - Sends a "ping", not as in the ICMP one but a manual one to check connection.

# Cryptography
- KeyExchange() - Dark magic. I'll work this one out later.
- Encrypt(text, publicKey)
- Decrypt(text, privateKey)
- HashPassword() 
=======

- privateMessageFromServer(Username) - It'll extrapolate the rest by accessing the database.

- broadcast(Username) - Sends to all users but the username.

- InternalMessage(Username) - This sends an internal message, such as "Ping" or "You have been kicked" or "Set the input - mode to stars, we're receiving a password."

- IsOnline(Username) - Sends a "ping", not as in the ICMP one but a manual one to check connection.

  

# Cryptography

- KeyExchange() - Dark magic. I'll work this one out later.

- Encrypt(text, publicKey)

- Decrypt(text, privateKey)

- HashPassword()

  
>>>>>>> d14bc0460e4ca24abd58b9f86ea97d85919d561a

# Accounts

Keep in mind, the username is basically the sole account identifier.

An account contains (With example values):
<<<<<<< HEAD
{
Username : "Alex", 
=======

{Username : "Alex",

>>>>>>> d14bc0460e4ca24abd58b9f86ea97d85919d561a
Password : "sjfhjsbfh9w8fn028h02n etc",

PendingPms : {Sender: "Luke", Message : "Hello!"},

isAdmin : True

isOnline : True

isOP: True

connectionObject: {IP : 127.0.0.1, PROTOCOL : TCP, NOTES : "I am not copying an entire sockets connection object"}

}

NewAccount(Username, password[unhashed at this point], isAdmin)

GetAccountData(Username, key you want)

PushAccountData(Username, key you want to replace/add, value)

DeleteAccount(Username, password-hashed)

  

# Miscellaneous

PrintLog() - prints and logs to a file at the same time

  

# Program structure

I want there to be a loop accepting connections and referring to a thread called Main(), that asks for account details.

At this point they can also create an account, if they have a password. Then, they go into the loop of "I send message, message goes to everyone, everyone reads message, people reply, I see message.

<<<<<<< HEAD
I also want a couple of other threads to be run. I also want one to periodically ping every account set to online (A manual ping is done on logging in and they are set to online) and update the IsOnline field (The main thread closes if this is false). I want one to go through the pendingPms of every online user and send them the PM if there is one. 
=======
  I also want a couple of other threads to be run. One goes through all the clients and, if they have shouldBan to true, disconnects them. I also want one to periodically ping every account set to online (A manual ping is done on logging in and they are set to online) and update the IsOnline field (The main thread closes if this is false). I want one to go through the pendingPms of every online user and send them the PM if there is one.

  
>>>>>>> d14bc0460e4ca24abd58b9f86ea97d85919d561a

# Features I want

- PM's

- Accounts (Obviously)

- The old /exit -a, /wipe -a, and /faketext -a

- Admin status to be account based

- Non admins be able to elevate to admin for a single message, in "sudo like" fashion, with a password.

- People to be able to change their passwords, elevate to admin, et cetera

- The OP being able to make people admins without giving them the password

- /broadcast to pretend to be the server - peace of cake to implement and quite entertaining

- /here, /online - display everyone currently online

- /namelist, /people, /everyone, /users - display everyone registered

- /ping - shows ping time to the server. Takes a while to implement but a useful tool.

- /status - gives basically all the data in their username dict.

# Now for the old readme

# Commands

Client Side

- /wipe, /clear - Clears chat history locally.

- /exit, /quit - Closes client locally.

- /faketext - Clears chat history and replaces it with a fake "lesson friendly" conversation. The conversation is shit, replace it.

  

Server side

- /pm [name] - open a PM prompt with another person. Make sure there are no spaces at the end... I'll fix that at some point. The spaces rule applies to all the other commands that take names for arguments.

- /ban [name] - pretty redundant, useful only for blocking offensive usernames, considering people can just reconnect with a different name. Note this blocks the name after the random characters, and won't ban anyone currently with that name. A recommended procedure for someone with a username you don't like is to ban the base username (E.G. in 2n0An1-Mark just ban Mark) then kick the person. Requires administrator.

- /unban [name] - Undoes the above. Requires administrator.

- /kick [name] - kicks someone but only once they have sent a message. I need to fix this one too. I don't expect to use these much or at all tbh. Requires administrator.

- /broadcast [message] - sends a message but without your name at the front, basically. It's more for future proofing if I implement channels etc.

- /wipe -a - this is a good contender for the most useful command. Sends a authenticated message from the server (using my patented HashTime technology) to wipe everyone's chat history. Requires administrator.

- /exit -a - Sends a authenticateMade d message from the server to close everyone's chats. Requires administrator.

- /faketext -a - Sends an authenticated message from the server to replace everyone's chats with a "lesson friendly" conversation. Requires administrator.

- /verify - more of a diagnostic tool, this writes your client HashTime and tells the server to send theirs. Not appropriate for security-even ignoring the multitude of problems with HashTime, the server has direct write and wipe control over your message feed, where your client HashTime appears.

- /here, /namelist, /users - prints all users currently in names database. May or may not be connected.

- /status - gives port, client IP, client name, and client admin status.

- /pingTest - gets ping in ms

- sudo shutdown server - A command for if there is some need to shut down the server. Requires higher authentication than administrator, which only I know.

  

# How do I get admin?

If a list of words (written below) are in your username, it'll prompt you for the password. Enter it, and you'll be admin. Enter wrong, and you'll be kicked and have to try again or pick a different username. Don't bother looking for it in the code, it's hashed and salted.

  

The words (case insensitive) are:

- Alex

- System

- Server

- Admin

- Root

- Administrator

- Sudo
