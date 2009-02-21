import re

from standard_pattern import player

class player_validated:
	# "[SC-UBW] Don<2273><BOT><Team>" STEAM USERID validated
	pattern = re.compile(player()+" STEAM USERID validated")

	@staticmethod
	def isMatch(instr):
		return (player_validated.pattern.match(instr) != None)

	def __init__(self,instr):
		obj = player_validated.pattern.match(instr)
		self.name = obj.group("name")
		self.uniqueid = obj.group("uniqueid")
		self.steamid = obj.group("steamid")
		self.team = obj.group("team")
	
	def __str__(self):
		return "player steamid validated %s (%s)" % (self.name,self.steamid)

from eventhandler import eventhandler
eventhandler.registerEvent(player_validated)
