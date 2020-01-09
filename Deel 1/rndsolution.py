import csv
import random
import matplotlib.pyplot as plt

class Routes():
    def __init__(self):
        self.connections = {}
        self.total = []

        with open('Bijlage/ConnectiesHolland.csv', 'rt') as csv_file:
            reader = csv.reader(csv_file, delimiter=',')
            for row in reader: 
                if row[0] not in self.connections:
                    self.connections[row[0]] = {}
                    self.total.append(row[0])
                self.connections[row[0]][row[1]] = row[2]

                if row[1] not in self.connections:
                    self.connections[row[1]] = {}
                    self.total.append(row[1])
                self.connections[row[1]][row[0]] = row[2]


    def randomsolution(self):
        self.stations = self.total.copy()
        print(random.choice(self.stations))
        
    
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