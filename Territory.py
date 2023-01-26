from Structures.PlayerID import PlayerID
from typing import Iterator, Optional


class Territory:
    def __init__(self, territoryId: int, connections: dict, continent: int):
        self.territoryId = territoryId
        self.continent = continent
        self.ownedByPlayer = None
        self.numberOfTroops = 0
        self.paths = []

        self.insertConnections(connections)

    def __eq__(self, other):
        return self.territoryId == other.territoryId

    def __hash__(self):
        return self.territoryId

    def insertConnections(self, connections: dict):
        for territory in connections[str(self.territoryId)]:
            self.paths.append(territory)

    def paths(self) -> Iterator[int]:
        for i in self.paths:
            yield i

    def canReach(self, territoryId) -> bool:
        return territoryId in self.paths

    def numberOfTroops(self) -> int:
        return self.numberOfTroops

    def setOneTroop(self):
        self.numberOfTroops = 1

    def addTroops(self, troopsToAdd):
        self.numberOfTroops += troopsToAdd

    def removeTroops(self, troopsToRemove):
        self.numberOfTroops -= troopsToRemove

    @property
    def ownedByPlayer(self) -> Optional[PlayerID]:
        if self.ownedByPlayer is None:
            return self.ownedByPlayer
        else:
            return None

    @ownedByPlayer.setter
    def ownedByPlayer(self, playerName: PlayerID):
        self.ownedByPlayer = playerName
