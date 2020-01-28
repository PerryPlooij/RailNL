# ************************************************************************************************
# * random_once.py
# *
# * PGT Party
# *
# * Timetable with every connection once and the startstation and connection randomly chosen.
# ************************************************************************************************


import copy, csv, random, time
import matplotlib.pyplot as plt

from datetime import datetime
from time import gmtime, strftime

from Code.Classes import quality


class Routes():
    def __init__(self, stationconnections, stations, timeframe, maxtrajects):
        self.connections = stationconnections[0]
        self.connection = stationconnections[1]
        self.startstation = stationconnections[2]

        self.stations = stations
        self.timeframe = timeframe
        self.maxtrajects = maxtrajects

        self.traject = self.heuristiek()

    def randomsolution(self):
        """ Create random solution and check if a new solution is better than the previous solution  """
        
        bestquality = 0
        besttraject = None

        # Set the runetime, 60 * 0.1 = runtime of 6 seconds
        t_end = time.time() + 60 * 0.1

        while time.time() < t_end:
            maxtime = self.timeframe - 20
            while maxtime <= self.timeframe:
                count = 1
                self.trajects = {}

                self.start = copy.deepcopy(self.startstation)

                # Deepcopy allconnections to make sure all connections are available by making new trajects
                self.allconnections = copy.deepcopy(self.connections)

                # Deepcopy the total amount of connections (connectioncopy) to reduce the amount (connection)
                # when making a new connection
                self.connectioncopy = copy.deepcopy(self.connection)

                # Make a maximum of 7 traject or when all connections are used with a random station as startstation
                while len(self.allconnections.keys()) != 0 and count <= self.maxtrajects:
                    if self.start: 
                        city = random.choice(self.start)
                        self.maketraject(city, count, maxtime)
                        self.start.remove(city)
                    else:
                        city = random.choice(list(self.allconnections.keys()))
                        self.maketraject(city, count, maxtime)
                    count += 1

                # Check if the new quality is higher than the previous quality
                new_quality = quality.calculate_quality(self.connectioncopy, self.connection, self.trajects)

                if new_quality > bestquality:
                    bestquality = new_quality
                    besttraject = self.trajects

                maxtime += 1

        return besttraject, bestquality

    def maketraject(self, city, count, maxtime):
        """ Making a new traject with a given maxtime """

        endtime = 0
        time = 0
        traject = []
        traject.append(city)

        # Check if a new city can be added to the traject
        while time < maxtime and city in self.allconnections:
            best_stop_time = 100
            best_stop_city = ""
        
            # Search for a new station in the cityconnections
            for i in range(len(self.allconnections[city])):
                connection = random.choice(list(self.allconnections[city]))
                time_traject = int(self.allconnections[city][connection])
                
                # Add new station to the traject if the new time is less or equal to the maxtime
                if time + time_traject < maxtime:
                    best_stop_time = connectiontime
                    best_stop_city = connection
                    break
            
            # If new city is found set time to new time and delete connection of allconnections
            if best_stop_city != '':
                time += best_stop_time
                endtime = time
                del self.allconnections[city][connection]
                del self.allconnections[connection][city]
                self.connectioncopy = self.connectioncopy - 1

                if len(self.allconnections[city]) == 0:
                    del self.allconnections[city]

                if len(self.allconnections[connection]) == 0:
                    del self.allconnections[connection]

                city = best_stop_city
                traject.append(city)
            else:
                endtime = time
                time = maxtime
            
                # Make traject with a length of at least two stations
                if len(traject) == 1:
                    connections = self.connections[traject[0]]
                    endcity = min(connections, key=lambda k: connections[k])
                    endtime = int(connections[endcity])
                    traject.append(endcity)

        self.trajects[count] = (traject, endtime)