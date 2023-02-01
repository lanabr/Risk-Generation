class Territory:
    def __init__(self, territoryId, connections, continent):
        self.territoryId = territoryId
        self.continent = continent
        self.__ownedByPlayer = None
        self.__numberOfTroops = 0
        self._paths = []

        self.__insertConnections(connections)

    def __eq__(self, other):
        return self.territoryId == other.territoryId

    def __hash__(self):
        return self.territoryId

    def __insertConnections(self, connections):
        for territory in connections[str(self.territoryId)]:
            self._paths.append(territory)

    @property
    def paths(self):
        for i in self.paths:
            yield i

    def canReach(self, territoryId):
        return territoryId in self.paths

    @property
    def numberOfTroops(self):
        return self.__numberOfTroops

    def setOneTroop(self):
        self.__numberOfTroops = 1

    def addTroops(self, troopsToAdd):
        self.__numberOfTroops += troopsToAdd

    def removeTroops(self, troopsToRemove):
        self.__numberOfTroops -= troopsToRemove

    @property
    def ownedByPlayer(self):
        if self.__ownedByPlayer is not None:
            return self.__ownedByPlayer
        else:
            return None

    @ownedByPlayer.setter
    def ownedByPlayer(self, playerName):
        self.__ownedByPlayer = playerName
