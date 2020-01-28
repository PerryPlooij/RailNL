# *********************************************************************************************************************
# * main.py
# *
# * PGT Party
# *
# * Run part one or two of the case and a chosen algorithm using the given arguments in the command-line.
# *********************************************************************************************************************


import argparse
import textwrap

from Code.Classes import load, solution
from Code.Heuristics import greedy
from Code.Heuristics import random_once
from Code.Heuristics import random_twice
from Code.Heuristics import depth_first


if __name__ == '__main__':

    # User-friendly command-line interface with required arguments
    parser = argparse.ArgumentParser(description='running heuristics', formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('part', type=int, choices=[1, 2], 
                        help=textwrap.dedent('''\
                            1: Holland
                            2: National

                            '''))
    parser.add_argument('heuristic', type=int, choices=[1, 2, 3, 4],
                        help=textwrap.dedent('''\
                            1: Greedy
                            2: Random once
                            3: Random twice
                            4: Depth first
                            '''))
    args = parser.parse_args()

    stations = 'Attachment/StationsNationaal.csv'


    # --------------------------------------- Chose part of the case ----------------------------------------

    # Run part 1 of the case (stations in Holland)
    if args.part == 1:
        name = "Part1"
        timeframe = 120
        maxtrajects = 7
        connection_national = 'Attachment/ConnectiesHolland.csv'

    # Run part 2 of the case (all stations in the Netherlands)
    else:
        name = "Part2"
        timeframe = 180
        maxtrajects = 20
        connection_national = 'Attachment/ConnectiesNationaal.csv'

    import_info = load.Load(connection_national, stations)


    # ---------------------------------------- Heuristic / algoritms ----------------------------------------
    
    # Run the Greedy algorithm 
    if args.heuristic == 1: 
        best = greedy.Greedy(import_info.connections, import_info.stations, timeframe, maxtrajects)
        file = 'Solutions/{}/greedy.csv'.format(name)
    
    # Run heuristic 'random_once' where every connection is chosen once
    elif args.heuristic == 2: 
        best = random_once.Random_once(import_info.connections, import_info.stations, timeframe, maxtrajects)
        file = 'Solutions/{}/random_once.csv'.format(name)
    
    # Run heuristic 'random twice' where a connection is chosen once or twice
    elif args.heuristic == 3:
        best = random_twice.Random_twice(import_info.connections, import_info.stations, timeframe, maxtrajects)
        file = 'Solutions/{}/random_twice.csv'.format(name)
    
    # Run the depth first algoritm
    else:
        best = depth_first.Routes(import_info.connections, import_info.stations, timeframe, maxtrajects)
        file = 'Solutions/{}/depth_first.csv'.format(name)

    besttraject = best.traject[0]
    bestquality = best.traject[1]

    # ----------------------------------------------- Export ------------------------------------------------
    solution.export(file, besttraject, bestquality)
    
    # -------------------------------------------- Visualisation --------------------------------------------
    solution.visualisation(besttraject, best.stations)