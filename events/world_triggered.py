import re

class world_triggered:
	# World triggered "Round_End"
	pattern = re.compile("World triggered \"(?P<event>.*)\"")

	@staticmethod
	def isMatch(instr):
		return (world_triggered.pattern.match(instr) != None)

	def __init__(self,instr):
		obj = world_triggered.pattern.match(instr)
		self.event = obj.group("event")
	
	def __str__(self):
		return "World triggered %s" % (self.event)

from eventhandler import eventhandler
eventhandler.registerEvent(world_triggered)
