import copy, csv, random, time
import matplotlib.pyplot as plt

from datetime import datetime
from time import strftime

from Code.Classes import quality


class Depth_first:
    """
        When creating a traject, a station from the list of startstation is chosen randomly. From this station,
        a randon station of the connections is chosen to make a connection with. A connection can appear once or twice
        in the created train lining system. For a connection that occurs twice, it is checked whether there is a 
        possibility of removing one of the two connections. 
    """

    def __init__(self, stationconnections, stations, timeframe, maxtrajects):
        self.connections = stationconnections[0]
        self.connection = stationconnections[1]
        self.startstation = stationconnections[2]

        self.stations = stations
        self.timeframe = timeframe
        self.maxtrajects = maxtrajects

        self.traject = self.randomsolution()

    def randomsolution(self):
        """ 
            Create a lining system and check if a new solution is better than te previous solution.
            A traject starts at a station from the list with startstations. When all startstation are used, 
            a startstation is chosen randomly of the other stations.
        """

        bestquality = 0
        besttraject = None

        # Set the runetime, 60 * 0.1 = runtime of 6 seconds.
        t_end = time.time() + 60 * 0.1

        while time.time() < t_end:
            maxtime = self.timeframe - 20
            while maxtime <= self.timeframe:
                count = 1
                self.trajects = {}

                # Deepcopy some variables to delete a value of the variable while creating a lining system.
                # Because of deepcopy, all values can be used again when a new lining system is made.
                # Allconnections has been deepcopied twice because a connection can be used twice in the lining system.
                self.start = copy.deepcopy(self.startstation)
                self.allconnections = copy.deepcopy(self.connections)
                self.allconnections2 = copy.deepcopy(self.connections)
                self.connectioncopy = copy.deepcopy(self.connection)

                # Make a maximum of maxtraject or when all connections are used.
                while len(self.allconnections2.keys()) != 0 and count <= self.maxtrajects:
                    if self.start: 
                        city = random.choice(self.start)
                        self.maketraject(city, count, maxtime)
                        self.start.remove(city)
                    else:
                        city = random.choice(list(self.allconnections.keys()))
                        self.maketraject(city, count, maxtime)
                    count += 1

                # Check if the new quality is higher than the previous quality.
                new_quality = quality.calculate_quality(self.connectioncopy, self.connection, self.trajects)
                new_quality = self.improve(new_quality)

                if new_quality > bestquality:
                    bestquality = new_quality
                    besttraject = self.trajects

                maxtime += 1

        return besttraject, bestquality

    def maketraject(self, city, count, maxtime):
        """
            Making a traject starts with the chosen station in 'randomsolution'. The next station of the traject is
            chosen by taking a random station of all connections. This heuristic uses every connection once or twice. 
        """

        endtime = 0
        time = 0
        traject = []
        traject.append(city)

        # Check if a new city can be added to the traject.
        while time < maxtime and city in self.allconnections:
            best_stop_time = 100
            best_stop_city = ""

            # Search for a new station in the cityconnections.
            for i in range(len(self.allconnections[city])):
                if city in self.allconnections2:
                    connection = random.choice(list(self.allconnections2[city]))
                    time_traject = int(self.allconnections2[city][connection])
                else:
                    connection = random.choice(list(self.allconnections[city]))
                    time_traject = int(self.allconnections[city][connection])

                # Add new station to the traject if the new time is less or equal to the maxtime.
                if time + time_traject <= maxtime:
                    best_stop_time = time_traject
                    best_stop_city = connection
                    break

            # If new city is found set time to new time and delete connection of allconnections.
            if best_stop_city != '':
                time += best_stop_time
                endtime = time

                # Delete city and connection of the rigth dictionary.
                if city in self.allconnections2 and connection in self.allconnections2[city]:
                    del self.allconnections2[city][connection]
                    del self.allconnections2[connection][city]
                    self.connectioncopy = self.connectioncopy - 1
                else:
                    del self.allconnections[city][connection]
                    del self.allconnections[connection][city]

                if city in self.allconnections2 and len(self.allconnections2[city]) == 0:
                    del self.allconnections2[city]

                if connection in self.allconnections2 and len(self.allconnections2[connection]) == 0:
                    del self.allconnections2[connection]

                if len(self.allconnections[city]) == 0:
                    del self.allconnections[city]

                if len(self.allconnections[connection]) == 0:
                    del self.allconnections[connection]

                city = best_stop_city
                traject.append(city)
            else:
                endtime = time
                time = maxtime

                # Make traject with a length of at least two stations.
                if len(traject) == 1:
                    connections = self.connections[traject[0]]
                    endcity = min(connections, key=lambda k: connections[k])
                    endtime = int(connections[endcity])
                    traject.append(endcity)

        self.trajects[count] = (traject, endtime)

    def improve(self, best):
        """ Delete double connections at the end or beginning of a traject. """

        run = True
        while run:
            for key1, value1 in self.trajects.items():

                # Check if connection at beginning of traject exists in other traject.
                if len(value1[0]) >= 2:
                    beginbegin = value1[0][0]
                    beginend = value1[0][1]

                    for key2, value2 in self.trajects.items():
                        for i in range(1, len(value2[0]) - 1):
                            add = False
                            if value2[0][i] == beginbegin and value2[0][i + 1] == beginend:
                                time = self.trajects[key1][1]
                                newtime = time - int(self.connections[beginbegin][beginend])
                                add = True

                            elif value2[0][i] == beginend and value2[0][i + 1] == beginbegin:
                                time = self.trajects[key1][1]
                                newtime = time - int(self.connections[beginend][beginbegin])
                                add = True

                            # Delete startstation and change trajecttime.
                            if add:
                                del self.trajects[key1][0][0]
                                listtraject = list(self.trajects[key1])
                                listtraject[len(listtraject) - 1] = newtime
                                self.trajects[key1] = tuple(listtraject)
                                break

                # Check if a connection at the end of a traject exists in another traject.
                if len(value1[0]) >= 2:
                    endbegin = value1[0][-2]
                    endend = value1[0][-1]

                    for key2, value2 in self.trajects.items():
                        for i in range(len(value2[0]) - 2):
                            add = False
                            if value2[0][i] == endbegin and value2[0][i + 1] == endend:
                                time = self.trajects[key1][1]
                                newtime = time - int(self.connections[endbegin][endend])
                                add = True

                            elif value2[0][i] == endend and value2[0][i + 1] == endbegin:
                                time = self.trajects[key1][1]
                                newtime = time - int(self.connections[endend][endbegin])
                                add = True

                            # Delete endstation and change trajecttime.
                            if add:
                                del self.trajects[key1][0][-1]
                                listtraject = list(self.trajects[key1])
                                listtraject[len(listtraject) - 1] = newtime
                                self.trajects[key1] = tuple(listtraject)
                                break

            new = quality.calculate_quality(self.connectioncopy, self.connection, self.trajects)
            if new == best:
                run = False
            else:
                best = new

        return best