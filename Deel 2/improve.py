import csv

connections = {}
verbinding = 0

with open('Bijlage/ConnectiesNationaal.csv', 'rt') as csv_file:
    reader = csv.reader(csv_file, delimiter=',')
    for row in reader: 
        verbinding += 1
        if row[0] not in connections:
            connections[row[0]] = {}
        connections[row[0]][row[1]] = int(float(row[2]))

        if row[1] not in connections:
            connections[row[1]] = {}
        connections[row[1]][row[0]] = int(float(row[2]))

besttraject = {1: (['Haarlem', 'Heemstede-Aerdenhout', 'Leiden Centraal', 'Schiphol Airport', 'Utrecht Centraal', 'Ede-Wageningen', 'Arnhem Centraal', 'Dieren', 'Zutphen', 'Deventer', 'Apeldoorn'], 143), 2: (['Den Helder', 'Alkmaar', 'Castricum', 'Zaandam', 'Hoorn', 'Alkmaar'], 107), 3: (['Den Haag HS', 'Delft', 'Den Haag Laan v NOI', 'Leiden Centraal', 'Alphen a/d Rijn', 'Gouda', 'Den Haag Centraal', 'Leiden Centraal', 'Den Haag HS', 'Gouda', 'Utrecht Centraal'], 143), 4: (['Amsterdam Amstel', 'Utrecht Centraal', 'Amsterdam Centraal', 'Almere Centrum', 'Lelystad Centrum'], 80), 5: (['Schiphol Airport', 'Amsterdam Zuid', 'Amsterdam Sloterdijk', 'Zaandam', 'Beverwijk', 'Castricum'], 66), 6: (['Amersfoort', 'Zwolle', 'Assen', 'Groningen', 'Leeuwarden', 'Heerenveen'], 143), 7: (['Arnhem Centraal', 'Nijmegen', 'Oss', 's-Hertogenbosch', 'Utrecht Centraal', 'Alphen a/d Rijn'], 94), 8: (['Vlissingen', 'Roosendaal', 'Dordrecht', 'Breda', 'Etten-Leur', 'Roosendaal'], 121), 9: (['Sittard', 'Roermond', 'Weert', 'Eindhoven', 's-Hertogenbosch', 'Tilburg', 'Eindhoven', 'Helmond', 'Venlo'], 139), 10: (['Hilversum', 'Almere Centrum', 'Amsterdam Amstel', 'Amsterdam Centraal', 'Amsterdam Sloterdijk', 'Haarlem', 'Beverwijk'], 94), 11: (['Enschede', 'Hengelo', 'Almelo', 'Deventer', 'Zwolle', 'Steenwijk', 'Heerenveen'], 103), 12: (['Amsterdam Zuid', 'Amsterdam Amstel', 'Hilversum', 'Utrecht Centraal', 'Amersfoort', 'Apeldoorn', 'Zutphen'], 111), 13: (['Zwolle', 'Almelo'], 42), 14: (['Schiedam Centrum', 'Rotterdam Blaak', 'Rotterdam Alexander', 'Rotterdam Centraal', 'Schiedam Centrum', 'Delft', 'Den Haag Centraal'], 53), 15: (['Breda', 'Tilburg'], 13), 16: (['Heerlen', 'Sittard', 'Maastricht'], 30), 17: (['Rotterdam Centraal', 'Dordrecht', 'Rotterdam Blaak'], 31), 18: (['Den Haag Laan v NOI', 'Gouda', 'Rotterdam Alexander'], 38)}
start = []
end = []

for key, value in besttraject.items():
    start.append(value[0][0])
    end.append(value[0][-1])

for stations in start:
    for key, value in connections[stations].items():
        time = 200
        if key in start:
            starttraject = start.index(stations) + 1
            besttraject[starttraject][0].reverse()
            endtraject = start.index(key) + 1
            time = value  + besttraject[starttraject][1] + besttraject[endtraject][1]
        elif key in end:
            starttraject = end.index(key) + 1
            endtraject = start.index(stations) + 1
            time = value  + besttraject[starttraject][1] + besttraject[endtraject][1]
        if time < 180 and besttraject[starttraject] != besttraject[endtraject]:
            newtraject = besttraject[starttraject][0] + besttraject[endtraject][0]
            print(newtraject)
            print(time)

print('end')
for stations in end:
    for key, value in connections[stations].items():
        time = 200
        if key in end:
            starttraject = end.index(stations) + 1
            endtraject = end.index(key) + 1
            time = value  + besttraject[starttraject][1] + besttraject[endtraject][1]
            besttraject[endtraject][0].reverse()

        if time < 180 and besttraject[starttraject] != besttraject[endtraject]:
            newtraject = besttraject[starttraject][0] + besttraject[endtraject][0]
            print(newtraject)
            print(time)    