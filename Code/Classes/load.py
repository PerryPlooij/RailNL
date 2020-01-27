# ************************************************************************************************
# * load.py
# *
# * PGT Party
# *
# * Import the connections and the stations to use in the heuristics.
# ************************************************************************************************


import csv


class Load():
    def __init__(self, connection_file, station_file, delete_station):
        self.connections = self.load_connections(connection_file, delete_station)
        self.stations = self.load_stations(station_file, delete_station)

    def load_connections(self, file, delete_station):
        """ Import all connections of the stations with the corresponding duration to a dictionary. """

        connections = {}
        startstation = []
        connection_total = 0

        with open(file, 'rt') as csv_file:
            reader = csv.reader(csv_file, delimiter = ',')

            for row in reader:
                if row[0] != delete_station and row[1] != delete_station: 
                    connection_total += 1
                    if row[0] not in connections:
                        connections[row[0]] = {} 
                    connections[row[0]][row[1]] = int(float(row[2]))

                    if row[1] not in connections:
                        connections[row[1]] = {}
                    connections[row[1]][row[0]] = int(float(row[2]))

        # Add startstations to a seperate list so those station can be used to create the first trajects
        for key, value in connections.items():
            if len(value) == 1:
                startstation.append(key)

        return connections, connection_total, startstation

    def load_stations(self, file, delete_station):
        """ Import all stations to a dictionary with the corresponding coordinates """

        stations = {}

        with open(file, 'rt') as csv_file:
            reader = csv.reader(csv_file, delimiter=',')
            stations = {}

            for row in reader:
                if row[0] != delete_station:
                    stations[row[0]] = (float(row[2]),float(row[1]))

        return stations