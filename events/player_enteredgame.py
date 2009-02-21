import re

from standard_pattern import player

class player_enteredgame:
	# "[SC-UBW] Don<2273><BOT><>" entered the game 
	pattern = re.compile(player()+" entered the game")

	@staticmethod
	def isMatch(instr):
		return (player_enteredgame.pattern.match(instr) != None)

	def __init__(self,instr):
		obj = player_enteredgame.pattern.match(instr)
                self.name = obj.group("name")
                self.uniqueid = obj.group("uniqueid")
                self.steamid = obj.group("steamid")
		self.oldteam = obj.group("team")
	
	def __str__(self):
		return "player %s (%s) entered the game" % (self.name,self.steamid)

from eventhandler import eventhandler
eventhandler.register(player_enteredgame)
