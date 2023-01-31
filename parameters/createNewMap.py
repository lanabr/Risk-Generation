import json

mapName = input("Input map name:")
numberOfTerritories = int(input("Insert number of territories: "))

mapDict = {"territories": list(range(numberOfTerritories))}

tempDict = {}
for i in range(numberOfTerritories):
    tempList = []
    loop = True
    while loop:
        newTerritory = input("Insert new territory connection to " + str(i) + ": ")
        if newTerritory == '':
            loop = False
        else:
            tempList.append(int(newTerritory))

    tempDict[int(i)] = tempList

mapDict["connections"] = tempDict

for territory in mapDict["connections"].keys():
    for connectedTerritory in mapDict["connections"][territory]:
        if territory not in mapDict["connections"][connectedTerritory]:
            mapDict["connections"][connectedTerritory].append(territory)

numberOfContinents = int(input("Insert number of continents: "))
mapDict["continents"] = {}

for i in range(numberOfContinents):
    mapDict["continents"][int(i)] = []

for territory in range(numberOfTerritories):
    continent = input("Insert number of continent for territory  " + str(territory) + ": ")
    mapDict["continents"][int(continent)].append(int(territory))

mapDict["continentsValue"] = {}
for i in range(numberOfContinents):
    mapDict["continentsValue"][int(i)] = int(input("Insert continent value for continent " + str(i) + ": "))

with open("parameters/" + mapName + ".json", "w") as fp:
    fp.write(json.dumps(mapDict, indent=4))
