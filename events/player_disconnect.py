import re

from standard_pattern import player

class player_disconnect:
	# "[SC-UBW] Don<2273><BOT><TERRORIST>" disconnected (reason "Kicked by Console")
	pattern = re.compile(player()+" disconnected \(reason \"(?P<reason>.*)\"")

	@staticmethod
	def isMatch(instr):
		return (player_disconnect.pattern.match(instr) != None)

	def __init__(self,instr):
		obj = player_disconnect.pattern.match(instr)
		self.name = obj.group("name")
		self.uniqueid = obj.group("uniqueid")
		self.steamid = obj.group("steamid")
		self.reason = obj.group("reason")
	
	def __str__(self):
		return "player disconnected %s (%s) reason: %s" % (self.name,self.steamid,self.reason)

from eventhandler import eventhandler
eventhandler.registerEvent(player_disconnect)
