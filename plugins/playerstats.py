import logging
main_log = logging.getLogger("main_log")

player_stats = {}

class PlayerStats:
	names = []
	ip = "unknown"
	kills = 0
	deaths = 0
	steamid = 0
	lastconnect = 0
	suicides = 0

	weapons = {} 

	def checkName(self,newname):
		found = 0
		for cur in self.names:
			if newname.lower() == cur.lower():
				found = 1
		if not found:
			self.names.append(newname)
class WeaponStats:
	kills = 0
	headshots = 0
	damage = 0
	tks = 0

def player_killed(event,ip,port,timestamp):
	global player_stats
	if not player_stats.has_key(event.attacker_steamid):
		player_stats[event.attacker_steamid] = PlayerStats()
	if not player_stats.has_key(event.victim_steamid):
		player_stats[event.victim_steamid] = PlayerStats()

	player_stats[event.attacker_steamid].checkName(event.attacker_name)
	player_stats[event.victim_steamid].checkName(event.victim_name)

	player_stats[event.attacker_steamid].kills += 1
	player_stats[event.victim_steamid].deaths += 1

	if not player_stats[event.attacker_steamid].weapons.has_key(event.weapon):
                player_stats[event.attacker_steamid].weapons[event.weapon] = WeaponStats()

        player_stats[event.attacker_steamid].weapons[event.weapon].kills += 1

	if event.headshot == 1:
		player_stats[event.attacker_steamid].weapons[event.weapon].headshots += 1


	dump_stats()

def player_suicide(event,ip,port,timestamp):
	global player_stats
	if not player_stats.has_key(event.steamid):
		player_stats[event.steamid] = PlayerStats()

	player_stats[event.steamid].checkName(event.name)
	player_stats[event.steamid].suicides += 1

def player_connect(event,ip,port,timestamp):
	global player_stats
	if not player_stats.has_key(event.steamid):
		player_stats[event.steamid] = PlayerStats()

	player_stats[event.steamid].checkName(event.name)
	player_stats[event.steamid].ip = event.ip
	player_stats[event.steamid].lastconnect = timestamp

def player_weaponstats(event,ip,port,timestamp):
	global player_stats
	if not player_stats.has_key(event.steamid):
		player_stats[event.steamid] = PlayerStats()

	player_stats[event.steamid].checkName(event.name)

	if not player_stats[event.steamid].weapons.has_key(event.weapon):
		player_stats[event.steamid].weapons[event.weapon] = WeaponStats()

	player_stats[event.steamid].weapons[event.weapon].kills += event.kills
	player_stats[event.steamid].weapons[event.weapon].headshots += event.headshots
	player_stats[event.steamid].weapons[event.weapon].damage += event.damage
	player_stats[event.steamid].weapons[event.weapon].tks += event.tks

def player_attacked(event,ip,port,timestamp):
        global player_stats
        if not player_stats.has_key(event.attacker_steamid):
                player_stats[event.attacker_steamid] = PlayerStats()

	player_stats[event.attacker_steamid].checkName(event.attacker_name)

        if not player_stats[event.attacker_steamid].weapons.has_key(event.weapon):
                player_stats[event.attacker_steamid].weapons[event.weapon] = WeaponStats()

        player_stats[event.attacker_steamid].weapons[event.weapon].damage += event.damage


def dump_stats():
	global player_stats
	of = open("stats.txt","w")
	for cur in player_stats.keys():
		of.write("%s:\n" % cur)
		of.write("\tAliases: %s\n" % (",".join(player_stats[cur].names)))
		of.write("\tKills: %i Deaths: %i Suicides: %i\n" % (player_stats[cur].kills,player_stats[cur].deaths,player_stats[cur].suicides))
		for cur_wep in player_stats[cur].weapons.keys():
			of.write("\t%s\n" % cur_wep)
			of.write("\t\tKills: %i Headshots: %i Damage: %i TK's: %i\n" % (player_stats[cur].weapons[cur_wep].kills,player_stats[cur].weapons[cur_wep].headshots,player_stats[cur].weapons[cur_wep].damage,player_stats[cur].weapons[cur_wep].tks))

	of.close()

from eventhandler import eventhandler
eventhandler.registerCallback(player_killed,['player_killed'])
eventhandler.registerCallback(player_suicide,['player_suicide'])
eventhandler.registerCallback(player_connect,['player_connect'])
eventhandler.registerCallback(player_weaponstats,['player_weaponstats'])
eventhandler.registerCallback(player_attacked,['player_attacked'])
