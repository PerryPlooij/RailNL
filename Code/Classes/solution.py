import csv
import time

from datetime import datetime
from time import gmtime, strftime

import matplotlib.pyplot as plt


def visualisation(traject, all_stations):
    """ 
        Make a visualisation of the best train lining system based on the coordinates of the stations and the trajects. 
    """

    colors = ["green", "red", "aqua", "orange", "yellow", "lawngreen", "deepskyblue", "violet", "pink", "deeppink", "darkviolet", "grey", "salmon", "gold", "mediumseagreen", "mediumturquoise", "darkkhaki", "chocolate", "silver", "navy"]
    img = plt.imread("doc/map.png")
    fix, ax = plt.subplots()
    ax.imshow(img, extent=[3.1, 7.5, 50.6, 53.7])
    counter = 0
    legendnumber = []

    # Retrieve coordinates of stations in the trajects
    for value in traject.items():
        x_coor = []
        y_coor = []
        
        for stations in value[1][0]:
            x_coor.append(all_stations[stations][0])
            y_coor.append(all_stations[stations][1])

        ax.plot(x_coor, y_coor, color=colors[counter], linestyle='dashed', marker='o', markersize=3)
        counter += 1
        legendnumber.append(counter) 

    plt.title('Train lining system')
    ax.legend(legendnumber, loc="best")
    plt.show()

def export(file, traject, quality):
    """ 
        Export the traject with the highest quality to a csv-file associated with the heuristic performed.  
    """
    
    date_now = datetime.now()
    date = date_now.strftime("%Y-%m-%d %H:%M:%S")

    with open(file, "a", newline="") as csv_write:
        writer = csv.writer(csv_write)
        writer.writerow([date])

        for key, value in traject.items():
            writer.writerow([key, value])
            
        writer.writerow([quality])
        writer.writerow([])