import copy
import csv
import random
import time

connections = {}
total_times = 1
total_plus = 0

# Statespace part 1
with open('Deel 1/Bijlage/ConnectiesHolland.csv', 'rt') as csv_file:
    reader = csv.reader(csv_file, delimiter=',')

    for row in reader: 
        if row[0] not in connections:
            connections[row[0]] = {} 
        connections[row[0]][row[1]] = row[2]

        if row[1] not in connections:
            connections[row[1]] = {}
        connections[row[1]][row[0]] = row[2]

for key, value in connections.items():
    total_times = total_times * len(value)
    total_plus += len(value)

print("part 1")
print(total_times)
mean = total_plus/len(connections)
print(mean)
print(mean ** len(connections))

connections = {}
total_times = 1
total_plus = 0

# Statespace part 2
with open('Deel 2/Bijlage/ConnectiesNationaal.csv', 'rt') as csv_file:
    reader = csv.reader(csv_file, delimiter=',')

    for row in reader: 
        if row[0] not in connections:
            connections[row[0]] = {} 
        connections[row[0]][row[1]] = row[2]

        if row[1] not in connections:
            connections[row[1]] = {}
        connections[row[1]][row[0]] = row[2]

for key, value in connections.items():
    total_times = total_times * len(value)
    total_plus += len(value)

print()
print("part 2")
print(total_times)
mean = total_plus/len(connections)
print(mean)
print(mean ** len(connections))
