class Heuristic:
    def __init__(self, weightTerr=0.8, weightUnit=0.2):
        self.weightTerr = weightTerr
        self.weightUnit = weightUnit

    def heuristicForPlayer(self, gs, player):
        terrFromPlayer = gs.map.getTerritoriesFromPlayer(player)
        unitsFromPlayer = 0

        for terr in terrFromPlayer:
            unitsFromPlayer += terr.numberOfTroops

        allUnits = 0
        allTerr = gs.map.territories

        for terr in allTerr:
            allUnits += terr.numberOfTroops

        return ((len(terrFromPlayer) / len(allTerr)) * self.weightTerr) + ((unitsFromPlayer / allUnits) * self.weightUnit)

    def heuristicFromGameState(self, gs, totalMoves):
        returnList = []
        for player, tM in zip(gs.listOfPlayers, totalMoves):
            hPlayer = self.heuristicForPlayer(gs, player.playerID)
            returnList.append((player, hPlayer, tM))
        return returnList
