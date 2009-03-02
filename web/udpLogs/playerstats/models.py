# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

from django.db import models

class Servers(models.Model):
    server_id = models.IntegerField(primary_key=True)
    server_ip = models.CharField(unique=True, max_length=48, blank=True)
    server_port = models.IntegerField(unique=True, null=True, blank=True)
    class Meta:
        db_table = u'servers'

class Players(models.Model):
    server = models.ForeignKey(Servers)
    player_id = models.IntegerField(primary_key=True)
    lastconnect = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'players'

class PlayerEvents(models.Model):
    server = models.ForeignKey(Players,related_name='fk_pe_sid')
    player = models.ForeignKey(Players,related_name='fk_pe_pid')
    event_name = models.CharField(max_length=192, primary_key=True)
    triggercount = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'player_events'

class PlayerMaps(models.Model):
    server = models.ForeignKey(Players,related_name='fk_pm_sid')
    player = models.ForeignKey(Players,related_name='fk_pm_pid')
    map_name = models.CharField(max_length=192, primary_key=True)
    kills = models.IntegerField(null=True, blank=True)
    deaths = models.IntegerField(null=True, blank=True)
    headshots = models.IntegerField(null=True, blank=True)
    suicides = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'player_maps'

class PlayerNames(models.Model):
    server = models.ForeignKey(Players,related_name='fk_pn_sid')
    player = models.ForeignKey(Players,related_name='fk_pn_pid')
    player_name = models.CharField(max_length=384, primary_key=True)
    lastuse = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'player_names'

class PlayerTargets(models.Model):
    server = models.ForeignKey(Players,related_name='fk_pt_sid')
    player = models.ForeignKey(Players,related_name='fk_pt_pid')
    target_id = models.ForeignKey(Players,related_name='fk_pt_tid')
    kills = models.IntegerField(null=True, blank=True)
    headshots = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'player_targets'

class PlayerTeam(models.Model):
    server = models.ForeignKey(Players,related_name='fk_ptm_sid')
    player = models.ForeignKey(Players,related_name='fk_ptm_pid')
    team_name = models.CharField(max_length=96, primary_key=True)
    join_count = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'player_team'

class PlayerWeapons(models.Model):
    server = models.ForeignKey(Players,related_name='fk_pw_sid')
    player = models.ForeignKey(Players,related_name='fk_pw_pid')
    weapon_name = models.CharField(max_length=192, primary_key=True)
    kills = models.IntegerField(null=True, blank=True)
    headshots = models.IntegerField(null=True, blank=True)
    damage = models.IntegerField(null=True, blank=True)
    tks = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'player_weapons'

