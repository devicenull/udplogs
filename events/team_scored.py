import re

class team_scored:
	# Team "CT" scored "1" with "4" players
	pattern = re.compile("Team \"(?P<team>.*)\" scored \"(?P<score>[0-9]+)\" with \"(?P<players>[0-9]+)\" players")

	@staticmethod
	def isMatch(instr):
		return (team_scored.pattern.match(instr) != None)

	def __init__(self,instr):
		obj = team_scored.pattern.match(instr)
		self.team = obj.group("team")
		self.score = obj.group("score")
		self.playercount = obj.group("players")
	
	def __str__(self):
		return "%s scored %s with %s players" % (self.team,self.score,self.playercount)

from eventhandler import eventhandler
eventhandler.registerEvent(team_scored)
