
#!/usr/bin/env python
# coding: utf-8

# Copyright (C) 2010 Arthur Furlan <afurlan@afurlan.org>
# 
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
# 
# On Debian systems, you can find the full text of the license in
# /usr/share/common-licenses/GPL-3


from jabberbot import JabberBot, botcmd
from datetime import datetime
import urllib
import re
import logging
logging.basicConfig()

class MUCJabberBot(JabberBot):

    ''' Add features in JabberBot to allow it to handle specific
    caractheristics of multiple users chatroom (MUC). '''

    def __init__(self, *args, **kwargs):
        ''' Initialize variables. '''

        # answer only direct messages or not?
        self.only_direct = kwargs.get('only_direct', False)
        try:
           del kwargs['only_direct']
        except KeyError:
           pass

        # initialize jabberbot
        super(MUCJabberBot, self).__init__(*args, **kwargs)

        # create a regex to check if a message is a direct message
        user, domain = str(self.jid).split('@')
        self.direct_message_re = re.compile('^%s(@%s)?[^\w]? ' \
                % (user, domain))

    def callback_message(self, conn, mess):
        ''' Changes the behaviour of the JabberBot in order to allow
        it to answer direct messages. This is used often when it is
        connected in MUCs (multiple users chatroom). '''

        message = mess.getBody()
        if not message:
            return

        if self.direct_message_re.match(message):
            mess.setBody(' '.join(message.split(' ', 1)[1:]))
            return super(MUCJabberBot, self).callback_message(conn, mess)
        elif not self.only_direct:
            return super(MUCJabberBot, self).callback_message(conn, mess)
	
    def xmpp_disconnect(self):
        time.sleep(5)
        while not self.jabber.reconnectAndReauth():
            time.sleep(5)
      #  socketlist[connection._sock]=3D'xmpp'

class Bot(MUCJabberBot):

    @botcmd
    def evetime(self, mess, args):
        """Displays current time in EVE Online"""
	reply = 'It is currently '+datetime.utcnow().strftime('%H:%M')+' EVE Time'
        self.send_simple_reply(mess, reply)

    @botcmd
    def test(self, mess, args):
        """DO NOT PUSH THE RED BUTTON"""
        #mess.getFrom().getResource()
	#self.send( 'xsrender@pfralliance.com', 'hai')
        #return self.get_sender_username(mess)
	data = "you do not follow directions well "+mess.getFrom().getResource()
	return data

    @botcmd
    def parrot(self, mess, args):
	return args

    @botcmd
    def update(self, mess, args):
	"""Command to update your chatroom privlidges call it as !update"""
        url = 'http://pfralliance.com/updateMUCUser.php?user='+mess.getFrom().getResource()
        u = urllib.urlopen(url)
        # u is  file-like object
        data = u.read()
	return data

    @botcmd
    def updateall(self, mess, args):
        """Runs the update function on all users.  For dev purposes, will be removed"""
	url = 'http://pfralliance.com/mucPermissions.php'
        u = urllib.urlopen(url)
        # u is  file-like object
        data = u.read()
        return data

    @botcmd
    def groups(self, mess, args):
 	"""Lists all usergroups that you can ping"""
        url = 'http://pfralliance.com/listUsergroup.php'
        u = urllib.urlopen(url)
        # u is  file-like object
        data = u.read()
        return data

    @botcmd
    def ping(self, mess, args):
	"""This lets you send a ping.  Syntax is !ping usergroup message.  Do not abuse this."""
	who=args.split(' ',1)
	if len(who) > 1:
		pingTarget=who[0]+"@ping.pfralliance.com"
		sender=mess.getFrom().getResource()
                time=datetime.utcnow().strftime('%H:%M:%S')
		content=who[1]+"\n\n Broadcast sent at "+time+" to "+who[0]+" by "+sender
		self.send( pingTarget, content)
		response="Ping sent to "+who[0]
		return response
	else:
		return "You did it wrong! Try !ping usergroup message.  Check !groups for a list of groups you can ping."

if __name__ == '__main__':
--
    nickname = 'Nickname'
    username = 'login_username'
    password = 'userpass'
    chatroom1 = 'recon@conference.pfralliance.com'
    chatroom2 = 'command@conference.pfralliance.com'
    chatroom3 = 'FC@conference.pfralliance.com'
    chatroom4 = 'capitals@conference.pfralliance.com'
    chatroom4 = 'general@conference.pfralliance.com'
    chatroom5 = 'beta@conference.pfralliance.com'
    
    mucbot = Bot(username, password,only_direct=False, command_prefix='!')
    mucbot.join_room(chatroom1, nickname)
    mucbot.join_room(chatroom2, nickname)
    mucbot.join_room(chatroom3, nickname)
    mucbot.join_room(chatroom4, nickname)
    mucbot.join_room(chatroom5, nickname)

   # mucbot.serve_forever()

    try:
        mucbot.serve_forever()
    except IOError:
        mucbot = Bot(username, password,only_direct=False, command_prefix='!')

