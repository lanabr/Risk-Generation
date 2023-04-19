import Action


class HumanPlayer:
    def __init__(self, playerID):
        self.playerID = playerID
        self.cards = []

    def playAllocation(self, gameState):
        gameMap = gameState.map

        print("Escolha um terriorio para colocar um exército, territórios disponíveis: ")

        territories = []

        for territory in gameMap.neutralTerritories:
            territories.append(territory.territoryId)
            print(territory.territoryId, end=" ")

        print()

        territoryChosen = input("Território escolhido: ")

        while int(territoryChosen) not in territories:
            print("Território já escolhido, tente novamente")

            territoryChosen = input("Território escolhido: ")

        action = Action.AllocationAction(int(territoryChosen), self.playerID)

        return action

    def playAddUnits(self, gameState):
        gameMap = gameState.map
        territories = []

        print("Você tem " + str(gameState.troopsToAddPickPhase) + " tropas para distribuir. Escolha um território para colocar um exército, territórios disponíveis: ")

        for territory in gameMap.territories:
            if territory.ownedByPlayer == self.playerID:
                print(territory.territoryId, end=" ")
                territories.append(territory.territoryId)

        print()

        territoryChosen = input("Território escolhido: ")

        while int(territoryChosen) not in territories:
            print("Este território não é seu, tente novamente")

            territoryChosen = input("Território escolhido: ")

        action = Action.AddUnitsInConflictAction(int(territoryChosen))

        return action

    def addUnitsInContinent(self, gameState, continent):
        gameMap = gameState.map
        territories = []

        print("Você tem " + str(gameState.troopsToAddContinentPhase[int(continent)]) + " tropas para distribuir no continente " + continent + ". Escolha um território para colocar um exército, territórios disponíveis: ")

        for territory in gameMap.territories:
            if territory.ownedByPlayer == self.playerID and territory.continent == continent:
                print(territory.territoryId, end=" ")
                territories.append(territory.territoryId)

        print()

        territoryChosen = input("Território escolhido: ")

        while int(territoryChosen) not in territories:
            print("Este território não está no continente especificado, tente novamente")

            territoryChosen = input("Território escolhido: ")

        action = Action.AddUnitsInConflictAction(int(territoryChosen))

        return action

    def addUnitsInTerritory(self, gameState, territory):

        print("Você tem " + gameState.troopsToAddTerritoryPhase + " tropas para distribuir no território" + str(territory) + ". Elas serão colocadas automaticamente.")

        action = Action.AddUnitsInConflictAction(territory)

        return action

    def playExchangeCards(self, gameState):
        print("Você tem " + str(gameState.cards) + " cartas para trocar. Escolha 3 cartas para trocar, cartas disponíveis: ")

        for card in self.cards:
            print("Carta 0: ", card.territory, card.design, end=" ")

        print("Se não deseja trocar cartas, digite 0 0 0")

        indexes = [input("Cartas escolhidas <n1 n2 n3>: ").split()]

        while indexes[0] != "0" and indexes[1] != "0" and indexes[2] != "0":
            action = Action.PassTurn()
            return action

        action = Action.AddUnitsInExchangeCardsAction([self.cards[int(indexes[0])], self.cards[int(indexes[1])], self.cards[int(indexes[2])]])

        return action

    def playAttack(self, gameState):
        gameMap = gameState.map

        print("Escolha um território para atacar e um território para ser atacado, territórios disponíveis: ")

        for territory in gameMap.territories:
            if territory.ownedByPlayer == self.playerID:
                print(str(territory.territoryId) + " ->", end=" ")
                for terr in gameMap._connections[str(territory.territoryId)]:
                    print(str(terr), end=" ")

                print()

        print()

        print("Caso não queira atacar, digite 0 0")

        territoryA, territoryD = input("Territórios escolhidos <ataque defesa>: ").split()

        if territoryA == "0" and territoryD == "0":
            action = Action.PassTurn()
            return action

        action = Action.AttackWithUnitsInConflictAction(int(territoryA), int(territoryD))

        return action

    def playMoveUnits(self, gameState):
        gameMap = gameState.map

        print("Escolha um território para mover os exércitos e um território para receber os exércitos, territórios disponíveis: ")

        for territory in gameMap.territories:
            if territory.ownedByPlayer == self.playerID:
                print(str(territory.territoryId) + " ->", end=" ")
                for terr in gameMap._connections[str(territory.territoryId)]:
                    print(str(terr), end=" ")

                print()

        print()

        print("Caso não queira mover exércitos, digite 0 0")

        territoryA, territoryD = input("Territórios escolhidos <origem destino>: ").split()

        if territoryA == "0" and territoryD == "0":
            action = Action.PassTurn()
            return action

        action = Action.MoveUnitsInConflictAction(int(territoryA), int(territoryD))
        return action
