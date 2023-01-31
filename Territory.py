class Territory:
    def __init__(self, territoryId, connections, continent):
        self.territoryId = territoryId
        self.continent = continent
        self._ownedByPlayer = None
        self._numberOfTroops = 0
        self._paths = []

        self.insertConnections(connections)

    def __eq__(self, other):
        return self.territoryId == other.territoryId

    def __hash__(self):
        return self.territoryId

    def insertConnections(self, connections):
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
        return self._numberOfTroops

    def setOneTroop(self):
        self._numberOfTroops = 1

    def addTroops(self, troopsToAdd):
        self._numberOfTroops += troopsToAdd

    def removeTroops(self, troopsToRemove):
        self._numberOfTroops -= troopsToRemove

    @property
    def ownedByPlayer(self):
        if self.ownedByPlayer is None:
            return self.ownedByPlayer
        else:
            return None

    @ownedByPlayer.setter
    def ownedByPlayer(self, playerName):
        self._ownedByPlayer = playerName
