import re

from standard_pattern import player

class player_weaponstats:
	# "froggy420<2687><STEAM_0:1:9830121><CT>" triggered "weaponstats" (weapon "m4a1") (shots "27") (hits "3") (kills "0") (headshots "0") (tks "0") (damage "60") (deaths "0")
	pattern = re.compile(player()+" triggered \"weaponstats\" \(weapon \"(?P<weapon>.*)\"\) \(shots \"(?P<shots>[0-9]+)\"\) \(hits \"(?P<hits>[0-9]+)\"\) \(kills \"(?P<kills>[0-9]+)\"\) \(headshots \"(?P<headshots>[0-9]+)\"\) \(tks \"(?P<tk>[0-9]+)\"\) \(damage \"(?P<damage>[0-9]+)\"\) \(deaths \"(?P<deaths>[0-9]+)\"\)")

	@staticmethod
	def isMatch(instr):
		return (player_weaponstats.pattern.match(instr) != None)

	def __init__(self,instr):
		obj = player_weaponstats.pattern.match(instr)
		self.name = obj.group("name")
		self.uniqueid = obj.group("uniqueid")
		self.steamid = obj.group("steamid")
		self.team = obj.group("team")

		self.weapon = obj.group("weapon")
		self.shots = int(obj.group("shots"))
		self.hits = int(obj.group("hits"))
		self.kills = int(obj.group("kills"))
		self.headshots = int(obj.group("headshots"))
		self.tks = int(obj.group("tk"))
		self.damage = int(obj.group("damage"))
		self.deaths = int(obj.group("deaths"))
	
	def __str__(self):
		return "player %s weaponstats for %s" % (self.name,self.weapon) 

from eventhandler import eventhandler
eventhandler.registerEvent(player_weaponstats)
