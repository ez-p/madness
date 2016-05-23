"""
Copyright 2016, Paul Powell, All rights reserved.
"""
import region
import data 

class Tournament:
    def __init__(self, year, winner, second, madness, algorithm):
        self.year = year
        self.winner = winner
        self.second = second 
        self.madness = madness
        self.algorithm = algorithm
        self.results = None
    
    def _is_upset(self, match):
        seeds = [match.teams[0].seed, match.teams[1].seed] 
        expected_winner = sorted(seeds)[0] 
        if match.winner.seed != expected_winner: 
            return 1 
        return 0

    def _upsets(self, results):
        upsets = 0 
        for r in data.all_regions(self.year):
            region = results[r]
            for round in region.rounds:
                for match in round.results:
                    upsets += self._is_upset(match)
            upsets += self._is_upset(region.final)

        upsets += self._is_upset(results['semi1'])
        upsets += self._is_upset(results['semi2'])
        upsets += self._is_upset(results['championship'])
        return upsets

    def __call__(self):
        if self.winner or self.second:
            self.results = self.run_specific()
            return self.results
        
        self.results = self._run(self.madness)
        return self.results

    def _run(self, madness):
        results = {'year':self.year,
                   'south':None,
                   'west':None,
                   'east':None,
                   'midwest':None,
                   'semi1':None,
                   'semi2':None,
                   'final_four':None,
                   'finalist':None,
                   'champion':None}

        final_four = {'south':None,
                      'west':None,
                      'east':None,
                      'midwest':None}

        # Database lookup, so cache this info
        all_regions = data.all_regions(self.year)
        for key in all_regions:
            r = region.Region(key, all_regions[key], self.algorithm)
            # Winner of region goes to final four
            final_four[key] = r(madness)
            results[key] = r

        semis = []
        for match in data.ff_games(self.year):
            team1,team2  = match
            semis.append(self.algorithm((final_four[team1],final_four[team2]), madness))

        finalist = (semis[0]()[0], semis[1]()[0])

        championship = self.algorithm(finalist, madness)
        champion,loser = championship()

        results['semi1'] = semis[0]
        results['semi2'] = semis[1]
        results['final_four'] = final_four
        results['finalist'] = finalist
        results['championship'] = championship 
        results['champion'] = champion
        results['2nd_place'] = loser
        results['upsets'] = self._upsets(results)

        return results

    def run_specific(self):
        count = 1
        results = self._run(self.madness)
        champion = results['champion']
        finalist = results['finalist']
        loser = results['2nd_place']

        if not self.second:
            # Just winner specified
            while champion.name != self.winner:
                count += 1
                results = self._run(self.madness)
                champion = results['champion']
                finalist = results['finalist']
                loser = results['2nd_place']
                if not count % 50000:
                    print "{} itertions.".format(count)
        elif not self.winner:
            # Just second specified
            while loser.name != self.second:
                count += 1
                results = self._run(self.madness)
                champion = results['champion']
                finalist = results['finalist']
                loser = results['2nd_place']
                if not count % 50000:
                    print "{} itertions.".format(count)
        else:
            # Winner and second specified
            while champion.name != self.winner or loser.name != self.second:
                count += 1
                results = self._run(self.madness)
                champion = results['champion']
                finalist = results['finalist']
                loser = results['2nd_place']
                if not count % 50000:
                    print "{} itertions.".format(count)

        print "Result found in {} iterations.".format(count)
        return results
