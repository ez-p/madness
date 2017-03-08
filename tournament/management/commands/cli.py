from django.core.management.base import BaseCommand
from django.conf import settings

import sys
import time

import tournament.engine.data as data
from tournament.engine.tourney import *
from tournament.engine.region import *
from _printer import Printer
import _stats as stats

def usage():
    print "\nUsage: python madness.py [-h] [-f] [-m VALUE] [-w WINNER] [-s SECOND] [-e ENGINE]"
    print "Options:"
    print "   -h, --help:    print detailed help"
    print "   -m, --madness: adjust the madness level of the tournament"
    print "   -w, --winner:  select the tournament winner"
    print "   -s, --second:  select the tournament runner up"
    print "   -f, --file:    save the bracket to a text file"
    print "   -e, --engine:  choose a tournament engine"
    print "   -y, --year:  choose a tournament engine"
    print ""
    print "Available Engines:"
    print "   SeedOdds  : Winner is determined based on team seeds"
    print "   FiftyFifty: Every teams has a 50-50 chance of winning"
    print ""
    print "Example:"
    print '   python madness.py -f -m 2 -w "Villanova" -s "North Carolina" -e "SeedOdds"'

def help():
    usage()
    print ""
    print "This program will randomnly select a NCAA bracket by simulating the"
    print "tournament. The secret sauce is the engine which calculates the winner"
    print "using a fancy algorithm."
    print ""
    print "You can manually select the winner and/or runner up using the options."
    print "The program will run simulations until a result that matches your"
    print "selections is obtained."
    print ""
    print "ENGINES"
    print "-------"
    print "Choose from the available engines for determining the tournament outcome"
    print ""
    print "SeedOdds: (Default) Team with the high seed has the better chance of winning."
    print "          The higher seed's chance of winning increases with the seed spread."
    print "          The number of upsets generated by this engine trends toward the 25"
    print "          year average of 18 when running hundreds of thousands of simulations."
    print ""
    print "Fifty-Fifty: For demonstration purposes only. The winner is determined by a"
    print "             coin flip."
    print ""
    print "MADNESS"
    print "-------"
    print "The algorithm can be adjusted using the 'madness' input parameter."
    print "By default the madness variable is set to one.  As the madness"
    print "variable increases so does the tournament craziness. Lower seed"
    print "teams have an increasing chance of winning against a higher seed"
    print "as the madness increases."
    print ""
    print "The default madness level of one creates the average amount of"
    print "madness seen over the last 25 years.  Increasing the madness past 2"
    print "can create some truly crazy brackets! For example a madness level 3"
    print "starts to show a large number of 4,5,6 seeds in the final four, and"
    print "you can even see some 7+ seeds in the final four."
    print ""
    print "POWER"
    print "-----"
    print "There is an internal 'power' level associated with each team."
    print "The default is zero. For especially strong teams this can be adjusted"
    print "up to one or two.  In 2015, undefeated Kentucky would warrants a power"
    print "level of five!"
    print ""
    print "The power level is tweaked for a particular year to resemble the rankings"
    print "at www.fivethirtyeight.com."

def find_region(year, name):
    all_regions_cache = data.all_regions(year)
    for region in all_regions_cache:
        names = []
        for entry in all_regions_cache[region].values():
            names.append(entry['name'])
        if name in names:
            return region

def possible_matchup(year, winner, second):
    w_region = find_region(year, winner)
    s_region = find_region(year, second)

    if w_region == s_region:
        d = "({})".format(w_region.capitalize())
        print "Selected teams are in the same region {}".format(d)
        return False

    if data.exclusives(year)[w_region] == s_region:
        d = "({}, {})".format(w_region.capitalize(), s_region.capitalize())
        print "Selected team regions are mutually exclusive {}".format(d)
        return False

    return True

def verify_team_name(year, name):
    if not name:
        return True

    for r in data.all_regions(year).values():
        for team in r.values():
            if name == team['name']:
                return True
    return False

def check_input(year, madness, winner, second):
    if not verify_team_name(year, winner):
        print "Team name invalid: '{}'".format(winner)
        return False

    if second:
        if not verify_team_name(year, second):
            print "Team name invalid: '{}'".format(second)
            return False

    if second and winner:
        if not possible_matchup(year, winner, second):
            return False
    return True

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:],
                                   "hfx:m:w:s:e:",
                                   ["help", "file", "stats=", "madness=",
                                    "winner=", "second=", "engine="])
    except getopt.GetoptError as err:
        print str(err)
        usage()
        sys.exit(2)
    
    # Madness of 1 gives us close to average number of upsets (18)
    # Madness of 0 gives less upsets
    # madness of 2 gives more upsets
    year = settings.DEFAULT_YEAR
    madness = 1
    winner = None
    second = None
    print_to_file = False
    stat_run = False
    iterations = None
    from tournament.engine.algorithms.seedodds import SeedOddsMatchup as engine
    for o,a in opts:
        if o in ("-m", "--madness"):
            madness = int(a)
        if o in ("-w", "--winner"):
            winner = a
        if o in ("-s", "--second"):
            second = a
        if o in ("-f", "--file"):
            print_to_file = True
        if o in ("-e", "--engine"):
            if a == "SeedOdds":
                from tournament.engine.algorithms.seedodds import SeedOddsMatchup as engine
            elif a == "FiftyFifty":
                from tournamen.engine.algorithms.fiftyfifty import FiftyFifty as engine
            else:
                print "Unkown engine: '{}'".format(a)
                usage()
                sys.exit()
        if o in ("-x", "--stats"):
            stat_run = True
            try:
                iterations = int(a)
            except:
                iterations = None
        if o in ("-h", "--help"):
            help()
            sys.exit()
   
    if not check_input(year, madness, winner, second):
        sys.exit()

    if stat_run:
        s = stats.Stats(year, winner, second, madness, engine, iterations)
        s.run()
        sys.exit(0)

    tourney = Tournament(year, winner, second, madness, engine)
    results = tourney()

    printer = Printer(tourney, print_to_file)
    printer.print_to_file(year)
    printer.print_to_screen()
    stats.print_stats(results)
    
class Command(BaseCommand):
    def add_arguments(self, parser):
        # Named arguments
        parser.add_argument('-m', '--madness', type=int, default=1, help="Specify madness level")
        parser.add_argument('-w', '--winner', help="Specify the winner")
        parser.add_argument('-s', '--second', help="Specify the runner-up")
        parser.add_argument('-f', '--file', help="Save tournament results to a file", action='store_true')
        parser.add_argument('-e', '--engine', choices=['SeedOdds','FiftyFifty'], default='SeedOdds',
                help="Specify the engine used to run the tournament.")
        parser.add_argument('-x', '--stats', type=int, default=0, help="Do a statistics run")
        parser.add_argument('-y', '--year', type=int, default=settings.DEFAULT_YEAR, help="Specify year")
        parser.add_argument('-d', '--db', help="Save tournament results to database", action='store_true')

    # Get'r done
    def handle(self, *args, **options):
        madness = options['madness']
        winner = options['winner']
        second = options['second']
        iterations = options['stats']
        year = options['year']
        
        if options['engine']  == "SeedOdds":
            from tournament.engine.algorithms.seedodds import SeedOddsMatchup as engine
        elif options['engine']  == "FiftyFifty":
            from tournament.engine.algorithms.fiftyfifty import FiftyFifty as engine
        else:
            # Shouldn't ever get here...
            print "Invalid Engine!"
            parser.print_usage()
       
        if not check_input(year, madness, winner, second):
            sys.exit()

        if iterations:
            s = stats.Stats(year, winner, second, madness, engine, iterations)
            s.run()
            sys.exit(0)

        tourney = Tournament(year, winner, second, madness, engine)
        start = time.time()
        results = tourney()
        print "Execution time: {}".format(time.time() - start)

        printer = Printer(tourney, options['file'])
        printer.print_to_file(year)
        printer.print_to_screen()
        stats.print_stats(results)

        if options['db']:
            # Save the results to the database
            import tournament.views as views
            id = views._save_tournament(results)
            print "\nResults saved to database: {}".format(id)
