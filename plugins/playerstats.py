import logging, time
main_log = logging.getLogger("main_log")

player_stats = {}
lastdump = time.time()

class PlayerStats:
	name = "unknown"
	ip = "unknown"
	kills = 0
	deaths = 0
	steamid = 0
	lastconnect = 0
	suicides = 0

	weapons = []

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

	player_stats[event.attacker_steamid].kills += 1
	player_stats[event.victim_steamid].deaths += 1

	if time.time()-lastdump > 30:
		dump_stats()

def player_suicide(event,ip,port,timestamp):
	global player_stats
	if not player_stats.has_key(event.steamid):
		player_stats[event.steamid] = PlayerStats()

	player_stats[event.steamid].suicides += 1

def player_connect(event,ip,port,timestamp):
	global player_stats
	if not player_stats.has_key(event.steamid):
		player_stats[event.steamid] = PlayerStats()

	player_stats[event.steamid].name = event.name
	player_stats[event.steamid].ip = event.ip
	player_stats[event.steamid].lastconnect = timestamp

def player_weaponstats(event,ip,port,timestamp):
	global player_stats
	if not player_stats.has_key(event.steamid):
		player_stats[event.steamid] = PlayerStats()

	if not player_stats[event.steamid].weapons.has_key(event.weapon):
		player_stats[event.steamid].weapons[event.weapon] = WeaponStats()

	player_stats[event.steamid].weapons[event.weapon].kills += event.kills
	player_stats[event.steamid].weapons[event.weapon].headshots += event.headshots
	player_stats[event.steamid].weapons[event.weapon].damage += event.damage
	player_stats[event.steamid].weapons[event.weapon].tks += event.tks

def dump_stats():
	global player_stats
	of = open("stats.txt","w")
	for cur in player_stats.keys():
		of.write("%s:\n" % cur)
		of.write("\tKills: %i Deaths: %i Suicides: %i\n" % (player_stats[cur].kills,player_stats[cur].deaths,player_stats[cur].suicides))
	of.close()

from eventhandler import eventhandler
eventhandler.registerCallback(player_killed,['player_killed'])
eventhandler.registerCallback(player_suicide,['player_suicide'])
eventhandler.registerCallback(player_connect,['player_connect'])
eventhandler.registerCallback(player_weaponstats,['player_weaponstats'])
