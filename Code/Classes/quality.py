# ******************************************************************************************************
# * quality.py
# *
# * PGT Party
# *
# * Calculate the quality of a train lining system based on the fraction connections used relative
# * to the total amount of connections, the amount of trajects and the total time of the lining system. 
# ******************************************************************************************************


class Quality():
    def __init__(self, connections, connection_total, trajects):
        self.connections = connections
        self.connection_total = connection_total
        self.trajects = trajects

        self.quality = self.calculate_quality()

    def calculate_quality(self):
        """ Calculate quality of the created train lining system """

        minutes = 0
        p = 1 - self.connections / self.connection_total
        T = len(self.trajects)

        for key, value in self.trajects.items():
            minutes += value[1]

        K = p * 10000 - (T * 100 + minutes)
        return K