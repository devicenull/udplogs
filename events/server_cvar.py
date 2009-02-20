import re

class server_cvar:
	# server_cvar: "mp_friendlyfire" "1"
	pattern = re.compile("server_cvar: \"(?P<cvar>.*)\" \"(?P<value>.*)\"")

	@staticmethod
	def isMatch(instr):
		return (server_cvar.pattern.match(instr) != None)

	def __init__(self,instr):
		pass

from eventhandler import eventhandler
eventhandler.register(server_cvar)
