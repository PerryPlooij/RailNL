import csv

class Load():
    def __init__(self, connection_file, station_file):
        self.connections = self.load_connections(connection_file)
        self.stations = self.load_stations(station_file)

    def load_connections(self, file):
        """ Import all connections of the stations """

        connections = {}
        startstation = []
        connection = 0

        with open(file, 'rt') as csv_file:
            reader = csv.reader(csv_file, delimiter = ',')

            for row in reader: 
                connection += 1
                if row[0] not in connections:
                    connections[row[0]] = {} 
                connections[row[0]][row[1]] = row[2]

                if row[1] not in connections:
                    connections[row[1]] = {}
                connections[row[1]][row[0]] = row[2]

        # Add startstations to a seperate list
        for key, value in connections.items():
            if len(value) == 1:
                startstation.append(key)

        return connections, connection, startstation

    def load_stations(self, file):
        """ Import all stations """

        stations = {}

        with open(file, 'rt') as csv_file:
            reader = csv.reader(csv_file, delimiter=',')
            stations = {}

            for row in reader:
                stations[row[0]] = (float(row[2]),float(row[1]))

        return stations