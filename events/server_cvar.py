import re

class server_cvar:
	# server_cvar: "mp_friendlyfire" "1"
	pattern = re.compile("server_cvar: \"(?P<cvar>.*)\" \"(?P<value>.*)\"")

	@staticmethod
	def isMatch(instr):
		return (server_cvar.pattern.match(instr) != None)

	def __init__(self,instr):
		obj = server_cvar.pattern.match(instr)
		self.cvar = obj.group("cvar")
		self.value = obj.group("value")
	
	def __str__(self):
		return "server_cvar: %s changed to \"%s\"" % (self.cvar,self.value)

from eventhandler import eventhandler
eventhandler.registerEvent(server_cvar)
