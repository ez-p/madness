# Power rankings adjusted somewhat to data at:
# http://projects.fivethirtyeight.com/2016-march-madness-predictions/
#
# See: three_k_run for 300,000 sample results
#
# For start of new year, reset to zero, or adjust based on new fivethirtyeight data
#
# Average upsets: 16
# 
# 300k iteration yields:
# Kansas(1): 59283/300000 (19.761%)
# North Carolina(1): 56051/300000 (18.6836666667%)
# Virginia(1): 38544/300000 (12.848%)
# Oklahoma(2): 25526/300000 (8.50866666667%)
# Michigan St(2): 24033/300000 (8.011%)
# Oregon(1): 15275/300000 (5.09166666667%)
# Villanova(2): 13974/300000 (4.658%)
# Xavier(2): 13726/300000 (4.57533333333%)
# Texas AM(3): 8502/300000 (2.834%)
# Miami Fla(3): 7545/300000 (2.515%)
# Utah(3): 7291/300000 (2.43033333333%)
# West Va(3): 7156/300000 (2.38533333333%)
# Duke(4): 4222/300000 (1.40733333333%)
# California(4): 3374/300000 (1.12466666667%)
# Kentucky(4): 2930/300000 (0.976666666667%)
# Iowa St(4): 2887/300000 (0.962333333333%)

year = 2017

south = {1:{'name':'North Carolina','power':0},
         2:{'name':'Kentucky','power':0},
         3:{'name':'UCLA', 'power':0},
         4:{'name':'Butler', 'power':0},
         5:{'name':'Minnesota', 'power':0},
         6:{'name':'Cincinnati', 'power':0},
         7:{'name':'Dayton', 'power':0},
         8:{'name':'Arkansas', 'power':0},
         9:{'name':'Seton Hall', 'power':0},
         10:{'name':'Wichita St', 'power':0},
         11:{'name':'Kansas-St or Wake Forest', 'power':0},
         12:{'name':'Middle Tenn', 'power':0},
         13:{'name':'Winthrop', 'power':0},
         14:{'name':'Kent St', 'power':0},
         15:{'name':'N. Kentucky', 'power':0},
         16:{'name':'Texas Southern', 'power':0}}

west = {1:{'name':'Gonzaga', 'power':2},
        2:{'name':'Arizona', 'power':0},
        3:{'name':'Florida St', 'power':0},
        4:{'name':'West Virginia', 'power':0},
        5:{'name':'Notre Dame', 'power':0},
        6:{'name':'Maryland', 'power':0},
        7:{'name':'Saint Marys', 'power':0},
        8:{'name':'N Western', 'power':0},
        9:{'name':'Vanderbilt', 'power':0},
        10:{'name':'VCU', 'power':0},
        11:{'name':'Xavier', 'power':0},
        12:{'name':'Princeton', 'power':0},
        13:{'name':'Bucknell', 'power':0},
        14:{'name':'Fl Gulf Coast', 'power':0},
        15:{'name':'N Dakota', 'power':0},
        16:{'name':'S Dakota St', 'power':0}}

east = {1:{'name':'Villanova', 'power':3},
        2:{'name':'Duke', 'power':1},
        3:{'name':'Baylor', 'power':0},
        4:{'name':'Florida', 'power':0},
        5:{'name':'Virginia', 'power':0},
        6:{'name':'SMU', 'power':0},
        7:{'name':'S Carolina', 'power':0},
        8:{'name':'Wisconsin', 'power':0},
        9:{'name':'Virginia Tech', 'power':0},
        10:{'name':'Marquette', 'power':0},
        11:{'name':'Providence or USC', 'power':0},
        12:{'name':'UNC Wilmington', 'power':0},
        13:{'name':'East Tenn St', 'power':0},
        14:{'name':'NM State', 'power':0},
        15:{'name':'Troy', 'power':0},
        16:{'name':'MSM or N Orleans', 'power':0}}

midwest = {1:{'name':'Kansas', 'power':1},
           2:{'name':'Louisville', 'power':0},
           3:{'name':'Oregon', 'power':0},
           4:{'name':'Purdue', 'power':0},
           5:{'name':'Iowa St', 'power':0},
           6:{'name':'Creighton', 'power':0},
           7:{'name':'Michigan', 'power':0},
           8:{'name':'Miama Fl', 'power':0},
           9:{'name':'Michigan St', 'power':0},
           10:{'name':'Oklahoma St', 'power':0},
           11:{'name':'Rhode Island', 'power':0},
           12:{'name':'Nevada', 'power':0},
           13:{'name':'Vermont', 'power':0},
           14:{'name':'Iona', 'power':0},
           15:{'name':'Jacksonville St', 'power':0},
           16:{'name':'NC Central or UC Davis','power':0}}

# What are the regions
all_regions = {'south':south,
               'west':west,
               'east':east,
               'midwest':midwest}

# What regions are mutually exclusive
exclusives = {'east':'west',
              'west':'east',
              'south':'midwest',
              'midwest':'south'}

# Describe the matchups in the final four
ff_games = (('east','west'),('south','midwest'))
