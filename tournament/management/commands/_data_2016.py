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

year = 2016

south = {1:{'name':'Kansas','power':2},
         2:{'name':'Villanova','power':0},
         3:{'name':'Miami Fla', 'power':0},
         4:{'name':'California', 'power':0},
         5:{'name':'Maryland', 'power':0},
         6:{'name':'Arizona', 'power':0},
         7:{'name':'Iowa', 'power':0},
         8:{'name':'Colorado', 'power':0},
         9:{'name':'Uconn', 'power':0},
         10:{'name':'Temple', 'power':0},
         11:{'name':'Wichita St', 'power':0},
         12:{'name':'S Dak St', 'power':0},
         13:{'name':'Hawaii', 'power':0},
         14:{'name':'Buffalo', 'power':0},
         15:{'name':'UNC-Asheville', 'power':0},
         16:{'name':'Austin Peay', 'power':0}}

west = {1:{'name':'Oregon', 'power':-1},
        2:{'name':'Oklahoma', 'power':1},
        3:{'name':'Texas AM', 'power':0},
        4:{'name':'Duke', 'power':0},
        5:{'name':'Baylor', 'power':0},
        6:{'name':'Texas', 'power':0},
        7:{'name':'Oregon St', 'power':0},
        8:{'name':'Saint Joes', 'power':0},
        9:{'name':'Cincinnati', 'power':0},
        10:{'name':'VCU', 'power':0},
        11:{'name':'N Iowa', 'power':0},
        12:{'name':'Yale', 'power':0},
        13:{'name':'UNC-Wilm', 'power':0},
        14:{'name':'Green Bay', 'power':0},
        15:{'name':'Cal-Baker', 'power':0},
        16:{'name':'Holy Cross', 'power':0}}

east = {1:{'name':'North Carolina', 'power':2},
        2:{'name':'Xavier', 'power':0},
        3:{'name':'West Va', 'power':0},
        4:{'name':'Kentucky', 'power':0},
        5:{'name':'Indiana', 'power':0},
        6:{'name':'Notre Dame', 'power':0},
        7:{'name':'Wisconsin', 'power':0},
        8:{'name':'USC', 'power':0},
        9:{'name':'Providence', 'power':0},
        10:{'name':'Pittsburgh', 'power':0},
        11:{'name':'Michigan', 'power':0},
        12:{'name':'Chattanooga', 'power':0},
        13:{'name':'Stony Brook', 'power':0},
        14:{'name':'SF Austin', 'power':0},
        15:{'name':'Weber St', 'power':0},
        16:{'name':'FGCU', 'power':0}}

midwest = {1:{'name':'Virginia', 'power':1},
           2:{'name':'Michigan St', 'power':1},
           3:{'name':'Utah', 'power':0},
           4:{'name':'Iowa St', 'power':0},
           5:{'name':'Purdue', 'power':0},
           6:{'name':'Seton Hall', 'power':0},
           7:{'name':'Dayton', 'power':0},
           8:{'name':'Texas tech', 'power':0},
           9:{'name':'Butler', 'power':0},
           10:{'name':'Syracuse', 'power':0},
           11:{'name':'Gonzaga', 'power':0},
           12:{'name':'Little Rock', 'power':0},
           13:{'name':'Iona', 'power':0},
           14:{'name':'Fresno St', 'power':0},
           15:{'name':'Middle Tenn', 'power':0},
           16:{'name':'Hampton','power':0}}

# What are the regions
all_regions = {'south':south,
               'west':west,
               'east':east,
               'midwest':midwest}

# What regions are mutually exclusive
exclusives = {'east':'midwest',
              'midwest':'east',
              'south':'west',
              'west':'south'}

# Describe the matchups in the final four
ff_games = (('south','west'),('east','midwest'))
