import csv

class Routes():
    def __init__(self):
        self.connections = {}
        self.trajects = {}
        self.start_end = []
        self.stations = []

        with open('Bijlage/ConnectiesHolland.csv', 'rt') as csv_file:
            reader = csv.reader(csv_file, delimiter=',')
            for row in reader: 
                if row[0] not in self.connections:
                    self.connections[row[0]] = {}
                    self.stations.append(row[0])
                self.connections[row[0]][row[1]] = row[2]

                if row[1] not in self.connections:
                    self.connections[row[1]] = {}
                    self.stations.append(row[1])
                self.connections[row[1]][row[0]] = row[2]

            for key, value in self.connections.items():
                if len(value) == 1:
                    self.start_end.append(key)


    def startsolution(self):
        count = 1

        # Startroutes
        for city in self.start_end:
            self.maketraject(city, count)
            count += 1

        # Overige routes
        while len(self.stations) != 0:
            for city in self.stations:
                self.maketraject(city, count)
                count += 1

        self.quality()

    def maketraject(self, city, count):
        endtime = 0
        time = 0
        traject = []
        traject.append(city)
        self.stations.remove(city)

        while time < 120:
            best_stop_time = 100
            best_stop_city = ""
            for connection in self.connections[city]:
                time_traject = int(self.connections[city][connection])

                if time_traject < best_stop_time and connection in self.stations and time + time_traject <= 120:
                    best_stop_time = time_traject
                    best_stop_city = connection
            
            if best_stop_city != '':
                time += best_stop_time
                endtime = time
                city = best_stop_city
                traject.append(city)
                self.stations.remove(city)
            else:
                endtime = time
                time = 120

            if len(traject) == 1:
                connections = self.connections[traject[0]]
                endcity = min(connections, key=lambda k: connections[k])
                endtime = int(connections[endcity])
                traject.append(endcity)

        self.trajects[count] = (traject, endtime)


    def quality(self):
        minutes = 0
        p = 1 - len(self.stations) / 22
        T = len(self.trajects)

        for key, value in self.trajects.items():
            minutes += value[1]

        K = p * 10000 - (T * 100 + minutes)
        print(K)


if __name__ == "__main__": 
    Routes()
    Routes().startsolution()
