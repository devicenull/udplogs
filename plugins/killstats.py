import logging,time

main_log = logging.getLogger("main_log")

from basestats import Stats

def player_killed(event,ip,port,timestamp):
	attacker = Stats.getPlayer(event.attacker_steamid,ip,port)
	victim = Stats.getPlayer(event.victim_steamid,ip,port)

	attacker.checkName(event.attacker_name)
	victim.checkName(event.victim_name)

	attacker.kills += 1
	victim.deaths += 1

        curWeapon = attacker.getWeapon(event.weapon)
	curWeapon.kills += 1

	if event.headshot == 1:
		curWeapon.headshots += 1

def player_suicide(event,ip,port,timestamp):
	player = Stats.getPlayer(event.steamid,ip,port)

	player.checkName(event.name)
	player.suicides += 1

def player_connect(event,ip,port,timestamp):
	player = Stats.getPlayer(event.steamid,ip,port)

	player.checkName(event.name)
	player.ip = event.ip
	player.lastconnect = time.time()

def player_weaponstats(event,ip,port,timestamp):
	player = Stats.getPlayer(event.steamid,ip,port)

	player.checkName(event.name)

	curWeapon = player.getWeapon(event.weapon)
	
	curWeapon.kills += event.kills
	curWeapon.headshots += event.headshots
	curWeapon.weapons[event.weapon].damage += event.damage
	curWeapon.weapons[event.weapon].tks += event.tks

def player_attacked(event,ip,port,timestamp):
	attacker = Stats.getPlayer(event.attacker_steamid,ip,port)

	attacker.checkName(event.attacker_name)

	curWeapon = attacker.getWeapon(event.weapon)
        curWeapon.damage += event.damage


from eventhandler import eventhandler
eventhandler.registerCallback(player_killed,['player_killed'])
eventhandler.registerCallback(player_suicide,['player_suicide'])
eventhandler.registerCallback(player_connect,['player_connect'])
eventhandler.registerCallback(player_weaponstats,['player_weaponstats'])
eventhandler.registerCallback(player_attacked,['player_attacked'])
