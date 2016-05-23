# Power rankings adjusted somewhat to data at:
# http://fivethirtyeight.com/interactives/march-madness-predictions-2015/#mens
#
# For start of new year, reset to zero, or adjust based on new fivethirtyeight data
#
# Average upsets: 15
#
# 300k iteration yields:
# Kentucky(1): 117937/300000 (39.3123333333%)
# Villanova(1): 35767/300000 (11.9223333333%)
# Wisconsin(1): 28324/300000 (9.44133333333%)
# Arizona(2): 26064/300000 (8.688%)
# Virginia(2): 22326/300000 (7.442%)
# Duke(1): 18937/300000 (6.31233333333%)
# Gonzaga(2): 11970/300000 (3.99%)
# Kansas(2): 8480/300000 (2.82666666667%)
# Iowa St(3): 5598/300000 (1.866%)
# Baylor(3): 4369/300000 (1.45633333333%)
# Notre Dame(3): 3881/300000 (1.29366666667%)
# Oklahoma(3): 3304/300000 (1.10133333333%)
# Georgetown(4): 2275/300000 (0.758333333333%)
# North Carolina(4): 1919/300000 (0.639666666667%)
# Maryland(4): 1665/300000 (0.555%)
# Louisville(4): 1491/300000 (0.497%)

year = 2015

south = {1:{'name':'Duke','power':0},
         2:{'name':'Gonzaga','power':0},
         3:{'name':'Iowa St', 'power':0},
         4:{'name':'Georgetown', 'power':0},
         5:{'name':'Utah', 'power':0},
         6:{'name':'SMU', 'power':0},
         7:{'name':'Iowa', 'power':0},
         8:{'name':'San Diego St', 'power':0},
         9:{'name':'St Johns', 'power':0},
         10:{'name':'Davidson', 'power':0},
         11:{'name':'UCLA', 'power':0},
         12:{'name':'Stephen Austin', 'power':0},
         13:{'name':'Eastern Wash', 'power':0},
         14:{'name':'UAB', 'power':0},
         15:{'name':'North Dakota St', 'power':0},
         16:{'name':'Robert Morris', 'power':0}}

west = {1:{'name':'Wisconsin', 'power':1},
        2:{'name':'Arizona', 'power':2},
        3:{'name':'Baylor', 'power':0},
        4:{'name':'North Carolina', 'power':0},
        5:{'name':'Arkansas', 'power':0},
        6:{'name':'Xavier', 'power':0},
        7:{'name':'VCU', 'power':0},
        8:{'name':'Oregon', 'power':0},
        9:{'name':'Oklahoma St', 'power':0},
        10:{'name':'Ohio St', 'power':0},
        11:{'name':'Ole Miss', 'power':0},
        12:{'name':'Wofford', 'power':0},
        13:{'name':'Harvard', 'power':0},
        14:{'name':'Georgia St', 'power':0},
        15:{'name':'Texas Southern', 'power':0},
        16:{'name':'Coastal Carolina', 'power':0}}

east = {1:{'name':'Villanova', 'power':2},
        2:{'name':'Virginia', 'power':2},
        3:{'name':'Oklahoma', 'power':0},
        4:{'name':'Louisville', 'power':0},
        5:{'name':'North Iowa', 'power':0},
        6:{'name':'Providence', 'power':0},
        7:{'name':'Michigan St', 'power':0},
        8:{'name':'NC State', 'power':0},
        9:{'name':'LSU', 'power':0},
        10:{'name':'Georgia', 'power':0},
        11:{'name':'Dayton', 'power':0},
        12:{'name':'Wyoming', 'power':0},
        13:{'name':'UC Irvine', 'power':0},
        14:{'name':'Albany', 'power':0},
        15:{'name':'Belmont', 'power':0},
        16:{'name':'Lafayette', 'power':0}}

midwest = {1:{'name':'Kentucky', 'power':5},
           2:{'name':'Kansas', 'power':0},
           3:{'name':'Notre Dame', 'power':0},
           4:{'name':'Maryland', 'power':0},
           5:{'name':'West Virginia', 'power':0},
           6:{'name':'Butler', 'power':0},
           7:{'name':'Wichita St', 'power':0},
           8:{'name':'Cincinnati', 'power':0},
           9:{'name':'Purdue', 'power':0},
           10:{'name':'Indiana', 'power':0},
           11:{'name':'Texas', 'power':0},
           12:{'name':'Buffalo', 'power':0},
           13:{'name':'Valparaiso', 'power':0},
           14:{'name':'Northeastern', 'power':0},
           15:{'name':'New Mexico St', 'power':0},
           16:{'name':'Hampton','power':0}}

all_regions = {'south':south,
               'west':west,
               'east':east,
               'midwest':midwest}

# What regions are mutually exclusive
exclusives = {'west':'midwest',
              'midwest':'west',
              'south':'east',
              'east':'south'}

# Describe the matchups in the final four
ff_games = (('south','east'),('west','midwest'))
