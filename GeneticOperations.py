from Parameters import Parameters
from CalculateCriteria import CalculateCriteria
import random
from time import time
from Map import Map
import json
import os

MAPCOUNT = 6


def calculateCriteria(gameParameters):
    metricsFile = "metrics/game" + gameParameters.mapPath[-6] + "-" \
                  + str(gameParameters.troopsWonBeginTurn) + "-" + gameParameters.advantageAttack + "-" \
                  + gameParameters.initialTerritoriesMode + "-" + gameParameters.troopsToNewTerritory + ".txt"

    criteria = CalculateCriteria()
    criteria.importMetricsFromFile(metricsFile)
    gameParameters.criteria["advantage"] = criteria.calculateAdvantage()
    gameParameters.criteria["duration"] = criteria.calculateDuration()
    gameParameters.criteria["drama"] = criteria.calculateDrama()
    gameParameters.criteria["leadChange"] = criteria.calculateLeadChange()
    gameParameters.criteria["branchingFactor"] = criteria.calculateBranchingFactor()
    gameParameters.criteria["completion"] = criteria.calculateCompletion()
    gameParameters.criteria["killerMoves"] = criteria.calculateKillerMoves()

    return gameParameters.criteria


def calculateFitness(gameParameters):
    fitness = 0
    ideal = {"advantage": 0, "duration": 0, "drama": 0.5, "leadChange": 0.5, "branchingFactor": 0.5, "completion": 1, "killerMoves": 0.5}

    for key in gameParameters.criteria:
        fitness += abs(gameParameters.criteria[key] - ideal[key])

    return fitness


def selectionTournament(population, tournamentSize):
    # tournament selection
    tournament = []
    for i in range(tournamentSize):
        tournament.append(population[random.randint(0, len(population) - 1)])

    tournament.sort(key=lambda x: x.fitness)

    return [tournament[0], tournament[1]]


def mapCrossover(mapPath1, mapPath2):
    random.seed(time())

    map1 = Map(mapPath1)
    map2 = Map(mapPath2)

    allContinents1 = list(map1._continents.keys())
    allContinents2 = list(map2._continents.keys())

    k1 = random.choice(range((len(allContinents1) // 2) - 1, (len(allContinents1) // 2) + 2))
    k1 = max(1, min(k1, len(allContinents1)))

    k2 = random.choice(range((len(allContinents2) // 2) - 1, (len(allContinents2) // 2) + 2))
    k2 = max(1, min(k2, len(allContinents2)))

    cont1 = random.choices(allContinents1, k=k1)
    cont2 = random.choices(allContinents2, k=k2)

    territoriesFrom1 = getTerritoriesFromContinents(map1, cont1)
    territoriesFrom2 = getTerritoriesFromContinents(map2, cont2)

    connectionsFrom1 = getConnectionsFromTerritories(map1, territoriesFrom1)
    connectionsFrom2 = getConnectionsFromTerritories(map2, territoriesFrom2)

    translate1Dict = {}  # type:ignore
    translate2Dict = {}  # type:ignore

    for i in range(0, len(territoriesFrom1)):
        translate1Dict[territoriesFrom1[i]] = i
    for i in range(0, len(territoriesFrom2)):
        translate2Dict[territoriesFrom2[i]] = i + len(territoriesFrom1)

    newMapContinents = []  # type:ignore

    for cont in cont1:
        newMapContinents.append([])
        for terr in map1._continents[cont]:
            newMapContinents[-1].append(translate1Dict[terr])

    for cont in cont2:
        newMapContinents.append([])
        for terr in map2._continents[cont]:
            newMapContinents[-1].append(translate2Dict[terr])

    newConnections = []  # type:ignore
    abroadConnections = {}  # type:ignore

    allNewTerr1 = list(translate1Dict.values())
    allNewTerr2 = list(translate2Dict.values())

    for terr in range(len(connectionsFrom1)):
        newConnections.append([])
        connFromAbroad = []  # type:ignore
        for connTerr in connectionsFrom1[terr]:
            if connTerr != -1:
                newConnections[-1].append(translate1Dict[connTerr])
            else:
                connect2 = random.choice(allNewTerr2)

                if connect2 not in connFromAbroad:
                    connFromAbroad.append(connect2)
                    newConnections[-1].append(connect2)

                    if connect2 not in abroadConnections.keys():
                        abroadConnections[connect2] = [terr]
                    else:
                        abroadConnections[connect2].append(terr)
                else:
                    pass

    for terr in range(len(connectionsFrom2)):
        newConnections.append([])
        for connTerr in connectionsFrom2[terr]:
            if connTerr != -1:
                newConnections[-1].append(translate2Dict[connTerr])
            else:
                if terr + len(connectionsFrom1) in abroadConnections.keys():
                    if len(abroadConnections[terr + len(connectionsFrom1)]) > 0:
                        newConnections[-1].append(abroadConnections[terr + len(connectionsFrom1)].pop(0))
                else:
                    pass

    newContValues = []
    for i in cont1:
        newContValues.append(map1._continentsValue[i])
    for i in cont2:
        newContValues.append(map2._continentsValue[i])

    territories = list(range(len(newConnections)))

    mapPath = exportMap(territories, newConnections, newMapContinents, newContValues)

    return mapPath


def getTerritoriesFromContinents(map, cont):
    territories = []  # type:ignore

    for c in cont:
        newTerritories = map._continents[c]
        for terr in newTerritories:
            territories.append(terr)

    return territories


def getConnectionsFromTerritories(map, territories):
    connections = []  # type:ignore

    for terr in territories:
        newListTerrs = []  # type:ignore
        for i in map._connections[str(terr)]:
            if i in territories:
                newListTerrs.append(i)
            else:
                newListTerrs.append(-1)
        connections.append(newListTerrs)

    return connections


def crossover(parents, numOffspring):
    # scattered crossover
    global MAPCOUNT

    offspring = []
    for i in range(numOffspring):
        newMapPath = mapCrossover(parents[0].mapPath, parents[1].mapPath)
        MAPCOUNT += 1
        newTroopsWonBeginTurn = random.choice([parents[0].troopsWonBeginTurn, parents[1].troopsWonBeginTurn])
        newAdvantageAttack = random.choice([parents[0].advantageAttack, parents[1].advantageAttack])
        newInitialTerritoriesMode = random.choice([parents[0].initialTerritoriesMode, parents[1].initialTerritoriesMode])
        newTroopsToNewTerritory = random.choice([parents[0].troopsToNewTerritory, parents[1].troopsToNewTerritory])

        offspring.append(Parameters(newMapPath, newTroopsWonBeginTurn, newAdvantageAttack, newInitialTerritoriesMode, newTroopsToNewTerritory))

    return offspring


def mapMutation(mapPath, mutation_rate):
    map = Map(mapPath)
    random.seed(time())

    territories = map.territories
    connections = map._connections
    continents = map.continents
    continentsValue = map.continentsValue

    if random.random() > mutation_rate:   # Create connection
        terr1 = random.randint(0, len(connections) - 1)
        terr2 = random.randint(0, len(connections) - 1)

        if terr1 != terr2 and terr2 not in connections[str(terr1)]:
            connections[str(terr1)].append(terr2)
            connections[str(terr2)].append(terr1)

    if random.random() > mutation_rate:   # Remove connection
        terr1 = random.randint(0, len(connections) - 1)
        terr2 = random.choice(connections[str(terr1)])

        connections[str(terr1)].remove(terr2)
        connections[str(terr2)].remove(terr1)

    if random.random() > mutation_rate:    # "Steal" a territory from a continent
        if len(continents) > 1:
            cont = random.choice(continents)
            stoleTerr = False
            while stoleTerr is False:
                terr1 = random.choice(cont)
                possibleTerr = random.choice(connections[str(terr1)])
                if possibleTerr not in cont:
                    stoleTerr = True
                    for c in continents:
                        c.remove(possibleTerr) if possibleTerr in c else None
                    cont.append(possibleTerr)

    if random.random() > mutation_rate:    # Swap the value of two continents
        if len(continents) > 1:
            cont1 = random.randint(0, len(continentsValue) - 1)
            cont2 = random.randint(0, len(continentsValue) - 1)

            temp = continentsValue[str(cont1)]
            continentsValue[cont1] = continentsValue[str(cont2)]
            continentsValue[cont2] = temp

    if random.random() > mutation_rate:    # Modify the value of a continent
        cont = random.randint(0, len(continentsValue) - 1)

        decide = random.choice([True, False])
        if decide:
            continentsValue[str(cont)] += 1
        else:
            continentsValue[str(cont)] = max(1, continentsValue[str(cont)])

    mapPath = exportMap(territories, connections, continents, continentsValue)

    return mapPath


def mutation(offspring):
    random.seed(time())
    mutation_rate = 0.7

    for child in offspring:
        child.mapPath = mapMutation(child.mapPath, mutation_rate)

        if random.random() > mutation_rate:
            possible = [1, 2, 3, 4, 5]

            possible.remove(child.troopsWonBeginTurn)

            child.troopsWonBeginTurn = random.choice(possible)

        if random.random() > mutation_rate:
            if child.advantageAttack == 'attack':
                child.advantageAttack = 'defense'
            else:
                child.advantageAttack = 'attack'

        if random.random() > mutation_rate:
            if child.initialTerritoriesMode == 'random':
                child.initialTerritoriesMode = 'pick'
            else:
                child.initialTerritoriesMode = 'random'

        if random.random() > mutation_rate:
            if child.troopsToNewTerritory == 'min':
                child.troopsToNewTerritory = 'max'
            else:
                child.troopsToNewTerritory = 'min'

    return offspring


def exportMap(territories, connections, continents, continentsValue):
    fileName = "parameters/map" + str(MAPCOUNT) + ".json"
    if os.path.exists(fileName):
        os.remove(fileName)

    exportDict = {"territories": territories}  # type:ignore

    connDict = {}  # type:ignore
    for i in range(len(connections)):
        connDict[str(i)] = connections[i]
    exportDict["connections"] = connDict

    contDict = {}  # type:ignore
    for i in range(len(continents)):
        contDict[str(i)] = continents[i]
    exportDict["continents"] = contDict

    contValueDict = {}  # type:ignore
    for i in range(len(continentsValue)):
        contValueDict[str(i)] = continentsValue[i]
    exportDict["continentsValue"] = contValueDict

    with open(fileName, "w") as fp:
        fp.write(json.dumps(exportDict, indent=4))

    return fileName
