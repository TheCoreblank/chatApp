# chatApp

A work-in-progress chat app designed to circumvent school systems.

  

Includes numerous anti-detection and plausible denial features.

Currently unencrypted, although passwords are not stored in plain text.

# IMPORTANT

It has a lot of problems. Just look at some of the older readme's!

Because of that, I am doing a full rewrite with an account system. That's in Server3.py. I am testing it with Client.py still (the protocols are still usably compatible) though soon I will create a new dev client in DevelopmentClient.py. Then I'll make a Client2.py, where I rebuild it to be disguised as notepad and be designed to work with Server3.py from the ground up. It'll probably be partially compatible with Server2.py, but just use the old client for that.

If someone actually wants to use this script, then keep in mind:

Server 2 has:
- Better error handling
- More features
- More testing
- Not developed anymore

Server 3 has
- PASSWORDS ARE STORED IN PLAIN TEXT
- Not as good error handling
- Less features
- No properly compatible client
- Has only been tested by the developer
- Is still in active development
- Has a proper account system
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
