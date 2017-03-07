"""
Copyright 2016, Paul Powell, All rights reserved.
"""
class Team:
    def __init__(self, info, region, seed, sf=1):
        self.name = info['name']
        self.region = region
        self.seed = seed
        self.power = info['power']
        # Second or first flag. 1 = Not Set, 2 = Second, 3 = First
        self.sf = sf

    def __repr__(self):
        return "{}({})".format(self.name, self.seed)
