import csv


class Routes(): 
    def __init__(self):
        self.connections = {}
        self.start_end = []
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
        pass

if __name__ == "__main__": 
    Routes().code()
