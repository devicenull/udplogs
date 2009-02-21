import re

from standard_pattern import player

class player_joinedteam:
	# "[SC-UBW] Don<2273><BOT><Unassigned>" joined team "TERRORIST"
	pattern = re.compile(player()+" joined team \"(?P<new_team>.*)\"")

	@staticmethod
	def isMatch(instr):
		return (player_joinedteam.pattern.match(instr) != None)

	def __init__(self,instr):
		obj = player_joinedteam.pattern.match(instr)
                self.name = obj.group("name")
                self.uniqueid = obj.group("uniqueid")
                self.steamid = obj.group("steamid")
		self.oldteam = obj.group("team")
		self.newteam = obj.group("new_team")
	
	def __str__(self):
		return "player %s (%s) joined team %s" % (self.name,self.steamid,self.newteam)

from eventhandler import eventhandler
eventhandler.register(player_joinedteam)
