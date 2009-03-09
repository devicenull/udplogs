import logging, threading

main_log = logging.getLogger("main_log")

from twisted.enterprise import adbapi
from twisted.internet import reactor

read_pool = adbapi.ConnectionPool("MySQLdb",db="playerstats",user="playerstats",use_unicode=True,charset="utf8")
write_pool = read_pool

def _DBError(err):
	main_log.error(err)
	reactor.crash()

class Stats:
	servers = {}
	
	@staticmethod
	def getPlayer(steamid, server_ip, server_port):
		srvkey = "%s:%i" % (server_ip, server_port)
		if not Stats.servers.has_key(srvkey):
			Stats.servers[srvkey] = {'map':'unknown', 'players':{}}

		if not Stats.servers[srvkey]['players'].has_key(steamid):
			Stats.servers[srvkey]['players'][steamid] = PlayerStats(steamid)

		return Stats.servers[srvkey]['players'][steamid]

	@staticmethod
	def getServerMap(server_ip, server_port):
		srvkey = "%s:%i" % (server_ip, server_port)
		if not Stats.servers.has_key(srvkey):
                        Stats.servers[srvkey] = {'map':'unknown', 'players':{}}

		return Stats.servers[srvkey]['map']

	@staticmethod
	def setServerMap(server_ip, server_port, map):
		srvkey = "%s:%i" % (server_ip, server_port)		
		Stats.servers[srvkey]['map'] = map

	@staticmethod
	def getPlayers(server_ip, server_port):
		srvkey = "%s:%i" % (server_ip, server_port)
		return Stats.servers[srvkey]['players']


class PlayerStats:
        steamid = ""
        names = []
        ip = "unknown"
        kills = 0
        deaths = 0
        steamid = 0
        lastconnect = 0
        suicides = 0
	headshots = 0

	victims = {}
        weapons = {}
	events = {}
	teams = {}

	_lock = None

        def __init__(self,steamid):
                self.steamid = steamid
                if self.steamid == "BOT":
                        self.steamid="STEAM_0:1:1199"
		self._lock = threading.Lock()

        def checkName(self,newname):
                found = 0
                for cur in self.names:
                        if newname.lower() == cur.lower():
                                found = 1
                if not found:
                        self.names.append(newname)


	def getWeapon(self,wpnname):
		if not self.weapons.has_key(wpnname):
			self.weapons[wpnname] = WeaponStats(wpnname)

		return self.weapons[wpnname]

	def getEvent(self,eventname):
		if not self.events.has_key(eventname):
			self.events[eventname] = EventStats(eventname)

		return self.events[eventname]

	def getTeam(self,teamname):
		if not self.teams.has_key(teamname):
			self.teams[teamname] = TeamStats(teamname)

		return self.teams[teamname]

	def getVictim(self,vicid):
		if not self.victims.has_key(vicid):
			self.victims[vicid] = VictimStats(self, vicid)

		return self.victims[vicid]

        def savePlayer(self, server_ip, server_port, map):
                later = write_pool.runInteraction(self._writePlayerToDB, (server_ip, server_port), map)
                later.addErrback(_DBError)

        def _writePlayerToDB(self,txn,(server_ip,server_port),map):
		txn.execute("START TRANSACTION")
                txn.execute("""SELECT server_id FROM servers WHERE server_ip=%s AND server_port=%s""",(server_ip, server_port))
		if txn.rowcount == 0:
			txn.execute("""INSERT INTO servers(server_ip,server_port) VALUES(%s,%s)""",(server_ip, server_port))
			server_id = txn.lastrowid
		else:	
			server_id = txn.fetchone()[0]

		txn.execute("""INSERT INTO players(server_id,player_id,lastconnect) VALUES(%s,SteamToInt(%s),floor(%s))
				ON DUPLICATE KEY UPDATE lastconnect=floor(%s)""",(server_id, self.steamid, self.lastconnect, self.lastconnect))

		txn.execute("""INSERT INTO player_maps(server_id,player_id,map_name,kills,deaths,headshots,suicides) VALUES(%s,SteamToInt(%s),%s,%s,%s,%s,%s)
                                ON DUPLICATE KEY UPDATE kills=kills+%s, deaths=deaths+%s, suicides=suicides+%s, headshots=headshots+%s""",
                                (server_id, self.steamid, map, self.kills, self.deaths, self.headshots, self.suicides, self.kills, self.deaths, self.suicides, self.headshots))
                self.kills=0
                self.deaths=0
                self.suicides=0
		self.headshots=0
	
		nmlist = []	
		query = """INSERT INTO player_names(server_id,player_id,player_name,lastuse) VALUES (%s,SteamToInt(%s),%s,NOW())"""
		for cur_name in self.names:
			nmlist.append((server_id, self.steamid,cur_name))
		
		txn.executemany(query,nmlist)

		# Save any team info we have
		#for cur_team in self.teams.keys():
		#	self.teams[cur_team]._writeTeamToDB(txn, self, server_id)
		#self.teams = {}

		# Save any event info we have
		#for cur in self.events.keys():
		#	self.events[cur]._writeEventToDB(txn, self, server_id)
		#self.events = {}

                # Now save any weapons we have
                #for cur in self.weapons.keys():
                #        self.weapons[cur]._writeWeaponToDB(txn, self, server_id)
		#self.weapons = {}

		# Aaand victims
		#for cur in self.victims.keys():
		#	self.victims[cur]._writeVictimToDB(txn, server_id)
		#self.victims = {}
		
		txn.execute("COMMIT")

class WeaponStats:
        name = "unknown"
        kills = 0
        headshots = 0
        damage = 0
        tks = 0

        def __init__(self,weapon):
                self.name = weapon

        def saveWeapon(self,player,server_id):
                later = write_pool.runInteraction(self._writeWeaponToDB, player, server_id)
                later.addErrback(_DBError)

        def _writeWeaponToDB(self,txn,player,server_id):
                txn.execute("""INSERT INTO player_weapons(server_id,player_id,weapon_name,kills,headshots,damage,tks) VALUES(%s,SteamToInt(%s),%s,%s,%s,%s,%s)
                                ON DUPLICATE KEY UPDATE kills=kills+%s, headshots=headshots+%s, damage=damage+%s, tks=tks+%s""",
                                (server_id, player.steamid, self.name, self.kills, self.headshots, self.damage, self.tks, self.kills, self.headshots, self.damage, self.tks))
                self.kills=0
                self.damage=0
                self.tks=0
                self.headshots=0


class EventStats:
	name = "unknown"
	trigger_count = 0
	last_trigger = 0

	def __init__(self,event):
		self.name = event

	def trigger(self):
		self.trigger_count += 1
		self.last_trigger = time.time()

	def saveEvent(self,player,server_id):
		later = write_pool.runInteraction(self._writeEventToDB, player, server_id)
		later.addErrback(_DBError)

	def _writeEventToDB(self,txn,player,server_id):
		txn.execute("""INSERT INTO player_events(server_id,player_id,event_name,triggercount) VALUES(%s,SteamToInt(%s),%s,%s)
				ON DUPLICATE KEY UPDATE triggercount=triggercount+%s"""
				,(server_id, player.steamid, self.name, self.trigger_count, self.trigger_count))
		self.trigger_count = 0

class TeamStats:
	name = "unknown"
	join_count = 0

	def __init__(self,team):
		self.name = team

	def saveEvent(self,player,server_id):
		later = write_pool.runInteraction(self._writeTeamToDB, player, server_id)
		later.addErrback(_DBError)

	def _writeTeamToDB(self,txn,player,server_id):
		txn.execute("""INSERT INTO player_team(server_id,player_id,team_name,join_count) VALUES(%s,SteamToInt(%s),%s,%s)
			ON DUPLICATE KEY UPDATE join_count=join_count+%s"""
			,(server_id, player.steamid, self.name, self.join_count, self.join_count))
		self.join_count = 0

class VictimStats:
	steamid = "unknown"
	kills = 0
	damage = 0
	headshots = 0
	attacker = 0

	def __init__(self,attacker,victim):
		self.attacker = attacker
		self.steamid = id

	def saveVictim(self,server_id):
		later = write_pool.runInteraction(self._writeVictimToDB,server_id)
		later.addErrback(_DBError)

	def _writeVictimToDB(self,txn,server_id):
		txn.execute("""INSERT INTO player_targets(server_id,player_id,target_id,kills,headshots,damage) VALUES(%s,SteamToInt(%s),SteamToInt(%s),%s,%s,%s)
			ON DUPLICATE KEY UPDATE kills=kills+%s, headshots=headshots+%s, damage=damage+%s"""
			,(server_id, self.attacker.steamid, self.steamid, self.kills, self.headshots, self.damage, self.kills, self.headshots, self.damage))

		self.kills = 0
		self.damage = 0
		self.headshots = 0
