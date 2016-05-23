"""
Copyright 2016, Paul Powell, All rights reserved.
"""
class Team:
    def __init__(self, info, region, seed):
        self.name = info['name']
        self.region = region
        self.seed = seed
        self.power = info['power']

    def __repr__(self):
        return "{}({})".format(self.name, self.seed)
