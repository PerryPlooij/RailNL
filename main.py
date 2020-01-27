import argparse
import textwrap

from Code.Classes import load, solution
from Code.Heuristics import greedy
from Code.Heuristics import random_once
from Code.Heuristics import random_twice
from Code.Heuristics import depth_first


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='running heuristics',
            formatter_class=argparse.RawTextHelpFormatter)

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

    # ------------------------------------------ Part of the case -------------------------------------------
    if args.part == 1:
        # Run part 1 of the case (stations in Holland)
        name = "Part1"
        timeframe = 120
        maxtrajects = 7
        connection_national = 'Attachment/ConnectiesHolland.csv'

        import_info = load.Load(connection_national, stations)
    else:
        # Run part 2 of the case (all stations in the Netherlands)
        name = "Part2"
        timeframe = 180
        maxtrajects = 20
        connection_national = 'Attachment/ConnectiesNationaal.csv'

        import_info = load.Load(connection_national, stations)

    # ---------------------------------------- Heuristic / algoritms ----------------------------------------
    if args.heuristic == 1:  
        # Run the Greedy algorithm  
        best = greedy.Routes(import_info.connections, import_info.stations, timeframe, maxtrajects)
        file = 'Solutions/{}/greedy.csv'.format(name)
    elif args.heuristic == 2: 
        # Run heuristic 'random_once' where every connection is chosen once
        best = random_once.Routes(import_info.connections, import_info.stations, timeframe, maxtrajects)
        file = 'Solutions/{}/random_once.csv'.format(name)
    elif args.heuristic == 3:
        # Run heuristic 'random twice' where a connection is chosen once or twice
        best = random_twice.Routes(import_info.connections, import_info.stations, timeframe, maxtrajects)
        file = 'Solutions/{}/random_twice.csv'.format(name)
    else:
        # Run the depth first algoritm
        best = depth_first.Routes(import_info.connections, import_info.stations, timeframe, maxtrajects)
        file = 'Solutions/{}/depth_first.csv'.format(name)


    # ------------------------------------- Besttraject and bestquality -------------------------------------
    besttraject = best.traject[0]
    bestquality = best.traject[1]

    # ----------------------------------------------- Export ------------------------------------------------
    solution.Solution(besttraject, bestquality, best.stations).export(file)
    
    # -------------------------------------------- Visualisation --------------------------------------------
    solution.Solution(besttraject, bestquality, best.stations).visualisation()