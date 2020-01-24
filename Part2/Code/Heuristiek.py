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
        with open('../Bijlage/ConnectiesNationaal.csv', 'rt') as csv_file:
            reader = csv.reader(csv_file, delimiter=',')
            
            for row in reader: 
                self.connection += 1
                if row[0] not in self.connections:
                    self.connections[row[0]] = {}
                self.connections[row[0]][row[1]] = int(float(row[2]))

                if row[1] not in self.connections:
                    self.connections[row[1]] = {}
                self.connections[row[1]][row[0]] = int(float(row[2]))

        # Import all stations 
        with open('../Bijlage/StationsNationaal.csv', 'rt') as csv_file:
            reader = csv.reader(csv_file, delimiter=',')
            self.stations = {}

            for row in reader:
                if row[0] not in self.stations:
                    self.stations[row[0]] = (float(row[2]),float(row[1]))


    def randomsolution(self):
        """ Create random solution and check if a new solution is better than the previous solution  """

        randomcount = 0
        bestquality = 0
        besttime = 0
        besttraject = None
        t_end = time.time() + 60 * 30
        self.best_fifty = []
        #while time.time() < t_end:
        while randomcount < 50:
            maxtime = 180
            while maxtime <= 180:
                count = 1
                self.trajects = {}

                # Deepcopy allconnections to make sure all connections are available by making new trajects
                self.allconnections = copy.deepcopy(self.connections)
                self.allconnections2 = copy.deepcopy(self.connections)
                # Deepcopy the total amount of connections (connectioncopy) to reduce the amount (connection)
                # when making a new connection
                self.connectioncopy = copy.deepcopy(self.connection)
                
                # Make a maximum of 20 traject or when all connections are used with a random station as startstation
                while len(self.allconnections.keys()) != 0 and count <= 20:
                    city = random.choice(list(self.allconnections.keys()))
                    self.maketraject(city, count, 20, maxtime, self.allconnections, self.allconnections2)
                    count += 1

                # Check if the new quality is higher than the previous quality
                quality = self.quality()
                #if quality > bestquality:
                    #bestquality = quality
                    #besttraject = self.trajects
                    #besttime = maxtime
                self.best_fifty.append((self.trajects, quality))

                maxtime += 1
            randomcount += 1
        
        
        
        #print(self.best_fifty)
        #print(besttraject)
        #print(bestquality)
        #self.visualisation(besttraject)

    def maketraject(self, city, count, maxcount, maxtime, lijst1, lijst2):
        """ Making a new traject with the given maxtime """
        
        endtime = 0
        time = 0
        traject = []
        traject.append(city)
        
        #print(type(lijst2))
        # Check if a new city can be added to the traject
        while time < maxtime and count <= maxcount and city in lijst1:
            best_stop_time = 100
            best_stop_city = ""

            # Search for a new station in the cityconnections
            for i in range(len(lijst1[city])):
                if city in lijst2:
                    connection = random.choice(list(lijst2[city]))
                    time_traject = int(lijst2[city][connection])
                else:
                    connection = random.choice(list(lijst1[city]))
                    time_traject = int(lijst1[city][connection])

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
                
                if city in lijst2 and connection in lijst2[city]:
                    del lijst2[city][connection]
                    del lijst2[connection][city]
                    
                    self.connectioncopy = self.connectioncopy - 1
                else:
                    del lijst1[city][connection]
                    del lijst1[connection][city]

                if city in lijst2 and len(lijst2[city]) == 0:
                    del lijst2[city]

                if connection in lijst2 and len(lijst2[connection]) == 0:
                    del lijst2[connection]

                if len(lijst1[city]) == 0:
                    del lijst1[city]

                if len(lijst1[connection]) == 0:
                    del lijst1[connection]

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
        


    def heuristiek(self):
        self.best_fifty.sort(key = lambda x: x[1])
        self.best_fifty.reverse()
        self.best_one = self.best_fifty[:1]

        #print(self.best_one)
        for items in self.best_fifty:
            print(items[1])

        

        first_5 = {key: value for key, value in list(self.best_one[0][0].items())[:5]}
        last_20 = {key: value for key, value in list(self.best_one[0][0].items())[5:]}
        
        stations = set()
        for key, value in last_20.items():
            for item in value[0]:
                stations.add(item)

        
        connections = {}
        for city in stations:
            if city not in connections.keys():
                connections[city] = self.connections[city]
           
        
        unused = set()
        for connection in connections.values():
            for plaats in connection:
                if plaats not in connections.keys():
                    unused.add(plaats)

        dict2 = {}
        for place in unused:
            dict1 = {}
            for key, value in connections.items():
                for city in value:
                    if city == place:
                        time = connections[key][city]
                        dict1[key] = time
                        dict2[place] = dict1

                    
        connections.update(dict2)
        connections2 = copy.deepcopy(connections)
        
        
        maxtime = 180
        while maxtime <= 180:
            count = 6
            self.trajects = {}
            while len(connections2.keys()) != 0 and count <= 20:
                city = random.choice(list(connections2.keys()))
                self.maketraject(city, count, 15,  maxtime, connections, connections2)
                count += 1
            
            maxtime += 1
        
        print(self.trajects)

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

        colors = ["green", "red", "aqua", "orange", "yellow", "lawngreen", "deepskyblue", "violet", "pink", "deeppink", "darkviolet", "grey", "salmon", "gold", "mediumseagreen", "mediumturquoise", "darkkhaki", "lightgoldenrodyellow", "silver", "navy"]
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

        plt.title('Lijnvoering Nederland')
        ax.legend(legendnumber, loc="best")
        plt.show()

    
if __name__ == "__main__":
    routes = Routes()
    routes.randomsolution()
    routes.heuristiek()