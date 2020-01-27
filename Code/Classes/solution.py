# ******************************************************************************************************
# * solution.py
# *
# * PGT Party
# *
# * 
# ******************************************************************************************************



import csv
import time

from datetime import datetime
from time import gmtime, strftime

import matplotlib.pyplot as plt

class Solution():
    def __init__(self, traject, quality, stations):
        self.traject = traject
        self.quality = quality
        self.stations = stations

    def visualisation(self):
        """ Make a visualisation of the best timetable """

        colors = ["green", "red", "aqua", "orange", "yellow", "lawngreen", "deepskyblue", "violet", "pink", "deeppink", "darkviolet", "grey", "salmon", "gold", "mediumseagreen", "mediumturquoise", "darkkhaki", "chocolate", "silver", "navy"]
        img = plt.imread("doc/map.png")
        fix, ax = plt.subplots()
        ax.imshow(img, extent=[3.1, 7.5, 50.6, 53.7])
        counter = 0
        legendnumber = []
    
        # Retrieve coordinates of stations in the trajects
        for value in self.traject.items():
            x_coor = []
            y_coor = []
            
            for stations in value[1][0]:
                x_coor.append(self.stations[stations][0])
                y_coor.append(self.stations[stations][1])

            ax.plot(x_coor, y_coor, color=colors[counter], linestyle='dashed', marker='o', markersize=3)
            counter += 1
            legendnumber.append(counter) 

        plt.title('Lijnvoering Noord- en Zuid-Holland')
        ax.legend(legendnumber, loc="best")
        plt.show()

    def export(self, file):
        """ Export besttraject and bestquality to a csv-file """
        
        date_now = datetime.now()
        date = date_now.strftime("%Y-%m-%d %H:%M:%S")

        with open(file, "a", newline="") as csv_write:
            writer = csv.writer(csv_write)
            writer.writerow([date])

            for key, value in self.traject.items():
                writer.writerow([key, value])
                
            writer.writerow([self.quality])
            writer.writerow([])