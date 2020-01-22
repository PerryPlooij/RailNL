# ****************************************************************************************************
# * random_twice_improved1.py
# *
# * PGT Party
# *
# * Timetable with every connection maximum twice and the startstation and connection randomly chosen.
# * After creating a solution, check if quality can be improved by deleting double connections.
# ****************************************************************************************************


import copy
import csv
import random
import time

import matplotlib.pyplot as plt


class Routes():
    def __init__(self):
        self.connections = {}
        self.connection = 0

        # Import all connections of the stations
        with open('../Bijlage/ConnectiesHolland.csv', 'rt') as csv_file:
            reader = csv.reader(csv_file, delimiter=',')
            
            for row in reader: 
                self.connection += 1
                if row[0] not in self.connections:
                    self.connections[row[0]] = {}
                self.connections[row[0]][row[1]] = row[2]

                if row[1] not in self.connections:
                    self.connections[row[1]] = {}
                self.connections[row[1]][row[0]] = row[2]
        
        # Import all stations 
        with open('../Bijlage/StationsNationaal.csv', 'rt') as csv_file:
            reader = csv.reader(csv_file, delimiter=',')
            self.stations = {}

            for row in reader:
                if row[0] not in self.stations:
                    self.stations[row[0]] = (float(row[2]),float(row[1]))


    def randomsolution(self):
        """ Create random solution and check if a new solution is better than the previous solution  """

        amount = 0
        randomcount = 0
        bestquality = 0
        besttime = 0
        besttraject = None
        t_end = time.time() + 60 * 2

        while time.time() < t_end:
        # while randomcount < 500:
            maxtime = 160
            while maxtime <= 180:
                count = 1
                amount += 1
                self.trajects = {}

                # Deepcopy allconnections twice to make sure all connections are available twice by making new trajects
                self.allconnections = copy.deepcopy(self.connections)
                self.allconnections2 = copy.deepcopy(self.connections)

                # Deepcopy the total amount of connections (connectioncopy) to reduce the amount (connection)
                # when making a new connection
                self.connectioncopy = copy.deepcopy(self.connection)

                # Make a maximum of 7 traject or when all connections are used with a random station as startstation
                while len(self.allconnections2.keys()) != 0 and count <= 7:
                    city = random.choice(list(self.allconnections2.keys()))
                    self.maketraject(city, count, maxtime)
                    count += 1
                
                # Check if the new quality is higher than the previous quality
                best = self.quality()
                best = self.improve(best)

                if best > bestquality:
                    bestquality = best
                    besttraject = self.trajects
                    besttime = maxtime
                    tijd = time.time() - t_start
                    print("tijd {}".format(tijd))
                    print("herhalingen {}".format(amount))
                    print("besttraject {}".format(besttraject))
                    print("bestquality {}".format(bestquality))

                maxtime += 1

            randomcount += 1

        self.visualisation(besttraject)


    def maketraject(self, city, count, maxtime):
        """ Making a new traject with a given maxtime """

        endtime = 0
        time = 0
        traject = []
        traject.append(city)
        
        # Check if a new city can be added to the traject
        while time < maxtime and count <= 7 and city in self.allconnections:
            best_stop_time = 100
            best_stop_city = ""

            # Search for a new station in the cityconnections
            for i in range(len(self.allconnections[city])):
                if city in self.allconnections2:
                    connection = random.choice(list(self.allconnections2[city]))
                    time_traject = int(self.allconnections2[city][connection])
                else:
                    connection = random.choice(list(self.allconnections[city]))
                    time_traject = int(self.allconnections[city][connection])

                # Add new station to the traject if the new time is less or equal to the maxtime
                if time + time_traject <= maxtime:
                    best_stop_time = time_traject
                    best_stop_city = connection
                    break

            # If new city is found set time to new time and delete connection of allconnections
            if best_stop_city != '':
                time += best_stop_time
                endtime = time

                # Delete city and connection of the rigth dictionary
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
            
                # Make traject with a length of at least two stations
                if len(traject) == 1:
                    connections = self.connections[traject[0]]
                    endcity = min(connections, key=lambda k: connections[k])
                    endtime = int(connections[endcity])
                    traject.append(endcity)

        self.trajects[count] = (traject, endtime)


    def improve(self, best):
        """ Delete double connections at the end or beginning of a traject """

        run = True
        while run:
            for key1, value1 in self.trajects.items():

                # Check if connection at beginning of traject exists in other traject
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

                            # Delete startstation and change trajecttime
                            if add:
                                del self.trajects[key1][0][0]
                                listtraject = list(self.trajects[key1])
                                listtraject[len(listtraject) - 1] = newtime
                                self.trajects[key1] = tuple(listtraject)
                                break

                # Check if connection at end of traject exists in other traject
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

                            # Delete endstation and change trajecttime
                            if add:
                                del self.trajects[key1][0][-1]
                                listtraject = list(self.trajects[key1])
                                listtraject[len(listtraject) - 1] = newtime
                                self.trajects[key1] = tuple(listtraject)
                                break
                                    
            new = self.quality()
            if new == best:
                run = False
            else:
                best = new
            return best


    def quality(self):
        """ Calculate quality of the created timetable """

        minutes = 0
        p = 1 - self.connectioncopy / self.connection
        T = len(self.trajects)

        for key, value in self.trajects.items():
            minutes += value[1]

        K = p * 10000 - (T * 100 + minutes)
        return K


    def visualisation(self, traject):
        """ Make a visualisation of the best timetable """

        colors = ["green", "red", "aqua", "orange", "yellow", "lawngreen", "deepskyblue"]
        img = plt.imread("../../doc/kaart.png")
        fix, ax = plt.subplots()
        ax.imshow(img, extent=[3.1, 7.5, 50.6, 53.7])
        counter = 0
        legendnumber = []

        # Retrieve coordinates of stations in the trajects
        for value in traject.items():
            x_coor = []
            y_coor = []

            for stations in value[1][0]:
                x_coor.append(self.stations[stations][0])
                y_coor.append(self.stations[stations][1])

            ax.plot(x_coor, y_coor, color=colors[counter], linestyle='dashed', marker='o', markersize=3)
            counter += 1
            legendnumber.append(counter) 

        plt.title('Lijnvoering Noord- en Zuid-Holland')
        ax.legend(legendnumber, loc="best")
        plt.show()


if __name__ == "__main__":
    routes = Routes()
    routes.randomsolution() 