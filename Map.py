from Structures.ValidPlayerColors import ValidPlayerColors
from Structures.ValidContinentColors import ValidContinentColors
from Territory import Territory

import networkx as nx
import json
import copy
import matplotlib.pyplot as plt
import random
import numpy as np


class Map:
    def __init__(self, mapPath):
        self.map = nx.DiGraph()
        self._territories = []
        self._connections = {}
        self._continents = {}
        self._continentsValue = {}

        self.loadMap(mapPath)

        self._neutralTerritories = copy.deepcopy(self.territories)

        self.playerColorSchema = {
            ValidPlayerColors.RED: "tomato",
            ValidPlayerColors.BLUE: "slateblue",
            ValidPlayerColors.GREEN: "springgreen",
            ValidPlayerColors.PURPLE: "mediumorchid",
            ValidPlayerColors.WHITE: "white"
        }

        self.continentColorSchema = {
            ValidContinentColors.SALMON: "salmon",
            ValidContinentColors.FORESTGREEN: "forestgreen",
            ValidContinentColors.LIME: "lime",
            ValidContinentColors.GOLD: "gold",
            ValidContinentColors.DARKORANGE: "darkorange",
            ValidContinentColors.DARKKHAKI: "darkkhaki",
            ValidContinentColors.PINK: "pink",
            ValidContinentColors.CORAL: "coral",
            ValidContinentColors.LAVENDER: "lavender",
            ValidContinentColors.MEDIUMPURPLE: "mediumpurple",
            ValidContinentColors.MAGENTA: "magenta",
            ValidContinentColors.MOCCASIN: "moccasin",
            ValidContinentColors.YELLOW: "yellow",
            ValidContinentColors.PALEGREEN: "palegreen",
            ValidContinentColors.TEAL: "teal",
            ValidContinentColors.CADETBLUE: "cadetblue",
            ValidContinentColors.PLUM: "plum",
            ValidContinentColors.DEEPPINK: "deeppink",
            ValidContinentColors.HOTPINK: "hotpink"
        }

    def loadMap(self, mapPath):
        with open(mapPath, "r") as fp:
            jsonDump = json.load(fp)

        self._connections = jsonDump["connections"]
        self._continents = jsonDump["continents"]
        self._continentsValue = jsonDump["continentsValue"]
        self.__loadTerritories(jsonDump["territories"], self._connections)

        self.__loadEdgesOnMap()

        mapping = dict(zip(self.map, range(0, len(list(self.map)))))
        self.map = nx.relabel_nodes(self.map, mapping)

        plt.ion()  # https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.ion.html

    def __loadTerritories(self, territories, connections):
        for i in territories:
            continent = self.findContinentByTerritory(i)
            newTerritory = Territory(i, self._connections, continent)
            self.territories.append(newTerritory)
            self.map.add_node(newTerritory)

        self.territories.sort(key=lambda x: x.territoryId)

    def findContinentByTerritory(self, territoryidToAdd):
        for continent in self._continents.keys():
            if territoryidToAdd in self._continents[continent]:
                return continent

    def __loadEdgesOnMap(self):
        for conn in self._connections:
            for edge in self._connections[conn]:
                self.map.add_edge(self.territories[int(conn)], self.territories[edge])

    @property
    def territories(self):
        return self._territories

    @property
    def neutralTerritories(self):
        return self._neutralTerritories

    @property
    def continents(self):
        return self._continents

    @property
    def continentsValue(self):
        return self._continentsValue

    def neutralTerritoriesFromContinent(self, continent):
        returnList = []
        for terr in self.neutralTerritories:
            if terr.continent == continent:
                returnList.append(terr)
        return returnList

    def captureNeutralTerritory(self, territory, playerID):
        territory.ownedByPlayer = playerID
        territory.addTroops(1)
        self.neutralTerritories.remove(territory)

    def getTerritoriesFromPlayer(self, playerID):
        returnList = []

        for territory in self.territories:
            if territory.ownedByPlayer == playerID:
                returnList.append(territory)

        return returnList

    def getTerritoriesFromEnemy(self, playerID):
        returnList = []

        for territory in self._territories:
            if territory.ownedByPlayer != playerID:
                returnList.append(territory)

        return returnList

    def getTerritoriesFromPlayerInFrontierWithEnemy(self, playerID):
        returnList = []

        playerTerritories = self.getTerritoriesFromPlayer(playerID)

        for territory in playerTerritories:
            territoryInFrontier = False
            for enemyTerritoryId in self.getTerritoriesIDAdjacent(territory):
                if self.territories[enemyTerritoryId].ownedByPlayer != playerID:
                    territoryInFrontier = True
            if territoryInFrontier:
                returnList.append(territory)

        return returnList

    def getEnemyFrontiersForTerritory(self, territoryToAnalyze: Territory):
        returnList = []
        listIdTerritories = list(self.map.neighbors(territoryToAnalyze.territoryId))
        for terrId in listIdTerritories:
            if self.territories[terrId].ownedByPlayer != territoryToAnalyze.ownedByPlayer:
                returnList.append(self.territories[terrId])

        return returnList

    def firstGetAdjacencyFromFrontierForMoveUnits(self, playerId, listOfMoved):
        territoriesInFrontier = self.getTerritoriesFromPlayerInFrontierWithEnemy(playerId)
        territoriesIdInFrontier = [o.territoryId for o in territoriesInFrontier]
        territoriesIdInFrontier = [i for i in territoriesIdInFrontier if i not in listOfMoved]
        playerTerritories = self.getTerritoriesFromPlayer(playerId)

        for territory in playerTerritories:
            if territory.numberOfTroops > 1:
                territoryNumberOfTroops = 100
                enemyTerritoryAdjacent = False
                for territoryIdInAdjacency in self.getTerritoriesIDAdjacent(territory):
                    if self.territories[territoryIdInAdjacency].ownedByPlayer != playerId:
                        enemyTerritoryAdjacent = True
                    if territoryIdInAdjacency in territoriesIdInFrontier:
                        if self.territories[territoryIdInAdjacency].numberOfTroops < territoryNumberOfTroops:
                            territoryNumberOfTroops = self.territories[territoryIdInAdjacency].numberOfTroops
                    if territoryIdInAdjacency is not None and enemyTerritoryAdjacent is False and territoryIdInAdjacency in territoriesIdInFrontier:
                        return territory.territoryId, territoryIdInAdjacency
        return None

    def getTerritoriesFromContinent(self, continent):
        returnList = []

        #print("0 ", self._continents)
        for territoryId in self._continents[continent]:
            returnList.append(self.territories[territoryId])

        return returnList

    def getTerritoriesIDAdjacent(self, territory):
        return list(self.map.neighbors(territory.territoryId))

    def colorTerritoryOccupation(self):
        returnList = []

        for territory in self.territories:
            if territory.ownedByPlayer is None:
                returnList.append(self.playerColorSchema[ValidPlayerColors.WHITE])

            else:
                returnList.append(self.playerColorSchema[territory.ownedByPlayer.playerColor])  # type: ignore

        return returnList

    def colorTerritoryContinent(self):
        colorList = list(self.continentColorSchema.values())
        returnList = []

        for territory in self.territories:
            returnList.append(colorList[int(territory.continent)])

        return returnList

    def territoryLabels(self):
        returnList = {}

        for territory in self.territories:
            returnList[territory.territoryId] = (str(territory.territoryId) + "(" + str(territory.numberOfTroops) + ")")

        return returnList

    def getFriendFrontiersForTerritory(self, territoryToAnalyze: Territory):
        returnList = []
        listIdTerritories = list(self.map.neighbors(territoryToAnalyze.territoryId))
        for terrId in listIdTerritories:
            if self.territories[terrId].ownedByPlayer == territoryToAnalyze.ownedByPlayer:
                returnList.append(self.territories[terrId])

        return returnList

    def showMap(self, seed = 639):
        random.seed(seed)
        np.random.seed(seed)

        occupationColors = self.colorTerritoryOccupation()
        continentColors = self.colorTerritoryContinent()
        territoryLabels = self.territoryLabels()

        plt.clf()
        pos = nx.spring_layout(self.map)

        nx.draw_networkx_nodes(self.map, pos=pos,
                                      node_color=occupationColors, edgecolors=continentColors,
                                      linewidths=2.0, node_size=550)

        nx.draw_networkx_edges(self.map, pos=pos)
        nx.draw_networkx_labels(self.map, pos=pos,
                                labels=territoryLabels, font_size=9)

        plt.savefig("map13655.png", bbox_inches='tight', dpi=100)
        plt.draw()
        plt.pause(0.01)

    def isPlanarGraph(self):
        return nx.check_planarity(self.map)[0]

    def isConnectedGraph(self):
        return nx.is_connected(self.map)


#mapa = Map("/home/lana/Documentos/results risk generation/result_190generations/results_risk_generation_190generations_50offspring_24tournamentsize_0.8mutationrate/map13655.json")
#mapa.showMap()






