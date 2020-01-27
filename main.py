from Code.Classes import load, solution
from Code.Heuristics import greedy
from Code.Heuristics import random_once
from Code.Heuristics import random_twice
from Code.Heuristics import random_twice_improved


if __name__ == '__main__':
    
    stations = 'Attachment/StationsNationaal.csv'

    # ----------------------------------------------- Part 1 ------------------------------------------------

    # timeframe = 120
    # maxtrajects = 7
    # connection_national = 'Attachment/ConnectiesHolland.csv'

    # delete_station = ""
    # if delete_station:
    #     name = "Advanced"
    # else:
    #     name = "Part1"
        
    # import_info = load.Load(connection_national, stations, delete_station)

    # ----------------------------------------------- Part 2 ------------------------------------------------

    timeframe = 180
    maxtrajects = 20
    connection_national = 'Attachment/ConnectiesNationaal.csv'

    delete_station = ""
    if delete_station:
        name = "Advanced"
    else:
        name = "Part2"

    import_info = load.Load(connection_national, stations, delete_station)
    
    # ------------------------------------------- Greedy ------------------------------------------

    # best = greedy.Routes(import_info.connections, import_info.stations, timeframe, maxtrajects)
    # file = 'Solutions/{}/greedy.csv'.format(name)

    # --------------------------------------------- Random once ---------------------------------------------

    # best = random_once.Routes(import_info.connections, import_info.stations, timeframe, maxtrajects)
    # file = 'Solutions/{}/random_once.csv'.format(name)

    # -------------------------------------------- Random twice ---------------------------------------------

    # best = random_twice.Routes(import_info.connections, import_info.stations, timeframe, maxtrajects)
    # file = 'Solutions/{}/random_twice.csv'.format(name)

    # ------------------------------------ Random twice with improvement ------------------------------------

    best = random_twice_improved.Routes(import_info.connections, import_info.stations, timeframe, maxtrajects)
    file = 'Solutions/{}/random_twice_improved.csv'.format(name)

    # ------------------------------------- Besttraject and bestquality -------------------------------------
    besttraject = best.traject[0]
    bestquality = best.traject[1]

    # ----------------------------------------------- Export ------------------------------------------------
    solution.Solution(besttraject, bestquality, best.stations).export(file)
    
    # -------------------------------------------- Visualisation --------------------------------------------
    solution.Solution(besttraject, bestquality, best.stations).visualisation()