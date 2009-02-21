import re

from standard_pattern import player

class player_weaponstats2:
	# "froggy420<2687><STEAM_0:1:9830121><CT>" triggered "weaponstats" (weapon "m4a1") (shots "27") (hits "3") (kills "0") (headshots "0") (tks "0") (damage "60") (deaths "0")
	pattern = re.compile(player()+" triggered \"weaponstats2\" \(weapon \"(?P<weapon>.*)\"\) \(head \"(?P<head>[0-9]+)\"\) \(chest \"(?P<chest>[0-9]+)\"\) \(stomach \"(?P<stomach>[0-9]+)\"\) \(leftarm \"(?P<leftarm>[0-9]+)\"\) \(rightarm \"(?P<rightarm>[0-9]+)\"\) \(leftleg \"(?P<leftleg>[0-9]+)\"\) \(rightleg \"(?P<rightleg>[0-9]+)\"\)")

	@staticmethod
	def isMatch(instr):
		return (player_weaponstats2.pattern.match(instr) != None)

	def __init__(self,instr):
		obj = player_weaponstats2.pattern.match(instr)
		self.name = obj.group("name")
		self.uniqueid = obj.group("uniqueid")
		self.steamid = obj.group("steamid")
		self.team = obj.group("team")

		self.weapon = obj.group("weapon")
		self.head = obj.group("head")
		self.chest = obj.group("chest")
		self.leftarm = obj.group("leftarm")
		self.rightarm = obj.group("rightarm")
		self.leftleg = obj.group("leftleg")
		self.rightleg = obj.group("rightleg")
	
	def __str__(self):
		return "player %s weaponstats2 for %s" % (self.name,self.weapon) 

from eventhandler import eventhandler
eventhandler.registerEvent(player_weaponstats2)
