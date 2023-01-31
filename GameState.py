from Structures.GamePhase import GamePhase
from Structures.TurnPhase import TurnPhase
from Structures.AddUnitsPhase import AddUnitsPhase
from Structures.Cards import TerritoryCards
from Map import Map
from Structures.ContinentHandler import ContinentHandler
import Action

import random
import numpy as np
import time
import math


class GameState:
    def __init__(self, listOfPlayers, parameters):
        self.listOfPlayers = listOfPlayers
        self.parameters = parameters
        self.map = Map(parameters.mapPath)

        self.gamePhase = GamePhase.ALLOCATION_PHASE
        self.turnPhase = TurnPhase.ADD_UNITS
        self.addUnitsPhase = AddUnitsPhase.CONTINENT_PHASE

        self.turnCount = 0
        self.playerTurnCount = 0
        self.currentPlayer = self.listOfPlayers[0]
        self.currentPlayerNumber = 0

        self.troopsToAddPickPhase = 0
        self.troopsToAddContinentPhase = []
        self.troopsToAddTerritoryPhase = 2

        self.territoryToAddTroops = None

        self.terrDeck = TerritoryCards(self.map)
        self.troopsPerCard = [2, 4, 6, 8, 10, 12, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 75, 80, 85, 90, 95, 100]
        self.currentChange = 0

        self.continentHandler = ContinentHandler(self.map.continents, self.map.territories, self.map.continentsValue)

    def checkGoal(self, player):
        continentCheck, territoriesCheck, troopsCheck = False, False, False

        flag = 0
        if player.card.continent is True:
            for continent in range(len(player.card.totalContinents)):
                if player.card.totalContinents[continent] == 1:
                    for terr in self.map.getTerritoriesFromContinent(str(continent)):
                        if terr.ownedByPlayer != player:
                            flag = 1
                            break
            if flag == 0:
                continentCheck = True

        if player.card.territories is True:
            if len(self.map.getTerritoriesFromPlayer(player)) >= math.ceil(player.card.territoriesPercentage * len(self.map.territories)):
                territoriesCheck = True

        flag = 0
        if player.card.troops is True:
            for terr in self.map.getTerritoriesFromPlayer(player):
                if terr.numberOfTroops < player.card.troopsInTerritories:
                    flag = 1
                    break

            if flag == 0:
                troopsCheck = True

        if player.card.continent == continentCheck and player.card.territories == territoriesCheck and player.card.troops == troopsCheck:
            return True

    def checkIfGameOver(self):
        if self.parameters.goalBasedOn == "cards":
            for player in self.listOfPlayers:
                if self.checkGoal(player):
                    self.gamePhase = GamePhase.GAME_OVER
        elif self.parameters.goalBasedOn == "all":
            for player in self.listOfPlayers:
                if len(self.map.getTerritoriesFromPlayer(player)) == len(self.map.territories):
                    self.gamePhase = GamePhase.GAME_OVER

    def passTurn(self):
        if self.gamePhase == GamePhase.CONFLICT_PHASE:
            self.turnCount += 1
        self.playerTurnCount += 1
        self.currentPlayerNumber = self.playerTurnCount % len(self.listOfPlayers)
        self.currentPlayer = self.listOfPlayers[self.currentPlayerNumber]
        self.checkGamePhase()

        self.troopsToAddPickPhase = self.calculateNumberOfTroops(self.currentPlayer)
        self.troopsToAddContinentPhase = self.troopsFromContinentsOwnedByPlayer(self.currentPlayer.playerID)

    def checkGamePhase(self):
        if len(self.map.neutralTerritories) == 0:
            self.gamePhase = GamePhase.CONFLICT_PHASE
            self.turnPhase = TurnPhase.EXCHANGE_CARDS
            self.addUnitsPhase = AddUnitsPhase.CONTINENT_PHASE

        self.checkIfGameOver()

        return self.gamePhase

    def passTurnPhase(self):
        if self.gamePhase == GamePhase.ALLOCATION_PHASE:
            self.passTurn()
            return
        if self.turnPhase == TurnPhase.EXCHANGE_CARDS:
            self.turnPhase = TurnPhase.ADD_UNITS
            self.addUnitsPhase = AddUnitsPhase.CONTINENT_PHASE
            return
        if self.turnPhase == TurnPhase.ADD_UNITS:
            if self.addUnitsPhase == AddUnitsPhase.CONTINENT_PHASE:
                self.addUnitsPhase = AddUnitsPhase.TERRITORY_PHASE
                return
            if self.addUnitsPhase == AddUnitsPhase.TERRITORY_PHASE:
                self.addUnitsPhase = AddUnitsPhase.PICK_PHASE
                return
            if self.addUnitsPhase == AddUnitsPhase.PICK_PHASE:
                self.turnPhase = TurnPhase.ATTACK_ENEMY
                return
        if self.turnPhase == TurnPhase.ATTACK_ENEMY:
            self.turnPhase = TurnPhase.MOVE_UNITS
            return
        if self.turnPhase == TurnPhase.MOVE_UNITS:
            self.turnPhase = TurnPhase.EXCHANGE_CARDS
            self.passTurn()
            return

    def takeAction(self, action):
        if isinstance(action, Action.PassTurn):
            self.passTurnPhase()
            return

        if self.gamePhase == GamePhase.ALLOCATION_PHASE:
            assert isinstance(action, Action.AllocationAction)

            self.map.captureNeutralTerritory(self.map.territories[action.territoryidToConquer], action.playerID)
            self.passTurn()

            return

        if self.turnPhase == TurnPhase.EXCHANGE_CARDS:
            assert isinstance(action, Action.AddUnitsInExchangeCardsAction)
            self.currentPlayer.cards.remove(action.cardsToExchange[0])
            self.currentPlayer.cards.remove(action.cardsToExchange[1])
            self.currentPlayer.cards.remove(action.cardsToExchange[2])

            self.terrDeck.deck.extend(action.cardsToExchange)

            self.troopsToAddPickPhase += self.troopsPerCard[self.currentChange]
            self.currentChange += 1

            self.passTurnPhase()
            return

        if self.turnPhase == TurnPhase.ADD_UNITS:
            assert isinstance(action, Action.AddUnitsInConflictAction)
            self.map.territories[action.territoryidToAdd].addTroops(1)

            if self.addUnitsPhase == AddUnitsPhase.CONTINENT_PHASE:
                self.troopsToAddContinentPhase -= 1
                if self.troopsToAddContinentPhase[self.map.__findContinentByTerritory(action.territoryidToAdd)] <= 0 and sum(self.troopsToAddContinentPhase) <= 0:
                    self.passTurnPhase()
                return

            if self.addUnitsPhase == AddUnitsPhase.TERRITORY_PHASE:
                if self.territoryToAddTroops is not None:
                    self.troopsToAddTerritoryPhase -= 1
                    if self.troopsToAddTerritoryPhase <= 0:
                        self.territoryToAddTroops = None
                        self.troopsToAddTerritoryPhase = 2
                        self.passTurnPhase()
                    return

            if self.addUnitsPhase == AddUnitsPhase.PICK_PHASE:
                self.troopsToAddPickPhase -= 1
                if self.troopsToAddPickPhase <= 0:
                    self.passTurnPhase()
                return

        if self.turnPhase == TurnPhase.ATTACK_ENEMY:
            assert isinstance(action, Action.AttackWithUnitsInConflictAction)

            territoryidAttacking = action.territoryidAttacking
            territoryidDefending = action.territoryidDefending
            combatResult = self.rollDicesAndCompare(self.map.territories[territoryidAttacking].numberOfTroops - 1, self.map.territories[territoryidDefending].numberOfTroops)

            self.map.territories[territoryidAttacking].removeTroops(combatResult[1])
            self.map.territories[territoryidDefending].removeTroops(combatResult[0])

            if self.map.territories[territoryidDefending].numberOfTroops <= 0:
                if self.parameters.troopsToNewTerritory == "min":
                    self.map.territories[territoryidAttacking].removeTroops(combatResult[0])
                    self.map.territories[territoryidDefending].setTroops(combatResult[0])
                elif self.parameters.troopsToNewTerritory == "max":
                    self.map.territories[territoryidAttacking].removeTroops(self.map.territories[territoryidAttacking].numberOfTroops - 1)
                    self.map.territories[territoryidDefending].setTroops(self.map.territories[territoryidAttacking].numberOfTroops - 1)
                self.map.territories[territoryidDefending].ownedByPlayer = self.currentPlayer
                self.currentPlayer.terrCards.append(random.choice(self.terrDeck.deck))

                self.checkIfGameOver()

            return

        if self.turnPhase == TurnPhase.MOVE_UNITS:
            assert isinstance(action, Action.MoveUnitsInConflictAction)

            territoryidFrom = action.territoryidFrom
            territoryidTo = action.territoryidTo
            self.map.territories[territoryidFrom].removeTroops(1)
            self.map.territories[territoryidTo].addTroops(1)

            return

    def rollDicesAndCompare(self, numberOfAttackUnits, numberOfDefenseUnits):
        dicesDefense = 0
        if self.parameters.advantageAttack == "attack":
            dicesDefense = 2
        elif self.parameters.advantageAttack == "defense":
            dicesDefense = 3

        random.seed(time.time())
        listReturn = [0, 0]
        attackingUnitsValue = []
        defenseUnitsValue = []

        for _ in range(min(numberOfAttackUnits, 3)):
            attackingUnitsValue.append(random.randint(0, 5))
        for _ in range(min(numberOfDefenseUnits, dicesDefense)):
            defenseUnitsValue.append(random.randint(0, 5))

        attackingUnitsValue.sort(reverse=True)
        defenseUnitsValue.sort(reverse=True)

        for i in range(min(len(attackingUnitsValue), len(defenseUnitsValue))):
            if defenseUnitsValue[i] > attackingUnitsValue[i]:
                listReturn[1] += 1
            else:
                listReturn[0] += 1

        return listReturn

    def troopsFromContinentsOwnedByPlayer(self, playerID):
        continentList = self.continentHandler.checkContinentsForPlayer(playerID)
        troopsPerContinent = [0 for _ in range(len(continentList))]

        for continent in continentList:
            troopsPerContinent.insert(continent, self.map.continentsValue[continent])

        return troopsPerContinent

    def calculateNumberOfTroops(self, playerID):
        numberOfTerritories = len(self.map.getTerritoriesFromPlayer(playerID))

        if self.turnCount > 0:
            troopsFromContinents = sum(self.troopsFromContinentsOwnedByPlayer(playerID))
        else:
            troopsFromContinents = 0

        return troopsFromContinents + max(3, math.ceil(numberOfTerritories / self.parameters.troopsWonBeginTurn))

    def continentToAdd(self, playerID):
        if sum(self.troopsToAddContinentPhase) > 0:
            for continent in range(len(self.troopsToAddContinentPhase)):
                if self.troopsToAddContinentPhase[continent] > 0:
                    return continent

    def territoryToAdd(self, playerID):
        return self.territoryToAddTroops

    def __eq__(self, o):
        for terrId in range(len(self.map.territories)):
            if self.map.territories[terrId].ownedByPlayer != o.map.territory[terrId].ownedByPlayer:
                return False
        return True
