"""
Copyright 2016, Paul Powell, All rights reserved.
"""
from tournament.models import *

# This converts the database data into the data format
# understood by the tournament engine

def build_region_dic(year, name):
    teams = {}
    y = Year.objects.get(year=year)
    region = RegionData.objects.filter(year=y).get(name=name)
    for t in region.team_set.all():
        teams[t.seed] = {'name':t.name, 'power':t.power}
    return teams

def south(year):
    return build_region_dic(year, 'south')

def west(year):
    return build_region_dic(year, 'west')

def east(year):
    return build_region_dic(year, 'east')

def midwest(year):
    return build_region_dic(year, 'midwest')

# What are the regions
def all_regions(year):
    return {'south':south(year),
             'west':west(year),
             'east':east(year),
             'midwest':midwest(year)}

# What regions are mutually exclusive
def exclusives(year):
    dic = {}
    y = Year.objects.get(year=year)
    for r in RegionData.objects.filter(year=y):
        dic[r.name] = r.exclusive.name
    return dic
    """
    return {'east':'midwest',
            'midwest':'east',
            'south':'west',
            'west':'south'}
    """

# Describe the matchups in the final four
def ff_games(year):
    games = []
    y = Year.objects.get(year=year)
    games.append((RegionData.objects.filter(year=y)[0].name, RegionData.objects.filter(year=y)[0].ff_match.name))
    for r in RegionData.objects.filter(year=y)[1:4]:
        if games[0][0] == r.name or games[0][0] == r.ff_match.name:
            continue
        games.append((r.name, r.ff_match.name))
        break
        
    return tuple(games)
    """
    return (('south','west'),('east','midwest'))
    """
