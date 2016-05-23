"""
Copyright 2016, Paul Powell, All rights reserved.
"""
import random
from matchup import Matchup

#
# Implement a matchup between two teams
# This is an example of implementing Matchup, which determines
# the winner when two teams play in the tournament.
#
class FiftyFifty(Matchup):
    # teams: tuple of Team objects (Team1, Team2)
    # madness: level of madness
    def __init__(self, teams, madness):
        super(FiftyFifty, self).__init__(teams)

        self.teams = teams
        self.madness = madness

    def _play(self, madness):
        seq = [1,2]
        val = random.choice(seq)
        if val == 1:
            self.winner = self.teams[0]
            self.loser = self.teams[1]
        else:
            self.winner = self.teams[1]
            self.loser = self.teams[0]
        return (self.winner, self.loser)
