import copy

import networkx as nx

from Parameters import Parameters
from CalculateCriteria import CalculateCriteria
import random
from time import time
from Map import Map
import json
import os


MAPCOUNT = 11


def calculateCriteria(gameParameters):
    metricsFile = "metrics/game" + str(gameParameters.troopsWonBeginTurn) + "-" + str(gameParameters.defenseDices) + "-" \
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


def fitnessDistance(gameParameters):
    fitness = 0
    ideal = {"advantage": 0, "duration": 0, "drama": 0.5, "leadChange": 0.5, "branchingFactor": 0.5, "completion": 1, "killerMoves": 0.5}

    #ideal = {"duration": 0, "drama": 0.5, "leadChange": 0.5, "branchingFactor": 0.5, "completion": 1, "killerMoves": 0.5}
    #ideal = {"advantage": 0, "drama": 0.5, "leadChange": 0.5, "branchingFactor": 0.5, "completion": 1, "killerMoves": 0.5}
    #ideal = {"advantage": 0, "duration": 0, "leadChange": 0.5, "branchingFactor": 0.5, "completion": 1, "killerMoves": 0.5}
    #ideal = {"advantage": 0, "duration": 0, "drama": 0.5, "branchingFactor": 0.5, "completion": 1, "killerMoves": 0.5}
    #ideal = {"advantage": 0, "duration": 0, "drama": 0.5, "leadChange": 0.5, "branchingFactor": 0.5, "killerMoves": 0.5}
    #ideal = {"advantage": 0, "duration": 0, "drama": 0.5, "leadChange": 0.5, "branchingFactor": 0.5, "completion": 1,}
    #ideal = {"advantage": 0, "duration": 0, "drama": 0.5, "leadChange": 0.5, "completion": 1, "killerMoves": 0.5}

    for key in ideal:
        fitness += abs(gameParameters.criteria[key] - ideal[key])

    return fitness


def fitnessWeighted(gameParameters):
    fitness = 0
    weights = {"advantage": 0.2, "drama": 0.2, "duration": 0.15, "leadChange": 0.15, "completion": 0.15, "killerMoves": 0.1, "branchingFactor": 0.05}

    #weights = {"drama": 0.25, "duration": 0.2, "leadChange": 0.15, "completion": 0.15, "killerMoves": 0.15, "branchingFactor": 0.1}
    #weights = {"advantage": 0.25, "duration": 0.2, "leadChange": 0.15, "completion": 0.15, "killerMoves": 0.15, "branchingFactor": 0.1}
    #weights = {"advantage": 0.25, "drama": 0.25, "leadChange": 0.15, "completion": 0.15, "killerMoves": 0.1, "branchingFactor": 0.1}
    #weights = {"advantage": 0.25, "drama": 0.25, "duration": 0.15, "completion": 0.15, "killerMoves": 0.1, "branchingFactor": 0.1}
    #weights = {"advantage": 0.25, "drama": 0.25, "duration": 0.15, "leadChange": 0.15, "killerMoves": 0.1, "branchingFactor": 0.1}
    #weights = {"advantage": 0.25, "drama": 0.25, "duration": 0.15, "leadChange": 0.15, "completion": 0.15, "branchingFactor": 0.05}

    #weights = {"advantage": 0.2, "drama": 0.2, "duration": 0.15, "leadChange": 0.15, "completion": 0.15, "killerMoves": 0.15}

    for key in gameParameters.criteria:
        fitness += weights[key] * gameParameters.criteria[key]

    return fitness


def calculateFitness(gameParameters):
    fitness = fitnessDistance(gameParameters)
    #fitness = fitnessWeighted(gameParameters)

    return fitness


def selectionTournament(population, tournamentSize):
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

    cont1 = random.sample(allContinents1, k=k1)
    cont2 = random.sample(allContinents2, k=k2)

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

    # check if there are territories connected to themselves
    for i in range(len(newConnections)):
        if i in newConnections[i]:
            newConnections[i].remove(i)

    # check if connections are symmetric
    for i in range(len(newConnections)):
        for j in newConnections[i]:
            if newConnections[j] is []:
                newConnections[j].append(i)
            if i not in newConnections[j]:
                newConnections[j].append(i)

    # if territory dont have any connections, add a random one
    for i in range(len(newConnections)):
        if len(newConnections[i]) == 0:
            listTerr = list(range(len(newConnections)))
            listTerr.remove(i)
            newTerr = random.choice(listTerr)

            newConnections[i].append(newTerr)
            newConnections[newTerr].append(i)

    territories = list(range(len(newConnections)))

    global MAPCOUNT
    mapPath = exportMap(territories, newConnections, newMapContinents, newContValues, MAPCOUNT)
    mapParts = [territories, newConnections, newMapContinents, newContValues]

    return mapPath, mapParts


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


def crossover(parents):
    global MAPCOUNT

    offspring = []
    mapParts = []

    features = [1, 1, 0, 0]
    random.shuffle(features)

    newMapPath1, mapPartsTemp1 = mapCrossover(parents[0].mapPath, parents[1].mapPath)
    featuresChild1 = (Parameters(newMapPath1, parents[features[0]].troopsWonBeginTurn, parents[features[1]].defenseDices, parents[features[2]].initialTerritoriesMode, parents[features[3]].troopsToNewTerritory))
    featuresChild1.mapNumber = MAPCOUNT

    MAPCOUNT += 1

    for i in range(len(features)):
        if features[i] == 1:
            features[i] = 0
        else:
            features[i] = 1

    newMapPath2, mapPartsTemp2 = mapCrossover(parents[0].mapPath, parents[1].mapPath)
    featuresChild2 = (Parameters(newMapPath2, parents[features[0]].troopsWonBeginTurn, parents[features[1]].defenseDices, parents[features[2]].initialTerritoriesMode, parents[features[3]].troopsToNewTerritory))
    featuresChild2.mapNumber = MAPCOUNT

    MAPCOUNT += 1

    mapParts.append(mapPartsTemp1)
    mapParts.append(mapPartsTemp2)

    offspring.append(featuresChild1)
    offspring.append(featuresChild2)

    return offspring, mapParts


def getContinentFromTerritory(continents, possibleTerr):
    for cont in continents:
        if possibleTerr in cont:
            return cont


def mapMutation(mutation_rate, mapParts, mapNumber):
    random.seed(time())

    territories = mapParts[0]
    connections = mapParts[1]
    continents = mapParts[2]
    continentsValue = mapParts[3]

    if random.random() > mutation_rate:   # Create connection
        terr1 = random.randint(0, len(connections) - 1)
        terr2 = random.randint(0, len(connections) - 1)

        if terr1 != terr2 and terr2 not in connections[terr1]:
            connections[terr1].append(terr2)
            connections[terr2].append(terr1)

    if random.random() > mutation_rate:   # Remove connection
        terr1 = random.randint(0, len(connections) - 1)
        terr2 = random.choice(connections[terr1])

        if len(connections[terr1]) > 1 and len(connections[terr2]) > 1:
            if terr2 in connections[terr1]:
                connections[terr1].remove(int(terr2))
                if terr1 in connections[terr2]:
                    connections[terr2].remove(int(terr1))

    #print("2 ", continents)

    if random.random() > mutation_rate:    # "Steal" a territory from a continent
        if len(continents) > 1:
            cont = random.choice(continents)
            stoleTerr = False
            terrList = copy.copy(cont)
            while stoleTerr is False and len(terrList) > 0:
                terr1 = random.choice(terrList)
                #print(cont, terr1)
                if len(connections[terr1]) < 1:
                    terrList.remove(terr1)
                    continue
                possibleTerr = random.choice(connections[terr1])
                contPossibleTerr = getContinentFromTerritory(continents, possibleTerr)
                terrList.remove(terr1)

                if possibleTerr not in cont and len(contPossibleTerr) > 1:
                    stoleTerr = True
                    for c in continents:
                        c.remove(possibleTerr) if possibleTerr in c else None
                    cont.append(possibleTerr)

    #print("3 ", continents)

    if random.random() > mutation_rate:    # Swap the value of two continents
        if len(continents) > 1:
            cont1 = random.randint(0, len(continentsValue) - 1)
            cont2 = random.randint(0, len(continentsValue) - 1)

            temp = continentsValue[cont1]
            continentsValue[cont1] = continentsValue[cont2]
            continentsValue[cont2] = temp

    if random.random() > mutation_rate:    # Modify the value of a continent
        cont = random.randint(0, len(continentsValue) - 1)

        decide = random.choice([True, False])
        if decide:
            continentsValue[cont] += 1
        else:
            continentsValue[cont] = max(1, continentsValue[cont])

    mapPath = exportMap(territories, connections, continents, continentsValue, mapNumber)

    return mapPath


def mutation(offspring, mapParts, mutationRate):
    random.seed(time())

    for child in offspring:
        child.mapPath = mapMutation(mutationRate, mapParts[offspring.index(child)], child.mapNumber)

        if random.random() > mutationRate:
            possible = [1, 2, 3, 4]

            possible.remove(child.troopsWonBeginTurn)

            child.troopsWonBeginTurn = random.choice(possible)

        if random.random() > mutationRate:
            if child.defenseDices == 3:
                child.defenseDices = 2
            else:
                child.defenseDices = 3

        if random.random() > mutationRate:
            if child.initialTerritoriesMode == 'random':
                child.initialTerritoriesMode = 'pick'
            else:
                child.initialTerritoriesMode = 'random'

        if random.random() > mutationRate:
            if child.troopsToNewTerritory == 'min':
                child.troopsToNewTerritory = 'max'
            else:
                child.troopsToNewTerritory = 'min'

    return offspring


def checkMap(offspring):
    for child in offspring:
        map = Map(child.mapPath)
        check = True

        # check planar graph
        if not nx.is_planar(map.map):
            check = False

        # check connected graph
        if not nx.is_strongly_connected(map.map):
            check = False

        if not check:
            offspring.remove(child)

    return offspring


def exportMap(territories, connections, continents, continentsValue, mapNumber):
    fileName = "parameters/map" + str(mapNumber) + ".json"
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


#print(len(checkMap([Parameters("parameters/results_risk_generation_10generations_10offspring_2tournamentsize_0.2mutationrate/map33.json", 1, 2, "random", "min")])))
