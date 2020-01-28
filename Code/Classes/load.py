import csv


class Load():
    """ 
        This class contains a function to import all connections of the station to a dictionary and a function to 
        import all stations with the corresponding coordinates. 
    """

    def __init__(self, connection_file, station_file):
        self.connections = self.load_connections(connection_file)
        self.stations = self.load_stations(station_file)

    def load_connections(self, file):
        """ 
            Import all connections of the stations with the corresponding duration to a dictionary called 'connections'.
            The variable 'startstations' is a list containing all stations with one connection to another station. 
            The total number of connections is stored in the variable 'connection_total'. This variable is used to 
            calculate the fraction of connections used in a train lining system in relation to the total number of 
            connections.
        """

        connections = {}
        startstation = []
        connection_total = 0

        with open(file, 'rt') as csv_file:
            reader = csv.reader(csv_file, delimiter = ',')

            for row in reader:
                connection_total += 1
                if row[0] not in connections:
                    connections[row[0]] = {} 
                connections[row[0]][row[1]] = int(float(row[2]))

                if row[1] not in connections:
                    connections[row[1]] = {}
                connections[row[1]][row[0]] = int(float(row[2]))

        for key, value in connections.items():
            if len(value) == 1:
                startstation.append(key)

        return connections, connection_total, startstation

    def load_stations(self, file):
        """ 
            Import all stations to a dictionary with the corresponding coordinates. This dictionary can be used to 
            create the visualisation of a train lining system.
        """

        stations = {}

        with open(file, 'rt') as csv_file:
            reader = csv.reader(csv_file, delimiter=',')
            stations = {}

            for row in reader:
                stations[row[0]] = (float(row[2]),float(row[1]))

        return stations