from django.db import models

# Create your models here.
class Match(models.Model):
    MATCH_STATUS = [
        ('draft_to_start', 'Draft to start'),
        ('draft_in_progress', 'Draft in progress'),
        ('draft_finished', 'Draft finished'),
        ('match_ended', 'Match ended'),
    ]

    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    match_id = models.BigIntegerField(unique=True)
    radiant_team = models.CharField(max_length=50)
    dire_team = models.CharField(max_length=50)
    draft_in_progress = models.BooleanField(default=False)
    match_status = models.CharField(max_length=50, choices=MATCH_STATUS, default='draft_to_start')
    pro_match = models.BooleanField(default=False)
    radiant_win_chance = models.FloatField(default=0.5)
    radiant_win = models.IntegerField(default=-1)
    radiant_pick1 = models.IntegerField()
    radiant_pick2 = models.IntegerField()
    radiant_pick3 = models.IntegerField()
    radiant_pick4 = models.IntegerField()
    radiant_pick5 = models.IntegerField()
    dire_pick1 = models.IntegerField()
    dire_pick2 = models.IntegerField()
    dire_pick3 = models.IntegerField()
    dire_pick4 = models.IntegerField()
    dire_pick5 = models.IntegerField()
    radiant_ban1 = models.IntegerField()
    radiant_ban2 = models.IntegerField()
    radiant_ban3 = models.IntegerField()
    radiant_ban4 = models.IntegerField()
    radiant_ban5 = models.IntegerField()
    radiant_ban6 = models.IntegerField()
    radiant_ban7 = models.IntegerField()
    dire_ban1 = models.IntegerField()
    dire_ban2 = models.IntegerField()
    dire_ban3 = models.IntegerField()
    dire_ban4 = models.IntegerField()
    dire_ban5 = models.IntegerField()
    dire_ban6 = models.IntegerField()
    dire_ban7 = models.IntegerField()