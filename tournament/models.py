"""
Copyright 2016, Paul Powell, All rights reserved.
"""
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

## **********************************************
## Static data representing the tournament format
## **********************************************
class Year(models.Model):
    year = models.CharField(max_length=8)

    def __str__(self):
        return "{}".format(self.year)

# A Region (south, east, midwest, or west)
class RegionData(models.Model):
    name = models.CharField(max_length=32)
    ff_match = models.ForeignKey('self', related_name='my_ff_match', null=True)
    exclusive = models.ForeignKey('self', related_name='my_exclusive', null=True)
    year = models.ForeignKey(Year)

    def __unicode__(self):
        return "({}) {}".format(self.year.year, self.name)

# Represent a team in the tournament
class Team(models.Model):
    year = models.ForeignKey(Year)
    region = models.ForeignKey(RegionData)
    name = models.CharField(max_length=128)
    seed = models.IntegerField()
    power = models.IntegerField(default=0)

    def __str__(self):
        return "({}) {}[{}]".format(self.year.year, self.name, self.seed)

class Algorithm(models.Model):
    name = models.CharField(max_length=128)
    
    def __unicode__(self):
        return self.name

## **********************************************
## Dynamic data produced by tournament simulation
## **********************************************
class Options(models.Model):
    madness = models.IntegerField(default=1)
    winner = models.ForeignKey(Team, blank=True, null=True, related_name="winner")
    second = models.ForeignKey(Team, blank=True, null=True, related_name="second")
    algorithm = models.ForeignKey(Algorithm)

class Tournament(models.Model):
    user = models.ForeignKey(
            User,
            on_delete=models.SET_NULL,
            null=True)
    date = models.DateTimeField(auto_now_add=True)
    year = models.ForeignKey(Year)
    winner = models.ForeignKey(Team, related_name="+")
    runnerup = models.ForeignKey(Team, related_name="+")
    upsets = models.IntegerField(default=0)
    options = models.ForeignKey(Options)

    def __unicode__(self):
        return "({}) vs {}".format(self.winner, self.runnerup)

class Region(models.Model):
    name = models.CharField(max_length=32)
    tournament = models.ForeignKey(Tournament)

    def __unicode__(self):
        return "({}) {}".format(self.tournament.year.year, self.name)
    
    @property
    def winner(self):
        for r in self.round_set.all():
            if r.matchup_set.count() == 1:
                return r.matchup_set.all()[0].winner 
    
    @property
    def loser(self):
        for r in self.round_set.all():
            if r.matchup_set.count() == 1:
                return r.matchup_set.all()[0].loser

    @property
    def rounds(self):
        """
        This is used to make sure the pretty printing of the tournament
        in the full view prints the rounds in the correct order.
        """
        rnds = {}
        for round in self.round_set.all():
            rnds[round.matchup_set.all().count()] = round
        return rnds

class Round(models.Model):
    region = models.ForeignKey(Region)

class Matchup(models.Model):
    team1 = models.ForeignKey(Team, related_name="+")
    team2 = models.ForeignKey(Team, related_name="+")
    winner = models.ForeignKey(Team, related_name="+")
    round = models.ForeignKey(Round, null=True)
    # Populated only if a final four matchup
    tournament = models.ForeignKey(Tournament, related_name="semis", null=True)

    @property
    def loser(self):
        if self.winner == self.team1:
            return self.team2
        return self.team1
