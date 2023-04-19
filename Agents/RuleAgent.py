import Action
import random


class RuleAgent:
    def __init__(self, playerID):
        self.playerID = playerID
        self.cards = []

        self.movedUnitThisTurn = []

        self.currentlyCapturingContinent = False
        self.continentBeingCaptured = None

    def playAllocation(self, gameState):
        gameMap = gameState.map

        if self.currentlyCapturingContinent:
            if len(gameMap.neutralTerritoriesFromContinent(self.continentBeingCaptured)) > 0:
                action = self.captureNeutralTerritoryFromContinent(gameMap)
            else:
                territoryChosen = random.choice(gameMap.neutralTerritories)
                action = Action.AllocationAction(territoryChosen.territoryId, self.playerID)
                self.currentlyCapturingContinent = False

        else:
            bestContinent = self.searchBestContinent(gameState)
            if bestContinent is not None:
                self.currentlyCapturingContinent = True
                self.continentBeingCaptured = bestContinent

                action = self.captureNeutralTerritoryFromContinent(gameMap)

            else:
                territoryChosen = random.choice(gameMap.neutralTerritories)
                action = Action.AllocationAction(territoryChosen.territoryId, self.playerID)

        return action

    def captureNeutralTerritoryFromContinent(self, gameMap):
        territories = gameMap.neutralTerritoriesFromContinent(self.continentBeingCaptured)
        territoryChosen = random.choice(territories)

        if len(territories) <= 1:
            self.currentlyCapturingContinent = False

        return Action.AllocationAction(territoryChosen.territoryId, self.playerID)

    def searchBestContinent(self, gameState):
        currentContinent = None
        currentYield = 0

        for continent in gameState.map.continents:
            emptyContinent = True
            for terr in gameState.map.getTerritoriesFromContinent(continent):
                if gameState.map.territories[terr.territoryId].ownedByPlayer is not None:
                    emptyContinent = False

            if emptyContinent:
                continentValue = gameState.map.continentsValue[continent[0]]
                #print("2 ", gameState.map._continents)
                continentYield = continentValue / len(gameState.map.getTerritoriesFromContinent(continent))

                if continentYield > currentYield:
                    currentContinent = continent[0]
                    currentYield = continentYield

        return currentContinent

    def playAddUnits(self, gameState):
        gameMap = gameState.map

        allTerr = gameMap.getTerritoriesFromPlayerInFrontierWithEnemy(self.playerID)

        if len(allTerr) == 0:
            allTerr = gameMap.getTerritoriesFromPlayer(self.playerID)

        lowestTroop = 10000
        lowestTerr = None
        for terr in allTerr:
            if terr.numberOfTroops < lowestTroop:
                lowestTroop = terr.numberOfTroops
                lowestTerr = terr

        # resets movement
        self.movedUnitThisTurn = []

        action = Action.AddUnitsInConflictAction(lowestTerr.territoryId)

        return action

    def addUnitsInContinent(self, gameState, continent):
        lowestTroop = 10000
        lowestTerr = None

        #print("1 ", gameState.map._continents)
        for terr in gameState.map.getTerritoriesFromContinent(continent):
            if terr.numberOfTroops < lowestTroop:
                lowestTroop = terr.numberOfTroops
                lowestTerr = terr

        action = Action.AddUnitsInConflictAction(lowestTerr.territoryId)

        return action

    def addUnitsInTerritory(self, gameState, territory):
        action = Action.AddUnitsInConflictAction(territory)

        return action

    def playExchangeCards(self, gameState):
        action = None

        if len(self.cards) == 3 or len(self.cards) == 4:
            for card in self.cards:
                if card.territory in gameState.map.getTerritoriesFromPlayer(self.playerID):
                    self.cards.remove(card)
                    card1 = random.choice(self.cards)
                    self.cards.remove(card1)
                    card2 = random.choice(self.cards)

                    self.cards.append(card)
                    self.cards.append(card1)

                    cards = [card, card1, card2]

                    gameState.territoryToAddTroops = card.territory

                    action = Action.AddUnitsInExchangeCardsAction(cards)

                    return action

        if len(self.cards) == 5:
            for card in self.cards:
                if card.territory in gameState.map.getTerritoriesFromPlayer(self.playerID):
                    self.cards.remove(card)
                    card1 = random.choice(self.cards)
                    self.cards.remove(card1)
                    card2 = random.choice(self.cards)

                    self.cards.append(card)
                    self.cards.append(card1)

                    cards = [card, card1, card2]

                    gameState.territoryToAddTroops = card.territory

                    action = Action.AddUnitsInExchangeCardsAction(cards)

                    return action

            if action is None:
                card1 = random.choice(self.cards)
                self.cards.remove(card1)
                card2 = random.choice(self.cards)
                self.cards.remove(card2)
                card3 = random.choice(self.cards)
                self.cards.remove(card3)

                self.cards.append(card1)
                self.cards.append(card2)
                self.cards.append(card3)

                cards = [card1, card2, card3]

                action = Action.AddUnitsInExchangeCardsAction(cards)

                return action

        action = Action.PassTurn()
        return action

    def playAttack(self, gameState):
        gameMap = gameState.map

        allTerr = gameMap.getTerritoriesFromPlayerInFrontierWithEnemy(self.playerID)

        for terr in allTerr:
            if terr.numberOfTroops >= 3:
                enemyTerritories = gameMap.getEnemyFrontiersForTerritory(terr)

                lowestEnemyTerrUnits = 10000
                lowestEnemyTerr = None
                for enemyTerr in enemyTerritories:
                    if enemyTerr.numberOfTroops < lowestEnemyTerrUnits:
                        lowestEnemyTerrUnits = enemyTerr.numberOfTroops
                        lowestEnemyTerr = enemyTerr
                action = Action.AttackWithUnitsInConflictAction(terr.territoryId, lowestEnemyTerr.territoryId)

                return action

        action = Action.PassTurn()
        return action

    def playMoveUnits(self, gameState):
        gameMap = gameState.map

        terrs = gameMap.firstGetAdjacencyFromFrontierForMoveUnits(self.playerID, self.movedUnitThisTurn)

        if terrs is None:
            action = Action.PassTurn()
            return action

        else:
            self.movedUnitThisTurn.append(terrs[0])
            action = Action.MoveUnitsInConflictAction(terrs[0], terrs[1])
            return action
