import sys
import tournament.engine.region as region
import tournament.engine.data as data

class Printer:
    def __init__(self, tournament, print_to_file):
        self.results = tournament.results
        self.to_file = print_to_file

    def make_file_name(self):
        team1 = self.results['finalist'][0].name
        team2 = self.results['finalist'][1].name
        champion = None
        second = None
        if self.results['champion'].name == team1:
            champion = team1
            second = team2
        else:
            champion = team2
            second = team1

        name = "{}_vs_-{}-.txt".format(second, champion)
        return name.replace(" ", "_")
    
    def print_round(self, f, round):
        f.write("Round {}\n".format(round.number))
        f.write("--------\n")
        for match in round.results:
            f.write("{} vs {}: {}\n".format(match.team1['team'],
                                            match.team2['team'],
                                            match.winner))

    def print_region(self, f, region):
        f.write("{}\n".format(region.name.upper()))
        f.write("======\n")
        for round in region.rounds:
            self.print_round(f, round) 

    def print_final_four(self, f, final_four):
        f.write("===== Final Four =====\n")
        f.write("South: {}\n".format(final_four['south']))
        f.write("West: {}\n".format(final_four['west']))
        f.write("East: {}\n".format(final_four['east']))
        f.write("Midwest: {}\n".format(final_four['midwest']))

    def print_championship(self, f, finalist): 
        f.write("===== Championship =====\n")
        for team in finalist:
            f.write("{}\n".format(team))

    def print_champ(self, f, results):
        f.write("===== Champion ({}) =====\n".format(results['year']))
        f.write("{}".format(results['champion']))
    

    def print_to_file(self):
        if not self.to_file:
            return
        with open(self.make_file_name(), 'a') as f:
            for r in data.all_regions():
                self.print_region(f, self.results[r])
                f.write("\n")
            self.print_final_four(f, self.results['final_four'])
            f.write("\n")
            self.print_championship(f, self.results['finalist'])
            f.write("\n")
            self.print_champ(f, self.results)

    def print_to_screen(self):
        self.print_final_four(sys.stdout, self.results['final_four'])
        sys.stdout.write("\n")
        self.print_championship(sys.stdout, self.results['finalist'])
        sys.stdout.write("\n")
        self.print_champ(sys.stdout, self.results)
        sys.stdout.write('\n\n')
