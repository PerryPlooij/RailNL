import copy
import csv
import random
import time

import matplotlib.pyplot as plt


class Routes():
    def __init__(self):
        self.connections = {}
        self.verbinding = 0

        with open('Bijlage/ConnectiesHolland.csv', 'rt') as csv_file:
            reader = csv.reader(csv_file, delimiter=',')
            for row in reader: 
                self.verbinding += 1
                if row[0] not in self.connections:
                    self.connections[row[0]] = {}
                self.connections[row[0]][row[1]] = row[2]

                if row[1] not in self.connections:
                    self.connections[row[1]] = {}
                self.connections[row[1]][row[0]] = row[2]
        
        with open('Bijlage/StationsNationaal.csv', 'rt') as csv_file:
            reader = csv.reader(csv_file, delimiter=',')
            self.stations = {}

            for row in reader:
                if row[0] not in self.stations:
                    self.stations[row[0]] = (float(row[2]),float(row[1]))
            #print(self.stations)


    def heuristiek(self):
        randomcount = 0
        bestquality = 0
        besttime = 0
        besttraject = None
        t_end = time.time() + 60 * 0.5

        #while time.time() < t_end:
        while randomcount < 10:
            maxtime = 0
            while maxtime <= 120:
                count = 1
                self.trajects = {}
                #self.allconnections = copy.deepcopy(self.connections)
                #self.verbindingcopy = copy.deepcopy(self.verbinding)
                while len(self.connections.keys()) != 0 and count <= 7:
                    city = random.choice(list(self.connections.keys()))
                    self.maketraject(city, count, maxtime)
                    count += 1

                if self.quality() > bestquality:
                    bestquality = self.quality()
                    besttraject = self.trajects
                    besttime = maxtime
                maxtime += 1
            randomcount += 1

        #print(self.connections)
        print(besttraject)
        print(bestquality)
        #self.visualisation(besttraject)



    def maketraject(self, city, count, maxtime):
        endtime = 0
        time = 0
        traject = []

        traject.append(city)
        








    def quality(self):
        self.minutes = 0
        self.p = 1 - self.verbindingcopy / self.verbinding
        self.T = len(self.trajects)

        for key, value in self.trajects.items():
            self.minutes += value[1]

        #print(self.trajects)
        #print(self.p, self.T, self.minutes)
        K = self.p * 10000 - (self.T * 100 + self.minutes)
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
    routes.heuristiek()