import re

from standard_pattern import player

class player_suicide:
	# "[SC-UBW] Yahn<2292><BOT><TERRORIST>" committed suicide with "world"
	pattern = re.compile(player()+" committed suicide with \"(?P<weapon>.*)\"")

	@staticmethod
	def isMatch(instr):
		return (player_suicide.pattern.match(instr) != None)

	def __init__(self,instr):
		obj = player_suicide.pattern.match(instr)
		self.name = obj.group("name")
		self.uniqueid = obj.group("uniqueid")
		self.steamid = obj.group("steamid")
		self.team = obj.group("team")

		self.weapon = obj.group("weapon")
	
	def __str__(self):
		return "player %s committed suicide with %s" % (self.name,self.weapon) 

from eventhandler import eventhandler
eventhandler.registerEvent(player_suicide)
