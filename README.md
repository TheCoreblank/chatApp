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
- When you have a big ping, you don't see the first "what is your name" message
- Everything is broken
- When doing PM's, kicks, bans, etc it gets the name from all the characters past a certain point... including spaces.
- You can have two people with the same names

# To do
- Fix the above
- Have a dict of connection:name
- Make it ping the client periodically to establish who is connected

# For when I rebuild
- Connection: name list
- Accounts system
- Encryption, at least for sending passwords
- Make your own client write your message to the list and the server send to everyone but you
- Fewer features: It's bloated
- Proper authentication
- A database with names, connection objects, and (Hashed and salted) password
- Don't use tkinter: I hate it. 

# Rebuild roadmap
- Tomorrow, I will look into my graphical framework, crypto libraries, and make a proper plan of the accounts system and how everything will communicate. I will list every function in the server; the client can be more ambigious, it doesn't do as much.

- The school week and weekend after that (I have school, it'll be slow) I want to make accounts and databases work: I want to fake (with input() and print()) the whole process of first connecting, enter the password to be allowed to make an account, enter your name, give it a password (hashed and salted) and then come back another time, log in, enter password, etc. 

- The school week after that I want to make a dev client for communicating with my new server while I write it and build the server's core network backend (No more raw UTF8 and writing everything you receive: No, this is gonna be my own protocol, and it might even have emojis!), with cryptography in mind.

- The weekend after that I want to finish that.

- The school week after that I want to put in proper cryptography/finish that. By the end of it, I want my dev clients talking to each other!

- Then over the weekend after that, I want to get the backend for the proper client going (Designed from the ground up with my new protocols, instead of things slapped on in the dev version.)

- For 3 weeks after that I want to put together the disguised client. Properly disguised, not this "Looks like word in the taskbar" bullshit.

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

# Is this unethical?
# <rant>
Yes, unless it's in REP, PSHE, Human Languages, Knitting, or another awful subject or your school doesn't do computer science or try to find someone to do computer science, in which case you are teaching yourself what your school neglected to teach you by setting up the server. It's also entirely ethical if your school did a computer ban then wondered why students weren't able to do their online homework at break and lunch. If your school did that, like mine, they are clearly too stupid for you to learn anything in lessons and you should find something more productive to do with your time, like browsing github.

# </rant>