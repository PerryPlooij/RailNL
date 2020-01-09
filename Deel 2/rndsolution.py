import csv
import random
import matplotlib.pyplot as plt

class Routes():
    def __init__(self):
        self.connections = {}
        self.total = []

        with open('Bijlage/ConnectiesNationaal.csv', 'rt') as csv_file:
            reader = csv.reader(csv_file, delimiter=',')
            for row in reader: 
                if row[0] not in self.connections:
                    self.connections[row[0]] = {}
                    self.total.append(row[0])
                self.connections[row[0]][row[1]] = int(float(row[2]))

                if row[1] not in self.connections:
                    self.connections[row[1]] = {}
                    self.total.append(row[1])
                self.connections[row[1]][row[0]] = int(float(row[2]))


    def randomsolution(self):
        randomcount = 0
        bestquality = 0
        besttime = 0
        besttraject = None

        while randomcount <= 10000:
            maxtime = 0
            while maxtime <= 180:
                count = 1
                self.trajects = {}
                self.stations = self.total.copy()
                while len(self.stations) != 0 and count <= 20:
                    city = random.choice(self.stations)
                    self.maketraject(city, count, maxtime)
                    count += 1

                if self.quality() > bestquality:
                    bestquality = self.quality()
                    besttraject = self.trajects
                    besttime = maxtime
                maxtime += 1

            randomcount += 1
            # print(self.trajects)
            # print(self.quality())
        print(besttime)
        print(besttraject)
        print(bestquality)


    def maketraject(self, city, count, maxtime):
        endtime = 0
        time = 0
        traject = []

        traject.append(city)
        self.stations.remove(city)

        while time < maxtime and count <= 20:
            best_stop_time = 100
            best_stop_city = ""
            add = False

            while add == False:
                aantal = 0
                connection = random.choice(list(self.connections[city]))
                time_traject = int(self.connections[city][connection])

                for items in self.connections[city]:
                    if items not in self.stations:
                        aantal += 1
                
                if aantal != len(self.connections[city]):
                    if connection in self.stations and time + time_traject <= maxtime:
                        add = True
                        best_stop_time = time_traject
                        best_stop_city = connection
                    elif time + time_traject > maxtime:
                        add = True
                else:
                    add = True

            if best_stop_city != '':
                time += best_stop_time
                endtime = time
                city = best_stop_city
                traject.append(city)
                self.stations.remove(city)
            else:
                endtime = time
                time = maxtime

            if len(traject) == 1:
                connections = self.connections[traject[0]]
                endcity = min(connections, key=lambda k: connections[k])
                endtime = int(connections[endcity])
                traject.append(endcity)

        self.trajects[count] = (traject, endtime)
        return self.trajects
    

    def quality(self):
        minutes = 0
        p = 1 - len(self.stations) / 22
        T = len(self.trajects)

        for key, value in self.trajects.items():
            minutes += value[1]

        K = p * 10000 - (T * 100 + minutes)
        return K

    
if __name__ == "__main__":
    routes = Routes()
    routes.randomsolution()