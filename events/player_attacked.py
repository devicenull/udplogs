import re

from standard_pattern import player,player2

class player_attacked:
	# "Erik<8><BOT><CT>" attacked "Pat<4><BOT><TERRORIST>" with "m4a1" (damage "20") (damage_armor "4") (health "80") (armor "95") (hitgroup "left arm")
	pattern = re.compile(player()+" attacked "+player2()+" with \"(?P<weapon>.*)\" \(damage \"(?P<damage>[0-9]+)\"\) \(damage_armor \"(?P<damage_armor>[0-9]+)\"\) \(health \"(?P<health>[0-9]+)\"\) \(armor \"(?P<armor>[0-9]+)\"\) \(hitgroup \"(?P<hitgroup>[a-zA-Z_\s]+)\"\)")

	@staticmethod
	def isMatch(instr):
		return (player_attacked.pattern.match(instr) != None)

	def __init__(self,instr):
		obj = player_attacked.pattern.match(instr)
		self.attacker_name = obj.group("name")
		self.attacker_uniqueid = obj.group("uniqueid")
		self.attacker_steamid = obj.group("steamid")
		self.attacker_team = obj.group("team")

                self.victim_name = obj.group("name2")
                self.victim_uniqueid = obj.group("uniqueid2")
                self.victim_steamid = obj.group("steamid2")
                self.victim_team = obj.group("team2")

		self.weapon = obj.group("weapon")
		self.damage = obj.group("damage")
		self.damage_armor = obj.group("damage_armor")
		self.health = obj.group("health")
		self.armor = obj.group("armor")
		self.hitgroup = obj.group("hitgroup")
	
	def __str__(self):
		return "player %s did %s damage to %s" % (self.attacker_name,self.damage,self.victim_name) 

from eventhandler import eventhandler
eventhandler.registerEvent(player_attacked)
