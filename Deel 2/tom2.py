# *************************************************************************************************
# * code.py (deel 1)
# *
# * PGT Party
# *
# * Random startoplossing.
# *************************************************************************************************


import copy
import csv
import random
import time

import matplotlib.pyplot as plt

#from coordinates import Stations


class Routes():
    def __init__(self):
        self.connections = {}
        self.verbinding = 0

        with open('Bijlage/ConnectiesNationaal.csv', 'rt') as csv_file:
            reader = csv.reader(csv_file, delimiter=',')
            for row in reader: 
                self.verbinding += 1
                if row[0] not in self.connections:
                    self.connections[row[0]] = {}
                self.connections[row[0]][row[1]] = int(float(row[2]))

                if row[1] not in self.connections:
                    self.connections[row[1]] = {}
                self.connections[row[1]][row[0]] = int(float(row[2]))

        with open('Bijlage/StationsNationaal.csv', 'rt') as csv_file:
            reader = csv.reader(csv_file, delimiter=',')
            self.stations = {}

            for row in reader:
                if row[0] not in self.stations:
                    self.stations[row[0]] = (float(row[2]),float(row[1]))


    def randomsolution(self):
        randomcount = 0
        bestquality = 0
        besttime = 0
        besttraject = None
        t_end = time.time() + 60 * 30

        # while time.time() < t_end:
        while randomcount < 500:
            maxtime = 170
            while maxtime <= 180:
                count = 1
                self.trajects = {}
                self.allconnections = copy.deepcopy(self.connections)
                self.allconnections2 = copy.deepcopy(self.connections)
                self.verbindingcopy = copy.deepcopy(self.verbinding)
                while len(self.allconnections2.keys()) != 0 and count <= 20:
                    city = random.choice(list(self.allconnections2.keys()))
                    self.maketraject(city, count, maxtime)
                    count += 1
                
                best = self.quality()
                self.improve(best)

                if self.quality() > bestquality:
                    bestquality = self.quality()
                    besttraject = self.trajects
                    besttime = maxtime
                maxtime += 1

            randomcount += 1

        print(besttraject)
        print(bestquality)
        self.visualisation(besttraject)

    def maketraject(self, city, count, maxtime):
        endtime = 0
        time = 0
        traject = []

        traject.append(city)
        
        while time < maxtime and count <= 20 and city in self.allconnections:
            best_stop_time = 100
            best_stop_city = ""
            add = False

            for i in range(len(self.allconnections[city])):
                aantal = 0
                if city in self.allconnections2:
                    connection = random.choice(list(self.allconnections2[city]))
                    time_traject = int(self.allconnections2[city][connection])
                else:
                    connection = random.choice(list(self.allconnections[city]))
                    time_traject = int(self.allconnections[city][connection])

                if time + time_traject <= maxtime:
                    best_stop_time = time_traject
                    best_stop_city = connection
                    break
        
            if best_stop_city != '':
                time += best_stop_time
                endtime = time
                if city in self.allconnections2 and connection in self.allconnections2[city]:
                    del self.allconnections2[city][connection]
                    del self.allconnections2[connection][city]
                    self.verbindingcopy = self.verbindingcopy - 1
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
            
            if len(traject) == 1:
                connections = self.connections[traject[0]]
                endcity = min(connections, key=lambda k: connections[k])
                endtime = int(connections[endcity])
                traject.append(endcity)

        self.trajects[count] = (traject, endtime)


    def improve(self, best):
        run = True
        while run:
            for key1, value1 in self.trajects.items():
                if len(value1[0]) >= 2:
                    beginbegin = value1[0][0]
                    begineind = value1[0][1]
                    for key2, value2 in self.trajects.items():
                        for i in range(1, len(value2[0]) - 1):
                            if value2[0][i] == beginbegin and value2[0][i + 1] == begineind:
                                time = self.trajects[key1][1]
                                newtime = time - self.connections[beginbegin][begineind]
                                del self.trajects[key1][0][0]
                                listtraject = list(self.trajects[key1])
                                listtraject[len(listtraject) - 1] = newtime
                                self.trajects[key1] = tuple(listtraject)
                                break
                            elif value2[0][i] == begineind and value2[0][i + 1] == beginbegin:
                                time = self.trajects[key1][1]
                                newtime = time - self.connections[begineind][beginbegin]
                                del self.trajects[key1][0][0]
                                listtraject = list(self.trajects[key1])
                                listtraject[len(listtraject) - 1] = newtime
                                self.trajects[key1] = tuple(listtraject)
                                break

                if len(value1[0]) >= 2:
                    eindbegin = value1[0][-2]
                    eindeind = value1[0][-1]
                    for key2, value2 in self.trajects.items():
                        for i in range(len(value2[0]) - 2):
                            if value2[0][i] == eindbegin and value2[0][i + 1] == eindeind:
                                newtime = self.trajects[key1][1] - self.connections[eindbegin][eindeind]
                                del self.trajects[key1][0][-1]
                                listtraject = list(self.trajects[key1])
                                listtraject[len(listtraject) - 1] = newtime
                                self.trajects[key1] = tuple(listtraject)
                                break
                            elif value2[0][i] == eindeind and value2[0][i + 1] == eindbegin:
                                time = self.trajects[key1][1]
                                newtime = time - self.connections[eindeind][eindbegin]
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

    def quality(self):
        minutes = 0
        p = 1 - self.verbindingcopy / self.verbinding
        T = len(self.trajects)

        for key, value in self.trajects.items():
            minutes += value[1]

        K = p * 10000 - (T * 100 + minutes)
        return K

    def visualisation(self, traject):
        colors = ["green", "red", "aqua", "orange", "yellow", "lawngreen", "deepskyblue", "violet", "pink", "deeppink", "darkviolet", "grey", "salmon", "gold", "mediumseagreen", "mediumturquoise", "darkkhaki", "lightgoldenrodyellow", "silver", "navy"]
        img = plt.imread("../doc/kaart.png")
        fix, ax = plt.subplots()
        ax.imshow(img, extent=[3.1, 7.5, 50.6, 53.7])
        counter = 0
        legenda = []

        for value in traject.items():
            x_coor = []
            y_coor = []
            for stations in value[1][0]:
                x_coor.append(self.stations[stations][0])
                y_coor.append(self.stations[stations][1])

            ax.plot(x_coor, y_coor, color=colors[counter], linestyle='dashed', marker='o', markersize=3)
            counter += 1
            legenda.append(counter) 

        # for value in traject.items():
        #     for stations in value[1][0]:
        #         plt.annotate(stations, (self.stations[stations][0], self.stations[stations][1]), fontsize=6)

        plt.title('Lijnvoering NL')
        ax.legend(legenda, loc="best")
        plt.show()


    
if __name__ == "__main__":
    routes = Routes()
    routes.randomsolution()