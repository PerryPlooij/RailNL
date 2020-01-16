import copy
import csv
import random
import time

import matplotlib.pyplot as plt

class Test():
    def vis(self):
        self.connections = {}
        self.verbinding = 0

        with open('Bijlage/ConnectiesNationaal.csv', 'rt') as csv_file:
            reader = csv.reader(csv_file, delimiter=',')
            for row in reader: 
                self.verbinding += 1
                if row[0] not in self.connections:
                    self.connections[row[0]] = {}
                self.connections[row[0]][row[1]] = int(float(row[2]))

                if row[1] not in self.connections:
                    self.connections[row[1]] = {}
                self.connections[row[1]][row[0]] = int(float(row[2]))

        with open('Bijlage/StationsNationaal.csv', 'rt') as csv_file:
            reader = csv.reader(csv_file, delimiter=',')
            self.stations = {}

            for row in reader:
                if row[0] not in self.stations:
                    self.stations[row[0]] = (float(row[2]),float(row[1]))

        traject = {1: (['Rotterdam Blaak', 'Rotterdam Alexander', 'Gouda', 'Den Haag Centraal', 'Leiden Centraal', 'Heemstede-Aerdenhout', 'Haarlem', 'Amsterdam Sloterdijk', 'Amsterdam Zuid', 'Schiphol Airport', 'Utrecht Centraal', 'Ede-Wageningen', 'Arnhem Centraal'], 168), 2: (['Den Haag Laan v NOI', 'Gouda', 'Alphen a/d Rijn', 'Leiden Centraal', 'Den Haag HS', 'Delft', 'Schiedam Centrum', 'Rotterdam Centraal', 'Dordrecht', 'Breda', 'Tilburg', 's-Hertogenbosch', 'Oss'], 167), 3: (['Rotterdam Alexander', 'Rotterdam Centraal', 'Dordrecht', 'Roosendaal', 'Vlissingen'], 110), 4: (['Dieren', 'Zutphen', 'Deventer', 'Almelo', 'Hengelo', 'Enschede', 'Hengelo', 'Almelo', 'Zwolle', 'Assen'], 160), 5: (['Roosendaal', 'Etten-Leur', 'Breda', 'Tilburg', 'Eindhoven', 'Weert', 'Roermond', 'Sittard', 'Heerlen', 'Sittard', 'Maastricht', 'Sittard'], 158), 6: (['Schiphol Airport', 'Leiden Centraal', 'Den Haag Laan v NOI', 'Delft', 'Den Haag Centraal', 'Leiden Centraal', 'Alphen a/d Rijn', 'Utrecht Centraal', 'Amersfoort', 'Zwolle'], 152), 7: (['Dordrecht', 'Rotterdam Blaak', 'Schiedam Centrum', 'Rotterdam Blaak', 'Rotterdam Alexander', 'Gouda', 'Den Haag HS', 'Gouda', 'Utrecht Centraal', 'Amsterdam Amstel', 'Almere Centrum'], 161), 8: (['Den Helder', 'Alkmaar', 'Castricum', 'Zaandam', 'Amsterdam Sloterdijk', 'Amsterdam Centraal', 'Almere Centrum', 'Lelystad Centrum', 'Almere Centrum', 'Hilversum', 'Utrecht Centraal'], 158), 9: (['Haarlem', 'Beverwijk', 'Zaandam', 'Hoorn', 'Alkmaar', 'Castricum', 'Beverwijk', 'Haarlem', 'Amsterdam Sloterdijk', 'Zaandam', 'Castricum'], 158), 10: (['Amsterdam Zuid', 'Amsterdam Amstel', 'Amsterdam Centraal', 'Utrecht Centraal', 's-Hertogenbosch', 'Eindhoven', 'Helmond', 'Venlo', 'Helmond', 'Eindhoven'], 168), 11: (['Assen', 'Groningen', 'Leeuwarden', 'Heerenveen', 'Steenwijk', 'Zwolle', 'Deventer', 'Apeldoorn', 'Amersfoort'], 164), 12: (['Oss', 'Nijmegen', 'Arnhem Centraal', 'Dieren', 'Zutphen', 'Apeldoorn', 'Amersfoort', 'Utrecht Centraal', 'Amsterdam Amstel', 'Hilversum', 'Utrecht Centraal'], 168)}
        print(traject)
        print("")

        best = 6908
        run = True
        while run:
            for key1, value1 in traject.items():
                beginbegin = value1[0][0]
                begineind = value1[0][1]
                for key2, value2 in traject.items():
                    for i in range(1, len(value2[0]) - 1):
                        if value2[0][i] == beginbegin and value2[0][i + 1] == begineind:
                            time = traject[key1][1]
                            newtime = time - self.connections[beginbegin][begineind]
                            del traject[key1][0][0]
                            listtraject = list(traject[key1])
                            listtraject[len(listtraject) - 1] = newtime
                            traject[key1] = tuple(listtraject)
                        elif value2[0][i] == begineind and value2[0][i + 1] == beginbegin:
                            time = traject[key1][1]
                            newtime = time - self.connections[begineind][beginbegin]
                            del traject[key1][0][0]
                            listtraject = list(traject[key1])
                            listtraject[len(listtraject) - 1] = newtime
                            traject[key1] = tuple(listtraject)

                eindbegin = value1[0][-2]
                eindeind = value1[0][-1]
                for key2, value2 in traject.items():
                    for i in range(len(value2[0]) - 2):
                        if value2[0][i] == eindbegin and value2[0][i + 1] == eindeind:
                            newtime = traject[key1][1] - self.connections[eindbegin][eindeind]
                            del traject[key1][0][-1]
                            listtraject = list(traject[key1])
                            listtraject[len(listtraject) - 1] = newtime
                            traject[key1] = tuple(listtraject)
                        elif value2[0][i] == eindeind and value2[0][i + 1] == eindbegin:
                            time = traject[key1][1]
                            newtime = time - self.connections[eindeind][eindbegin]
                            del traject[key1][0][-1]
                            listtraject = list(traject[key1])
                            listtraject[len(listtraject) - 1] = newtime
                            traject[key1] = tuple(listtraject)
                            
            print(traject)
            new = self.quality(traject)
            print(new)
            if new == best:
                run = False
            else:
                best = new
        self.visualisation(traject)           

    def quality(self, traject):
        self.minutes = 0
        self.p = 1
        self.T = len(traject)

        for key, value in traject.items():
            self.minutes += value[1]

        K = self.p * 10000 - (self.T * 100 + self.minutes)
        return K
   

    def visualisation(self, traject):
        colors = ["green", "red", "aqua", "orange", "yellow", "lawngreen", "deepskyblue", "violet", "pink", "deeppink", "darkviolet", "grey", "salmon", "gold", "mediumseagreen", "mediumturquoise", "darkkhaki", "lightgoldenrodyellow", "silver", "navy"]
        img = plt.imread("../doc/kaart.png")
        fix, ax = plt.subplots()
        ax.imshow(img, extent=[3.1, 7.5, 50.6, 53.7])
        counter = 0
        legenda = []

        for value in traject.items():
            x_coor = []
            y_coor = []
            for stations in value[1][0]:
                x_coor.append(self.stations[stations][0])
                y_coor.append(self.stations[stations][1])

            ax.plot(x_coor, y_coor, color=colors[counter], linestyle='dashed', marker='o', markersize=3)
            counter += 1
            legenda.append(counter) 

        plt.title('Lijnvoering NL')
        ax.legend(legenda, loc="best")
        plt.show()

if __name__ == "__main__":
    Test().vis()