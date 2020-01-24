# *******************************************************************************************
# * random_once1.py
# *
# * PGT Party
# *
# * Timetable with every connection once and the startstation and connection randomly chosen.
# *******************************************************************************************


import copy
import csv
import random
import time

from datetime import datetime
from time import strftime, gmtime

import matplotlib.pyplot as plt


class Routes():
    def __init__(self):
        self.connections = {}
        self.connection = 0
        self.startstation = []

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

        
        for key, value in self.connections.items():
            if len(value) == 1:
                self.startstation.append(key)

    def randomsolution(self):
        """ Create random solution and check if a new solution is better than the previous solution  """

        amount = 0
        randomcount = 0
        bestquality = 0
        besttime = 0
        besttraject = None
        t_end = time.time() + 60 * 5
        t_start = time.time()
        self.results = []

        # while time.time() < t_end:
        while randomcount < 1:
            maxtime = 100
            while maxtime <= 120: # and bestquality != 9219.0:
                amount += 1
                count = 1
                self.trajects = {}

                self.start = copy.deepcopy(self.startstation)

                # Deepcopy allconnections to make sure all connections are available by making new trajects
                self.allconnections = copy.deepcopy(self.connections)

                # Deepcopy the total amount of connections (connectioncopy) to reduce the amount (connection)
                # when making a new connection
                self.connectioncopy = copy.deepcopy(self.connection)

                # Make a maximum of 7 traject or when all connections are used with a random station as startstation
                while len(self.allconnections.keys()) != 0 and count <= 5:
                    if self.start: 
                        city = random.choice(self.start)
                        self.maketraject(city, count, maxtime)
                        self.start.remove(city)
                        count += 1
                    else:
                        city = random.choice(list(self.allconnections.keys()))
                        self.maketraject(city, count, maxtime)
                        count += 1

                # Check if the new quality is higher than the previous quality
                quality = self.quality()
                self.results.append(int(quality))
                if quality > bestquality:
                    bestquality = quality
                    besttraject = self.trajects
                    besttime = maxtime
                    tijd = time.time() - t_start
                    # print("tijd {}".format(tijd))
                    # print("herhalingen {}".format(amount))
                    # print("besttraject {}".format(besttraject))
                    # print("bestquality {}".format(bestquality))

                maxtime += 1

            randomcount += 1

        print(besttraject)
        print(bestquality)
        self.export(besttraject, bestquality)
        self.visualisation(besttraject)
    
    def hist(self):
        plt.hist(self.results, bins=15)
        plt.xlabel("Score")
        plt.ylabel("Count")
        plt.title("random_once1")
        plt.show


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
                if time + time_traject <= maxtime:
                    best_stop_time = time_traject
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


    def export(self, besttraject, bestquality):
        """ Export besttraject and bestquality to csv-file """
        
        csv_file = "../Solutions/random_once.csv"
        date_now = datetime.now()
        date = date_now.strftime("%Y-%m-%d %H:%M:%S")

        with open(csv_file, "a", newline="") as csv_write:
            writer = csv.writer(csv_write)
            writer.writerow([date])

            for key, value in besttraject.items():
                writer.writerow([key, value])
                
            writer.writerow([bestquality])
            writer.writerow([])


if __name__ == "__main__":
    routes = Routes()
    routes.randomsolution()