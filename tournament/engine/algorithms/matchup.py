"""
Copyright 2016, Paul Powell, All rights reserved.
"""
import abc

#
# Base class for implementing matchups between teams
#
# This provides the base for creating the algorithms
# that will be used to determine winners and ultimately
# the outcome of the tournament.
#
# Implementations must implement the _play method
#
class Matchup:
    __metaclass__ = abc.ABCMeta

    def __init__(self, teams):
        self.teams = teams

        # Set these in _play win winner and loser are determined
        self.winner = None
        self.loser = None

    # Return a winner Team object
    def __call__(self):
        return self._play(self.madness)

    def __repr__(self):
        return "[{}] vs {}".format(self.winner, self.loser)

    @abc.abstractmethod
    def _play(self, madness):
        #
        # Implement how game winner is determined.
        # Implementations must return a tuple of (self.winner, self.loser)
        #
        return (self.winner, self.loser)
