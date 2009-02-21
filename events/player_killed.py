import re

from standard_pattern import player, player2

class player_killed:
	# "[SC-UBW] Irving<41><BOT><TERRORIST>" killed "[SC-UBW] Wyatt<38><BOT><CT>" with "mac10" (headshot)
	# "[SC-UBW] Derek<34><BOT><CT>" killed "[SC-UBW] Irving<41><BOT><TERRORIST>" with "usp"
	pattern = re.compile(player()+" killed "+player2()+" with \"(?P<weapon>.*)\"(?P<headshot>.*)")

	@staticmethod
	def isMatch(instr):
		return (player_killed.pattern.match(instr) != None)

	def __init__(self,instr):
		obj = player_killed.pattern.match(instr)
		self.attacker_name = obj.group("name")
		self.attacker_uniqueid = obj.group("uniqueid")
		self.attacker_steamid = obj.group("steamid")
		self.attacker_team = obj.group("team")

		self.victim_name = obj.group("name2")
		self.victim_uniqueid = obj.group("uniqueid2")
		self.victim_steamid = obj.group("steamid2")
		self.victim_team = obj.group("team2")

		self.weapon = obj.group("weapon")
		self.headshot = (obj.group("headshot") == " (headshot)")
	
	def __str__(self):
		return "player %s killed %s with %s headshot: %i" % (self.attacker_name,self.victim_name,self.weapon,self.headshot) 

from eventhandler import eventhandler
eventhandler.registerEvent(player_killed)
