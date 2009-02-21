import re

from standard_pattern import player

class player_connect:
	# "[SC-UBW] Don<2273><BOT><Team>" connected, address "none"
	pattern = re.compile(player()+" connected, address \"(?P<ip>.*)\"")

	@staticmethod
	def isMatch(instr):
		return (player_connect.pattern.match(instr) != None)

	def __init__(self,instr):
		obj = player_connect.pattern.match(instr)
		self.name = obj.group("name")
		self.uniqueid = obj.group("uniqueid")
		self.steamid = obj.group("steamid")
		self.ip = obj.group("ip")
		self.team = obj.group("team")
	
	def __str__(self):
		return "player connected %s (%s) (%s)" % (self.name,self.steamid,self.ip)

from eventhandler import eventhandler
eventhandler.registerEvent(player_connect)
