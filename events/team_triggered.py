import re

class team_triggered:
	# Team "TERRORIST" triggered "Terrorists_Win" (CT "1") (T "4")
	pattern = re.compile("Team \"(?P<team>.*)\" triggered \"(?P<event>.*)\"")

	@staticmethod
	def isMatch(instr):
		return (team_triggered.pattern.match(instr) != None)

	def __init__(self,instr):
		obj = team_triggered.pattern.match(instr)
		self.team = obj.group("team")
		self.event = obj.group("event")
	
	def __str__(self):
		return "%s triggered %s" % (self.team,self.event)

from eventhandler import eventhandler
eventhandler.registerEvent(team_triggered)
