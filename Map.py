from Structures.ValidPlayerColors import ValidPlayerColors
from Structures.ValidContinentColors import ValidContinentColors
from Territory import Territory

import networkx as nx
import json
import copy
import matplotlib.pyplot as plt
import ra


class Map:
    def __init__(self, mapPath):
        self.map = nx.Graph()
        self.loadMap(mapPath)
        self.territories = []
        self.connections = {}
        self.continents = {}
        self.continentsValue = {}
        self.neutralTerritories = copy.deepcopy(self.territories)

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

        self.connections = jsonDump["connections"]
        self.continents = jsonDump["continents"]
        self.continentsValue = jsonDump["continentsValue"]
        self.loadTerritories(jsonDump["territories"], self.connections)

        self.loadEdgesOnMap()

        mapping = dict(zip(self.map, range(0, len(list(self.map)))))
        self.map = nx.relabel_nodes(self.map, mapping)

        plt.ion()  # https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.ion.html

    def loadTerritories(self, territories, connections):
        for i in territories:
            continent = self.findContinentByTerritory(i)
            newTerritory = Territory(i, self.connections, continent)
            self.territories.append(newTerritory)
            self.map.add_node(newTerritory)

        self.territories.sort(key=lambda x: x.territoryId)

    def loadEdgesOnMap(self):
        for conn in self.connections:
            for edge in self.connections[conn]:
                self.map.add_edge(self.territories[int(conn)], self.territories[edge])

    def findContinentByTerritory(self, territory):
        for continent in self.continents.keys():
            if territory in self.continents[continent]:
                return continent

    getFriendFrontiersForTerritory
    getFrontiersForTerritory

    def getTerritoriesFromPlayer(self, playerID):
        returnList: list[Territory] = []

        for territory in self.territories:
            if territory.ownedByPlayer == playerID:
                returnList.append(territory)

        return returnList

    def getTerritoriesFromContinent(self, continent):
        returnList = []
        for territoryId in self.continents[continent]:
            returnList.append(self.territories[territoryId])

        return returnList

    def getTerritoriesIDAdjacent(self, territory):
        return list(self.map.neighbors(territory.territoryId))

    def showMap(self, seed: int = 639):
        occupationColors = self.colorTerritoryOccupation()
        continentColors = self.colorTerritoryContinent()
        territoryLabels = self.territoryLabels()

        plt.clf()
        pos = nx.spring_layout(self.map)

        plot = nx.draw_networkx_nodes(self.map, pos=pos,
                                      node_color=occupationColors, edgecolors=continentColors,
                                      linewidths=2.0, node_size=550)

        nx.draw_networkx_edges(self.map, pos=pos)
        nx.draw_networkx_labels(self.map, pos=pos,
                                labels=territoryLabels, font_size=9)

        plt.show()
        plt.pause(0.01)

    def colorTerritoryOccupation(self):
        returnList = []

        for territory in self.territories:
            if territory.ownedByPlayer is None:
                returnList.append(self.playerColorSchema[ValidPlayerColors.WHITE])

            else:
                returnList.append(self.playerColorSchema[territory.ownedByPlayer.playerColor])

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

