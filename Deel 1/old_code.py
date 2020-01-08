import csv


class Routes(): 
    def __init__(self):
        self.connections = {}
        self.trajects = {}
        self.start_end = []
        self.stations = []

        with open('BIjlage/ConnectiesHolland.csv', 'rt') as csv_file:
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
        for city in self.start_end:
            time = 0
            traject = []
            traject.append(city)
            
            while time < 120:
                best_stop_time = 100
                best_stop_city = ""
                for connection in self.connections[city]:
                    time_traject = int(self.connections[city][connection])

                    if time_traject < best_stop_time and connection not in traject and time + time_traject <= 120:
                        best_stop_time = time_traject
                        best_stop_city = connection

                time += best_stop_time
                
                if best_stop_city != '':
                    city = best_stop_city
                    traject.append(city)

            self.trajects[count] = traject
            count += 1

        # Overige stations bepalen
        for station in self.connections:
            for key, value in self.trajects.items():
                if station in value and station in self.stations:
                    self.stations.remove(station)
        
        while len(self.stations) != 0:
            for city in self.stations:
                time = 0
                traject = []
                traject.append(city)
                
                while time < 120:
                    best_stop_time = 100
                    best_stop_city = ""
                    for connection in self.connections[city]:
                        time_traject = int(self.connections[city][connection])

                        if time_traject < best_stop_time and connection not in traject and time + time_traject <= 120:
                            best_stop_time = time_traject
                            best_stop_city = connection

                    time += best_stop_time
                    
                    if best_stop_city != '':
                        city = best_stop_city
                        traject.append(city)

                self.trajects[count] = traject
                count += 1

                for station in self.stations:
                    for key, value in self.trajects.items():
                        if station in value and station in self.stations:
                            self.stations.remove(station)


        print(self.trajects)

if __name__ == "__main__": 
    Routes().startsolution()
