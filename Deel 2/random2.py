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
            #print(self.stations)


    def randomsolution(self):
        randomcount = 0
        bestquality = 0
        besttime = 0
        besttraject = None
        # t_end = time.time() + 60 * 30

        # while time.time() < t_end:
        while randomcount < 1:
            maxtime = 0
            while maxtime <= 180:
                count = 1
                self.trajects = {}
                self.allconnections = copy.deepcopy(self.connections)
                self.verbindingcopy = copy.deepcopy(self.verbinding)
                while len(self.allconnections.keys()) != 0 and count <= 20:
                    city = random.choice(list(self.allconnections.keys()))
                    self.maketraject(city, count, maxtime)
                    count += 1

                if self.quality() > bestquality:
                    bestquality = self.quality()
                    besttraject = self.trajects
                    besttime = maxtime
                maxtime += 1

            randomcount += 1

        # print(besttraject)
        #print(bestquality)
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
                connection = random.choice(list(self.allconnections[city]))
                time_traject = int(self.allconnections[city][connection])

                if time + time_traject <= maxtime:
                    best_stop_time = time_traject
                    best_stop_city = connection
                    break
        
            if best_stop_city != '':
                time += best_stop_time
                endtime = time
                del self.allconnections[city][connection]
                del self.allconnections[connection][city]
                self.verbindingcopy = self.verbindingcopy - 1

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
        counter = 0
        perrys = []
        img = plt.imread("../doc/kaart.png")
        fix, ax = plt.subplots()
        ax.imshow(img, extent=[3.1, 7.3, 50.1, 53.9])
        print(traject)
        for value in traject.items():
            perry = "traject"
            x_coor = []
            y_coor = []
            #print(value[1][0])
            for stations in value[1][0]:
                #print(self.stations[stations])
                x_coor.append(self.stations[stations][0])
                y_coor.append(self.stations[stations][1])
            
            ax.plot(x_coor, y_coor, color=colors[counter], linestyle='dashed', marker='o' )
            
            perrys.append(counter)
            counter += 1 

        for value in traject.items():
            for stations in value[1][0]:
                plt.annotate(stations, (self.stations[stations][0], self.stations[stations][1]), fontsize=6)
        
        
        #ax.title('Lijnvoering NL')
        
        #ax.legend(perrys, loc='best')
        plt.show()


    
if __name__ == "__main__":
    routes = Routes()
    routes.randomsolution()