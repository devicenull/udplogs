import re

class server_map:
	# Started map "de_dust2" (CRC "1413637712")
	pattern = re.compile("Started map \"(?P<mapname>.*)\" \(CRC \"(?P<crc>[0-9]*)\"\)")

	@staticmethod
	def isMatch(instr):
		return (server_map.pattern.match(instr) != None)

	def __init__(self,instr):
		obj = server_map.pattern.match(instr)
		self.map = obj.group("map")
		self.crc = obj.group("crc")
	
	def __str__(self):
		return "server changed map to %s" % (self.map)

from eventhandler import eventhandler
eventhandler.registerEvent(server_map)
