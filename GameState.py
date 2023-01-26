from Structures.GamePhase import GamePhase
from Structures.TurnPhase import TurnPhase
from Structures.Cards import TerritoryCards
from Map import Map

import random
import numpy as np


class GameState:
    def __init__(self, listOfPlayers, parameters):
        self.listOfPlayers = listOfPlayers
        self.parameters = parameters
        self.map = Map(parameters.mapPath)

        self.gamePhase = GamePhase.ALLOCATION_PHASE
        self.turnPhase = TurnPhase.ADD_UNITS
        self.turnCount = 0

        self.terrDeck = TerritoryCards(self.map)
        self.troopsPerCard = [2, 4, 6, 8, 10, 12, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 75, 80, 85, 90, 95, 100]
        self.currentChange = 0

    def takeAction(self, action):
        pass

