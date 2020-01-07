import csv


class Routes(): 
    def __init__(self):
        self.connections = {}
        self.start_end = []
        self.trajects = {}

        with open('BIjlage/ConnectiesHolland.csv', 'rt') as csv_file:
            reader = csv.reader(csv_file, delimiter=',')
            for row in reader: 
                if row[0] not in self.connections:
                    self.connections[row[0]] = {}
                self.connections[row[0]][row[1]] = row[2]

                if row[1] not in self.connections:
                    self.connections[row[1]] = {}
                self.connections[row[1]][row[0]] = row[2]

            for key, value in self.connections.items():
                if len(value) == 1:
                    self.start_end.append(key)

    def code(self):
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
                city = best_stop_city
                traject.append(city)

            self.trajects[count] = traject
            count += 1
            
        print(self.trajects)

if __name__ == "__main__": 
    Routes().code()
