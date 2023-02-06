from Structures.PlayerID import PlayerID
from Structures.ValidPlayerColors import ValidPlayerColors
from Agents.RuleAgent import RuleAgent
from Parameters import Parameters
from Heuristics import Heuristic
from GameState import GameState
from Metrics import Metrics
from Structures.Cards import ObjectiveCards
from Structures.GamePhase import GamePhase
from Structures.TurnPhase import TurnPhase
from Structures.AddUnitsPhase import AddUnitsPhase
import Action

from time import time
import random


class Game:
    """
    Implementa um jogo com parâmetros, jogadores e regras.
    """

    def __init__(self, showActions, parameters, listOfPlayers):
        self.showActions   = showActions
        self.parameters    = parameters
        self.gameState     = GameState(listOfPlayers=listOfPlayers, parameters=parameters)
        self.listOfPlayers = listOfPlayers
        self.heuristic     = Heuristic()

    def getMoveChoicesAddUnits(self, playerID):
        friendTerritories = len(self.gameState.map.getTerritoriesFromPlayer(playerID))
        totalUnits = self.gameState.calculateNumberOfTroops(playerID)

        return friendTerritories * totalUnits

    def getMoveChoicesAttack(self, playerID):
        actions = 0
        friendTerritories = self.gameState.map.getTerritoriesFromPlayer(playerID)

        for terr in friendTerritories:
            if terr.numberOfTroops > 1:
                enemyTerritories = self.gameState.map.getEnemyFrontiersForTerritory(terr)
                if terr.numberOfTroops >= 4:
                    actions += len(enemyTerritories) * 3
                elif terr.numberOfTroops == 3:
                    actions += len(enemyTerritories) * 2
                elif terr.numberOfTroops == 2:
                    actions += len(enemyTerritories) * 1

        return actions

    def getMoveChoicesMoveUnits(self, playerID):
        friendTerritories = self.gameState.map.getTerritoriesFromPlayer(playerID)
        moves = 0

        for terr in friendTerritories:
            if terr.numberOfTroops > 1:
                if self.gameState.map.getFriendFrontiersForTerritory(terr) is not None:
                    moves += (terr.numberOfTroops - 1) * len(self.gameState.map.getFriendFrontiersForTerritory(terr))

        return moves

    def playtest(self, maxNumberOfTurns=300, maxNumberOfSeconds=20):
        metrics = Metrics()

        lastTurn = 0
        tieFlag = 0

        moveChoicesP1Attack = 0
        moveChoicesP2Attack = 0

        moveChoicesP1AddUnits = 0
        moveChoicesP2AddUnits = 0

        moveChoicesP1MoveUnits = 0
        moveChoicesP2MoveUnits = 0

        beginTime = time()

        if self.parameters.goalBasedOn == "cards":
            objectiveDeck = ObjectiveCards(self.gameState.map)

            self.listOfPlayers[0].objective = random.choice(objectiveDeck.deck)
            objectiveDeck.deck.remove(self.listOfPlayers[0].objective)
            self.listOfPlayers[1].objective = random.choice(objectiveDeck.deck)

        while self.gameState.gamePhase != GamePhase.GAME_OVER:
            if self.showActions:
                self.gameState.map.showMap()

            if self.gameState.currentPlayer == self.listOfPlayers[0]:
                player = self.listOfPlayers[0]
            elif self.gameState.currentPlayer == self.listOfPlayers[1]:
                player = self.listOfPlayers[1]

            if self.gameState.gamePhase == GamePhase.ALLOCATION_PHASE:
                self.playAllocationPhase(player)
            elif self.gameState.gamePhase == GamePhase.CONFLICT_PHASE:
                self.playConflictPhase(player)

            moveChoicesP1AddUnits, moveChoicesP2AddUnits, moveChoicesP1Attack, moveChoicesP2Attack, moveChoicesP1MoveUnits, moveChoicesP2MoveUnits = self.extractMetrics(player, moveChoicesP1AddUnits, moveChoicesP2AddUnits, moveChoicesP1Attack, moveChoicesP2Attack, moveChoicesP1MoveUnits, moveChoicesP2MoveUnits)

            if lastTurn != self.gameState.turnCount:
                heuristicResult = self.heuristic.heuristicFromGameState(self.gameState)

                totalP1 = moveChoicesP1AddUnits + moveChoicesP1Attack + moveChoicesP1MoveUnits
                totalP2 = moveChoicesP2AddUnits + moveChoicesP2Attack + moveChoicesP2MoveUnits

                metrics.addTurn((heuristicResult[0][1], heuristicResult[1][1], totalP1, totalP2))

                lastTurn = self.gameState.turnCount

                moveChoicesP1AddUnits, moveChoicesP2AddUnits = 0, 0
                moveChoicesP1Attack, moveChoicesP2Attack = 0, 0
                moveChoicesP1MoveUnits, moveChoicesP2MoveUnits = 0, 0

                if self.showActions:
                    print("turn: " + str(self.gameState.turnCount))
                    print()
                    print(heuristicResult[0][0].playerID.playerName + ": " + str(heuristicResult[0][1]))
                    print(heuristicResult[1][0].playerID.playerName + ": " + str(heuristicResult[1][1]))
                    print(heuristicResult[0][0].playerID.playerName + ": " + str(totalP1))
                    print(heuristicResult[1][0].playerID.playerName + ": " + str(totalP2))
                    print()

            if self.gameState.turnCount > maxNumberOfTurns or (time() - beginTime) > maxNumberOfSeconds:
                tieFlag = 1
                break

        heuristicResult = self.heuristic.heuristicFromGameState(self.gameState)

        winner = None
        if tieFlag or (self.gameState.checkGoal(self.gameState.listOfPlayers[0]) == False and self.gameState.checkGoal(self.gameState.listOfPlayers[1]) == False):
            winner = -1
        else:
            if heuristicResult[0][1] > heuristicResult[1][1]:
                winner = 0
            else:
                winner = 1

        metrics.endGame((heuristicResult[0][1], heuristicResult[1][1], 0, 0), winner)

        if self.showActions:
            print(heuristicResult[0][0].playerID.playerName + ": " + str(heuristicResult[0][1]))
            print(heuristicResult[1][0].playerID.playerName + ": " + str(heuristicResult[1][1]))

        return metrics

    def extractMetrics(self, player, moveChoicesP1AddUnits, moveChoicesP2AddUnits, moveChoicesP1Attack, moveChoicesP2Attack, moveChoicesP1MoveUnits, moveChoicesP2MoveUnits):
        if self.gameState.turnPhase == TurnPhase.ADD_UNITS and self.gameState.gamePhase == GamePhase.CONFLICT_PHASE:
            if player.playerID == self.listOfPlayers[0].playerID:
                moveChoicesP1AddUnits += self.getMoveChoicesAddUnits(player.playerID)
            else:
                moveChoicesP2AddUnits += self.getMoveChoicesAddUnits(player.playerID)
        elif self.gameState.turnPhase == TurnPhase.ATTACK_ENEMY:
            if player.playerID == self.listOfPlayers[0].playerID:
                moveChoicesP1Attack += self.getMoveChoicesAttack(player.playerID)
            else:
                moveChoicesP2Attack += self.getMoveChoicesAttack(player.playerID)
        elif self.gameState.turnPhase == TurnPhase.MOVE_UNITS:
            if player.playerID == self.listOfPlayers[0].playerID:
                moveChoicesP1MoveUnits += self.getMoveChoicesMoveUnits(player.playerID)
            else:
                moveChoicesP2MoveUnits += self.getMoveChoicesMoveUnits(player.playerID)

        return moveChoicesP1AddUnits, moveChoicesP2AddUnits, moveChoicesP1Attack, moveChoicesP2Attack, moveChoicesP1MoveUnits, moveChoicesP2MoveUnits

    def playAllocationPhase(self, player):
        action = None

        if self.parameters.initialTerritoriesMode == "random":
            territoryChosen = random.choice(self.gameState.map.neutralTerritories)
            action = Action.AllocationAction(territoryChosen.territoryId, player.playerID)
        elif self.parameters.initialTerritoriesMode == "pick":
            action = player.playAllocation(self.gameState)

        self.gameState.takeAction(action)

    def playConflictPhase(self, player):
        action = None

        if self.gameState.turnPhase == TurnPhase.EXCHANGE_CARDS:
            action = self.exchangeCardsPhase(player)
        elif self.gameState.turnPhase == TurnPhase.ADD_UNITS:
            action = self.addUnitsPhase(player)
        elif self.gameState.turnPhase == TurnPhase.ATTACK_ENEMY:
            action = self.attackPhase(player)
        elif self.gameState.turnPhase == TurnPhase.MOVE_UNITS:
            action = self.moveUnitsPhase(player)

        self.gameState.takeAction(action)

    def exchangeCardsPhase(self, player):
        action = None

        if 3 <= len(player.cards) <= 5:
            action = player.playExchangeCards(self.gameState)

        if action is None:
            action = Action.PassTurn()

        return action

    def addUnitsPhase(self, player):
        action = None

        if self.gameState.addUnitsPhase == AddUnitsPhase.CONTINENT_PHASE:
            if self.gameState.hasContinentTroopsToAdd(player.playerID):
                action = player.addUnitsInContinent(self.gameState, self.gameState.continentToAdd(player.playerID))
        elif self.gameState.addUnitsPhase == AddUnitsPhase.TERRITORY_PHASE:
            if self.gameState.hasTerritoryTroopsToAdd(player.playerID):
                action = player.addUnitsInTerritory(self.gameState, self.gameState.territoryToAdd(player.playerID))
        elif self.gameState.addUnitsPhase == AddUnitsPhase.PICK_PHASE:
            action = player.playAddUnits(self.gameState)

        if action is None:
            action = Action.PassTurn()

        return action

    def attackPhase(self, player):
        action = player.playAttack(self.gameState)
        return action

    def moveUnitsPhase(self, player):
        action = player.playMoveUnits(self.gameState)
        return action


if __name__ == "__main__":
    agent1 = RuleAgent(PlayerID("Player1", ValidPlayerColors.BLUE))
    agent2 = RuleAgent(PlayerID("Player2", ValidPlayerColors.RED))

    """
    To test:
    
    game = Game(showActions=True, parameters=Parameters("C:/Users/LanaR/PycharmProjects/Risk-Generation/parameters/map.json", "all", 1, "defense", "random", "max"), listOfPlayers=[agent1, agent2])
    game = Game(showActions=True, parameters=Parameters("C:/Users/LanaR/PycharmProjects/Risk-Generation/parameters/map.json", "all", 1, "defense", "random", "min"), listOfPlayers=[agent1, agent2])
    game = Game(showActions=True, parameters=Parameters("C:/Users/LanaR/PycharmProjects/Risk-Generation/parameters/map.json", "all", 1, "defense", "pick", "max"), listOfPlayers=[agent1, agent2])
    game = Game(showActions=True, parameters=Parameters("C:/Users/LanaR/PycharmProjects/Risk-Generation/parameters/map.json", "all", 1, "defense", "pick", "min"), listOfPlayers=[agent1, agent2])
    game = Game(showActions=True, parameters=Parameters("C:/Users/LanaR/PycharmProjects/Risk-Generation/parameters/map.json", "all", 1, "attack", "random", "max"), listOfPlayers=[agent1, agent2])
    game = Game(showActions=True, parameters=Parameters("C:/Users/LanaR/PycharmProjects/Risk-Generation/parameters/map.json", "all", 1, "attack", "random", "min"), listOfPlayers=[agent1, agent2])
    game = Game(showActions=True, parameters=Parameters("C:/Users/LanaR/PycharmProjects/Risk-Generation/parameters/map.json", "all", 1, "attack", "pick", "max"), listOfPlayers=[agent1, agent2])
    game = Game(showActions=True, parameters=Parameters("C:/Users/LanaR/PycharmProjects/Risk-Generation/parameters/map.json", "all", 1, "attack", "pick", "min"), listOfPlayers=[agent1, agent2])
    game = Game(showActions=True, parameters=Parameters("C:/Users/LanaR/PycharmProjects/Risk-Generation/parameters/map.json", "all", 2, "defense", "random", "max"), listOfPlayers=[agent1, agent2])
    game = Game(showActions=True, parameters=Parameters("C:/Users/LanaR/PycharmProjects/Risk-Generation/parameters/map.json", "all", 2, "defense", "random", "min"), listOfPlayers=[agent1, agent2])
    game = Game(showActions=True, parameters=Parameters("C:/Users/LanaR/PycharmProjects/Risk-Generation/parameters/map.json", "all", 2, "defense", "pick", "max"), listOfPlayers=[agent1, agent2])
    game = Game(showActions=True, parameters=Parameters("C:/Users/LanaR/PycharmProjects/Risk-Generation/parameters/map.json", "all", 2, "defense", "pick", "min"), listOfPlayers=[agent1, agent2])
    game = Game(showActions=True, parameters=Parameters("C:/Users/LanaR/PycharmProjects/Risk-Generation/parameters/map.json", "all", 2, "attack", "random", "max"), listOfPlayers=[agent1, agent2])
    game = Game(showActions=True, parameters=Parameters("C:/Users/LanaR/PycharmProjects/Risk-Generation/parameters/map.json", "all", 2, "attack", "random", "min"), listOfPlayers=[agent1, agent2])
    game = Game(showActions=True, parameters=Parameters("C:/Users/LanaR/PycharmProjects/Risk-Generation/parameters/map.json", "all", 2, "attack", "pick", "max"), listOfPlayers=[agent1, agent2])
    game = Game(showActions=True, parameters=Parameters("C:/Users/LanaR/PycharmProjects/Risk-Generation/parameters/map.json", "all", 2, "attack", "pick", "min"), listOfPlayers=[agent1, agent2])
    game = Game(showActions=True, parameters=Parameters("C:/Users/LanaR/PycharmProjects/Risk-Generation/parameters/map.json", "all", 3, "defense", "random", "max"), listOfPlayers=[agent1, agent2])
    game = Game(showActions=True, parameters=Parameters("C:/Users/LanaR/PycharmProjects/Risk-Generation/parameters/map.json", "all", 3, "defense", "random", "min"), listOfPlayers=[agent1, agent2])
    game = Game(showActions=True, parameters=Parameters("C:/Users/LanaR/PycharmProjects/Risk-Generation/parameters/map.json", "all", 3, "defense", "pick", "max"), listOfPlayers=[agent1, agent2])
    game = Game(showActions=True, parameters=Parameters("C:/Users/LanaR/PycharmProjects/Risk-Generation/parameters/map.json", "all", 3, "defense", "pick", "min"), listOfPlayers=[agent1, agent2])
    game = Game(showActions=True, parameters=Parameters("C:/Users/LanaR/PycharmProjects/Risk-Generation/parameters/map.json", "all", 3, "attack", "random", "max"), listOfPlayers=[agent1, agent2])
    game = Game(showActions=True, parameters=Parameters("C:/Users/LanaR/PycharmProjects/Risk-Generation/parameters/map.json", "all", 3, "attack", "random", "min"), listOfPlayers=[agent1, agent2])
    game = Game(showActions=True, parameters=Parameters("C:/Users/LanaR/PycharmProjects/Risk-Generation/parameters/map.json", "all", 3, "attack", "pick", "max"), listOfPlayers=[agent1, agent2])
    game = Game(showActions=True, parameters=Parameters("C:/Users/LanaR/PycharmProjects/Risk-Generation/parameters/map.json", "all", 3, "attack", "pick", "min"), listOfPlayers=[agent1, agent2])
    game = Game(showActions=True, parameters=Parameters("C:/Users/LanaR/PycharmProjects/Risk-Generation/parameters/map.json", "all", 4, "defense", "random", "max"), listOfPlayers=[agent1, agent2])
    game = Game(showActions=True, parameters=Parameters("C:/Users/LanaR/PycharmProjects/Risk-Generation/parameters/map.json", "all", 4, "defense", "random", "min"), listOfPlayers=[agent1, agent2])
    game = Game(showActions=True, parameters=Parameters("C:/Users/LanaR/PycharmProjects/Risk-Generation/parameters/map.json", "all", 4, "defense", "pick", "max"), listOfPlayers=[agent1, agent2])
    game = Game(showActions=True, parameters=Parameters("C:/Users/LanaR/PycharmProjects/Risk-Generation/parameters/map.json", "all", 4, "defense", "pick", "min"), listOfPlayers=[agent1, agent2])
    game = Game(showActions=True, parameters=Parameters("C:/Users/LanaR/PycharmProjects/Risk-Generation/parameters/map.json", "all", 4, "attack", "random", "max"), listOfPlayers=[agent1, agent2])
    game = Game(showActions=True, parameters=Parameters("C:/Users/LanaR/PycharmProjects/Risk-Generation/parameters/map.json", "all", 4, "attack", "random", "min"), listOfPlayers=[agent1, agent2])
    game = Game(showActions=True, parameters=Parameters("C:/Users/LanaR/PycharmProjects/Risk-Generation/parameters/map.json", "all", 4, "attack", "pick", "max"), listOfPlayers=[agent1, agent2])
    game = Game(showActions=True, parameters=Parameters("C:/Users/LanaR/PycharmProjects/Risk-Generation/parameters/map.json", "all", 4, "attack", "pick", "min"), listOfPlayers=[agent1, agent2])
    game = Game(showActions=True, parameters=Parameters("C:/Users/LanaR/PycharmProjects/Risk-Generation/parameters/map.json", "all", 5, "defense", "random", "max"), listOfPlayers=[agent1, agent2])
    game = Game(showActions=True, parameters=Parameters("C:/Users/LanaR/PycharmProjects/Risk-Generation/parameters/map.json", "all", 5, "defense", "random", "min"), listOfPlayers=[agent1, agent2])
    game = Game(showActions=True, parameters=Parameters("C:/Users/LanaR/PycharmProjects/Risk-Generation/parameters/map.json", "all", 5, "defense", "pick", "max"), listOfPlayers=[agent1, agent2])
    game = Game(showActions=True, parameters=Parameters("C:/Users/LanaR/PycharmProjects/Risk-Generation/parameters/map.json", "all", 5, "defense", "pick", "min"), listOfPlayers=[agent1, agent2])
    game = Game(showActions=True, parameters=Parameters("C:/Users/LanaR/PycharmProjects/Risk-Generation/parameters/map.json", "all", 5, "attack", "random", "max"), listOfPlayers=[agent1, agent2])
    game = Game(showActions=True, parameters=Parameters("C:/Users/LanaR/PycharmProjects/Risk-Generation/parameters/map.json", "all", 5, "attack", "random", "min"), listOfPlayers=[agent1, agent2])
    game = Game(showActions=True, parameters=Parameters("C:/Users/LanaR/PycharmProjects/Risk-Generation/parameters/map.json", "all", 5, "attack", "pick", "max"), listOfPlayers=[agent1, agent2])
    game = Game(showActions=True, parameters=Parameters("C:/Users/LanaR/PycharmProjects/Risk-Generation/parameters/map.json", "all", 5, "attack", "pick", "min"), listOfPlayers=[agent1, agent2])
    game = Game(showActions=True, parameters=Parameters("C:/Users/LanaR/PycharmProjects/Risk-Generation/parameters/map.json", "cards", 1, "defense", "random", "max"), listOfPlayers=[agent1, agent2])
    game = Game(showActions=True, parameters=Parameters("C:/Users/LanaR/PycharmProjects/Risk-Generation/parameters/map.json", "cards", 1, "defense", "random", "min"), listOfPlayers=[agent1, agent2])
    game = Game(showActions=True, parameters=Parameters("C:/Users/LanaR/PycharmProjects/Risk-Generation/parameters/map.json", "cards", 1, "defense", "pick", "max"), listOfPlayers=[agent1, agent2])
    game = Game(showActions=True, parameters=Parameters("C:/Users/LanaR/PycharmProjects/Risk-Generation/parameters/map.json", "cards", 1, "defense", "pick", "min"), listOfPlayers=[agent1, agent2])
    game = Game(showActions=True, parameters=Parameters("C:/Users/LanaR/PycharmProjects/Risk-Generation/parameters/map.json", "cards", 1, "attack", "random", "max"), listOfPlayers=[agent1, agent2])
    game = Game(showActions=True, parameters=Parameters("C:/Users/LanaR/PycharmProjects/Risk-Generation/parameters/map.json", "cards", 1, "attack", "random", "min"), listOfPlayers=[agent1, agent2])
    game = Game(showActions=True, parameters=Parameters("C:/Users/LanaR/PycharmProjects/Risk-Generation/parameters/map.json", "cards", 1, "attack", "pick", "max"), listOfPlayers=[agent1, agent2])
    game = Game(showActions=True, parameters=Parameters("C:/Users/LanaR/PycharmProjects/Risk-Generation/parameters/map.json", "cards", 1, "attack", "pick", "min"), listOfPlayers=[agent1, agent2])
    game = Game(showActions=True, parameters=Parameters("C:/Users/LanaR/PycharmProjects/Risk-Generation/parameters/map.json", "cards", 2, "defense", "random", "max"), listOfPlayers=[agent1, agent2])
    game = Game(showActions=True, parameters=Parameters("C:/Users/LanaR/PycharmProjects/Risk-Generation/parameters/map.json", "cards", 2, "defense", "random", "min"), listOfPlayers=[agent1, agent2])
    game = Game(showActions=True, parameters=Parameters("C:/Users/LanaR/PycharmProjects/Risk-Generation/parameters/map.json", "cards", 2, "defense", "pick", "max"), listOfPlayers=[agent1, agent2])
    game = Game(showActions=True, parameters=Parameters("C:/Users/LanaR/PycharmProjects/Risk-Generation/parameters/map.json", "cards", 2, "defense", "pick", "min"), listOfPlayers=[agent1, agent2])
    game = Game(showActions=True, parameters=Parameters("C:/Users/LanaR/PycharmProjects/Risk-Generation/parameters/map.json", "cards"", 2, "attack", "random", "max"), listOfPlayers=[agent1, agent2])
    game = Game(showActions=True, parameters=Parameters("C:/Users/LanaR/PycharmProjects/Risk-Generation/parameters/map.json", "cards", 2, "attack", "random", "min"), listOfPlayers=[agent1, agent2])
    game = Game(showActions=True, parameters=Parameters("C:/Users/LanaR/PycharmProjects/Risk-Generation/parameters/map.json", "cards", 2, "attack", "pick", "max"), listOfPlayers=[agent1, agent2])
    game = Game(showActions=True, parameters=Parameters("C:/Users/LanaR/PycharmProjects/Risk-Generation/parameters/map.json", "cards", 2, "attack", "pick", "min"), listOfPlayers=[agent1, agent2])
    game = Game(showActions=True, parameters=Parameters("C:/Users/LanaR/PycharmProjects/Risk-Generation/parameters/map.json", "cards", 3, "defense", "random", "max"), listOfPlayers=[agent1, agent2])
    game = Game(showActions=True, parameters=Parameters("C:/Users/LanaR/PycharmProjects/Risk-Generation/parameters/map.json", "cards", 3, "defense", "random", "min"), listOfPlayers=[agent1, agent2])
    game = Game(showActions=True, parameters=Parameters("C:/Users/LanaR/PycharmProjects/Risk-Generation/parameters/map.json", "cards", 3, "defense", "pick", "max"), listOfPlayers=[agent1, agent2])
    game = Game(showActions=True, parameters=Parameters("C:/Users/LanaR/PycharmProjects/Risk-Generation/parameters/map.json", "cards", 3, "defense", "pick", "min"), listOfPlayers=[agent1, agent2])
    game = Game(showActions=True, parameters=Parameters("C:/Users/LanaR/PycharmProjects/Risk-Generation/parameters/map.json", "cards", 3, "attack", "random", "max"), listOfPlayers=[agent1, agent2])
    game = Game(showActions=True, parameters=Parameters("C:/Users/LanaR/PycharmProjects/Risk-Generation/parameters/map.json", "cards", 3, "attack", "random", "min"), listOfPlayers=[agent1, agent2])
    game = Game(showActions=True, parameters=Parameters("C:/Users/LanaR/PycharmProjects/Risk-Generation/parameters/map.json", "cards", 3, "attack", "pick", "max"), listOfPlayers=[agent1, agent2])
    game = Game(showActions=True, parameters=Parameters("C:/Users/LanaR/PycharmProjects/Risk-Generation/parameters/map.json", "cards", 3, "attack", "pick", "min"), listOfPlayers=[agent1, agent2])
    game = Game(showActions=True, parameters=Parameters("C:/Users/LanaR/PycharmProjects/Risk-Generation/parameters/map.json", "cards", 4, "defense", "random", "max"), listOfPlayers=[agent1, agent2])
    game = Game(showActions=True, parameters=Parameters("C:/Users/LanaR/PycharmProjects/Risk-Generation/parameters/map.json", "cards", 4, "defense", "random", "min"), listOfPlayers=[agent1, agent2])
    game = Game(showActions=True, parameters=Parameters("C:/Users/LanaR/PycharmProjects/Risk-Generation/parameters/map.json", "cards", 4, "defense", "pick", "max"), listOfPlayers=[agent1, agent2])
    game = Game(showActions=True, parameters=Parameters("C:/Users/LanaR/PycharmProjects/Risk-Generation/parameters/map.json", "cards", 4, "defense", "pick", "min"), listOfPlayers=[agent1, agent2])
    game = Game(showActions=True, parameters=Parameters("C:/Users/LanaR/PycharmProjects/Risk-Generation/parameters/map.json", "cards", 4, "attack", "random", "max"), listOfPlayers=[agent1, agent2])
    game = Game(showActions=True, parameters=Parameters("C:/Users/LanaR/PycharmProjects/Risk-Generation/parameters/map.json", "cards", 4, "attack", "random", "min"), listOfPlayers=[agent1, agent2])
    game = Game(showActions=True, parameters=Parameters("C:/Users/LanaR/PycharmProjects/Risk-Generation/parameters/map.json", "cards", 4, "attack", "pick", "max"), listOfPlayers=[agent1, agent2])
    game = Game(showActions=True, parameters=Parameters("C:/Users/LanaR/PycharmProjects/Risk-Generation/parameters/map.json", "cards", 4, "attack", "pick", "min"), listOfPlayers=[agent1, agent2])
    game = Game(showActions=True, parameters=Parameters("C:/Users/LanaR/PycharmProjects/Risk-Generation/parameters/map.json", "cards", 5, "defense", "random", "max"), listOfPlayers=[agent1, agent2])
    game = Game(showActions=True, parameters=Parameters("C:/Users/LanaR/PycharmProjects/Risk-Generation/parameters/map.json", "cards", 5, "defense", "random", "min"), listOfPlayers=[agent1, agent2])
    game = Game(showActions=True, parameters=Parameters("C:/Users/LanaR/PycharmProjects/Risk-Generation/parameters/map.json", "cards", 5, "defense", "pick", "max"), listOfPlayers=[agent1, agent2])
    game = Game(showActions=True, parameters=Parameters("C:/Users/LanaR/PycharmProjects/Risk-Generation/parameters/map.json", "cards", 5, "defense", "pick", "min"), listOfPlayers=[agent1, agent2])
    game = Game(showActions=True, parameters=Parameters("C:/Users/LanaR/PycharmProjects/Risk-Generation/parameters/map.json", "cards", 5, "attack", "random", "max"), listOfPlayers=[agent1, agent2])
    game = Game(showActions=True, parameters=Parameters("C:/Users/LanaR/PycharmProjects/Risk-Generation/parameters/map.json", "cards", 5, "attack", "random", "min"), listOfPlayers=[agent1, agent2])
    game = Game(showActions=True, parameters=Parameters("C:/Users/LanaR/PycharmProjects/Risk-Generation/parameters/map.json", "cards", 5, "attack", "pick", "max"), listOfPlayers=[agent1, agent2])
    game = Game(showActions=True, parameters=Parameters("C:/Users/LanaR/PycharmProjects/Risk-Generation/parameters/map.json", "cards", 5, "attack", "pick", "min"), listOfPlayers=[agent1, agent2])    
    """

    game = Game(showActions=False, parameters=Parameters("/home/lana/PycharmProjects/Risk-Generation/parameters/map.json", "cards", 3, "attack", "pick", "min"), listOfPlayers=[agent1, agent2])

    game.playtest().printMetrics()
